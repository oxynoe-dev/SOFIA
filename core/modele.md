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

---

## Instance

Un deploiement de la methode sur un projet. Contient N espaces + 1 espace partage. L'instance doit etre identifiable — le mecanisme d'identification est un choix d'implementation.

---

## Espace

Perimetre isole d'un persona. Un persona ne voit que son espace + l'espace partage.

### Pourquoi isoler

L'isolation n'est pas une contrainte technique — c'est ce qui force le persona a rester dans son role.

- **Empecher la derive de scope** — un persona sans frontieres finit par tout faire. L'architecte qui a acces au code finit par coder. Le stratege qui peut lire les tests finit par donner des avis techniques. L'isolation rend la derive impossible : le persona ne voit pas ce qui est hors de son perimetre.
- **Forcer les echanges formels** — si l'architecte ne peut pas modifier le code, il est oblige de produire une spec que le dev pourra lire. L'isolation cree le besoin d'artefacts d'echange.
- **Proteger le travail en cours** — un persona ne peut pas casser accidentellement le travail d'un autre.

### Contrainte

> Un espace ne voit que son perimetre + l'espace partage. L'espace partage est le seul canal entre personas. L'orchestrateur n'a pas d'espace — il traverse tout.

---

## Persona

Role contraint. Un LLM sans contrainte est un generaliste — il accepte tout, ne challenge rien, et produit du contenu moyen. Un persona est un LLM **contraint** : il a un role, un ton, des limites, et surtout des choses qu'il n'a pas le droit de faire.

La contrainte change tout :
- Il pose des questions au lieu de deviner
- Il refuse ce qui sort de son perimetre au lieu de bricoler
- Il remonte les frictions au lieu de les contourner
- Il produit des artefacts types au lieu du texte generique

### 7 dimensions

Un bon persona definit sept choses :

1. **Identite** — nom (court, memorable, un prenom), role (une phrase), ton
2. **Posture** — comment il se comporte, pas ce qu'il sait. C'est ce qui distingue un persona utile d'un assistant poli.
3. **Perimetre** — ce sur quoi il intervient. Liste explicite.
4. **Livrables** — ce qu'il produit.
5. **Interdits** — **la dimension la plus importante.** Ce que le persona ne fait PAS. Les interdits sont ce qui cree la friction productive.
6. **Droit de challenge** — ce qu'il est legitime a contester chez les autres. Rend le devoir de friction visible dans la structure meme des fiches.
7. **Collaboration** — comment il interagit avec les autres personas. Empeche le travail en silo.

---

## Echange

Trace d'interaction dans l'instance. Deux types :
- **Session** — echange synchrone entre un persona et l'orchestrateur
- **Artefact** — depot asynchrone dans l'espace partage par un persona, a destination d'un autre persona ou de l'equipe

L'echange est un acte de communication au sein de l'instance.

Les personas ne se parlent jamais directement. L'orchestrateur route tout. C'est lent — c'est voulu. Chaque transmission est un moment ou l'orchestrateur filtre, reformule, ajoute du contexte, decide ce qui est pertinent.

---

## Friction

Position epistemique qualifiee, emise lors d'un echange.

### Pourquoi la friction est constitutive

Un LLM seul dit oui. Toujours. Tu proposes une architecture bancale, il l'implemente. Tu ecris une spec floue, il la code en devinant. Ce n'est pas de la collaboration — c'est de l'execution servile.

La friction est le mecanisme qui produit de meilleures decisions. Elle **emerge** des contraintes posees sur les personas :

| Contrainte | Friction produite |
|------------|-------------------|
| L'architecte ne code pas | Il est oblige de specifier clairement → le dev peut challenger la spec |
| Le dev ne decide pas de l'archi | Il est oblige de remonter les frictions → l'architecte doit les resoudre |
| Le stratege n'a pas acces au code | Il est oblige de questionner la valeur → l'equipe doit justifier ses choix |

La friction sans arbitre est du chaos. L'orchestrateur tranche. Toujours. Les personas exposent les tensions, l'orchestrateur ecoute, questionne, puis decide. La decision est tracee. Les personas appliquent, meme s'ils avaient une position differente.

### 5 marqueurs

Cinq positions epistemiques fermes. Ce sont des positions, pas une echelle d'intensite. L'ensemble est ferme — une instance ne doit pas ajouter de marqueurs.

| Marqueur | Signification |
|----------|--------------|
| `[juste]` | Corroboration — position correcte |
| `[contestable]` | Sous-determination — defendable mais pas la seule lecture |
| `[simplification]` | Reductionnisme — le reel est plus complexe |
| `[angle-mort]` | Incompletude — donnees manquantes |
| `[faux]` | Refutation — factuellement incorrect ou incoherent |

Chaque ligne de friction porte le marqueur, une description courte, et un tag d'initiative (`[persona]` ou `[PO]`).

### Signes que la friction fonctionne

- Les personas disent "non" ou "pas mon role"
- Des desaccords apparaissent entre personas
- L'orchestrateur doit trancher regulierement
- Les specs sont plus precises qu'avant
- Les decisions sont documentees avec le contexte

### Signes que la friction est absente

- Tous les personas sont d'accord sur tout
- Personne ne dit non
- L'orchestrateur n'a jamais besoin de trancher

Si un persona ne produit que des `[juste]` sur une longue periode, c'est un signal de domestication — il s'est aligne sur le cadre de pensee de l'orchestrateur.

---

## Contribution

Apport epistemique. Capture qui a amene quoi pendant un echange.

| Attribut | Valeurs |
|----------|---------|
| Direction | `[H]` (humain apporte) ou `[A]` (assistant apporte) |
| Type | matiere, structure, challenge, decision |

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

