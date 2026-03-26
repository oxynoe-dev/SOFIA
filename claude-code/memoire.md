# Mémoire persistante

> La mémoire est un complément aux fichiers, pas un remplacement.

---

## Ce que c'est

Claude Code offre un système de mémoire persistante (`MEMORY.md` +
fichiers mémoire) qui survit entre les conversations. Le persona
peut y stocker des informations utiles pour les sessions futures.

## Types de mémoire

| Type | Contenu | Exemple |
|------|---------|---------|
| **user** | Profil de l'utilisateur — rôle, préférences, connaissances | "Expert Go, nouveau sur React" |
| **feedback** | Corrections et validations de l'utilisateur | "Ne pas mocker la BDD dans les tests" |
| **project** | Contexte projet non dérivable du code | "Freeze des merges jeudi pour release mobile" |
| **reference** | Pointeurs vers des ressources externes | "Bugs trackés dans Linear projet INGEST" |

## Quoi stocker, quoi pas

### Stocker

- Ce que l'utilisateur préfère et pourquoi
- Les corrections reçues (pour ne pas refaire la même erreur)
- Le contexte projet qui n'est pas dans le code
- Les liens vers les ressources externes

### Ne PAS stocker

- Les patterns de code, conventions, architecture → lisibles dans le code
- L'historique git → `git log` est la source de vérité
- Les solutions de debug → le fix est dans le code
- Ce qui est dans le CLAUDE.md → déjà chargé à chaque session
- Les détails de la session en cours → c'est un résumé de session, pas une mémoire

## Structure

```
.claude/projects/{projet}/memory/
├── MEMORY.md                 ← index (pointeurs, pas contenu)
├── user_profile.md           ← profil utilisateur
├── feedback_testing.md       ← feedback sur les tests
├── project_deadline.md       ← contexte projet
└── reference_monitoring.md   ← lien vers dashboard
```

`MEMORY.md` est un index — il contient des liens vers les fichiers
mémoire, pas le contenu lui-même. Le garder court (< 200 lignes).

## Mémoire vs résumé de session

| | Mémoire | Résumé de session |
|---|---------|-------------------|
| **Durée de vie** | Mois | Jours |
| **Scope** | Cross-session | Une session |
| **Contenu** | Ce qui est vrai durablement | Ce qui s'est passé aujourd'hui |
| **Exemple** | "L'utilisateur préfère un seul PR pour les refactors" | "Créé ADR-058, review déposée, 3 points ouverts" |

Règle simple : si c'est utile dans 3 mois, c'est une mémoire.
Si c'est utile demain, c'est un résumé de session.
