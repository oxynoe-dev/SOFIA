## Distillerie

![Pattern — Distillerie](../../doc/figures/fig-pattern-distillerie.svg)

Les observations terrain remontent dans la méthode. Les retours d'expérience deviennent des patterns documentés.

### Structure

Le cycle a trois temps :

1. **Observation** : un apprentissage, une friction ou un REX est documenté dans `feedback/` ou dans un résumé de session. C'est du matériau brut, lié à un contexte spécifique.
2. **Extraction** : l'orchestrateur ou un persona identifie ce qui est universel dans l'observation — ce qui se répéterait dans un autre contexte.
3. **Intégration** : le pattern extrait est formalisé et intégré dans `core/` ou `doc/`. Il devient une pièce de la méthode, découplé de son contexte d'origine.

La distillerie est ce qui différencie une collection de notes d'une méthode vivante. Sans ce mécanisme, les apprentissages restent éparpillés et non réutilisables.

### Quand le reconnaître

- Une observation dans `feedback/` est citée plusieurs fois dans des contextes différents.
- Un problème déjà rencontré réapparaît — signe qu'il n'a pas été capitalisé.
- Une décision prise intuitivement mérite d'être explicitée comme principe.

### Exemple

L'observation que les personas doivent être définis par leur média de production (documentée dans `feedback/calibrage-personas.md`) a été extraite et formalisée comme pattern `calibrage-media.md`. Le feedback original reste dans `feedback/` comme trace ; le pattern vit dans `doc/patterns/`.

### Variantes

- **Distillerie inverse** : un pattern existant est invalidé par le terrain. Le feedback documente la déviation, le pattern est amendé ou retiré.
- **Distillerie croisée** : une observation d'un domaine (ex. architecture) produit un pattern applicable dans un autre (ex. méthode d'équipe).

### Risques

- **Sur-généralisation** : transformer une observation ponctuelle en pattern universel trop vite.
- **Fossilisation** : un pattern documenté n'est jamais remis en question même quand le terrain évolue.
- **Accumulation sans extraction** : les feedbacks s'empilent mais personne ne les distille.
