# Friction intentionnelle

> Si tout le monde est d'accord, personne ne pense.

---

## Le problème du LLM complaisant

Un LLM seul dit oui. Toujours. Tu proposes une architecture bancale,
il l'implémente. Tu écris une spec floue, il la code en devinant.
Tu oublies un cas limite, il ne le mentionne pas.

Ce n'est pas de la collaboration. C'est de l'exécution servile.

## La friction comme mécanisme

Dans une vraie équipe, la qualité vient des désaccords :
- Le dev dit "cette spec n'est pas codable"
- L'architecte dit "cette implémentation casse un contrat"
- Le stratège dit "personne ne paiera pour ça"
- L'UX dit "l'utilisateur ne comprendra jamais ce flux"

Ces frictions ne sont pas des bugs. Ce sont des **signaux**.
Ils forcent à clarifier, à trancher, à documenter.

SOFIA reproduit ce mécanisme avec des personas contraints.

## Comment la friction émerge

La friction n'est pas un paramètre qu'on active. Elle **émerge**
des contraintes posées sur les personas :

| Contrainte | Friction produite |
|------------|-------------------|
| L'architecte ne code pas | Il est obligé de spécifier clairement → le dev peut challenger la spec |
| Le dev ne décide pas de l'archi | Il est obligé de remonter les frictions → l'architecte doit les résoudre |
| Le stratège n'a pas accès au code | Il est obligé de questionner la valeur → l'équipe doit justifier ses choix |
| L'UX ne valide pas la faisabilité | Elle est obligée de consulter le dev → les contraintes techniques sont explicites |

## L'arbitre

La friction sans arbitre est du chaos. Deux personas qui se contredisent
indéfiniment ne produisent rien.

**L'orchestrateur est l'arbitre. Toujours.**

- Les personas exposent les tensions
- L'orchestrateur écoute, questionne, puis tranche
- La décision est tracée (ADR, note, session)
- Les personas appliquent la décision, même s'ils l'ont challengée

Un persona ne force jamais l'acceptation. Il pose les points bloquants,
il ne vote pas.

## Les artefacts comme vecteur de friction

Les personas ne "discutent" pas en live. Ils échangent par **fichiers** :

- L'architecte dépose une review d'un ADR
- Le dev répond par un signalement de friction d'implémentation
- Le stratège dépose une note avec 3 questions qui dérangent
- L'UX produit une review de design avec observations priorisées

Ce protocole est plus lent qu'un chat. C'est voulu :
- L'écriture force la structuration de la pensée
- Les fichiers sont versionnés et traçables
- N'importe qui peut relire l'échange plus tard

## Signes que la friction fonctionne

- Les personas disent "non" ou "pas mon rôle"
- Des désaccords apparaissent entre personas
- L'orchestrateur doit trancher régulièrement
- Les specs sont plus précises qu'avant
- Les décisions sont documentées avec le contexte

## Signes que la friction est absente

- Tous les personas sont d'accord sur tout
- Personne ne dit non
- Les specs restent vagues et personne ne le signale
- L'orchestrateur n'a jamais besoin de trancher
- Pas de trace des décisions

Si tu reconnais la deuxième liste, tes personas sont trop complaisants
ou leurs contraintes trop lâches. Revois les interdits.

## Mesurer la friction

La friction est qualitative — pas mesurable par un compteur. Mais elle
peut être **signalée** dans les artefacts. Cinq marqueurs qualifient
la position d'un persona sur une proposition :

| Marqueur | Signification |
|----------|--------------|
| **✓ Juste** | Position correcte — arguments additionnels fournis |
| **~ Contestable** | Position défendable mais pas la seule |
| **⚡ Simplification** | Le réel est plus complexe que ce qui est présenté |
| **◐ Angle mort** | Quelque chose que l'auteur ne voit pas ou choisit de ne pas voir |
| **✗ Faux** | Factuellement incorrect ou logiquement incohérent |

### Usage

Les personas qualifient leurs positions dans les **notes et reviews**
avec ces marqueurs. Usage optionnel, pas mécanique — ne classifier que
les affirmations qui le méritent.

### Ce que ça révèle

Un scan des marqueurs sur un artefact donne le niveau de friction :
- Que des ✓ → friction absente — signal d'alerte
- Mix ✓/~/⚡ → friction saine
- Présence de ◐ ou ✗ → tension à traiter

Si un persona ne produit que des ✓ sur une longue période, c'est un
signal de domestication — il s'est aligné sur le cadre de pensée de
l'orchestrateur.
