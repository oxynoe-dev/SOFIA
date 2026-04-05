# Cas d'école — ADR-051 : quand l'architecte dit "pas maintenant"

> Friction productive entre un dev et une architecte. Personne n'a tort.

---

## Le contexte

Projet Katen, v0.21. Le développeur (Axel) propose un ADR pour ajouter
l'exécution concurrente via Web Workers au moteur. L'ADR est solide :
fondement théorique (réseaux de Petri, transitions indépendantes),
design propre (pool de workers, partition des fireables), opt-in.

## Ce qui se passe

L'architecte (Mira) review l'ADR et recommande **Deferred** :

- Pas de douleur mesurée — aucun benchmark ne montre un bottleneck CPU
- La roadmap a des priorités avant (cleanup engine, mode Code)
- Un point de sécurité (eval dans les workers) est non négociable
- Le protocole de test formel manque (principe D1 du projet)

La review est dure. 5 recommandations, 3 en priorité haute.

## Pourquoi c'est un bon exemple de friction

**Le dev n'a pas tort.** L'ADR anticipe un besoin réel. La concurrence
sera nécessaire quand le moteur traitera des compositions lourdes
(veille sur 200 sources, compute ML). Le design est prêt.

**L'architecte n'a pas tort.** L'ADR ajoute de la complexité au coeur
du moteur pour un besoin qui n'existe pas encore. Les principes du
projet disent "make it work, make it right, make it fast — dans cet
ordre". On n'est pas à l'étape "fast".

**La tension produit une meilleure décision :**
- L'ADR est conservé (pas rejeté — deferred)
- Le point eval est identifié comme non négociable → sera corrigé
- Le protocole de test sera écrit avant toute implémentation
- Le benchmark sera le trigger de réactivation

Sans la review, l'ADR aurait pu être implémenté trop tôt, ajoutant
de la complexité sur un player en cours de refactoring. Sans l'ADR,
le besoin de concurrence n'aurait pas été formalisé et serait arrivé
en urgence plus tard.

## Ce que ça illustre

1. **Les interdits créent la friction** — Mira ne code pas, donc
   elle ne peut pas "laisser passer" un ADR pour aller plus vite.
   Elle est obligée de le challenger sur les principes.

2. **Le dev remonte, l'architecte filtre** — Axel anticipe un besoin
   technique. Mira le confronte à la roadmap et aux principes. Les
   deux perspectives sont nécessaires.

3. **Deferred ≠ Rejected** — la décision n'est pas "non" mais
   "pas maintenant, et voici ce qu'il faudra corriger quand le
   moment viendra". Le travail d'Axel n'est pas perdu.

4. **L'humain tranche** — le PO lit la review, évalue, décide.
   Les personas ont exposé la tension. L'humain la résout.

## Le piège évité

Sans friction : le dev implémente la concurrence en v0.22, le
cleanup engine en v0.23 casse le player, la concurrence doit être
réécrite. Deux mois de travail perdus.

Avec friction : l'ADR attend que le player soit stable. Quand il
sera réactivé, le design sera meilleur et le player sera propre.
