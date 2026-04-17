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
| **marqueur** | `[sound]`, `[contestable]`, `[simplification]`, `[blind_spot]`, `[refuted]` | DOIT |
| **description** | Resume court de la position | DOIT |
| **initiative** | `[persona]` ou `[PO]` — qui a initie le sujet de friction | DOIT |
| **resolution** | `ratified`, `contested`, `revised`, `rejected` — geste epistemique de resolution | DEVRAIT |
| **antecedent** | Reference a une friction anterieure dans le lignage | DOIT (si lignage) |

**Portee** : une friction est rattachee a un echange, lui-meme rattache a un espace dans une instance.

## Marqueurs

5 positions epistemiques. Ce sont des positions, pas une echelle d'intensite. L'ensemble est ferme — une instance NE DOIT PAS ajouter de marqueurs.

| Marqueur | Signification |
|----------|--------------|
| `[sound]` | Corroboration — position correcte |
| `[contestable]` | Sous-determination — defendable mais pas la seule lecture |
| `[simplification]` | Reductionnisme — le reel est plus complexe |
| `[blind_spot]` | Incompletude — donnees manquantes |
| `[refuted]` | Refutation — factuellement incorrect ou incoherent |

Les marqueurs DOIVENT etre exprimes en mots-cles entre crochets.

> **FR retrocompat.** Le parser accepte aussi les identifiants FR (juste, angle-mort, faux, ratifie, conteste, revise, rejete, nouveau, lu, traite, matiere).

> **Note theorique.** Ces 5 positions sont compatibles (sans equivalence stricte) avec le modele d'argumentation de Toulmin (1958) : `[sound]` ≈ absence de rebuttal, `[contestable]` ≈ challenge du qualifier, `[simplification]` ≈ challenge du warrant, `[blind_spot]` ≈ challenge des data, `[refuted]` ≈ refutation du claim. Ce rapprochement est un eclairage, pas une contrainte du protocole.

## Resolution

4 gestes epistemiques. Chaque friction DEVRAIT porter un tag de resolution qui qualifie ce qui s'est passe apres la qualification — pas le contenu, mais le denouement.

| Tag | Signification |
|-----|---------------|
| `ratified` | Accord — la position est acceptee par l'autre partie |
| `contested` | Desaccord maintenu — pas de changement de position |
| `revised` | Desaccord avec changement de position de l'une des parties |
| `rejected` | Desaccord terminal — la position est ecartee |

L'ensemble est ferme — une instance NE DOIT PAS ajouter de tags de resolution.

Le tag de resolution est pose par le redacteur du resume (persona pour les sessions, emetteur pour les artefacts). Il reflete la perception du redacteur sur le denouement, pas un verdict objectif. L'orchestrateur PEUT corriger.

### Mutabilite inter-sessions et lignage

Une resolution peut evoluer dans une session ulterieure (`contested` → `revised`, `rejected` → `ratified`, etc.). La trace de session reste un document historique immutable — c'est la nouvelle session qui porte la revision.

Quand une friction revise une resolution anterieure, elle DOIT porter un champ `ref:` qui pointe vers la friction d'origine :

```
ref: <id-session>/<id-friction>
```

> **Exemple** :
>
> ```
> - [sound] la distinction protocolaire/observationnelle couvre bien le cas — [aurele] → ratified (ref: 2026-04-10-1430-aurele/3)
> ```

Le `ref:` cree un **lignage** : une chaine de frictions liees (position initiale → contestation → resolution). Une chaine constitue une seule friction logique. La resolution courante est celle du dernier maillon.

**Regles du lignage** :

1. Une chaine de frictions liees par `ref:` = une friction logique, pas N frictions independantes.
2. La resolution courante est celle du dernier maillon de la chaine.
3. Une friction est **ouverte** si elle n'a pas de resolution ET qu'aucune friction ulterieure ne la resout via `ref:`.

Cette mutabilite est coherente avec le caractere defaisable du raisonnement plausible (Rescher 1976) : ce qui est ratifie aujourd'hui peut etre conteste demain a l'entree de nouvelles donnees.

> **Note theorique.** Ces 4 gestes sont inspires du protocole PXP (Mestha et al. 2025 — RATIFY, REFUTE, REVISE, REJECT). PXP qualifie les gestes dans un echange multi-tour humain-LLM. H2A les applique a la resolution des frictions, pas aux messages individuels. Ce rapprochement est un eclairage, pas une contrainte du protocole.

## Format

Chaque ligne de friction DOIT porter :
1. Le marqueur entre crochets
2. Une description courte
3. Un tag d'initiative : `[persona]` ou `[PO]`
4. Un tag de resolution (DEVRAIT) : `→ ratified`, `→ contested`, `→ revised`, `→ rejected`

> **Exemple** (implementation Markdown, voir `implementation/implementation.md`) :
>
> ```
> ## Friction
> - [contestable] le mapping Toulmin est suggestif, pas acquis — [PO] → revised
> - [blind_spot] scaffolding absent de la review Böckeler — [aurele] → ratified
> ```

## Interpretation

| Signal | Lecture |
|--------|--------|
| Que des `[sound]` | Friction absente — signal d'alerte. Le persona est peut-etre en mode validation plutot qu'en mode collaboration. |
| Mix `[sound]` / `[contestable]` / `[simplification]` | Friction saine — positions diverses, collaboration productive. |
| Presence de `[blind_spot]` ou `[refuted]` | Tension a traiter — l'orchestrateur DEVRAIT arbitrer explicitement. |
| Que des `ratified` | Resolution sans tension — pas forcement problematique, mais a surveiller. |
| Absence de resolution sur N frictions | Frictions posees mais pas denouees — items a traiter ou a reporter dans Ouvert. |
| Ratio `contested`/`rejected` eleve | Divergences persistantes — l'orchestrateur DEVRAIT investiguer. |

## Couche

La friction est **observationnelle**. Qualifier une position (resistance vs correction, angle-mort vs oubli) requiert un jugement semantique. Le persona pre-remplit, l'orchestrateur valide.

L'audit PEUT verifier la presence de la section et la conformite des marqueurs (computationnel), mais pas la justesse des qualifications (inferentiel).

## reportPattern()

Meta-operation sur la friction. Mitigation de l'opacite residuelle de l'orchestrateur (invariant 5, voir `h2a.md`).

### Probleme

Face a un rejet repete de friction, trois hypotheses sont phenomenologiquement identiques de l'interieur : erreur du persona (biais LLM), conviction legitime de l'orchestrateur, resistance inconsciente. L'orchestrateur ne peut pas arbitrer sa propre resistance a la friction. Ce probleme est insoluble au sens strict (version appliquee du Münchhausen-Trilemma), mais mitigeable.

### Declenchement

Le persona detecte une **convergence thematique de rejets** — N rejets portant sur le meme axe, la meme hypothese, le meme presuppose non examine. La detection releve de la couche observationnelle : le persona fait l'analyse, pas un comptage mecanique.

### Mecanisme

**Etape 1 — Constat factuel.** Le persona signale le pattern sans jugement. Purement descriptif, verifiable.

**Etape 2 — Trois hypotheses argumentees.** Le persona argumente chacune :

- **Erreur LLM** : pourquoi les frictions pourraient etre mal calibrees (pattern repetitif, manque de contexte, hallucination possible)
- **Conviction legitime** : pourquoi la position de l'orchestrateur pourrait etre correcte malgre les objections (reconstruction de la coherence)
- **Resistance** : pourquoi il est possible que l'orchestrateur ait un angle mort (ce que le rejet systematique protege, ce qu'il coute de considerer)

Le persona ne tranche pas — compatible avec l'invariant "humain arbitre".

**Etape 3 — Qualification obligatoire.** L'orchestrateur DOIT qualifier sa reponse en articulant pourquoi il choisit l'hypothese qu'il choisit. Cette justification est tracee.

### Garde-fous

**Asymetrie de charge de preuve.** Si l'orchestrateur choisit "erreur LLM" → charge faible (montrer pourquoi la friction est mal fondee). Si l'orchestrateur choisit "conviction" → charge elevee (steelmanner la position adverse et expliquer pourquoi elle ne suffit pas).

**Compteur visible.** La distribution des choix d'hypothese est maintenue et rendue visible. Ce compteur releve de la couche protocolaire (computationnel, verifiable).

### Couche

La detection de la convergence thematique releve de la couche **observationnelle**. Le compteur de choix releve de la couche **protocolaire**.

---

## Rendu

Les marqueurs mots-cles et les tags de resolution sont le format du protocole. Les implementations DOIVENT les rendre lisiblement. Voir `implementation/implementation.md` pour le rendu Markdown.
