# Friction

> Qualifier les positions, pas les compter.

---

## Definition

La friction est une prise de position d'un participant (persona ou orchestrateur) sur une proposition de l'autre. Elle qualifie la nature d'un accord ou d'un desaccord.

La friction est un mecanisme productif, pas un defaut. Voir `core/modele.md` pour le pourquoi.

## Dimensions

| Dimension | Valeurs | Obligatoire |
|-----------|---------|-------------|
| **echange** | Reference a l'echange (session ou artefact) qui a genere la friction | DOIT |
| **emetteur** | Persona ou orchestrateur qui emet la position | DOIT |
| **marqueur** | `[juste]`, `[contestable]`, `[simplification]`, `[angle-mort]`, `[faux]` | DOIT |
| **description** | Resume court de la position | DOIT |
| **initiative** | `[persona]` ou `[PO]` — qui a initie le sujet de friction | DOIT |

**Portee** : une friction est rattachee a un echange, lui-meme rattache a un espace dans une instance.

## Marqueurs

5 positions epistemiques. Ce sont des positions, pas une echelle d'intensite. L'ensemble est ferme — une instance NE DOIT PAS ajouter de marqueurs.

| Marqueur | Signification |
|----------|--------------|
| `[juste]` | Corroboration — position correcte |
| `[contestable]` | Sous-determination — defendable mais pas la seule lecture |
| `[simplification]` | Reductionnisme — le reel est plus complexe |
| `[angle-mort]` | Incompletude — donnees manquantes |
| `[faux]` | Refutation — factuellement incorrect ou incoherent |

Les marqueurs DOIVENT etre exprimes en mots-cles entre crochets.

> **Note theorique.** Ces 5 positions sont compatibles (sans equivalence stricte) avec le modele d'argumentation de Toulmin (1958) : `[juste]` ≈ absence de rebuttal, `[contestable]` ≈ challenge du qualifier, `[simplification]` ≈ challenge du warrant, `[angle-mort]` ≈ challenge des data, `[faux]` ≈ refutation du claim. Ce rapprochement est un eclairage, pas une contrainte du protocole.

## Format

Chaque ligne de friction DOIT porter :
1. Le marqueur entre crochets
2. Une description courte
3. Un tag d'initiative : `[persona]` ou `[PO]`

> **Exemple** (implementation Markdown, voir `implementation/implementation.md`) :
>
> ```
> ## Friction
> - [contestable] le mapping Toulmin est suggestif, pas acquis — [PO]
> - [angle-mort] scaffolding absent de la review Böckeler — [aurele]
> ```

## Interpretation

| Signal | Lecture |
|--------|--------|
| Que des `[juste]` | Friction absente — signal d'alerte. Le persona est peut-etre en mode validation plutot qu'en mode collaboration. |
| Mix `[juste]` / `[contestable]` / `[simplification]` | Friction saine — positions diverses, collaboration productive. |
| Presence de `[angle-mort]` ou `[faux]` | Tension a traiter — l'orchestrateur DEVRAIT arbitrer explicitement. |

## Couche

La friction est **observationnelle**. Qualifier une position (resistance vs correction, angle-mort vs oubli) requiert un jugement semantique. Le persona pre-remplit, l'orchestrateur valide.

L'audit PEUT verifier la presence de la section et la conformite des marqueurs (computationnel), mais pas la justesse des qualifications (inferentiel).

## Rendu

Les marqueurs mots-cles sont le format du protocole.
