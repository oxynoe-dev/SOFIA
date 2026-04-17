#!/usr/bin/env python3
"""analysis.py — Produce analysis JSON from SOFIA instances for analysis.html.

Usage:
    python analysis.py <instance-path> [<instance-path> ...] [--output <path>]

Accepts one or more instances. Produces a single analysis.json with:
- Per-instance data (friction, resolutions, flux, direction, signalerPattern)
- Aggregated totals across all instances
- Time series per instance and aggregated
- Artefact friction from shared/ (reviews, notes, any .md with H2A frontmatter)

Outputs analysis.json (consumed by analysis.html).

Zero external dependency — Python 3.10+ stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Import shared parsing from audit-instance.py
# ---------------------------------------------------------------------------

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
audit = importlib.import_module("audit-instance")

FRICTION_MARKERS = audit.FRICTION_MARKERS
FRICTION_BRACKET_ALIASES = audit.FRICTION_BRACKET_ALIASES
RESOLUTION_TAGS = audit.RESOLUTION_TAGS
RESOLUTION_ALIASES = audit.RESOLUTION_ALIASES


# ---------------------------------------------------------------------------
# Session parser
# ---------------------------------------------------------------------------

def parse_session_date(filepath: Path) -> str | None:
    """Extract date from session filename or frontmatter."""
    fm = audit.parse_frontmatter(filepath)
    if fm and "date" in fm:
        return fm["date"].strip()
    # Fallback: filename pattern YYYY-MM-DD-HHmm-persona.md
    m = re.match(r"(\d{4}-\d{2}-\d{2})", filepath.name)
    return m.group(1) if m else None


def date_to_week(d: str) -> str:
    """Convert YYYY-MM-DD to week label (YYYY-WNN)."""
    try:
        dt = date.fromisoformat(d)
        iso = dt.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"
    except (ValueError, AttributeError):
        return "unknown"


def parse_friction_lines(text: str) -> list[dict]:
    """Parse friction lines anywhere in the text.

    Scans all list items ('- ...') for friction markers (icon or [bracket])
    combined with an initiative tag ([PO] or [name]). Same parser for
    sessions, reviews, notes — a friction marker is a friction marker.
    """
    records = []

    for line in text.splitlines():
        stripped = line.strip()
        # Accept '- ✓ ...' (list item) or '✓ ...' (bare marker)
        if stripped.startswith("- "):
            item = stripped[2:].strip()
        else:
            item = stripped
        record = {"marker": None, "initiative": None, "resolution": None, "ref": None, "description": None}

        # Marker — icons
        for char, key in FRICTION_MARKERS.items():
            if char == "~":
                if item.startswith("~"):
                    record["marker"] = key
                    break
            elif char in item:
                record["marker"] = key
                break

        # Marker — brackets (FR and EN via aliases)
        if not record["marker"]:
            bracket_pattern = r"\[(" + "|".join(re.escape(k) for k in FRICTION_BRACKET_ALIASES) + r")\]"
            bracket_match = re.search(bracket_pattern, item)
            if bracket_match:
                tag = bracket_match.group(1)
                record["marker"] = FRICTION_BRACKET_ALIASES[tag]

        if not record["marker"]:
            continue

        # Initiative — require [PO] or — [name] to confirm it's a friction line
        if "[PO]" in item or "[po]" in item:
            record["initiative"] = "PO"
        elif re.search(r"—\s*\[(\w+)\]", item):
            record["initiative"] = "persona"
        else:
            continue

        # Resolution (FR and EN via aliases)
        res_match = re.search(r"→\s*(\w+)", item)
        if res_match:
            tag = audit.strip_accents(res_match.group(1).lower())
            if tag in RESOLUTION_ALIASES:
                record["resolution"] = RESOLUTION_ALIASES[tag]
            elif tag in RESOLUTION_TAGS:
                record["resolution"] = tag

        # Ref
        ref_match = re.search(r"\(ref:\s*([^)]+)\)", item)
        if ref_match:
            record["ref"] = ref_match.group(1).strip()

        # Description — strip marker, initiative, resolution to get the core text
        desc = re.sub(r"[✓~⚡◐✗]\s*", "", item)
        desc = re.sub(r"\[(juste|contestable|simplification|angle-mort|faux|sound|blind.spot|refuted)\]\s*", "", desc)
        desc = re.sub(r"\s*—\s*\[\w+\]\s*(→\s*\w+)?(\s*\(ref:[^)]+\))?", "", desc)
        record["description"] = desc.strip()[:120]  # cap at 120 chars

        records.append(record)

    return records


def parse_flux_lines(text: str) -> list[dict]:
    """Parse ## Flux lines into structured records."""
    lines = text.splitlines()
    in_section = False
    records = []

    for line in lines:
        if line.strip().startswith("## Flux"):
            in_section = True
            continue
        if in_section and line.strip().startswith("## "):
            break
        if not in_section:
            continue

        stripped = line.strip()
        if not stripped.startswith("- "):
            continue

        item = stripped[2:].strip()
        # Pattern: H:matiere — description or A:structure — description
        flux_match = re.match(r"([HA]):(\w+)", item)
        if flux_match:
            records.append({
                "direction": flux_match.group(1),
                "type": flux_match.group(2),
            })

    return records


def parse_signaler_pattern(text: str) -> dict | None:
    """Parse ## signalerPattern section."""
    lines = text.splitlines()
    in_section = False
    result = {"theme": None, "choix": None, "justification": None}

    for line in lines:
        if line.strip().startswith("## signalerPattern"):
            in_section = True
            continue
        if in_section and line.strip().startswith("## "):
            break
        if not in_section:
            continue

        stripped = line.strip()
        if stripped.startswith("- Theme"):
            m = re.search(r"Theme\s*:\s*(.+)", stripped)
            if m:
                result["theme"] = m.group(1).strip()
        elif stripped.startswith("- Choix"):
            m = re.search(r"Choix\s*:\s*(.+)", stripped)
            if m:
                result["choix"] = audit.strip_accents(m.group(1).strip().lower())
        elif stripped.startswith("- Justification"):
            m = re.search(r"Justification\s*:\s*(.+)", stripped)
            if m:
                result["justification"] = m.group(1).strip()

    if not in_section:
        return None
    return result


# ---------------------------------------------------------------------------
# Artefact discovery
# ---------------------------------------------------------------------------

def find_artefacts(instance_path: Path) -> list[Path]:
    """Find all .md files in shared/ that could contain friction markers."""
    shared = instance_path / "shared"
    if not shared.is_dir():
        return []

    artefacts = []
    skip_dirs = {"orga", "audits", "archives"}
    skip_prefixes = ("conventions", "roadmap", "naming", "inventaire")

    for md in sorted(shared.rglob("*.md")):
        rel_parts = md.relative_to(shared).parts
        if any(p in skip_dirs for p in rel_parts):
            continue
        if md.name.startswith(skip_prefixes):
            continue
        artefacts.append(md)

    return artefacts


def parse_artefact_date(filepath: Path) -> str | None:
    """Extract date from artefact frontmatter or filename."""
    fm = audit.parse_frontmatter(filepath)
    if fm and "date" in fm:
        return fm["date"].strip()
    # Fallback: date in filename
    m = re.search(r"(\d{4}-\d{2}-\d{2})", filepath.name)
    return m.group(1) if m else None


def parse_artefact_persona(filepath: Path) -> str | None:
    """Extract emitting persona from artefact frontmatter or filename."""
    fm = audit.parse_frontmatter(filepath)
    if fm and "de" in fm:
        return fm["de"].strip()
    # Fallback: last segment of filename before extension (review-xxx-PERSONA.md)
    parts = filepath.stem.rsplit("-", 1)
    if len(parts) == 2:
        return parts[-1]
    return None


# ---------------------------------------------------------------------------
# Direction computation
# ---------------------------------------------------------------------------

def compute_direction(initiative: str, marker: str) -> str:
    """Compute friction direction from initiative + marker.

    Returns one of: a_corroborates_h, a_contests_h, h_corroborates_a, h_contests_a
    """
    is_corroboration = marker == "sound"
    if initiative == "persona":
        return "a_corroborates_h" if is_corroboration else "a_contests_h"
    else:  # PO
        return "h_corroborates_a" if is_corroboration else "h_contests_a"


def resolve_lineage(records: list[dict]) -> list[dict]:
    """Resolve friction lineage via ref: fields.

    A chain of frictions linked by ref = one logical friction.
    The last resolution in the chain propagates to the source.
    Records with a ref are marked as amendments (not counted as standalone).
    """
    # Build index: source_key -> list of records at that source
    by_source = {}
    for i, r in enumerate(records):
        source = r.get("source", "")
        # Strip extension for matching
        source_key = source.rsplit(".", 1)[0] if "." in source else source
        if source_key not in by_source:
            by_source[source_key] = []
        by_source[source_key].append((i, r))

    # For each record with a ref, find the source and propagate
    resolved_sources = set()  # indices of records that are resolved by a later ref
    for i, r in enumerate(records):
        ref = r.get("ref")
        if not ref:
            continue

        # Parse ref: {id-source}/{index}
        parts = ref.strip().split("/")
        if len(parts) < 2:
            continue

        ref_index_str = parts[-1]
        ref_source = "/".join(parts[:-1])

        try:
            ref_index = int(ref_index_str) - 1  # 1-based to 0-based
        except ValueError:
            continue

        # Find the source record
        # Try matching with and without path prefix
        matched = None
        for key in by_source:
            if key.endswith(ref_source) or ref_source.endswith(key.split("/")[-1]):
                source_records = by_source[key]
                if 0 <= ref_index < len(source_records):
                    matched = source_records[ref_index]
                    break

        if matched:
            src_idx, src_record = matched
            # Propagate resolution from amendment to source
            if r.get("resolution") and not src_record.get("resolution"):
                src_record["resolution"] = r["resolution"]
            # Mark source as resolved by lineage
            resolved_sources.add(src_idx)
            # Mark this record as an amendment
            r["is_amendment"] = True

    # Mark non-amendment records
    for i, r in enumerate(records):
        if "is_amendment" not in r:
            r["is_amendment"] = False

    return records


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def analyze_instance(instance_path: Path) -> dict:
    """Run full analysis on an instance. Returns structured data for analysis.html."""

    # Discover personas
    real_personas = sorted(audit.discover_personas(instance_path))

    # Find all session files
    session_files = sorted(instance_path.rglob("sessions/*.md"))
    session_files = [f for f in session_files if "shared" not in f.relative_to(instance_path).parts]

    # Per-session analysis
    def _new_bucket():
        return {
            "markers": defaultdict(int), "resolutions": defaultdict(int),
            "directions": defaultdict(int), "flux_h": 0, "flux_a": 0,
            "sessions": 0, "artefacts": 0,
            "frictions": 0, "frictions_sessions": 0, "frictions_artefacts": 0,
        }

    by_week: dict[str, dict] = defaultdict(_new_bucket)
    by_day: dict[str, dict] = defaultdict(_new_bucket)

    by_persona: dict[str, dict] = defaultdict(lambda: {
        "markers": defaultdict(int),
        "resolutions": defaultdict(int),
        "directions": defaultdict(int),
        "flux_h": 0, "flux_a": 0,
        "flux_types_h": defaultdict(int),
        "flux_types_a": defaultdict(int),
        "sessions": 0, "artefacts": 0,
        "frictions": 0, "frictions_sessions": 0, "frictions_artefacts": 0,
        "signaler_pattern": [],
    })

    # Per-persona time series buckets
    by_persona_week: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(_new_bucket))
    by_persona_day: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(_new_bucket))

    all_weeks = set()
    all_days = set()

    # Individual friction records for pilotage dashboard
    all_friction_records: list[dict] = []

    for filepath in session_files:
        fm = audit.parse_frontmatter(filepath)
        if fm is None:
            continue

        normalized = audit.normalize_frontmatter(fm)
        persona = normalized.get("persona", "")
        if not persona:
            continue

        session_date = parse_session_date(filepath)
        if not session_date:
            continue

        week = date_to_week(session_date)
        day = session_date  # YYYY-MM-DD
        all_weeks.add(week)
        all_days.add(day)

        try:
            text = filepath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        by_week[week]["sessions"] += 1
        by_day[day]["sessions"] += 1
        by_persona[persona]["sessions"] += 1
        by_persona_week[persona][week]["sessions"] += 1
        by_persona_day[persona][day]["sessions"] += 1

        # Friction
        friction_records = parse_friction_lines(text)
        for rec in friction_records:
            marker = rec["marker"]
            initiative = rec["initiative"]
            resolution = rec["resolution"]
            direction = compute_direction(initiative, marker)

            for bucket in (by_week[week], by_day[day], by_persona_week[persona][week], by_persona_day[persona][day]):
                bucket["markers"][marker] += 1
                bucket["frictions"] += 1
                bucket["frictions_sessions"] += 1
                bucket["directions"][direction] += 1
                if resolution:
                    bucket["resolutions"][resolution] += 1

            by_persona[persona]["markers"][marker] += 1
            by_persona[persona]["frictions"] += 1
            by_persona[persona]["frictions_sessions"] += 1
            by_persona[persona]["directions"][direction] += 1

            if resolution:
                by_persona[persona]["resolutions"][resolution] += 1

            # Collect individual record for pilotage
            all_friction_records.append({
                "persona": persona,
                "date": session_date,
                "source": filepath.relative_to(instance_path).as_posix(),
                "source_type": "session",
                "marker": marker,
                "initiative": initiative,
                "direction": direction,
                "resolution": resolution,
                "description": rec.get("description", ""),
                "ref": rec.get("ref"),
            })

        # Flux
        flux_records = parse_flux_lines(text)
        for rec in flux_records:
            if rec["direction"] == "H":
                by_week[week]["flux_h"] += 1
                by_day[day]["flux_h"] += 1
                by_persona[persona]["flux_h"] += 1
                by_persona[persona]["flux_types_h"][rec["type"]] += 1
                by_persona_week[persona][week]["flux_h"] += 1
                by_persona_day[persona][day]["flux_h"] += 1
            else:
                by_week[week]["flux_a"] += 1
                by_day[day]["flux_a"] += 1
                by_persona[persona]["flux_a"] += 1
                by_persona[persona]["flux_types_a"][rec["type"]] += 1
                by_persona_week[persona][week]["flux_a"] += 1
                by_persona_day[persona][day]["flux_a"] += 1

        # signalerPattern
        sp = parse_signaler_pattern(text)
        if sp is not None:
            sp["session"] = filepath.stem
            sp["date"] = session_date
            by_persona[persona]["signaler_pattern"].append(sp)

    # --------------- Artefacts from shared/ ---------------
    artefact_files = find_artefacts(instance_path)

    for filepath in artefact_files:
        persona = parse_artefact_persona(filepath)
        if not persona:
            continue

        artefact_date = parse_artefact_date(filepath)
        if not artefact_date:
            continue

        week = date_to_week(artefact_date)
        day = artefact_date
        all_weeks.add(week)
        all_days.add(day)

        try:
            text = filepath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        # Count artefact
        by_week[week]["artefacts"] += 1
        by_day[day]["artefacts"] += 1
        by_persona[persona]["artefacts"] += 1
        by_persona_week[persona][week]["artefacts"] += 1
        by_persona_day[persona][day]["artefacts"] += 1

        # Friction from artefacts — same parser as sessions
        friction_records = parse_friction_lines(text)
        for rec in friction_records:
            marker = rec["marker"]
            initiative = rec["initiative"]
            resolution = rec["resolution"]
            direction = compute_direction(initiative, marker)

            for bucket in (by_week[week], by_day[day], by_persona_week[persona][week], by_persona_day[persona][day]):
                bucket["markers"][marker] += 1
                bucket["frictions"] += 1
                bucket["frictions_artefacts"] += 1
                bucket["directions"][direction] += 1
                if resolution:
                    bucket["resolutions"][resolution] += 1

            by_persona[persona]["markers"][marker] += 1
            by_persona[persona]["frictions"] += 1
            by_persona[persona]["frictions_artefacts"] += 1
            by_persona[persona]["directions"][direction] += 1

            if resolution:
                by_persona[persona]["resolutions"][resolution] += 1

            # Collect individual record for pilotage
            all_friction_records.append({
                "persona": persona,
                "date": artefact_date,
                "source": filepath.relative_to(instance_path).as_posix(),
                "source_type": "artefact",
                "marker": marker,
                "initiative": initiative,
                "direction": direction,
                "resolution": resolution,
                "description": rec.get("description", ""),
                "ref": rec.get("ref"),
            })

    # Sort periods
    sorted_weeks = sorted(all_weeks)
    sorted_days = sorted(all_days)

    # Build time series helper
    marker_keys = list(FRICTION_MARKERS.values())
    direction_keys = ["a_corroborates_h", "a_contests_h", "h_corroborates_a", "h_contests_a"]
    resolution_keys = list(RESOLUTION_TAGS)

    def build_series(by_period: dict, sorted_keys: list[str]) -> dict:
        return {
            "labels": sorted_keys,
            "markers": {k: [by_period[p]["markers"].get(k, 0) for p in sorted_keys] for k in marker_keys},
            "directions": {k: [by_period[p]["directions"].get(k, 0) for p in sorted_keys] for k in direction_keys},
            "resolutions": {k: [by_period[p]["resolutions"].get(k, 0) for p in sorted_keys] for k in resolution_keys},
            "frictions_per_session": [
                round(by_period[p]["frictions"] / max(by_period[p]["sessions"], 1), 1)
                for p in sorted_keys
            ],
            "resolutions_per_session": [
                round(sum(by_period[p]["resolutions"].values()) / max(by_period[p]["sessions"], 1), 1)
                for p in sorted_keys
            ],
            "flux_h": [by_period[p]["flux_h"] for p in sorted_keys],
            "flux_a": [by_period[p]["flux_a"] for p in sorted_keys],
            "sessions": [by_period[p]["sessions"] for p in sorted_keys],
            "artefacts": [by_period[p]["artefacts"] for p in sorted_keys],
            "frictions_sessions": [by_period[p]["frictions_sessions"] for p in sorted_keys],
            "frictions_artefacts": [by_period[p]["frictions_artefacts"] for p in sorted_keys],
        }

    time_series = {
        "week": build_series(by_week, sorted_weeks),
        "day": build_series(by_day, sorted_days),
    }

    # Build persona summary
    personas_data = {}
    for p in sorted(by_persona.keys()):
        d = by_persona[p]
        total_flux = d["flux_h"] + d["flux_a"]
        flux_h_pct = round(d["flux_h"] / max(total_flux, 1) * 100)
        flux_a_pct = 100 - flux_h_pct if total_flux > 0 else 0

        a_total = d["directions"].get("a_corroborates_h", 0) + d["directions"].get("a_contests_h", 0)
        h_total = d["directions"].get("h_corroborates_a", 0) + d["directions"].get("h_contests_a", 0)
        ratio = round(a_total / max(h_total, 1), 1)

        # signalerPattern summary
        sp_count = len(d["signaler_pattern"])
        sp_erreur = sum(1 for s in d["signaler_pattern"] if s.get("choix") and ("erreur" in s["choix"] or "llm" in s["choix"]))
        sp_conviction = sum(1 for s in d["signaler_pattern"] if s.get("choix") and "conviction" in s["choix"])
        sp_resistance = sum(1 for s in d["signaler_pattern"] if s.get("choix") and "resistance" in s["choix"])

        resolved = sum(d["resolutions"].values())
        total_frictions = d["frictions"]

        personas_data[p] = {
            "sessions": d["sessions"],
            "artefacts": d["artefacts"],
            "frictions": total_frictions,
            "frictions_sessions": d["frictions_sessions"],
            "frictions_artefacts": d["frictions_artefacts"],
            "markers": dict(d["markers"]),
            "resolutions": dict(d["resolutions"]),
            "resolved_pct": round(resolved / max(total_frictions, 1) * 100),
            "directions": dict(d["directions"]),
            "direction_ratio": ratio,
            "flux_h": d["flux_h"],
            "flux_a": d["flux_a"],
            "flux_h_pct": flux_h_pct,
            "flux_a_pct": flux_a_pct,
            "signaler_pattern_count": sp_count,
            "signaler_pattern_erreur_llm": sp_erreur,
            "signaler_pattern_conviction": sp_conviction,
            "signaler_pattern_resistance": sp_resistance,
            "time_series": {
                "week": build_series(by_persona_week[p], sorted_weeks),
                "day": build_series(by_persona_day[p], sorted_days),
            },
        }

    # Totals
    total_frictions = sum(d["frictions"] for d in by_persona.values())
    total_frictions_sessions = sum(d["frictions_sessions"] for d in by_persona.values())
    total_frictions_artefacts = sum(d["frictions_artefacts"] for d in by_persona.values())
    total_resolved = sum(sum(d["resolutions"].values()) for d in by_persona.values())
    total_sessions = sum(d["sessions"] for d in by_persona.values())
    total_artefacts = sum(d["artefacts"] for d in by_persona.values())
    total_sp = sum(len(d["signaler_pattern"]) for d in by_persona.values())

    # Resolution totals
    res_totals = defaultdict(int)
    for d in by_persona.values():
        for k, v in d["resolutions"].items():
            res_totals[k] += v

    return {
        "meta": {
            "instance": instance_path.name,
            "date": date.today().isoformat(),
            "personas": real_personas,
            "sessions_scanned": len(session_files),
            "artefacts_scanned": len(artefact_files),
        },
        "totals": {
            "frictions": total_frictions,
            "frictions_sessions": total_frictions_sessions,
            "frictions_artefacts": total_frictions_artefacts,
            "resolved": total_resolved,
            "resolved_pct": round(total_resolved / max(total_frictions, 1) * 100),
            "sessions": total_sessions,
            "artefacts": total_artefacts,
            "signaler_pattern": total_sp,
            "resolutions": dict(res_totals),
        },
        "time_series": time_series,
        "personas": personas_data,
        "friction_records": resolve_lineage(sorted(all_friction_records, key=lambda r: r.get("date", ""))),
    }


# ---------------------------------------------------------------------------
# Multi-instance aggregation
# ---------------------------------------------------------------------------

def aggregate_instances(instances_data: dict[str, dict]) -> dict:
    """Aggregate multiple instance analyses into a combined view."""
    marker_keys = list(FRICTION_MARKERS.values())
    direction_keys = ["a_corroborates_h", "a_contests_h", "h_corroborates_a", "h_contests_a"]
    resolution_keys = list(RESOLUTION_TAGS)

    def aggregate_period(period_key: str) -> dict:
        """Aggregate a single period type (week or day) across instances."""
        all_labels = set()
        for d in instances_data.values():
            all_labels.update(d["time_series"][period_key]["labels"])
        sorted_labels = sorted(all_labels)
        label_idx = {l: i for i, l in enumerate(sorted_labels)}
        n = len(sorted_labels)

        agg = {
            "labels": sorted_labels,
            "markers": {k: [0]*n for k in marker_keys},
            "directions": {k: [0]*n for k in direction_keys},
            "resolutions": {k: [0]*n for k in resolution_keys},
            "flux_h": [0]*n, "flux_a": [0]*n, "sessions": [0]*n,
            "artefacts": [0]*n, "frictions_sessions": [0]*n, "frictions_artefacts": [0]*n,
        }
        sessions_count = [0]*n
        frictions_count = [0]*n

        for d in instances_data.values():
            ts = d["time_series"][period_key]
            inst_labels = ts["labels"]
            for i, label in enumerate(inst_labels):
                idx = label_idx[label]
                for k in marker_keys:
                    v = ts["markers"].get(k, [])
                    if i < len(v): agg["markers"][k][idx] += v[i]
                for k in direction_keys:
                    v = ts["directions"].get(k, [])
                    if i < len(v): agg["directions"][k][idx] += v[i]
                for k in resolution_keys:
                    v = ts["resolutions"].get(k, [])
                    if i < len(v): agg["resolutions"][k][idx] += v[i]
                if i < len(ts["flux_h"]): agg["flux_h"][idx] += ts["flux_h"][i]
                if i < len(ts["flux_a"]): agg["flux_a"][idx] += ts["flux_a"][i]
                if i < len(ts.get("sessions", [])): agg["sessions"][idx] += ts["sessions"][i]
                if i < len(ts.get("artefacts", [])): agg["artefacts"][idx] += ts["artefacts"][i]
                if i < len(ts.get("frictions_sessions", [])): agg["frictions_sessions"][idx] += ts["frictions_sessions"][i]
                if i < len(ts.get("frictions_artefacts", [])): agg["frictions_artefacts"][idx] += ts["frictions_artefacts"][i]
                # Reconstruct raw counts for per-session ratios
                frictions_count[idx] += sum(agg["markers"][k][idx] for k in marker_keys) - frictions_count[idx]  # delta
                fps = ts.get("frictions_per_session", [])
                if i < len(fps) and fps[i] > 0:
                    sessions_count[idx] += round(sum(ts["markers"].get(k, [0]*len(inst_labels))[i] for k in marker_keys) / fps[i])

        # Recompute frictions_count properly
        frictions_count = [sum(agg["markers"][k][i] for k in marker_keys) for i in range(n)]
        res_count = [sum(agg["resolutions"][k][i] for k in resolution_keys) for i in range(n)]

        agg["frictions_per_session"] = [
            round(frictions_count[i] / max(sessions_count[i], 1), 1) for i in range(n)
        ]
        agg["resolutions_per_session"] = [
            round(res_count[i] / max(sessions_count[i], 1), 1) for i in range(n)
        ]
        return agg

    # Aggregate totals
    total_frictions = sum(d["totals"]["frictions"] for d in instances_data.values())
    total_frictions_sessions = sum(d["totals"]["frictions_sessions"] for d in instances_data.values())
    total_frictions_artefacts = sum(d["totals"]["frictions_artefacts"] for d in instances_data.values())
    total_resolved = sum(d["totals"]["resolved"] for d in instances_data.values())
    total_sessions = sum(d["totals"]["sessions"] for d in instances_data.values())
    total_artefacts = sum(d["totals"]["artefacts"] for d in instances_data.values())
    total_sp = sum(d["totals"]["signaler_pattern"] for d in instances_data.values())

    res_totals = defaultdict(int)
    for d in instances_data.values():
        for k, v in d["totals"]["resolutions"].items():
            res_totals[k] += v

    # Aggregate personas — merge across instances instead of overwriting
    all_personas = {}
    for inst_name, d in instances_data.items():
        for p, pdata in d["personas"].items():
            if p not in all_personas:
                # Deep copy to avoid mutating source
                all_personas[p] = {k: (dict(v) if isinstance(v, dict) else list(v) if isinstance(v, list) else v) for k, v in pdata.items()}
            else:
                existing = all_personas[p]
                # Sum numeric fields
                for k in ("sessions", "artefacts", "frictions", "frictions_sessions", "frictions_artefacts",
                           "flux_h", "flux_a", "signaler_pattern_count",
                           "signaler_pattern_erreur_llm", "signaler_pattern_conviction", "signaler_pattern_resistance"):
                    existing[k] = existing.get(k, 0) + pdata.get(k, 0)
                # Merge dict fields (markers, resolutions, directions)
                for dk in ("markers", "resolutions", "directions"):
                    if dk in pdata:
                        if dk not in existing:
                            existing[dk] = {}
                        for k, v in pdata[dk].items():
                            existing[dk][k] = existing[dk].get(k, 0) + v
                # Recompute derived fields
                total_flux = existing["flux_h"] + existing["flux_a"]
                existing["flux_h_pct"] = round(existing["flux_h"] / max(total_flux, 1) * 100)
                existing["flux_a_pct"] = 100 - existing["flux_h_pct"] if total_flux > 0 else 0
                a_total = existing["directions"].get("a_corroborates_h", 0) + existing["directions"].get("a_contests_h", 0)
                h_total = existing["directions"].get("h_corroborates_a", 0) + existing["directions"].get("h_contests_a", 0)
                existing["direction_ratio"] = round(a_total / max(h_total, 1), 1)
                existing["resolved_pct"] = round(sum(existing.get("resolutions", {}).values()) / max(existing["frictions"], 1) * 100)

    return {
        "meta": {
            "instance": "all",
            "date": date.today().isoformat(),
            "personas": sorted(all_personas.keys()),
            "sessions_scanned": sum(d["meta"]["sessions_scanned"] for d in instances_data.values()),
            "artefacts_scanned": sum(d["meta"]["artefacts_scanned"] for d in instances_data.values()),
        },
        "totals": {
            "frictions": total_frictions,
            "frictions_sessions": total_frictions_sessions,
            "frictions_artefacts": total_frictions_artefacts,
            "resolved": total_resolved,
            "resolved_pct": round(total_resolved / max(total_frictions, 1) * 100),
            "sessions": total_sessions,
            "artefacts": total_artefacts,
            "signaler_pattern": total_sp,
            "resolutions": dict(res_totals),
        },
        "time_series": {
            "week": aggregate_period("week"),
            "day": aggregate_period("day"),
        },
        "personas": all_personas,
        "friction_records": sorted(
            [r for d in instances_data.values() for r in d.get("friction_records", [])],
            key=lambda r: r.get("date", ""),
        ),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Produce analysis JSON for analysis.html")
    parser.add_argument("instances", nargs="+", help="Path(s) to SOFIA instance root(s)")
    parser.add_argument("--output", help="Output path (default: ./analysis.json if multi-instance, <instance>/shared/audits/analysis.json if single)")
    args = parser.parse_args()

    instance_paths = []
    for p in args.instances:
        path = Path(p).resolve()
        if not (path / "sofia.md").is_file() and not (path / "voix.md").is_file():
            print(f"⚠ Instance ignoree (pas de sofia.md) : {path}", file=sys.stderr)
            continue
        instance_paths.append(path)

    if not instance_paths:
        print("✗ Aucune instance valide trouvee.", file=sys.stderr)
        sys.exit(1)

    # Analyze each instance
    instances_data = {}
    for path in instance_paths:
        name = path.name
        print(f"  Analyse {name}...")
        instances_data[name] = analyze_instance(path)

    # Build output: instances + aggregated
    multi = len(instance_paths) > 1
    aggregated = aggregate_instances(instances_data) if multi else None

    output = {
        "instances": instances_data,
    }
    if aggregated:
        output["all"] = aggregated

    # Default view = aggregated if multi, single instance if solo
    if multi:
        output["default"] = "all"
    else:
        output["default"] = list(instances_data.keys())[0]

    # Output path
    if args.output:
        output_path = Path(args.output)
    elif multi:
        output_path = Path("analysis.json")
    else:
        output_path = instance_paths[0] / "shared" / "audits" / "analysis.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n✓ {output_path}")
    for name, d in instances_data.items():
        fs = d['totals']['frictions_sessions']
        fa = d['totals']['frictions_artefacts']
        print(f"  {name}: {d['totals']['frictions']} frictions ({fs} sessions, {fa} artefacts), {d['totals']['sessions']} sessions, {d['meta']['artefacts_scanned']} artefacts, {len(d['personas'])} personas")
    if aggregated:
        fs = aggregated['totals']['frictions_sessions']
        fa = aggregated['totals']['frictions_artefacts']
        print(f"  all: {aggregated['totals']['frictions']} frictions ({fs} sessions, {fa} artefacts), {aggregated['totals']['sessions']} sessions")


if __name__ == "__main__":
    main()
