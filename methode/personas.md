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

Un bon persona définit **six choses** :

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
- Personne ne décide à la place de l'humain

Les interdits sont ce qui crée la friction productive. Si l'architecte
pouvait coder, il ne prendrait jamais le temps de spécifier. Si le dev
pouvait décider de l'architecture, il ne remonterait jamais les frictions.

### 6. Collaboration

Comment le persona interagit avec les autres :

| Avec | Mode |
|------|------|
| Architecte | Le dev implémente les contrats et remonte les frictions |
| UX | Le dev signale les contraintes techniques sur les specs UI |
| Chercheur | Le dev consulte quand une implémentation touche au modèle formel |

La table de collaboration empêche les personas de travailler en silo.

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
