# Architecture — SOFIA

**Date** : 16/04/2026
**Auteur** : Aurele — Architecte methode
**Statut** : Reference

---

## 1. Identite

| | |
|---|---|
| **Nom** | SOFIA |
| **Vocation** | Methode d'orchestration d'assistants IA specialises |
| **Protocole** | H2A (Human-to-Assistant) |
| **Repo** | `oxynoe-dev/sofia` |
| **Licence** | MIT |
| **Public** | Developpeurs et equipes utilisant des assistants IA en CLI (Claude Code, puis Mistral, Gemini...) |
| **Principe fondateur** | La contrainte force la qualite — un LLM sans limites ne produit rien de bon |

### Motivation

![Le triangle SOFIA](figures/fig-triangle-sofia.svg)

Trois concepts interdependants sont a l'origine de SOFIA :
- **Persona** — un LLM contraint par un role, un perimetre et des interdits
- **Friction** — les desaccords qui emergent des contraintes entre personas
- **Artefact** — le fichier structure qui materialise l'echange et la trace

L'**orchestrateur** (humain) est au centre : il orchestre, filtre, contextualise, tranche. Sans lui, la friction est du chaos. Avec lui, elle produit de meilleures decisions.

### Positionnement

SOFIA n'est pas un framework, pas une librairie, pas un outil. C'est une **methode** : un ensemble de principes, de protocoles et de references pour organiser des assistants IA specialises autour d'un projet.

Le protocole H2A definit la couche de coordination humain-assistants. Il se positionne a cote des protocoles techniques existants :

| Protocole | Couche | Nature |
|-----------|--------|--------|
| MCP (Anthropic) | Agent ↔ Outils | Technique — wire protocol |
| A2A (Google) | Agent ↔ Agent | Technique — communication |
| **H2A** | **Humain ↔ Assistant** | **Organisationnel — coordination** |

H2A n'est pas un protocole technique — il definit la semantique des interactions, pas leur implementation.

---

## 2. Principes d'architecture

### P1 — Le core tient sans outil

Les 7 principes et le modele conceptuel sont independants de Claude Code. On pourrait appliquer SOFIA avec des fichiers texte et un editeur. Le runtime est un accelerateur, pas un prerequis.

### P2 — Cinq couches + canvas

| Couche | Repond a | Change quand |
|--------|----------|-------------|
| Core | Quels sont les invariants ? | La methode change (rare) |
| Protocol | Quelle est la semantique des interactions ? | Le protocole evolue |
| Implementation | Comment ca se materialise ? | On change de stack (filesystem → API) |
| Runtime | Comment le provider execute ? | On change de provider (Claude → Mistral) |
| Canvas | A quoi ca ressemble en vrai ? | On documente de nouveaux patterns |

On peut changer l'implementation sans toucher au protocole. On peut changer le runtime sans toucher a l'implementation. On peut lire le core sans connaitre l'outil.

### P3 — L'orchestrateur est l'unique point de passage

Aucun echange direct entre personas. L'orchestrateur filtre, reformule, contextualise, tranche. C'est le cout de la qualite.

### P4 — L'isolation cree le besoin d'artefacts

Un persona qui ne voit pas le code est oblige de specifier. Un persona qui ne decide pas de l'architecture est oblige de remonter les frictions. L'isolation n'est pas une limitation — c'est le mecanisme generateur.

### P5 — Les fichiers sont la source de verite

Pas les conversations, pas la memoire, pas les sessions compressees. Les fichiers versionnes dans git.

### P6 — Gradient d'activation

| Seuil | Ce qui s'active |
|---|---|
| **1 persona** | CLAUDE.md + sessions/ — la base |
| **2+ personas** | shared/ (notes, reviews) — le bus d'echange |
| **3+ personas** | Conventions formalisees, team-orga |
| **5+ personas, 2+ produits** | Convergence (produit compagnon) — dashboard, inbox |

On commence petit, on ajoute de la structure quand la charge mentale de l'orchestrateur l'exige.

### P7 — Semantique d'abord, implementation ensuite

Le protocole definit le quoi (entites, invariants, operations). L'implementation definit le comment (Markdown, git, filesystem). Cette separation permet :
- D'auditer mecaniquement la couche protocolaire
- De changer de stack sans changer de methode
- De raisonner sur le protocole sans se noyer dans les details de rendu

---

![Architecture SOFIA](figures/arch-sofia.svg)

## 3. Architecture — 5 couches + canvas

Cinq couches dans le repo produit, plus une couche canvas transversale.

```
sofia/
├── core/              ← invariants methode (principes, modele, devoirs)
├── protocol/          ← protocole H2A (invariants, operations, entites)
├── implementation/    ← materialisation courante (filesystem, audit, scaffolding)
├── runtime/           ← adaptateurs par provider (claude-code, sofia.md)
├── canvas/            ← references d'instanciation + outils d'inspiration
│   ├── archetypes/    ← modeles de personas par role
│   ├── artefacts/     ← a quoi ressemble une note, une review, une session...
│   ├── patterns/      ← structures recurrentes observees sur le terrain
│   ├── workflows/     ← processus types
│   └── examples/      ← katen/ (snapshot d'instance terrain)
└── doc/               ← documentation, feedback, ADR, figures
```

### core/ — pourquoi SOFIA existe

Les invariants. Si tu les supprimes, ce n'est plus SOFIA.

| Document | Contenu |
|----------|---------|
| `principes.md` | 7 principes — la contrainte force la qualite, l'orchestrateur arbitre, les artefacts sont le protocole |
| `modele.md` | 7 entites constitutives (Orchestrateur, Instance, Espace, Persona, Echange, Friction, Contribution) |
| `devoirs.md` | 6 devoirs de l'orchestrateur — obligations non-delegables |

**Regle de versionnage** : modifier un document core = minor bump.

### protocol/ — quoi tracer (contrat d'auditabilite)

4 documents. Protocole H2A + 3 specs operationnelles. Noms en anglais (i18n). Ce que l'audit lit cross-instance.

| Document | Contenu | Ce que l'audit lit |
|----------|---------|---------------------|
| `h2a.md` | 5 invariants, 9 operations, distinction protocolaire/observationnelle | Entites, invariants, critere d'auditabilite |
| `friction.md` | 5 marqueurs, 4 resolutions PXP, mutabilite, signalerPattern() | Ratio par assistant, detection domestication |
| `exchange.md` | Sessions (synchrone) et artefacts (asynchrone), frontmatter, nommage | Frequence, assistant, date, section friction |
| `contribution.md` | Flux epistemique — direction (H/A), type (matiere, structure, contestation, decision) | Tags H/A, ratio matiere/structure |

**5 invariants H2A** :
1. Friction constitutive
2. Humain arbitre
3. Isolation
4. Tracabilite
5. Opacite residuelle (limitation structurelle, pas une capacite)

**Distinction protocolaire / observationnelle** :

| Couche | Statut | Verification |
|--------|--------|-------------|
| Protocolaire | Garanti | Computationnelle (deterministe, automatisable) |
| Observationnelle | Best-effort | Inferentielle (jugement semantique, non-deterministe) |

### implementation/ — comment ca se materialise

Separe de la semantique (protocol/) pour permettre d'autres materialisations (API REST, BDD...). La distinction : "la friction porte 5 dimensions" est du protocole ; "la friction est une ligne Markdown avec symbole + mot-cle + initiative" est de l'implementation.

| Composant | Role |
|-----------|------|
| `implementation.md` | Stack courante, mapping operations → gestes concrets |
| `filesystem/audit-instance.py` | Conformite d'une instance (60 tests) |
| `filesystem/create-instance.py` | Scaffolde une nouvelle instance (31 tests) |
| `filesystem/analysis.py` | Analyse multi-instance — friction, contribution, direction (en calibration) |
| `filesystem/analysis.html` | Dashboard interactif — 7 graphiques, 3 tables, 4 filtres |
| `filesystem/conventions.md` | Template de conventions standard |

### runtime/ — avec quel outil

Le seul point qui change quand on porte SOFIA sur un autre assistant IA. Remplacable sans toucher core/, protocol/ ni implementation/.

| Composant | Role |
|-----------|------|
| `claude-code/claude-md.md` | Anatomie du CLAUDE.md — le gardien du persona |
| `claude-code/memoire.md` | Memoire persistante entre conversations |
| `claude-code/sessions.md` | Protocole ouverture/fermeture, resume obligatoire |
| `claude-code/hooks.md` | Automatisations declenchees par des evenements |
| `sofia.md` | Persona Sofia — 4 modes operationnels |

**Multi-provider** (v0.4) : `runtime/mistral/`, `runtime/gemini/`, etc. In-repo, pas repos separes (ADR-010).

### canvas/ — a quoi ca ressemble

Pas de la prescription — de l'inspiration. On s'en inspire, on ne copie pas.

| Repertoire | Contenu | Tag implementation |
|------------|---------|-------------------|
| `archetypes/` | 9 modeles de personas par role | Non — agnostique |
| `artefacts/` | 10 formats de reference | `implementation:filesystem` |
| `patterns/` | 4 structures recurrentes | Non — agnostique |
| `workflows/` | 10 processus types | Non — agnostique |
| `examples/` | katen/ — snapshot instance terrain | `implementation:filesystem` |

Le tag `implementation:filesystem` distingue ce qui est lie a l'implementation courante de ce qui est de la methode pure.

### doc/ — comment s'organiser

Tout le reste. Recommande, pas obligatoire.

| Contenu | Role |
|---------|------|
| `arch-sofia.md` | Ce document |
| `utilisateur.md` | Guide utilisateur unifie |
| `demarrer-manuel.md` | Guide de demarrage sans Sofia |
| `guide-operateur.md` | 9 operations H2A vues de l'orchestrateur |
| `grammaire-derivation.md` | Grammaire de derivation (2 modes, 8 etapes) |
| `condition-cachee.md` | Profil cible, auto-diagnostic |
| `livre-bleu-sofia.md` | Livre bleu en .md |
| `feedback/` | 11 REX terrain |
| `adr/` | 12 decisions structurantes |
| `figures/` | Visuels SVG |

---

## 4. Modele conceptuel

### MCD — 7 entites constitutives

![MCD SOFIA — 7 entites H2A](figures/fig-mcd-h2a.svg)

7 entites, organisees en 3 niveaux. Ref: `core/modele.md`.

| Niveau | Entites | Nature |
|--------|---------|--------|
| **Topologie** | Orchestrateur, Instance, Espace, Persona | La structure — qui, ou, dans quoi |
| **Interaction** | Echange | Le flux — sessions et artefacts |
| **Observation** | Friction, Contribution | Les signaux — positions et apports epistemiques |

### Entites

| Entite | Definition | Champs cles |
|--------|-----------|-------------|
| **Orchestrateur** | L'humain. Orchestre, arbitre, route. N'a pas d'espace — traverse tout | identifiant, instances |
| **Instance** | Deploiement de la methode sur un projet. Identifiee par `sofia.md` | identifiant, espaces, version_methode |
| **Espace** | Perimetre isole d'un persona. 1 persona = 1 espace | identifiant, persona, partage |
| **Persona** | Role contraint. 7 dimensions (identite, posture, perimetre, livrables, interdits, challenge, collaboration) | 7 dimensions |
| **Echange** | Trace d'interaction — `session` (synchrone) ou `artefact` (depot asynchrone) | type, instance, espace, date |
| **Friction** | Position epistemique qualifiee. 5 marqueurs, 4 resolutions PXP | marqueur, initiative, resolution, description |
| **Contribution** | Apport epistemique. Direction (H/A) + type (matiere, structure, contestation, decision) | direction, type, description |

### Relations

| De | Vers | Relation | Cardinalite |
|----|------|----------|-------------|
| Orchestrateur | Instance | orchestre | 1 → 1..* |
| Instance | Espace | contient | 1 → 1..* |
| Espace | Persona | opere | 1 → 1 |
| Persona | Echange | emet / recoit | 1 → * |
| Orchestrateur | Echange | participe | 1 → * |
| Echange | Friction | genere | 1 → 0..* |
| Echange | Contribution | genere | 1 → 0..* |
| Persona | Persona | challenge | * → * |
| Friction | Friction | amende (antecedent) | 0..1 → 0..1 |

### Couches de formalisation

La distinction protocolaire/observationnelle traverse le MCD :

| Entite | Couche | Verification |
|--------|--------|-------------|
| Instance, Espace, Echange | Protocolaire | Computationnelle — l'audit verifie mecaniquement |
| Friction (marqueur, initiative) | Observationnelle | Inferentielle — le persona pre-remplit, l'orchestrateur valide |
| Friction (resolution) | Observationnelle | Inferentielle — DEVRAIT, pas DOIT |
| Friction (antecedent/lignage) | Protocolaire | Computationnelle — ref: verifiable, chaine de frictions |
| Contribution | Observationnelle | Inferentielle — PEUT, optionnelle |

### Flux des echanges

![Flux elementaire](figures/fig-flux-elementaire.svg)

Tout passe par l'orchestrateur. Deux patterns :

#### Session (persona ↔ orchestrateur)

1. L'orchestrateur ouvre une session avec un persona
2. Echange direct — dialogue, arbitrage, decisions
3. La friction est tracee dans la session avec les marqueurs
4. Le persona ecrit le resume dans `sessions/`

#### Message (persona ↔ persona)

1. Persona A depose un artefact dans `shared/` (note, review, feature)
2. L'orchestrateur lit, decide de router
3. L'orchestrateur ouvre une session avec Persona B et lui presente l'artefact
4. Persona B lit, repond, depose sa reponse dans `shared/`
5. L'orchestrateur route la reponse vers Persona A lors d'une prochaine session

Les personas ne se parlent jamais directement. L'orchestrateur est le routeur humain de tous les echanges. La friction emerge a chaque etape.

### Instance SOFIA

![Anatomie d'une instance](figures/fig-anatomie-instance.svg)

Le fichier `sofia.md` a la racine identifie le depot comme instance et lie a la methode.

Deux types d'instance :
- **Operationnelle** — longue duree, memoire cumulative, produit des livrables metier
- **D'audit** — ephemere, sans memoire inter-cycles, challengers miroir 1:1, detruite apres synthese

Sofia monte les deux types depuis le produit. Elle n'a pas de workspace dans les instances — son exteriorite est la condition de son objectivite (ADR-009).

---

## 5. Portabilite multi-provider

### Architecture actuelle

`core/` et `protocol/` sont provider-agnostic. `implementation/` est potentiellement multi-stack. `runtime/` est le seul point de variation par provider. Ajouter un provider = ajouter `runtime/mistral/`, etc.

### Strategie (ADR-010)

Tout dans le meme repo. Pas de repos separes par plateforme (supersede ADR-004).

```
runtime/
├── claude-code/       ← implementation de reference
├── mistral/           ← cible v0.4 (ete 2026)
└── gemini/            ← si pertinent
```

Pre-requis : retours utilisateurs v0.3. Ne pas anticiper sans feedback.

La distinction implementation/runtime est structurante :
- `implementation/` repond a "comment les artefacts sont stockes et audites" (filesystem, API, BDD)
- `runtime/` repond a "comment le persona recoit ses instructions et persiste son contexte" (CLAUDE.md, MISTRAL.md)

---

## 6. Decisions

| Decision | ADR | Raison |
|----------|-----|--------|
| Semver | 001 | Credibilite GitHub + communication |
| Marqueur d'instance sofia.md | 005 | Instance auto-descriptive |
| Isolation core/ pre-publication | 006 | Stabilite avant contributions |
| Core / Protocol / Runtime | 008 | Separation invariants / contrat / implementation |
| Couche Instance + position Sofia | 009 | Instanciation ≠ methode, exteriorite Sofia |
| Multi-plateforme in-repo | 010 | Runtime adapters, pas repos separes (supersede 004) |
| Protocole H2A | 011 | Formalisation coordination humain-assistants |
| Extraction implementation/ | 012 | Semantique ≠ materialisation |

---

> **Implementation courante.** Ce document decrit l'architecture de la methode — pas son outillage. Pour le detail de la materialisation (stack, mapping operations → gestes concrets, audit, scaffolding, dashboard) : voir `implementation/implementation.md` et `implementation/filesystem/`.

---

*Aurele — 16/04/2026*
