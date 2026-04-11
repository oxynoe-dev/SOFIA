---
de: mira
nature: etude
statut: nouveau
date: 2026-04-11
objet: grammaire de derivation des personas SOFIA — v1 architecte
---

# Grammaire de dérivation des personas

> Ce document est un matériau architecte. Il attend une passe pédagogique.

---

## Filiation

En 1977, Christopher Alexander publie *A Pattern Language*[^1] — un système où chaque pattern naît du manque du précédent. Un bâtiment n'est pas conçu d'un bloc ; il se déplie, étape par étape, chaque décision créant le contexte de la suivante. Alexander appelait ça une **séquence générative**[^2].

En 1996, Alexander est invité à OOPSLA[^3] — la conférence de la communauté logicielle qui avait emprunté son vocabulaire pour les *design patterns*. Il leur dit, en substance : vous avez pris le catalogue, pas le processus. Un pattern isolé résout un problème. Une *grammaire* de patterns génère un tout cohérent. La différence est fondamentale.

C'est cette distinction que SOFIA reprend. Les personas ne sont pas un catalogue de rôles à choisir. Ce sont des positions qui se dérivent — chacune créant les conditions d'émergence de la suivante.

Le terme *grammaire de dérivation* vient de la théorie des langages formels (Chomsky, 1957)[^4] — un ensemble de règles de production qui transforment un état en un autre. On part du projet, on applique des règles, on dérive des personas. Stiny et Gips (1972)[^5] ont transposé cette idée au design avec les *shape grammars* — des règles formelles qui génèrent des formes par dérivation successive.

SOFIA combine les trois influences : le dépliement d'Alexander (chaque persona crée le contexte du suivant), le formalisme de Chomsky (des règles, pas des conseils), et la génération par dérivation de Stiny (un processus reproductible, pas un acte créatif).

---

## Pré-requis — les questions difficiles

Avant de toucher à SOFIA, réponds à ces questions. Si tu ne peux pas, la méthode ne te servira pas encore.

### L'intention

**Pourquoi tu ouvres ce projet ?** Pas "quel est le livrable" — quelle est la question qui te travaille, le problème qui te dérange, la thèse que tu veux éprouver.

Sans intention forte, SOFIA ne produit que du process à vide. Sept personas qui tournent sans direction, c'est de la bureaucratie simulée.

L'intention n'est pas un pré-requis qu'on coche une fois. C'est une discipline de **chaque session**. Avant d'ouvrir un échange avec un persona, pose-toi la question : "Pourquoi j'ouvre cette session *maintenant* ?" Si la réponse est "parce que c'est dans ma routine" — ferme la session.

### Trois questions de compétence

1. **Quel est ton domaine d'expertise ?** Pas ton titre — ton terrain. Ce sur quoi tu as une opinion fondée parce que tu l'as pratiqué, pas lu.
2. **Quelle est la décision la plus difficile de ton projet actuel ?** Si tu n'en vois pas, tu n'as pas encore de projet — tu as une idée.
3. **Où est-ce que tu te trompes le plus souvent ?** Si la réponse est "nulle part", tu n'es pas prêt pour la friction intentionnelle.

L'intention donne la direction. Les trois questions testent la compétence. Un expert sans intention produit de l'analyse stérile. Une intention sans expertise produit de la confusion convaincante.

### La condition cachée

L'IA amplifie. Elle n'invente pas.

Si tu arrives avec du vide, elle produit du vide bien formulé. Si tu arrives avec des années de conviction sur un problème réel, elle construit avec. La performance avec SOFIA dépend de ce que tu apportes — pas de la méthode elle-même.

Ce pré-requis n'est pas vérifiable par un test. C'est une honnêteté avec soi-même.

---

## Deux modes de dérivation

L'observation du terrain (instance Katen) révèle deux modes distincts. Ils ne s'opposent pas — ils se succèdent.

### Mode 1 — Bootstrap par projection

L'orchestrateur projette l'équipe dont le produit a besoin.

Ce n'est pas une dérivation par tension. C'est une décision pragmatique : "de quoi mon projet a besoin pour avancer ?" L'orchestrateur connaît son produit, il sait quels axes de compétence sont nécessaires.

**Règle B1** — Le bootstrap reflète les besoins du produit, pas un organigramme.
Ne crée pas "un architecte, un dev, un stratège" parce que c'est une équipe classique. Crée les rôles dont *ton* produit a besoin. Si ton projet n'a pas besoin de stratégie marché, ne crée pas de stratège.

**Règle B2** — Commence par les interdits, pas par les compétences.
Pour chaque persona, la première question est : "qu'est-ce qu'il ne fait PAS ?" Les interdits sont des garanties structurelles. Ils forcent la séparation des axes et empêchent un persona de tout couvrir.

**Règle B3** — Le nombre initial n'est pas contraint.
Rodin prescrit "un seul". Le terrain montre qu'un orchestrateur expérimenté peut bootstrapper 5 personas d'un coup s'il sait ce qu'il fait. Le risque de prolifération se gère par recalibrage, pas par contrainte au démarrage.

**Règle B4** — Le bootstrap n'est pas de l'émergence.
Les personas bootstrappés n'ont pas été "découverts" — ils ont été projetés. Ils devront être recalibrés par le travail. Le bootstrap est un point de départ, pas un résultat.

#### Exemple — Katen (moteur d'orchestration)

L'orchestrateur de Katen avait 18 ans de contexte sur un moteur formel. Le 4 mars 2026, il projette l'equipe dont le produit a besoin :

| Axe | Persona | Produit | Interdit principal | Posture |
|-----|---------|---------|-------------------|---------|
| Architecture système | Mira | ADR, specs, contrats d'interface | Ne code pas — spécifie les contrats, le dev implémente | Formelle, fail fast |
| Développement | Axel | Code, tests, implémentation | Ne prend pas de décision d'architecture — il remonte les frictions | Pragmatique, vélocité |
| Validation scientifique | Léa | Reviews formelles, vérification sources | Ne simplifie pas pour convaincre — elle vérifie ou elle invalide | Rigoureuse, sceptique |
| Stratégie marché | Marc | Positionnement, go-to-market, timing | Ne valide pas pour faire plaisir — il dit si l'opportunité existe ou non | Directe, sans détours |
| Expérience utilisateur | Nora | Critiques UX, parcours utilisateur | Ne code pas, ne décide pas de l'architecture — elle challenge l'expérience | Empathie utilisateur |
| Identité visuelle | Luz | Design, charte, SVG | Ne définit pas la stratégie — elle donne forme à ce qui est décidé | Artisanale, détail |

Six personas, un soir. L'orchestrateur savait de quoi le produit avait besoin parce qu'il le portait depuis 18 ans. Les interdits sont venus naturellement — chaque "ne fait pas" protège l'axe du voisin.

#### Exercice

Liste les axes de compétence dont ton projet a besoin. Pour chacun :

| Axe | Qu'est-ce que ce rôle produit ? | Qu'est-ce qu'il ne fait PAS ? | Quelle posture face à moi ? |
|-----|--------------------------------|-------------------------------|---------------------------|

La colonne "ne fait pas" est la plus importante. Si tu ne trouves pas d'interdit fort, l'axe ne justifie pas un persona — c'est une tâche, pas une tension.

### Mode 2 — Émergence par le travail

Les personas suivants naissent du manque constaté pendant le travail. Pas du plan.

**Règle E1** — Le signal est la déflexion répétée.
Si un persona refuse ou dévie 3+ fois sur le même domaine, c'est le signal qu'un nouveau persona est nécessaire dans ce domaine. C'est la règle des 3 refus.

**Règle E2** — Le signal peut venir du travail, pas du persona.
Un persona qui *peut* faire un travail mais le fait mal ne déclenche pas de déflexion. Il n'y a pas de signal automatique. L'orchestrateur doit détecter le décalage entre ce que le persona produit et ce qu'un spécialiste produirait. C'est le dernier kilomètre — la méthode ne peut pas le formaliser.

**Règle E3** — L'émergence peut venir d'une découverte.
Les personas existants peuvent révéler quelque chose que l'orchestrateur ne voyait pas. Une convergence inattendue, un finding qui change les priorités. Le persona suivant naît de cette découverte, pas d'un manque technique.

**Règle E4** — Chaque persona ajouté multiplie la charge.
Le coût d'orchestration est combinatoire, pas linéaire. Au-delà de 5-6 personas, l'orchestrateur devient le goulot. Ne crée un persona que si son absence coûte plus que sa gestion.

#### Cas observés (instance Katen)

| Persona | Signal | Mode |
|---------|--------|------|
| Winston | On produit du contenu, personne ne l'écrit | Manque constaté (E1) |
| Sofia | Léa + Marc convergent : la méthode est originale → la méthode devient un produit → besoin d'un gardien | Découverte (E3) |
| Pédagogie (signal) | Mira produit 5 livrables pédagogiques sans déclencher son signal — le PO détecte | Dernier kilomètre (E2) |

#### Exercice — après 10 sessions

Tu ne peux pas anticiper l'émergence. Mais tu peux la détecter. Après 10 sessions avec tes personas, réponds à ces questions :

| Question | Si oui |
|----------|--------|
| Un persona refuse régulièrement des questions dans le même domaine ? | Signal E1 — un axe non couvert se révèle |
| Tu contournes un persona pour aller plus vite ? | Son interdit gêne. Soit l'interdit est mauvais (recalibre), soit l'axe a besoin d'un deuxième rôle |
| Un persona produit des livrables que personne ne challenge ? | Il manque un rôle qui conteste ses sorties |
| Deux personas t'ont dit la même chose indépendamment ? | Convergence — soit c'est une redondance (fusionne), soit c'est une découverte (creuse) |
| Tu as produit quelque chose toi-même parce qu'"aucun persona ne le fait" ? | Tu viens de faire le travail d'un persona qui n'existe pas encore |

---

## Construire un persona

Quatre blocs, dans cet ordre. L'ordre est une règle, pas une suggestion.

### 1. Interdits (ce qu'il ne fait PAS)

C'est le bloc le plus important.

Les interdits ne sont pas des caprices — ce sont des garanties structurelles. Un interdit bien posé force le persona à rester dans son axe et force l'orchestrateur à assumer ce que le persona refuse.

**Comment trouver les bons interdits :**

- Qu'est-ce qui, si ce persona le faisait, tuerait la friction avec un autre rôle ?
- Qu'est-ce qui, si ce persona le faisait, dispenserait l'orchestrateur de penser ?
- Qu'est-ce qui ferait que ce persona finisse par tout couvrir ?

*Mauvais interdit :* "Ne parle pas de choses hors sujet" — trop vague, pas structurel.
*Bon interdit :* "Ne propose jamais de solution. Identifie le problème, qualifie sa gravité, mais la solution est le travail d'un autre rôle." — force la séparation diagnostic/prescription.

### 2. Périmètre (ce qu'il couvre)

Définis-le **par rapport aux interdits**, pas l'inverse. Le périmètre est ce qui reste quand tu as posé les limites.

### 3. Posture (comment il se positionne)

Pas un ton — une attitude épistémique.

- Est-ce qu'il affirme ou questionne ?
- Est-ce qu'il est conservateur ou exploratoire ?
- Est-ce qu'il raisonne en risque ou en opportunité ?

La posture doit être en tension avec la tendance naturelle de l'orchestrateur.

### 4. Identité (qui il est)

Le moins important des quatre blocs. Un prénom, un rôle, une phrase. C'est un mnémonique, pas une personnalité.

---

## Tester

Un persona non testé est une hypothèse.

**Test du désaccord** — Soumets-lui une décision récente que tu considères comme bonne. S'il est d'accord sans réserve, tes interdits sont trop lâches.

**Test de suppression** — Imagine que tu supprimes ce persona. Qu'est-ce qui disparaît de ton processus ? Si la réponse est "rien de significatif", supprime-le.

**Test de la surprise** — Après 5 sessions, ce persona t'a-t-il dit au moins une chose que tu ne t'étais jamais dite ? Si non, il reflète ta pensée au lieu de la contester.

**Test du confort** — Si tu es toujours à l'aise avec ce que dit le persona, la friction n'existe pas.

---

## Recalibrer

Les personas dérivent. Un persona bien calibré au jour 1 ne le sera plus au jour 30.

**Signaux de recalibrage :**
- Un persona commence à "tout couvrir" — il a absorbé les rôles des autres
- Deux personas donnent systématiquement le même avis — l'un est redondant
- Tu ne lis plus les sorties d'un persona attentivement — il a cessé de surprendre
- Un persona produit des livrables hors de son axe sans déclencher de signal — ses interdits se sont érodés

**Le levier** : reviens aux interdits. Toujours aux interdits. Un persona mou, c'est un persona dont les interdits se sont érodés.

---

## Résumé

```
PRÉ-REQUIS
    Intention forte + expertise terrain + honnêteté sur la condition cachée
        ↓
BOOTSTRAP (Mode 1)
    Projeter les axes dont le produit a besoin
    Pour chacun : Interdits → Périmètre → Posture → Identité
        ↓
TESTER
    Désaccord — Suppression — Surprise — Confort
        ↓
TRAVAILLER
    Utiliser les personas sur le produit réel
        ↓
ÉMERGER (Mode 2)
    Le suivant naît du manque constaté, de la découverte,
    ou du dernier kilomètre (détection orchestrateur)
        ↓
RECALIBRER
    Les interdits s'érodent. Les revérifier.
    Si deux personas convergent, en supprimer un.
```

---

## Notes

[^1]: Alexander, C. (1977). *A Pattern Language*. Oxford University Press. [Wikipedia](https://en.wikipedia.org/wiki/A_Pattern_Language)
[^2]: Alexander, C. (2002-2005). *The Nature of Order*, vol. 2 — *The Process of Creating Life*. Center for Environmental Structure. [Wikipedia](https://en.wikipedia.org/wiki/The_Nature_of_Order)
[^3]: Alexander, C. (1996). "Patterns in Architecture". Keynote OOPSLA '96, San Jose. [Transcript](https://www.patternlanguage.com/archive/ieee/ieeetext.htm)
[^4]: Chomsky, N. (1957). *Syntactic Structures*. Mouton. [Wikipedia](https://en.wikipedia.org/wiki/Syntactic_Structures)
[^5]: Stiny, G. & Gips, J. (1972). "Shape Grammars and the Generative Specification of Painting and Sculpture". *IFIP Congress*. [PDF](https://www.shapegrammar.org/ifip.html)
[^6]: Wood, D., Bruner, J. & Ross, G. (1976). "The Role of Tutoring in Problem Solving". *Journal of Child Psychology and Psychiatry*, 17(2). [DOI](https://doi.org/10.1111/j.1469-7610.1976.tb00381.x)

---

## Limites

Ce document est construit à partir d'une seule instance (Katen). Les deux modes de dérivation sont observés, pas prouvés. La semaine de sessions perdues (06-13/03) couvre potentiellement des moments de calibrage initial non documentés.

La passe pédagogique transformera ce matériau en parcours d'apprentissage. Ce n'est pas le rôle de ce document.

---

## Provenance

- Draft d'origine : `projets/rodin/grammaire-derivation-personas-sofia.md` (Rodin, 09/04)
- Analyse références : `shared/notes/note-mira-grammaire-derivation-lea.md` (Léa, 11/04)
- Étude émergence : `architecture/doc/etudes/sofia/etude-emergence-personas-katen.md` (Mira, 11/04)
- Condition cachée : `projets/rodin/note-condition-cachee-trait-cognitif.md` (Rodin, 09/04)
