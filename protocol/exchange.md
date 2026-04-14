# Exchange

> Sessions et artefacts — tout passe par l'orchestrateur.

---

## Principe

Tout echange entre l'orchestrateur et un persona est soit une **session** (synchrone), soit un **artefact** (depot asynchrone). Les personas ne communiquent jamais directement — l'orchestrateur est le routeur unique.

Principe source : `core/principes.md` — l'orchestrateur arbitre toutes les decisions ; `core/modele.md` — l'echange est une entite constitutive.

## Dimensions communes

Tout echange (session ou artefact) porte :

| Dimension | Valeurs | Obligatoire |
|-----------|---------|-------------|
| **instance** | Reference a l'instance | DOIT |
| **espace** | Espace du persona concerne | DOIT |
| **date_heure** | Date et heure de l'echange | DOIT |

La distinction session / artefact est structurelle — une session est synchrone, un artefact est un depot asynchrone.

Tout echange genere 0..* frictions (voir `friction.md`) et 0..* contributions (voir `contribution.md`).

---

## Sessions

### Principe

Une session est le mecanisme principal d'interaction humain-assistant. L'orchestrateur initie, le persona produit, l'orchestrateur cloture.

### Definition

Une session est un echange synchrone entre l'orchestrateur et un persona.

### Dimensions specifiques

| Dimension | Valeurs | Obligatoire |
|-----------|---------|-------------|
| **persona** | Identifiant du persona | DOIT |
| **identifiant** | Unique | DOIT |

### Cycle de vie

1. **Ouverture** — l'orchestrateur initie la session. Le persona DOIT consulter la derniere trace de session de son espace avant toute intervention.
2. **Echange** — dialogue libre. L'orchestrateur apporte du contexte, des directives, des artefacts d'autres personas. Le persona produit dans son perimetre.
3. **Fermeture** — le persona DOIT produire un resume structure avant cloture.

### Resume de session

Chaque session DOIT produire une trace identifiable portant les dimensions ci-dessus.

#### Sections protocolaires (DOIT)

Couche protocolaire — contenu deterministe et verifiable.

| Section | Contenu |
|---------|---------|
| Produit | Liste des artefacts crees ou modifies |
| Decisions | Choix retenus pendant la session |
| Notes deposees | Artefacts deposes dans l'espace partage |
| Ouvert | Questions non resolues, items en attente |

Chaque section DOIT etre presente. Si rien a reporter : "Aucun".

Contraintes :
- Pas de prose — listes courtes uniquement.
- 30 lignes max pour l'ensemble du resume.

#### Sections observationnelles (DEVRAIT / PEUT)

Couche observationnelle — contenu inferentiel, soumis a validation humaine.

| Section | Contenu | Statut |
|---------|---------|--------|
| Friction | Frictions qualifiees (voir `friction.md`) | DEVRAIT |
| Flux | Apports epistemiques (voir `contribution.md`) | PEUT |

Le persona pre-remplit ces sections. L'orchestrateur PEUT corriger, completer ou supprimer le contenu.

### Tracabilite

Chaque session DOIT produire une trace identifiable. Le mecanisme de persistance est defini dans `implementation/implementation.md`.

---

## Artefacts

### Principe

Les personas ne communiquent jamais directement. Tout echange inter-personas transite par l'orchestrateur via l'espace partage.

### Definition

Un artefact est un depot asynchrone dans l'espace partage par un persona, a destination d'un autre persona ou de l'equipe.

### Dimensions specifiques

| Dimension | Valeurs | Obligatoire |
|-----------|---------|-------------|
| **emetteur** | Persona qui depose l'artefact | DOIT |
| **destinataire** | Persona ou `equipe` | DOIT |
| **nature** | `signal`, `question`, `demande`, `reponse` | DOIT |
| **statut** | `nouveau` → `lu` → `traite` | DOIT |

Le champ `nature` DOIT utiliser l'un des 4 types ci-dessus. Le champ `statut` DOIT suivre le cycle de vie indique.

### Friction dans les artefacts

Un artefact PEUT porter des marqueurs de friction (voir `friction.md`). C'est le cas typique des reviews et des notes qui prennent position sur le travail d'un autre persona.

Les marqueurs suivent le meme format que dans les sessions : marqueur, description, tag d'initiative. L'emetteur de l'artefact est l'emetteur de la friction.

### Contribution dans les artefacts

Un artefact PEUT porter des contributions (voir `contribution.md`). C'est le cas typique des reviews et des notes qui impliquent un apport des deux parties : l'orchestrateur apporte la matiere source (`[H]`), le persona apporte l'analyse (`[A]`). La direction `[H]`/`[A]` s'applique comme dans les sessions — l'artefact est produit pendant une session.

### Routage

1. Persona A depose un artefact dans l'espace partage (`statut: nouveau`)
2. L'orchestrateur lit l'artefact et decide de le router
3. L'orchestrateur ouvre une session avec Persona B et lui presente l'artefact (`statut: lu`)
4. Persona B traite et PEUT deposer une reponse (`nature: reponse`)
5. L'artefact original passe a `statut: traite`

L'orchestrateur DOIT etre le routeur de tous les echanges. Un persona NE DOIT PAS consulter directement un artefact qui ne lui est pas destine.

### Archivage

Quand un artefact passe a `statut: traite`, il DEVRAIT etre archive. Le mecanisme d'archivage est defini dans `implementation/implementation.md`.
