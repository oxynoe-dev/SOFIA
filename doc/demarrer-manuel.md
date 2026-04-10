# Démarrer sans Sofia — mode manuel

> Installer les personas à la main, fichier par fichier.

---

## Quand utiliser le mode manuel

- Tu veux comprendre chaque pièce avant de l'assembler
- Tu as déjà une idée précise des rôles dont tu as besoin
- Tu préfères garder le contrôle sur la structure
- Tu veux adapter la méthode à un autre provider

Le mode manuel produit exactement le même résultat que Sofia. Il n'y a pas de version "allégée" — juste un chemin différent pour y arriver.

---

## Vue d'ensemble

```
mon-projet/
├── voix.md                  ← marqueur d'instance
├── shared/
│   ├── conventions.md       ← règles d'échange
│   ├── orga/
│   │   └── personas/        ← fiches persona
│   ├── notes/               ← échanges inter-personas
│   ├── review/              ← reviews croisées
│   └── roadmap-{produit}.md ← planification
├── {workspace-1}/
│   ├── CLAUDE.md            ← contrat du persona
│   └── sessions/            ← résumés de session
├── {workspace-2}/
│   ├── CLAUDE.md
│   └── sessions/
└── ...
```

---

## Avant de commencer : instance et projet

Une instance SOFIA n'est pas ton projet — c'est l'atelier où les personas réfléchissent. Le projet (code, produit) vit dans un repo séparé. Voir la section [L'isolation > Instance et projet](utilisateur.md#instance-et-projet) du guide utilisateur pour le détail et les trois configurations possibles.

---

## Étape 1 — Cloner le repo SOFIA

```bash
git clone https://github.com/oxynoe-dev/sofia
```

C'est ta référence. Les templates et la documentation sont dedans. Tu n'as pas besoin de le garder dans ton projet — juste de le consulter.

---

## Étape 2 — Créer le marqueur d'instance

À la racine de ton projet, crée `voix.md` :

```markdown
# Instance SOFIA

Ce dépôt est une **instance de la méthode SOFIA**.

- **Méthode** : [oxynoe-dev/sofia](https://github.com/oxynoe-dev/sofia)
- **Version méthode appliquée** : v0.2.x
- **Projet** : {ton projet}
- **Équipe** : {nombre} assistants IA + 1 humain orchestrateur

## Structure instance

| Dossier | Rôle | Persona |
|---------|------|---------|
| `{workspace}/` | {description} | {persona} |
| `shared/` | Bus d'échange inter-personas | Partagé |
```

---

## Étape 3 — Créer la structure partagée

```bash
mkdir -p shared/orga/personas shared/notes shared/review
```

### conventions.md

Crée `shared/conventions.md`. C'est le contrat d'échange entre personas. Au minimum :

```markdown
# Conventions

## Échanges inter-personas

Les personas ne se parlent pas. Ils échangent par artefacts déposés dans shared/.

### Notes
- Format : `note-{destinataire}-{sujet}-{auteur}.md`
- Emplacement : `shared/notes/`
- Quand traitée : déplacer dans `shared/notes/archives/`

### Reviews
- Format : `review-{sujet}-{auteur}.md`
- Emplacement : `shared/review/`
- Quand traitée : déplacer dans `shared/review/archives/`

## Commits
- Instance : `{persona}: {résumé court} ({date})`
- Repos produit : l'orchestrateur vérifie et commit
```

---

## Étape 4 — Définir ton premier persona

Commence par **un seul**. Les autres viendront.

### Choisir le rôle

| Ton contexte | Premier persona |
|--------------|-----------------|
| Solo dev, code désorganisé | Architecte |
| Équipe, pas de specs | Lead produit |
| Solo dev, design prioritaire | Design system lead |
| Data/ML, pipeline flou | Data architect |

Le premier persona est un rôle **structurant** — celui qui va cadrer la démarche.

### Créer la fiche persona

Crée `shared/orga/personas/persona-{nom}.md`. S'inspirer du format `instance/artefacts/persona.md` et des archétypes dans `instance/archetypes/`. Les champs essentiels :

```markdown
# {Nom} — {Rôle}

## Profil
{En une phrase : qui est ce persona et quelle est sa posture.}

## Domaines d'intervention
- {domaine 1}
- {domaine 2}

## Ce qu'il/elle ne fait PAS
- {interdit 1}
- {interdit 2}

## Ce qu'il/elle challenge
- {axe de friction 1}
```

La section "Ce qu'il ne fait pas" est **la plus importante**. C'est elle qui crée la contrainte productive.

---

## Étape 5 — Créer le workspace

```bash
mkdir -p {workspace}/sessions
```

### Le CLAUDE.md

Crée `{workspace}/CLAUDE.md`. C'est le fichier que Claude Code lit à chaque conversation. Vise 60-100 lignes.

```markdown
# {Projet} — Instructions Claude Code

## Persona
Claude incarne **{Nom}** — {rôle}.
Voir `shared/orga/personas/persona-{nom}.md` pour la fiche complète.

## Posture
- {comportement 1 — comment il s'exprime}
- {comportement 2 — ce qu'il privilégie}
- {comportement 3 — son rapport aux autres}

## Périmètre
Ce workspace contient :
- {type de contenu}

## Documents clés
| Fichier | Rôle |
|---------|------|
| `{chemin}` | {description} |

## Isolation
- Ne jamais lire/écrire en dehors de `{périmètre autorisé}`

## Conventions
- **Langue** : français
- **Reviews** : `review-<sujet>-{nom}.md` dans `shared/review/`
- **Bus shared/** : voir `shared/conventions.md`

## Workflow
0. **Ouverture** : lire le dernier résumé dans `sessions/`
1. Lire les documents existants avant toute intervention
2. Produire des {types de livrables}
3. Ne pas {interdit principal}

## Émergence
Quand tu deflectes une question parce qu'elle sort de ton périmètre, note le domaine. Si tu deflectes 3+ fois sur le même domaine, signale-le :
"Je reçois régulièrement des questions sur [domaine] — c'est en dehors de mon périmètre. Ce sujet relève d'un autre persona."

## Résumé de session — obligatoire
- `sessions/{YYYY-MM-DD}-{HHmm}-{nom}.md`
- Sections : Produit, Décisions, Notes déposées, Ouvert
- Pas de prose, 30 lignes max
```

---

## Étape 6 — Première session

Lance Claude Code dans le workspace :

```bash
cd {workspace}
claude
```

Le persona va lire son CLAUDE.md et se comporter selon le contrat. Demande-lui quelque chose dans son périmètre. Observe :

- **Il refuse ce qui est hors périmètre ?** Bon signe.
- **Il accepte tout ?** Resserre les contraintes dans le CLAUDE.md.
- **Il est trop rigide ?** Assouplis la posture.

Le calibrage se fait en 2-3 sessions. C'est normal.

---

## Ajouter un deuxième persona

Quand le besoin émerge — pas avant. Les signaux :

- Le premier persona te dit régulièrement "ce n'est pas mon rôle"
- Tu passes du temps à faire un travail qu'un persona pourrait structurer
- Deux domaines distincts sont en tension

Reprends à l'étape 4. Crée la fiche, crée le workspace, lance une première session.

---

## Checklist

- [ ] `voix.md` à la racine
- [ ] `shared/conventions.md`
- [ ] `shared/orga/personas/persona-{nom}.md`
- [ ] `{workspace}/CLAUDE.md` (60-100 lignes)
- [ ] `{workspace}/sessions/`
- [ ] Première session lancée
- [ ] Le persona dit "non" quand il faut
