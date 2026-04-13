## Chaîne Produit

![Workflow — Chaîne produit](../../doc/figures/fig-workflow-chaine-produit.svg)

Chaîne complète de production : chaque étape a un gardien, aucun raccourci.

---

### Quand l'utiliser

Pour toute feature ou évolution qui traverse plusieurs domaines — de la priorisation à la livraison. C'est le workflow de référence quand plusieurs personas interviennent.

### Étapes

1. **L'orchestrateur priorise** — l'item entre dans la roadmap avec contexte et owner
2. **Archi spécifie** — contrats, contraintes, ADR si besoin. Gardien : cohérence avec l'architecture cible et les principes (cf. `core/principes.md`)
3. **Dev implémente** — mode plan, TDD, code. Gardien : conformité à la spec
4. **UX challenge** — l'UX vérifie l'expérience utilisateur, l'accessibilité, la cohérence visuelle. Gardien : le produit est utilisable, pas seulement fonctionnel
5. **Recherche vérifie** — vérification formelle, sources, rigueur. Gardien : ce qui est affirmé est vrai et correctement contextualisé
6. **L'orchestrateur arbitre** — dernière porte. Validation finale, go/no-go

### Rôles impliqués

| Persona | Rôle |
|---------|------|
| Orchestrateur | Priorise (étape 1), arbitre (étape 6) |
| Architecte | Spécifie, garde la cohérence structurelle |
| Dev | Implémente selon la spec |
| UX | Challenge l'expérience et l'accessibilité |
| Recherche | Vérifie formellement les affirmations |

### Artefacts produits

- Roadmap item priorisé
- Spec / contrat d'interface
- Code + tests
- Review UX (note dans `shared/review/`)
- Validation formelle si applicable
- Décision orchestrateur documentée

### Pièges

- **Sauter une étape** — chaque étape sautée génère de la dette. La dette la plus coûteuse est celle qu'on ne voit pas (cf. `protocol/tracabilite.md`)
- **Paralléliser sans contrat** — dev et UX en parallèle sans spec commune = deux visions divergentes à réconcilier après coup
- **Confondre validation orchestrateur et approbation automatique** — l'orchestrateur est la dernière porte, pas un tampon. Il peut renvoyer à n'importe quelle étape
