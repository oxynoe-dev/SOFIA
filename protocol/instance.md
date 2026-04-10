# Marqueur d'instance

> Un fichier `voix.md` à la racine identifie un dépôt comme instance SOFIA.

---

## Le principe

Quand un dépôt suit la méthode SOFIA, il contient un fichier `voix.md`
à sa racine. Ce fichier est le **marqueur d'instance** — il lie le dépôt
à la méthode et documente sa structure spécifique.

## Contenu type

```markdown
# Instance SOFIA

Ce dépôt est une **instance de la méthode SOFIA**.

- **Méthode** : [oxynoe-dev/sofia](https://github.com/oxynoe-dev/sofia)
- **Version méthode appliquée** : v0.2.x
- **Projet** : {nom du projet}
- **Équipe** : {nombre} assistants IA spécialisés + {nombre} orchestrateur(s) humain(s)

## Structure instance

| Dossier | Rôle | Persona |
|---------|------|---------|
| `{workspace}/` | {description} | {persona} |
| `shared/` | Bus d'échange inter-personas | Partagé |

## Conventions

Voir `shared/conventions.md`.
```

## Pourquoi

- **Identification** — en ouvrant un dépôt, on sait immédiatement
  si c'est une instance SOFIA et quelle version de la méthode il suit.
- **Lien vers la source** — le lien vers le repo SOFIA permet de
  retrouver la documentation complète.
- **Cartographie** — la table des workspaces donne la vue d'ensemble
  sans lire tous les CLAUDE.md.

## Convention

- Le fichier s'appelle `voix.md` (pas `VOIX.md`, pas `.voix`)
- Il vit à la racine du dépôt instance
- Il est committé (pas gitignored)
