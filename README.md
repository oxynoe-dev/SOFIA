# Voix

> Des rôles spécialisés qui pensent ensemble. Le produit émerge de leur conversation.

---

## Le problème

Un LLM généraliste fait tout. Mal.

Il code, il conseille, il rédige, il review — dans la même conversation,
avec le même ton, sans contrainte de périmètre. Il dit oui à tout.
Il ne challenge rien. Il ne se souvient de rien.

Le résultat : un assistant servile qui produit du contenu moyen,
sans friction, sans trace, sans progression.

## La thèse

**Des rôles contraints produisent mieux qu'un agent libre.**

Un architecte qui ne code pas est obligé de spécifier clairement.
Un développeur qui ne décide pas de l'architecture est obligé de
remonter les frictions. Un stratège qui n'a pas accès au code est
obligé de penser en termes de valeur, pas d'implémentation.

La contrainte n'est pas une limite — c'est ce qui force la qualité.

## Ce que Voix est

Une **méthode** pour travailler avec des personas IA spécialisées,
en friction intentionnelle, pilotées par un humain qui arbitre.

Concrètement :
- Des **personas** — des rôles IA avec un nom, une posture, un périmètre, des interdits
- De la **friction** — les personas se challengent, l'humain tranche
- De l'**isolation** — chaque persona a son workspace, ses instructions, ses limites
- De l'**orchestration** — l'humain est le message bus, il porte le contexte entre les personas
- De la **traçabilité** — tout est tracé : décisions, sessions, reviews, échanges
- Des **artefacts** — les personas communiquent par fichiers, pas par chat

## Ce que Voix n'est pas

- Pas un framework — pas de code à installer, pas de dépendance
- Pas un produit — c'est une méthode, documentée dans un repo
- Pas agnostique — Voix est conçu pour **Claude Code** et exploite ses fonctionnalités (CLAUDE.md, mémoire persistante, workspaces isolés)

## Quick start

```bash
git clone https://github.com/oxynoe-dev/voix
cd voix
claude
```

Claude Code ouvre le repo, charge le guide intégré et te pose
les bonnes questions. En 10 minutes, tu as ton premier persona
calibré pour ton projet.

## En savoir plus

| | |
|---|---|
| `methode/` | Les principes, l'orchestration — pourquoi ça marche |
| `claude-code/` | Le support — comment ça s'implémente dans Claude Code |
| `templates/` | Les templates — prêts à l'emploi |
| `exemples/katen/` | Le terrain — 5 personas en production sur un vrai projet |
| `retours/` | Le vécu — ce qui marche et ce qui casse |

## Origine

Voix est née du projet [Katen](https://katen.run) — un moteur de
composition visuelle construit avec 5 personas IA spécialisées
(architecte, dev, UX, chercheuse, stratège) sur 28 sessions fondatrices.

La méthode a émergé de la pratique, pas de la théorie. Elle est
documentée ici pour être partagée.

## Licence

MIT
