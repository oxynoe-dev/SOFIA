#!/usr/bin/env python3
"""create-instance.py — Scaffold a new SOFIA instance.

Usage:
    python create-instance.py <instance-path> [--personas alice,bob] [--produit myproject]

Creates the minimal directory structure with conventions and placeholder files.
Sofia fills in the content (personas, contextes).

Scaffolding minimal: sofia.md, shared/conventions.md, shared/orga/, workspaces.
Les sous-repertoires de shared/ (notes/, review/, etc.) emergent a l'usage.

Zero external dependency — Python 3.10+ stdlib only.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from datetime import date


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

CONVENTIONS_TEMPLATE = Path(__file__).parent / "conventions.md"


def sofia_md(instance_name: str, produit: str, personas: list[str]) -> str:
    rows = ""
    for p in personas:
        rows += f"| `{p}/` | Workspace | {p.capitalize()} |\n"
    rows += "| `shared/` | Bus d'echange inter-personas | Partage |"

    return f"""# Instance SOFIA

Ce depot est une **instance de la methode SOFIA**.

- **Methode** : [oxynoe-dev/sofia](https://github.com/oxynoe-dev/sofia)
- **Version methode appliquee** : v0.3.x
- **Projet** : {produit}
- **Equipe** : {len(personas)} assistants IA specialises + 1 orchestrateur humain

## Structure instance

| Dossier | Role | Persona |
|---------|------|---------|
{rows}

## Conventions

Voir `shared/conventions.md`.
"""


def load_conventions(instance_name: str) -> str:
    """Load conventions from template file, or return minimal fallback."""
    if CONVENTIONS_TEMPLATE.is_file():
        return CONVENTIONS_TEMPLATE.read_text(encoding="utf-8")
    # Fallback minimal si le template n'est pas trouve
    return f"""# Conventions

> Conventions de cette instance. Completer selon les besoins du projet.
"""


def team_orga_md(instance_name: str, personas: list[str]) -> str:
    rows = ""
    for p in personas:
        rows += f"| {p.capitalize()} | *a definir* | `{p}/` |\n"

    return f"""# Team-orga — {instance_name}

## Personas

| Persona | Role | Workspace |
|---------|------|-----------|
{rows}| Orchestrateur | Arbitrage, validation | — |

## Flux de collaboration

*A completer apres calibrage des personas.*

| De | Vers | Mode |
|----|------|------|

## RACI

*Optionnel — a completer si pertinent.*
"""


def persona_placeholder(name: str) -> str:
    return f"""---
nom: {name.capitalize()}
role: *a definir par Sofia*
---

# {name.capitalize()} — *role a definir*

**Role** : *a definir*
**Statut** : Assistant IA specialise

---

## Profil

*A completer.*

---

## Posture

- *A completer*

---

## Domaines d'intervention

- *A completer*

---

## Ce qu'il/elle produit

- *A completer*

---

## Ce qu'il/elle challenge

- *A completer*

---

## Ce qu'il/elle ne fait pas

- *A completer*

---

## Collaboration

| Avec | Mode |
|------|------|

---

*Instance {name} — {date.today().year}*
"""


def contexte_placeholder(name: str, produit: str, workspace: str) -> str:
    return f"""---
persona: {name}
produit: {produit}
---

# Contexte {name.capitalize()} — {produit} ({workspace}/)

## Perimetre

Ce workspace contient :
- *A completer*

## Documents cles

### Dans ce workspace ({workspace}/)

| Fichier | Role |
|---------|------|
| *A completer* | |

### Dans le repo produit ({produit}/)

| Chemin | Role |
|--------|------|
| *A completer* | |

## Isolation

- **Ne jamais lire/ecrire en dehors de** `*a definir*`

## Conventions

- **Langue** : francais
- **Bus shared/** : voir `shared/conventions.md`
- **Roadmaps** : chaque item porte un `@owner`

## Workflow

0. **Ouverture de session** : lire le dernier resume dans `sessions/`
1. **Lire** les documents existants avant toute intervention
2. **Produire** dans son perimetre
3. **Deposer** les artefacts pour les autres personas dans `shared/`

## Emergence

Quand tu deflectes une question parce qu'elle sort de ton perimetre,
note le domaine. Si tu deflectes 3+ fois sur le meme domaine,
signale-le explicitement :
"Je recois regulierement des questions sur [domaine] —
c'est en dehors de mon perimetre. Ce sujet releve d'un autre persona."

## Session protocol — mandatory

Summary: `sessions/{{YYYY-MM-DD}}-{{HHmm}}-{name}.md`. No prose, 30 lines max.

Mandatory sections (MUST): `## Produced`, `## Decisions`, `## Shared notes`, `## Open`.
Observational sections: `## Orchestrator friction` (SHOULD), `## Flow` (MAY).

Friction format: `{{symbol}} [{{marker}}] {{description}} — [{{initiative}}] → {{resolution}}`
- Markers: ✓ `[sound]`, ~ `[contestable]`, ⚡ `[simplification]`, ◐ `[blind_spot]`, ✗ `[refuted]`
- Initiative: `[persona]` or `[PO]`
- Resolution (SHOULD): `→ ratified`, `→ contested`, `→ revised`, `→ rejected`

Closure: the orchestrator gives the signal. Produce the full summary with the real content of the session — do not reproduce the format, apply it. Then display a validation block (sections filled, frictions qualified, frontmatter, commit message). Wait for orchestrator confirmation before committing.

Commit: `{name}: {{short summary}} ({{date}})`.
"""


def claude_md(name: str, produit: str) -> str:
    return f"""Quel que soit le premier message de l'utilisateur, a l'ouverture de session, avant toute reponse, lis ces deux fichiers :
- `../shared/orga/personas/persona-{name}.md`
- `../shared/orga/contextes/contexte-{name}-{produit}.md`
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def create_instance(instance_path: Path, personas: list[str], produit: str) -> list[str]:
    """Create the full instance structure. Returns list of files created."""
    created = []
    instance_name = instance_path.name

    # Root
    instance_path.mkdir(parents=True, exist_ok=True)

    # sofia.md
    f = instance_path / "sofia.md"
    f.write_text(sofia_md(instance_name, produit, personas), encoding="utf-8")
    created.append("sofia.md")

    # shared/ — scaffolding minimal (pas de notes/, review/, features/)
    for d in ["shared/orga/personas", "shared/orga/contextes"]:
        (instance_path / d).mkdir(parents=True, exist_ok=True)

    # conventions.md — depuis le template
    f = instance_path / "shared" / "conventions.md"
    f.write_text(load_conventions(instance_name), encoding="utf-8")
    created.append("shared/conventions.md")

    # team-orga.md
    f = instance_path / "shared" / "orga" / "team-orga.md"
    f.write_text(team_orga_md(instance_name, personas), encoding="utf-8")
    created.append("shared/orga/team-orga.md")

    # Per persona
    for name in personas:
        name_lower = name.lower()
        workspace = name_lower

        # Persona file
        f = instance_path / "shared" / "orga" / "personas" / f"persona-{name_lower}.md"
        f.write_text(persona_placeholder(name_lower), encoding="utf-8")
        created.append(f"shared/orga/personas/persona-{name_lower}.md")

        # Contexte file
        produit_slug = produit.lower().replace(" ", "-")
        f = instance_path / "shared" / "orga" / "contextes" / f"contexte-{name_lower}-{produit_slug}.md"
        f.write_text(contexte_placeholder(name_lower, produit, workspace), encoding="utf-8")
        created.append(f"shared/orga/contextes/contexte-{name_lower}-{produit_slug}.md")

        # Workspace
        ws = instance_path / workspace
        ws.mkdir(parents=True, exist_ok=True)
        (ws / "sessions").mkdir(exist_ok=True)

        # CLAUDE.md
        f = ws / "CLAUDE.md"
        f.write_text(claude_md(name_lower, produit_slug), encoding="utf-8")
        created.append(f"{workspace}/CLAUDE.md")

    return created


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new SOFIA instance",
        epilog="The script creates the structure. Sofia fills the content."
    )
    parser.add_argument("instance", help="Path to create the instance")
    parser.add_argument("--personas", required=True,
                        help="Comma-separated persona names (e.g. alice,bob)")
    parser.add_argument("--produit", required=True,
                        help="Project/product name")
    args = parser.parse_args()

    instance_path = Path(args.instance).resolve()
    personas = [p.strip() for p in args.personas.split(",") if p.strip()]

    if len(personas) < 2:
        print("✗ Minimum 2 personas requis — un persona seul ne genere pas de friction.", file=sys.stderr)
        sys.exit(1)

    if instance_path.exists() and any(instance_path.iterdir()):
        if (instance_path / "sofia.md").is_file():
            print(f"✗ Instance deja existante : {instance_path}/sofia.md", file=sys.stderr)
            sys.exit(1)

    print(f"Creation instance SOFIA : {instance_path}")
    print(f"Personas : {', '.join(personas)}")
    print(f"Produit : {args.produit}")
    print()

    created = create_instance(instance_path, personas, args.produit)

    for f in created:
        print(f"  ✓ {f}")

    print()
    print(f"✓ Instance creee — {len(created)} fichiers.")
    print(f"  Sofia peut maintenant remplir le contenu des personas et contextes.")
    print(f"  Pour lancer un persona : cd {instance_path}/{{workspace}} && claude")


if __name__ == "__main__":
    main()
