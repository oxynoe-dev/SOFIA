## Publication

![Workflow — Publication](../figures/fig-workflow-publication.svg)

Workflow de publication : de la redaction a la mise en ligne.

---

### Quand l'utiliser

Pour tout contenu publie — page web, document public, livre blanc/bleu, communication externe. S'applique des qu'un contenu sort du perimetre interne.

### Etapes

1. **Redaction** — le redacteur ou l'expert produit le contenu brut. Le fond prime sur la forme a ce stade
2. **Validation fond** — les experts concernes valident chacun sur leur axe (technique, strategique, formel). Chaque axe produit une review
3. **Mise en forme** — le producteur (graphiste, integrateur) met en forme. La structure et le style suivent les conventions du support cible
4. **Challenge UX / accessibilite** — l'UX verifie la lisibilite, la navigation, l'accessibilite. Le contenu doit fonctionner pour le public cible
5. **Go PO** — derniere porte. Le PO verifie l'integrite factuelle : ce qui est publie est vrai, les sources sont correctes, le positionnement est juste
6. **Mise en ligne** — deploiement effectif. Le PO execute ou autorise

### Roles impliques

| Persona | Role |
|---------|------|
| Redacteur / Expert | Produit le contenu |
| Experts (archi, recherche, strategie) | Valident sur leur axe |
| Graphiste / Producteur | Mise en forme |
| UX | Challenge accessibilite et lisibilite |
| PO | Derniere porte — integrite factuelle, go/no-go |

### Artefacts produits

- Brouillon (dans le workspace du redacteur)
- Reviews par axe (dans `shared/review/`)
- Contenu mis en forme (dans le support cible)
- Validation PO (implicite : le go est le commit/deploiement)

### Pieges

- **Publier sans validation fond** — la mise en forme donne une illusion de qualite. Un document bien presente mais factuellement faux est pire qu'un brouillon correct
- **Le PO valide la forme, pas le fond** — le role du PO en derniere porte est specifiquement l'integrite factuelle. La forme a ete validee avant
- **Sources non verifiees** — une reference citee sans avoir ete lue en entier propage des erreurs dans tout ce qui la cite ensuite (cf. `recherche.md`)
