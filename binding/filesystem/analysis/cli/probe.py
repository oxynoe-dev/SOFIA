"""probe.py — Produce probe.json from instance structure.

Reads instance directly (not records.json):
- Structural conformity checks (PS/PP/PA/PF/AN/AR/AF/IS/IN/IR)
- Signals (friction holes, domestication, etc.)
- Context sizes per persona
- Orchestrator friction from session summaries

This is the conformity pipeline — independent from the data pipeline.
Self-contained: no dependency on audit-instance.py.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from analysis.lib.constants import (
    FRICTION_MARKERS,
    RESOLUTION_TAGS,
    RESOLUTION_ALIASES,
    EMITTER_KEYS,
    RECIPIENT_KEYS,
    NATURE_KEYS,
    STATUT_KEYS,
    OBJET_KEYS,
    VALID_STATUTS,
    STATUT_ALIASES,
    strip_accents,
)
from analysis.lib.parser import (
    parse_frontmatter,
    parse_frontmatter_from_text,
    normalize_frontmatter,
    count_friction_markers_from_text,
    DEFAULT_ARTIFACT_TYPES,
    parse_artifact_types_from_conventions,
    resolve_artifact_dir,
    safe_relative,
    discover_personas,
    measure_context_sizes,
)


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------------------
# Phase 1 — Structural conformity
# ---------------------------------------------------------------------------

def check_structure(instance: Path, protocol_only: bool = False, artifact_types: set[str] | None = None, artifact_defs: dict | None = None) -> list[dict]:
    """Run structural conformity checks.

    protocol_only: skip instance-level checks
    artifact_types: set of artifact types to audit (default: {"notes", "reviews"})
    artifact_defs: dict mapping type name -> {dir, naming, extra_fields}
    """
    if artifact_types is None:
        artifact_types = {"notes", "reviews"}
    if artifact_defs is None:
        artifact_defs = dict(DEFAULT_ARTIFACT_TYPES)
    checks = []

    def add(cid: str, severity: str, passed: bool, detail: str, files: list[str] | None = None):
        status = "pass" if passed else severity
        entry = {"id": cid, "status": status, "detail": detail}
        if files:
            entry["files"] = files
        checks.append(entry)

    # PS1: sofia.md or voix.md (instance marker)
    marker_found = (instance / "sofia.md").is_file() or (instance / "voix.md").is_file()
    marker_name = "sofia.md" if (instance / "sofia.md").is_file() else "voix.md" if (instance / "voix.md").is_file() else "sofia.md/voix.md"
    add("PS1", "fail", marker_found, f"{marker_name} present" if marker_found else "sofia.md ou voix.md manquant")

    # PS2: shared/
    add("PS2", "fail", (instance / "shared").is_dir(), "shared/ present" if (instance / "shared").is_dir() else "shared/ manquant")

    # PS3: shared/conventions.md
    add("PS3", "warn", (instance / "shared" / "conventions.md").is_file(),
        "shared/conventions.md present" if (instance / "shared" / "conventions.md").is_file() else "shared/conventions.md manquant")

    # Prefix mapping: type name -> 2-letter prefix for check IDs
    _type_prefixes = {"notes": "AN", "reviews": "AR", "features": "AF", "adr": "AD"}

    # A{X}1: per-type directory presence (skipped in --protocol-only)
    if not protocol_only:
        for type_name in sorted(artifact_types):
            defn = artifact_defs.get(type_name)
            if not defn:
                continue
            prefix = _type_prefixes.get(type_name, "A" + type_name[0:1].upper())
            rel_dir = defn["dir"]
            type_dir = resolve_artifact_dir(instance, rel_dir)
            type_ok = type_dir.is_dir()
            type_archives = (type_dir / "archives").is_dir() if type_ok else False
            if type_ok and type_archives:
                add(f"{prefix}1", "info", True, f"{rel_dir}/ present avec archives/")
            elif type_ok:
                add(f"{prefix}1", "info", False, f"{rel_dir}/ present mais archives/ manquant")
            else:
                add(f"{prefix}1", "info", True, f"{rel_dir}/ absent (emerge a l'usage)")

        # IS1: shared/orga/
        add("IS1", "info", (instance / "shared" / "orga").is_dir(),
            "shared/orga/ present" if (instance / "shared" / "orga").is_dir() else "shared/orga/ manquant")

    # PS4: at least 1 workspace with CLAUDE.md
    workspaces = [d for d in instance.iterdir() if d.is_dir() and (d / "CLAUDE.md").is_file() and d.name != "shared"]
    add("PS4", "fail", len(workspaces) > 0,
        f"{len(workspaces)} workspaces avec CLAUDE.md" if workspaces else "aucun workspace avec CLAUDE.md")

    # PS5: each workspace has sessions/
    ws_without_sessions = [d.name for d in workspaces if not (d / "sessions").is_dir()]
    if ws_without_sessions:
        add("PS5", "warn", False, f"{len(ws_without_sessions)} workspaces sans sessions/", ws_without_sessions)
    else:
        add("PS5", "warn", True, "tous les workspaces ont sessions/")

    # -- PP: Protocol Persona checks --
    personas_dir = instance / "shared" / "orga" / "personas"
    contextes_dir = instance / "shared" / "orga" / "contextes"

    # PP1: persona files exist
    persona_files = list(personas_dir.glob("persona-*.md")) if personas_dir.is_dir() else []
    persona_names = [f.stem.removeprefix("persona-") for f in persona_files]
    if persona_files:
        add("PP1", "warn", True, f"{len(persona_files)} persona files dans shared/orga/personas/")
    else:
        add("PP1", "warn", False, "aucun persona-*.md dans shared/orga/personas/")

    # PP2: each workspace references an existing persona (via CLAUDE.md)
    orphan_ws = []
    for ws in workspaces:
        claude_md = ws / "CLAUDE.md"
        try:
            content = claude_md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            orphan_ws.append(ws.name)
            continue
        # Look for persona-*.md reference in CLAUDE.md
        found = False
        for pn in persona_names:
            if f"persona-{pn}" in content:
                found = True
                break
        # Also check for contexte-*.md reference (points to persona indirectly)
        if not found:
            for pn in persona_names:
                if f"contexte-{pn}" in content:
                    found = True
                    break
        if not found:
            orphan_ws.append(ws.name)
    if orphan_ws:
        add("PP2", "info", False, f"{len(orphan_ws)} workspaces sans reference persona dans CLAUDE.md", orphan_ws)
    else:
        add("PP2", "info", True, "tous les workspaces referencent un persona")

    # PP3: persona files have required sections (7 dimensions)
    # Bilingual section mapping -> dimension
    section_aliases = {
        # EN
        "profile": "identity", "identity": "identity",
        "stance": "stance", "posture": "stance",
        "scope": "scope", "domaines d'intervention": "scope", "domaines d intervention": "scope",
        "what they produce": "deliverables", "deliverables": "deliverables",
        "ce qu'il produit": "deliverables", "ce qu il produit": "deliverables",
        "ce qu'elle produit": "deliverables", "ce qu elle produit": "deliverables",
        "what they don't do": "prohibitions", "prohibitions": "prohibitions",
        "ce qu'il ne fait pas": "prohibitions", "ce qu il ne fait pas": "prohibitions",
        "ce qu'elle ne fait pas": "prohibitions", "ce qu elle ne fait pas": "prohibitions",
        "what they challenge": "challenge", "right to contest": "challenge",
        "ce qu'il challenge": "challenge", "ce qu il challenge": "challenge",
        "ce qu'elle challenge": "challenge", "ce qu elle challenge": "challenge",
        "collaboration": "collaboration",
        # FR aliases
        "profil": "identity",
    }
    required_dimensions = {"identity", "stance", "scope", "deliverables", "prohibitions", "challenge", "collaboration"}
    pp3_issues = []
    for pf in persona_files:
        try:
            text = pf.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # Extract ## sections
        found_dims = set()
        for line in text.splitlines():
            if line.startswith("## "):
                section_name = strip_accents(line[3:].strip().lower())
                dim = section_aliases.get(section_name)
                if dim:
                    found_dims.add(dim)
        missing_dims = required_dimensions - found_dims
        if missing_dims:
            pp3_issues.append(f"{pf.name} (missing: {', '.join(sorted(missing_dims))})")
    if pp3_issues:
        add("PP3", "warn", False, f"{len(pp3_issues)} personas avec dimensions manquantes", pp3_issues)
    else:
        add("PP3", "warn", True, f"tous les personas ont les 7 dimensions")

    # PP4: each persona has a context file
    pp4_missing = []
    if contextes_dir.is_dir():
        for name in persona_names:
            matches = list(contextes_dir.glob(f"contexte-{name}*.md"))
            if not matches:
                pp4_missing.append(name)
    else:
        pp4_missing = persona_names.copy()
    if pp4_missing:
        add("PP4", "info", False, f"{len(pp4_missing)} personas sans contexte", pp4_missing)
    else:
        add("PP4", "info", True, "tous les personas ont un fichier contexte")

    # IS2: roadmaps (emerge a l'usage -- absent = normal) -- instance level
    roadmaps = list((instance / "shared").glob("roadmap-*.md")) if (instance / "shared").is_dir() else []
    if not protocol_only:
        add("IS2", "info", True,
            f"{len(roadmaps)} roadmaps dans shared/" if roadmaps else "aucune roadmap dans shared/ (emerge a l'usage)")

    # -- PA: Protocol Artifact -- global checks on ALL .md in shared/ --
    # Scan every .md under shared/ except: conventions.md, roadmap-*.md, orga/
    shared_dir = instance / "shared"
    pa_files = []
    if shared_dir.is_dir():
        exclude_dirs = {"orga", "audits"}
        for f in shared_dir.rglob("*.md"):
            rel_parts = f.relative_to(shared_dir).parts
            if rel_parts[0] in exclude_dirs:
                continue
            if f.name == "conventions.md":
                continue
            if f.name.startswith("roadmap-"):
                continue
            pa_files.append(f)

    # PA1: frontmatter present on all artifacts in shared/
    pa_no_fm = [str(f.relative_to(instance)) for f in pa_files if parse_frontmatter(f) is None]
    if pa_no_fm:
        add("PA1", "warn", False, f"{len(pa_no_fm)}/{len(pa_files)} artifacts sans frontmatter dans shared/", pa_no_fm)
    else:
        add("PA1", "warn", True, f"{len(pa_files)} artifacts avec frontmatter dans shared/")

    # PA2: required fields (from, to, nature, status, date) on all artifacts
    pa_required = {"de", "pour", "nature", "statut", "date"}
    pa_missing_files = []
    for f in pa_files:
        fm = parse_frontmatter(f)
        if fm is None:
            continue
        fm_keys = set(fm.keys())
        has_emitter = bool(fm_keys & EMITTER_KEYS)
        has_recipient = bool(fm_keys & RECIPIENT_KEYS)
        has_nature = bool(fm_keys & NATURE_KEYS)
        has_statut = bool(fm_keys & STATUT_KEYS)
        has_date = "date" in fm_keys
        missing = []
        if not has_emitter:
            missing.append("from")
        if not has_recipient:
            missing.append("to")
        if not has_nature:
            missing.append("nature")
        if not has_statut:
            missing.append("status")
        if not has_date:
            missing.append("date")
        if missing:
            pa_missing_files.append(f"{f.relative_to(instance)} (missing: {', '.join(missing)})")
    if pa_missing_files:
        add("PA2", "warn", False, f"{len(pa_missing_files)} artifacts avec champs manquants", pa_missing_files)
    else:
        add("PA2", "warn", True, f"tous les artifacts ont les champs requis")

    # PA3: valid status values on all artifacts
    pa_bad_statut = []
    for f in pa_files:
        fm = parse_frontmatter(f)
        if fm is None:
            continue
        statut_key = next((k for k in STATUT_KEYS if k in fm), None)
        if statut_key is None:
            continue
        val = strip_accents(fm[statut_key].lower().strip())
        if val not in VALID_STATUTS:
            pa_bad_statut.append(f"{f.relative_to(instance)} (status: {fm[statut_key]})")
    if pa_bad_statut:
        add("PA3", "warn", False, f"{len(pa_bad_statut)} artifacts avec statut invalide", pa_bad_statut)
    else:
        add("PA3", "warn", True, "tous les statuts artifacts sont valides")

    # -- Per-type artifact checks (dynamic from artifact_defs) --
    base_required = {"de", "pour", "nature", "statut", "date"}

    for type_name in sorted(artifact_types):
        defn = artifact_defs.get(type_name)
        if not defn:
            continue
        prefix = _type_prefixes.get(type_name)
        if not prefix:
            # Dynamic prefix: first letter uppercase + second letter, e.g. "specs" -> "AS"
            prefix = "A" + type_name[0:1].upper()
        rel_dir = defn["dir"]
        base = resolve_artifact_dir(instance, rel_dir)
        extra_fields = defn.get("extra_fields", set())
        naming_re = defn.get("naming", "")

        # {prefix}2: frontmatter presence
        if base.is_dir():
            all_md = list(base.rglob("*.md"))
            no_fm = [safe_relative(f, instance) for f in all_md if parse_frontmatter(f) is None]
            if no_fm:
                add(f"{prefix}2", "warn", False, f"{len(no_fm)}/{len(all_md)} {type_name} sans frontmatter", no_fm)
            else:
                add(f"{prefix}2", "warn", True, f"{len(all_md)} {type_name} avec frontmatter")

        # {prefix}3: required fields
        required = base_required | extra_fields
        if base.is_dir():
            missing_fields_files = []
            for f in base.rglob("*.md"):
                fm = parse_frontmatter(f)
                if fm is None:
                    continue
                fm_keys = set(fm.keys())
                has_emitter = bool(fm_keys & EMITTER_KEYS)
                has_recipient = bool(fm_keys & RECIPIENT_KEYS)
                has_nature = bool(fm_keys & NATURE_KEYS)
                has_statut = bool(fm_keys & STATUT_KEYS)
                has_date = "date" in fm_keys
                has_objet = bool(fm_keys & OBJET_KEYS)
                missing = []
                if not has_emitter:
                    missing.append("from")
                if not has_recipient:
                    missing.append("to")
                if not has_nature:
                    missing.append("nature")
                if not has_statut:
                    missing.append("status")
                if not has_date:
                    missing.append("date")
                if "objet" in extra_fields and not has_objet:
                    missing.append("subject")
                if missing:
                    missing_fields_files.append(f"{safe_relative(f, instance)} (missing: {', '.join(missing)})")
            if missing_fields_files:
                add(f"{prefix}3", "warn", False, f"{len(missing_fields_files)} {type_name} avec champs manquants", missing_fields_files)
            else:
                add(f"{prefix}3", "warn", True, f"tous les {type_name} ont les champs requis")

    # IS3: accents in frontmatter values -- instance level
    if not protocol_only:
        accent_files = []
        for rel_dir in ["shared/notes", "shared/review"]:
            base = resolve_artifact_dir(instance, rel_dir)
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
            add("IS3", "info", False, f"{len(accent_files)} fichiers avec accents dans le frontmatter", accent_files)
        else:
            add("IS3", "info", True, "pas d'accents dans les valeurs frontmatter")

    # PF1: sessions frontmatter
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
        add("PF1", "info", False, f"{len(bad_sessions)}/{len(session_files)} sessions sans frontmatter conforme", bad_sessions)
    else:
        add("PF1", "info", True, f"{len(session_files)} sessions avec frontmatter conforme")

    # A{X}4: naming conventions -- instance level
    if protocol_only:
        return checks

    for type_name in sorted(artifact_types):
        defn = artifact_defs.get(type_name)
        if not defn or not defn.get("naming"):
            continue
        prefix = _type_prefixes.get(type_name, "A" + type_name[0:1].upper())
        rel_dir = defn["dir"]
        base = resolve_artifact_dir(instance, rel_dir)
        if not base.is_dir():
            continue
        pattern = re.compile(defn["naming"])
        bad_names = []
        for f in base.rglob("*.md"):
            if "archives" in f.relative_to(base).parts or "archive" in f.relative_to(base).parts:
                continue
            if not pattern.match(f.name):
                bad_names.append(safe_relative(f, instance))
        if bad_names:
            add(f"{prefix}4", "info", False, f"{len(bad_names)} {type_name} hors convention de nommage", bad_names)
        else:
            add(f"{prefix}4", "info", True, f"tous les {type_name} suivent la convention")

    roadmap_pattern = re.compile(r"^roadmap-.+\.md$")
    if roadmaps:
        bad_rm = [str(f.relative_to(instance)) for f in roadmaps if not roadmap_pattern.match(f.name)]
        if bad_rm:
            add("IN1", "info", False, f"{len(bad_rm)} roadmaps hors convention", bad_rm)
        else:
            add("IN1", "info", True, "toutes les roadmaps suivent roadmap-{{produit}}.md")

    # A{X}5: done files not in archives/
    for type_name in sorted(artifact_types):
        defn = artifact_defs.get(type_name)
        if not defn:
            continue
        prefix = _type_prefixes.get(type_name, "A" + type_name[0:1].upper())
        rel_dir = defn["dir"]
        base = resolve_artifact_dir(instance, rel_dir)
        if not base.is_dir():
            continue
        misplaced = []
        for f in base.rglob("*.md"):
            in_archives = "archives" in f.relative_to(base).parts or "archive" in f.relative_to(base).parts
            if in_archives:
                continue
            fm = parse_frontmatter(f)
            if fm is None:
                continue
            statut_raw = next((fm[k] for k in STATUT_KEYS if k in fm), "")
            statut = strip_accents(statut_raw.lower().strip())
            if statut in ("traite", "done"):
                misplaced.append(safe_relative(f, instance))
        if misplaced:
            add(f"{prefix}5", "warn", False, f"{len(misplaced)} {type_name} done hors archives/", misplaced)
        else:
            add(f"{prefix}5", "warn", True, f"tous les {type_name} done sont dans archives/")

    # IS4: files in archives/ with non-traite status
    bad_archive = []
    for rel_dir in ["shared/notes", "shared/review"]:
        base = resolve_artifact_dir(instance, rel_dir)
        if not base.is_dir():
            continue
        for f in base.rglob("*.md"):
            in_archives = "archives" in f.relative_to(base).parts or "archive" in f.relative_to(base).parts
            if not in_archives:
                continue
            fm = parse_frontmatter(f)
            if fm is None:
                continue
            statut_raw = next((fm[k] for k in STATUT_KEYS if k in fm), "")
            statut = strip_accents(statut_raw.lower().strip())
            if statut and statut not in ("traite", "done"):
                bad_archive.append(f"{f.relative_to(instance)} (statut: {statut_raw})")
    if bad_archive:
        add("IS4", "info", False, f"{len(bad_archive)} fichiers dans archives/ sans statut traite", bad_archive)
    else:
        add("IS4", "info", True, "tous les fichiers dans archives/ ont statut traite")

    # IR1-IR8: roadmap checks
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

            # IR1: header format -- # Roadmap {Nom}
            has_header = bool(lines_text) and lines_text[0].startswith("# Roadmap")
            if not has_header:
                no_header.append(rel)

            # IR2: owner in blockquote -- > ... Owner : @persona
            has_owner_header = bool(re.search(r"^>\s*.*[Oo]wners?\s*:\s*@\w+", text, re.MULTILINE))
            if not has_owner_header:
                no_owner_header.append(rel)

            # IR3: version metadata comments -- <!-- produit: X | ... statut: X -->
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

                # IR4: status marker
                has_status = bool(re.search(r"\[(done|running|todo|blocked|ready)\]", stripped))
                if not has_status:
                    items_without_status.append(f"{rel}:{lineno}")

                # IR5: @owner
                has_owner = bool(re.search(r"@\w+", stripped))
                if not has_owner:
                    items_without_owner.append(f"{rel}:{lineno}")

                # convergence marker
                if "\u2194" in stripped:
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

        # IR1: header
        if no_header:
            add("IR1", "warn", False, f"{len(no_header)} roadmaps sans en-tete '# Roadmap'", no_header)
        else:
            add("IR1", "warn", True, "toutes les roadmaps ont un en-tete conforme")

        # IR2: owner in header
        if no_owner_header:
            add("IR2", "warn", False, f"{len(no_owner_header)} roadmaps sans Owner dans le blockquote", no_owner_header)
        else:
            add("IR2", "warn", True, "toutes les roadmaps declarent un Owner")

        # IR3: version metadata
        if no_version_meta:
            add("IR3", "info", False, f"{len(no_version_meta)} roadmaps avec sections ### sans commentaire metadata", no_version_meta)
        else:
            add("IR3", "info", True, "toutes les sections version ont un commentaire metadata")

        # IR4: status per item
        if items_without_status:
            add("IR4", "warn", False, f"{len(items_without_status)}/{total_items} items sans statut [done/running/todo/blocked/ready]", items_without_status[:20])
        else:
            add("IR4", "warn", True, f"tous les {total_items} items ont un statut")

        # IR5: @owner per item
        if items_without_owner:
            add("IR5", "warn", False, f"{len(items_without_owner)}/{total_items} items sans @porteur", items_without_owner[:20])
        else:
            add("IR5", "warn", True, f"tous les {total_items} items ont un @porteur")

        # IR6: convergence markers
        if no_convergence:
            add("IR6", "info", False,
                f"{len(no_convergence)}/{len(roadmaps)} roadmaps sans marqueur \u2194 ({total_with_convergence} marqueurs au total)",
                no_convergence)
        else:
            add("IR6", "info", True, f"toutes les roadmaps utilisent \u2194 ({total_with_convergence} marqueurs)")

        # IR7: cible markers
        if no_cible:
            add("IR7", "info", False,
                f"{len(no_cible)}/{len(roadmaps)} roadmaps sans marqueur cible: ({total_with_cible} marqueurs au total)",
                no_cible)
        else:
            add("IR7", "info", True, f"toutes les roadmaps utilisent cible: ({total_with_cible} marqueurs)")

        # IR8: source markers
        if no_source:
            add("IR8", "info", False,
                f"{len(no_source)}/{len(roadmaps)} roadmaps sans marqueur source: ({total_with_source} marqueurs au total)",
                no_source)
        else:
            add("IR8", "info", True, f"toutes les roadmaps utilisent source: ({total_with_source} marqueurs)")

    return checks


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
                "pour": normalized.get("pour", []),
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
    """Parse ## Orchestrator friction / ## Friction orchestrateur sections from session files."""
    by_persona: dict[str, dict] = defaultdict(lambda: {
        "sound": 0, "contestable": 0, "simplification": 0,
        "blind_spot": 0, "refuted": 0,
        "total_sessions": 0, "sessions_with_friction": 0,
        "initiative_persona": 0, "initiative_po": 0,
        "resolution_ratified": 0, "resolution_contested": 0,
        "resolution_revised": 0, "resolution_rejected": 0,
        "resolution_missing": 0, "ref_count": 0,
        "signaler_pattern_count": 0,
        "signaler_pattern_erreur_llm": 0,
        "signaler_pattern_conviction": 0,
        "signaler_pattern_resistance": 0,
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

        # Find ## Orchestrator friction / ## Friction orchestrateur section
        lines = text.splitlines()
        in_section = False
        friction_lines = []
        for line in lines:
            stripped = line.strip()
            if (stripped.startswith("## Friction") or stripped.startswith("## Orchestrator friction")) and not stripped.startswith("## Friction Engineering"):
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

            # Count markers -- content after "- "
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

            # Resolution tag (-> ratified/contested/revised/rejected + FR aliases)
            resolution_match = re.search(r"\u2192\s*(\w+)", stripped)
            if resolution_match:
                tag = strip_accents(resolution_match.group(1).lower())
                if tag in RESOLUTION_ALIASES:
                    by_persona[persona][f"resolution_{RESOLUTION_ALIASES[tag]}"] += 1
                elif tag in RESOLUTION_TAGS:
                    by_persona[persona][f"resolution_{tag}"] += 1
            else:
                by_persona[persona]["resolution_missing"] += 1

            # ref: (mutabilite inter-sessions)
            if "(ref:" in stripped or "ref:" in stripped:
                by_persona[persona]["ref_count"] += 1

        if has_friction:
            by_persona[persona]["sessions_with_friction"] += 1

        # signalerPattern section
        in_sp = False
        for line in lines:
            if line.strip().startswith("## signalerPattern") or line.strip().startswith("## reportPattern"):
                in_sp = True
                by_persona[persona]["signaler_pattern_count"] += 1
                continue
            if in_sp and line.strip().startswith("## "):
                break
            if in_sp and (line.strip().startswith("- Choix") or line.strip().startswith("- Choice")):
                choix_match = re.search(r"(?:Choix|Choice)\s*:\s*(.+)", line.strip())
                if choix_match:
                    choix = strip_accents(choix_match.group(1).strip().lower())
                    if "erreur" in choix or "llm" in choix:
                        by_persona[persona]["signaler_pattern_erreur_llm"] += 1
                    elif "conviction" in choix:
                        by_persona[persona]["signaler_pattern_conviction"] += 1
                    elif "resistance" in choix:
                        by_persona[persona]["signaler_pattern_resistance"] += 1

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
        if total > 0 and pm.get("sound", 0) == total:
            signals.append(f"Domestication inter-personas (100% sound) : {p}")

    # Domestication orchestrator
    for p, data in po_friction.items():
        if real_personas and p not in real_personas:
            continue
        total = data["sound"] + data["contestable"] + data["simplification"] + data["blind_spot"] + data["refuted"]
        if total > 0 and data["sound"] == total and data["total_sessions"] >= 10:
            signals.append(f"Domestication orchestrateur (100% sound, {data['total_sessions']} sessions) : {p}")

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
    resolution_cols = ["ratified", "contested", "revised", "rejected", "no-res"]
    extra_cols = ["sessions", "w/friction", "init.persona", "init.PO"]
    sp_cols = ["sp.count"]
    all_cols = marker_keys + resolution_cols + extra_cols + sp_cols
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
        for tag in ["ratified", "contested", "revised", "rejected"]:
            row += str(d.get(f"resolution_{tag}", 0)).rjust(col_width)
        row += str(d.get("resolution_missing", 0)).rjust(col_width)
        row += str(d["total_sessions"]).rjust(col_width)
        row += str(d["sessions_with_friction"]).rjust(col_width)
        row += str(d["initiative_persona"]).rjust(col_width)
        row += str(d["initiative_po"]).rjust(col_width)
        row += str(d.get("signaler_pattern_count", 0)).rjust(col_width)
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
    lines.append(f"# Audit instance \u2014 {instance_name} ({today})")
    lines.append("")

    # Phase 1
    lines.append("## Phase 1 \u2014 Conformite structurelle")
    lines.append("")
    summary = defaultdict(int)
    for c in checks:
        summary[c["status"]] += 1
        icon = {"pass": "\u2713", "warn": "\u26a0", "fail": "\u2717", "info": "\u2139"}.get(c["status"], "?")
        lines.append(f"- [{icon}] **{c['id']}** \u2014 {c['detail']}")
    lines.append("")
    lines.append(f"**Total** : {summary['pass']} pass, {summary['warn']} warn, {summary['fail']} fail, {summary['info']} info")
    lines.append("")

    # Phase 2
    lines.append("## Phase 2 \u2014 Echanges & friction")
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
        lines.append("### Orchestrator friction")
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
            lines.append(f"- \u26a0 {w}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output writers
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
    c.execute("CREATE TABLE marqueurs (persona TEXT, sound INT, contestable INT, simplification INT, blind_spot INT, refuted INT)")
    for p in all_personas:
        pm = all_data["friction"]["markers"].get(p, {})
        c.execute("INSERT INTO marqueurs VALUES (?, ?, ?, ?, ?, ?)",
                  (p, pm.get("sound", 0), pm.get("contestable", 0), pm.get("simplification", 0),
                   pm.get("blind_spot", 0), pm.get("refuted", 0)))

    # Activity
    c.execute("CREATE TABLE activite (persona TEXT, sessions INTEGER)")
    for p, count in all_data["activite"]["by_persona"].items():
        c.execute("INSERT INTO activite VALUES (?, ?)", (p, count))

    # PO friction
    c.execute("""CREATE TABLE friction_po (
        persona TEXT, sound INT, contestable INT, simplification INT, blind_spot INT, refuted INT,
        resolution_ratified INT, resolution_contested INT, resolution_revised INT, resolution_rejected INT, resolution_missing INT,
        total_sessions INT, sessions_with_friction INT, initiative_persona INT, initiative_po INT,
        ref_count INT, signaler_pattern_count INT,
        signaler_pattern_erreur_llm INT, signaler_pattern_conviction INT, signaler_pattern_resistance INT
    )""")
    for p, d in all_data["friction_po"]["by_persona"].items():
        c.execute("INSERT INTO friction_po VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (p, d["sound"], d["contestable"], d["simplification"], d["blind_spot"], d["refuted"],
                   d.get("resolution_ratified", 0), d.get("resolution_contested", 0),
                   d.get("resolution_revised", 0), d.get("resolution_rejected", 0), d.get("resolution_missing", 0),
                   d["total_sessions"], d["sessions_with_friction"], d["initiative_persona"], d["initiative_po"],
                   d.get("ref_count", 0), d.get("signaler_pattern_count", 0),
                   d.get("signaler_pattern_erreur_llm", 0), d.get("signaler_pattern_conviction", 0),
                   d.get("signaler_pattern_resistance", 0)))

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Probe orchestration
# ---------------------------------------------------------------------------

def probe_instance(instance_path: Path) -> dict:
    """Run full probe on an instance. Returns probe data."""
    # Artifact types from conventions
    declared_types = parse_artifact_types_from_conventions(instance_path)
    artifact_types = set(declared_types.keys()) if declared_types else {"notes", "reviews"}
    artifact_defs = dict(DEFAULT_ARTIFACT_TYPES)
    if declared_types:
        artifact_defs.update(declared_types)

    # Phase 1 -- Structure checks
    checks = check_structure(instance_path, artifact_types=artifact_types, artifact_defs=artifact_defs)

    # Phase 2 -- Exchanges & friction from artifacts
    artifacts, scan_warnings = scan_artifacts(instance_path)
    exchange_matrix = build_exchange_matrix(artifacts) if artifacts else {}
    friction_matrix = build_friction_matrix(artifacts) if artifacts else {}
    marker_totals = build_marker_totals(artifacts) if artifacts else {}

    # Phase 2b -- Orchestrator friction from sessions
    po_friction, po_warnings = scan_session_friction(instance_path)

    # Personas
    real_personas = discover_personas(instance_path)
    all_personas_set = set()
    for a in artifacts:
        all_personas_set.add(a["de"])
        all_personas_set.update(a["pour"])
    all_personas = sorted(all_personas_set)

    # Signals
    signals = generate_signals(exchange_matrix, friction_matrix, marker_totals, po_friction, all_personas, real_personas)

    # Context sizes
    context_sizes = measure_context_sizes(instance_path)

    # Activity (sessions per persona)
    by_persona_sessions = {p: d["total_sessions"] for p, d in po_friction.items()}
    total_sessions = sum(d["total_sessions"] for d in po_friction.values())

    return {
        "meta": {
            "instance": instance_path.name,
            "date": date.today().isoformat(),
        },
        "structure": {"checks": checks},
        "friction_po": {"by_persona": po_friction},
        "context_sizes": context_sizes,
        "signals": signals,
        "exchange_matrix": exchange_matrix,
        "friction_matrix": friction_matrix,
        # Legacy compat for dashboard
        "activite": {"meta": {"total_sessions": total_sessions}, "by_persona": by_persona_sessions},
        "echanges": {"matrix": exchange_matrix},
        "friction": {"matrix": friction_matrix, "markers": marker_totals},
    }


def probe_instances(instance_paths: list[Path]) -> dict:
    """Probe multiple instances."""
    result = {}
    for path in instance_paths:
        result[path.name] = probe_instance(path)
    return result


def write_probe(probe_data: dict, output_path: Path | None = None):
    """Write probe.json."""
    if output_path is None:
        output_path = DATA_DIR / "probe.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(probe_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# CLI — backward-compatible main()
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Audit a SOFIA instance")
    parser.add_argument("instance", help="Path to the SOFIA instance root")
    parser.add_argument("--format", choices=["md", "json", "csv", "sqlite"], default="md",
                        help="Output format (default: md)")
    parser.add_argument("--protocol-only", action="store_true",
                        help="Skip instance-level checks (AN1-AR1, IS2, IS3, AN4-IN1, AN5-AR5, IS4, IR1-IR8)")
    parser.add_argument("--artifacts", type=str, default=None,
                        help="Comma-separated artifact types to audit (default: notes,reviews). "
                             "Use 'notes,reviews,features' to include features.")
    args = parser.parse_args()

    instance_path = Path(args.instance).resolve()

    # Detect instance
    if not (instance_path / "sofia.md").is_file() and not (instance_path / "voix.md").is_file():
        print(f"\u2717 Instance introuvable : pas de sofia.md dans {instance_path}", file=sys.stderr)
        sys.exit(1)

    instance_name = instance_path.name
    fmt = args.format

    # Output directory
    output_dir = instance_path / "shared" / "audits"
    output_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()

    # Parse artifact types -- CLI flag overrides, then conventions.md, then defaults
    declared_types = parse_artifact_types_from_conventions(instance_path)
    if args.artifacts:
        artifact_types = set(a.strip() for a in args.artifacts.split(","))
    elif declared_types:
        artifact_types = set(declared_types.keys())
    else:
        artifact_types = {"notes", "reviews"}

    # Merge declared type definitions with defaults
    artifact_defs = dict(DEFAULT_ARTIFACT_TYPES)
    if declared_types:
        for name, defn in declared_types.items():
            artifact_defs[name] = defn

    # Phase 1 -- Structure
    checks = check_structure(instance_path, protocol_only=args.protocol_only, artifact_types=artifact_types, artifact_defs=artifact_defs)
    check_summary = defaultdict(int)
    for c in checks:
        check_summary[c["status"]] += 1

    structure_data = {
        "meta": {"instance": instance_name, "date": today, "sofia_md": (instance_path / "sofia.md").is_file()},
        "checks": checks,
        "summary": dict(check_summary),
    }

    # Phase 2 -- Exchanges & friction
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

    # Phase 2b -- Orchestrator friction
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

    # Context sizes
    context_sizes = measure_context_sizes(instance_path)

    # All data for output writers
    all_data = {
        "structure": structure_data,
        "echanges": echanges_data,
        "friction": friction_data,
        "friction_po": po_data,
        "activite": activite_data,
        "context_sizes": context_sizes,
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
    print(f"\u2713 {output_dir.relative_to(instance_path)}/ : {', '.join(files_written)}")


if __name__ == "__main__":
    main()
