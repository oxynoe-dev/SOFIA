#!/usr/bin/env python3
"""build_dist.py — Generate a static, self-contained dashboard.

Usage:
    python build_dist.py [--output DIR] [--data-dir PATH]

Produces a folder that can be served by any static file server
(nginx, npx serve, python -m http.server) or deployed to GitHub Pages.
No Python backend required — all data is pre-generated JSON.

Examples:
    # Self-contained dist/ (data inside)
    python build_dist.py

    # h2a-data structure (data alongside dashboard)
    python build_dist.py --output ../h2a-data/dashboard --data-dir ../h2a-data/data
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "analysis" / "app"
DATA_DIR = ROOT / "analysis" / "data"
LEGEND_DIR = ROOT / "analysis" / "legend"
DEFAULT_OUTPUT = ROOT / "dist"


def build_dist(output: Path, data_dir: Path | None = None):
    """Build the static distribution.

    Args:
        output: Where to write the dashboard files.
        data_dir: Where to copy JSON data. If None, copies into output/data/.
                  If set, copies there and patches JS paths accordingly.
    """
    # Clean dashboard output
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    # Resolve data destination and JS fetch path
    if data_dir is None:
        data_out = output / "data"
        data_fetch_prefix = "data"
    else:
        data_out = data_dir
        # Compute relative path from dashboard to data for fetch URLs
        try:
            rel = data_out.resolve().relative_to(output.resolve().parent)
            data_fetch_prefix = "../" + str(rel)
        except ValueError:
            data_fetch_prefix = str(data_out.resolve())
        if not data_out.exists():
            data_out.mkdir(parents=True)

    # Copy CSS
    css_out = output / "css"
    css_out.mkdir()
    shutil.copy2(APP_DIR / "css" / "tokens.css", css_out / "tokens.css")

    # Copy JS (with path patching)
    js_out = output / "js"
    js_out.mkdir()
    for jsfile in (APP_DIR / "js").glob("*.js"):
        content = jsfile.read_text(encoding="utf-8")
        if jsfile.name == "app.js":
            content = content.replace("fetch('/lens')", f"fetch('{data_fetch_prefix}/lens.json')")
            content = content.replace("fetch('/mirror')", f"fetch('{data_fetch_prefix}/mirror.json')")
            content = content.replace("fetch('/probe')", f"fetch('{data_fetch_prefix}/probe.json')")
            content = content.replace(
                "fetch('/refresh', { method: 'POST' })",
                "Promise.reject(new Error('Static mode — no server'))"
            )
        if jsfile.name == "legend.js":
            content = content.replace("fetch('/legend')", "fetch('legend/legend.html')")
        if jsfile.name == "probe.js":
            content = content.replace("fetch('/audit', { method: 'POST' })", f"fetch('{data_fetch_prefix}/probe.json')")
        (js_out / jsfile.name).write_text(content, encoding="utf-8")

    # Copy data (JSON) — per instance + aggregated
    data_out.mkdir(parents=True, exist_ok=True)
    for jsonfile in ["lens.json", "mirror.json", "probe.json"]:
        src = DATA_DIR / jsonfile
        if src.is_file():
            shutil.copy2(src, data_out / jsonfile)
        else:
            print(f"  ⚠ {jsonfile} not found — run: python analysis.py <instances>")

    # Copy legend
    legend_out = output / "legend"
    legend_out.mkdir()
    legend_src = LEGEND_DIR / "legend.html"
    if legend_src.is_file():
        shutil.copy2(legend_src, legend_out / "legend.html")

    # Copy HTML (rename to index.html, remove refresh button)
    html_src = ROOT / "analysis.html"
    html_content = html_src.read_text(encoding="utf-8")
    html_content = re.sub(r'<button id="btn-refresh"[^>]*>.*?</button>', '', html_content)
    (output / "index.html").write_text(html_content, encoding="utf-8")

    print(f"✓ Dashboard built → {output}")
    print(f"  Data → {data_out}")
    print(f"  {sum(1 for _ in output.rglob('*') if _.is_file())} dashboard files")
    print(f"  Serve with: cd {output.parent} && python3 -m http.server 8042")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build static dashboard distribution")
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUTPUT), help="Dashboard output directory")
    parser.add_argument("--data-dir", "-d", default=None, help="External data directory (default: output/data/)")
    args = parser.parse_args()

    data_path = Path(args.data_dir).resolve() if args.data_dir else None
    build_dist(Path(args.output).resolve(), data_path)
