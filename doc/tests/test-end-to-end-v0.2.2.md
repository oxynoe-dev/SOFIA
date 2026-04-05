# Test end-to-end — v0.2.2

> Scénario : un dev solo découvre Voix et monte une instance pour son projet.

## Contexte fictif

**Projet** : Luma — app mobile de suivi de plantes
**Profil** : dev solo, 3 mois d'expérience Claude Code, React Native + Supabase
**Situation** : MVP qui marche mais code qui dérive, pas de doc, pas de vision claire

## Pré-requis

- Claude Code installé
- Accès GitHub
- Aucune connaissance préalable de Voix

## Étapes

### Phase 1 — Découverte

| # | Étape | Vérification | Pass |
|---|-------|-------------|------|
| 1 | `git clone` voix dans `/tmp/luma-voix-test` | Le repo se clone proprement | |
| 2 | Ouvrir Claude Code dans le repo | Le CLAUDE.md se charge, le guide se présente | |
| 3 | Dire : "Je construis une app mobile de suivi de plantes, solo dev, React Native + Supabase, j'ai un MVP mais le code part dans tous les sens" | Le guide pose des questions, ne plaque pas un modèle | |

### Phase 2 — Design des personas

| # | Étape | Vérification | Pass |
|---|-------|-------------|------|
| 4 | Le guide propose des rôles (pas des noms) | Max 3 au démarrage, pertinents pour un solo dev | |
| 5 | Calibrer 2 personas (ex: dev + architecte) | Le guide utilise les archétypes `persona-dev.md` et `persona-architecte.md` comme base | |
| 6 | Le guide génère les fiches personas | Format conforme au template `persona.md` | |
| 7 | Le guide génère les CLAUDE.md des workspaces | Format conforme au template `workspace/CLAUDE.md`, isolation correcte | |

### Phase 3 — Structure instance

| # | Étape | Vérification | Pass |
|---|-------|-------------|------|
| 8 | Le guide génère la structure instance | `shared/`, `sessions/`, `backlog.md`, `voix.md` présent | |
| 9 | Le guide vérifie la friction | Questions sur contradictions possibles, arbitrage humain | |
| 10 | Créer `/tmp/luma-instance`, y copier la structure | Fichiers cohérents, chemins corrects | |

### Phase 4 — Session complète

| # | Étape | Vérification | Pass |
|---|-------|-------------|------|
| 11 | Ouvrir Claude Code dans un workspace de l'instance | Le persona se charge, workflow d'ouverture fonctionne | |
| 12 | Mini-tâche + résumé + fermeture | Protocole session tourne end-to-end | |
| 13 | Déposer une note dans `shared/notes/` | Frontmatter correct, nommage correct | |
| 14 | Ouvrir l'autre persona | Le scan d'ouverture détecte la note | |

## Critères de succès

- Le guide ne propose jamais plus de 3 personas au démarrage
- Les templates générés sont utilisables sans modification manuelle
- Le protocole de session (ouverture → travail → fermeture → résumé) tourne sans friction
- La communication inter-personas via `shared/` fonctionne
- Un utilisateur sans connaissance de Voix peut suivre le parcours en < 1h

## Frictions à documenter

Tout ce qui bloque, surprend, ou nécessite une intervention manuelle non prévue.
Les noter ici au fur et à mesure du test :

- [ ] ...
