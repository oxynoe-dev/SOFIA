# Retour d'expérience — Isolation des rôles de production

> Quand les personas commencent à produire, les frontières bougent.

---

## Le problème

La méthode SOFIA documente bien l'isolation des rôles de réflexion :
l'architecte ne code pas, le stratège ne touche pas au code, le dev ne
tranche pas sur l'architecture. Ces interdits créent la friction productive.

Mais quand les personas passent de la réflexion à la **production** —
rédiger un livre blanc, générer un PDF, publier sur les réseaux — les
frontières de périmètre deviennent floues. Qui publie quoi sur quel canal ?
Qui maintient les scripts de build ? Qui valide avant la sortie ?

## Ce qu'on a observé

Sur Katen, les scripts de publication étaient dispersés dans les workspaces
individuels : `maturation/bin/publish-*.py` chez Winston,
`graphisme/tools/build_pptx.py` chez Sofia. Résultat :

- L'architecte ne pouvait pas auditer les scripts sans sortir de son périmètre
- Le dev ne pouvait pas vérifier la qualité du code
- Personne n'avait de vue d'ensemble sur la chaîne de publication

## La solution

Deux décisions :

**1. Séparer réflexion et production dans les rôles.** Un persona qui
réfléchit ET produit le livrable final est juge et partie. La friction
disparaît. Sur Katen : Sofia produit (tous canaux), Nora challenge
(UX, accessibilité). Celle qui décide de la forme est celle qui la livre.
Celle qui challenge ne produit pas.

**2. Centraliser les scripts dans `shared/tools/`.** Chaque persona
déclenche ses scripts, mais le code vit dans un espace visible par tous.
L'architecte audite la cohérence, le dev audite la qualité, l'UX audite
l'output.

## Pour ton projet

Quand tes personas commencent à produire des livrables publics :
- Pose la question "qui publie quoi sur quel canal" explicitement
- Sépare le producteur du challenger — celui qui rédige n'est pas celui
  qui valide
- Mets les scripts de publication dans un espace lisible par tous
- L'orchestrateur valide avant toute sortie (devoir 3 de la méthode)

L'isolation de la réflexion est dans les fiches personas. L'isolation de
la production est dans les conventions de publication. Les deux sont
nécessaires.

## Multi-support — quand un livrable existe sur plusieurs canaux

Le problème s'aggrave quand un même contenu doit exister en markdown,
PDF, HTML et visuels réseaux. La question n'est plus seulement "qui
publie" mais "qui possède quelle transformation".

### Ce qu'on a observé

Sans contrat clair sur les canaux, les tâches tombent entre les chaises :
- Le rédacteur modifie le markdown, personne ne rebuild le PDF
- Le graphiste produit des visuels, personne ne les intègre au site
- Le build script existe mais personne ne sait qui le déclenche

### La règle

**Un canal = un propriétaire.** Le persona qui produit le livrable
pour un canal donné est responsable du déclenchement, de la cohérence
et de la mise à jour. Les autres challengent via review — ils ne
produisent pas.

| Canal | Propriétaire | Challengers |
|-------|-------------|-------------|
| Markdown source | Rédacteur | Architecte (structure), Chercheur (sources) |
| PDF/HTML généré | Graphiste | UX (accessibilité), Rédacteur (contenu) |
| Visuels réseaux | Graphiste | Stratège (message), UX (lisibilité) |
| Site web | Dev ou Graphiste | UX (parcours), Architecte (cohérence) |

L'orchestrateur valide avant toute sortie — quel que soit le canal.
