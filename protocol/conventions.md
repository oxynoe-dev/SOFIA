# Conventions

> Les règles concrètes d'une instance SOFIA.

---

Les principes disent **pourquoi**. Les conventions disent **comment**.
Ce document est la référence pour toute instance SOFIA. Il consolide
les règles dispersées dans les autres documents core/ et les rend
applicables.

## Structure d'une instance

```
instance/
├── sofia.md                     ← marqueur d'instance (voir instance.md)
├── shared/                      ← bus d'échange inter-personas
│   ├── conventions.md           ← conventions spécifiques à l'instance
│   ├── roadmap-{produit}.md     ← roadmaps produit
│   ├── backlog-archive.md       ← items terminés
│   ├── notes/                   ← messages inter-personas
│   │   └── archives/            ← notes traitées
│   ├── review/                  ← analyses critiques
│   │   └── archives/            ← reviews traitées
│   ├── features/                ← specs fonctionnalités
│   ├── orga/                    ← organisation équipe
│   │   ├── personas/            ← fiches persona (agnostiques produit)
│   │   └── contextes/           ← contexte-{persona}-{produit}.md
│   └── tools/                   ← scripts partagés
├── {workspace}/                 ← un par persona
│   ├── CLAUDE.md                ← instructions du persona
│   ├── sessions/                ← résumés de session
│   └── doc/                     ← production du persona
└── ...
```

Chaque persona a son workspace. `shared/` est le seul espace
accessible par tous.

## Nommage des artefacts

| Type | Convention | Emplacement |
|------|-----------|-------------|
| Note | `note-{destinataire}-{sujet}-{auteur}.md` | `shared/notes/` |
| Review | `review-{sujet}-{auteur}.md` | `shared/review/` |
| Feature | `feature-{sujet}.md` | `shared/features/` |
| Résumé de session | `{YYYY-MM-DD}-{HHmm}-{persona}.md` | `{workspace}/sessions/` |
| ADR | `adr-{NNN}.md` | Selon le projet |
| Roadmap | `roadmap-{produit}.md` | `shared/` |

Un artefact = un sujet. Pas de fichier fourre-tout.

## Frontmatter

**Tout fichier markdown de l'instance porte un frontmatter YAML.** Pas seulement `shared/` — tout : notes, reviews, features, études, specs, sessions, personas. Le frontmatter est le protocole universel de cycle de vie d'un artefact.

Pas d'accents dans les valeurs (`traite`, pas `traité`).

### Frontmatter par type d'artefact

**Notes** (bus shared/) :
```yaml
---
de: mira
pour: lea
nature: signal         # signal | question | demande | reponse
statut: nouveau        # nouveau | lu | traite
date: 2026-04-09
---
```

**Reviews** (bus shared/) :
```yaml
---
de: mira
pour: axel
nature: review
statut: nouveau        # nouveau | lu | traite
date: 2026-04-09
objet: adr-051
---
```

**Features** (bus shared/) :
```yaml
---
de: nora
pour: equipe
nature: feature
statut: proposition    # proposition | validee | rejetee | en-cours | livree
date: 2026-04-09
produit: convergence
---
```

**Études** (workspaces) :
```yaml
---
nature: etude
de: mira
statut: proposition    # proposition | validee | rejetee | archivee
date: 2026-04-09
produit: sofia
---
```

**Personas** (shared/orga/personas/) :
```yaml
---
nom: Mira
role: Architecte systeme & solution
workspace: architecture/
---
```

**Sessions** (workspaces) :
```yaml
---
nature: session
persona: mira
date: 2026-04-09
---
```

### Statuts (notes et reviews)

| Statut | Signification |
|--------|--------------|
| `nouveau` | Déposé, pas encore lu par le destinataire |
| `lu` | Lu par le destinataire |
| `traite` | Traité — prêt pour archivage |

Les artefacts sans frontmatter sont considérés `traite`.

## Archivage

Quand un artefact passe `traite`, le déplacer dans `archives/`
du dossier parent. Seuls les fichiers actifs restent à la racine.

```
shared/notes/
├── note-mira-xyz-axel.md        ← actif
└── archives/
    └── note-mira-abc-axel.md    ← traité
```

## Résumés de session

Chaque session produit un résumé. Sans exception.

**Fichier** : `{workspace}/sessions/{YYYY-MM-DD}-{HHmm}-{persona}.md`

**Sections obligatoires** :
- `## Produit` — fichiers créés ou modifiés, avec chemin
- `## Décisions` — ce qui a été tranché
- `## Notes déposées` — fichiers dans shared/
- `## Friction orchestrateur` — échanges marquants avec l'orchestrateur (voir ci-dessous)
- `## Ouvert` — ce qui reste à traiter

Pas de prose. Des listes courtes. 30 lignes max.

### Friction orchestrateur

La section `## Friction orchestrateur` capture la dynamique persona↔orchestrateur
pendant la session. C'est le seul endroit où cette friction est tracée —
les notes et reviews capturent l'inter-personas, les sessions capturent
la relation avec l'arbitre.

Chaque ligne porte un marqueur de friction (ref : `core/friction.md`) :

```markdown
## Friction orchestrateur
- ~ Emplacement audit-instance — [mira] proposé protocol/tools/, orchestrateur a challengé, convergence retenue
- ✓ Spec audit-instance — [mira] initiative spec complete, orchestrateur a validé
- ◐ Phase 1 structurelle — [PO] absente de la spec initiale, signalée par orchestrateur
- ✓ Factorisation CLAUDE.md — [PO] initiative orchestrateur, persona a affiné le design
```

Chaque ligne porte un **tag d'initiative** entre crochets :
- `[persona]` — le persona a pris position, l'orchestrateur a réagi
- `[PO]` — l'orchestrateur a pris position, le persona a réagi

**Ce que ça révèle** (via le script d'audit) :
- Quel persona prend des initiatives (vs exécute seulement)
- Quel persona challenge l'orchestrateur (et vice versa)
- Quel persona dit toujours oui → signal de domestication
- Ratio `[persona]` / `[PO]` → qui mène la session

**Règles** :
- Ne pas forcer — si la session est purement logistique, la section peut être vide ou absente
- Un item = un sujet, un marqueur, un tag d'initiative. Pas de prose
- Le marqueur qualifie la **position exprimée** (pas la personne)

## Commits

### Instance (experiments/)

Format : `{persona}: {résumé court} ({date})`

Les personas commitent directement dans le repo instance.
Un commit à la fois — pas de sessions parallèles sur le même repo.

### Repos produit

Les personas préparent le message de commit. L'orchestrateur exécute.

## Roadmaps

Chaque roadmap a un **owner** — un persona responsable de la cohérence.
L'owner ne priorise pas, il signale et range.

Il n'y a pas de backlog par persona. Tous les items vivent dans les
roadmaps. Les items terminés migrent vers `backlog-archive.md`.

### Structure d'une version

Chaque version dans un fichier roadmap porte un en-tête structuré :

```markdown
### v0.2.7 — Documentation runtime
<!-- produit: SOFIA | cible: 2026-04-15 | cloture: | statut: running -->

Description courte de la version (1-2 lignes).
```

| Champ | Obligatoire | Valeurs | Exemple |
|-------|-------------|---------|---------|
| `produit` | oui | nom du produit | `SOFIA` |
| `cible` | non | date ISO | `2026-04-15` |
| `cloture` | non | date ISO (rempli quand done) | `2026-04-12` |
| `statut` | oui | done \| running \| todo \| blocked | `running` |

Le commentaire HTML est invisible au rendu markdown mais parsable par
les outils d'instance.

### Structure d'un item

```
- [{statut}] {titre} @{porteur} [cible:{date}] [↔ {dep1}, {dep2}]
```

| Champ | Obligatoire | Position | Exemple |
|-------|-------------|----------|---------|
| `statut` | oui | entre crochets en début | `[running]` |
| `titre` | oui | texte libre après le statut | `Audit experiments par Sofia` |
| `@porteur` | oui | après le titre | `@mira` |
| `cible:{date}` | non | après le porteur | `cible:2026-04-15` |
| `↔ {deps}` | non | en fin de ligne | `↔ katen, convergence` |

### Statuts item

| Statut | Sémantique |
|--------|-----------|
| `done` | Terminé, livré |
| `running` | En cours de travail actif |
| `ready` | Prêt à démarrer, pas de blocage |
| `todo` | Planifié, pas encore prêt |
| `blocked` | Bloqué — raison après `⊘` |

### Dépendances

Le marqueur `↔` en fin de ligne désigne les produits ou personas dont
l'item dépend ou qu'il alimente. Pour les dépendances sur une version
spécifique, utiliser `produit:version` (ex : `↔ katen:v0.23`).

### Version visible

Les rendus produit (documentation, site, livre bleu) affichent le
numéro de version SOFIA applicable. Le lecteur sait quel état de la
méthode il consulte.

## CLAUDE.md — anatomie

Le `CLAUDE.md` est un **aiguillage runtime**, pas un document de contenu.
Il pointe vers deux fichiers qui portent la substance :

```markdown
Lis `persona-mira.md`.
Lis `contexte-mira-katen.md`.
```

### Trois couches

| Fichier | Couche | Contenu | Emplacement |
|---------|--------|---------|-------------|
| `CLAUDE.md` | Runtime | Aiguillage — 2 lignes | Racine du workspace ou du repo produit |
| `persona-{nom}.md` | Core | Rôle, posture, contraintes, friction, protocole de session | `shared/orga/personas/` |
| `contexte-{persona}-{produit}.md` | Instance | Documents clés, périmètre, commandes spécifiques au persona dans ce repo | `shared/orga/contextes/` |

### Pourquoi cette séparation

- **Le persona est agnostique du produit.** Mira est architecte qu'elle travaille
  sur Katen, SOFIA ou un autre projet. Son rôle, sa posture, ses contraintes
  ne changent pas.
- **Le contexte est spécifique.** Mira dans katen/ lit les ADR et les principes.
  Axel dans katen/ lit le code et les tests. Le même produit, deux vues.
- **Le CLAUDE.md est un détail runtime.** C'est le format Claude Code. Un autre
  provider aura un autre mécanisme d'injection. Le contenu (persona + contexte)
  reste le même.

### Conséquence

Plus de duplication entre le CLAUDE.md du workspace instance et le CLAUDE.md
du repo produit. Un seul persona.md, un contexte par couple persona×produit,
des CLAUDE.md de 2 lignes partout.

Voir `runtime/claude-code/claude-md.md` pour le détail runtime.

## Publication web

Toute page publiée sur un domaine de l'instance doit porter :
- `<title>` au format `{Page} — {Domaine}`
- `<meta name="description">` (150 car. max)
- Open Graph tags (`og:title`, `og:description`, `og:type`, `og:url`)
- Favicon déclaré
- Entrée dans le `sitemap.xml` du domaine

## Conventions d'instance

Ce document définit les conventions **méthode** — communes à toute
instance SOFIA. Chaque instance peut ajouter ses propres conventions
dans `shared/conventions.md` (structure spécifique, rôles supplémentaires,
règles de publication, etc.).
