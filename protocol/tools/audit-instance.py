#!/usr/bin/env python3
"""audit-instance.py — Scan a SOFIA instance and produce exchange + friction matrices.

Usage:
    python audit-instance.py <instance-path>

Outputs:
    audit-echanges.json   — who talks to whom (volume)
    audit-friction.json   — who challenges whom (reviews + signals) + friction markers
    stdout                — formatted report

Zero external dependency — Python 3.10+ stdlib only.
"""
from __future__ import annotations

import sys
import json
import re
from pathlib import Path
from datetime import date
from collections import defaultdict

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FRICTION_MARKERS = {
    "✓": "juste",
    "~": "contestable",
    "⚡": "simplification",
    "◐": "angle_mort",
    "✗": "faux",
}

# Alias normalization for frontmatter fields
EMITTER_KEYS = {"de", "auteur", "emetteur", "from"}
RECIPIENT_KEYS = {"pour", "destinataire", "destinataires", "to"}
NATURE_KEYS = {"nature", "type"}

# Accent normalization
_ACCENT_MAP = str.maketrans(
    "àâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ",
    "aaaeeeeiioouuycAAAEEEEIIOOUUYC",
)


def strip_accents(s: str) -> str:
    return s.translate(_ACCENT_MAP)

# ---------------------------------------------------------------------------
# Frontmatter parser
# ---------------------------------------------------------------------------

def parse_frontmatter(filepath: Path) -> dict | None:
    """Parse YAML frontmatter between --- delimiters. Returns None if absent."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    if not text.startswith("---"):
        return None

    end = text.find("---", 3)
    if end == -1:
        return None

    fm = {}
    for line in text[3:end].strip().splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip().lower()] = value.strip()

    return fm if fm else None


def normalize_frontmatter(fm: dict) -> dict:
    """Normalize frontmatter fields to canonical names."""
    result = {}

    # emitter
    for k in EMITTER_KEYS:
        if k in fm:
            result["de"] = strip_accents(fm[k].lower().strip())
            break

    # recipient(s)
    for k in RECIPIENT_KEYS:
        if k in fm:
            raw = fm[k].lower().strip()
            # split on comma or space
            recipients = [strip_accents(r.strip()) for r in re.split(r"[,\s]+", raw) if r.strip()]
            result["pour"] = recipients
            break

    if "pour" not in result:
        result["pour"] = []

    # nature
    for k in NATURE_KEYS:
        if k in fm:
            result["nature"] = strip_accents(fm[k].lower().strip())
            break

    # date
    if "date" in fm:
        result["date"] = fm["date"].strip()

    return result


# ---------------------------------------------------------------------------
# Friction markers parser
# ---------------------------------------------------------------------------

def count_friction_markers(filepath: Path) -> dict[str, int]:
    """Count friction markers in the body of a file (after frontmatter)."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {v: 0 for v in FRICTION_MARKERS.values()}

    # Skip frontmatter
    body = text
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            body = text[end + 3:]

    counts = {v: 0 for v in FRICTION_MARKERS.values()}
    for char, key in FRICTION_MARKERS.items():
        if char == "~":
            # ~ at start of line or after list marker (- ~ or * ~)
            counts[key] = len(re.findall(r"(?:^|(?<=[-*]\s))~", body, re.MULTILINE))
        else:
            counts[key] = body.count(char)

    return counts


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_artifacts(instance_path: Path) -> tuple[list[dict], list[str]]:
    """Scan notes and reviews, return (artifacts, warnings)."""
    artifacts = []
    warnings = []

    dirs = {
        "shared/notes": "note",
        "shared/review": "review",
    }

    for rel_dir, default_nature in dirs.items():
        base = instance_path / rel_dir
        if not base.is_dir():
            warnings.append(f"directory not found: {rel_dir}/")
            continue

        for filepath in sorted(base.rglob("*.md")):

            fm = parse_frontmatter(filepath)
            if fm is None:
                warnings.append(f"no frontmatter: {filepath.relative_to(instance_path)}")
                continue

            normalized = normalize_frontmatter(fm)
            if "de" not in normalized:
                warnings.append(f"no emitter field: {filepath.relative_to(instance_path)}")
                continue

            nature = normalized.get("nature", default_nature)
            markers = count_friction_markers(filepath)

            artifacts.append({
                "file": str(filepath.relative_to(instance_path)),
                "de": normalized["de"],
                "pour": normalized["pour"],
                "nature": nature,
                "date": normalized.get("date", ""),
                "markers": markers,
                "source_dir": default_nature,
            })

    return artifacts, warnings


# ---------------------------------------------------------------------------
# Matrix builders
# ---------------------------------------------------------------------------

def build_exchange_matrix(artifacts: list[dict]) -> dict[str, dict[str, int]]:
    """Build exchange matrix: emitter → recipient → count."""
    matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for a in artifacts:
        for dest in a["pour"]:
            matrix[a["de"]][dest] += 1
    return {k: dict(v) for k, v in matrix.items()}


def build_friction_matrix(artifacts: list[dict]) -> dict[str, dict[str, int]]:
    """Build friction matrix: only reviews and signals."""
    matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for a in artifacts:
        if a["nature"] in ("review", "signal"):
            for dest in a["pour"]:
                matrix[a["de"]][dest] += 1
    return {k: dict(v) for k, v in matrix.items()}


def build_marker_totals(artifacts: list[dict]) -> dict[str, dict[str, int]]:
    """Aggregate friction markers per emitter (reviews + signals only)."""
    totals: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for a in artifacts:
        if a["nature"] in ("review", "signal"):
            for key, count in a["markers"].items():
                totals[a["de"]][key] += count
    return {k: dict(v) for k, v in totals.items()}


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def format_matrix_table(matrix: dict[str, dict[str, int]], all_personas: list[str]) -> str:
    """Format a matrix as an aligned text table."""
    col_width = max(len(p) for p in all_personas) + 2
    header = " " * col_width + "".join(p.rjust(col_width) for p in all_personas)
    lines = [header]

    for emitter in all_personas:
        row = emitter.ljust(col_width)
        for receiver in all_personas:
            if emitter == receiver:
                cell = "-"
            else:
                cell = str(matrix.get(emitter, {}).get(receiver, 0))
            row += cell.rjust(col_width)
        lines.append(row)

    return "\n".join(lines)


def format_markers_table(markers: dict[str, dict[str, int]], all_personas: list[str]) -> str:
    """Format markers as an aligned text table."""
    marker_keys = list(FRICTION_MARKERS.values())
    col_width = max(len(k) for k in marker_keys) + 2
    name_width = max(len(p) for p in all_personas) + 2

    header = " " * name_width + "".join(k.rjust(col_width) for k in marker_keys)
    lines = [header]

    for persona in all_personas:
        row = persona.ljust(name_width)
        pm = markers.get(persona, {})
        for key in marker_keys:
            row += str(pm.get(key, 0)).rjust(col_width)
        lines.append(row)

    return "\n".join(lines)


def generate_signals(
    exchange_matrix: dict,
    friction_matrix: dict,
    marker_totals: dict,
    all_personas: list[str],
) -> list[str]:
    """Generate diagnostic signals."""
    signals = []

    # Friction holes: 0 reviews emitted
    no_friction_out = [
        p for p in all_personas
        if p not in friction_matrix or sum(friction_matrix[p].values()) == 0
    ]
    if no_friction_out:
        signals.append(f"Trous friction (0 reviews emises) : {', '.join(no_friction_out)}")

    # Pure receivers: 0 reviews emitted, N received
    friction_received = defaultdict(int)
    for emitter, targets in friction_matrix.items():
        for target, count in targets.items():
            friction_received[target] += count

    for p in no_friction_out:
        received = friction_received.get(p, 0)
        if received > 0:
            signals.append(f"Recepteur pur (0 reviews emises, {received} recues) : {p}")

    # No incoming friction
    no_friction_in = [
        p for p in all_personas
        if friction_received.get(p, 0) == 0 and p in exchange_matrix
    ]
    if no_friction_in:
        signals.append(f"Sans friction entrante : {', '.join(no_friction_in)}")

    # Domestication: 100% juste markers
    for p in all_personas:
        pm = marker_totals.get(p, {})
        total = sum(pm.values())
        if total > 0 and pm.get("juste", 0) == total:
            signals.append(f"Domestication (100% juste) : {p}")

    return signals


def print_report(
    instance_name: str,
    artifacts: list[dict],
    warnings: list[str],
    exchange_matrix: dict,
    friction_matrix: dict,
    marker_totals: dict,
    all_personas: list[str],
):
    """Print the full text report to stdout."""
    today = date.today().isoformat()
    notes_count = sum(1 for a in artifacts if a["source_dir"] == "note")
    reviews_count = sum(1 for a in artifacts if a["source_dir"] == "review")

    print(f"audit-instance — {instance_name} ({today})")
    print("=" * 50)
    print()
    print(f"Fichiers scannes : {len(artifacts)} ({notes_count} notes, {reviews_count} reviews)")
    print(f"Fichiers ignores : {len(warnings)} (sans frontmatter ou invalides)")
    print()

    print("--- Matrice d'echanges ---")
    print(format_matrix_table(exchange_matrix, all_personas))
    print()

    print("--- Matrice de friction ---")
    print(format_matrix_table(friction_matrix, all_personas))
    print()

    print("--- Marqueurs de friction ---")
    print(format_markers_table(marker_totals, all_personas))
    print()

    signals = generate_signals(exchange_matrix, friction_matrix, marker_totals, all_personas)
    if signals:
        print("--- Signaux ---")
        for s in signals:
            print(s)
        print()

    if warnings:
        print("--- Warnings ---")
        for w in warnings:
            print(f"  ⚠ {w}")
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python audit-instance.py <instance-path>", file=sys.stderr)
        sys.exit(1)

    instance_path = Path(sys.argv[1]).resolve()

    # Detect instance
    if not (instance_path / "sofia.md").is_file():
        print(f"✗ Instance introuvable : pas de sofia.md dans {instance_path}", file=sys.stderr)
        sys.exit(1)

    instance_name = instance_path.name

    # Scan
    artifacts, warnings = scan_artifacts(instance_path)

    if not artifacts:
        print("✗ Aucun artefact trouve avec frontmatter valide.", file=sys.stderr)
        sys.exit(1)

    # Build matrices
    exchange_matrix = build_exchange_matrix(artifacts)
    friction_matrix = build_friction_matrix(artifacts)
    marker_totals = build_marker_totals(artifacts)

    # Collect all personas (sorted)
    all_personas_set = set()
    for a in artifacts:
        all_personas_set.add(a["de"])
        all_personas_set.update(a["pour"])
    all_personas = sorted(all_personas_set)

    # Count stats
    notes_count = sum(1 for a in artifacts if a["source_dir"] == "note")
    reviews_count = sum(1 for a in artifacts if a["source_dir"] == "review")
    friction_arts = [a for a in artifacts if a["nature"] in ("review", "signal")]
    signals_count = sum(1 for a in friction_arts if a["nature"] == "signal")

    today = date.today().isoformat()

    # Write audit-echanges.json
    echanges_data = {
        "meta": {
            "instance": instance_name,
            "date": today,
            "notes_scanned": notes_count,
            "reviews_scanned": reviews_count,
            "skipped": len(warnings),
        },
        "matrix": exchange_matrix,
    }

    output_dir = Path.cwd()
    echanges_path = output_dir / "audit-echanges.json"
    echanges_path.write_text(
        json.dumps(echanges_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Write audit-friction.json
    friction_data = {
        "meta": {
            "instance": instance_name,
            "date": today,
            "reviews": reviews_count,
            "signals": signals_count,
        },
        "matrix": friction_matrix,
        "markers": marker_totals,
    }

    friction_path = output_dir / "audit-friction.json"
    friction_path.write_text(
        json.dumps(friction_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Print report
    print_report(
        instance_name,
        artifacts,
        warnings,
        exchange_matrix,
        friction_matrix,
        marker_totals,
        all_personas,
    )

    print(f"✓ {echanges_path.name} + {friction_path.name}")


if __name__ == "__main__":
    main()