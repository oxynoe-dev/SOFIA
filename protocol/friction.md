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
| **resolution** | `ratifie`, `conteste`, `revise`, `rejete` — geste epistemique de resolution | DEVRAIT |

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

## Resolution

4 gestes epistemiques. Chaque friction DEVRAIT porter un tag de resolution qui qualifie ce qui s'est passe apres la qualification — pas le contenu, mais le denouement.

| Tag | Signification |
|-----|---------------|
| `ratifie` | Accord — la position est acceptee par l'autre partie |
| `conteste` | Desaccord maintenu — pas de changement de position |
| `revise` | Desaccord avec changement de position de l'une des parties |
| `rejete` | Desaccord terminal — la position est ecartee |

L'ensemble est ferme — une instance NE DOIT PAS ajouter de tags de resolution.

Le tag de resolution est pose par le redacteur du resume (persona pour les sessions, emetteur pour les artefacts). Il reflete la perception du redacteur sur le denouement, pas un verdict objectif. L'orchestrateur PEUT corriger.

> **Note theorique.** Ces 4 gestes sont inspires du protocole PXP (Mestha et al. 2025 — RATIFY, REFUTE, REVISE, REJECT). PXP qualifie les gestes dans un echange multi-tour humain-LLM. H2A les applique a la resolution des frictions, pas aux messages individuels. Ce rapprochement est un eclairage, pas une contrainte du protocole.

## Format

Chaque ligne de friction DOIT porter :
1. Le marqueur entre crochets
2. Une description courte
3. Un tag d'initiative : `[persona]` ou `[PO]`
4. Un tag de resolution (DEVRAIT) : `→ ratifie`, `→ conteste`, `→ revise`, `→ rejete`

> **Exemple** (implementation Markdown, voir `implementation/implementation.md`) :
>
> ```
> ## Friction
> - [contestable] le mapping Toulmin est suggestif, pas acquis — [PO] → revise
> - [angle-mort] scaffolding absent de la review Böckeler — [aurele] → ratifie
> ```

## Interpretation

| Signal | Lecture |
|--------|--------|
| Que des `[juste]` | Friction absente — signal d'alerte. Le persona est peut-etre en mode validation plutot qu'en mode collaboration. |
| Mix `[juste]` / `[contestable]` / `[simplification]` | Friction saine — positions diverses, collaboration productive. |
| Presence de `[angle-mort]` ou `[faux]` | Tension a traiter — l'orchestrateur DEVRAIT arbitrer explicitement. |
| Que des `ratifie` | Resolution sans tension — pas forcement problematique, mais a surveiller. |
| Absence de resolution sur N frictions | Frictions posees mais pas denouees — items a traiter ou a reporter dans Ouvert. |
| Ratio `conteste`/`rejete` eleve | Divergences persistantes — l'orchestrateur DEVRAIT investiguer. |

## Couche

La friction est **observationnelle**. Qualifier une position (resistance vs correction, angle-mort vs oubli) requiert un jugement semantique. Le persona pre-remplit, l'orchestrateur valide.

L'audit PEUT verifier la presence de la section et la conformite des marqueurs (computationnel), mais pas la justesse des qualifications (inferentiel).

## Rendu

Les marqueurs mots-cles et les tags de resolution sont le format du protocole. Les implementations DOIVENT les rendre lisiblement. Voir `implementation/implementation.md` pour le rendu Markdown.
