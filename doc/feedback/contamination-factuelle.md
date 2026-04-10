# Retour d'expérience — Contamination factuelle

> Le repo n'est pas une source de vérité pour les faits. Il l'a jamais été.

---

## Le problème

Les LLMs ne comptent pas, ne calculent pas les durées, et privilégient
la cohérence interne sur la vérité externe. Une donnée approximative
entrée une fois — parfois par l'orchestrateur, parfois hallucinée par l'IA —
sera propagée dans tous les documents générés ensuite.

Plus le repo grandit, plus l'erreur devient invisible. Elle *ressemble*
à de la cohérence parce que chaque document contaminé renforce les autres.
L'IA ne doute pas d'une donnée qu'elle retrouve dans 10 fichiers du repo.
Le fait qu'elle l'ait elle-même écrite dans ces 10 fichiers n'entre pas
dans son raisonnement.

## Cas réel — Katen

L'orchestrateur a utilisé "15 ans" pour décrire sa durée de réflexion sur le projet.
C'était une approximation — la vraie durée est de 18 ans (2008-2026).
L'IA a repris ce chiffre, l'a propagé dans ~30 documents, et l'a stabilisé.

Audit :
- ~30 documents actifs contenaient "14 ans" ou "15 ans" au lieu de "18 ans"
- ~12 documents dataient le concept original "2010-2012" au lieu de "2008-2012"
- 2 fichiers dataient l'arXiv "(2010)" au lieu de "(2011)"

L'erreur venait de l'orchestrateur lui-même. L'IA l'a amplifiée et rendue invisible.

## Le mécanisme

1. Une donnée approximative entre dans une session
2. L'IA la reprend sans vérifier, la formule joliment, la propage
3. Chaque document contaminé devient une source pour les sessions suivantes
4. L'erreur se stabilise — elle a l'air correcte parce qu'elle est
   cohérente avec les autres documents contaminés

C'est un **effet de renforcement mutuel**. Le même phénomène existe à
l'échelle du web (model collapse, Habsburg AI) — mais à l'échelle du
web, c'est irréversible. Dans un repo SOFIA, c'est traçable et corrigeable.
À condition que l'orchestrateur vérifie.

## Ce qui est vulnérable

- **Dates et durées** — les LLMs ne calculent pas les écarts temporels
- **Chiffres** — compteurs, métriques, quantités
- **Noms propres** — variations orthographiques, attributions erronées
- **Références bibliographiques** — années, auteurs, titres, contexte d'usage

## Trois classes d'erreur de sourcing

La contamination ne se limite pas aux faits bruts. Les sources
elles-mêmes peuvent être problématiques de trois façons :

**Classe 1 — Assertion sans source.** Le texte affirme quelque chose
comme un fait, aucune source ne le soutient. L'IA a produit une
assertion vraisemblable à partir de sa distribution, pas d'une donnée.

**Classe 2 — Source qui contredit l'assertion.** La source existe et
est citée — mais elle dit autre chose que ce que le texte prétend.
L'IA a "résumé" en déformant, ou a confondu deux sources.

**Classe 3 — Source vraie, usage incohérent.** La source est correcte
et fidèlement citée — mais elle ne dit pas ce que le contexte d'usage
requiert. Exemple : citer une étude sur des agents IA pour justifier
un comportement humain, sans caveat sur le transfert.

La classe 3 est la plus dangereuse : tout a l'air correct, la source
est vérifiable, le résumé est fidèle. Seul quelqu'un qui comprend le
contexte d'usage peut détecter l'incohérence.

## Les gardes-fous

### 1. Vérification factuelle en continu

Pas en fin de projet — en continu. Chaque session qui manipule des faits
(dates, chiffres, refs) devrait inclure une passe de vérification.
C'est le devoir 1 de la méthode.

### 2. Passes de décontamination

Audits ciblés sur les données les plus sensibles, à intervalles réguliers.
Sur Katen, un audit a identifié ~55 occurrences dans ~42 fichiers en une
session. C'est faisable — à condition de le planifier.

### 3. Source de vérité explicite

Les faits critiques du projet doivent être déclarés une fois, dans un
document de référence, et toujours vérifiés contre cette source. Pas
contre le repo — contre la source.

## Pour ton projet

Ce n'est pas un défaut de la méthode. C'est une propriété de la
technologie sous-jacente. Les erreurs de précision sont normales —
les LLMs privilégient la vraisemblance sur la vérité.

L'orchestrateur est le seul garde-fou. La méthode doit le dire explicitement,
et l'orchestrateur doit l'intégrer comme pratique, pas comme principe abstrait.

Et c'est un des arguments les plus forts en faveur de la méthode SOFIA :
dans un monde où le web se contamine irréversiblement, un repo structuré
avec des reviews croisées est un des rares espaces où la décontamination
reste possible.
