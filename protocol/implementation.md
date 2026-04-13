# Implementation

> Comment H2A est implemente aujourd'hui — et comment il pourrait l'etre demain.

---

## Principe

H2A definit la semantique des interactions (entites, invariants, couches protocolaire/observationnelle). Ce document decrit l'implementation courante. Une implementation differente serait conforme a H2A tant qu'elle respecte la semantique definie dans `h2a.md`, `friction.md`, `contribution.md` et `exchange.md`.

## Implementation courante

### Stack

| Composant | Choix | Role |
|-----------|-------|------|
| Format des artefacts | Markdown + frontmatter YAML | Lisible par l'humain et par l'outil d'audit, pas de dependance logicielle |
| Persistance | git | Historique immutable, diff, blame — trace par session |
| Structure des espaces | Repertoires filesystem | Un repertoire = un espace. Isolation naturelle |
| Espace partage | `shared/` a la racine de l'instance | Canal unique entre personas |
| Marqueur d'instance | Fichier `sofia.md` a la racine | Identifie un deploiement SOFIA et sa version |
| Provider IA | Claude Code | CLAUDE.md comme instruction persona, hooks, memoire projet |

### Conventions de tracabilite

**Commits** (recommande) :
```
{persona}: {resume court} ({date})
```
Un commit par session.

**Resumes de session** :
```
{espace}/sessions/{YYYY-MM-DD}-{HHmm}-{persona}.md
```

### Structure d'une instance

```
instance/
├── sofia.md                     ← marqueur d'instance
├── shared/                      ← espace partage (bus d'echange)
│   ├── conventions.md           ← conventions specifiques a l'instance
│   ├── roadmap-{produit}.md     ← roadmaps produit
│   ├── notes/                   ← messages inter-personas
│   │   └── archives/
│   ├── review/                  ← analyses critiques
│   │   └── archives/
│   ├── features/                ← specs fonctionnalites
│   └── orga/                    ← organisation equipe
│       ├── personas/            ← fiches persona
│       └── contextes/           ← contextes par persona-produit
├── {espace}/                    ← un par persona
│   ├── CLAUDE.md                ← instructions du persona (runtime)
│   ├── sessions/                ← resumes de session
│   └── doc/                     ← production du persona
└── ...
```

### Nommage des artefacts

| Type | Convention | Emplacement |
|------|-----------|-------------|
| Note | `note-{destinataire}-{sujet}-{emetteur}.md` | `shared/notes/` |
| Review | `review-{sujet}-{emetteur}.md` | `shared/review/` |
| Feature | `feature-{sujet}.md` | `shared/features/` |
| Resume de session | `{YYYY-MM-DD}-{HHmm}-{persona}.md` | `{espace}/sessions/` |
| ADR | `adr-{NNN}.md` | Selon le projet |
| Roadmap | `roadmap-{produit}.md` | `shared/` |

### Frontmatter

Tout fichier markdown de l'instance porte un frontmatter YAML. Pas d'accents dans les valeurs.

**Messages** (notes, reviews) :
```yaml
---
de: persona-emetteur
pour: persona-destinataire
nature: signal           # signal | question | demande | reponse
statut: nouveau          # nouveau | lu | traite
date: YYYY-MM-DD
---
```

**Sessions** :
```yaml
---
persona: nom-persona
date: YYYY-MM-DD
session: "HHmm"
---
```

### Archivage

Quand un artefact passe a `statut: traite`, il est deplace dans `archives/` du repertoire parent.

### Statut du cycle de vie

| Statut | Signification |
|--------|--------------|
| `nouveau` | Depose, pas encore lu par le destinataire |
| `lu` | Lu par le destinataire |
| `traite` | Le destinataire a fait ce qu'il fallait avec |

### Outillage

| Outil | Role |
|-------|------|
| `audit-instance.py` | Verifie la conformite d'une instance au protocole |
| `create-instance.py` | Scaffolde une nouvelle instance |
| `sofia.md` | Persona meta — instancie, audite. Operatrice du protocole |

---

## Ce qui est implementation vs protocole

| Element | Protocole (h2a.md) | Implementation (ce doc) |
|---------|--------------------|-----------------------|
| "Chaque session produit une trace" | ✓ | |
| "La trace est un fichier .md commite dans git" | | ✓ |
| "Les marqueurs sont [juste] [contestable] etc." | ✓ | |
| "Les marqueurs sont dans un fichier Markdown" | | ✓ |
| "L'espace partage est le seul canal" | ✓ | |
| "L'espace partage est un dossier shared/" | | ✓ |
| "L'instance est identifiable" | ✓ | |
| "L'instance est identifiee par un fichier sofia.md" | | ✓ |

---

## Perspectives

### API HTTP

H2A pourrait etre implemente comme une API REST :
- Chaque entite (Instance, Espace, Persona, Echange, Friction, Contribution) devient une ressource
- Les frontmatter YAML deviennent des schemas JSON
- Les statuts (`nouveau` → `lu` → `traite`) deviennent des transitions d'etat
- L'audit devient un endpoint de verification

### Base de donnees

Les resumes de session, messages et marqueurs de friction pourraient vivre dans une base relationnelle ou documentaire. L'historique git serait remplace par un log d'evenements.

### Interoperabilite MCP / A2A

H2A couvre la couche humain-assistant. MCP et A2A couvrent les couches agent-outils et agent-agent. Un systeme complet pourrait combiner les trois :
- H2A pour la coordination humain-assistants
- MCP pour l'acces aux ressources par les assistants
- A2A pour la coordination inter-assistants (si l'invariant de routage humain est assoupli)

### Wire format

Si H2A evolue vers un protocole technique, il faudra definir un wire format (JSON, protobuf, etc.) et une spec d'interoperabilite. Ce n'est pas dans le scope actuel.
