#!/usr/bin/env python3
"""aggregate.py — Aggregate per-instance JSON into a unified dataset.

Usage:
    python aggregate.py <data-dir>

Scans <data-dir> for subdirectories containing lens.json / mirror.json,
merges them into unified files at the root of <data-dir>, and generates
an index.json listing available instances.

Idempotent: re-running produces the same output. Adding an instance =
creating a new subdirectory with its JSON files + re-running.

Examples:
    python aggregate.py ../h2a-data/data
    python aggregate.py ../h2a-data/data    # after adding labo-artiste/
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analysis.lib.constants import SCHEMA_VERSION


def _discover_instances(data_dir: Path) -> list[str]:
    """Find subdirectories containing at least one expected JSON file."""
    instances = []
    for sub in sorted(data_dir.iterdir()):
        if not sub.is_dir():
            continue
        if (sub / "lens.json").is_file() or (sub / "mirror.json").is_file():
            instances.append(sub.name)
    return instances


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: dict):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ── Mirror aggregation ──


def _aggregate_mirror(data_dir: Path, instances: list[str]) -> dict:
    """Merge per-instance mirror.json into one unified mirror.json."""
    result = {"instances": {}, "default": instances[0] if instances else None}

    all_friction = []
    all_personas_data: dict[str, dict] = {}
    all_map: dict[str, dict] = {}
    all_personas_set: set[str] = set()

    for inst in instances:
        raw = _load_json(data_dir / inst / "mirror.json")
        if raw is None:
            continue
        # Extract the instance data (it's under instances/<name>)
        inst_data = raw.get("instances", {}).get(inst)
        if inst_data is None:
            # Fallback: take the first (and likely only) instance
            inst_data = next(iter(raw.get("instances", {}).values()), None)
        if inst_data is None:
            continue

        result["instances"][inst] = inst_data

        # Collect for "all" aggregation
        all_friction.extend(inst_data.get("friction_records", []))
        personas = inst_data.get("personas", {})
        for p, pdata in personas.items():
            all_personas_set.add(p)
            if p not in all_personas_data:
                all_personas_data[p] = {
                    "flux_h": 0, "flux_a": 0,
                    "flux_types_h": defaultdict(int),
                    "flux_types_a": defaultdict(int),
                }
            all_personas_data[p]["flux_h"] += pdata.get("flux_h", 0)
            all_personas_data[p]["flux_a"] += pdata.get("flux_a", 0)
            for k, v in pdata.get("flux_types_h", {}).items():
                all_personas_data[p]["flux_types_h"][k] += v
            for k, v in pdata.get("flux_types_a", {}).items():
                all_personas_data[p]["flux_types_a"][k] += v
        if inst_data.get("map"):
            all_map[inst] = inst_data["map"]

    # Finalize personas data (convert defaultdict to dict)
    for p in all_personas_data:
        all_personas_data[p]["flux_types_h"] = dict(all_personas_data[p]["flux_types_h"])
        all_personas_data[p]["flux_types_a"] = dict(all_personas_data[p]["flux_types_a"])

    if len(result["instances"]) > 1:
        sorted_personas = sorted(all_personas_set)
        result["all"] = {
            "meta": {
                "instance": "all",
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "personas": sorted_personas,
            },
            "friction_records": all_friction,
            "personas": all_personas_data,
            "map": {"instances": all_map},
        }

    return result


# ── Lens aggregation ──


def _merge_time_series(all_series: list[dict], granularity: str) -> dict:
    """Merge time series from multiple instances by summing values per label."""
    label_set: set[str] = set()
    marker_keys = ["sound", "contestable", "simplification", "blind_spot", "refuted"]
    direction_keys = ["a_corroborates_h", "a_contests_h", "h_corroborates_a", "h_contests_a"]
    resolution_keys = ["ratified", "contested", "revised", "rejected"]

    for series in all_series:
        ts = series.get("time_series", {}).get(granularity, {})
        label_set.update(ts.get("labels", []))

    labels = sorted(label_set)
    label_idx = {l: i for i, l in enumerate(labels)}
    n = len(labels)

    def _empty_dict(keys: list[str]) -> dict[str, list[int]]:
        return {k: [0] * n for k in keys}

    markers = _empty_dict(marker_keys)
    directions = _empty_dict(direction_keys)
    resolutions = _empty_dict(resolution_keys)
    flux_h = [0] * n
    flux_a = [0] * n
    sessions = [0] * n

    for series in all_series:
        ts = series.get("time_series", {}).get(granularity, {})
        src_labels = ts.get("labels", [])
        for src_i, label in enumerate(src_labels):
            dst_i = label_idx.get(label)
            if dst_i is None:
                continue
            for k in marker_keys:
                vals = ts.get("markers", {}).get(k, [])
                if src_i < len(vals):
                    markers[k][dst_i] += vals[src_i]
            for k in direction_keys:
                vals = ts.get("directions", {}).get(k, [])
                if src_i < len(vals):
                    directions[k][dst_i] += vals[src_i]
            for k in resolution_keys:
                vals = ts.get("resolutions", {}).get(k, [])
                if src_i < len(vals):
                    resolutions[k][dst_i] += vals[src_i]
            fh = ts.get("flux_h", [])
            if src_i < len(fh):
                flux_h[dst_i] += fh[src_i]
            fa = ts.get("flux_a", [])
            if src_i < len(fa):
                flux_a[dst_i] += fa[src_i]
            ss = ts.get("sessions", [])
            if src_i < len(ss):
                sessions[dst_i] += ss[src_i]

    # Compute derived series
    frictions_per_session = []
    resolutions_per_session = []
    for i in range(n):
        total_f = sum(markers[k][i] for k in marker_keys)
        total_r = sum(resolutions[k][i] for k in resolution_keys)
        s = sessions[i] if sessions[i] > 0 else 1
        frictions_per_session.append(round(total_f / s, 2))
        resolutions_per_session.append(round(total_r / s, 2))

    return {
        "labels": labels,
        "markers": markers,
        "directions": directions,
        "resolutions": resolutions,
        "flux_h": flux_h,
        "flux_a": flux_a,
        "sessions": sessions,
        "frictions_per_session": frictions_per_session,
        "resolutions_per_session": resolutions_per_session,
    }


def _aggregate_lens(data_dir: Path, instances: list[str]) -> dict:
    """Merge per-instance lens.json into one unified lens.json."""
    result = {"instances": {}, "default": instances[0] if instances else None}

    all_inst_data = []
    all_personas_set: set[str] = set()
    total_sessions = 0
    total_artifacts = 0
    total_sp = 0

    for inst in instances:
        raw = _load_json(data_dir / inst / "lens.json")
        if raw is None:
            continue
        inst_data = raw.get("instances", {}).get(inst)
        if inst_data is None:
            inst_data = next(iter(raw.get("instances", {}).values()), None)
        if inst_data is None:
            continue

        result["instances"][inst] = inst_data
        all_inst_data.append(inst_data)
        all_personas_set.update(inst_data.get("meta", {}).get("personas", []))
        total_sessions += inst_data.get("meta", {}).get("sessions_scanned", 0)
        total_artifacts += inst_data.get("meta", {}).get("artifacts_scanned", 0)
        total_sp += inst_data.get("totals", {}).get("signaler_pattern", 0)

    if len(result["instances"]) > 1:
        sorted_personas = sorted(all_personas_set)

        # Merge persona-level data
        merged_personas: dict[str, dict] = {}
        sum_keys = [
            "frictions", "flux_h", "flux_a", "sessions",
            "signaler_pattern_count", "signaler_pattern_erreur_llm",
            "signaler_pattern_conviction", "signaler_pattern_resistance",
        ]
        marker_keys = ["sound", "contestable", "simplification", "blind_spot", "refuted"]
        direction_keys = ["a_corroborates_h", "a_contests_h", "h_corroborates_a", "h_contests_a"]
        resolution_keys = ["ratified", "contested", "revised", "rejected"]

        for inst_data in all_inst_data:
            for p, pdata in inst_data.get("personas", {}).items():
                if p not in merged_personas:
                    merged_personas[p] = {
                        "markers": {k: 0 for k in marker_keys},
                        "directions": {k: 0 for k in direction_keys},
                        "resolutions": {k: 0 for k in resolution_keys},
                        "flux_types_h": defaultdict(int),
                        "flux_types_a": defaultdict(int),
                    }
                    for sk in sum_keys:
                        merged_personas[p][sk] = 0
                for sk in sum_keys:
                    merged_personas[p][sk] += pdata.get(sk, 0)
                for k in marker_keys:
                    merged_personas[p]["markers"][k] += pdata.get("markers", {}).get(k, 0)
                for k in direction_keys:
                    merged_personas[p]["directions"][k] += pdata.get("directions", {}).get(k, 0)
                for k in resolution_keys:
                    merged_personas[p]["resolutions"][k] += pdata.get("resolutions", {}).get(k, 0)
                for k, v in pdata.get("flux_types_h", {}).items():
                    merged_personas[p]["flux_types_h"][k] += v
                for k, v in pdata.get("flux_types_a", {}).items():
                    merged_personas[p]["flux_types_a"][k] += v

        # Finalize: compute derived fields + convert defaultdict
        for p, pdata in merged_personas.items():
            pdata["flux_types_h"] = dict(pdata["flux_types_h"])
            pdata["flux_types_a"] = dict(pdata["flux_types_a"])
            total_h = pdata.get("flux_h", 0)
            total_a = pdata.get("flux_a", 0)
            total_flux = total_h + total_a
            pdata["flux_h_pct"] = round(100 * total_h / total_flux) if total_flux else 0
            pdata["flux_a_pct"] = round(100 * total_a / total_flux) if total_flux else 0
            ac = pdata["directions"].get("a_contests_h", 0)
            hc = pdata["directions"].get("h_contests_a", 0)
            pdata["direction_ratio"] = round(ac / hc, 2) if hc > 0 else ac

        result["all"] = {
            "meta": {
                "instance": "all",
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "personas": sorted_personas,
                "sessions_scanned": total_sessions,
                "artifacts_scanned": total_artifacts,
            },
            "totals": {"signaler_pattern": total_sp},
            "time_series": {
                "week": _merge_time_series(all_inst_data, "week"),
                "day": _merge_time_series(all_inst_data, "day"),
            },
            "personas": merged_personas,
        }

    return result


# ── Index ──


def _build_index(data_dir: Path, instances: list[str]) -> dict:
    """Build index.json with instance metadata."""
    index: dict = {
        "instances": instances,
        "generated": datetime.now(timezone.utc).isoformat(),
    }
    return index


# ── Main ──


def _check_schema_version(data_dir: Path, instances: list[str]) -> bool:
    """Check that all per-instance JSON share a compatible schema_version."""
    versions = set()
    for inst in instances:
        for jsonfile in ["lens.json", "mirror.json"]:
            raw = _load_json(data_dir / inst / jsonfile)
            if raw and "schema_version" in raw:
                versions.add(raw["schema_version"])
    if not versions:
        print("  ⚠ No schema_version found — legacy data, proceeding")
        return True
    if len(versions) > 1:
        print(f"  ✗ Incompatible schema versions across instances: {versions}", file=sys.stderr)
        return False
    found = versions.pop()
    if found != SCHEMA_VERSION:
        print(f"  ✗ Schema version mismatch: data={found}, expected={SCHEMA_VERSION}. Re-run analysis.py.", file=sys.stderr)
        return False
    return True


def aggregate(data_dir: Path):
    """Run full aggregation on a data directory."""
    instances = _discover_instances(data_dir)
    if not instances:
        print(f"⚠ No instances found in {data_dir}")
        return

    if not _check_schema_version(data_dir, instances):
        sys.exit(1)

    print(f"Found {len(instances)} instance(s): {', '.join(instances)}")

    # Collect sofia_versions from per-instance JSON
    sofia_versions = {}
    for inst in instances:
        raw = _load_json(data_dir / inst / "mirror.json") or _load_json(data_dir / inst / "lens.json")
        if raw and "sofia_versions" in raw:
            sofia_versions.update(raw["sofia_versions"])

    def _stamp(data: dict) -> dict:
        data["schema_version"] = SCHEMA_VERSION
        data["generated"] = datetime.now(timezone.utc).isoformat()
        if sofia_versions:
            data["sofia_versions"] = sofia_versions
        return data

    # Index
    index = _build_index(data_dir, instances)
    _write_json(data_dir / "index.json", _stamp(index))
    print(f"  ✓ index.json")

    # Mirror
    mirror = _aggregate_mirror(data_dir, instances)
    if mirror["instances"]:
        _write_json(data_dir / "mirror.json", _stamp(mirror))
        print(f"  ✓ mirror.json — {len(mirror['instances'])} instance(s)")

    # Lens
    lens = _aggregate_lens(data_dir, instances)
    if lens["instances"]:
        _write_json(data_dir / "lens.json", _stamp(lens))
        print(f"  ✓ lens.json — {len(lens['instances'])} instance(s)")

    print(f"✓ Aggregation complete → {data_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Aggregate per-instance JSON into unified dataset"
    )
    parser.add_argument("data_dir", help="Data directory containing instance subdirectories")
    args = parser.parse_args()

    aggregate(Path(args.data_dir).resolve())
