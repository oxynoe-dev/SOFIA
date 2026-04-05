## Challenger

![Pattern — Challenger](../figures/fig-pattern-challenger.svg)

Un producteur avance, N challengers verifient chacun sur leur axe.

### Structure

Le pattern est asymetrique : un seul persona produit l'artefact, les autres le challengent sans le modifier. Chaque challenger a un droit de bloquant sur son axe uniquement — pas sur l'ensemble.

Le cout est lineaire (1 producteur + N challengers = N interactions), pas combinatoire (N personas qui discutent entre eux = N^2 interactions). C'est ce qui permet de scaler le nombre de challengers sans exploser la charge de coordination.

Le producteur integre les retours ou justifie pourquoi il ne le fait pas. Le PO arbitre en cas de desaccord.

### Quand le reconnaitre

- Un persona produit un livrable (code, spec, document) qui touche plusieurs axes de qualite.
- Il faut valider sans creer de comite ou de reunion.
- Les axes de verification sont independants les uns des autres.

### Exemple

Axel code une feature du moteur Katen. Mira challenge sur la coherence architecturale, Lea sur le formalisme (contrats, invariants), Nora sur l'ergonomie de l'API. Chacun produit un retour sur son axe. Axel integre.

### Variantes

- **Challenger unique** : un seul axe suffit (ex. Mira review un ADR d'Axel sur l'archi seule).
- **Challenger tournant** : le producteur change selon la nature du livrable, mais le mecanisme reste le meme.
- **Challenge croise** : deux personas se challengent mutuellement sur des livrables distincts (chacun est producteur de l'un, challenger de l'autre).

### Risques

- **Dilution** : trop de challengers ralentit le producteur sans gain proportionnel.
- **Bloquant abusif** : un challenger bloque sur un detail hors de son axe.
- **Passivite** : le challenger valide sans vraiment verifier — le pattern perd sa valeur.
