# Traçabilité

> Si ce n'est pas tracé, ça n'existe pas.

---

## Pourquoi tracer ?

Les conversations avec Claude Code sont éphémères. Le contexte se
compresse, les sessions se ferment, la mémoire a ses limites.

La seule chose qui persiste de manière fiable, ce sont les **fichiers**.

La traçabilité dans SOFIA repose sur trois mécanismes :

## 1. Résumés de session

**Chaque session produit un résumé.** Sans exception.

Format : `sessions/{YYYY-MM-DD}-{HHmm}-{persona}.md`

Contenu obligatoire :
- **Produit** — fichiers créés ou modifiés, avec chemin
- **Décisions** — ce qui a été tranché
- **Notes déposées** — fichiers dans shared/
- **Ouvert** — ce qui reste à traiter

Pas de prose. Des listes courtes. 30 lignes max.

**Pourquoi c'est vital** : la prochaine session commence par lire
le dernier résumé. C'est sa seule mémoire fiable de ce qui s'est
passé avant.

## 2. ADR (Architecture Decision Records)

Les décisions structurantes sont tracées dans des ADR.

Format standard :
- **Contexte** — pourquoi la question se pose
- **Décision** — ce qu'on a choisi
- **Alternatives** — ce qu'on a envisagé et rejeté
- **Conséquences** — ce que ça implique
- **Statut** — Proposed → Accepted → Superseded

Un ADR n'est pas un document lourd. C'est une trace de **pourquoi**
on a décidé ça, à ce moment-là, avec ce contexte.

L'ADR est écrit **avant** l'implémentation, pas après.

## 3. Reviews croisées

Quand un persona intervient sur le travail d'un autre, il produit
une review :

Format : `shared/review/review-{sujet}-{auteur}.md`

Une review contient :
- Des observations factuelles (pas des opinions)
- Des recommandations priorisées
- Des questions ouvertes pour l'orchestrateur

La review est un artefact, pas un commentaire. Elle est versionnée,
relisable, et sert de base à la discussion.

## La mémoire persistante (MEMORY.md)

Claude Code offre un système de mémoire persistante entre les
conversations. C'est un complément aux fichiers, pas un remplacement.

Voir `runtime/claude-code/memoire.md` pour les détails.

Règle simple : si c'est utile uniquement pour la prochaine conversation,
c'est un résumé de session. Si c'est utile dans 3 mois, c'est une mémoire.
