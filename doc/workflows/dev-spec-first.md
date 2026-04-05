## Dev Spec-First

![Workflow — Dev spec-first](../figures/fig-workflow-dev.svg)

Workflow de developpement : ne jamais coder sans cible validee.

---

### Quand l'utiliser

A chaque feature, correction ou refactoring qui touche le code produit. S'applique des qu'un item est priorise par le PO.

### Etapes

1. **PO priorise** — l'item existe dans la roadmap avec un owner explicite
2. **Archi specifie** — contrat d'interface, contraintes, ADR si decision structurelle (cf. `protocol/artefacts.md` pour les formats). La spec est le contrat : elle definit le quoi, pas le comment
3. **Dev planifie en mode plan** — decomposition feature par feature, chaque etape confrontee aux principes et aux ADR existants
4. **Tests d'abord (TDD)** — ecrire les tests avant le code, selon la couche : moteur/operateurs = TDD strict, CLI/IHM = tests apres implementation
5. **Code** — implementer en respectant les responsabilites modules et les conventions du projet
6. **Review archi** — l'architecte verifie la coherence avec la spec et les principes. Ecarts documentes, pas ignores
7. **Commit** — le dev prepare le message, le PO execute

### Roles impliques

| Persona | Role |
|---------|------|
| PO | Priorise, arbitre, commite |
| Architecte | Specifie le contrat, review post-implementation |
| Dev | Planifie, teste, code |

### Artefacts produits

- Spec ou contrat d'interface (dans le workspace archi)
- ADR si decision structurelle (cf. `decision-adr.md`)
- Tests unitaires / integration
- Code + commit

### Pieges

- **Coder avant la spec** — "je sais ce qu'il faut faire" mene a du refactoring evitable. La spec force a poser les contraintes avant de toucher au code
- **Confondre plan et spec** — un plan decompose des etapes, une spec definit un contrat. Le plan sans spec produit du code sans cible
- **Skipper la review archi** — la review n'est pas une formalite. Elle detecte les ecarts entre spec et implementation avant qu'ils ne se propagent
