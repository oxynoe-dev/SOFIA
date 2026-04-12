#!/usr/bin/env python3
"""audit-instance.py — Audit a SOFIA instance: structure + exchanges + friction.

Usage:
    python audit-instance.py <instance-path>

Outputs (in <instance>/shared/audits/):
    audit-structure.json    — structural conformity checks
    audit-echanges.json     — exchange matrix (who talks to whom)
    audit-friction.json     — friction matrix + markers
    audit-friction-po.json  — orchestrator friction from sessions
    audit-report.md         — full human-readable report

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

EMITTER_KEYS = {"de", "auteur", "emetteur", "from"}
RECIPIENT_KEYS = {"pour", "destinataire", "destinataires", "to"}
NATURE_KEYS = {"nature", "type"}

VALID_STATUTS = {"nouveau", "lu", "traite"}

_ACCENT_MAP = str.maketrans(
    "àâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ",
    "aaaeeeeiioouuycAAAEEEEIIOOUUYC",
)


def strip_accents(s: str) -> str:
    return s.translate(_ACCENT_MAP)


# ---------------------------------------------------------------------------
# Frontmatter parser
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
        line = line.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip().lower()] = value.strip()
    return fm if fm else None


def parse_frontmatter(filepath: Path) -> dict | None:
    """Parse YAML frontmatter from file. Returns None if absent."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    return parse_frontmatter_from_text(text)


def normalize_frontmatter(fm: dict) -> dict:
    """Normalize frontmatter fields to canonical names."""
    result = {}

    for k in EMITTER_KEYS:
        if k in fm:
            result["de"] = strip_accents(fm[k].lower().strip())
            break

    for k in RECIPIENT_KEYS:
        if k in fm:
            raw = fm[k].lower().strip()
            result["pour"] = [strip_accents(r.strip()) for r in re.split(r"[,\s]+", raw) if r.strip()]
            break

    if "pour" not in result:
        result["pour"] = []

    for k in NATURE_KEYS:
        if k in fm:
            result["nature"] = strip_accents(fm[k].lower().strip())
            break

    if "date" in fm:
        result["date"] = fm["date"].strip()

    if "statut" in fm:
        result["statut"] = strip_accents(fm["statut"].lower().strip())

    if "objet" in fm:
        result["objet"] = fm["objet"].strip()

    if "persona" in fm:
        result["persona"] = strip_accents(fm["persona"].lower().strip())

    return result


# ---------------------------------------------------------------------------
# Friction markers parser
# ---------------------------------------------------------------------------

def _extract_body(text: str) -> str:
    """Return file body after frontmatter."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:]
    return text


def _count_tilde(text: str) -> int:
    """Count ~ as friction marker: at start of line or after list marker."""
    return len(re.findall(r"(?:^[-*]\s+|^)~", text, re.MULTILINE))


def count_friction_markers_from_text(text: str) -> dict[str, int]:
    """Count friction markers in a file's text (body after frontmatter)."""
    body = _extract_body(text)
    counts = {v: 0 for v in FRICTION_MARKERS.values()}
    for char, key in FRICTION_MARKERS.items():
        if char == "~":
            counts[key] = _count_tilde(body)
        else:
            counts[key] = body.count(char)
    return counts


# ---------------------------------------------------------------------------
# Phase 1 — Structural conformity
# ---------------------------------------------------------------------------

def check_structure(instance: Path) -> list[dict]:
    """Run structural conformity checks."""
    checks = []

    def add(cid: str, severity: str, passed: bool, detail: str, files: list[str] | None = None):
        status = "pass" if passed else severity
        entry = {"id": cid, "status": status, "detail": detail}
        if files:
            entry["files"] = files
        checks.append(entry)

    # S1: sofia.md or voix.md (instance marker)
    marker_found = (instance / "sofia.md").is_file() or (instance / "voix.md").is_file()
    marker_name = "sofia.md" if (instance / "sofia.md").is_file() else "voix.md" if (instance / "voix.md").is_file() else "sofia.md/voix.md"
    add("S1", "fail", marker_found, f"{marker_name} present" if marker_found else "sofia.md ou voix.md manquant")

    # S2: shared/
    add("S2", "fail", (instance / "shared").is_dir(), "shared/ present" if (instance / "shared").is_dir() else "shared/ manquant")

    # S3: shared/conventions.md
    add("S3", "warn", (instance / "shared" / "conventions.md").is_file(),
        "shared/conventions.md present" if (instance / "shared" / "conventions.md").is_file() else "shared/conventions.md manquant")

    # S4: shared/notes/ with archives/
    notes_dir = instance / "shared" / "notes"
    notes_ok = notes_dir.is_dir()
    notes_archives = (notes_dir / "archives").is_dir() if notes_ok else False
    if notes_ok and notes_archives:
        add("S4", "warn", True, "shared/notes/ present avec archives/")
    elif notes_ok:
        add("S4", "warn", False, "shared/notes/ present mais archives/ manquant")
    else:
        add("S4", "warn", False, "shared/notes/ manquant")

    # S5: shared/review/ with archives/
    review_dir = instance / "shared" / "review"
    review_ok = review_dir.is_dir()
    review_archives = (review_dir / "archives").is_dir() if review_ok else False
    if review_ok and review_archives:
        add("S5", "warn", True, "shared/review/ present avec archives/")
    elif review_ok:
        add("S5", "warn", False, "shared/review/ present mais archives/ manquant")
    else:
        add("S5", "warn", False, "shared/review/ manquant")

    # S6: shared/features/
    add("S6", "info", (instance / "shared" / "features").is_dir(),
        "shared/features/ present" if (instance / "shared" / "features").is_dir() else "shared/features/ manquant")

    # S7: shared/orga/
    add("S7", "info", (instance / "shared" / "orga").is_dir(),
        "shared/orga/ present" if (instance / "shared" / "orga").is_dir() else "shared/orga/ manquant")

    # S8: at least 1 workspace with CLAUDE.md
    workspaces = [d for d in instance.iterdir() if d.is_dir() and (d / "CLAUDE.md").is_file() and d.name != "shared"]
    add("S8", "fail", len(workspaces) > 0,
        f"{len(workspaces)} workspaces avec CLAUDE.md" if workspaces else "aucun workspace avec CLAUDE.md")

    # S9: each workspace has sessions/
    ws_without_sessions = [d.name for d in workspaces if not (d / "sessions").is_dir()]
    if ws_without_sessions:
        add("S9", "warn", False, f"{len(ws_without_sessions)} workspaces sans sessions/", ws_without_sessions)
    else:
        add("S9", "warn", True, "tous les workspaces ont sessions/")

    # S10: at least 1 roadmap
    roadmaps = list((instance / "shared").glob("roadmap-*.md")) if (instance / "shared").is_dir() else []
    add("S10", "warn", len(roadmaps) > 0,
        f"{len(roadmaps)} roadmaps dans shared/" if roadmaps else "aucune roadmap dans shared/")

    # F1-F2: frontmatter presence
    for label, rel_dir, fid in [("notes", "shared/notes", "F1"), ("reviews", "shared/review", "F2")]:
        base = instance / rel_dir
        if not base.is_dir():
            continue
        all_md = list(base.rglob("*.md"))
        no_fm = [str(f.relative_to(instance)) for f in all_md if parse_frontmatter(f) is None]
        if no_fm:
            add(fid, "warn", False, f"{len(no_fm)}/{len(all_md)} {label} sans frontmatter", no_fm)
        else:
            add(fid, "warn", True, f"{len(all_md)} {label} avec frontmatter")

    # F3-F4: required fields
    required_notes = {"de", "pour", "nature", "statut", "date"}
    required_reviews = {"de", "pour", "nature", "statut", "date", "objet"}
    for label, rel_dir, fid, required in [
        ("notes", "shared/notes", "F3", required_notes),
        ("reviews", "shared/review", "F4", required_reviews),
    ]:
        base = instance / rel_dir
        if not base.is_dir():
            continue
        missing_fields_files = []
        for f in base.rglob("*.md"):
            fm = parse_frontmatter(f)
            if fm is None:
                continue
            fm_keys = set(fm.keys())
            # check with aliases
            has_emitter = bool(fm_keys & EMITTER_KEYS)
            has_recipient = bool(fm_keys & RECIPIENT_KEYS)
            has_nature = bool(fm_keys & NATURE_KEYS)
            has_statut = "statut" in fm_keys
            has_date = "date" in fm_keys
            has_objet = "objet" in fm_keys
            missing = []
            if not has_emitter:
                missing.append("de")
            if not has_recipient:
                missing.append("pour")
            if not has_nature:
                missing.append("nature")
            if not has_statut:
                missing.append("statut")
            if not has_date:
                missing.append("date")
            if "objet" in required and not has_objet:
                missing.append("objet")
            if missing:
                missing_fields_files.append(f"{f.relative_to(instance)} (manque: {', '.join(missing)})")
        if missing_fields_files:
            add(fid, "warn", False, f"{len(missing_fields_files)} {label} avec champs manquants", missing_fields_files)
        else:
            add(fid, "warn", True, f"tous les {label} ont les champs requis")

    # F5: accents in frontmatter values
    accent_files = []
    for rel_dir in ["shared/notes", "shared/review"]:
        base = instance / rel_dir
        if not base.is_dir():
            continue
        for f in base.rglob("*.md"):
            fm = parse_frontmatter(f)
            if fm is None:
                continue
            for v in fm.values():
                if v != strip_accents(v):
                    accent_files.append(str(f.relative_to(instance)))
                    break
    if accent_files:
        add("F5", "info", False, f"{len(accent_files)} fichiers avec accents dans le frontmatter", accent_files)
    else:
        add("F5", "info", True, "pas d'accents dans les valeurs frontmatter")

    # F6: valid statut values
    bad_statut_files = []
    for rel_dir in ["shared/notes", "shared/review"]:
        base = instance / rel_dir
        if not base.is_dir():
            continue
        for f in base.rglob("*.md"):
            fm = parse_frontmatter(f)
            if fm is None or "statut" not in fm:
                continue
            val = strip_accents(fm["statut"].lower().strip())
            if val not in VALID_STATUTS:
                bad_statut_files.append(f"{f.relative_to(instance)} (statut: {fm['statut']})")
    if bad_statut_files:
        add("F6", "warn", False, f"{len(bad_statut_files)} fichiers avec statut invalide", bad_statut_files)
    else:
        add("F6", "warn", True, "tous les statuts sont valides")

    # F7: sessions frontmatter
    session_files = list(instance.rglob("sessions/*.md"))
    session_files = [f for f in session_files if "shared" not in f.relative_to(instance).parts]
    bad_sessions = []
    for f in session_files:
        fm = parse_frontmatter(f)
        if fm is None:
            bad_sessions.append(f"{f.relative_to(instance)} (pas de frontmatter)")
            continue
        missing = []
        if fm.get("nature") != "session":
            missing.append("nature: session")
        if "persona" not in fm:
            missing.append("persona")
        if "date" not in fm:
            missing.append("date")
        if missing:
            bad_sessions.append(f"{f.relative_to(instance)} (manque: {', '.join(missing)})")
    if bad_sessions:
        add("F7", "info", False, f"{len(bad_sessions)}/{len(session_files)} sessions sans frontmatter conforme", bad_sessions)
    else:
        add("F7", "info", True, f"{len(session_files)} sessions avec frontmatter conforme")

    # N1-N3: naming conventions
    note_pattern = re.compile(r"^note-.+-.+\.md$")
    review_pattern = re.compile(r"^review-.+-.+\.md$")
    roadmap_pattern = re.compile(r"^roadmap-.+\.md$")

    for label, rel_dir, nid, pattern in [
        ("notes", "shared/notes", "N1", note_pattern),
        ("reviews", "shared/review", "N2", review_pattern),
    ]:
        base = instance / rel_dir
        if not base.is_dir():
            continue
        bad_names = []
        for f in base.rglob("*.md"):
            if "archives" in f.relative_to(base).parts or "archive" in f.relative_to(base).parts:
                continue
            if not pattern.match(f.name):
                bad_names.append(str(f.relative_to(instance)))
        if bad_names:
            add(nid, "info", False, f"{len(bad_names)} {label} hors convention de nommage", bad_names)
        else:
            add(nid, "info", True, f"toutes les {label} suivent la convention")

    if roadmaps:
        bad_rm = [str(f.relative_to(instance)) for f in roadmaps if not roadmap_pattern.match(f.name)]
        if bad_rm:
            add("N3", "info", False, f"{len(bad_rm)} roadmaps hors convention", bad_rm)
        else:
            add("N3", "info", True, "toutes les roadmaps suivent roadmap-{{produit}}.md")

    # A1: traite files not in archives/
    misplaced_traite = []
    for rel_dir in ["shared/notes", "shared/review"]:
        base = instance / rel_dir
        if not base.is_dir():
            continue
        for f in base.rglob("*.md"):
            in_archives = "archives" in f.relative_to(base).parts or "archive" in f.relative_to(base).parts
            if in_archives:
                continue
            fm = parse_frontmatter(f)
            if fm is None:
                continue
            statut = strip_accents(fm.get("statut", "").lower().strip())
            if statut == "traite":
                misplaced_traite.append(str(f.relative_to(instance)))
    if misplaced_traite:
        add("A1", "warn", False, f"{len(misplaced_traite)} fichiers traite hors archives/", misplaced_traite)
    else:
        add("A1", "warn", True, "tous les fichiers traite sont dans archives/")

    # A2: files in archives/ with non-traite status
    bad_archive = []
    for rel_dir in ["shared/notes", "shared/review"]:
        base = instance / rel_dir
        if not base.is_dir():
            continue
        for f in base.rglob("*.md"):
            in_archives = "archives" in f.relative_to(base).parts or "archive" in f.relative_to(base).parts
            if not in_archives:
                continue
            fm = parse_frontmatter(f)
            if fm is None:
                continue
            statut = strip_accents(fm.get("statut", "").lower().strip())
            if statut and statut != "traite":
                bad_archive.append(f"{f.relative_to(instance)} (statut: {fm.get('statut', '')})")
    if bad_archive:
        add("A2", "info", False, f"{len(bad_archive)} fichiers dans archives/ sans statut traite", bad_archive)
    else:
        add("A2", "info", True, "tous les fichiers dans archives/ ont statut traite")

    # R1-R8: roadmap checks
    if roadmaps:
        no_header = []
        no_owner_header = []
        no_version_meta = []
        items_without_owner = []
        items_without_status = []
        no_convergence = []
        no_cible = []
        no_source = []
        total_items = 0
        total_with_convergence = 0
        total_with_cible = 0
        total_with_source = 0

        for rm in roadmaps:
            rel = str(rm.relative_to(instance))
            try:
                text = rm.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            lines_text = text.splitlines()

            # R1: header format — # Roadmap {Nom}
            has_header = bool(lines_text) and lines_text[0].startswith("# Roadmap")
            if not has_header:
                no_header.append(rel)

            # R2: owner in blockquote — > ... Owner : @persona
            has_owner_header = bool(re.search(r"^>\s*.*[Oo]wners?\s*:\s*@\w+", text, re.MULTILINE))
            if not has_owner_header:
                no_owner_header.append(rel)

            # R3: version metadata comments — <!-- produit: X | ... statut: X -->
            version_comments = re.findall(r"<!--\s*produit:", text)
            sections = [l for l in lines_text if l.startswith("### ")]
            if sections and not version_comments:
                no_version_meta.append(rel)

            # Count cible in version comments <!-- produit: X | cible: 2026-... -->
            version_cibles = len(re.findall(r"<!--[^>]*cible:\s*\d{4}", text))
            total_with_cible += version_cibles

            # Count markers across all items
            rm_has_convergence = False
            rm_has_cible = version_cibles > 0
            rm_has_source = False

            for i, line in enumerate(lines_text):
                stripped = line.strip()
                if not stripped.startswith("- "):
                    continue
                # skip sub-items (indented with more than 0 leading spaces before -)
                if line.startswith("  "):
                    continue

                total_items += 1
                lineno = i + 1  # 1-based for display

                # R4: status marker
                has_status = bool(re.search(r"\[(done|running|todo|blocked|ready)\]", stripped))
                if not has_status:
                    items_without_status.append(f"{rel}:{lineno}")

                # R5: @owner
                has_owner = bool(re.search(r"@\w+", stripped))
                if not has_owner:
                    items_without_owner.append(f"{rel}:{lineno}")

                # convergence marker
                if "↔" in stripped:
                    total_with_convergence += 1
                    rm_has_convergence = True

                # cible on item line or next indented lines
                if "cible:" in stripped:
                    total_with_cible += 1
                    rm_has_cible = True
                else:
                    for j in range(i + 1, min(i + 4, len(lines_text))):
                        next_line = lines_text[j].strip()
                        if next_line.startswith("cible:"):
                            total_with_cible += 1
                            rm_has_cible = True
                            break
                        if next_line.startswith("- ") or next_line.startswith("## "):
                            break

                # source
                if "source:" in stripped:
                    total_with_source += 1
                    rm_has_source = True
                else:
                    for j in range(i + 1, min(i + 4, len(lines_text))):
                        next_line = lines_text[j].strip()
                        if next_line.startswith("source:"):
                            total_with_source += 1
                            rm_has_source = True
                            break
                        if next_line.startswith("- ") or next_line.startswith("## "):
                            break

            if not rm_has_convergence:
                no_convergence.append(rel)
            if not rm_has_cible:
                no_cible.append(rel)
            if not rm_has_source:
                no_source.append(rel)

        # R1: header
        if no_header:
            add("R1", "warn", False, f"{len(no_header)} roadmaps sans en-tete '# Roadmap'", no_header)
        else:
            add("R1", "warn", True, "toutes les roadmaps ont un en-tete conforme")

        # R2: owner in header
        if no_owner_header:
            add("R2", "warn", False, f"{len(no_owner_header)} roadmaps sans Owner dans le blockquote", no_owner_header)
        else:
            add("R2", "warn", True, "toutes les roadmaps declarent un Owner")

        # R3: version metadata
        if no_version_meta:
            add("R3", "info", False, f"{len(no_version_meta)} roadmaps avec sections ### sans commentaire metadata", no_version_meta)
        else:
            add("R3", "info", True, "toutes les sections version ont un commentaire metadata")

        # R4: status per item
        if items_without_status:
            add("R4", "warn", False, f"{len(items_without_status)}/{total_items} items sans statut [done/running/todo/blocked/ready]", items_without_status[:20])
        else:
            add("R4", "warn", True, f"tous les {total_items} items ont un statut")

        # R5: @owner per item
        if items_without_owner:
            add("R5", "warn", False, f"{len(items_without_owner)}/{total_items} items sans @porteur", items_without_owner[:20])
        else:
            add("R5", "warn", True, f"tous les {total_items} items ont un @porteur")

        # R6: convergence markers
        if no_convergence:
            add("R6", "info", False,
                f"{len(no_convergence)}/{len(roadmaps)} roadmaps sans marqueur ↔ ({total_with_convergence} marqueurs au total)",
                no_convergence)
        else:
            add("R6", "info", True, f"toutes les roadmaps utilisent ↔ ({total_with_convergence} marqueurs)")

        # R7: cible markers
        if no_cible:
            add("R7", "info", False,
                f"{len(no_cible)}/{len(roadmaps)} roadmaps sans marqueur cible: ({total_with_cible} marqueurs au total)",
                no_cible)
        else:
            add("R7", "info", True, f"toutes les roadmaps utilisent cible: ({total_with_cible} marqueurs)")

        # R8: source markers
        if no_source:
            add("R8", "info", False,
                f"{len(no_source)}/{len(roadmaps)} roadmaps sans marqueur source: ({total_with_source} marqueurs au total)",
                no_source)
        else:
            add("R8", "info", True, f"toutes les roadmaps utilisent source: ({total_with_source} marqueurs)")

    return checks


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


# ---------------------------------------------------------------------------
# Phase 2 — Exchange & friction scanners
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
            try:
                text = filepath.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                warnings.append(f"unreadable: {filepath.relative_to(instance_path)}")
                continue

            fm = parse_frontmatter_from_text(text)
            if fm is None:
                warnings.append(f"no frontmatter: {filepath.relative_to(instance_path)}")
                continue

            normalized = normalize_frontmatter(fm)
            if "de" not in normalized:
                warnings.append(f"no emitter field: {filepath.relative_to(instance_path)}")
                continue

            nature = normalized.get("nature", default_nature)
            markers = count_friction_markers_from_text(text)

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


def build_exchange_matrix(artifacts: list[dict]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for a in artifacts:
        for dest in a["pour"]:
            matrix[a["de"]][dest] += 1
    return {k: dict(v) for k, v in matrix.items()}


def build_friction_matrix(artifacts: list[dict]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for a in artifacts:
        if a["nature"] in ("review", "signal"):
            for dest in a["pour"]:
                matrix[a["de"]][dest] += 1
    return {k: dict(v) for k, v in matrix.items()}


def build_marker_totals(artifacts: list[dict]) -> dict[str, dict[str, int]]:
    totals: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for a in artifacts:
        if a["nature"] in ("review", "signal"):
            for key, count in a["markers"].items():
                totals[a["de"]][key] += count
    return {k: dict(v) for k, v in totals.items()}


# ---------------------------------------------------------------------------
# Phase 2b — Orchestrator friction from sessions
# ---------------------------------------------------------------------------

def scan_session_friction(instance_path: Path) -> tuple[dict[str, dict], list[str]]:
    """Parse ## Friction orchestrateur sections from session files."""
    by_persona: dict[str, dict] = defaultdict(lambda: {
        "juste": 0, "contestable": 0, "simplification": 0,
        "angle_mort": 0, "faux": 0,
        "total_sessions": 0, "sessions_with_friction": 0,
        "initiative_persona": 0, "initiative_po": 0,
    })
    warnings = []

    session_files = sorted(instance_path.rglob("sessions/*.md"))
    session_files = [f for f in session_files if "shared" not in f.relative_to(instance_path).parts]

    for filepath in session_files:
        fm = parse_frontmatter(filepath)
        if fm is None:
            continue

        normalized = normalize_frontmatter(fm)
        persona = normalized.get("persona", "")
        if not persona:
            continue

        by_persona[persona]["total_sessions"] += 1

        try:
            text = filepath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        # Find ## Friction orchestrateur section
        lines = text.splitlines()
        in_section = False
        friction_lines = []
        for line in lines:
            if line.strip().startswith("## Friction orchestrateur"):
                in_section = True
                continue
            if in_section and line.strip().startswith("## "):
                break
            if in_section:
                friction_lines.append(line)

        if not friction_lines:
            continue

        has_friction = False
        for line in friction_lines:
            stripped = line.strip()
            if not stripped.startswith("- "):
                continue

            # Count markers — content after "- "
            item_text = stripped[2:].strip()
            for char, key in FRICTION_MARKERS.items():
                if char == "~":
                    if item_text.startswith("~"):
                        by_persona[persona][key] += 1
                        has_friction = True
                elif char in item_text:
                    by_persona[persona][key] += 1
                    has_friction = True

            # Initiative tag
            if "[PO]" in stripped or "[po]" in stripped:
                by_persona[persona]["initiative_po"] += 1
            else:
                # [persona_name] or no tag = persona initiative
                by_persona[persona]["initiative_persona"] += 1

        if has_friction:
            by_persona[persona]["sessions_with_friction"] += 1

    return dict(by_persona), warnings


# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------

def generate_signals(
    exchange_matrix: dict,
    friction_matrix: dict,
    marker_totals: dict,
    po_friction: dict,
    all_personas: list[str],
    real_personas: set[str] | None = None,
) -> list[str]:
    signals = []

    # Only signal on real personas (filter out distribution lists like equipe, all, po, etc.)
    signalable = [p for p in all_personas if p in real_personas] if real_personas else all_personas

    # Friction holes
    no_friction_out = [
        p for p in signalable
        if p not in friction_matrix or sum(friction_matrix[p].values()) == 0
    ]
    if no_friction_out:
        signals.append(f"Trous friction (0 reviews emises) : {', '.join(no_friction_out)}")

    # Pure receivers
    friction_received = defaultdict(int)
    for emitter, targets in friction_matrix.items():
        for target, count in targets.items():
            friction_received[target] += count

    for p in no_friction_out:
        received = friction_received.get(p, 0)
        if received > 0:
            signals.append(f"Recepteur pur (0 emises, {received} recues) : {p}")

    # No incoming friction
    no_friction_in = [
        p for p in signalable
        if friction_received.get(p, 0) == 0 and p in exchange_matrix
    ]
    if no_friction_in:
        signals.append(f"Sans friction entrante : {', '.join(no_friction_in)}")

    # Domestication inter-personas
    for p in signalable:
        pm = marker_totals.get(p, {})
        total = sum(pm.values())
        if total > 0 and pm.get("juste", 0) == total:
            signals.append(f"Domestication inter-personas (100% juste) : {p}")

    # Domestication orchestrator
    for p, data in po_friction.items():
        if real_personas and p not in real_personas:
            continue
        total = data["juste"] + data["contestable"] + data["simplification"] + data["angle_mort"] + data["faux"]
        if total > 0 and data["juste"] == total and data["total_sessions"] >= 10:
            signals.append(f"Domestication orchestrateur (100% juste, {data['total_sessions']} sessions) : {p}")

    return signals


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_matrix_table(matrix: dict[str, dict[str, int]], personas: list[str]) -> str:
    col_width = max((len(p) for p in personas), default=8) + 2
    header = " " * col_width + "".join(p.rjust(col_width) for p in personas)
    lines = [header]
    for emitter in personas:
        row = emitter.ljust(col_width)
        for receiver in personas:
            cell = "-" if emitter == receiver else str(matrix.get(emitter, {}).get(receiver, 0))
            row += cell.rjust(col_width)
        lines.append(row)
    return "\n".join(lines)


def format_markers_table(markers: dict[str, dict[str, int]], personas: list[str]) -> str:
    marker_keys = list(FRICTION_MARKERS.values())
    col_width = max(len(k) for k in marker_keys) + 2
    name_width = max((len(p) for p in personas), default=8) + 2
    header = " " * name_width + "".join(k.rjust(col_width) for k in marker_keys)
    lines = [header]
    for persona in personas:
        row = persona.ljust(name_width)
        pm = markers.get(persona, {})
        for key in marker_keys:
            row += str(pm.get(key, 0)).rjust(col_width)
        lines.append(row)
    return "\n".join(lines)


def format_po_friction_table(po_friction: dict) -> str:
    marker_keys = list(FRICTION_MARKERS.values())
    extra_cols = ["sessions", "w/friction", "init.persona", "init.PO"]
    all_cols = marker_keys + extra_cols
    col_width = max(len(c) for c in all_cols) + 2
    personas = sorted(po_friction.keys())
    name_width = max((len(p) for p in personas), default=8) + 2

    header = " " * name_width + "".join(c.rjust(col_width) for c in all_cols)
    lines = [header]
    for p in personas:
        d = po_friction[p]
        row = p.ljust(name_width)
        for k in marker_keys:
            row += str(d.get(k, 0)).rjust(col_width)
        row += str(d["total_sessions"]).rjust(col_width)
        row += str(d["sessions_with_friction"]).rjust(col_width)
        row += str(d["initiative_persona"]).rjust(col_width)
        row += str(d["initiative_po"]).rjust(col_width)
        lines.append(row)
    return "\n".join(lines)


def generate_report_md(
    instance_name: str,
    checks: list[dict],
    artifacts: list[dict],
    scan_warnings: list[str],
    exchange_matrix: dict,
    friction_matrix: dict,
    marker_totals: dict,
    po_friction: dict,
    all_personas: list[str],
    signals: list[str],
) -> str:
    today = date.today().isoformat()
    notes_count = sum(1 for a in artifacts if a["source_dir"] == "note")
    reviews_count = sum(1 for a in artifacts if a["source_dir"] == "review")

    lines = []
    lines.append(f"# Audit instance — {instance_name} ({today})")
    lines.append("")

    # Phase 1
    lines.append("## Phase 1 — Conformite structurelle")
    lines.append("")
    summary = defaultdict(int)
    for c in checks:
        summary[c["status"]] += 1
        icon = {"pass": "✓", "warn": "⚠", "fail": "✗", "info": "ℹ"}.get(c["status"], "?")
        lines.append(f"- [{icon}] **{c['id']}** — {c['detail']}")
    lines.append("")
    lines.append(f"**Total** : {summary['pass']} pass, {summary['warn']} warn, {summary['fail']} fail, {summary['info']} info")
    lines.append("")

    # Phase 2
    lines.append("## Phase 2 — Echanges & friction")
    lines.append("")
    lines.append(f"Fichiers scannes : {len(artifacts)} ({notes_count} notes, {reviews_count} reviews)")
    lines.append(f"Fichiers ignores : {len(scan_warnings)}")
    lines.append("")

    lines.append("### Matrice d'echanges")
    lines.append("")
    lines.append("```")
    lines.append(format_matrix_table(exchange_matrix, all_personas))
    lines.append("```")
    lines.append("")

    lines.append("### Matrice de friction")
    lines.append("")
    lines.append("```")
    lines.append(format_matrix_table(friction_matrix, all_personas))
    lines.append("```")
    lines.append("")

    lines.append("### Marqueurs de friction")
    lines.append("")
    lines.append("```")
    lines.append(format_markers_table(marker_totals, all_personas))
    lines.append("```")
    lines.append("")

    # PO friction
    if po_friction:
        lines.append("### Friction orchestrateur")
        lines.append("")
        lines.append("```")
        lines.append(format_po_friction_table(po_friction))
        lines.append("```")
        lines.append("")

    # Activity
    if po_friction:
        lines.append("### Activite (sessions par persona)")
        lines.append("")
        lines.append("```")
        personas_by_sessions = sorted(po_friction.keys(), key=lambda p: po_friction[p]["total_sessions"], reverse=True)
        name_w = max((len(p) for p in personas_by_sessions), default=8) + 2
        for p in personas_by_sessions:
            lines.append(f"{p.ljust(name_w)}{po_friction[p]['total_sessions']:>6}")
        total_s = sum(d["total_sessions"] for d in po_friction.values())
        lines.append(f"{'Total'.ljust(name_w)}{total_s:>6}")
        lines.append("```")
        lines.append("")

    # Signals
    if signals:
        lines.append("### Signaux")
        lines.append("")
        for s in signals:
            lines.append(f"- {s}")
        lines.append("")

    # Warnings
    if scan_warnings:
        lines.append("### Warnings")
        lines.append("")
        for w in scan_warnings:
            lines.append(f"- ⚠ {w}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def write_json(output_dir: Path, all_data: dict):
    """Write one JSON file per data key."""
    for name, data in all_data.items():
        (output_dir / f"audit-{name}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(output_dir: Path, all_data: dict, all_personas: list[str]):
    """Write CSV files for matrices."""
    import csv

    # Exchange matrix
    with open(output_dir / "audit-echanges.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["de/pour"] + all_personas)
        matrix = all_data["echanges"]["matrix"]
        for p in all_personas:
            row = [p] + [matrix.get(p, {}).get(q, 0) for q in all_personas]
            w.writerow(row)

    # Friction matrix
    with open(output_dir / "audit-friction.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["de/pour"] + all_personas)
        matrix = all_data["friction"]["matrix"]
        for p in all_personas:
            row = [p] + [matrix.get(p, {}).get(q, 0) for q in all_personas]
            w.writerow(row)

    # Markers
    marker_keys = list(FRICTION_MARKERS.values())
    with open(output_dir / "audit-marqueurs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["persona"] + marker_keys)
        markers = all_data["friction"]["markers"]
        for p in all_personas:
            pm = markers.get(p, {})
            w.writerow([p] + [pm.get(k, 0) for k in marker_keys])

    # Activity
    with open(output_dir / "audit-activite.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["persona", "sessions"])
        for p, count in sorted(all_data["activite"]["by_persona"].items(), key=lambda x: -x[1]):
            w.writerow([p, count])

    # Structure checks
    with open(output_dir / "audit-structure.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "status", "detail"])
        for c in all_data["structure"]["checks"]:
            w.writerow([c["id"], c["status"], c["detail"]])


def write_sqlite(output_dir: Path, all_data: dict, all_personas: list[str]):
    """Write a single SQLite database with all audit data."""
    import sqlite3

    db_path = output_dir / "audit.db"
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()

    # Meta
    c.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT)")
    meta = all_data["echanges"]["meta"]
    for k, v in meta.items():
        c.execute("INSERT INTO meta VALUES (?, ?)", (k, str(v)))

    # Structure checks
    c.execute("CREATE TABLE checks (id TEXT, status TEXT, detail TEXT)")
    for check in all_data["structure"]["checks"]:
        c.execute("INSERT INTO checks VALUES (?, ?, ?)", (check["id"], check["status"], check["detail"]))

    # Exchanges
    c.execute("CREATE TABLE echanges (de TEXT, pour TEXT, count INTEGER)")
    for emitter, targets in all_data["echanges"]["matrix"].items():
        for target, count in targets.items():
            c.execute("INSERT INTO echanges VALUES (?, ?, ?)", (emitter, target, count))

    # Friction
    c.execute("CREATE TABLE friction (de TEXT, pour TEXT, count INTEGER)")
    for emitter, targets in all_data["friction"]["matrix"].items():
        for target, count in targets.items():
            c.execute("INSERT INTO friction VALUES (?, ?, ?)", (emitter, target, count))

    # Markers
    c.execute("CREATE TABLE marqueurs (persona TEXT, juste INT, contestable INT, simplification INT, angle_mort INT, faux INT)")
    for p in all_personas:
        pm = all_data["friction"]["markers"].get(p, {})
        c.execute("INSERT INTO marqueurs VALUES (?, ?, ?, ?, ?, ?)",
                  (p, pm.get("juste", 0), pm.get("contestable", 0), pm.get("simplification", 0),
                   pm.get("angle_mort", 0), pm.get("faux", 0)))

    # Activity
    c.execute("CREATE TABLE activite (persona TEXT, sessions INTEGER)")
    for p, count in all_data["activite"]["by_persona"].items():
        c.execute("INSERT INTO activite VALUES (?, ?)", (p, count))

    # PO friction
    c.execute("CREATE TABLE friction_po (persona TEXT, juste INT, contestable INT, simplification INT, angle_mort INT, faux INT, total_sessions INT, sessions_with_friction INT, initiative_persona INT, initiative_po INT)")
    for p, d in all_data["friction_po"]["by_persona"].items():
        c.execute("INSERT INTO friction_po VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (p, d["juste"], d["contestable"], d["simplification"], d["angle_mort"], d["faux"],
                   d["total_sessions"], d["sessions_with_friction"], d["initiative_persona"], d["initiative_po"]))

    conn.commit()
    conn.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Audit a SOFIA instance")
    parser.add_argument("instance", help="Path to the SOFIA instance root")
    parser.add_argument("--format", choices=["md", "json", "csv", "sqlite"], default="md",
                        help="Output format (default: md)")
    args = parser.parse_args()

    instance_path = Path(args.instance).resolve()

    # Detect instance
    if not (instance_path / "sofia.md").is_file() and not (instance_path / "voix.md").is_file():
        print(f"✗ Instance introuvable : pas de sofia.md dans {instance_path}", file=sys.stderr)
        sys.exit(1)

    instance_name = instance_path.name
    fmt = args.format

    # Output directory
    output_dir = instance_path / "shared" / "audits"
    output_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()

    # Phase 1 — Structure
    checks = check_structure(instance_path)
    check_summary = defaultdict(int)
    for c in checks:
        check_summary[c["status"]] += 1

    structure_data = {
        "meta": {"instance": instance_name, "date": today, "sofia_md": (instance_path / "sofia.md").is_file()},
        "checks": checks,
        "summary": dict(check_summary),
    }

    # Phase 2 — Exchanges & friction
    artifacts, scan_warnings = scan_artifacts(instance_path)

    empty_instance = not artifacts

    if empty_instance:
        exchange_matrix = {}
        friction_matrix = {}
        marker_totals = {}
        all_personas = sorted(discover_personas(instance_path))
        notes_count = reviews_count = signals_count = 0
        echanges_data = {
            "meta": {"instance": instance_name, "date": today,
                     "notes_scanned": 0, "reviews_scanned": 0, "skipped": 0},
            "matrix": {},
        }
        friction_data = {
            "meta": {"instance": instance_name, "date": today,
                     "reviews": 0, "signals": 0},
            "matrix": {},
            "markers": {},
        }
    else:
        exchange_matrix = build_exchange_matrix(artifacts)
        friction_matrix = build_friction_matrix(artifacts)
        marker_totals = build_marker_totals(artifacts)

        all_personas_set = set()
        for a in artifacts:
            all_personas_set.add(a["de"])
            all_personas_set.update(a["pour"])
        all_personas = sorted(all_personas_set)

        notes_count = sum(1 for a in artifacts if a["source_dir"] == "note")
        reviews_count = sum(1 for a in artifacts if a["source_dir"] == "review")
        friction_arts = [a for a in artifacts if a["nature"] in ("review", "signal")]
        signals_count = sum(1 for a in friction_arts if a["nature"] == "signal")

        echanges_data = {
            "meta": {"instance": instance_name, "date": today,
                     "notes_scanned": notes_count, "reviews_scanned": reviews_count,
                     "skipped": len(scan_warnings)},
            "matrix": exchange_matrix,
        }

        friction_data = {
            "meta": {"instance": instance_name, "date": today,
                     "reviews": reviews_count, "signals": signals_count},
            "matrix": friction_matrix,
            "markers": marker_totals,
        }

    # Phase 2b — Orchestrator friction
    po_friction, po_warnings = scan_session_friction(instance_path)
    scan_warnings.extend(po_warnings)

    total_sessions = sum(d["total_sessions"] for d in po_friction.values())
    sessions_with = sum(d["sessions_with_friction"] for d in po_friction.values())

    po_data = {
        "meta": {"instance": instance_name, "date": today,
                 "sessions_scanned": total_sessions, "sessions_with_friction": sessions_with},
        "by_persona": po_friction,
    }

    # Activity
    by_persona_sessions = {p: d["total_sessions"] for p, d in po_friction.items()}
    activite_data = {
        "meta": {"instance": instance_name, "date": today, "total_sessions": total_sessions},
        "by_persona": by_persona_sessions,
    }

    # Discover real personas for signal filtering
    real_personas = discover_personas(instance_path)

    # Signals
    signals = generate_signals(exchange_matrix, friction_matrix, marker_totals, po_friction, all_personas, real_personas)

    # Report (always generated for stdout)
    report = generate_report_md(
        instance_name, checks, artifacts, scan_warnings,
        exchange_matrix, friction_matrix, marker_totals,
        po_friction, all_personas, signals)

    # All data for output writers
    all_data = {
        "structure": structure_data,
        "echanges": echanges_data,
        "friction": friction_data,
        "friction_po": po_data,
        "activite": activite_data,
    }

    # Write outputs based on format
    files_written = []

    if fmt == "md":
        (output_dir / "audit-report.md").write_text(report + "\n", encoding="utf-8")
        files_written.append("audit-report.md")

    elif fmt == "json":
        write_json(output_dir, all_data)
        files_written.extend(f"audit-{k}.json" for k in all_data)

    if fmt == "csv":
        write_csv(output_dir, all_data, all_personas)
        files_written.extend(["audit-echanges.csv", "audit-friction.csv", "audit-marqueurs.csv",
                              "audit-activite.csv", "audit-structure.csv"])

    if fmt == "sqlite":
        write_sqlite(output_dir, all_data, all_personas)
        files_written.append("audit.db")

    # Stdout
    print(report)
    print(f"✓ {output_dir.relative_to(instance_path)}/ : {', '.join(files_written)}")


if __name__ == "__main__":
    main()