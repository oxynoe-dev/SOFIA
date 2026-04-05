## Distillerie

![Pattern — Distillerie](../figures/fig-pattern-distillerie.svg)

Les observations terrain remontent dans la methode. Les retours d'experience deviennent des patterns documentes.

### Structure

Le cycle a trois temps :

1. **Observation** : un apprentissage, une friction ou un REX est documente dans `feedback/` ou dans un resume de session. C'est du materiau brut, lie a un contexte specifique.
2. **Extraction** : le PO ou un persona identifie ce qui est universel dans l'observation — ce qui se repeterait dans un autre contexte.
3. **Integration** : le pattern extrait est formalise et integre dans `core/` ou `doc/`. Il devient une piece de la methode, decouple de son contexte d'origine.

La distillerie est ce qui differencie une collection de notes d'une methode vivante. Sans ce mecanisme, les apprentissages restent eparpilles et non reutilisables.

### Quand le reconnaitre

- Une observation dans `feedback/` est citee plusieurs fois dans des contextes differents.
- Un probleme deja rencontre reapparait — signe qu'il n'a pas ete capitalise.
- Une decision prise intuitivement merite d'etre explicitee comme principe.

### Exemple

L'observation que les personas doivent etre definis par leur media de production (documentee dans `feedback/calibrage-personas.md`) a ete extraite et formalisee comme pattern `calibrage-media.md`. Le feedback original reste dans `feedback/` comme trace ; le pattern vit dans `doc/patterns/`.

### Variantes

- **Distillerie inverse** : un pattern existant est invalide par le terrain. Le feedback documente la deviation, le pattern est amende ou retire.
- **Distillerie croisee** : une observation d'un domaine (ex. architecture) produit un pattern applicable dans un autre (ex. methode d'equipe).

### Risques

- **Sur-generalisation** : transformer une observation ponctuelle en pattern universel trop vite.
- **Fossilisation** : un pattern documente n'est jamais remis en question meme quand le terrain evolue.
- **Accumulation sans extraction** : les feedbacks s'empilent mais personne ne les distille.
