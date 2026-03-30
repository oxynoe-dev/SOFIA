# Marqueur d'instance

> Un fichier `voix.md` a la racine identifie un depot comme instance Voix.

---

## Le principe

Quand un depot suit la methode Voix, il contient un fichier `voix.md`
a sa racine. Ce fichier est le **marqueur d'instance** — il lie le depot
a la methode et documente sa structure specifique.

## Contenu type

```markdown
# Instance Voix

Ce depot est une **instance de la methode Voix**.

- **Methode** : [oxynoe-dev/voix](https://github.com/oxynoe-dev/voix)
- **Version methode appliquee** : v0.2.x
- **Projet** : {nom du projet}
- **Equipe** : {nombre} assistants IA specialises + {nombre} PO humain(s)

## Structure instance

| Dossier | Role | Persona |
|---------|------|---------|
| `{workspace}/` | {description} | {persona} |
| `shared/` | Bus d'echange inter-personas | Partage |

## Conventions

Voir `shared/conventions.md`.
```

## Pourquoi

- **Identification** — en ouvrant un depot, on sait immediatement
  si c'est une instance Voix et quelle version de la methode il suit.
- **Lien vers la source** — le lien vers le repo Voix permet de
  retrouver la documentation complete.
- **Cartographie** — la table des workspaces donne la vue d'ensemble
  sans lire tous les CLAUDE.md.

## Convention

- Le fichier s'appelle `voix.md` (pas `VOIX.md`, pas `.voix`)
- Il vit a la racine du depot instance
- Il est committe (pas gitignored)
