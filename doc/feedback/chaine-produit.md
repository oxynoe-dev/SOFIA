# Retour d'experience — Chaine produit

> Specifier, implementer, challenger. Trois roles, un cycle, zero raccourci.

---

## Le pattern

La chaine produit est le cycle de base de Katen. C'est le pattern le plus
ancien, le plus rode, et le plus revelateur de la methode Voix en action.

```
PO identifie un besoin ou une friction
  → ouvre session architecte

Architecte specifie
  → ADR, contrats d'interface, specs formelles
  → ne code pas — si la spec est floue, le dev le dira

Dev implemente
  → code, tests, retours de frictions
  → ne reinterprete pas — si la spec est ambigue, il remonte

UX challenge
  → review des flux, etats visuels, accessibilite
  → ne produit pas le code — elle specifie les comportements

Chercheuse verifie
  → invariantes formelles, coherence avec le modele Petri-net
  → ne tranche pas sur l'archi — elle valide la theorie

PO arbitre et tranche
  → quand les personas divergent, l'humain decide
  → la decision est tracee (ADR, note, session)
```

## Ce qu'on a observe sur Katen

### La spec force la clarte

Mira ne code pas. C'est la contrainte la plus productive de l'equipe.
Parce qu'elle ne peut pas "montrer dans le code", elle est obligee de
specifier clairement — contrats d'interface, etats attendus, cas limites.
Le resultat : 62 ADR, 24 principes d'architecture. Des specs qu'Axel
peut implementer sans deviner.

Sans cette contrainte, l'architecte saute directement au pseudo-code.
La spec reste floue. Le dev interprete. Les bugs sont structurels,
pas techniques.

### La friction d'implementation remonte les vrais problemes

Axel ne contourne pas. Quand un contrat d'interface genere une complexite
inattendue, il le signale plutot que de bricoler. Ces remontees ont change
des ADR — pas parce que la spec etait mauvaise, mais parce que le terrain
revele ce que la theorie ne voit pas.

Cas concret : la parallelisation des operateurs. Mira bloque ("pas
maintenant, la roadmap a des priorites avant"). Lea confirme par un
angle orthogonal ("aucun interet pour la recherche"). Deux refus, deux
raisons independantes. Le sujet est reporte. Trois semaines plus tard,
le design revient — meilleur qu'il ne l'aurait ete.

### L'UX challenge ce que le dev ne voit pas

Nora questionne les flux d'onboarding qui satisfont le developpeur mais
perdent l'utilisateur. Elle ne code pas — elle specifie les comportements
attendus. Axel remonte les contraintes techniques. La friction entre les
deux produit des interfaces qui tiennent techniquement ET humainement.

### La chercheuse ancre dans le formel

Lea ne tranche pas sur l'architecture. Mais quand une implementation
touche aux invariantes du modele Petri-net — firing policy, etats des
connexions, reversibilite — elle verifie. Son "ca ne tient pas" a la
meme autorite qu'un test qui echoue : on ne passe pas en force.

### Le PO porte le contexte

Le PO est le seul a voir toutes les sessions. Il filtre, reformule,
contextualise. Quand Mira depose une review pour Axel, le PO ajoute :
"on a decide hier avec Marc de decaler la publication — ca change la
priorite de cette spec." Ce contexte, aucun persona ne l'a seul.

## Les ADR comme colonne vertebrale

Chaque decision structurante produit un ADR. Le format est standard :
contexte, decision, consequences, statut. L'ADR n'est pas de la
bureaucratie — c'est de la memoire.

Un ADR non ecrit est une decision qui sera remise en question trois
sessions plus tard par quelqu'un qui n'en avait pas connaissance.
Sur 210+ sessions, ca arrive vite.

Les ADR passent potentiellement par 4 challengers :
- **Mira** — coherence avec l'architecture cible
- **Axel** — faisabilite d'implementation
- **Lea** — rigueur formelle (quand le sujet touche au modele)
- **Marc** — impact strategique (quand le sujet touche au positionnement)

Le PO tranche. L'ADR est accepte, rejete ou reporte. Le statut est trace.

## Pour ton projet

La chaine produit est le cas d'usage fondamental de Voix. Quelques regles :

- **L'architecte ne code pas.** C'est la contrainte numero un. Si ton
  architecte peut coder, il ne specifiera jamais clairement.
- **Le dev ne reinterprete pas.** Si la spec est floue, il remonte. Il
  ne devine pas. La friction est le signal, pas le bruit.
- **L'UX ne produit pas le code.** Elle specifie les comportements. Le
  dev remonte les contraintes. La friction entre les deux est le mecanisme
  qui produit de bonnes interfaces.
- **Trace tout.** ADR, sessions, reviews. Si ce n'est pas trace, ca
  n'existe pas.
- **Le PO arbitre.** Quand deux personas divergent, l'humain tranche.
  Pas le persona le plus eloquent. L'humain.
