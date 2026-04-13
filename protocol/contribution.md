# Contribution

> Qui a amene quoi.

---

## Definition

La contribution capture la direction et la nature des apports pendant une session : qui a nourri quoi. C'est le flux epistemique de l'echange synchrone humain-assistant.

## Dimensions

| Dimension | Valeurs | Obligatoire |
|-----------|---------|-------------|
| **session** | Reference a la session qui a genere la contribution | DOIT |
| **direction** | `[H]` (humain apporte) ou `[A]` (assistant apporte) | DOIT |
| **type** | `matiere`, `structure`, `challenge`, `decision` | DOIT |
| **description** | Resume court de l'apport | DOIT |

**Portee** : une contribution est rattachee a une session, elle-meme rattachee a un espace dans une instance. Les messages ne generent pas de contributions (voir `exchange.md`).

## Couche

La contribution est entierement **observationnelle**. La distinction entre types d'apport (matiere vs structure vs challenge) est semantique et non-deterministe. La section `## Flux` est optionnelle (PEUT).

## Tags de direction

| Tag | Signification |
|-----|---------------|
| `[H]` | L'humain apporte |
| `[A]` | L'assistant apporte |

## Types d'apport

| Type | Definition |
|------|-----------|
| `matiere` | Information nouvelle — fait, donnee, reference, insight |
| `structure` | Mise en forme, categorisation, synthese |
| `challenge` | Remise en question, contre-exemple, recadrage |
| `decision` | Arbitrage, choix retenu |

## Format

Chaque ligne de contribution porte : tag de direction, type, description courte.

Le comptage par direction et type est optionnel (PEUT).

> **Exemple** (implementation Markdown, voir `implementation.md`) :
>
> ```
> ## Flux
> - H:matiere — article Böckeler, demande d'avis
> - A:matiere — filiation scaffolding absente chez Böckeler
> - A:structure — trois niveaux de complementarite harness/SOFIA
> - H:decision — on garde la notation mots-cles
>
> H:2 (matiere 1, decision 1) | A:2 (matiere 1, structure 1)
> ```

## Distinction contribution / friction

Un meme echange PEUT apparaitre dans `## Flux` et dans `## Friction` :

- **Contribution** capture l'apport (qui a amene quoi)
- **Friction** capture la tension (positions qui s'opposent, resistance)

Critere : une correction acceptee sans resistance = `H:challenge` dans le flux, pas de friction. Si l'assistant resiste ou si la resolution demande plusieurs echanges, c'est aussi une friction.

## Lecture

| Pattern | Interpretation |
|---------|---------------|
| H >> A sur matiere | L'assistant structure/scaffolde, l'humain apporte le fond |
| A >> H sur matiere | L'humain pilote, l'assistant apporte le fond |
| H ≈ A | Co-construction equilibree |

Ce n'est pas un jugement de valeur — c'est un signal sur le mode de collaboration actif.
