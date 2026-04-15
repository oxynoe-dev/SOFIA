# Conventions

> Conventions de cette instance. Completer selon les besoins du projet.

---

## Structure

> A maintenir au fil de l'eau. Quand un nouveau repertoire apparait dans `shared/` (notes/, review/, etc.), l'ajouter ici pour que les personas sachent ou chercher et ou deposer.

```
instance/
├── sofia.md
├── shared/
│   ├── conventions.md
│   └── orga/
│       ├── personas/
│       └── contextes/
├── {espace}/
│   ├── CLAUDE.md
│   └── sessions/
└── ...
```

---

## Sessions

### Resume de session

A chaque fermeture, le persona cree un fichier dans `{espace}/sessions/` :

```
{YYYY-MM-DD}-{HHmm}-{persona}.md
```

Le `HHmm` est l'heure de la cloture (pas du boot).

### Frontmatter session

```yaml
---
persona: nom-persona
date: YYYY-MM-DD
session: "HHmm"
---
```

### Sections protocolaires (DOIT)

| Section | Contenu |
|---------|---------|
| `## Produit` | Fichiers crees ou modifies |
| `## Decisions` | Choix retenus |
| `## Notes deposees` | Artefacts deposes dans shared/ |
| `## Ouvert` | Questions non resolues |

Pas de prose — listes courtes. 30 lignes max.

### Sections observationnelles

| Section | Statut | Contenu |
|---------|--------|---------|
| `## Friction orchestrateur` | DEVRAIT | Frictions qualifiees |
| `## Flux` | PEUT | Apports epistemiques |

## Commits

```
{persona}: {resume court} ({date})
```

Un commit par session.

---

## Artefacts

Tout artefact depose dans `shared/` porte un frontmatter YAML. Pas d'accents dans les valeurs.

```yaml
---
de: persona-emetteur
pour: persona-destinataire
nature: signal           # signal | question | demande | reponse
statut: nouveau          # nouveau | lu | traite
date: YYYY-MM-DD
---
```

### Cycle de vie

| Statut | Signification |
|--------|--------------|
| `nouveau` | Depose, pas encore lu par le destinataire |
| `lu` | Lu par le destinataire |
| `traite` | Traite par le destinataire |

### Resolution

Quand un artefact est traite, chaque point DEVRAIT porter un tag de resolution dans le corps du document :

`→ ratifie` | `→ conteste` | `→ revise` | `→ rejete`

---

## Friction

Chaque ligne porte : marqueur + description + initiative + resolution.

```
- [marqueur] description — [initiative] → resolution
```

### Marqueurs

5 positions epistemiques. Ensemble ferme — ne pas en ajouter.

| Symbole | Marqueur | Signification |
|---------|----------|--------------|
| ✓ | `[juste]` | Corroboration — position correcte |
| ~ | `[contestable]` | Sous-determination — defendable mais pas la seule lecture |
| ⚡ | `[simplification]` | Reductionnisme — le reel est plus complexe |
| ◐ | `[angle-mort]` | Incompletude — donnees manquantes |
| ✗ | `[faux]` | Refutation — factuellement incorrect ou incoherent |

Les mots-cles entre crochets font foi pour l'audit.

### Initiative

`[persona]` ou `[PO]` — qui a initie le sujet de friction.

### Resolution

| Tag | Signification |
|-----|---------------|
| `ratifie` | Accord — la position est acceptee |
| `conteste` | Desaccord maintenu — pas de changement de position |
| `revise` | Desaccord avec changement de position |
| `rejete` | Desaccord terminal — la position est ecartee |

Un tag par point de friction.

### Mutabilite inter-sessions

Une resolution peut evoluer dans une session ulterieure. La friction DEVRAIT porter un champ `ref:` pointant vers la friction d'origine :

```
- ✓ [juste] description — [persona] → ratifie (ref: 2026-04-10-1430-persona/3)
```

### Lecture rapide

- Que des ✓ → friction absente — signal d'alerte
- Mix ✓/~/⚡ → friction saine
- Presence de ◐ ou ✗ → tension a traiter
- Absence de resolution → frictions non denouees, a traiter ou reporter dans Ouvert

---

## Contribution (flux epistemique)

Section `## Flux` — optionnelle.

```
- {direction}:{type} — description
```

| Direction | Signification |
|-----------|--------------|
| `H` | L'humain (orchestrateur) apporte |
| `A` | L'assistant (persona) apporte |

| Type | Definition |
|------|-----------|
| `matiere` | Information nouvelle |
| `structure` | Mise en forme, categorisation, synthese |
| `contestation` | Remise en question, contre-exemple |
| `decision` | Arbitrage, choix retenu |

Comptage optionnel en fin de section.
