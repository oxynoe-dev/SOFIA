#!/usr/bin/env python3
"""build_dist.py — Generate a static, self-contained dashboard.

Usage:
    python build_dist.py [--output DIR] [--data-dir PATH] [--sanitize]

Produces a folder that can be served by any static file server
(nginx, npx serve, python -m http.server) or deployed to GitHub Pages.
No Python backend required — all data is pre-generated JSON.

Examples:
    # Self-contained dist/ (data inside)
    python build_dist.py

    # h2a-data structure (data alongside dashboard)
    python build_dist.py --output ../h2a-data/dashboard --data-dir ../h2a-data/data

    # Sanitized for open-source publication (strips descriptions, sources, filenames)
    python build_dist.py --data-dir ../h2a-data/data --sanitize
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "analysis" / "app"
DATA_DIR = ROOT / "analysis" / "data"
LEGEND_DIR = ROOT / "analysis" / "legend"
DEFAULT_OUTPUT = ROOT / "dist"


def build_dist(output: Path, data_dir: Path | None = None, sanitize: bool = False):
    """Build the static distribution.

    Args:
        output: Where to write the dashboard files.
        data_dir: Where to copy JSON data. If None, copies into output/data/.
                  If set, copies there and patches JS paths accordingly.
        sanitize: If True, strip sensitive fields before copying JSON.
    """
    # Clean only generated artifacts (preserve .git, README, etc.)
    output.mkdir(parents=True, exist_ok=True)
    for sub in ["css", "js", "data", "legend"]:
        target = output / sub
        if target.is_dir():
            shutil.rmtree(target)
    index = output / "index.html"
    if index.is_file():
        index.unlink()

    # Resolve data destination and JS fetch path
    # Data is always copied INTO dashboard/data/ so the bundle is self-contained.
    # If --data-dir is set, data is ALSO copied there (for the repo structure).
    data_out = output / "data"
    data_fetch_prefix = "data"
    external_data_dir = data_dir

    # Copy CSS
    css_out = output / "css"
    css_out.mkdir()
    shutil.copy2(APP_DIR / "css" / "tokens.css", css_out / "tokens.css")

    # Copy JS (with path patching)
    js_out = output / "js"
    js_out.mkdir()
    for jsfile in (APP_DIR / "js").glob("*.js"):
        if jsfile.name == "probe.js":
            continue  # Probe is not included in static builds
        content = jsfile.read_text(encoding="utf-8")
        if jsfile.name == "app.js":
            content = content.replace("fetch('/lens')", f"fetch('{data_fetch_prefix}/lens.json')")
            content = content.replace("fetch('/mirror')", f"fetch('{data_fetch_prefix}/mirror.json')")
            content = content.replace("fetch('/probe')", f"fetch('{data_fetch_prefix}/probe.json')")
            content = content.replace(
                "fetch('/refresh', { method: 'POST' })",
                "Promise.reject(new Error('Static mode — no server'))"
            )
            # Remove probe references from switchTab
            content = content.replace(
                "const subMenu = document.getElementById('probe-instances-menu');",
                "const subMenu = null;"
            )
            content = content.replace(
                "subMenu.classList.toggle('visible', tab === 'probe');",
                "if (subMenu) subMenu.classList.toggle('visible', tab === 'probe');"
            )
            content = content.replace(
                "if (tab === 'probe' && !PROBE_DATA) runProbe();",
                ""
            )
            content = content.replace(
                "const noSidebar = (tab === 'probe' || tab === 'map' || tab === 'legend');",
                "const noSidebar = (tab === 'map' || tab === 'legend');"
            )
            content = content.replace(
                "if (tab === 'probe') t.style.paddingTop = '36px';\n    else t.style.paddingTop = '';",
                "t.style.paddingTop = '';"
            )
            # Remove probe from context menu
            content = re.sub(
                r".*navigateTo\('probe'.*\n",
                "",
                content
            )
        if jsfile.name == "legend.js":
            content = content.replace("fetch('/legend')", "fetch('legend/legend.html')")
        (js_out / jsfile.name).write_text(content, encoding="utf-8")

    # Copy data (JSON) — into dashboard/data/ (self-contained)
    # If --sanitize, strip sensitive fields (descriptions, sources, filenames)
    sanitizer = None
    if sanitize:
        from sanitize import (
            sanitize_lens, sanitize_mirror, sanitize_probe, sanitize_records,
        )
        sanitizer = {
            "records.json": sanitize_records,
            "lens.json": sanitize_lens,
            "mirror.json": sanitize_mirror,
            "probe.json": sanitize_probe,
        }
        print("  🔒 Sanitize mode — stripping sensitive fields")

    # Read from external data dir if provided, otherwise from internal DATA_DIR
    data_src = external_data_dir if external_data_dir and external_data_dir.is_dir() else DATA_DIR

    data_out.mkdir(parents=True, exist_ok=True)
    for jsonfile in ["lens.json", "mirror.json"]:
        src = data_src / jsonfile
        if src.is_file():
            if sanitizer and jsonfile in sanitizer:
                with open(src) as f:
                    data = json.load(f)
                data = sanitizer[jsonfile](data)
                with open(data_out / jsonfile, "w") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                if external_data_dir:
                    external_data_dir.mkdir(parents=True, exist_ok=True)
                    with open(external_data_dir / jsonfile, "w") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                shutil.copy2(src, data_out / jsonfile)
                if external_data_dir and external_data_dir.resolve() != data_src.resolve():
                    external_data_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, external_data_dir / jsonfile)
        else:
            print(f"  ⚠ {jsonfile} not found — run: python analysis.py <instances>")

    # Copy legend
    legend_out = output / "legend"
    legend_out.mkdir()
    legend_src = LEGEND_DIR / "legend.html"
    if legend_src.is_file():
        shutil.copy2(legend_src, legend_out / "legend.html")

    # Copy HTML (rename to index.html, remove refresh button + probe tab)
    html_src = ROOT / "analysis.html"
    html_content = html_src.read_text(encoding="utf-8")
    html_content = re.sub(r'<button id="btn-refresh"[^>]*>.*?</button>', '', html_content)
    # Remove Probe nav button
    html_content = re.sub(r"<li><button onclick=\"switchTab\('probe'\)\">Probe</button></li>", '', html_content)
    # Remove Probe sub-menu
    html_content = re.sub(r'<div class="sub-menu" id="probe-instances-menu"></div>', '', html_content)
    # Remove Probe tab content
    html_content = re.sub(r'<div id="tab-probe".*?</div><!-- /tab-probe -->', '', html_content, flags=re.DOTALL)
    # Remove Probe script
    html_content = re.sub(r'<script src="js/probe.js"></script>', '', html_content)
    # Remove Probe from legend TOC
    html_content = re.sub(r'<a href="#probe"[^>]*>Probe</a>', '', html_content)
    # Clean Probe from description text
    html_content = html_content.replace(' · <strong>Probe</strong> = conformity audit', '')
    (output / "index.html").write_text(html_content, encoding="utf-8")

    print(f"✓ Dashboard built → {output}")
    if external_data_dir:
        print(f"  Data also copied → {external_data_dir}")
    print(f"  {sum(1 for _ in output.rglob('*') if _.is_file())} files")
    print(f"  Serve with: cd {output} && python3 -m http.server 8042")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build static dashboard distribution")
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUTPUT), help="Dashboard output directory")
    parser.add_argument("--data-dir", "-d", default=None, help="External data directory (default: output/data/)")
    parser.add_argument("--sanitize", action="store_true", help="Strip sensitive fields for open-source publication")
    args = parser.parse_args()

    data_path = Path(args.data_dir).resolve() if args.data_dir else None
    build_dist(Path(args.output).resolve(), data_path, args.sanitize)
