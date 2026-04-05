# Conventions

> Les règles concrètes d'une instance Voix.

---

Les principes disent **pourquoi**. Les conventions disent **comment**.
Ce document est la référence pour toute instance Voix. Il consolide
les règles dispersées dans les autres documents core/ et les rend
applicables.

## Structure d'une instance

```
instance/
├── voix.md                      ← marqueur d'instance (voir instance.md)
├── shared/                      ← bus d'échange inter-personas
│   ├── conventions.md           ← conventions spécifiques à l'instance
│   ├── roadmap-{produit}.md     ← roadmaps produit
│   ├── backlog-archive.md       ← items terminés
│   ├── notes/                   ← messages inter-personas
│   │   └── archives/            ← notes traitées
│   ├── review/                  ← analyses critiques
│   │   └── archives/            ← reviews traitées
│   ├── features/                ← specs fonctionnalités
│   ├── orga/                    ← organisation équipe (personas, lexique)
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

Chaque artefact dans `shared/` porte un frontmatter :

```yaml
---
de: mira
pour: lea
type: signal           # signal | question | demande | reponse
statut: nouveau        # nouveau | lu | traite
date: 2026-03-30
---
```

Pas d'accents dans les valeurs (`traite`, pas `traité`).

### Statuts

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
- `## Ouvert` — ce qui reste à traiter

Pas de prose. Des listes courtes. 30 lignes max.

## Commits

### Instance (experiments/)

Format : `{persona}: {résumé court} ({date})`

Les personas commitent directement dans le repo instance.
Un commit à la fois — pas de sessions parallèles sur le même repo.

### Repos produit

Les personas préparent le message de commit. Le PO exécute.

## Roadmaps

Chaque roadmap a un **owner** — un persona responsable de la cohérence.
L'owner ne priorise pas, il signale et range.

Chaque item porte un `@owner` — le persona responsable de l'exécution.

Il n'y a pas de backlog par persona. Tous les items vivent dans les
roadmaps. Les items terminés migrent vers `backlog-archive.md`.

## CLAUDE.md — anatomie

Le `CLAUDE.md` de chaque workspace contient :

1. **Persona** — qui, quelle posture
2. **Périmètre** — quoi, quels livrables
3. **Accès** — où lire, où écrire, où c'est interdit
4. **Conventions** — formats, workflow
5. **Protocole de session** — boot, fermeture

Voir `runtime/claude-code/claude-md.md` pour le détail.

## Publication web

Toute page publiée sur un domaine de l'instance doit porter :
- `<title>` au format `{Page} — {Domaine}`
- `<meta name="description">` (150 car. max)
- Open Graph tags (`og:title`, `og:description`, `og:type`, `og:url`)
- Favicon déclaré
- Entrée dans le `sitemap.xml` du domaine

## Conventions d'instance

Ce document définit les conventions **méthode** — communes à toute
instance Voix. Chaque instance peut ajouter ses propres conventions
dans `shared/conventions.md` (structure spécifique, rôles supplémentaires,
règles de publication, etc.).
