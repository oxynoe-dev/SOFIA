---
de: mira
pour: sofia, nora
type: contenu
date: 2026-04-05
objet: Page Méthode — vue d'ensemble architecturale de Voix
source: core/*.md, doc/arch-voix.md
---

# La méthode Voix

> Des rôles spécialisés qui pensent ensemble. Le produit émerge de leur friction.

---

## Trois piliers

Voix repose sur trois idées. Elles ne fonctionnent pas l'une sans l'autre.

**Contraindre** — Un assistant IA sans limites dit oui à tout et ne produit rien de bon. Voix impose à chaque assistant un rôle strict, un périmètre, et surtout des interdits. C'est la limitation qui le rend utile.

**Frotter** — Si tous les rôles sont d'accord, personne ne pense. La friction entre un architecte qui refuse de coder et un dev qui refuse d'implémenter une spec floue est un signal, pas un bug. Les désaccords forcent la clarté.

**Arbitrer** — La friction sans arbitre est du chaos. L'humain écoute, questionne, puis tranche. Toujours. Aucun assistant ne valide ses propres propositions. Aucun assistant ne force l'acceptation d'une décision.

![Les trois piliers de Voix](figures/fig-methode-piliers.svg)

---

## Sept principes

| # | Principe | En bref |
|---|----------|---------|
| 1 | La friction est productive | Les désaccords entre rôles sont des signaux |
| 2 | L'humain arbitre | Les assistants proposent, l'humain tranche |
| 3 | Chaque voix compte | Un rôle inutilisé est un rôle à supprimer |
| 4 | La contrainte force la qualité | Définis ce que le rôle ne fait pas avant ce qu'il fait |
| 5 | Les artefacts sont le protocole | Les échanges passent par des fichiers, pas du chat |
| 6 | Tout est tracé | Si ce n'est pas tracé, ça n'existe pas |
| 7 | Commence petit, itère | Un rôle au démarrage. Les autres émergent du travail |

→ [Lire les principes en détail](/voix/doc/principes)

---

## Anatomie d'un persona

Un persona est un assistant IA contraint par un CLAUDE.md — un fichier d'instructions qui définit son identité, sa posture, son périmètre et ses interdits.

Chaque persona vit dans son propre workspace. Il ne voit que ses fichiers. Il ne peut pas lire ou écrire chez les autres. L'isolation force les échanges formels : pour communiquer, il faut déposer un artefact.

![Anatomie d'un persona](figures/fig-methode-persona.svg)

### Ce qui tourne autour d'un persona

**Sessions** — Chaque conversation produit un résumé. C'est le pont entre les sessions : la suivante commence par lire la précédente. Format structuré, 30 lignes max.

**Livrables** — Chaque persona produit des livrables typés selon son rôle : specs, reviews, code, notes stratégiques, maquettes. Pas du texte générique — des artefacts nommés, adressables, versionnés.

**Artefacts échangés** — Les personas ne se parlent pas. Ils déposent des fichiers dans un bus partagé (`shared/`). Notes, reviews, features — chacun avec un frontmatter qui dit qui l'a écrit, pour qui, et si c'est traité.

**Émergence** — Un persona bien contraint détecte quand une question sort de son périmètre. Après 3 refus sur le même domaine, il signale le manque. Le persona suivant naît de cette observation, pas d'un plan initial.

→ [Voir les personas en détail](/voix/doc/personas)

---

## L'orchestration

L'humain est le message bus. Rien ne circule entre personas sans lui.

![Orchestration — le rôle du PO](figures/fig-methode-orchestration.svg)

Le PO ouvre une session avec un persona, obtient un livrable, ferme la session. Ouvre une session avec un autre persona, transmet le livrable, recueille la réaction. Chaque transmission est un moment de filtrage, de reformulation, d'ajout de contexte.

**Ce que le PO ne délègue pas** :
- La priorisation — quel persona intervient, dans quel ordre
- La consolidation — synthétiser les retours de plusieurs personas
- La décision — trancher quand les personas divergent
- Le filtrage — ce qui est pertinent à transmettre ou pas

C'est lent. C'est le prix de la qualité. Si l'échange n'en vaut pas le coût, c'est que le sujet ne nécessitait pas plusieurs personas.

---

## Trois couches

La méthode se structure en trois couches indépendantes. On peut changer l'une sans toucher les autres.

**Core** — Les invariants. Principes, personas, friction. Ce qui ne change pas quand on change d'outil. Si demain Claude Code disparaît, le core tient.

**Protocol** — Le contrat d'interface. Artefacts, conventions, traçabilité, instance. Fichiers, pas API. Git, pas base de données. Le protocol est ce qui rend la méthode portable — n'importe quel outil capable de lire et écrire des fichiers markdown peut implémenter Voix.

**Runtime** — L'implémentation concrète. CLAUDE.md, Claude Code, hooks, mémoire persistante. Remplaçable sans toucher au core ni au protocol. C'est la seule couche qui change si on porte Voix sur un autre provider.

| Couche | Contenu | Change quand… |
|---|---|---|
| **Core** | principes, personas, friction, devoirs | …la méthode évolue (rare) |
| **Protocol** | artefacts, conventions, traçabilité, instance | …le format d'échange évolue |
| **Runtime** | CLAUDE.md, hooks, sessions, mémoire | …on change d'outil |

---

## Le gradient

La méthode ne se déploie pas en big bang. Elle grandit avec le projet.

| Seuil | Ce qui s'active |
|---|---|
| 1 persona | CLAUDE.md + sessions/ — la base |
| 2+ personas | shared/ — le bus d'échange (notes, reviews) |
| 3+ personas | backlogs par workspace |
| 4+ personas | features/ — les specs formalisées |
| 5+, multi-produit | Convergence — dashboard de pilotage |

On commence petit. On ajoute de la structure quand la charge mentale du PO l'exige.

---

## Terrain

La méthode a été développée et validée sur le projet Katen — un moteur de composition multimédia construit avec 7 personas sur 210+ sessions.

| Indicateur | Valeur |
|---|---|
| Personas actifs | 7 (architecte, dev, UX, stratégie, recherche, rédaction, graphisme) |
| Sessions | 210+ |
| ADR produits | 62 |
| Produits livrés | 1 (Katen v0.2) |

→ [Voir les fiches personas Katen](/voix/doc/tutoriels)
→ [Lire le livre bleu](/voix/livre-bleu)

---

## Six devoirs de l'humain

Les personas produisent, challengent, documentent. Mais certaines responsabilités ne se délèguent pas.

1. **Vérifier les faits** — Les LLMs ne comptent pas. Dates, chiffres, références : vérification humaine systématique.
2. **Arbitrer** — Écouter, questionner, trancher. La décision est tracée.
3. **Relire ce qui sort** — Aucun document ne sort sans relecture complète.
4. **Calibrer les personas** — Ajuster les contraintes en continu.
5. **Séparer réflexion et production** — Celui qui rédige n'est pas celui qui valide.
6. **Maintenir l'attention** — Quand tu approuves sans lire, c'est le moment de ralentir.

→ [Lire les devoirs en détail](/voix/doc/organisation)
