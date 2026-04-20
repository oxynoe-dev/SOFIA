"""mirror.py — Produce mirror.json from records.json.

Aggregates friction records into:
- Trajectory (challenge % over time)
- Radar (5 axes per persona)
- KPI (friction density, resolution rate)
- Map (persona cards, links)

Calls scan.py internally if records.json is absent or stale.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from analysis.lib.constants import FRICTION_MARKERS, RESOLUTION_TAGS, DIRECTION_KEYS, strip_accents
from analysis.lib.parser import parse_frontmatter, date_to_week


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def ensure_records(instance_paths: list[Path] | None = None) -> dict:
    """Load records.json, regenerating via scan.py if needed."""
    records_path = DATA_DIR / "records.json"
    if records_path.is_file():
        return json.loads(records_path.read_text(encoding="utf-8"))

    if not instance_paths:
        raise FileNotFoundError("records.json not found and no instance paths provided")

    from analysis.cli.scan import scan_instances, write_records
    records = scan_instances(instance_paths)
    write_records(records, records_path)
    return records


def build_mirror(records: dict) -> dict:
    """Build mirror.json content from scan records."""
    result = {"instances": {}}

    for inst_name, inst_data in records.items():
        friction_records = inst_data.get("friction_records", [])
        contrib_records = inst_data.get("contribution_records", [])
        sp_records = inst_data.get("signaler_patterns", [])
        personas = inst_data.get("meta", {}).get("personas", [])

        # --- Per-persona aggregation ---
        by_persona = defaultdict(lambda: {
            "markers": defaultdict(int),
            "resolutions": defaultdict(int),
            "directions": defaultdict(int),
            "frictions": 0, "sessions_frictions": 0, "artifact_frictions": 0,
            "flux_h": 0, "flux_a": 0,
            "flux_types_h": defaultdict(int),
            "flux_types_a": defaultdict(int),
        })

        # Count sessions per persona (from friction sources)
        sessions_per_persona = defaultdict(set)
        for r in friction_records:
            p = r["persona"]
            by_persona[p]["markers"][r["marker"]] += 1
            by_persona[p]["resolutions"][r.get("resolution", "none")] += 1
            by_persona[p]["directions"][r["direction"]] += 1
            by_persona[p]["frictions"] += 1
            if r["source_type"] == "session":
                by_persona[p]["sessions_frictions"] += 1
                sessions_per_persona[p].add(r["source"])
            else:
                by_persona[p]["artifact_frictions"] += 1

        for r in contrib_records:
            p = r["persona"]
            ctype = r.get("type", "substance")
            if r["direction"] == "H":
                by_persona[p]["flux_h"] += 1
                by_persona[p]["flux_types_h"][ctype] += 1
            else:
                by_persona[p]["flux_a"] += 1
                by_persona[p]["flux_types_a"][ctype] += 1

        # --- Trajectory (challenge % by week) ---
        by_week = defaultdict(lambda: {"total": 0, "challenge": 0})
        for r in friction_records:
            if r.get("is_amendment"):
                continue
            w = r.get("week", "unknown")
            by_week[w]["total"] += 1
            if r["marker"] != "sound":
                by_week[w]["challenge"] += 1

        sorted_weeks = sorted(by_week.keys())
        trajectory = {
            "labels": sorted_weeks,
            "challenge_pct": [
                round(by_week[w]["challenge"] / max(by_week[w]["total"], 1) * 100, 1)
                for w in sorted_weeks
            ],
            "density": [by_week[w]["total"] for w in sorted_weeks],
        }

        # --- Radar (5 axes per persona) ---
        radars = {}
        for p in personas:
            d = by_persona.get(p, {})
            total_f = d.get("frictions", 0)
            markers = d.get("markers", {})
            resolutions = d.get("resolutions", {})
            directions = d.get("directions", {})

            # Diversity: how many different marker types used (0-100, 5 = 100)
            types_used = sum(1 for v in markers.values() if v > 0)
            diversity = round(types_used / 5 * 100) if total_f > 0 else 0

            # Challenge: % non-sound
            non_sound = total_f - markers.get("sound", 0)
            challenge = round(non_sound / max(total_f, 1) * 100) if total_f > 0 else 0

            # Resolution: % resolved
            resolved = sum(v for k, v in resolutions.items() if k in RESOLUTION_TAGS)
            resolution = round(resolved / max(total_f, 1) * 100) if total_f > 0 else 0

            # Coverage: sessions with friction / total sessions
            sess_count = len(sessions_per_persona.get(p, set()))
            total_sess = inst_data["meta"].get("sessions_scanned", 0)
            coverage = round(sess_count / max(total_sess, 1) * 100)

            # Contribution: A contributions / total flux
            flux_total = d.get("flux_h", 0) + d.get("flux_a", 0)
            contribution = round(d.get("flux_a", 0) / max(flux_total, 1) * 100) if flux_total > 0 else 0

            radars[p] = {
                "diversity": diversity,
                "challenge": challenge,
                "resolution": resolution,
                "coverage": coverage,
                "contribution": contribution,
            }

        # --- KPI ---
        total_frictions = len([r for r in friction_records if not r.get("is_amendment")])
        total_resolved = sum(1 for r in friction_records if r.get("resolution") in RESOLUTION_TAGS and not r.get("is_amendment"))
        total_sessions = inst_data["meta"].get("sessions_scanned", 0)
        challenge_count = sum(1 for r in friction_records if r["marker"] != "sound" and not r.get("is_amendment"))

        kpi = {
            "friction_density": round(total_frictions / max(total_sessions, 1), 1),
            "resolution_rate": round(total_resolved / max(total_frictions, 1) * 100),
            "challenge_pct": round(challenge_count / max(total_frictions, 1) * 100),
            "total_frictions": total_frictions,
            "total_sessions": total_sessions,
        }

        # --- Map cards ---
        map_cards = {}
        for p in personas:
            d = by_persona.get(p, {})
            map_cards[p] = {
                "frictions": d.get("frictions", 0),
                "sessions": len(sessions_per_persona.get(p, set())),
            }

        # --- Open frictions (no resolution) ---
        open_frictions = [
            {"persona": r["persona"], "date": r["date"], "marker": r["marker"],
             "description": r.get("description", "")[:80], "source": r["source"]}
            for r in friction_records
            if not r.get("resolution") and not r.get("is_amendment")
        ]

        # --- Map topology ---
        persona_roles = inst_data["meta"].get("persona_roles", {})
        context_sizes = inst_data["meta"].get("context_sizes", {})
        links = []
        for p in personas:
            d = by_persona.get(p, {})
            total = d.get("frictions", 0)
            if total > 0:
                links.append({"persona": p, "total": total})

        map_data = {
            "persona_roles": persona_roles,
            "links": links,
            "context_sizes": context_sizes,
            "description": "",
        }

        # --- Per-persona data for client-side rendering ---
        personas_data = {}
        for p in personas:
            d = by_persona.get(p, {})
            personas_data[p] = {
                "flux_h": d.get("flux_h", 0),
                "flux_a": d.get("flux_a", 0),
                "flux_types_h": dict(d.get("flux_types_h", defaultdict(int))),
                "flux_types_a": dict(d.get("flux_types_a", defaultdict(int))),
            }

        result["instances"][inst_name] = {
            "meta": inst_data["meta"],
            "friction_records": friction_records,
            "personas": personas_data,
            "map": map_data,
            "trajectory": trajectory,
            "radars": radars,
            "kpi": kpi,
            "map_cards": map_cards,
            "open_frictions": open_frictions[-20:],  # last 20
        }

    if result["instances"]:
        result["default"] = next(iter(result["instances"]))

    return result


def write_mirror(mirror_data: dict, output_path: Path | None = None):
    """Write mirror.json."""
    if output_path is None:
        output_path = DATA_DIR / "mirror.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(mirror_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build mirror.json from records")
    parser.add_argument("instances", nargs="*", help="Instance paths (triggers scan if records.json absent)")
    args = parser.parse_args()

    paths = [Path(p).resolve() for p in args.instances] if args.instances else None
    records = ensure_records(paths)
    mirror = build_mirror(records)
    write_mirror(mirror)
    print(f"✓ mirror.json — {len(mirror['instances'])} instances")
