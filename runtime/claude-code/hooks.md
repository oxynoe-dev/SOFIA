# Hooks

> Automatiser ce qui doit l'être, pas plus.

---

## Ce que c'est

Claude Code permet de configurer des **hooks** — des commandes shell
qui s'exécutent en réponse à des événements (avant/après un tool call,
à la soumission d'un prompt, etc.).

## Hooks utiles pour SOFIA

### Rappel de résumé de session

Un hook qui rappelle au persona de produire un résumé quand la
conversation dépasse un certain nombre d'échanges. En pratique,
l'instruction dans le CLAUDE.md suffit généralement.

### Vérification d'isolation

Un hook pre-edit qui vérifie que le persona n'écrit pas en dehors
de son périmètre autorisé. Utile si le persona a tendance à déborder.

### Format de commit

Un hook pre-commit qui vérifie le format du message de commit
selon les conventions du projet.

## Quand ne PAS utiliser de hooks

- Pour reproduire un comportement que le CLAUDE.md gère déjà
- Pour des vérifications que le persona peut faire lui-même
- Pour des automatisations complexes qui obscurcissent le workflow

Les hooks sont un filet de sécurité, pas un mécanisme principal.
Si tu as besoin de beaucoup de hooks, tes instructions CLAUDE.md
ne sont probablement pas assez claires.

## Configuration

Les hooks se configurent dans `settings.json` :

```json
{
  "hooks": {
    "preToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "script-de-verification.sh"
      }
    ]
  }
}
```

Voir la documentation Claude Code pour les détails.
