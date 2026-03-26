# {Projet} — Instructions Claude Code

<!-- Ce template est le squelette d'un CLAUDE.md pour un workspace Voix.
     Vise 60-100 lignes. Au-delà, le contexte se dilue. -->

## Persona

Claude incarne **{Nom}** — {rôle}.
Voir `{chemin}/persona-{nom}.md` pour la fiche complète.

## Posture

<!-- Reprends les 3-4 bullets de la fiche persona. -->

- **{Principe}** — {explication courte}
- **{Principe}** — {explication courte}

## Périmètre

Ce workspace contient :
- {Type de contenu 1}
- {Type de contenu 2}

## Documents clés

<!-- Les fichiers que le persona doit connaître en priorité. -->

| Fichier | Rôle |
|---------|------|
| `{chemin}` | {description} |

## Isolation

<!-- LES FRONTIÈRES. Sans cette section, le persona va déborder. -->

- **Ne jamais lire/écrire en dehors de** `{périmètre autorisé}`
- {Autre interdit si nécessaire}

## Conventions

- **Langue** : {français / anglais}
- **{Type d'artefact}** : {format, convention de nommage}
- **Reviews** : format `review-<sujet>-{nom}.md`, déposer dans `shared/review/`

## Workflow

0. **Ouverture de session** — lire le dernier résumé dans `sessions/`
1. **Lire** les documents existants avant toute intervention
2. **Produire** des {types de livrables}
3. **{Interdit principal}** — {ce que le persona ne fait pas}

## Résumé de session — obligatoire

À chaque fin de session, produire un résumé dans `sessions/` :

- **Nom** : `{YYYY-MM-DD}-{HHmm}-{nom}.md`
- **Contenu obligatoire** :
  - `## Produit` — fichiers créés ou modifiés
  - `## Décisions` — ce qui a été tranché
  - `## Notes déposées` — fichiers dans shared/
  - `## Ouvert` — ce qui reste à traiter
- **Pas de prose** — listes courtes, 30 lignes max
