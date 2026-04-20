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


def _build_series(friction_records: list[dict], contrib_records: list[dict],
                   granularity: str = "day", session_dates: list[str] | None = None) -> dict:
    """Build time series at given granularity (day or week).

    session_dates: optional list of YYYY-MM-DD dates from all sessions,
    so that weeks with sessions but no friction still appear on the timeline.
    """
    marker_keys = list(FRICTION_MARKERS.values())
    resolution_keys = list(RESOLUTION_TAGS)

    by_period = defaultdict(lambda: {
        "markers": defaultdict(int),
        "directions": defaultdict(int),
        "resolutions": defaultdict(int),
        "flux_h": 0, "flux_a": 0,
        "sessions": 0, "artifacts": 0,
        "frictions": 0, "resolved": 0,
    })

    # Count sessions per period from actual session dates (not just friction sources)
    session_count_per_period = defaultdict(int)
    if session_dates:
        from analysis.lib.parser import date_to_week
        for d in session_dates:
            period = date_to_week(d) if granularity == "week" else d
            session_count_per_period[period] += 1
            _ = by_period[period]  # seed entry so silent weeks appear

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
            by_period[period]["resolved"] += 1
        if r["source_type"] == "session":
            session_sources[period].add(r["source"])
        else:
            by_period[period]["artifacts"] += 1

    # Session count: use actual session dates (includes silent sessions)
    # Fall back to friction sources if no session_dates provided
    for period in by_period:
        if session_count_per_period:
            by_period[period]["sessions"] = session_count_per_period.get(period, 0)
        else:
            by_period[period]["sessions"] = len(session_sources.get(period, set()))

    for r in contrib_records:
        period = r.get("week") if granularity == "week" else r.get("date", "unknown")
        if r["direction"] == "H":
            by_period[period]["flux_h"] += 1
        else:
            by_period[period]["flux_a"] += 1

    sorted_periods = sorted(p for p in by_period.keys() if p != "unknown")

    return {
        "labels": sorted_periods,
        "markers": {k: [by_period[p]["markers"].get(k, 0) for p in sorted_periods] for k in marker_keys},
        "directions": {k: [by_period[p]["directions"].get(k, 0) for p in sorted_periods] for k in DIRECTION_KEYS},
        "resolutions": {k: [by_period[p]["resolutions"].get(k, 0) for p in sorted_periods] for k in resolution_keys},
        "flux_h": [by_period[p]["flux_h"] for p in sorted_periods],
        "flux_a": [by_period[p]["flux_a"] for p in sorted_periods],
        "sessions": [by_period[p]["sessions"] for p in sorted_periods],
        "artefacts": [by_period[p]["artifacts"] for p in sorted_periods],
        "frictions_per_session": [
            round(by_period[p]["frictions"] / max(by_period[p]["sessions"], 1), 1)
            for p in sorted_periods
        ],
        "resolutions_per_session": [
            round(by_period[p]["resolved"] / max(by_period[p]["sessions"], 1), 1)
            for p in sorted_periods
        ],
        "frictions_sessions": [by_period[p]["frictions"] for p in sorted_periods],
        "frictions_artefacts": [by_period[p]["artifacts"] for p in sorted_periods],
    }


def _build_persona_data(friction_records: list[dict], contrib_records: list[dict],
                         signaler_patterns: list[dict], personas: list[str]) -> dict:
    """Build per-persona aggregation with all fields the dashboard needs."""
    by_persona = defaultdict(lambda: {
        "markers": defaultdict(int),
        "directions": defaultdict(int),
        "resolutions": defaultdict(int),
        "frictions": 0,
        "flux_h": 0, "flux_a": 0,
        "sessions": set(),
        "flux_types_h": defaultdict(int),
        "flux_types_a": defaultdict(int),
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
        if r["source_type"] == "session":
            by_persona[p]["sessions"].add(r["source"])

    for r in contrib_records:
        p = r["persona"]
        if r["direction"] == "H":
            by_persona[p]["flux_h"] += 1
            by_persona[p]["flux_types_h"][r.get("type", "substance")] += 1
        else:
            by_persona[p]["flux_a"] += 1
            by_persona[p]["flux_types_a"][r.get("type", "substance")] += 1

    # Signaler patterns per persona
    sp_by_persona = defaultdict(lambda: {"count": 0, "erreur_llm": 0, "conviction": 0, "resistance": 0})
    for sp in signaler_patterns:
        p = sp["persona"]
        sp_by_persona[p]["count"] += 1
        choix = sp.get("choix", "")
        if choix in ("erreur_llm", "conviction", "resistance"):
            sp_by_persona[p][choix] += 1

    # Per-persona time series
    persona_friction = defaultdict(list)
    persona_contrib = defaultdict(list)
    for r in friction_records:
        persona_friction[r["persona"]].append(r)
    for r in contrib_records:
        persona_contrib[r["persona"]].append(r)

    result = {}
    for p in personas:
        d = by_persona.get(p, {})
        flux_h = d.get("flux_h", 0) if isinstance(d, dict) else 0
        flux_a = d.get("flux_a", 0) if isinstance(d, dict) else 0
        flux_total = flux_h + flux_a
        a_contests = d.get("directions", {}).get("a_contests_h", 0) if isinstance(d, dict) else 0
        h_contests = d.get("directions", {}).get("h_contests_a", 0) if isinstance(d, dict) else 0
        sp = sp_by_persona.get(p, {})

        sessions = d.get("sessions", set()) if isinstance(d, dict) else set()

        result[p] = {
            "markers": dict(d.get("markers", {})) if isinstance(d, dict) else {},
            "directions": dict(d.get("directions", {})) if isinstance(d, dict) else {},
            "resolutions": dict(d.get("resolutions", {})) if isinstance(d, dict) else {},
            "frictions": d.get("frictions", 0) if isinstance(d, dict) else 0,
            "flux_h": flux_h,
            "flux_a": flux_a,
            "flux_h_pct": round(flux_h / flux_total * 100) if flux_total > 0 else 0,
            "flux_a_pct": round(flux_a / flux_total * 100) if flux_total > 0 else 0,
            "flux_types_h": dict(d.get("flux_types_h", {})) if isinstance(d, dict) else {},
            "flux_types_a": dict(d.get("flux_types_a", {})) if isinstance(d, dict) else {},
            "sessions": len(sessions),
            "direction_ratio": round(a_contests / max(h_contests, 1), 1) if (a_contests + h_contests) > 0 else 0,
            "signaler_pattern_count": sp.get("count", 0),
            "signaler_pattern_erreur_llm": sp.get("erreur_llm", 0),
            "signaler_pattern_conviction": sp.get("conviction", 0),
            "signaler_pattern_resistance": sp.get("resistance", 0),
            "time_series": {
                "week": _build_series(persona_friction.get(p, []), persona_contrib.get(p, []), "week"),
                "day": _build_series(persona_friction.get(p, []), persona_contrib.get(p, []), "day"),
            },
        }
    return result


def build_lens(records: dict) -> dict:
    """Build lens.json content from scan records."""
    result = {"instances": {}, "default": None}

    for inst_name, inst_data in records.items():
        friction_recs = inst_data.get("friction_records", [])
        contrib_recs = inst_data.get("contribution_records", [])
        sp_recs = inst_data.get("signaler_patterns", [])
        personas = inst_data.get("meta", {}).get("personas", [])

        # All session dates (including sessions with no friction)
        session_dates = inst_data.get("session_dates", [])

        if result["default"] is None:
            result["default"] = inst_name

        result["instances"][inst_name] = {
            "meta": inst_data["meta"],
            "totals": {
                "signaler_pattern": len(sp_recs),
            },
            "time_series": {
                "week": _build_series(friction_recs, contrib_recs, "week", session_dates),
                "day": _build_series(friction_recs, contrib_recs, "day", session_dates),
            },
            "personas": _build_persona_data(friction_recs, contrib_recs, sp_recs, personas),
        }

    # ── Cross-instance aggregation ──
    if len(result["instances"]) > 1:
        all_friction = []
        all_contrib = []
        all_sp = []
        all_session_dates = []
        all_personas = set()
        total_sessions = 0
        total_artifacts = 0
        for inst_data in records.values():
            all_friction.extend(inst_data.get("friction_records", []))
            all_contrib.extend(inst_data.get("contribution_records", []))
            all_sp.extend(inst_data.get("signaler_patterns", []))
            all_session_dates.extend(inst_data.get("session_dates", []))
            all_personas.update(inst_data.get("meta", {}).get("personas", []))
            total_sessions += inst_data.get("meta", {}).get("sessions_scanned", 0)
            total_artifacts += inst_data.get("meta", {}).get("artifacts_scanned", 0)
        sorted_personas = sorted(all_personas)
        result["all"] = {
            "meta": {
                "instance": "all",
                "date": next(iter(records.values()))["meta"]["date"],
                "personas": sorted_personas,
                "sessions_scanned": total_sessions,
                "artifacts_scanned": total_artifacts,
            },
            "totals": {"signaler_pattern": len(all_sp)},
            "time_series": {
                "week": _build_series(all_friction, all_contrib, "week", all_session_dates),
                "day": _build_series(all_friction, all_contrib, "day", all_session_dates),
            },
            "personas": _build_persona_data(all_friction, all_contrib, all_sp, sorted_personas),
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
