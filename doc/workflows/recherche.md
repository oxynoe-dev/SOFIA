## Recherche

![Workflow — Recherche](../figures/fig-workflow-recherche.svg)

Workflow de recherche : de l'identification des sources a la verification de leur usage.

---

### Quand l'utiliser

A chaque fois qu'un document cite une source externe — article, paper, documentation, specification. S'applique aussi quand un persona affirme un fait qui necessite une reference.

### Etapes

1. **Identification des sources** — reperer les sources pertinentes pour le sujet. Privilegier les sources primaires (paper original, spec officielle) aux sources secondaires (articles de blog, tutoriels)
2. **Relecture complete de la source** — lire la source en entier, pas seulement l'abstract ou la section citee. Une source partiellement lue est une source mal comprise
3. **Contextualisation** — formuler explicitement pourquoi cette source est pertinente pour ce sujet. Quel est le lien entre ce que la source dit et ce qu'on veut montrer
4. **Verification contexte d'usage** — la question critique : la source dit-elle vraiment ce qu'on lui fait dire ? Verifier que le contexte original de la source correspond a l'usage qu'on en fait

### Roles impliques

| Persona | Role |
|---------|------|
| Recherche | Execute le workflow, produit les verifications |
| Expert du domaine (archi, dev, strategie) | Fournit le contexte d'usage — pourquoi cette source est citee |
| PO | Arbitre en cas de desaccord sur la pertinence |

### Artefacts produits

- Review de sources (dans `shared/review/`, format `review-sources-{sujet}-{auteur}.md`)
- Notes de contextualisation si necessaire
- Corrections dans les documents citants si une source est mal utilisee

### Pieges

- **Contamination factuelle** — une reference mal contextualisee propage une erreur dans tous les documents qui la citent. C'est l'erreur la plus couteuse : elle est invisible et se multiplie
- **Citer sans lire** — citer une source sur la base de son titre ou de son abstract. Le contenu reel peut contredire l'usage qu'on en fait
- **Confondre autorite et pertinence** — une source peut etre fiable (auteur reconnu, journal serieux) sans etre pertinente pour le contexte d'usage. La qualite de la review depend de la question posee, pas seulement de la source (cf. `core/artefacts.md`)
