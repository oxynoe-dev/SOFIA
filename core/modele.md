# Modele d'instance

> Les 7 entites constitutives d'une instance SOFIA.

---

## Vue d'ensemble

Le modele SOFIA definit les entites sans lesquelles la methode n'existe pas. Si tu supprimes une de ces entites, ce n'est plus SOFIA.

7 entites, organisees en 3 niveaux :
1. Topologie — Orchestrateur, Instance, Espace, Persona
2. Interaction — Echange
3. Observation — Friction, Contribution

---

## Orchestrateur

L'humain. Il orchestre les instances, arbitre les conflits entre personas, route les echanges. Il n'a pas d'espace propre — il traverse tout.

C'est le seul participant qui n'est pas contraint par l'isolation. C'est aussi le seul qui tranche.

Ses responsabilites sont non-delegables. Voir `devoirs.md`.

| Champ | Type | Obligatoire | Definition |
|-------|------|-------------|-----------|
| **identifiant** | texte | DOIT | Identifiant unique de l'orchestrateur |
| **instances** | liste | DOIT | Instances orchestrees |

---

## Instance

Un deploiement de la methode sur un projet. Contient N espaces + 1 espace partage. L'instance doit etre identifiable — le mecanisme d'identification est un choix d'implementation.

| Champ | Type | Obligatoire | Definition |
|-------|------|-------------|-----------|
| **identifiant** | texte | DOIT | Identifiant unique de l'instance |
| **espaces** | liste | DOIT | Espaces de travail (1 par persona + 1 partage) |
| **orchestrateur** | ref | DOIT | L'orchestrateur qui pilote cette instance |
| **version_methode** | texte | DOIT | Version de SOFIA appliquee |

---

## Espace

Perimetre isole d'un persona. Un persona ne voit que son espace + l'espace partage.

| Champ | Type | Obligatoire | Definition |
|-------|------|-------------|-----------|
| **identifiant** | texte | DOIT | Identifiant unique dans l'instance |
| **persona** | ref | DOIT | Le persona qui opere dans cet espace |
| **partage** | booleen | DOIT | Espace partage (bus d'echange) ou espace persona |

### Pourquoi isoler

L'isolation n'est pas une contrainte technique — c'est ce qui force le persona a rester dans son role.

- **Empecher la derive de scope** — un persona sans frontieres finit par tout faire. L'architecte qui a acces au code finit par coder. Le stratege qui peut lire les tests finit par donner des avis techniques. L'isolation rend la derive impossible : le persona ne voit pas ce qui est hors de son perimetre.
- **Forcer les echanges formels** — si l'architecte ne peut pas modifier le code, il est oblige de produire une spec que le dev pourra lire. L'isolation cree le besoin d'artefacts d'echange.
- **Proteger le travail en cours** — un persona ne peut pas casser accidentellement le travail d'un autre.

### Contrainte

> Un espace ne voit que son perimetre + l'espace partage. L'espace partage est le seul canal entre personas. L'orchestrateur n'a pas d'espace — il traverse tout.

---

## Persona

Role contraint. Un LLM sans contrainte est un generaliste — il accepte tout, ne conteste rien, et produit du contenu moyen. Un persona est un LLM **contraint** : il a un role, un ton, des limites, et surtout des choses qu'il n'a pas le droit de faire.

La contrainte change tout :
- Il pose des questions au lieu de deviner
- Il refuse ce qui sort de son perimetre au lieu de bricoler
- Il remonte les frictions au lieu de les contourner
- Il produit des artefacts types au lieu du texte generique

### 7 dimensions

| Dimension | Obligatoire | Definition |
|-----------|-------------|-----------|
| **Identite** | DOIT | Nom (court, memorable, un prenom), role (une phrase), ton |
| **Posture** | DOIT | Comment il se comporte, pas ce qu'il sait |
| **Perimetre** | DOIT | Ce sur quoi il intervient. Liste explicite |
| **Livrables** | DOIT | Ce qu'il produit |
| **Interdits** | DOIT | Ce que le persona ne fait PAS. Les interdits creent la friction productive |
| **Droit de contestation** | DOIT | Ce qu'il est legitime a contester chez les autres |
| **Collaboration** | DOIT | Comment il interagit avec les autres personas |

---

## Echange

Trace d'interaction dans l'instance. L'echange est un acte de communication au sein de l'instance.

Les personas ne se parlent jamais directement. L'orchestrateur route tout. C'est lent — c'est voulu. Chaque transmission est un moment ou l'orchestrateur filtre, reformule, ajoute du contexte, decide ce qui est pertinent.

| Champ | Type | Obligatoire | Definition |
|-------|------|-------------|-----------|
| **type** | enum | DOIT | `session` (synchrone) ou `artefact` (depot asynchrone) |
| **instance** | ref | DOIT | Instance dans laquelle l'echange a lieu |
| **espace** | ref | DOIT | Espace du persona concerne |
| **date_heure** | datetime | DOIT | Date et heure de l'echange |
| **persona** | ref | DOIT | Persona implique |

Voir `protocol/exchange.md` pour les dimensions specifiques par type.

---

## Friction

Prise de position qualifiee d'un participant sur une proposition de l'autre, emise lors d'un echange.

| Champ | Type | Obligatoire | Definition |
|-------|------|-------------|-----------|
| **echange** | ref | DOIT | L'echange qui a genere la friction |
| **emetteur** | ref | DOIT | Persona ou orchestrateur qui emet la position |
| **marqueur** | enum | DOIT | `[juste]`, `[contestable]`, `[simplification]`, `[angle-mort]`, `[faux]` |
| **description** | texte | DOIT | Resume court de la position |
| **initiative** | enum | DOIT | `[persona]` ou `[PO]` — qui a initie le sujet |

Voir `protocol/friction.md` pour le detail des marqueurs et le format.

### Pourquoi la friction est constitutive

La friction est le mecanisme qui produit de meilleures decisions. Elle **emerge** des contraintes posees sur les personas :

| Contrainte | Friction produite |
|------------|-------------------|
| L'architecte ne code pas | Il est contraint de specifier clairement — le dev peut contester la spec |
| Le dev ne decide pas de l'archi | Il est contraint de remonter les frictions — l'architecte doit les resoudre |
| Le stratege n'a pas acces au code | Il est contraint de questionner la valeur — l'equipe doit justifier ses choix |

La friction sans arbitre est du chaos. L'orchestrateur tranche. Les personas exposent les tensions, l'orchestrateur ecoute, questionne, puis decide. La decision est tracee.

### Signes que la friction fonctionne

- Les personas disent "non" ou "pas mon role"
- Des desaccords apparaissent entre personas
- L'orchestrateur doit trancher regulierement

### Signes que la friction est absente

- Tous les personas sont d'accord sur tout
- Personne ne dit non
- L'orchestrateur n'a jamais besoin de trancher

Si un persona ne produit que des `[juste]` sur une longue periode, c'est un signal de domestication.

---

## Contribution

Apport epistemique. Capture qui a amene quoi pendant un echange.

| Champ | Type | Obligatoire | Definition |
|-------|------|-------------|-----------|
| **echange** | ref | DOIT | L'echange qui a genere la contribution |
| **direction** | enum | DOIT | `[H]` (humain apporte) ou `[A]` (assistant apporte) |
| **type** | enum | DOIT | `matiere`, `structure`, `contestation`, `decision` |
| **description** | texte | DOIT | Resume court de l'apport |

Voir `protocol/contribution.md` pour le detail des types et le format.

La contribution est distincte de la friction : la friction capture la tension (positions qui s'opposent, resistance), la contribution capture l'apport (qui a nourri quoi). Une correction acceptee sans resistance est une contribution, pas une friction.

---

## Relations

| De | Vers | Relation | Cardinalite |
|----|------|----------|-------------|
| Orchestrateur | Instance | orchestre | 1 → 1..* |
| Instance | Espace | contient | 1 → 1..* |
| Espace | Persona | opere | 1 → 1 |
| Persona | Echange | emet / recoit | 1 → * |
| Orchestrateur | Echange | participe | 1 → * |
| Echange | Friction | genere | 1 → * |
| Echange | Contribution | genere | 1 → * |
| Persona | Persona | challenge | * → * |

