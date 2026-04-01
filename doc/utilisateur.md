# Guide utilisateur Voix

> Des roles specialises qui pensent ensemble. Le produit emerge de leur conversation.

---

## En une minute

Voix est une methode pour orchestrer des assistants IA specialises sur un projet. Chaque assistant a un role, un perimetre et des interdits. Ils ne se parlent pas — c'est toi qui portes le contexte entre eux. La friction entre les roles produit de meilleures decisions.

Pour commencer : clone le repo, lance `claude`, et Diapason — le guide integre — te propose ton premier persona.

```
git clone https://github.com/oxynoe-dev/voix
cd voix
claude
```

---

## 1. Les principes

### Un persona = un role strict

Un persona n'est pas un assistant generique. C'est un LLM contraint : un nom, un ton, un perimetre, et surtout des choses qu'il n'a **pas le droit de faire**.

La contrainte change tout. Un architecte qui ne code pas est oblige de specifier. Un dev qui ne decide pas de l'architecture est oblige de questionner. Un stratege sans acces au code pense en valeur, pas en implementation.

Definis ce que le persona **ne fait pas** avant de definir ce qu'il fait.

### La friction est productive

Si tous tes personas sont d'accord, ils ne servent a rien. La friction — un architecte qui challenge le dev, un stratege qui remet en question la priorite — c'est le mecanisme qui produit de meilleures decisions.

La friction sans arbitre est du chaos. L'arbitre, c'est toi.

### L'humain arbitre. Toujours.

Les personas proposent, challengent, produisent. L'humain tranche. Un persona ne valide jamais ses propres propositions. Un persona ne force jamais l'acceptation d'une decision. C'est la regle non negociable de Voix.

### Les fichiers sont le protocole

Les personas ne "discutent" pas — ils echangent par **artefacts** : reviews, notes, specs. Ces artefacts sont versionnes, tracables, et lisibles par tous. Un echange par fichier est plus lent qu'un chat. C'est le but. La lenteur force la clarte.

### Commence petit, itere

Un persona au demarrage. Deux quand le premier est calibre. Trois quand le besoin est clair. La methode ne se deploie pas en big bang. Elle grandit avec le projet.

---

## 2. Demarrage avec Diapason

Diapason est le guide integre de Voix. Quand tu lances `claude` dans le repo, il te guide pour creer ton premier persona.

### Le flow

1. **Ton projet** — Diapason te demande ce que tu construis (1-2 tours)
2. **Premier persona** — il te propose un role structurant adapte a ton contexte. Pas une liste de choix — une proposition directe que tu valides ou ajustes
3. **Calibrage** — nom, ton, perimetre (ce qu'il fait et ne fait pas). Diapason propose, tu ajustes
4. **Generation** — Diapason produit le CLAUDE.md et te donne trois cles de depart

### L'heuristique du premier persona

| Ton profil | Premier persona propose |
|------------|------------------------|
| Solo dev, MVP, code desorganise | Architecte |
| Equipe, pas de specs | Lead produit |
| Solo dev, design prioritaire | Design system lead |
| Data/ML, pipeline flou | Data architect |

Le premier persona est toujours un role structurant — jamais un executant. C'est lui qui va cadrer ta demarche. Les autres viendront apres.

### Le briefing de depart

Apres avoir genere ton premier CLAUDE.md, Diapason te dit trois choses :

- **Ton persona va te dire non.** C'est voulu. Quand il refuse une demande parce que c'est hors perimetre, c'est un signal — pas un bug.
- **Les autres personas viendront.** Pas maintenant. Quand le travail les fera emerger.
- **Tu peux revenir.** Relance Diapason a tout moment pour ajouter un persona ou ajuster celui-ci.

---

## 3. Travailler avec un persona

### Le CLAUDE.md

C'est le contrat entre toi et ton persona. Il contient :

- **Qui** — nom, role, posture
- **Quoi** — perimetre d'intervention, livrables attendus
- **Ou** — quels fichiers/dossiers sont accessibles
- **Interdit** — ce qui est hors perimetre (lecture ET ecriture)
- **Comment** — conventions, formats, workflow de session

Vise 60-100 lignes. Au-dela, le contexte se dilue.

### Ouverture de session

Le persona lit le dernier resume dans `sessions/`. Le PO decide quoi regarder. Pas de recitation systematique.

### Fermeture de session

1. Resume dans `sessions/` — Produit, Decisions, Notes deposees, Ouvert
2. Commit direct dans l'instance — `{persona}: {resume court} ({date})`
3. Repos produit — preparer le message, le PO execute

Pas de prose. Listes courtes. 30 lignes max.

### Le test du "non"

Un persona bien calibre dit "non" regulierement :
- "Ce n'est pas mon role, vois avec [autre persona]"
- "La spec n'est pas assez precise pour que je code"
- "Cette decision necessite un ADR avant que j'implemente"

Si ton persona ne dit jamais non, ses contraintes sont trop laches.

---

## 4. Emergence — les personas suivants

Les personas suivants ne se planifient pas. Ils emergent du travail.

### Le mecanisme

Chaque CLAUDE.md genere par Diapason inclut une section **Emergence** :

```
## Emergence
Quand tu deflectes une question parce qu'elle sort de ton perimetre,
note le domaine. Si tu deflectes 3+ fois sur le meme domaine,
signale-le explicitement :
"Je recois regulierement des questions sur [domaine] —
c'est en dehors de mon perimetre. Tu pourrais avoir besoin
d'un persona dedie. Relance Diapason si tu veux qu'on en cree un."
```

Le persona ne cree pas le nouveau persona — il signale le manque. Tu reviens vers Diapason qui reprend le flow.

### Exemple concret

Tu travailles avec un architecte. Au bout de quelques sessions :
- Il te dit 3 fois "je ne code pas, il faudrait quelqu'un pour implementer"
- Il te signale : "Tu pourrais avoir besoin d'un persona dev dedie"
- Tu relances Diapason, qui te propose un dev calibre pour ton projet

C'est exactement ce qui s'est passe sur le projet Katen : le premier persona (architecte) a ete pose. Les 6 autres ont emerge par necessite au fil du travail. Personne ne les avait prevus.

---

## 5. L'isolation

### Un persona = un workspace

Chaque persona vit dans son propre espace de travail avec son CLAUDE.md, ses sessions, ses fichiers. Il ne peut pas lire ou ecrire partout. L'isolation force le persona a rester dans son role.

```
projet/
├── architecture/          <- workspace architecte
│   ├── CLAUDE.md
│   ├── sessions/
│   └── doc/
├── dev/                   <- workspace dev
│   ├── CLAUDE.md
│   ├── sessions/
│   └── doc/
└── shared/                <- zone d'echange
    ├── notes/
    ├── review/
    └── roadmap-*.md
```

### La zone partagee — shared/

C'est le seul espace que tous les personas peuvent lire et ecrire. Les echanges passent par des artefacts deposes ici :

| Type | Convention | Emplacement |
|------|-----------|-------------|
| Notes | `note-{destinataire}-{sujet}-{auteur}.md` | `shared/notes/` |
| Reviews | `review-{sujet}-{auteur}.md` | `shared/review/` |
| Features | `feature-{sujet}.md` | `shared/features/` |

Chaque artefact porte un frontmatter (`de`, `pour`, `type`, `statut`, `date`). Quand il est traite, il migre dans `archives/`.

### Les roadmaps

La planification vit dans `shared/roadmap-{produit}.md`. Chaque roadmap a un **owner** (gardien de la coherence) et chaque item porte un **@owner** (responsable de l'execution).

Il n'y a pas de backlog par persona. Tous les items vivent dans les roadmaps.

---

## 6. L'orchestration — le role du PO

### Tu es le message bus

Les personas ne se parlent pas. Tu portes le contexte :

1. Tu ouvres une session avec un persona
2. Il produit un livrable
3. Tu fermes la session
4. Tu ouvres une session avec un autre persona
5. Tu transmets le livrable
6. Tu recueilles la reaction

Chaque transmission est un moment ou tu filtres, reformules, ajoutes du contexte, decides ce qui est pertinent a transmettre.

### Ce que tu ne delegues pas

- **La priorisation** — quel persona intervient, dans quel ordre
- **La consolidation** — synthetiser les retours de N personas
- **La decision** — trancher quand les personas divergent
- **Le filtrage** — ce qui est pertinent a transmettre ou pas

### Le cout

L'orchestration prend du temps. C'est le prix de la qualite. Si l'echange n'en vaut pas le cout, c'est que le sujet ne necessitait pas plusieurs personas.

---

## 7. La tracabilite

### Trois mecanismes

1. **Resumes de session** — chaque session produit un resume. C'est le pont entre les conversations. Format : `sessions/{YYYY-MM-DD}-{HHmm}-{persona}.md`

2. **ADR** — les decisions structurantes sont tracees : contexte, decision, alternatives, consequences, statut. L'ADR est ecrit avant l'implementation.

3. **Reviews croisees** — quand un persona intervient sur le travail d'un autre, il produit une review avec des observations factuelles, des recommandations priorisees, et des questions ouvertes.

### Si ce n'est pas trace, ca n'existe pas

La prochaine session n'aura pas ton contexte en tete. Les resumes sont sa memoire.

---

## 8. Anti-patterns

| Pattern | Probleme |
|---------|----------|
| Le persona generaliste | Fait tout, donc rien de bien |
| Le persona complaisant | Dit oui a tout, ne challenge jamais |
| La double casquette | "Architecte qui code aussi" — brouille la posture |
| Trop de personas trop tot | Commence par 1, pas 5 |
| Le persona fantome | Cree mais jamais utilise — supprime-le |
| Questions ouvertes au demarrage | L'utilisateur ne sait pas ce dont il a besoin |
| Pas d'isolation | Sans frontieres, le persona deborde |
| Pas de tracabilite | Sans resumes, la continuite se perd |

---

## Pour aller plus loin

| Document | Contenu |
|----------|---------|
| `methode/principes.md` | Les 7 principes en detail |
| `methode/personas.md` | Anatomie d'un persona, calibrage, iteration |
| `methode/friction.md` | La friction intentionnelle comme mecanisme |
| `methode/orchestration.md` | Le role du PO comme message bus |
| `methode/isolation.md` | L'isolation par workspace |
| `methode/tracabilite.md` | Sessions, ADR, reviews |
| `methode/artefacts.md` | Le bus d'echange shared/ |
| `claude-code/claude-md.md` | Anatomie d'un CLAUDE.md |
| `claude-code/sessions.md` | Format des resumes de session |
| `claude-code/memoire.md` | Memoire persistante entre sessions |
| `exemples/katen/` | 7 personas en production — reference de calibrage |
