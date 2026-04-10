# SOFIA

> Des rôles spécialisés qui pensent avec vous. Le produit émerge de leur friction.

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

## Ce que SOFIA est

Une **méthode agnostique** pour travailler avec des personas IA spécialisées,
en friction intentionnelle, pilotées par un orchestrateur humain qui arbitre.
Les principes et le protocole ne dépendent d'aucun outil ;
le `runtime/` fournit une implémentation pour Claude Code, d'autres peuvent suivre.

Concrètement :
- Des **personas** — des rôles IA avec un nom, une posture, un périmètre, des interdits
- De la **friction** — les personas se challengent, l'orchestrateur tranche
- De l'**isolation** — chaque persona a son workspace, ses instructions, ses limites
- De l'**orchestration** — l'orchestrateur est le message bus, il porte le contexte entre les personas
- De la **traçabilité** — tout est tracé : décisions, sessions, reviews, échanges
- Des **artefacts** — les personas communiquent par fichiers, pas par chat

## Ce que SOFIA n'est pas

- Pas un framework — pas de code à installer, pas de dépendance
- Pas un produit — c'est une méthode, documentée dans un repo

## Quick start

```bash
git clone https://github.com/oxynoe-dev/sofia
cd sofia
claude
```

Claude Code ouvre le repo, charge le guide intégré (Sofia) et te pose
les bonnes questions. En 10 minutes, tu as ton premier persona
calibré pour ton projet.

> **Alpha preview** — Sofia repose sur le comportement conversationnel du runtime. Les résultats peuvent varier selon l'environnement. Si le flow ne se lance pas, le [mode manuel](doc/demarrer-manuel.md) couvre la même chose étape par étape.

## En savoir plus

| | |
|---|---|
| `core/` | Les invariants — principes, personas, friction, devoirs + templates |
| `protocol/` | Le contrat d'interface — artefacts, conventions, tracabilite, isolation, orchestration |
| `runtime/` | L'implementation concrete — Claude Code aujourd'hui, Mistral demain, d'autres après |
| `doc/` | Guides, workflows, patterns, retours terrain, architecture, ADR |

## Origine

SOFIA est née du projet [Katen](https://katen.run) — un moteur
d'orchestration formellement vérifié pour pipelines Data & IA, construit
avec 7 assistants IA spécialisés (architecte, dev, UX, chercheuse,
stratège, graphiste, rédacteur) sur 280+ sessions.

Une méthode qui a émergé d'une pratique personnelle — à confronter
à votre expertise.

**Site** : [oxynoe.io](https://oxynoe.io)

## Licence

MIT
