## Registre de livrables

Chaque produit a des **livrables de référence** — les documents qui font autorité. Un livrable a un responsable (persona) et un cycle de vie.

### Structure

Chaque roadmap produit contient une section `## Livrables de référence` qui liste les documents source de vérité :

```markdown
## Livrables de référence

| Livrable | Chemin | Responsable | Statut |
|----------|--------|-------------|--------|
| Architecture cible | `doc/reference/target-architecture.md` | @mira | actif |
| Spec CVM | `doc/reference/spec-cvm.md` | @mira | actif |
| Livre bleu | `maturation/livre-bleu-sofia.md` | @winston | actif |
```

### Règles

- **Un livrable = un responsable.** Pas de copropriété — un persona porte le document, les autres challengent via review.
- **L'orchestrateur définit les livrables avec le persona responsable.** C'est une décision conjointe.
- **Le statut suit le cycle de vie** : `draft` → `actif` → `obsolete` → `archive`.
- **Le registre est dans la roadmap**, pas dans un fichier séparé — il vit avec le produit qu'il documente.

### Quand l'utiliser

Quand l'instance a suffisamment de documents pour que la question "quel est le document de référence pour X ?" n'ait pas de réponse évidente. Le registre rend explicite ce qui était implicite.

### Risques

- **Registre fantôme** : un registre qui n'est pas maintenu est pire que pas de registre — il donne un faux sentiment de contrôle. Le responsable du livrable maintient l'entrée.
- **Prolifération** : ne lister que les documents source de vérité, pas tous les documents. Si tout est "livrable de référence", rien ne l'est.
