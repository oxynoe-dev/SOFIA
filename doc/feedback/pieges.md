# Pièges et erreurs classiques

> Ce qui ne marche pas, pour que tu ne le découvres pas toi-même.

---

## 1. Trop de personas trop tôt

Tu n'as pas besoin de 5 personas au jour 1. Commence par 1.
Calibre-le. Ajoute le deuxième quand le besoin est clair.

**Signe** : tu as des personas que tu n'utilises jamais.
**Solution** : supprime les personas inutilisés. Sans remords.

## 2. Le persona complaisant

Un persona qui dit toujours oui ne sert à rien. C'est un assistant
avec un prénom.

**Signe** : le persona ne dit jamais "non", "ce n'est pas mon rôle",
ou "la spec est trop floue".
**Solution** : renforce les interdits dans la fiche persona et le CLAUDE.md.

## 3. Oublier les résumés de session

La prochaine session n'a aucun contexte sans résumé. Tu perdras
du temps à réexpliquer, ou pire, le persona partira dans une
direction incohérente avec la session précédente.

**Signe** : tu commences chaque session par 10 minutes d'explication.
**Solution** : le résumé est obligatoire dans le CLAUDE.md. Pas optionnel.

## 4. L'isolation molle

Un CLAUDE.md sans section Isolation est un CLAUDE.md cassé.
Le persona ira lire et écrire partout, et la friction disparaît.

**Signe** : l'architecte modifie du code, le dev réécrit des specs.
**Solution** : ajoute des frontières explicites. "Ne jamais lire/écrire
en dehors de X."

## 5. L'orchestrateur qui ne tranche pas

Les personas exposent des tensions. Si l'orchestrateur ne tranche pas,
les tensions s'accumulent et rien n'avance.

**Signe** : les mêmes questions ouvertes reviennent session après session.
**Solution** : tranche. Même si c'est imparfait. Un ADR "Accepted" vaut
mieux qu'un ADR "Proposed" éternel.

## 6. Confondre persona et assistant

Un persona n'est pas un assistant plus poli. C'est un rôle avec
des contraintes qui le forcent à penser différemment. Si tu retires
les contraintes, tu retrouves un assistant généraliste.

**Signe** : tu donnes les mêmes instructions à tous tes personas.
**Solution** : chaque persona a une posture, des interdits, un
périmètre **différents**. C'est la différence qui crée la valeur.

## 7. La session perdue

Claude Code peut crasher. L'app peut planter. Le contexte peut
se corrompre. Ça arrivera.

**Signe** : tu as perdu une semaine de travail.
**Solution** : les fichiers sont la seule source de vérité. Produis
des artefacts (ADR, specs, reviews) en permanence. Le résumé de
session est le minimum vital. Les fichiers survivent aux crashs.

## 8. Le dev qui ne flush jamais

Le persona développeur est différent des autres. Il code, il est
dans le flow, il a une session longue qui tourne en continu. Couper
pour un résumé de session casse le rythme.

Résultat : pas de résumé, pas de trace des décisions intermédiaires.
Le code est dans git, mais le **pourquoi** des choix d'implémentation
disparaît si la session crash.

**Signe** : ta session dev ne se ferme jamais et n'a aucun résumé.
**Pas de solution miracle** — c'est un compromis. Quelques pistes :
- Demander au dev de flush un résumé rapide à des points naturels
  (fin d'une feature, avant un refactoring)
- Accepter que le commit message et le code **sont** la trace du dev
- Compenser par des reviews plus fréquentes des autres personas

Les personas "penseurs" (architecte, stratège, chercheur) ont des
sessions courtes avec des livrables fichier. Le persona "faiseur"
a une session longue avec des livrables code. Ce n'est pas le même
rythme et ce n'est pas grave — mais il faut le savoir.

## 9. Copier les personas d'un autre projet

Les personas Katen sont calibrés pour Katen. Si tu les copies
sans les adapter, ils ne correspondront ni à ton projet, ni à
ta façon de travailler.

**Signe** : le persona parle de réseaux de Petri alors que tu fais
une app mobile.
**Solution** : utilise les exemples comme **référence de structure**,
pas comme contenu. Le guide SOFIA est là pour t'aider à concevoir
les tiens.
