# Résumés de session

> La prochaine session n'aura pas ton contexte. Le résumé est sa seule mémoire.

---

## Pourquoi c'est obligatoire

Claude Code compresse les messages anciens quand la conversation
s'allonge. Le contexte du début de session disparaît. Et entre deux
conversations, tout est perdu sauf la mémoire persistante.

Le résumé de session est le **pont** entre les conversations.
C'est le premier fichier que le persona lit en ouvrant une session.

## Format

**Nom** : `{YYYY-MM-DD}-{HHmm}-{persona}.md`

**Contenu** :

```markdown
# Session {YYYY-MM-DD} ~{HH}h{mm} — {Persona}

## Produit
- `chemin/fichier.md` — créé : description courte
- `chemin/autre.md` — modifié : ce qui a changé

## Décisions
- **{Sujet}** — ce qui a été tranché

## Notes déposées
- `shared/review/review-xyz-persona.md`
- `shared/notes/note-dest-sujet-persona.md`

## Ouvert
Points en suspens, a reprendre en prochaine session.
```

## Règles

- **Toujours** — même si la session est courte, même si "rien de structurant"
- **Pas de prose** — listes courtes, 30 lignes max
- **Chemins relatifs** — pour que ce soit lisible hors contexte
- **Un résumé par session** — pas de résumé cumulatif

## Workflow

### Ouverture

1. Lire le dernier résumé dans `sessions/`
2. Le PO decide quoi regarder. Pas de recitation systematique.

### Fermeture

1. Produire le résumé dans `sessions/`
2. **Instance** (`experiments/` ou equivalent) : commit auto
   - Format : `{persona}: {résumé court} ({date})`
   - Scope : uniquement les fichiers modifiés/créés dans la session
3. **Repos produit** (code, methode, etc.) : preparer le message de commit, le PO execute

Le persona n'a pas besoin qu'on lui rappelle — c'est dans son
CLAUDE.md. Si tu constates qu'il oublie, renforce l'instruction.

## Statuts

Les roadmaps utilisent 5 statuts normalisés :

| Statut | Signification |
|--------|--------------|
| `[done]` | Terminé |
| `[running]` | En cours |
| `[ready]` | Prêt à démarrer |
| `[todo]` | À faire |
| `[blocked]` | Bloqué — raison après `⊘` |

Exemple : `- [blocked] Naming 3e mode ⊘ décision PO — 3 options ouvertes`

Le marqueur `↔` signale une convergence inter-voix (le sujet concerne plusieurs personas).
