---
persona: {nom}
produit: {produit}
---

# Contexte {Nom} — {Produit} ({workspace})

<!-- Ce fichier contient tout ce qui est spécifique au couple persona×produit :
     périmètre, documents clés, isolation, conventions, workflow.
     Le rôle, la posture et les interdits vivent dans persona-{nom}.md.
     Voir protocol/conventions.md § "CLAUDE.md — anatomie" pour le détail. -->

## Périmètre

Ce workspace contient :
- {Type de contenu 1}
- {Type de contenu 2}

## Documents clés

### Dans ce workspace ({workspace}/)

| Fichier | Rôle |
|---------|------|
| `{chemin}` | {description} |

### Dans le repo produit ({produit}/)

| Chemin | Rôle |
|--------|------|
| `{chemin}` | {description} |

## Repos liés

| Repo | Rôle | Persona |
|------|------|---------|
| `{repo}` | {description} | {persona} |

## Isolation

<!-- LES FRONTIÈRES. Sans cette section, le persona va déborder. -->

- **Ne jamais lire/écrire en dehors de** `{périmètre autorisé}`
- {Autre interdit si nécessaire}

## Conventions

- **Langue** : {français / anglais}
- **{Type d'artefact}** : {format, convention de nommage}
- **Reviews** : format `review-<sujet>-{nom}.md`, déposer dans `shared/review/`
- **Bus shared/** : voir `shared/conventions.md`
- **Roadmaps** : chaque item porte un `@owner`. Tu es responsable des items marqués `@{nom}`.

## Workflow

0. **Ouverture de session** :
   - Lire le dernier résumé dans `sessions/`
   - Lire les roadmaps produit pertinentes dans `shared/`
   - Scanner `shared/notes/` et `shared/review/` — traiter les artefacts à son nom
   - Remonter les points ouverts à l'orchestrateur avant de commencer
1. **Lire** les documents existants avant toute intervention
2. **Produire** des {types de livrables}
3. **{Interdit principal}** — {ce que le persona ne fait pas}

## Émergence

Quand tu deflectes une question parce qu'elle sort de ton périmètre,
note le domaine. Si tu deflectes 3+ fois sur le même domaine,
signale-le explicitement :
"Je reçois régulièrement des questions sur [domaine] —
c'est en dehors de mon périmètre. Ce sujet relève d'un autre persona."

## Protocole de session — obligatoire

Résumé : `sessions/{YYYY-MM-DD}-{HHmm}-{nom}.md` — `## Produit`, `## Décisions`, `## Notes déposées`, `## Friction orchestrateur`, `## Ouvert`. Pas de prose, 30 lignes max.

`## Friction orchestrateur` : échanges marquants avec l'orchestrateur, qualifiés avec ✓/~/⚡/◐/✗ (ref: `core/friction.md`). Si session purement logistique, section vide ou absente.

Fermeture : résumé → commit direct `{nom}: {résumé court} ({date})` → repos produit : préparer le message, l'orchestrateur exécute.
