# Onboarding d'un nouveau persona

> Comment intégrer un nouveau persona dans une instance SOFIA existante.

---

## Quand ajouter un persona ?

Un persona se justifie quand :
- Un **domaine** émerge que personne ne couvre correctement
- Deux personas existants sont en **tension** sur un sujet récurrent
- L'orchestrateur passe du temps à faire un travail qu'un persona pourrait structurer

Un persona ne se justifie **pas** quand :
- C'est une tâche, pas un rôle (utilise une note ou un backlog item)
- Le domaine est couvert mais "pas assez bien" (améliore le persona existant)

## Étapes

### 1. Définir le rôle

Avant de nommer le persona, définir :
- **Quoi** — quels types de livrables il produit
- **Pas quoi** — ce qu'il ne fait explicitement pas (le plus important)
- **Avec qui** — ses interactions principales

### 2. Créer la fiche persona

S'inspirer du format `instance/artefacts/persona.md` et des archétypes dans `instance/archetypes/`. Champs clés :
- Profil, posture, domaines d'intervention
- Collaboration (tableau avec/mode)
- Ce qu'il ne fait pas

### 3. Créer le workspace

```
{instance}/
├── shared/orga/
│   ├── personas/persona-{nom}.md       ← fiche persona (rôle, posture, interdits)
│   └── contextes/contexte-{nom}-{produit}.md  ← contexte workspace (docs, isolation, workflow)
└── {workspace}/
    ├── CLAUDE.md      ← aiguillage runtime (2 lignes → persona + contexte)
    └── sessions/      ← vide, le persona écrira son premier résumé
```

Le CLAUDE.md est un aiguillage de 2 lignes (voir `runtime/claude-code/claude-md.md`). Le contenu vit dans deux fichiers :
- **persona-{nom}.md** — rôle, posture, interdits, collaboration (template : `instance/artefacts/persona.md`)
- **contexte-{nom}-{produit}.md** — périmètre, documents clés, isolation, workflow (template : `instance/artefacts/contexte-persona-produit.md`)

### 4. Briefer le persona

À la première session, le persona doit :
1. Lire sa fiche persona
2. Lire les documents clés de son domaine
3. Scanner `shared/notes/` pour d'éventuels messages
4. Déposer un premier résumé de session

### 5. Présenter au reste de l'équipe

Déposer une note dans `shared/notes/` :

```
note-equipe-nouveau-persona-{auteur}.md
```

Contenu : qui, pourquoi, quel périmètre, avec qui il interagit.
Les autres personas le découvriront à leur prochaine ouverture de session.

## Exemple : onboarding Sofia (Katen, mars 2026)

Sofia a été onboardée par Nora (UX) :
1. Fiche persona définie avec posture "le détail fait le produit"
2. Workspace `graphisme/` créé avec CLAUDE.md spécifique
3. Brief : liste de lecture ciblée (design-principles, design-system, feature-v022)
4. Première session : exploration visuelle, planche de référence v1

Le brief était un document dédié (`onboarding-sofia.md`) — court, ordonné,
avec des renvois vers les docs existants plutôt que du contenu dupliqué.

## Anti-patterns

- **Le persona fourre-tout** — "il fait un peu de tout". Si tu ne peux pas
  dire ce qu'il ne fait pas, il n'est pas calibré.
- **Le persona orphelin** — aucune interaction avec les autres. Un persona
  isolé ne génère pas de friction utile.
- **Le persona miroir** — il fait la même chose qu'un autre avec un nom
  différent. Fusionne plutôt que de dédoubler.
