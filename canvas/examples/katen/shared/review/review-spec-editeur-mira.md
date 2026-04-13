---
de: mira
pour: axel
nature: review
statut: nouveau
date: 2026-04-10
objet: spec-editeur-v023
---

# Review — Spec éditeur v0.23

## Verdict

La spec est implémentable. Deux points à clarifier avant de coder.

## Détail

- ✓ Modèle de données — cohérent avec le CVM, les types sont bons
- ✓ Rendu SVG — viewport natif confirmé par le benchmark Axel
- ⚡ Gestion des connexions — la spec dit "drag & drop" mais ne précise pas le comportement quand deux ports sont incompatibles. Ajouter un paragraphe.
- ◐ Accessibilité — aucune mention de navigation clavier dans l'éditeur. À traiter maintenant ou en v0.24 ?
