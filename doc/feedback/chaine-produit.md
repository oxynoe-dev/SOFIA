# Retour d'expérience — Chaîne produit

> Spécifier, implémenter, challenger. Trois rôles, un cycle, zéro raccourci.

---

## Le pattern

La chaîne produit est le cycle de base de Katen. C'est le pattern le plus
ancien, le plus rodé, et le plus révélateur de la méthode SOFIA en action.

```
PO identifie un besoin ou une friction
  → ouvre session architecte

Architecte spécifie
  → ADR, contrats d'interface, specs formelles
  → ne code pas — si la spec est floue, le dev le dira

Dev implémente
  → code, tests, retours de frictions
  → ne réinterprète pas — si la spec est ambiguë, il remonte

UX challenge
  → review des flux, états visuels, accessibilité
  → ne produit pas le code — elle spécifie les comportements

Chercheuse vérifie
  → invariantes formelles, cohérence avec le modèle Petri-net
  → ne tranche pas sur l'archi — elle valide la théorie

PO arbitre et tranche
  → quand les personas divergent, l'humain décide
  → la décision est tracée (ADR, note, session)
```

## Ce qu'on a observé sur Katen

### La spec force la clarté

Mira ne code pas. C'est la contrainte la plus productive de l'équipe.
Parce qu'elle ne peut pas "montrer dans le code", elle est obligée de
spécifier clairement — contrats d'interface, états attendus, cas limites.
Le résultat : 62 ADR, 24 principes d'architecture. Des specs qu'Axel
peut implémenter sans deviner.

Sans cette contrainte, l'architecte saute directement au pseudo-code.
La spec reste floue. Le dev interprète. Les bugs sont structurels,
pas techniques.

### La friction d'implémentation remonte les vrais problèmes

Axel ne contourne pas. Quand un contrat d'interface génère une complexité
inattendue, il le signale plutôt que de bricoler. Ces remontées ont changé
des ADR — pas parce que la spec était mauvaise, mais parce que le terrain
révèle ce que la théorie ne voit pas.

Cas concret : la parallélisation des opérateurs. Mira bloque ("pas
maintenant, la roadmap a des priorités avant"). Léa confirme par un
angle orthogonal ("aucun intérêt pour la recherche"). Deux refus, deux
raisons indépendantes. Le sujet est reporté. Trois semaines plus tard,
le design revient — meilleur qu'il ne l'aurait été.

### L'UX challenge ce que le dev ne voit pas

Nora questionne les flux d'onboarding qui satisfont le développeur mais
perdent l'utilisateur. Elle ne code pas — elle spécifie les comportements
attendus. Axel remonte les contraintes techniques. La friction entre les
deux produit des interfaces qui tiennent techniquement ET humainement.

### La chercheuse ancre dans le formel

Léa ne tranche pas sur l'architecture. Mais quand une implémentation
touche aux invariantes du modèle Petri-net — firing policy, états des
connexions, réversibilité — elle vérifie. Son "ça ne tient pas" a la
même autorité qu'un test qui échoue : on ne passe pas en force.

### Le PO porte le contexte

Le PO est le seul à voir toutes les sessions. Il filtre, reformule,
contextualise. Quand Mira dépose une review pour Axel, le PO ajoute :
"on a décidé hier avec Marc de décaler la publication — ça change la
priorité de cette spec." Ce contexte, aucun persona ne l'a seul.

## Les ADR comme colonne vertébrale

Chaque décision structurante produit un ADR. Le format est standard :
contexte, décision, conséquences, statut. L'ADR n'est pas de la
bureaucratie — c'est de la mémoire.

Un ADR non écrit est une décision qui sera remise en question trois
sessions plus tard par quelqu'un qui n'en avait pas connaissance.
Sur 210+ sessions, ça arrive vite.

Les ADR passent potentiellement par 4 challengers :
- **Mira** — cohérence avec l'architecture cible
- **Axel** — faisabilité d'implémentation
- **Léa** — rigueur formelle (quand le sujet touche au modèle)
- **Marc** — impact stratégique (quand le sujet touche au positionnement)

Le PO tranche. L'ADR est accepté, rejeté ou reporté. Le statut est tracé.

## Pour ton projet

La chaîne produit est le cas d'usage fondamental de SOFIA. Quelques règles :

- **L'architecte ne code pas.** C'est la contrainte numéro un. Si ton architecte peut coder, il ne spécifiera jamais clairement.
- **Le dev ne réinterprète pas.** Si la spec est floue, il remonte. Il ne devine pas. La friction est le signal, pas le bruit.
- **L'UX ne produit pas le code.** Elle spécifie les comportements. Le dev remonte les contraintes. La friction entre les deux produit de bonnes interfaces.
- **Trace tout.** ADR, sessions, reviews. Si ce n'est pas tracé, ça n'existe pas.
- **L'humain arbitre.** Quand deux personas divergent, l'humain tranche. Pas le persona le plus éloquent.
