#!/usr/bin/env python3
"""analysis.py — Produce analysis JSON from SOFIA instances for analysis.html.

Usage:
    python analysis.py <instance-path> [<instance-path> ...] [--output <path>]

Accepts one or more instances. Produces a single analysis.json with:
- Per-instance data (friction, resolutions, flux, direction, signalerPattern)
- Aggregated totals across all instances
- Time series per instance and aggregated

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
RESOLUTION_TAGS = audit.RESOLUTION_TAGS


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
    """Parse ## Friction orchestrateur lines into structured records."""
    lines = text.splitlines()
    in_section = False
    records = []

    for line in lines:
        if line.strip().startswith("## Friction orchestrateur"):
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
        record = {"marker": None, "initiative": None, "resolution": None, "ref": None}

        # Marker
        for char, key in FRICTION_MARKERS.items():
            if char == "~":
                if item.startswith("~"):
                    record["marker"] = key
                    break
            elif char in item:
                record["marker"] = key
                break

        # Also check bracketed markers
        if not record["marker"]:
            bracket_match = re.search(r"\[(juste|contestable|simplification|angle-mort|faux)\]", item)
            if bracket_match:
                tag = bracket_match.group(1).replace("-", "_")
                record["marker"] = tag

        # Initiative
        if "[PO]" in item or "[po]" in item:
            record["initiative"] = "PO"
        else:
            record["initiative"] = "persona"

        # Resolution
        res_match = re.search(r"→\s*(\w+)", item)
        if res_match:
            tag = audit.strip_accents(res_match.group(1).lower())
            if tag in RESOLUTION_TAGS:
                record["resolution"] = tag

        # Ref
        ref_match = re.search(r"\(ref:\s*([^)]+)\)", item)
        if ref_match:
            record["ref"] = ref_match.group(1).strip()

        if record["marker"]:
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
# Direction computation
# ---------------------------------------------------------------------------

def compute_direction(initiative: str, marker: str) -> str:
    """Compute friction direction from initiative + marker.

    Returns one of: a_corrobore_h, a_conteste_h, h_corrobore_h, h_conteste_a
    """
    is_corroboration = marker == "juste"
    if initiative == "persona":
        return "a_corrobore_h" if is_corroboration else "a_conteste_h"
    else:  # PO
        return "h_corrobore_a" if is_corroboration else "h_conteste_a"


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
            "sessions": 0, "frictions": 0,
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
        "sessions": 0, "frictions": 0,
        "signaler_pattern": [],
    })

    all_weeks = set()
    all_days = set()

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

        # Friction
        friction_records = parse_friction_lines(text)
        for rec in friction_records:
            marker = rec["marker"]
            initiative = rec["initiative"]
            resolution = rec["resolution"]
            direction = compute_direction(initiative, marker)

            for bucket in (by_week[week], by_day[day]):
                bucket["markers"][marker] += 1
                bucket["frictions"] += 1
                bucket["directions"][direction] += 1
                if resolution:
                    bucket["resolutions"][resolution] += 1

            by_persona[persona]["markers"][marker] += 1
            by_persona[persona]["frictions"] += 1
            by_persona[persona]["directions"][direction] += 1

            if resolution:
                by_persona[persona]["resolutions"][resolution] += 1

        # Flux
        flux_records = parse_flux_lines(text)
        for rec in flux_records:
            if rec["direction"] == "H":
                by_week[week]["flux_h"] += 1
                by_day[day]["flux_h"] += 1
                by_persona[persona]["flux_h"] += 1
                by_persona[persona]["flux_types_h"][rec["type"]] += 1
            else:
                by_week[week]["flux_a"] += 1
                by_day[day]["flux_a"] += 1
                by_persona[persona]["flux_a"] += 1
                by_persona[persona]["flux_types_a"][rec["type"]] += 1

        # signalerPattern
        sp = parse_signaler_pattern(text)
        if sp is not None:
            sp["session"] = filepath.stem
            sp["date"] = session_date
            by_persona[persona]["signaler_pattern"].append(sp)

    # Sort periods
    sorted_weeks = sorted(all_weeks)
    sorted_days = sorted(all_days)

    # Build time series helper
    marker_keys = list(FRICTION_MARKERS.values())
    direction_keys = ["a_corrobore_h", "a_conteste_h", "h_corrobore_a", "h_conteste_a"]
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

        a_total = d["directions"].get("a_corrobore_h", 0) + d["directions"].get("a_conteste_h", 0)
        h_total = d["directions"].get("h_corrobore_a", 0) + d["directions"].get("h_conteste_a", 0)
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
            "frictions": total_frictions,
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
        }

    # Totals
    total_frictions = sum(d["frictions"] for d in by_persona.values())
    total_resolved = sum(sum(d["resolutions"].values()) for d in by_persona.values())
    total_sessions = sum(d["sessions"] for d in by_persona.values())
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
        },
        "totals": {
            "frictions": total_frictions,
            "resolved": total_resolved,
            "resolved_pct": round(total_resolved / max(total_frictions, 1) * 100),
            "sessions": total_sessions,
            "signaler_pattern": total_sp,
            "resolutions": dict(res_totals),
        },
        "time_series": time_series,
        "personas": personas_data,
    }


# ---------------------------------------------------------------------------
# Multi-instance aggregation
# ---------------------------------------------------------------------------

def aggregate_instances(instances_data: dict[str, dict]) -> dict:
    """Aggregate multiple instance analyses into a combined view."""
    marker_keys = list(FRICTION_MARKERS.values())
    direction_keys = ["a_corrobore_h", "a_conteste_h", "h_corrobore_a", "h_conteste_a"]
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
    total_resolved = sum(d["totals"]["resolved"] for d in instances_data.values())
    total_sessions = sum(d["totals"]["sessions"] for d in instances_data.values())
    total_sp = sum(d["totals"]["signaler_pattern"] for d in instances_data.values())

    res_totals = defaultdict(int)
    for d in instances_data.values():
        for k, v in d["totals"]["resolutions"].items():
            res_totals[k] += v

    # Aggregate personas
    all_personas = {}
    for inst_name, d in instances_data.items():
        for p, pdata in d["personas"].items():
            all_personas[p] = pdata

    return {
        "meta": {
            "instance": "all",
            "date": date.today().isoformat(),
            "personas": sorted(all_personas.keys()),
            "sessions_scanned": sum(d["meta"]["sessions_scanned"] for d in instances_data.values()),
        },
        "totals": {
            "frictions": total_frictions,
            "resolved": total_resolved,
            "resolved_pct": round(total_resolved / max(total_frictions, 1) * 100),
            "sessions": total_sessions,
            "signaler_pattern": total_sp,
            "resolutions": dict(res_totals),
        },
        "time_series": {
            "week": aggregate_period("week"),
            "day": aggregate_period("day"),
        },
        "personas": all_personas,
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
        print(f"  {name}: {d['totals']['frictions']} frictions, {d['totals']['sessions']} sessions, {len(d['personas'])} personas")
    if aggregated:
        print(f"  all: {aggregated['totals']['frictions']} frictions, {aggregated['totals']['sessions']} sessions")


if __name__ == "__main__":
    main()
