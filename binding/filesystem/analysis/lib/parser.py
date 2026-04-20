"""parser.py — Unified parsing for H2A protocol artifacts.

Frontmatter, friction lines, flux sections, signalerPattern, session metadata.
Used by scan.py, probe.py, and legacy scripts.
"""
from __future__ import annotations

import re
from pathlib import Path

from .constants import (
    FRICTION_MARKERS,
    FRICTION_BRACKET_ALIASES,
    RESOLUTION_TAGS,
    RESOLUTION_ALIASES,
    EMITTER_KEYS,
    RECIPIENT_KEYS,
    NATURE_KEYS,
    STATUT_KEYS,
    OBJET_KEYS,
    STATUT_ALIASES,
    strip_accents,
)

# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def parse_frontmatter_from_text(text: str) -> dict | None:
    """Parse YAML frontmatter from text string. Returns None if absent."""
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    fm = {}
    for line in text[3:end].strip().splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip().lower()
        val = val.strip().strip('"').strip("'")
        if key and val:
            fm[key] = val
    return fm if fm else None


def parse_frontmatter(filepath: Path) -> dict | None:
    """Parse YAML frontmatter from a file. Returns None if absent or unreadable."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    return parse_frontmatter_from_text(text)


def normalize_frontmatter(fm: dict) -> dict:
    """Normalize frontmatter: resolve aliases, strip accents, split recipients."""
    result = {}

    # Emitter
    for k in EMITTER_KEYS:
        if k in fm:
            result["de"] = strip_accents(fm[k].lower().strip())
            break

    # Recipient(s)
    for k in RECIPIENT_KEYS:
        if k in fm:
            raw = fm[k]
            parts = [strip_accents(p.strip().lower()) for p in re.split(r"[,;+]", raw)]
            result["pour"] = parts if len(parts) > 1 else parts
            break

    # Nature
    for k in NATURE_KEYS:
        if k in fm:
            result["nature"] = strip_accents(fm[k].lower().strip())
            break

    # Statut (with value aliases)
    for k in STATUT_KEYS:
        if k in fm:
            raw = strip_accents(fm[k].lower().strip())
            result["statut"] = STATUT_ALIASES.get(raw, raw)
            break

    # Date
    if "date" in fm:
        result["date"] = fm["date"].strip()

    # Objet
    for k in OBJET_KEYS:
        if k in fm:
            result["objet"] = fm[k].strip()
            break

    return result


# ---------------------------------------------------------------------------
# Friction lines
# ---------------------------------------------------------------------------

def parse_friction_lines(text: str) -> list[dict]:
    """Parse friction lines anywhere in text.

    Scans all list items for friction markers (icon or [bracket])
    combined with an initiative tag ([PO] or [name]).
    Same parser for sessions, reviews, notes.
    """
    records = []

    for line in text.splitlines():
        stripped = line.strip()
        item = stripped[2:].strip() if stripped.startswith("- ") else stripped
        record = {"marker": None, "initiative": None, "resolution": None, "ref": None, "description": None}

        # Marker — icons
        for char, key in FRICTION_MARKERS.items():
            if char == "~":
                if item.startswith("~"):
                    record["marker"] = key
                    break
            elif char in item:
                record["marker"] = key
                break

        # Marker — brackets (FR and EN via aliases)
        if not record["marker"]:
            bracket_pattern = r"\[(" + "|".join(re.escape(k) for k in FRICTION_BRACKET_ALIASES) + r")\]"
            bracket_match = re.search(bracket_pattern, item)
            if bracket_match:
                record["marker"] = FRICTION_BRACKET_ALIASES[bracket_match.group(1)]

        if not record["marker"]:
            continue

        # Initiative — require [PO] or — [name]
        if "[PO]" in item or "[po]" in item:
            record["initiative"] = "PO"
        elif re.search(r"—\s*\[(\w+)\]", item):
            record["initiative"] = "persona"
        else:
            continue

        # Resolution (FR and EN via aliases)
        res_match = re.search(r"→\s*(\w+)", item)
        if res_match:
            tag = strip_accents(res_match.group(1).lower())
            if tag in RESOLUTION_ALIASES:
                record["resolution"] = RESOLUTION_ALIASES[tag]
            elif tag in RESOLUTION_TAGS:
                record["resolution"] = tag

        # Ref
        ref_match = re.search(r"\(ref:\s*([^)]+)\)", item)
        if ref_match:
            record["ref"] = ref_match.group(1).strip()

        # Description
        desc = re.sub(r"[✓~⚡◐✗]\s*", "", item)
        desc = re.sub(r"\[(juste|contestable|simplification|angle-mort|faux|sound|blind.spot|refuted)\]\s*", "", desc)
        desc = re.sub(r"\s*—\s*\[\w+\]\s*(→\s*\w+)?(\s*\(ref:[^)]+\))?", "", desc)
        record["description"] = desc.strip()[:120]

        records.append(record)

    return records


def count_friction_markers_from_text(text: str) -> dict[str, int]:
    """Count friction markers in text. Returns {marker_key: count}."""
    counts = {v: 0 for v in FRICTION_MARKERS.values()}
    body = _extract_body(text)

    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ") and not stripped.startswith("* "):
            continue
        item = stripped[2:].strip()

        for char, key in FRICTION_MARKERS.items():
            if char == "~":
                if item.startswith("~"):
                    counts[key] += 1
                    break
            elif char in item:
                counts[key] += 1
                break

    # Also count tilde as list markers
    counts["contestable"] += _count_tilde(body) - counts.get("contestable", 0) if False else 0

    return counts


def _extract_body(text: str) -> str:
    """Extract body (after frontmatter) from text."""
    if not text.startswith("---"):
        return text
    end = text.find("---", 3)
    return text[end + 3:] if end != -1 else text


def _count_tilde(text: str) -> int:
    """Count tilde markers in list items."""
    return sum(1 for line in text.splitlines()
               if line.strip().startswith("- ~") or line.strip().startswith("* ~"))


# ---------------------------------------------------------------------------
# Flux (contribution) lines
# ---------------------------------------------------------------------------

def parse_flux_lines(text: str) -> list[dict]:
    """Parse ## Flow / ## Flux lines into structured records."""
    lines = text.splitlines()
    in_section = False
    records = []

    for line in lines:
        if line.strip().startswith("## Flux") or line.strip().startswith("## Flow"):
            in_section = True
            continue
        if in_section and line.strip().startswith("## "):
            break
        if not in_section:
            continue

        stripped = line.strip()
        if not stripped.startswith("- "):
            continue

        item = stripped[2:].strip()
        flux_match = re.match(r"([HA]):(\w+)", item)
        if flux_match:
            flux_type = flux_match.group(2)
            flux_aliases = {"matiere": "substance", "challenge": "contestation"}
            flux_type = flux_aliases.get(flux_type, flux_type)
            records.append({"direction": flux_match.group(1), "type": flux_type})

    return records


# ---------------------------------------------------------------------------
# signalerPattern / reportPattern
# ---------------------------------------------------------------------------

def parse_signaler_pattern(text: str) -> dict | None:
    """Parse ## signalerPattern / ## reportPattern section."""
    lines = text.splitlines()
    in_section = False
    result = {"theme": None, "choix": None, "justification": None}

    for line in lines:
        if line.strip().startswith("## signalerPattern") or line.strip().startswith("## reportPattern"):
            in_section = True
            continue
        if in_section and line.strip().startswith("## "):
            break
        if not in_section:
            continue

        stripped = line.strip()
        if stripped.startswith("- Theme") or stripped.startswith("- Topic"):
            m = re.search(r"(?:Theme|Topic)\s*:\s*(.+)", stripped)
            if m:
                result["theme"] = m.group(1).strip()
        elif stripped.startswith("- Choix") or stripped.startswith("- Choice"):
            m = re.search(r"(?:Choix|Choice)\s*:\s*(.+)", stripped)
            if m:
                result["choix"] = strip_accents(m.group(1).strip().lower())
        elif stripped.startswith("- Justification"):
            m = re.search(r"Justification\s*:\s*(.+)", stripped)
            if m:
                result["justification"] = m.group(1).strip()

    return result if in_section else None


# ---------------------------------------------------------------------------
# Session metadata
# ---------------------------------------------------------------------------

def parse_session_date(filepath: Path) -> str | None:
    """Extract date from session filename or frontmatter."""
    fm = parse_frontmatter(filepath)
    if fm and "date" in fm:
        return fm["date"].strip()
    m = re.match(r"(\d{4}-\d{2}-\d{2})", filepath.name)
    return m.group(1) if m else None


def parse_artifact_date(filepath: Path) -> str | None:
    """Extract date from artifact frontmatter or filename."""
    fm = parse_frontmatter(filepath)
    if fm and "date" in fm:
        return fm["date"].strip()
    m = re.search(r"(\d{4}-\d{2}-\d{2})", filepath.name)
    return m.group(1) if m else None


def parse_artifact_persona(filepath: Path) -> str | None:
    """Extract emitting persona from artifact frontmatter or filename."""
    fm = parse_frontmatter(filepath)
    if fm and "de" in fm:
        return fm["de"].strip()
    parts = filepath.stem.rsplit("-", 1)
    return parts[-1] if len(parts) == 2 else None


# ---------------------------------------------------------------------------
# Direction computation
# ---------------------------------------------------------------------------

def compute_direction(initiative: str, marker: str) -> str:
    """Compute friction direction from initiative + marker."""
    is_corroboration = marker == "sound"
    if initiative == "persona":
        return "a_corroborates_h" if is_corroboration else "a_contests_h"
    else:
        return "h_corroborates_a" if is_corroboration else "h_contests_a"


# ---------------------------------------------------------------------------
# Artifact discovery
# ---------------------------------------------------------------------------

def find_artifacts(instance_path: Path) -> list[Path]:
    """Find all .md files in shared/ that could contain friction markers."""
    shared = instance_path / "shared"
    if not shared.is_dir():
        return []

    artifacts = []
    skip_dirs = {"orga", "audits", "archives"}
    skip_prefixes = ("conventions", "roadmap", "naming", "inventaire")

    for md in sorted(shared.rglob("*.md")):
        rel_parts = md.relative_to(shared).parts
        if any(p in skip_dirs for p in rel_parts):
            continue
        if md.name.startswith(skip_prefixes):
            continue
        artifacts.append(md)

    return artifacts


# ---------------------------------------------------------------------------
# Lineage resolution
# ---------------------------------------------------------------------------

def resolve_lineage(records: list[dict]) -> list[dict]:
    """Resolve friction lineage via ref: fields.

    A chain of frictions linked by ref = one logical friction.
    The last resolution in the chain propagates to the source.
    """
    by_source = {}
    for i, r in enumerate(records):
        source = r.get("source", "")
        source_key = source.rsplit(".", 1)[0] if "." in source else source
        if source_key not in by_source:
            by_source[source_key] = []
        by_source[source_key].append((i, r))

    for i, r in enumerate(records):
        ref = r.get("ref")
        if not ref:
            continue

        parts = ref.strip().split("/")
        if len(parts) < 2:
            continue

        ref_index_str = parts[-1]
        ref_source = "/".join(parts[:-1])

        try:
            ref_index = int(ref_index_str) - 1
        except ValueError:
            continue

        matched = None
        for key in by_source:
            if key.endswith(ref_source) or ref_source.endswith(key.split("/")[-1]):
                source_records = by_source[key]
                if 0 <= ref_index < len(source_records):
                    matched = source_records[ref_index]
                    break

        if matched:
            src_idx, src_record = matched
            if r.get("resolution") and not src_record.get("resolution"):
                src_record["resolution"] = r["resolution"]
            r["is_amendment"] = True

    for r in records:
        if "is_amendment" not in r:
            r["is_amendment"] = False

    return records


# ---------------------------------------------------------------------------
# Date utilities
# ---------------------------------------------------------------------------

def date_to_week(d: str) -> str:
    """Convert YYYY-MM-DD to week label (YYYY-WNN)."""
    from datetime import date as dt_date
    try:
        dt = dt_date.fromisoformat(d)
        iso = dt.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"
    except (ValueError, AttributeError):
        return "unknown"


# ---------------------------------------------------------------------------
# Artifact type discovery from conventions.md
# ---------------------------------------------------------------------------

# Default artifact types (used if conventions.md has no ## Artifact types table)
DEFAULT_ARTIFACT_TYPES = {
    "notes": {"dir": "shared/notes", "naming": r"^note-.+-.+\.md$", "extra_fields": set()},
    "reviews": {"dir": "shared/review", "naming": r"^review-.+-.+\.md$", "extra_fields": {"objet"}},
}


def parse_artifact_types_from_conventions(instance: Path) -> dict[str, dict] | None:
    """Parse the ## Artifact types table from shared/conventions.md.

    Returns a dict mapping type name -> {dir, naming, extra_fields}, or None
    if the section is absent (caller should fall back to DEFAULT_ARTIFACT_TYPES).
    """
    conv = instance / "shared" / "conventions.md"
    if not conv.is_file():
        return None
    try:
        text = conv.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    # Find ## Artifact types section
    lines = text.splitlines()
    in_section = False
    table_lines = []
    for line in lines:
        if re.match(r"^#{1,3}\s+[Aa]rtifact [Tt]ypes?\s*$", line):
            in_section = True
            continue
        if in_section and line.startswith("#"):
            break
        if in_section and "|" in line:
            table_lines.append(line)

    if len(table_lines) < 3:  # header + separator + at least 1 row
        return None

    # Parse table rows (skip header and separator)
    result = {}
    for row in table_lines[2:]:
        cells = [c.strip() for c in row.split("|")]
        cells = [c for c in cells if c]  # remove empty from leading/trailing |
        if len(cells) < 2:
            continue
        # Skip HTML comment rows
        if cells[0].startswith("<!--"):
            continue
        type_name = cells[0].strip().lower()
        directory = cells[1].strip().rstrip("/") if len(cells) > 1 else f"shared/{type_name}"
        naming = cells[2].strip() if len(cells) > 2 else ""
        extra = cells[3].strip() if len(cells) > 3 else ""

        # Convert naming pattern like note-{subject}-{author}.md -> regex
        naming_re = ""
        if naming and naming.startswith("`"):
            naming = naming.strip("`")
        if naming:
            # Replace {xxx} placeholders with .+ regex
            naming_re = "^" + re.sub(r"\{[^}]+\}", ".+", re.escape(naming).replace(r"\.\+", ".+")) + "$"
            # Fix: re.escape escapes the dots, we need .md at end
            naming_re = naming_re.replace(r"\.md", r"\.md")

        extra_fields = set()
        if extra:
            extra_fields = {f.strip() for f in extra.split(",") if f.strip()}

        result[type_name] = {
            "dir": directory.rstrip("/"),
            "naming": naming_re,
            "extra_fields": extra_fields,
        }

    return result if result else None


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

def resolve_artifact_dir(instance: Path, rel_dir: str) -> Path:
    """Resolve an artifact directory path relative to the instance root.
    Handles ../ for external repos (e.g., ../sofia/doc/adr/)."""
    return (instance / rel_dir).resolve()


def safe_relative(f: Path, instance: Path) -> str:
    """Return a path relative to instance, or the original rel_dir prefix if external."""
    try:
        return str(f.relative_to(instance.resolve()))
    except ValueError:
        # External file -- show from the parent of instance
        try:
            return str(f.relative_to(instance.resolve().parent))
        except ValueError:
            return str(f)


# ---------------------------------------------------------------------------
# Persona discovery
# ---------------------------------------------------------------------------

def discover_personas(instance_path: Path) -> set[str]:
    """Discover real personas from shared/orga/personas/persona-*.md."""
    personas_dir = instance_path / "shared" / "orga" / "personas"
    if not personas_dir.is_dir():
        return set()
    result = set()
    for f in personas_dir.glob("persona-*.md"):
        name = f.stem.removeprefix("persona-")
        if name:
            result.add(strip_accents(name.lower()))
    return result


def discover_persona_roles(instance_path: Path) -> dict[str, str]:
    """Discover persona → role mapping from shared/orga/personas/persona-*.md frontmatter."""
    personas_dir = instance_path / "shared" / "orga" / "personas"
    if not personas_dir.is_dir():
        return {}
    roles = {}
    for f in personas_dir.glob("persona-*.md"):
        name = f.stem.removeprefix("persona-")
        if not name:
            continue
        key = strip_accents(name.lower())
        fm = parse_frontmatter(f)
        if fm:
            roles[key] = fm.get("role", "")
    return roles


# ---------------------------------------------------------------------------
# Context size audit
# ---------------------------------------------------------------------------

def measure_context_sizes(instance_path: Path) -> dict[str, dict]:
    """Measure persona.md + contexte.md sizes for each persona."""
    personas_dir = instance_path / "shared" / "orga" / "personas"
    contextes_dir = instance_path / "shared" / "orga" / "contextes"
    results = {}

    if not personas_dir.is_dir():
        return results

    for f in personas_dir.glob("persona-*.md"):
        name = f.stem.removeprefix("persona-")
        if not name:
            continue

        persona_lines = 0
        try:
            persona_lines = len(f.read_text(encoding="utf-8").splitlines())
        except (OSError, UnicodeDecodeError):
            pass

        # Find matching contexte(s)
        contexte_lines = 0
        contexte_files = []
        if contextes_dir.is_dir():
            for cf in contextes_dir.glob(f"contexte-{name}*.md"):
                try:
                    lines = len(cf.read_text(encoding="utf-8").splitlines())
                    contexte_lines += lines
                    contexte_files.append({"file": cf.name, "lines": lines})
                except (OSError, UnicodeDecodeError):
                    pass

        total = persona_lines + contexte_lines
        status = "ok" if total < 150 else "warn" if total < 250 else "danger"

        results[strip_accents(name.lower())] = {
            "persona_lines": persona_lines,
            "contexte_lines": contexte_lines,
            "total_lines": total,
            "status": status,
            "contexte_files": contexte_files,
        }

    return results
