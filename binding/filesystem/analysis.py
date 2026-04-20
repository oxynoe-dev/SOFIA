#!/usr/bin/env python3
"""analysis.py — Single entry point for the H2A analysis pipeline.

Usage:
    python analysis.py <instance> [<instance> ...] [--only mirror|lens|probe] [--serve]

Orchestrates:
    1. scan.py  → records.json     (internal, called by mirror/lens)
    2. mirror.py → mirror.json     (Map + Mirror views)
    3. lens.py   → lens.json       (Lens view — time series)
    4. probe.py  → probe.json      (Probe view — conformity)

All outputs go to analysis/data/ (gitignored).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure imports work
sys.path.insert(0, str(Path(__file__).resolve().parent))

from analysis.cli.scan import scan_instances, write_records
from analysis.cli.mirror import build_mirror, write_mirror
from analysis.cli.lens import build_lens, write_lens
from analysis.cli.probe import probe_instances, write_probe

DATA_DIR = Path(__file__).resolve().parent / "analysis" / "data"


def run_pipeline(instance_paths: list[Path], only: str | None = None):
    """Run the full analysis pipeline (or a single view)."""

    views = {"mirror", "lens", "probe"}
    if only and only not in views:
        print(f"✗ Unknown view: {only}. Choose from: {', '.join(sorted(views))}", file=sys.stderr)
        sys.exit(1)

    targets = {only} if only else views

    # --- Data pipeline (scan + mirror + lens) ---
    if targets & {"mirror", "lens"}:
        print("  Scanning instances...")
        records = scan_instances(instance_paths)
        records_path = DATA_DIR / "records.json"
        write_records(records, records_path)

        total_f = sum(len(d["friction_records"]) for d in records.values())
        print(f"  ✓ records.json — {total_f} frictions")

        if "mirror" in targets:
            mirror = build_mirror(records)
            write_mirror(mirror)
            print(f"  ✓ mirror.json — {len(mirror['instances'])} instances")

        if "lens" in targets:
            lens = build_lens(records)
            write_lens(lens)
            print(f"  ✓ lens.json — {len(lens['instances'])} instances")

    # --- Conformity pipeline (probe) ---
    if "probe" in targets:
        print("  Probing instances...")
        probe_data = probe_instances(instance_paths)
        write_probe(probe_data)
        for name, data in probe_data.items():
            checks = data["structure"]["checks"]
            passed = sum(1 for c in checks if c["status"] == "pass")
            warns = sum(1 for c in checks if c["status"] == "warn")
            print(f"  ✓ probe.json — {name}: {passed} pass, {warns} warn")


def main():
    parser = argparse.ArgumentParser(
        description="H2A analysis pipeline — single entry point",
        epilog="Examples:\n"
               "  python analysis.py ../methodes ../produits ../oxynoe\n"
               "  python analysis.py ../methodes --only probe\n"
               "  python analysis.py ../methodes ../produits --serve\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("instances", nargs="+", help="Path(s) to SOFIA instance root(s)")
    parser.add_argument("--only", choices=["mirror", "lens", "probe"],
                        help="Run only one view (default: all)")
    parser.add_argument("--serve", action="store_true",
                        help="Start the dashboard server after analysis")
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

    run_pipeline(instance_paths, only=args.only)

    if args.serve:
        print(f"\n  Starting server on http://localhost:{args.port}")
        # Import and run serve.py
        from analysis.app.serve import run_server
        run_server(instance_paths, args.port)

    print("\n✓ Done.")


if __name__ == "__main__":
    main()
