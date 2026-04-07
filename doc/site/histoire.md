---
de: winston
pour: sofia, nora
type: contenu
date: 2026-04-05
objet: Histoire de la méthode SOFIA — sous-page site
source: livre-bleu-voix.md, doc/winston-style.md, cadrage PO
---

# Histoire

[Olivier Cugnon de Sévricourt](https://www.linkedin.com/in/oliviercds/) — ingénieur de formation (ESIEE Paris 2006), architecte SI de métier. Vingt ans de systèmes complexes — des Petri nets de 2008 aux pipelines LLM de 2026.

---

## Le problème de départ — le contexte ne tient pas

Début 2026. Je travaille avec un LLM sur un projet logiciel. Ça avance. Mais très vite, un mur : la fenêtre de contexte.

Le LLM oublie. Pas un peu — structurellement. Une conversation de deux heures, et il perd le fil. Les décisions prises en début de session n'existent plus en fin de session. Le contexte s'évapore.

La question n'est pas "comment rendre le LLM plus intelligent". La question est : comment ne pas perdre ce qu'on construit avec lui ?

---

## Les fichiers comme mémoire

La réponse est simple, presque banale : sortir le contexte de la conversation. Le poser dans des fichiers. Des notes, des specs, des reviews, des décisions. Structurés, nommés, versionnés.

Le LLM ne se souvient pas ? Pas grave. Les fichiers, eux, restent. À chaque session, on recharge ce qui compte. Le contexte n'est plus dans la tête de la machine — il est dans le repo.

Ce qui ressemblait à un bricolage est devenu un protocole. Les artefacts ne sont pas un sous-produit du travail. Ils sont le travail. Écrire force à clarifier. Structurer force à penser. La lenteur du fichier par rapport au chat n'est pas un défaut — c'est le mécanisme qui produit de la clarté.

---

## La séparation des dépendances

Le vrai tournant. Un seul contexte pour tout — architecture, code, stratégie, rédaction, UX — ça ne tient pas. Les sujets se contaminent. Le LLM mélange les niveaux. On parle d'architecture et il glisse vers l'implémentation. On parle de stratégie et il dérive vers le code.

La solution : isoler. Un contexte par domaine. Des instructions spécifiques. Des périmètres. Des interdits.

L'architecte ne code pas. Le développeur ne décide pas de l'architecture. Le stratège n'a pas accès au code. Chacun son espace, ses fichiers, ses règles.

Ce n'est pas une théorie des organisations. C'est de la gestion de dépendances. Le même réflexe qu'en ingénierie logicielle : quand tout dépend de tout, rien ne marche. On isole, on définit des interfaces, on contrôle les échanges.

Les personas sont nés de là — pas d'une envie de simuler une équipe, mais d'un besoin technique de séparer les préoccupations.

---

## La friction — ce qui émerge de l'isolation

Quand les personas sont isolés, quelque chose d'inattendu se produit. Ils ne sont plus d'accord.

L'architecte bloque une implémentation qui va trop vite. Le stratège remet en question une priorité technique. La chercheuse signale qu'une référence ne tient pas. La graphiste refuse un thème qui ne porte pas l'identité du projet. L'UX questionne un flux qui satisfait le développeur mais perd l'utilisateur.

Ce n'était pas prévu. C'est arrivé parce que les contraintes forcent des angles différents. Un LLM généraliste dit oui à tout. Un LLM contraint par un rôle et des interdits — il pousse dans sa direction.

La friction n'est pas un problème à résoudre. C'est le mécanisme qui révèle les angles morts. Si tous les personas sont d'accord, ils ne servent à rien.

---

## L'émergence — un persona à la fois

La méthode n'a pas été conçue en avance. Elle a grandi avec le projet.

Un persona au démarrage. Deux quand le premier est calibré. Trois quand le besoin est clair. Sept au total — pas par symétrie théorique, parce que chaque manque constaté a produit un nouveau rôle.

Chaque ajout a un coût : du temps de calibrage, de la complexité d'orchestration, du contexte à maintenir. Ce coût n'est justifié que par un manque réel — un angle mort que personne ne couvre, une compétence que les personas existants ne portent pas.

210+ sessions. 62 ADR documentées. Des échecs tracés. La méthode est le sous-produit d'un travail réel, pas d'un exercice de pensée.

---

## La thèse — après coup

C'est seulement en regardant ce que la méthode avait produit que la thèse s'est formulée.

Il est possible d'aller plus vite et mieux à ressources humaines constantes. Pas moins de gens. Les mêmes gens, augmentés. Pas remplacés — amplifiés.

L'IA amplifie. Elle n'invente pas. Si on lui donne du vide, elle produit du vide bien formulé. Si on lui donne des années de conviction sur un problème réel, elle construit avec.

La friction intentionnelle entre des rôles contraints, avec un humain qui arbitre — c'est ce qui transforme un outil de génération en outil de pensée.

Ce n'est pas une théorie. C'est ce qui est sorti du terrain quand on a résolu les problèmes un par un : le contexte qui ne tient pas, les fichiers comme mémoire, la séparation des dépendances, et la friction qui émerge de l'isolation.

La méthode est née des contraintes. La thèse est venue après.
