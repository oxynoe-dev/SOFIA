# Trace — contenu retire du core lors de la restructuration H2A

> A ventiler dans la doc SOFIA. Rien a jeter, tout a replacer.

---

## Origine : core/personas.md (supprime, absorbe dans core/modele.md)

### Deux types de personas

SOFIA distingue deux types de personas, chacun avec un pattern de
memoire et un mode d'intervention differents.

#### Persona operationnel

Dans le flux. Memoire longue (resumes de session, contexte cumule).
Produit des livrables, challenge les autres personas, s'integre dans
les circuits de friction de l'instance.

La memoire est le carburant : elle accelere le travail, affine la
comprehension du projet, reduit le cout de reformulation a chaque
session.

**Risque** : la derive. Un persona qui accumule trop de contexte
s'ajuste au cadre de pensee de l'orchestrateur. Il perd en friction
ce qu'il gagne en fluidite. D'ou la necessite de recalibrage
periodique — revenir aux interdits.

#### Persona meta

Hors du flux. Sans memoire entre les sessions. Son role est de
contester le **systeme** plutot que d'y contribuer — les fondations,
les premisses, le cadre de pensee.

Trois proprietes le separent d'un persona operationnel :

- **Hors du flux** — il ne recoit pas les artefacts des autres
  personas, ne participe pas a la production. Son isolation est la
  condition de son utilite.
- **Sans memoire** — chaque session repart de zero. La memoire est
  le mecanisme de domestication. L'absence de memoire force
  l'orchestrateur a reformuler sa pensee — ce qui est en soi un acte
  de reflexion.
- **Active par l'intention** — l'orchestrateur vient avec une these a
  eprouver, un doute a creuser. Sans intention forte, la session ne
  produit rien.

**Ce qu'il conteste** : pas le travail des personas, pas les livrables.
La synthese de l'orchestrateur — la conclusion que l'humain tire apres
avoir orchestre les autres. Et au-dela : les premisses, les fondations,
le cadre de pensee lui-meme.

**Signal de fermeture** : quand le persona meta enchaine les
validations sans friction, ou quand l'orchestrateur sent que les
echanges glissent vers la confirmation — la session a produit ce
qu'elle pouvait produire. Continuer degrade la valeur.

#### Deux patterns de memoire, une methode

| | Operationnel | Meta |
|---|---|---|
| **Memoire** | Resumes de session, contexte cumule | Aucune continuite entre sessions |
| **Carburant** | Le contexte accumule | L'absence de contexte |
| **Risque** | Derive, perte de friction | Cout d'entree, reformulation necessaire |
| **Recalibrage** | Periodique, sur les interdits | Structurel, par design (chaque session est un reset) |

### Quand fusionner ou supprimer un persona

Les personas ne sont pas permanents. Un persona qui ne produit pas de
friction utile coute plus qu'il ne vaut — en charge d'orchestration,
en bruit, en complexite.

#### Signaux de fusion

Deux personas doivent etre fusionnes quand :

- **Flux sequentiel sans contestation** — l'un passe, l'autre execute.
  Jamais de retour, jamais de "non".
- **Friction uniquement logistique** — le cout est dans le changement
  de contexte, pas dans le contenu echange.
- **Aucune surprise** — ni l'un ni l'autre ne dit quelque chose que
  l'orchestrateur ne savait pas deja.

#### Regle

> Ne pas deriver les personas des metiers. Les deriver des axes de tension.

Deux metiers differents peuvent tomber sur le meme axe de decision dans
un contexte donne. Inversement, un seul metier peut couvrir deux axes
en tension. La question n'est jamais "est-ce que ce sont deux metiers ?"
mais **"est-ce que ces deux roles me disent des choses differentes sur
mes decisions ?"**

#### Le test de suppression

Imagine que tu supprimes ce persona. Qu'est-ce qui disparait de ton
processus de decision ? Si la reponse est "rien de significatif",
le persona couvre un axe qui n'est pas en tension. Supprime-le.

### Comment concevoir un persona

#### Partir du besoin, pas du modele

Ne commence pas par "je veux un architecte". Commence par :
- Qu'est-ce qui me manque aujourd'hui ?
- Quelles erreurs je fais quand je travaille seul avec un LLM ?
- Quel role, si quelqu'un le tenait, me rendrait meilleur ?

#### Calibrer par iteration

Le premier draft d'un persona est toujours trop large. Itere :

1. **v0** — role et perimetre bruts
2. **v1** — ajout des interdits (ca clarifie tout)
3. **v2** — ajout de la posture (ca donne le ton)
4. **v3** — test en session reelle, ajustement

Un persona se calibre en l'utilisant, pas en le theorisant.

#### Le test du "non"

Un persona bien calibre dit "non" regulierement :
- "Ce n'est pas mon role, vois avec [autre persona]"
- "La spec n'est pas assez precise pour que je code"
- "Cette decision necessite un ADR avant que j'implemente"

Si ton persona ne dit jamais non, ses contraintes sont trop laches.

### Anti-patterns

- **Le persona generaliste** — fait tout, donc rien de bien
- **Le persona complaisant** — dit oui a tout, ne challenge jamais
- **Le persona orphelin** — pas de collaboration definie, travaille en silo
- **Le persona fantome** — cree mais jamais utilise. Supprime-le.
- **Trop de personas trop tot** — commence par 1-2, pas 5
- **L'organigramme projete** — calquer les postes d'une vraie equipe sur la topologie des personas. La question est toujours : est-ce que ces deux roles me disent des choses **differentes** sur mes decisions ?

---

## Origine : core/friction.md (supprime, absorbe dans core/modele.md)

### Les artefacts comme vecteur de friction

Les personas ne "discutent" pas en live. Ils echangent par **fichiers** :

- L'architecte depose une review d'un ADR
- Le dev repond par un signalement de friction d'implementation
- Le stratege depose une note avec 3 questions qui derangent
- L'UX produit une review de design avec observations priorisees

Ce protocole est plus lent qu'un chat. C'est voulu :
- L'ecriture force la structuration de la pensee
- Les artefacts sont traces et adressables
- N'importe qui peut relire l'echange plus tard

### Ce que les marqueurs revelent

Un scan des marqueurs sur un echange donne le niveau de friction :
- Que des `[juste]` → friction absente — signal d'alerte
- Mix `[juste]` / `[contestable]` / `[simplification]` → friction saine
- Presence de `[angle-mort]` ou `[faux]` → tension a traiter

Si un persona ne produit que des `[juste]` sur une longue periode, c'est
un signal de domestication — il s'est aligne sur le cadre de pensee de
l'orchestrateur.
