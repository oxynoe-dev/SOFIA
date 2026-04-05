# Retour d'experience — Contamination factuelle

> Le repo n'est pas une source de verite pour les faits. Il l'a jamais ete.

---

## Le probleme

Les LLMs ne comptent pas, ne calculent pas les durees, et privilegient
la coherence interne sur la verite externe. Une donnee approximative
entree une fois — parfois par l'humain, parfois hallucinee par l'IA —
sera propagee dans tous les documents generes ensuite.

Plus le repo grandit, plus l'erreur devient invisible. Elle *ressemble*
a de la coherence parce que chaque document contamine renforce les autres.
L'IA ne doute pas d'une donnee qu'elle retrouve dans 10 fichiers du repo.
Le fait qu'elle l'ait elle-meme ecrite dans ces 10 fichiers n'entre pas
dans son raisonnement.

## Cas reel — Katen

Le PO a utilise "15 ans" pour decrire sa duree de reflexion sur le projet.
C'etait une approximation — la vraie duree est de 18 ans (2008-2026).
L'IA a repris ce chiffre, l'a propage dans ~30 documents, et l'a stabilise.

Audit :
- ~30 documents actifs contenaient "14 ans" ou "15 ans" au lieu de "18 ans"
- ~12 documents dataient le concept original "2010-2012" au lieu de "2008-2012"
- 2 fichiers dataient l'arXiv "(2010)" au lieu de "(2011)"

L'erreur venait du PO lui-meme. L'IA l'a amplifiee et rendue invisible.

## Le mecanisme

1. Une donnee approximative entre dans une session
2. L'IA la reprend sans verifier, la formule joliment, la propage
3. Chaque document contamine devient une source pour les sessions suivantes
4. L'erreur se stabilise — elle a l'air correcte parce qu'elle est
   coherente avec les autres documents contamines

C'est un **effet de renforcement mutuel**. Le meme phenomene existe a
l'echelle du web (model collapse, Habsburg AI) — mais a l'echelle du
web, c'est irreversible. Dans un repo Voix, c'est tracable et corrigeable.
A condition que l'humain verifie.

## Ce qui est vulnerable

- **Dates et durees** — les LLMs ne calculent pas les ecarts temporels
- **Chiffres** — compteurs, metriques, quantites
- **Noms propres** — variations orthographiques, attributions erronees
- **References bibliographiques** — annees, auteurs, titres, contexte d'usage

## Les gardes-fous

### 1. Verification factuelle en continu

Pas en fin de projet — en continu. Chaque session qui manipule des faits
(dates, chiffres, refs) devrait inclure une passe de verification.
C'est le devoir 1 de la methode.

### 2. Passes de decontamination

Audits cibles sur les donnees les plus sensibles, a intervalles reguliers.
Sur Katen, un audit a identifie ~55 occurrences dans ~42 fichiers en une
session. C'est faisable — a condition de le planifier.

### 3. Source de verite explicite

Les faits critiques du projet doivent etre declares une fois, dans un
document de reference, et toujours verifies contre cette source. Pas
contre le repo — contre la source.

## Pour ton projet

Ce n'est pas un defaut de la methode. C'est une propriete de la
technologie sous-jacente. Les erreurs de precision sont normales —
les LLMs privilegient la vraisemblance sur la verite.

L'humain est le seul garde-fou. La methode doit le dire explicitement,
et l'humain doit l'integrer comme pratique, pas comme principe abstrait.

Et c'est un des arguments les plus forts en faveur de la methode Voix :
dans un monde ou le web se contamine irreversiblement, un repo structure
avec des reviews croisees est un des rares espaces ou la decontamination
reste possible.
