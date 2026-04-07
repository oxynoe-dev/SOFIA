# Retour d'expérience — Calibrage des personas

> Définir par le média, pas seulement par la compétence.

---

## Le problème

Les fiches personas initiales définissaient les rôles par compétence métier :
"UI Designer", "UX Lead", "Dev full stack". Ça suffit pour la réflexion —
l'architecte spécifie, le dev implémente, le stratège questionne.

Ça ne suffit plus quand les personas commencent à **produire**. Quand un
même contenu doit exister en markdown, en PDF, en HTML et en visuel pour
les réseaux — qui est responsable de chaque transformation ? "UI Designer"
ne dit rien sur ce point.

## Ce qu'on a observé

Sur Katen, trois personas produisaient du contenu pour des canaux de
diffusion, chacun avec ses propres outils, sans contrat clair sur les
frontières. Le livre bleu SOFIA a révélé le problème : Winston le rédige,
Sofia le met en forme PDF, mais qui produit la version web ? Les scripts
de publication de Winston généraient du HTML — ça chevauchait le périmètre
de Nora.

## L'apprentissage

Définir un persona par le "quoi" (design UI) ne suffit pas. Il faut aussi
le "pour quel média" :

- **Winston** : markdown source (rédaction)
- **Sofia** : PDF, PPTX, visuels réseaux, assets web (production multi-support)
- **Nora** : rien — elle challenge, elle ne livre pas

Le média clarifie la frontière là où la compétence la brouille. Sofia et
Nora ont toutes les deux des compétences en design. C'est le média qui
les sépare : Sofia produit sur tous les canaux, Nora challenge l'output.

## Pour ton projet

Quand tu calibres un persona, pose deux questions :
1. **Quoi** — quelle compétence ?
2. **Sur quel média** — quel format de sortie ?

Si deux personas ont la même compétence mais des médias différents, la
frontière est claire. Si deux personas ont le même média, tu as un conflit
de périmètre à résoudre.

Le calibrage n'est pas un exercice de jour 1. Il évolue avec l'usage.
Prévois de revisiter les fiches personas quand les rôles de production
émergent — et ils émergent toujours.
