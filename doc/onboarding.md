# Onboarding d'un nouveau persona

> Comment integrer un nouveau persona dans une instance Voix existante.

---

## Quand ajouter un persona ?

Un persona se justifie quand :
- Un **domaine** emerge que personne ne couvre correctement
- Deux personas existants sont en **tension** sur un sujet recurrent
- Le PO passe du temps a faire un travail qu'un persona pourrait structurer

Un persona ne se justifie **pas** quand :
- C'est une tache, pas un role (utilise une note ou un backlog item)
- Le domaine est couvert mais "pas assez bien" (ameliore le persona existant)

## Etapes

### 1. Definir le role

Avant de nommer le persona, definir :
- **Quoi** — quels types de livrables il produit
- **Pas quoi** — ce qu'il ne fait explicitement pas (le plus important)
- **Avec qui** — ses interactions principales

### 2. Creer la fiche persona

Utiliser le template `core/templates/persona.md`. Champs cles :
- Profil, posture, domaines d'intervention
- Collaboration (tableau avec/mode)
- Ce qu'il ne fait pas

### 3. Creer le workspace

```
{instance}/
└── {workspace}/
    ├── CLAUDE.md      ← genere depuis core/templates/workspace/CLAUDE.md
    ├── backlog.md     ← genere depuis core/templates/backlog.md
    └── sessions/      ← vide, le persona ecrira son premier resume
```

Le CLAUDE.md doit contenir :
- Persona + lien vers la fiche
- Perimetre + documents cles
- Isolation (lecture/ecriture autorisees)
- Workflow (ouverture/fermeture de session)
- Conventions du projet

### 4. Briefer le persona

A la premiere session, le persona doit :
1. Lire sa fiche persona
2. Lire les documents cles de son domaine
3. Scanner `shared/notes/` pour d'eventuels messages
4. Deposer un premier resume de session

### 5. Presenter au reste de l'equipe

Deposer une note dans `shared/notes/` :

```
note-equipe-nouveau-persona-{auteur}.md
```

Contenu : qui, pourquoi, quel perimetre, avec qui il interagit.
Les autres personas le decouvriront a leur prochaine ouverture de session.

## Exemple : onboarding Sofia (Katen, mars 2026)

Sofia a ete onboardee par Nora (UX) :
1. Fiche persona definie avec posture "le detail fait le produit"
2. Workspace `graphisme/` cree avec CLAUDE.md specifique
3. Brief : liste de lecture ciblee (design-principles, design-system, feature-v022)
4. Premiere session : exploration visuelle, planche de reference v1

Le brief etait un document dedie (`onboarding-sofia.md`) — court, ordonne,
avec des renvois vers les docs existants plutot que du contenu duplique.

## Anti-patterns

- **Le persona fourre-tout** — "il fait un peu de tout". Si tu ne peux pas
  dire ce qu'il ne fait pas, il n'est pas calibre.
- **Le persona orphelin** — aucune interaction avec les autres. Un persona
  isole ne genere pas de friction utile.
- **Le persona miroir** — il fait la meme chose qu'un autre avec un nom
  different. Fusionne plutot que de dedoubler.
