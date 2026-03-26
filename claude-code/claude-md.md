# Anatomie d'un CLAUDE.md

> Le CLAUDE.md est le contrat entre toi et ton persona.

---

## Ce que c'est

Le fichier `CLAUDE.md` à la racine d'un workspace contient les
instructions que Claude Code lit à chaque conversation. C'est le
seul mécanisme fiable pour donner un rôle, une posture et des
limites à l'agent.

## Structure recommandée

```markdown
# {Projet} — Instructions Claude Code

## Persona
Claude incarne **{Nom}** — {rôle}.
Voir `{chemin}/persona-{nom}.md` pour la fiche complète.

## Posture
- {comportement 1}
- {comportement 2}
- {comportement 3}

## Périmètre
Ce workspace contient : {description}
- {type de contenu 1}
- {type de contenu 2}

## Documents clés
| Fichier | Rôle |
|---------|------|
| `{chemin}` | {description} |

## Isolation
- Ne jamais lire/écrire en dehors de `{périmètre autorisé}`
- {autres interdits}

## Conventions
- **Langue** : {français / anglais / les deux}
- **{Type d'artefact}** : {format attendu}
- **Reviews** : format `review-<sujet>-{nom}.md`, déposer dans `shared/review/`

## Workflow
1. **Ouverture de session** — lire le dernier résumé dans `sessions/`
2. **Lire** les documents existants avant toute intervention
3. **Produire** des {types de livrables}
4. **{Interdit}** — {ce que le persona ne fait pas}

## Résumé de session — obligatoire
À chaque fin de session, produire un résumé dans `sessions/` :
- **Nom** : `{YYYY-MM-DD}-{HHmm}-{nom}.md`
- **Contenu** : Produit, Décisions, Notes déposées, Ouvert
- **Pas de prose** — listes courtes, 30 lignes max
```

## Sections clé par clé

### Persona

Une ligne. Qui est l'agent dans cette conversation.
Référence la fiche persona complète plutôt que de tout dupliquer.

### Posture

3-4 bullets qui définissent le **comportement**, pas les compétences.
C'est ce qui donne le ton à chaque réponse.

### Périmètre

Ce que le workspace contient. Pas une liste de fichiers — une
description du territoire. Le persona sait ainsi ce qui est "chez lui".

### Documents clés

Les fichiers importants avec leur rôle. Le persona les consulte
en priorité. Inclure les documents hors workspace si nécessaire
(en chemin absolu).

### Isolation

**La section la plus importante.** Les frontières. Ce que le persona
ne peut pas toucher. Sans cette section, le persona va déborder.

### Workflow

Comment une session se déroule. Toujours commencer par lire le
dernier résumé. Toujours finir par en produire un.

### Résumé de session

Format imposé. Le persona ne peut pas "oublier" — c'est dans
ses instructions.

## Erreurs courantes

- **Trop long** — un CLAUDE.md de 200 lignes n'est pas lu entièrement. Vise 60-100 lignes.
- **Pas d'isolation** — sans frontières explicites, le persona ira partout
- **Pas de workflow** — sans ouverture/fermeture de session, la continuité se perd
- **Duplication** — ne copie pas la fiche persona dans le CLAUDE.md, référence-la
- **Trop de détails techniques** — le CLAUDE.md dit quoi faire, pas comment le faire
