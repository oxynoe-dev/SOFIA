# Isolation par workspace

> Un persona = un workspace = un périmètre = un CLAUDE.md.

---

## Le principe

Chaque persona vit dans son propre espace de travail. Il a ses
fichiers, ses instructions, ses conventions, et ses limites.
Il ne peut pas lire ou écrire partout.

L'isolation n'est pas une contrainte technique — c'est ce qui
**force** le persona à rester dans son rôle.

## Pourquoi isoler ?

### Empêcher la dérive de scope

Un persona sans frontières finit par tout faire. L'architecte qui
a accès au code finit par coder. Le stratège qui peut lire les tests
finit par donner des avis techniques.

L'isolation rend la dérive impossible : le persona ne **voit** pas
ce qui est hors de son périmètre.

### Forcer les échanges formels

Si l'architecte ne peut pas modifier le code, il est obligé de
produire une spec que le dev pourra lire. Si le dev ne peut pas
modifier l'architecture, il est obligé de déposer un signalement
de friction.

L'isolation crée le besoin d'artefacts d'échange.

### Protéger le travail en cours

Un persona ne peut pas casser accidentellement le travail d'un
autre. L'UX ne va pas reformater du code. Le dev ne va pas
réécrire une review de design.

## Structure type

```
projet/
├── architecture/          ← workspace architecte
│   ├── CLAUDE.md          ← instructions pour ce persona
│   ├── sessions/          ← résumés de session
│   └── doc/               ← specs, ADR, audits
│
├── dev/                   ← workspace dev
│   ├── CLAUDE.md
│   ├── sessions/
│   └── ...
│
├── ux/                    ← workspace UX
│   ├── CLAUDE.md
│   ├── sessions/
│   └── ...
│
└── shared/                ← zone d'échange
    ├── review/            ← reviews croisées
    └── notes/             ← notes inter-personas
```

## La zone partagée

Les personas communiquent via un dossier partagé (`shared/`).
C'est le seul espace que tous les personas peuvent lire et écrire.

Conventions :
- **Reviews** : `review-<sujet>-<auteur>.md` — déposées dans `shared/review/`
- **Notes** : `note-<destinataire>-<sujet>-<auteur>.md` — déposées dans `shared/notes/`

Le dossier partagé est le "couloir" du bureau. On y dépose des
documents, on ne s'y installe pas.

## Le CLAUDE.md comme gardien

Le fichier `CLAUDE.md` à la racine de chaque workspace contient :

1. **Qui** — quel persona, quelle posture
2. **Quoi** — périmètre d'intervention, livrables attendus
3. **Où** — quels fichiers/dossiers sont accessibles
4. **Interdit** — ce qui est hors périmètre (lecture ET écriture)
5. **Comment** — conventions, formats, workflow

Voir `claude-code/claude-md.md` pour l'anatomie detaillee.

## Multi-instance : le cas du dev

Certains personas travaillent sur **deux repos** — leur workspace
d'analyse (dans l'instance) et un repo produit separe. C'est le cas
typique du dev : il planifie dans `instance/dev/` et code dans `produit/`.

### Structure

```
instance/                       ← repo instance (experiments/)
├── dev/                        ← workspace dev (sessions, backlog, plans)
│   ├── CLAUDE.md
│   ├── sessions/
│   └── backlog.md
└── shared/                     ← bus d'echange

produit/                        ← repo produit (katen/)
├── CLAUDE.md                   ← instructions dev completes
├── src/
└── tests/
```

### Regles

- Le **CLAUDE.md du repo produit** est l'entree principale du dev — c'est
  la que vivent les conventions de code, l'architecture, le processus de version.
- Le **workspace dev/ dans l'instance** contient les sessions, le backlog,
  et les plans — pas du code.
- Les commits instance = auto (`{persona}: {resume} ({date})`).
  Les commits produit = PO execute.
- Le dev lit `shared/notes/` et `shared/review/` au meme titre que
  les autres personas — c'est dans son workflow d'ouverture.

### Pourquoi separer ?

Le code versionne est un livrable public. Les sessions et plans sont
de l'outillage interne. Les mettre ensemble :
- Expose l'historique d'analyse dans le repo public
- Melange les commits de code et les commits de session
- Casse l'isolation si le repo produit est ouvert par un autre outil
