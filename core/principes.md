# Principes de SOFIA

> Les principes invariants de la methode.

---

## 1. La friction est productive

La friction est le mecanisme par lequel des positions divergentes produisent de meilleures decisions. Elle n'est pas un defaut a minimiser — elle est une propriete recherchee du systeme.

L'absence de friction est un signal d'alerte. La friction sans arbitrage est du chaos.

## 2. L'orchestrateur est l'unique arbitre

Les personas proposent, contestent, produisent. Seul l'orchestrateur tranche. Un persona ne valide pas ses propres propositions et ne force pas l'acceptation d'une decision.

## 3. Chaque voix compte

Un persona est un role avec une responsabilite, un perimetre et des contraintes. Il repond a un besoin identifie. Un persona qui n'est plus ecoute n'a plus de raison d'exister.

## 4. La contrainte force la qualite

C'est la limitation qui produit la friction utile. Un persona se definit par ce qu'il **ne fait pas** avant ce qu'il fait :

- Un architecte qui ne code pas est contraint de specifier clairement
- Un developpeur qui ne decide pas de l'architecture est contraint de questionner
- Un stratege sans acces au code est contraint de raisonner en valeur

Un persona sans contrainte ne genere pas de friction.

## 5. Les artefacts sont le protocole

Les personas n'echangent pas directement. Tout passe par des artefacts traces, adressables et lisibles : reviews, notes, specs.

L'echange par artefact est plus lent qu'un echange direct. C'est une propriete, pas un defaut — la lenteur force la clarte. Le format et le systeme de persistance sont des choix d'implementation (voir `implementation/implementation.md`).

## 6. Tout est trace

Chaque session produit une trace identifiable. Chaque echange inter-personas produit un artefact. Ce qui n'est pas trace n'existe pas pour les sessions suivantes.

## 7. Commence petit, itere

La methode grandit avec le projet. On demarre avec le minimum necessaire. L'ajout d'un persona repond a un besoin constate, pas anticipe.
