## Contamination factuelle (anti-pattern)

![Anti-pattern — Contamination factuelle](../figures/fig-pattern-contamination-factuelle.svg)

Un LLM privilegie la coherence interne sur la verite externe. Une erreur entree une fois se propage partout.

### Mecanisme

1. Une approximation factuelle entre dans le corpus — par hallucination du LLM ou par erreur humaine.
2. Le LLM utilise cette information comme reference pour les documents suivants. Il ne la verifie pas : elle est coherente avec le contexte existant.
3. Plus le nombre de documents contenant l'erreur augmente, plus elle devient invisible. Elle fait partie du "consensus" interne du corpus.
4. La correction tardive est couteuse : il faut identifier tous les documents contamines, verifier chaque occurrence, et corriger sans introduire de nouvelles incoherences.

Le probleme fondamental : le LLM optimise pour la coherence interne, pas pour la verite. Un fait faux mais coherent ne declenche aucun signal d'alerte.

### Signaux d'alerte

- Un chiffre, une date ou une duree est cite dans plusieurs documents sans source primaire identifiable.
- Un fait "semble vrai" mais personne ne se souvient de l'avoir verifie.
- Lors d'une relecture, un detail factuel surprend legerement mais est accepte parce qu'il apparait deja ailleurs.

### Exemple

Dans le projet Katen, la duree "15 ans d'experience" a ete utilisee au lieu de "18 ans". L'erreur s'est propagee dans environ 30 documents produits par differents personas. Detectee tardivement, la correction a necessite un audit systematique de tous les documents contenant cette reference.

### Prevention

- **Verification continue** : a chaque session, verifier les faits cles (dates, durees, chiffres, noms propres) contre les sources primaires. Ne pas repousser a la fin du projet.
- **Sources explicites** : quand un fait est cite, indiquer d'ou il vient. Un fait sans source est un candidat a la contamination.
- **Audit factuel periodique** : dedicacer des sessions a la verification factuelle pure, independamment de la production.
- **Droit de doute** : tout persona qui lit un fait et hesite doit le signaler, meme si le fait apparait dans 10 autres documents.

### Risques (si non traite)

- **Perte de credibilite** : un document publie contenant des erreurs factuelles disqualifie l'ensemble.
- **Cout de correction exponentiel** : plus on attend, plus la decontamination est lourde.
- **Faux sentiment de fiabilite** : la coherence interne donne l'illusion que tout est correct.
