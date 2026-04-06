# Contribuer a Voix

Voix est en **alpha**. Les contributions sont les bienvenues — retours terrain, corrections, propositions de patterns.

Avant de contribuer, lire le guide utilisateur : [`doc/utilisateur.md`](doc/utilisateur.md).

## Comment contribuer

1. **Ouvrir une issue d'abord** — bug, question, proposition de feature. Cela permet de discuter avant de coder.
2. **Si pertinent, proposer une PR** — une issue validee peut deboucher sur une pull request.
3. **Les retours d'experience comptent** — un rapport de friction, un pattern qui marche, une limite rencontree : tout est utile.

## Structure du repo

| Dossier | Role | Stabilite |
|---------|------|-----------|
| `core/` | Invariants (principes, personas, friction, devoirs) | Stable — modifications rares et deliberees |
| `protocol/` | Contrat d'interface (artefacts, conventions, tracabilite, isolation, orchestration) | Semi-stable — evolue avec les retours |
| `runtime/` | Implementation concrete (Claude Code aujourd'hui, autres demain) | Volatile — adapte aux outils |
| `doc/` | Guides, workflows, patterns, feedback, architecture, ADR | Ouvert aux contributions |

## Conventions

- **Langue source** : francais. Les documents techniques peuvent contenir des termes anglais quand ils sont etablis (runtime, pattern, workflow).
- **Nommage fichiers** : kebab-case, pas d'accents dans les noms de fichiers. Ex : `guide-installation.md`.
- **Format** : Markdown. Pas de HTML inline sauf necessite.

## Branches

- `main` — branche protegee, pas de push direct.
- `feature/{sujet}` — nouvelle fonctionnalite ou contenu.
- `fix/{sujet}` — correction.

Toute contribution passe par une PR contre `main`.

## Commits

Messages en francais, format :

```
{type}: {description courte}
```

Types :
- `feat` — nouveau contenu ou fonctionnalite
- `fix` — correction
- `doc` — documentation, guides, exemples
- `refactor` — reorganisation sans changement de sens

Exemples :
```
feat: ajout pattern delegation inter-personas
fix: correction lien casse dans guide utilisateur
doc: clarification du protocole d'isolation
refactor: deplacement des ADR dans doc/architecture/adr/
```

## Pull requests

- Une PR = un sujet. Garder les PR focalisees.
- Decrire le contexte et la motivation dans la description.
- Review requise avant merge.
- Si la PR touche `core/` ou `protocol/`, expliquer pourquoi l'invariant ou le contrat doit evoluer.

## Code de conduite

- **Bienveillance** — on construit ensemble, on apprend ensemble.
- **Clarte** — pas de jargon inutile. Si un terme n'est pas evident, l'expliquer.
- **Honnetete** — dire ce qui ne marche pas est aussi utile que dire ce qui marche.
- **Respect du perimetre** — Voix est une methode, pas un produit logiciel. Les contributions restent dans ce cadre.

## Licence

Voix est sous licence [MIT](LICENSE). Toute contribution est soumise a la meme licence.
