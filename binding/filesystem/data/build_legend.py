#!/usr/bin/env python3
"""Build legend.html from doc/legend.md.

Usage:
    python build_legend.py

Reads ../../doc/legend.md, converts to HTML fragment, writes legend.html
next to analysis.html (in filesystem/).

Zero external dependency — Python 3.10+ stdlib only.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent  # data/
FILESYSTEM = HERE.parent               # filesystem/
SOFIA_ROOT = FILESYSTEM.parent.parent   # sofia/
LEGEND_MD = SOFIA_ROOT / "doc" / "legend.md"
OUTPUT = FILESYSTEM / "legend.html"


def inline_format(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r'<strong style="color:var(--ice)">\1</strong>', s)
    s = re.sub(r"`(.+?)`", r'<code>\1</code>', s)
    return s


def render_markdown(md: str) -> str:
    lines = md.split("\n")
    html = []
    in_table = False
    in_list = False

    for i, line in enumerate(lines):
        trimmed = line.strip()

        # Skip frontmatter
        if trimmed == "---" and i < 5:
            continue

        # Headers
        if trimmed.startswith("# "):
            if in_table: html.append("</tbody></table>"); in_table = False
            if in_list: html.append("</ul>"); in_list = False
            html.append(f'<h1>{trimmed[2:]}</h1>')

        elif trimmed.startswith("## "):
            if in_table: html.append("</tbody></table>"); in_table = False
            if in_list: html.append("</ul>"); in_list = False
            anchor = re.sub(r"[^a-z0-9]+", "-", trimmed[3:].lower()).strip("-")
            html.append(f'<h2 id="{anchor}">{trimmed[3:]}</h2>')

        elif trimmed.startswith("### "):
            if in_table: html.append("</tbody></table>"); in_table = False
            if in_list: html.append("</ul>"); in_list = False
            html.append(f'<h3>{trimmed[4:]}</h3>')

        # Horizontal rule
        elif trimmed == "---" and i > 5:
            if in_table: html.append("</tbody></table>"); in_table = False
            if in_list: html.append("</ul>"); in_list = False
            html.append('<hr style="border:none; border-top:1px solid var(--border); margin:2rem 0;">')

        # Table
        elif trimmed.startswith("|"):
            cells = [c.strip() for c in trimmed.split("|")[1:-1]]
            if all(re.match(r"^[-:]+$", c) for c in cells):
                continue
            if not in_table:
                if in_list: html.append("</ul>"); in_list = False
                html.append("<table><thead><tr>")
                html.extend(f"<th>{inline_format(c)}</th>" for c in cells)
                html.append("</tr></thead><tbody>")
                in_table = True
            else:
                html.append("<tr>")
                html.extend(f"<td>{inline_format(c)}</td>" for c in cells)
                html.append("</tr>")

        # List
        elif trimmed.startswith("- "):
            if in_table: html.append("</tbody></table>"); in_table = False
            if not in_list: html.append("<ul>"); in_list = True
            html.append(f"<li>{inline_format(trimmed[2:])}</li>")

        # Empty
        elif trimmed == "":
            if in_table: html.append("</tbody></table>"); in_table = False
            if in_list: html.append("</ul>"); in_list = False

        # Paragraph
        else:
            if in_table: html.append("</tbody></table>"); in_table = False
            if in_list: html.append("</ul>"); in_list = False
            html.append(f"<p>{inline_format(trimmed)}</p>")

    if in_table: html.append("</tbody></table>")
    if in_list: html.append("</ul>")
    return "\n".join(html)


def main():
    if not LEGEND_MD.is_file():
        print(f"✗ {LEGEND_MD} not found")
        return

    md = LEGEND_MD.read_text(encoding="utf-8")
    body = render_markdown(md)

    OUTPUT.write_text(body + "\n", encoding="utf-8")
    print(f"✓ {OUTPUT.relative_to(SOFIA_ROOT)}")


if __name__ == "__main__":
    main()
