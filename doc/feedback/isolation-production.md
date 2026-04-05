# Retour d'experience — Isolation des roles de production

> Quand les personas commencent a produire, les frontieres bougent.

---

## Le probleme

La methode Voix documente bien l'isolation des roles de reflexion :
l'architecte ne code pas, le stratege ne touche pas au code, le dev ne
tranche pas sur l'architecture. Ces interdits creent la friction productive.

Mais quand les personas passent de la reflexion a la **production** —
rediger un livre blanc, generer un PDF, publier sur les reseaux — les
frontieres de perimetre deviennent floues. Qui publie quoi sur quel canal ?
Qui maintient les scripts de build ? Qui valide avant la sortie ?

## Ce qu'on a observe

Sur Katen, les scripts de publication etaient disperses dans les workspaces
individuels : `maturation/bin/publish-*.py` chez Winston,
`graphisme/tools/build_pptx.py` chez Sofia. Resultat :

- L'architecte ne pouvait pas auditer les scripts sans sortir de son perimetre
- Le dev ne pouvait pas verifier la qualite du code
- Personne n'avait de vue d'ensemble sur la chaine de publication

## La solution

Deux decisions :

**1. Separer reflexion et production dans les roles.** Un persona qui
reflechit ET produit le livrable final est juge et partie. La friction
disparait. Sur Katen : Sofia produit (tous canaux), Nora challenge
(UX, accessibilite). Celle qui decide de la forme est celle qui la livre.
Celle qui challenge ne produit pas.

**2. Centraliser les scripts dans `shared/tools/`.** Chaque persona
declenche ses scripts, mais le code vit dans un espace visible par tous.
L'architecte audite la coherence, le dev audite la qualite, l'UX audite
l'output.

## Pour ton projet

Quand tes personas commencent a produire des livrables publics :
- Pose la question "qui publie quoi sur quel canal" explicitement
- Separe le producteur du challenger — celui qui redige n'est pas celui
  qui valide
- Mets les scripts de publication dans un espace lisible par tous
- Le PO valide avant toute sortie (devoir 3 de la methode)

L'isolation de la reflexion est dans les fiches personas. L'isolation de
la production est dans les conventions de publication. Les deux sont
necessaires.
