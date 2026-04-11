# Anatomie d'un CLAUDE.md

> Le CLAUDE.md est un aiguillage runtime, pas un document de contenu.

---

## Ce que c'est

Le fichier `CLAUDE.md` à la racine d'un workspace contient les
instructions que Claude Code lit à chaque conversation. Depuis la
factorisation en trois couches, il ne porte plus le contenu — il pointe
vers les fichiers qui le portent.

## Structure

```markdown
Quel que soit le premier message de l'utilisateur, à l'ouverture de session, avant toute réponse, lis ces deux fichiers :
- `{chemin-relatif}/shared/orga/personas/persona-{nom}.md`
- `{chemin-relatif}/shared/orga/contextes/contexte-{nom}-{produit}.md`
```

C'est tout. Deux lignes. Le reste vit dans le persona et le contexte.

**Le chemin est relatif au workspace**, pas a la racine du repo :
- Workspace dans l'instance (`instance/archi/`) → `../shared/orga/...`
- Workspace hors de l'instance (`katen/`) → `../instance/shared/orga/...`

Pour un persona qui n'a qu'un seul contexte (ex: un persona-guide comme Sofia), une seule ligne suffit :

```markdown
Quel que soit le premier message de l'utilisateur, à l'ouverture de session, avant toute réponse, lis ce fichier :
- `{chemin-relatif}/shared/orga/personas/persona-{nom}.md`
```

## Trois couches

| Fichier | Couche | Contenu | Emplacement |
|---------|--------|---------|-------------|
| `CLAUDE.md` | Runtime | Aiguillage — 2 lignes | Racine du workspace ou du repo produit |
| `persona-{nom}.md` | Core | Rôle, posture, contraintes, friction, protocole de session | `shared/orga/personas/` |
| `contexte-{persona}-{produit}.md` | Instance | Documents clés, périmètre, isolation, conventions, workflow | `shared/orga/contextes/` |

### Pourquoi cette séparation

- **Le persona est agnostique du produit.** Mira est architecte qu'elle travaille
  sur Katen, SOFIA ou un autre projet. Son rôle, sa posture, ses contraintes
  ne changent pas.
- **Le contexte est spécifique.** Mira dans katen/ lit les ADR et les principes.
  Axel dans katen/ lit le code et les tests. Le même produit, deux vues.
- **Le CLAUDE.md est un détail runtime.** C'est le format Claude Code. Un autre
  provider aura un autre mécanisme d'injection. Le contenu (persona + contexte)
  reste le même.

### Conséquence

Plus de duplication entre le CLAUDE.md du workspace instance et le CLAUDE.md
du repo produit. Un seul persona.md, un contexte par couple persona×produit,
des CLAUDE.md de 2 lignes partout.

## Ce que porte le persona (persona-{nom}.md)

Le fichier persona est **agnostique du produit**. Il définit :

- Profil — qui est ce persona
- Posture — comment il se comporte (3-4 bullets)
- Domaines d'intervention — sur quoi il intervient
- Ce qu'il produit — types de livrables
- Ce qu'il challenge — droit de regard, friction intentionnelle
- Ce qu'il ne fait pas — **la section la plus importante**, les interdits
- Collaboration — avec qui et comment

Template : `instance/artefacts/persona.md`

## Ce que porte le contexte (contexte-{persona}-{produit}.md)

Le fichier contexte est **spécifique au couple persona×produit**. Il définit :

- Périmètre — ce que le workspace contient
- Documents clés — les fichiers à connaître en priorité
- Repos liés — les dépôts connectés
- Isolation — **les frontières**, ce que le persona ne peut pas toucher
- Conventions — langue, formats, nommage
- Workflow — ouverture/fermeture de session, étapes spécifiques
- Émergence — protocole de détection des rôles manquants
- Protocole de session — format du résumé, commit

Template : `instance/artefacts/contexte-persona-produit.md`

## Erreurs courantes

- **CLAUDE.md de 60+ lignes** — si le CLAUDE.md fait plus de 3 lignes, le contenu devrait être dans le persona ou le contexte
- **Chemin absolu ou relatif a la racine** — le chemin doit etre relatif au workspace (working directory de Claude Code), pas a la racine du repo. Sinon le persona ne trouve pas ses fichiers au boot
- **Duplication** — ne copie pas la fiche persona dans le contexte, ni le contexte dans le persona
- **Pas d'isolation dans le contexte** — sans frontières explicites, le persona ira partout
- **Pas de workflow dans le contexte** — sans ouverture/fermeture de session, la continuité se perd

## Référence

Voir `protocol/conventions.md` § "CLAUDE.md — anatomie" pour la spec normative.
