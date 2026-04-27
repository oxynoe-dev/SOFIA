#!/usr/bin/env python3
"""analysis.py — Single entry point for the H2A analysis pipeline.

Usage:
    python analysis.py <instance> [<instance> ...] [--only mirror|lens|probe] [--output DIR] [--sanitize] [--serve]

Orchestrates:
    1. scan.py  → records.json     (internal, called by mirror/lens)
    2. mirror.py → mirror.json     (Map + Mirror views)
    3. lens.py   → lens.json       (Lens view — time series)
    4. probe.py  → probe.json      (Probe view — conformity)

Output structure (per-instance + aggregated):
    <output>/
    ├── methodes/         per-instance
    │   ├── lens.json
    │   ├── mirror.json
    │   └── records.json
    ├── produits/         per-instance
    │   └── ...
    ├── lens.json         aggregated (all instances)
    ├── mirror.json       aggregated
    └── index.json        instance list

Default output: analysis/data/ (gitignored).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure imports work
sys.path.insert(0, str(Path(__file__).resolve().parent))

from analysis.cli.scan import scan_instances, write_records
from analysis.cli.mirror import build_mirror, write_mirror
from analysis.cli.lens import build_lens, write_lens
from analysis.cli.probe import probe_instances, write_probe
from analysis.lib.constants import SCHEMA_VERSION, get_instance_sofia_version
from sanitize import sanitize_records, sanitize_mirror, sanitize_lens, sanitize_probe

DATA_DIR = Path(__file__).resolve().parent / "analysis" / "data"


def _stamp(data: dict, sofia_versions: dict[str, str] | None = None) -> dict:
    """Inject schema_version and sofia_versions into a JSON dict."""
    data["schema_version"] = SCHEMA_VERSION
    data["generated"] = datetime.now(timezone.utc).isoformat()
    if sofia_versions:
        data["sofia_versions"] = sofia_versions
    return data


def _write_index(out: Path, instances: list[str]):
    """Write index.json listing available instances."""
    index = {
        "instances": instances,
        "generated": datetime.now(timezone.utc).isoformat(),
    }
    (out / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def run_pipeline(instance_paths: list[Path], only: str | None = None,
                  output_dir: Path | None = None, sanitize: bool = False):
    """Run the full analysis pipeline (or a single view).

    Writes per-instance JSON into <output>/<instance>/ and aggregated
    JSON at <output>/ root.

    Args:
        instance_paths: Paths to SOFIA instance roots.
        only: Run only one view (mirror, lens, probe).
        output_dir: Where to write JSON files. Defaults to analysis/data/.
        sanitize: If True, strip sensitive fields before writing.
    """
    out = output_dir if output_dir else DATA_DIR

    views = {"mirror", "lens", "probe"}
    if only and only not in views:
        print(f"✗ Unknown view: {only}. Choose from: {', '.join(sorted(views))}", file=sys.stderr)
        sys.exit(1)

    targets = {only} if only else views

    # Collect protocol versions from each instance's sofia.md
    instance_path_map = {p.name: p for p in instance_paths}
    sofia_versions = {p.name: get_instance_sofia_version(p) for p in instance_paths}

    # --- Data pipeline (scan + mirror + lens) ---
    if targets & {"mirror", "lens"}:
        print("  Scanning instances...")
        records = scan_instances(instance_paths)

        # Write per-instance JSON
        for inst_name, inst_data in records.items():
            inst_out = out / inst_name
            inst_out.mkdir(parents=True, exist_ok=True)
            single = {inst_name: inst_data}
            records_out = single
            if sanitize:
                records_out = sanitize_records(records_out)
            write_records(records_out, inst_out / "records.json")

            inst_ver = {inst_name: sofia_versions.get(inst_name, "unknown")}
            if "mirror" in targets:
                mirror_single = build_mirror(single)
                if sanitize:
                    mirror_single = sanitize_mirror(mirror_single)
                write_mirror(_stamp(mirror_single, inst_ver), inst_out / "mirror.json")

            if "lens" in targets:
                lens_single = build_lens(single)
                if sanitize:
                    lens_single = sanitize_lens(lens_single)
                write_lens(_stamp(lens_single, inst_ver), inst_out / "lens.json")

            print(f"  ✓ {inst_name}/ — per-instance JSON")

        # Write aggregated JSON at root
        total_f = sum(len(d["friction_records"]) for d in records.values())
        records_agg = records
        if sanitize:
            records_agg = sanitize_records(records_agg)
        write_records(records_agg, out / "records.json")
        print(f"  ✓ records.json — {total_f} frictions (aggregated)")

        if "mirror" in targets:
            mirror = build_mirror(records)
            if sanitize:
                mirror = sanitize_mirror(mirror)
            write_mirror(_stamp(mirror, sofia_versions), out / "mirror.json")
            print(f"  ✓ mirror.json — {len(mirror['instances'])} instances (aggregated)")

        if "lens" in targets:
            lens = build_lens(records)
            if sanitize:
                lens = sanitize_lens(lens)
            write_lens(_stamp(lens, sofia_versions), out / "lens.json")
            print(f"  ✓ lens.json — {len(lens['instances'])} instances (aggregated)")

        # Write index
        instance_names = sorted(records.keys())
        _write_index(out, instance_names)
        print(f"  ✓ index.json — {len(instance_names)} instances")

    # --- Conformity pipeline (probe) ---
    if "probe" in targets:
        print("  Probing instances...")
        probe_data = probe_instances(instance_paths)
        # Write per-instance probe
        for inst_name, inst_probe in probe_data.items():
            inst_out = out / inst_name
            inst_out.mkdir(parents=True, exist_ok=True)
            probe_single = {inst_name: inst_probe}
            if sanitize:
                probe_single = sanitize_probe(probe_single)
            inst_ver = {inst_name: sofia_versions.get(inst_name, "unknown")}
            write_probe(_stamp(probe_single, inst_ver), inst_out / "probe.json")
        # Print summary before stamping (stamp mutates the dict)
        for name, pdata in probe_data.items():
            checks = pdata["structure"]["checks"]
            passed = sum(1 for c in checks if c["status"] == "pass")
            warns = sum(1 for c in checks if c["status"] == "warn")
            print(f"  ✓ probe.json — {name}: {passed} pass, {warns} warn")
        # Write aggregated probe
        probe_agg = probe_data
        if sanitize:
            probe_agg = sanitize_probe(probe_agg)
        write_probe(_stamp(probe_agg, sofia_versions), out / "probe.json")


def main():
    parser = argparse.ArgumentParser(
        description="H2A analysis pipeline — single entry point",
        epilog="Examples:\n"
               "  python analysis.py ../methodes ../produits ../oxynoe\n"
               "  python analysis.py ../methodes --only probe\n"
               "  python analysis.py ../methodes ../produits -o ../h2a-data/data\n"
               "  python analysis.py ../methodes ../produits -o ../h2a-data/data --sanitize\n"
               "  python analysis.py ../methodes ../produits --serve\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("instances", nargs="+", help="Path(s) to SOFIA instance root(s)")
    parser.add_argument("--only", choices=["mirror", "lens", "probe"],
                        help="Run only one view (default: all)")
    parser.add_argument("--serve", action="store_true",
                        help="Start the dashboard server after analysis")
    parser.add_argument("--output", "-o", default=None,
                        help="Output directory for JSON files (default: analysis/data/)")
    parser.add_argument("--sanitize", action="store_true",
                        help="Strip sensitive fields for open-source publication")
    parser.add_argument("--port", type=int, default=8042,
                        help="Server port (default: 8042)")
    args = parser.parse_args()

    # Validate instances
    instance_paths = []
    for p in args.instances:
        resolved = Path(p).resolve()
        if not (resolved / "sofia.md").is_file() and not (resolved / "voix.md").is_file():
            print(f"  ⚠ Skipping (no sofia.md): {resolved}", file=sys.stderr)
            continue
        instance_paths.append(resolved)

    if not instance_paths:
        print("✗ No valid instances found.", file=sys.stderr)
        sys.exit(1)

    names = ", ".join(p.name for p in instance_paths)
    print(f"✓ H2A Analysis Pipeline")
    print(f"  Instances: {names}")

    output_dir = Path(args.output).resolve() if args.output else None
    if output_dir:
        print(f"  Output: {output_dir}")
    if args.sanitize:
        print(f"  🔒 Sanitize mode — stripping sensitive fields")
    run_pipeline(instance_paths, only=args.only, output_dir=output_dir,
                 sanitize=args.sanitize)

    if args.serve:
        print(f"\n  Starting server on http://localhost:{args.port}")
        # Import and run serve.py
        from analysis.app.serve import run_server
        run_server(instance_paths, args.port)

    print("\n✓ Done.")


if __name__ == "__main__":
    main()
