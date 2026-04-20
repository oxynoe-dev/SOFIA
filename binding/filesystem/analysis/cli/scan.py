"""scan.py — Scan SOFIA instances and produce records.json.

Internal module — called by mirror.py and lens.py, not directly by the user.
Extracts friction records, exchange records, and contribution records
from sessions and artifacts.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from analysis.lib.constants import FRICTION_MARKERS, RESOLUTION_TAGS, strip_accents
from analysis.lib.parser import (
    parse_frontmatter,
    normalize_frontmatter,
    parse_friction_lines,
    parse_flux_lines,
    parse_signaler_pattern,
    parse_session_date,
    parse_artifact_date,
    parse_artifact_persona,
    compute_direction,
    find_artifacts,
    resolve_lineage,
    date_to_week,
    discover_personas,
)


# ---------------------------------------------------------------------------
# Scan instance → records
# ---------------------------------------------------------------------------

def scan_instance(instance_path: Path) -> dict:
    """Scan an instance and return raw records.

    Returns:
        {
            "meta": {...},
            "friction_records": [...],
            "contribution_records": [...],
            "signaler_patterns": [...],
            "personas": [...],
        }
    """
    real_personas = sorted(discover_personas(instance_path))

    # --- Sessions ---
    session_files = sorted(instance_path.rglob("sessions/*.md"))
    session_files = [f for f in session_files if "shared" not in f.relative_to(instance_path).parts]

    friction_records: list[dict] = []
    contribution_records: list[dict] = []
    signaler_patterns: list[dict] = []

    for filepath in session_files:
        fm = parse_frontmatter(filepath)
        if fm is None:
            continue

        persona = fm.get("persona", "").strip()
        if not persona:
            continue
        persona = strip_accents(persona.lower())

        session_date = parse_session_date(filepath)
        if not session_date:
            continue

        try:
            text = filepath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        # Friction
        for rec in parse_friction_lines(text):
            direction = compute_direction(rec["initiative"], rec["marker"])
            friction_records.append({
                "persona": persona,
                "date": session_date,
                "week": date_to_week(session_date),
                "source": filepath.relative_to(instance_path).as_posix(),
                "source_type": "session",
                "marker": rec["marker"],
                "initiative": rec["initiative"],
                "direction": direction,
                "resolution": rec["resolution"],
                "description": rec.get("description", ""),
                "ref": rec.get("ref"),
            })

        # Contributions
        for rec in parse_flux_lines(text):
            contribution_records.append({
                "persona": persona,
                "date": session_date,
                "week": date_to_week(session_date),
                "source": filepath.relative_to(instance_path).as_posix(),
                "direction": rec["direction"],
                "type": rec["type"],
            })

        # signalerPattern
        sp = parse_signaler_pattern(text)
        if sp is not None:
            sp["persona"] = persona
            sp["session"] = filepath.stem
            sp["date"] = session_date
            signaler_patterns.append(sp)

    # --- Artifacts from shared/ ---
    for filepath in find_artifacts(instance_path):
        persona = parse_artifact_persona(filepath)
        if not persona:
            continue
        persona = strip_accents(persona.lower())

        artifact_date = parse_artifact_date(filepath)
        if not artifact_date:
            continue

        try:
            text = filepath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        for rec in parse_friction_lines(text):
            direction = compute_direction(rec["initiative"], rec["marker"])
            friction_records.append({
                "persona": persona,
                "date": artifact_date,
                "week": date_to_week(artifact_date),
                "source": filepath.relative_to(instance_path).as_posix(),
                "source_type": "artifact",
                "marker": rec["marker"],
                "initiative": rec["initiative"],
                "direction": direction,
                "resolution": rec["resolution"],
                "description": rec.get("description", ""),
                "ref": rec.get("ref"),
            })

    # Resolve lineage
    friction_records = resolve_lineage(
        sorted(friction_records, key=lambda r: r.get("date", ""))
    )

    return {
        "meta": {
            "instance": instance_path.name,
            "date": date.today().isoformat(),
            "personas": real_personas,
            "sessions_scanned": len(session_files),
            "artifacts_scanned": len(find_artifacts(instance_path)),
        },
        "friction_records": friction_records,
        "contribution_records": contribution_records,
        "signaler_patterns": signaler_patterns,
    }


def scan_instances(instance_paths: list[Path]) -> dict:
    """Scan multiple instances and return combined records."""
    all_records = {}
    for path in instance_paths:
        name = path.name
        all_records[name] = scan_instance(path)
    return all_records


def write_records(records: dict, output_path: Path):
    """Write records to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# CLI (for direct testing)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scan SOFIA instances → records.json")
    parser.add_argument("instances", nargs="+", help="Instance paths")
    parser.add_argument("--output", default=str(Path(__file__).resolve().parent.parent / "data" / "records.json"))
    args = parser.parse_args()

    paths = [Path(p).resolve() for p in args.instances]
    records = scan_instances(paths)
    write_records(records, Path(args.output))

    total_frictions = sum(len(d["friction_records"]) for d in records.values())
    total_contribs = sum(len(d["contribution_records"]) for d in records.values())
    print(f"✓ {args.output}")
    for name, data in records.items():
        print(f"  {name}: {len(data['friction_records'])} frictions, {len(data['contribution_records'])} contributions")
    print(f"  total: {total_frictions} frictions, {total_contribs} contributions")
