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
A chaque fermeture, le persona cree un **nouveau** fichier. Le `HHmm` est l'heure de la cloture (pas du boot). Une session longue avec plusieurs clotures produit plusieurs fichiers.

### Structure d'une instance

Le scaffolding est **minimal** — seuls les elements necessaires au protocole sont crees a l'initialisation. L'organisation interne de `shared/` (sous-repertoires, conventions de nommage des artefacts, archivage) releve des conventions d'instance, pas de l'implementation standard.

```
instance/                        ← scaffolding (create-instance)
├── sofia.md                     ← marqueur d'instance
├── shared/                      ← espace partage (bus d'echange)
│   ├── conventions.md           ← conventions specifiques a l'instance
│   └── orga/                    ← organisation equipe
│       ├── personas/            ← fiches persona
│       └── contextes/           ← contextes par persona-produit
├── {espace}/                    ← un par persona
│   ├── CLAUDE.md                ← instructions du persona (runtime)
│   └── sessions/                ← resumes de session
└── ...
```

Le protocole impose `shared/` comme canal unique et les artefacts avec frontmatter. Comment l'instance organise ses artefacts dans `shared/` (sous-repertoires, nommage, archivage) est une decision locale documentee dans `conventions.md`.

### Installation du protocole sur un persona

Le protocole H2A est installe via le **contexte** (`shared/orga/contextes/contexte-{persona}-{produit}.md`), pas via la fiche persona. La fiche persona definit le role (agnostique de l'instance). Le contexte installe les regles de l'instance.

Chaque contexte DOIT contenir une section `## Protocole H2A` qui :
- Pointe vers `shared/conventions.md` (a lire au premier boot, relire avant chaque artefact et fermeture)
- Rappelle les sections obligatoires du resume de session (Produit, Decisions, Notes deposees, Ouvert)
- Rappelle les sections observationnelles (Friction orchestrateur DEVRAIT, Flux PEUT)
- Rappelle la convention de commit
- Contient le **template friction inline** — le format exact attendu, directement visible dans le contexte

Sans cette section, le persona ne tracera pas la friction — c'est le cas d'usage le plus frequent d'ecart prescription/usage.

**Template friction inline** (a inclure dans chaque contexte) :

```
Format friction : {symbole} [{marqueur}] {description} — [{initiative}] → {resolution}
Marqueurs : ✓ [sound], ~ [contestable], ⚡ [simplification], ◐ [blind_spot], ✗ [refuted]
Initiative : [persona] ou [PO]
Resolution (DEVRAIT) : → ratified, → contested, → revised, → rejected
Lignage : si amende une friction anterieure, ajouter (ref: {id-source}/{index})
```

Le template est un filet de securite — le persona a le format sous les yeux au moment de produire, sans relire un fichier externe.

### Frontmatter

Tout artefact depose dans l'espace partage porte un frontmatter YAML. Pas d'accents dans les valeurs.

**Artefacts** :
```yaml
---
from: persona-emetteur
to: persona-destinataire
nature: signal           # signal | question | demande | reponse
status: new              # new | read | done
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

Quand un artefact passe a `status: done`, il est deplace dans `archives/` du repertoire parent.

### Statut du cycle de vie

| Status | Signification |
|--------|--------------|
| `new` | Depose, pas encore lu par le destinataire |
| `read` | Lu par le destinataire |
| `done` | Le destinataire a fait ce qu'il fallait avec |

> **Retrocompat** : le parser accepte aussi les valeurs FR (`nouveau`, `lu`, `traite`).

### Resolution des artefacts

Quand un artefact est traite, chaque point DEVRAIT porter un tag de resolution dans le corps du document (pas dans le frontmatter — un artefact contient souvent plusieurs points).

Convention : le destinataire annote chaque point avec `→ ratified`, `→ contested`, `→ revised` ou `→ rejected` avant archivage.

**Exemple** :
```markdown
## Proposition A
→ ratified

## Proposition B
→ rejected (justification courte)

## Proposition C
→ revised (precision sur ce qui change)
```

> **Retrocompat** : le parser accepte aussi les tags FR (`ratifie`, `conteste`, `revise`, `rejete`).

### Friction dans les resumes de session

Section `## Friction orchestrateur` (DEVRAIT — voir `exchange.md` §Sessions, couche observationnelle).

Chaque ligne porte les 5 dimensions definies dans `friction.md`, rendues ainsi :

```
## Friction orchestrateur
- [marqueur] description — [initiative] → resolution
```

**Marqueurs** : rendus en mots-cles entre crochets + symbole visuel dans les conventions d'instance.

| Protocole (`friction.md`) | Rendu Markdown |
|--------------------------|----------------|
| `[sound]` | ✓ ou `[sound]` |
| `[contestable]` | ~ ou `[contestable]` |
| `[simplification]` | ⚡ ou `[simplification]` |
| `[blind_spot]` | ◐ ou `[blind_spot]` |
| `[refuted]` | ✗ ou `[refuted]` |

> **Retrocompat** : le parser accepte aussi les brackets FR (`[juste]`, `[angle-mort]`, `[faux]`).

Les symboles visuels (✓/~/⚡/◐/✗) sont une commodite d'instance. Les mots-cles entre crochets font foi pour l'audit.

**Initiative** : `[persona]` ou `[PO]` — qui a initie le sujet de friction.

**Resolution** : tag de geste epistemique apres la fleche `→`. Voir `protocol/friction.md` §Resolution.

| Protocole (`friction.md`) | Rendu Markdown |
|--------------------------|----------------|
| `ratified` | `→ ratified` |
| `contested` | `→ contested` |
| `revised` | `→ revised` |
| `rejected` | `→ rejected` |

Le tag de resolution est pose par point de friction, pas par section.

**Exemple** :
```
## Friction orchestrateur
- ✓ [sound] le mapping Toulmin eclaire sans contraindre — [PO] → ratified
- ~ [contestable] le mapping Toulmin est suggestif, pas acquis — [PO] → revised
- ◐ [blind_spot] scaffolding absent de la review Böckeler — [aurele] → ratified
```

### Lignage (dimension `antecedent`)

Quand une friction amende une friction anterieure (voir `protocol/friction.md` §Lignage), la dimension `antecedent` est materialisee par un champ `ref:` en fin de ligne :

```
- ✓ [sound] la distinction protocolaire/observationnelle couvre le cas — [aurele] → ratified (ref: 2026-04-10-1430-aurele/3)
```

**Format** : `ref: {id-source}/{index}` ou :
- `{id-source}` = nom du fichier (sans extension) — resume de session ou artefact
- `{index}` = position de la friction dans le fichier source (1-based, ordre d'apparition)

**Regles d'implementation** :
- Le parser DOIT suivre les `ref:` et propager la resolution du dernier maillon vers la friction source.
- Une friction referencee par un `ref:` n'apparait pas dans la liste des frictions ouvertes si le maillon qui la reference porte une resolution.
- Les compteurs comptent la friction logique une seule fois, avec le marqueur d'origine et la resolution finale.

Les dimensions `echange` et `emetteur` sont implicites : l'echange est la session courante, l'emetteur est le persona auteur du resume.

### reportPattern dans les resumes de session

Section `## reportPattern` (PEUT — couche observationnelle pour le constat, protocolaire pour le compteur).

Le persona consigne le declenchement et le choix de l'orchestrateur :

```
## reportPattern
- Theme : [theme] — N frictions rejetees (sessions YYYY-MM-DD, ...)
- Choix : erreur LLM | conviction | resistance
- Justification : ...
```

L'audit compte les declenchements et la distribution des choix (compteur protocolaire).

### Contribution dans les resumes de session

Section `## Flux` (PEUT — voir `exchange.md` §Sessions, couche observationnelle).

Chaque ligne porte les dimensions definies dans `contribution.md`, rendues ainsi :

```
## Flux
- {direction}:{type} — description
```

**Direction** : `H` (humain apporte) ou `A` (assistant apporte).
**Type** : `substance`, `structure`, `contestation`, `decision`.

**Comptage** (optionnel) : une ligne de synthese en fin de section.

**Exemple** :
```
## Flux
- H:substance — article Böckeler, demande d'avis
- A:substance — filiation scaffolding absente chez Böckeler
- A:structure — trois niveaux de complementarite harness/SOFIA
- H:decision — on garde la notation mots-cles

H:2 (substance 1, decision 1) | A:2 (substance 1, structure 1)
```

La dimension `session` est implicite : c'est la session courante.

### Operations — implementation filesystem

Mapping des operations H2A (voir `protocol/h2a.md`) sur l'implementation courante.

| Operation | Mode | Geste concret |
|-----------|------|--------------|
| openSession() | manuel | L'orchestrateur lance un terminal dans le workspace du persona (ou reprend une session Claude Code existante) |
| closeSession() | manuel | L'orchestrateur donne le signal. Le persona **relit `shared/conventions.md`**, puis produit le resume, prepare le commit. L'orchestrateur execute le commit |
| depositArtefact() | manuel | L'orchestrateur instruit le persona. Le persona **relit `shared/conventions.md`**, puis produit l'artefact (note, review, feature) et depose dans `shared/` |
| routeArtefact() | manuel | L'orchestrateur lit l'artefact dans `shared/`, ouvre une session avec le destinataire, lui presente l'artefact. **Cross-instance** : l'orchestrateur depose l'artefact dans `shared/` de l'instance du destinataire, pas de l'emetteur |
| markRead() | manuel | L'orchestrateur met `status: read` dans le frontmatter de l'artefact |
| markDone() | manuel | L'orchestrateur met `status: done` dans le frontmatter — l'artefact est ensuite deplace dans `archives/` |
| qualifyFriction() | automatique | Le persona pre-remplit la section `## Friction orchestrateur` a la fermeture. L'orchestrateur valide ou corrige |
| qualifyContribution() | automatique | Le persona pre-remplit la section `## Flux` a la fermeture. L'orchestrateur valide ou corrige |
| reportPattern() | automatique | Le persona detecte une convergence thematique de rejets en cours de session. Il interpelle l'orchestrateur avec le constat + 3 hypotheses argumentees. L'orchestrateur repond avec son choix + justification. A la fermeture, le persona consigne dans une section `## reportPattern` du resume |

**Manuel** = l'orchestrateur declenche par un geste explicite.
**Automatique** = le persona produit a la fermeture de session, l'orchestrateur valide.

Le persona NE DOIT PAS fermer de lui-meme ni deposer d'artefact sans instruction de l'orchestrateur.

### Outillage

| Outil | Role |
|-------|------|
| `implementation/filesystem/audit-instance.py` | Verifie la conformite d'une instance au protocole |
| `implementation/filesystem/create-instance.py` | Scaffolde une nouvelle instance |
| `sofia.md` | Persona meta — instancie, audite. Operatrice du protocole |

---

## Ce qui est implementation vs protocole

| Element | Protocole (h2a.md) | Implementation (ce doc) |
|---------|--------------------|-----------------------|
| "Chaque session produit une trace" | ✓ | |
| "La trace est un fichier .md commite dans git" | | ✓ |
| "Les marqueurs sont [sound] [contestable] etc." | ✓ | |
| "Les marqueurs sont dans un fichier Markdown" | | ✓ |
| "L'espace partage est le seul canal" | ✓ | |
| "L'espace partage est un dossier shared/" | | ✓ |
| "L'instance est identifiable" | ✓ | |
| "L'instance est identifiee par un fichier sofia.md" | | ✓ |
| "La friction porte 5 dimensions" | ✓ | |
| "La friction est une ligne Markdown avec symbole + mot-cle + initiative" | | ✓ |
| "La contribution porte direction et type" | ✓ | |
| "La contribution est une ligne `{H\|A}:{type} — description`" | | ✓ |
| "La friction porte un tag de resolution" | ✓ | |
| "Le tag de resolution est rendu `→ ratified` en fin de ligne Markdown" | | ✓ |
| "Une resolution peut evoluer entre sessions avec ref:" | ✓ | |
| "Le ref: est rendu `(ref: id-session/n)` en fin de ligne Markdown" | | ✓ |
| "reportPattern() produit un constat + 3 hypotheses + qualification" | ✓ | |
| "reportPattern est une section `## reportPattern` dans le resume" | | ✓ |
| "Le compteur de choix reportPattern est auditable" | ✓ | |

---

## Perspectives

### API HTTP

H2A pourrait etre implemente comme une API REST :
- Chaque entite (Instance, Espace, Persona, Echange, Friction, Contribution) devient une ressource
- Les frontmatter YAML deviennent des schemas JSON
- Les statuts (`new` → `read` → `done`) deviennent des transitions d'etat
- L'audit devient un endpoint de verification

### Base de donnees

Les resumes de session, artefacts et marqueurs de friction pourraient vivre dans une base relationnelle ou documentaire. L'historique git serait remplace par un log d'evenements.

### Interoperabilite MCP / A2A

H2A couvre la couche humain-assistant. MCP et A2A couvrent les couches agent-outils et agent-agent. Un systeme complet pourrait combiner les trois :
- H2A pour la coordination humain-assistants
- MCP pour l'acces aux ressources par les assistants
- A2A pour la coordination inter-assistants (si l'invariant de routage humain est assoupli)

### Wire format

Si H2A evolue vers un protocole technique, il faudra definir un wire format (JSON, protobuf, etc.) et une spec d'interoperabilite. Ce n'est pas dans le scope actuel.
