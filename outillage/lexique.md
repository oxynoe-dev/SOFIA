# Lexique — template

> Glossaire partage des termes du projet.

---

## Pourquoi un lexique ?

Quand 7 personas travaillent sur le meme projet, les mots derivent.
"Composition" peut signifier un fichier .kc, un concept CVM, ou un
pattern reutilisable selon qui parle.

Le lexique fixe les termes. Chaque persona le lit, personne ne reinvente.

## Format

```markdown
## {Terme}

**Definition** : {une phrase}
**Contexte** : {ou ce terme s'utilise}
**Ne pas confondre avec** : {termes proches}
**Decide le** : {date} — {reference ADR ou session}
```

## Conventions

- Un terme = une entree. Pas de synonymes dans la meme entree.
- Si un terme a change de sens (renommage, evolution), documenter l'historique.
- Le PO arbitre les conflits de definition.
- Le lexique vit dans `shared/orga/lexique.md` au niveau de l'instance.

## Exemple

```markdown
## Kata

**Definition** : une composition Katen — un programme visuel executable.
**Contexte** : fichiers .kc, documentation utilisateur, UI.
**Ne pas confondre avec** : "composition" (concept CVM interne), "pattern" (template reutilisable).
**Decide le** : 2026-03-22 — ADR-054.
```
