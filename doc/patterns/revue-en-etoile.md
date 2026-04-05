## Revue en etoile

![Pattern — Revue en etoile](../figures/fig-pattern-revue-etoile.svg)

Un artefact est soumis a N personas en parallele, chacun le review sur son axe. Le PO consolide.

### Structure

1. Le PO identifie un artefact qui necessite une validation multi-angle.
2. Il le soumet simultanement a N personas, chacun avec une consigne de review sur son axe propre.
3. Les personas produisent leurs reviews en parallele, sans se lire mutuellement.
4. Le PO collecte les reviews, identifie les convergences et les contradictions, et consolide une decision.

La difference avec le pattern challenger : le challenger s'insere dans un flux de production sequentiel (le producteur integre les retours). La revue en etoile est un mecanisme ponctuel de validation — les reviewers ne modifient pas l'artefact, le PO tranche.

### Quand le reconnaitre

- Un document structurant (ADR, spec, plan) doit etre valide avant adoption.
- Plusieurs axes de qualite sont en jeu et aucun persona ne les couvre tous.
- On veut des regards independants, pas contamines par les avis des autres.

### Exemple

Le PO soumet un ADR a Mira (coherence avec l'architecture cible), Lea (rigueur formelle, references), et Marc (alignement strategique). Chacun produit une review independante dans `shared/review/`. Le PO lit les trois, identifie un point de tension entre coherence archi et strategie, et tranche.

### Variantes

- **Etoile partielle** : seuls 2 axes sur N sont sollicites, selon la nature de l'artefact.
- **Etoile iterative** : apres consolidation, l'artefact est amende et resoumis pour un second tour.

### Risques

- **Redondance** : les reviewers couvrent involontairement le meme terrain — perte de temps.
- **Paralysie** : les reviews divergent et le PO n'arrive pas a trancher.
- **Faux parallele** : les reviews sont lancees "en parallele" mais en realite sequentielles (un persona lit la review d'un autre avant de produire la sienne).
