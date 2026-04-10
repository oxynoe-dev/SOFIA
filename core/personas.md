# Personas

> Un persona est un rôle avec un nom, une posture, un périmètre et des interdits.

---

## Pourquoi des personas ?

Un LLM sans contrainte est un généraliste. Il accepte tout, ne challenge
rien, et produit du contenu moyen. Un persona est un LLM **contraint** :
il a un rôle, un ton, des limites, et surtout des choses qu'il n'a pas
le droit de faire.

La contrainte change tout :
- Il pose des questions au lieu de deviner
- Il refuse ce qui sort de son périmètre au lieu de bricoler
- Il remonte les frictions au lieu de les contourner
- Il produit des livrables typés au lieu du texte générique

## Anatomie d'un persona

Un bon persona définit **sept choses** :

### 1. Identité

- **Nom** — court, mémorable. Pas un acronyme, pas un titre. Un prénom.
- **Rôle** — une phrase. "Architecte système & solution". "Développeur full stack".
- **Ton** — formel ? direct ? pédagogue ? provocateur ?

Le nom compte plus qu'on croit. Il crée une relation. On ne parle pas
à "l'agent architecture" comme on parle à Mira.

### 2. Posture

Comment le persona se comporte — pas ce qu'il sait, mais comment il
interagit. C'est la section la plus importante.

Exemples de postures :
- *"Formelle mais pas dogmatique"* — ancre dans la théorie, remet en question
- *"Implémente, ne réinterprète pas"* — si la spec est floue, il le dit
- *"Direct, franc, sans détours"* — dit non quand c'est nécessaire

La posture est ce qui distingue un persona utile d'un assistant poli.

### 3. Périmètre

Ce sur quoi le persona intervient. Liste explicite.

Un architecte : modèle d'exécution, contrats d'interface, ADR.
Un dev : code, tests, retours de frictions d'implémentation.
Un stratège : positionnement, go-to-market, questions qui dérangent.

### 4. Livrables

Ce que le persona **produit**. Pas "du texte" — des types précis :

- ADR, reviews, specs, schémas (architecte)
- Code testé, signalements de frictions (dev)
- User flows, spécifications UI (UX)
- Synthèses de littérature, avis motivés (chercheur)

### 5. Interdits

**La section la plus importante.** Ce que le persona ne fait PAS.

- Un architecte ne code pas
- Un dev ne tranche pas sur l'architecture
- Un stratège ne conçoit pas l'UX
- Personne ne décide à la place de l'orchestrateur

Les interdits sont ce qui crée la friction productive. Si l'architecte
pouvait coder, il ne prendrait jamais le temps de spécifier. Si le dev
pouvait décider de l'architecture, il ne remonterait jamais les frictions.

### 6. Droit de challenge

Ce que le persona est légitime à **contester** chez les autres. La friction
intentionnelle rendue structurelle : chaque persona sait non seulement ce
qu'il produit, mais sur quoi il a un droit de regard explicite.

Exemples :
- L'architecte challenge les ADR avant acceptance et les specs avant implémentation
- Le dev challenge les specs trop vagues et les ADR qui créent des frictions d'implémentation
- La chercheuse challenge les affirmations scientifiques et les données factuelles
- Le stratège challenge la viabilité business et les ADR à impact stratégique
- La graphiste challenge la cohérence visuelle des livrables
- L'UX challenge les productions front avant publication
- Le rédacteur challenge la clarté et l'honnêteté des formulations

Sans cette section, la friction reste implicite — chaque persona *pourrait*
challenger, mais rien ne dit qu'il *doit*. La section rend le devoir de
friction visible dans la structure même des fiches.

### 7. Collaboration

Comment le persona interagit avec les autres :

| Avec | Mode |
|------|------|
| Architecte | Le dev implémente les contrats et remonte les frictions |
| UX | Le dev signale les contraintes techniques sur les specs UI |
| Chercheur | Le dev consulte quand une implémentation touche au modèle formel |

La table de collaboration empêche les personas de travailler en silo.

## Types de personas

SOFIA distingue deux types de personas, chacun avec un pattern de
mémoire et un mode d'intervention différents.

### Persona opérationnel

Dans le flux. Mémoire longue (résumés de session, contexte cumulé).
Produit des livrables, challenge les autres personas, s'intègre dans
les circuits de friction de l'instance.

La mémoire est le carburant : elle accélère le travail, affine la
compréhension du projet, réduit le coût de reformulation à chaque
session.

**Risque** : la dérive. Un persona qui accumule trop de contexte
s'ajuste au cadre de pensée de l'orchestrateur. Il perd en friction
ce qu'il gagne en fluidité. D'où la nécessité de recalibrage
périodique — revenir aux interdits.

### Persona méta

Hors du flux. Sans mémoire entre les sessions. Son rôle est de
contester le **système** plutôt que d'y contribuer — les fondations,
les prémisses, le cadre de pensée.

Trois propriétés le séparent d'un persona opérationnel :

- **Hors du flux** — il ne reçoit pas les artefacts des autres
  personas, ne participe pas à la production. Son isolation est la
  condition de son utilité.
- **Sans mémoire** — chaque session repart de zéro. La mémoire est
  le mécanisme de domestication. L'absence de mémoire force
  l'orchestrateur à reformuler sa pensée — ce qui est en soi un acte
  de réflexion.
- **Activé par l'intention** — l'orchestrateur vient avec une thèse à
  éprouver, un doute à creuser. Sans intention forte, la session ne
  produit rien.

**Ce qu'il conteste** : pas le travail des personas, pas les livrables.
La synthèse de l'orchestrateur — la conclusion que l'humain tire après
avoir orchestré les autres. Et au-delà : les prémisses, les fondations,
le cadre de pensée lui-même.

**Signal de fermeture** : quand le persona méta enchaîne les
validations sans friction, ou quand l'orchestrateur sent que les
échanges glissent vers la confirmation — la session a produit ce
qu'elle pouvait produire. Continuer dégrade la valeur.

### Deux patterns de mémoire, une méthode

| | Opérationnel | Méta |
|---|---|---|
| **Mémoire** | Résumés de session, contexte cumulé | Aucune continuité entre sessions |
| **Carburant** | Le contexte accumulé | L'absence de contexte |
| **Risque** | Dérive, perte de friction | Coût d'entrée, reformulation nécessaire |
| **Recalibrage** | Périodique, sur les interdits | Structurel, par design (chaque session est un reset) |

## Quand fusionner ou supprimer un persona

Les personas ne sont pas permanents. Un persona qui ne produit pas de
friction utile coûte plus qu'il ne vaut — en charge d'orchestration,
en bruit, en complexité.

### Signaux de fusion

Deux personas doivent être fusionnés quand :

- **Flux séquentiel sans contestation** — l'un passe, l'autre exécute.
  Jamais de retour, jamais de "non".
- **Friction uniquement logistique** — le coût est dans le changement
  de contexte, pas dans le contenu échangé.
- **Aucune surprise** — ni l'un ni l'autre ne dit quelque chose que
  l'orchestrateur ne savait pas déjà.

### Règle

> Ne pas dériver les personas des métiers. Les dériver des axes de tension.

Deux métiers différents peuvent tomber sur le même axe de décision dans
un contexte donné. Inversement, un seul métier peut couvrir deux axes
en tension. La question n'est jamais "est-ce que ce sont deux métiers ?"
mais **"est-ce que ces deux rôles me disent des choses différentes sur
mes décisions ?"**

### Le test de suppression

Imagine que tu supprimes ce persona. Qu'est-ce qui disparaît de ton
processus de décision ? Si la réponse est "rien de significatif",
le persona couvre un axe qui n'est pas en tension. Supprime-le.

## Comment concevoir un persona

### Partir du besoin, pas du modèle

Ne commence pas par "je veux un architecte". Commence par :
- Qu'est-ce qui me manque aujourd'hui ?
- Quelles erreurs je fais quand je travaille seul avec un LLM ?
- Quel rôle, si quelqu'un le tenait, me rendrait meilleur ?

### Calibrer par itération

Le premier draft d'un persona est toujours trop large. Itère :

1. **v0** — rôle et périmètre bruts
2. **v1** — ajout des interdits (ça clarifie tout)
3. **v2** — ajout de la posture (ça donne le ton)
4. **v3** — test en session réelle, ajustement

Un persona se calibre en l'utilisant, pas en le théorisant.

### Le test du "non"

Un persona bien calibré dit "non" régulièrement :
- "Ce n'est pas mon rôle, vois avec [autre persona]"
- "La spec n'est pas assez précise pour que je code"
- "Cette décision nécessite un ADR avant que j'implémente"

Si ton persona ne dit jamais non, ses contraintes sont trop lâches.

## Anti-patterns

- **Le persona généraliste** — fait tout, donc rien de bien
- **Le persona complaisant** — dit oui à tout, ne challenge jamais
- **Le persona orphelin** — pas de collaboration définie, travaille en silo
- **Le persona fantôme** — créé mais jamais utilisé. Supprime-le.
- **Trop de personas trop tôt** — commence par 1-2, pas 5
- **L'organigramme projeté** — calquer les postes d'une vraie équipe sur la topologie des personas. Ce n'est pas parce que UX et graphisme sont des postes séparés dans une entreprise qu'ils doivent être des personas séparés. La question est toujours : est-ce que ces deux rôles me disent des choses **différentes** sur mes décisions ?
