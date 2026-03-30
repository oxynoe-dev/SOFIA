# Test end-to-end — v0.2.2

> Scenario : un dev solo decouvre Voix et monte une instance pour son projet.

## Contexte fictif

**Projet** : Luma — app mobile de suivi de plantes
**Profil** : dev solo, 3 mois d'experience Claude Code, React Native + Supabase
**Situation** : MVP qui marche mais code qui derive, pas de doc, pas de vision claire

## Pre-requis

- Claude Code installe
- Acces GitHub
- Aucune connaissance prealable de Voix

## Etapes

### Phase 1 — Decouverte

| # | Etape | Verification | Pass |
|---|-------|-------------|------|
| 1 | `git clone` voix dans `/tmp/luma-voix-test` | Le repo se clone proprement | |
| 2 | Ouvrir Claude Code dans le repo | Le CLAUDE.md se charge, le guide se presente | |
| 3 | Dire : "Je construis une app mobile de suivi de plantes, solo dev, React Native + Supabase, j'ai un MVP mais le code part dans tous les sens" | Le guide pose des questions, ne plaque pas un modele | |

### Phase 2 — Design des personas

| # | Etape | Verification | Pass |
|---|-------|-------------|------|
| 4 | Le guide propose des roles (pas des noms) | Max 3 au demarrage, pertinents pour un solo dev | |
| 5 | Calibrer 2 personas (ex: dev + architecte) | Le guide utilise les archetypes `persona-dev.md` et `persona-architecte.md` comme base | |
| 6 | Le guide genere les fiches personas | Format conforme au template `persona.md` | |
| 7 | Le guide genere les CLAUDE.md des workspaces | Format conforme au template `workspace/CLAUDE.md`, isolation correcte | |

### Phase 3 — Structure instance

| # | Etape | Verification | Pass |
|---|-------|-------------|------|
| 8 | Le guide genere la structure instance | `shared/`, `sessions/`, `backlog.md`, `voix.md` present | |
| 9 | Le guide verifie la friction | Questions sur contradictions possibles, arbitrage humain | |
| 10 | Creer `/tmp/luma-instance`, y copier la structure | Fichiers coherents, chemins corrects | |

### Phase 4 — Session complete

| # | Etape | Verification | Pass |
|---|-------|-------------|------|
| 11 | Ouvrir Claude Code dans un workspace de l'instance | Le persona se charge, workflow d'ouverture fonctionne | |
| 12 | Mini-tache + resume + fermeture | Protocole session tourne end-to-end | |
| 13 | Deposer une note dans `shared/notes/` | Frontmatter correct, nommage correct | |
| 14 | Ouvrir l'autre persona | Le scan d'ouverture detecte la note | |

## Criteres de succes

- Le guide ne propose jamais plus de 3 personas au demarrage
- Les templates generes sont utilisables sans modification manuelle
- Le protocole de session (ouverture → travail → fermeture → resume) tourne sans friction
- La communication inter-personas via `shared/` fonctionne
- Un utilisateur sans connaissance de Voix peut suivre le parcours en < 1h

## Frictions a documenter

Tout ce qui bloque, surprend, ou necessite une intervention manuelle non prevue.
Les noter ici au fur et a mesure du test :

- [ ] ...
