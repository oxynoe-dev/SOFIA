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
- **{Sujet}** — ce qui reste à traiter
```

## Règles

- **Toujours** — même si la session est courte, même si "rien de structurant"
- **Pas de prose** — listes courtes, 30 lignes max
- **Chemins relatifs** — pour que ce soit lisible hors contexte
- **Section Ouvert** — c'est la todo list de la prochaine session
- **Un résumé par session** — pas de résumé cumulatif

## Workflow

### Ouverture

1. Lire le dernier résumé dans `sessions/`
2. Remonter les points ouverts au PO
3. Commencer le travail

### Fermeture

1. Produire le résumé
2. Vérifier que les notes sont déposées dans shared/
3. Terminé

Le persona n'a pas besoin qu'on lui rappelle — c'est dans son
CLAUDE.md. Si tu constates qu'il oublie, renforce l'instruction.
