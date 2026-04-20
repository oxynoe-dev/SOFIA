"""lens.py — Produce lens.json from records.json.

Aggregates friction records into time series:
- MarkerSeries (markers by day/week)
- DirectionSeries (who challenges whom over time)
- ResolutionSeries (resolution distribution over time)
- FluxSeries (H vs A contributions over time)

Calls scan.py internally if records.json is absent or stale.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from analysis.lib.constants import FRICTION_MARKERS, RESOLUTION_TAGS, DIRECTION_KEYS
from analysis.lib.parser import date_to_week


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


def _build_series(friction_records: list[dict], contrib_records: list[dict], granularity: str = "day") -> dict:
    """Build time series at given granularity (day or week)."""
    marker_keys = list(FRICTION_MARKERS.values())
    resolution_keys = list(RESOLUTION_TAGS)

    by_period = defaultdict(lambda: {
        "markers": defaultdict(int),
        "directions": defaultdict(int),
        "resolutions": defaultdict(int),
        "flux_h": 0, "flux_a": 0,
        "sessions": 0, "artifacts": 0,
        "frictions": 0,
    })

    session_sources = defaultdict(set)

    for r in friction_records:
        if r.get("is_amendment"):
            continue
        period = r.get("week") if granularity == "week" else r.get("date", "unknown")
        by_period[period]["markers"][r["marker"]] += 1
        by_period[period]["directions"][r["direction"]] += 1
        by_period[period]["frictions"] += 1
        if r.get("resolution") in RESOLUTION_TAGS:
            by_period[period]["resolutions"][r["resolution"]] += 1
        if r["source_type"] == "session":
            session_sources[period].add(r["source"])
        else:
            by_period[period]["artifacts"] += 1

    for period, sources in session_sources.items():
        by_period[period]["sessions"] = len(sources)

    for r in contrib_records:
        period = r.get("week") if granularity == "week" else r.get("date", "unknown")
        if r["direction"] == "H":
            by_period[period]["flux_h"] += 1
        else:
            by_period[period]["flux_a"] += 1

    sorted_periods = sorted(by_period.keys())
    n = len(sorted_periods)

    return {
        "labels": sorted_periods,
        "markers": {k: [by_period[p]["markers"].get(k, 0) for p in sorted_periods] for k in marker_keys},
        "directions": {k: [by_period[p]["directions"].get(k, 0) for p in sorted_periods] for k in DIRECTION_KEYS},
        "resolutions": {k: [by_period[p]["resolutions"].get(k, 0) for p in sorted_periods] for k in resolution_keys},
        "flux_h": [by_period[p]["flux_h"] for p in sorted_periods],
        "flux_a": [by_period[p]["flux_a"] for p in sorted_periods],
        "sessions": [by_period[p]["sessions"] for p in sorted_periods],
        "artifacts": [by_period[p]["artifacts"] for p in sorted_periods],
        "frictions_per_session": [
            round(by_period[p]["frictions"] / max(by_period[p]["sessions"], 1), 1)
            for p in sorted_periods
        ],
    }


def _build_persona_series(friction_records: list[dict], contrib_records: list[dict], personas: list[str]) -> dict:
    """Build per-persona aggregation for Lens tables."""
    by_persona = defaultdict(lambda: {
        "markers": defaultdict(int),
        "directions": defaultdict(int),
        "resolutions": defaultdict(int),
        "frictions": 0,
        "flux_h": 0, "flux_a": 0,
    })

    for r in friction_records:
        if r.get("is_amendment"):
            continue
        p = r["persona"]
        by_persona[p]["markers"][r["marker"]] += 1
        by_persona[p]["directions"][r["direction"]] += 1
        by_persona[p]["frictions"] += 1
        if r.get("resolution") in RESOLUTION_TAGS:
            by_persona[p]["resolutions"][r["resolution"]] += 1

    for r in contrib_records:
        p = r["persona"]
        if r["direction"] == "H":
            by_persona[p]["flux_h"] += 1
        else:
            by_persona[p]["flux_a"] += 1

    result = {}
    for p in personas:
        d = by_persona.get(p, {})
        result[p] = {
            "markers": dict(d.get("markers", {})),
            "directions": dict(d.get("directions", {})),
            "resolutions": dict(d.get("resolutions", {})),
            "frictions": d.get("frictions", 0),
            "flux_h": d.get("flux_h", 0),
            "flux_a": d.get("flux_a", 0),
        }
    return result


def build_lens(records: dict) -> dict:
    """Build lens.json content from scan records."""
    result = {"instances": {}}

    for inst_name, inst_data in records.items():
        friction_recs = inst_data.get("friction_records", [])
        contrib_recs = inst_data.get("contribution_records", [])
        personas = inst_data.get("meta", {}).get("personas", [])

        result["instances"][inst_name] = {
            "meta": inst_data["meta"],
            "time_series": {
                "week": _build_series(friction_recs, contrib_recs, "week"),
                "day": _build_series(friction_recs, contrib_recs, "day"),
            },
            "personas": _build_persona_series(friction_recs, contrib_recs, personas),
        }

    return result


def write_lens(lens_data: dict, output_path: Path | None = None):
    """Write lens.json."""
    if output_path is None:
        output_path = DATA_DIR / "lens.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(lens_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build lens.json from records")
    parser.add_argument("instances", nargs="*", help="Instance paths (triggers scan if records.json absent)")
    args = parser.parse_args()

    paths = [Path(p).resolve() for p in args.instances] if args.instances else None
    records = ensure_records(paths)
    lens = build_lens(records)
    write_lens(lens)
    print(f"✓ lens.json — {len(lens['instances'])} instances")
