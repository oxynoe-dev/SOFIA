# Lexique — template

> Glossaire partagé des termes du projet.

---

## Pourquoi un lexique ?

Quand 7 personas travaillent sur le même projet, les mots dérivent.
"Composition" peut signifier un fichier .kc, un concept CVM, ou un
pattern réutilisable selon qui parle.

Le lexique fixe les termes. Chaque persona le lit, personne ne réinvente.

## Format

```markdown
## {Terme}

**Définition** : {une phrase}
**Contexte** : {où ce terme s'utilise}
**Ne pas confondre avec** : {termes proches}
**Décidé le** : {date} — {référence ADR ou session}
```

## Conventions

- Un terme = une entrée. Pas de synonymes dans la même entrée.
- Si un terme a changé de sens (renommage, évolution), documenter l'historique.
- L'orchestrateur arbitre les conflits de définition.
- Le lexique vit dans `shared/orga/lexique.md` au niveau de l'instance.

## Exemple

```markdown
## Kata

**Définition** : une composition Katen — un programme visuel exécutable.
**Contexte** : fichiers .kc, documentation utilisateur, UI.
**Ne pas confondre avec** : "composition" (concept CVM interne), "pattern" (template réutilisable).
**Décidé le** : 2026-03-22 — ADR-054.
```
