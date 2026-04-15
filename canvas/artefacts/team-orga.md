---
implementation: filesystem
---

# Organisation de l'équipe {Projet}

**Projet** : {Projet}
**Date** : {date}
**Auteur** : {persona architecte ou orchestrateur}

---

## L'équipe

<!-- Liste complète : l'orchestrateur + tous les personas actifs.
     Mettre à jour à chaque ajout/suppression de persona. -->

| Persona | Rôle | Statut |
|---------|------|--------|
| **{Nom orchestrateur}** | Orchestrateur | Humain — décideur |
| **{Persona 1}** | {Rôle} | Assistant IA spécialisé |
| **{Persona 2}** | {Rôle} | Assistant IA spécialisé |

---

## Flux de collaboration

<!-- Les flux principaux entre personas. Adapter selon l'équipe.
     Nommer les flux, décrire la direction, indiquer qui déclenche quoi.
     Les flux typiques : décisionnel, technique, scientifique, éditorial. -->

### Flux décisionnel
Le Product Owner initie et valide. {Persona archi} traduit en architecture,
{persona stratège} en stratégie. Les décisions remontent à l'orchestrateur.

### Flux technique
{Persona archi} spécifie les contrats → {persona dev} implémente et remonte
les frictions → {persona UX} spécifie les comportements UI.

### Flux éditorial
<!-- Si l'équipe a un rédacteur et une chaîne de publication.
     Préciser : qui rédige, qui valide le fond, qui produit la forme,
     qui challenge avant publication, qui déclenche les scripts. -->

{Persona rédacteur} rédige le contenu. Les experts valident le fond.
{Persona prod} produit la forme. {Persona UX} challenge avant publication.
L'orchestrateur valide avant toute sortie.

---

## Règles de fonctionnement

<!-- Les invariants de l'équipe. Adapter, mais ces trois règles
     sont non négociables dans SOFIA : -->

- **L'orchestrateur est le seul décideur final** — les personas proposent, analysent, challengent. L'orchestrateur tranche.
- **Les frictions remontent** — tout blocage ou incohérence entre personas est signalé explicitement, pas contourné.
- **Rien ne sort sans validation orchestrateur** — l'orchestrateur relit avant toute publication.

<!-- Ajouter les règles spécifiques au projet : -->

---

## Périmètres — matrice RACI simplifiée

<!-- Adapter les lignes aux décisions clés du projet.
     R = Responsable · A = Approbateur · C = Consulté
     L'orchestrateur est toujours Approbateur. -->

| Décision | Orchestrateur | {P1} | {P2} | {P3} |
|---|---|---|---|---|
| {Décision 1} | A | R | C | — |
| {Décision 2} | A | C | R | — |
| {Décision 3} | A | — | C | R |
| Publication (tous canaux) | A | C | C | C |

*R = Responsable · A = Approbateur · C = Consulté*

---

## Droits de challenge

<!-- Chaque persona a un droit de regard explicite sur certains livrables
     des autres. La friction ne repose pas sur la bonne volonté — elle est
     structurelle. Remplir pour chaque persona actif. -->

| Persona | Challenge |
|---------|-----------|
| **{Persona 1}** | {sur quoi il/elle a un droit de regard} |
| **{Persona 2}** | {sur quoi il/elle a un droit de regard} |
| **{Persona 3}** | {sur quoi il/elle a un droit de regard} |

---

*{Projet} — {date}*
