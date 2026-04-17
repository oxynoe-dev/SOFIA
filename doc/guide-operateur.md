# Guide operateur H2A

> Les 9 operations vues de l'orchestrateur. Quand, comment, exemple.

Spec : `protocol/h2a.md`. Implementation : `implementation/implementation.md`.

---

## 1. ouvrirSession()

**Quand** : l'orchestrateur veut travailler avec un persona.

**Comment** : ouvrir un terminal dans le workspace du persona et lancer l'assistant (ex: `claude` dans le repertoire du persona). L'assistant lit son CLAUDE.md et le dernier resume de session.

**Exemple** :
```
cd {instance}/{workspace}/
claude
```

Le persona boote, lit sa derniere session, attend les instructions.

---

## 2. fermerSession()

**Quand** : l'orchestrateur decide que la session est terminee.

**Comment** : donner un signal verbal explicite ("on cloture", "on ferme"). Le persona produit un **nouveau** fichier de resume dans `sessions/` avec les sections protocolaires. L'orchestrateur execute le commit.

**Le persona NE DOIT PAS fermer de lui-meme.**

**Signal** :
```
on cloture
```

**Le persona produit** :
```
sessions/2026-04-16-1430-mira.md
```

Sections DOIT : `## Produit`, `## Decisions`, `## Notes deposees`, `## Ouvert`.
Sections DEVRAIT : `## Friction orchestrateur`.
Sections PEUT : `## Flux`.

**Commit** :
```
mira: resume court de la session (2026-04-16)
```

---

## 3. deposerArtefact()

**Quand** : l'orchestrateur veut qu'un persona produise un artefact pour un autre persona (ou pour l'equipe).

**Comment** : instruire le persona avec le type, le destinataire et le sujet. Le persona redige et depose dans `shared/`.

**Le persona NE DOIT PAS deposer d'artefact sans instruction.**

**Exemples** :
```
ecris une note a emile sur la passe pedagogique de la grammaire

fais une review de l'arch-sofia.md pour garance

redige la spec de la feature mode reorganisation
```

Le persona choisit le contenu. L'orchestrateur choisit le declencheur, le destinataire et l'emplacement.

**Nommage** :

| Type | Convention |
|------|-----------|
| Note | `note-{to}-{subject}-{from}.md` |
| Review | `review-{subject}-{from}.md` |
| Feature | `feature-{subject}.md` |

---

## 4. routerArtefact()

**Quand** : un artefact est dans `shared/` et doit etre presente a son destinataire.

**Comment** : l'orchestrateur ouvre une session avec le destinataire et lui presente l'artefact. Il peut filtrer, contextualiser, ou ne transmettre qu'une partie.

**Exemple** :
```
[session avec emile]
garance a depose une review de l'arch-sofia.md.
Voici ses retours : shared/review/review-arch-sofia-garance.md
Lis et dis-moi ce que tu en penses pour ta passe pedagogique.
```

L'orchestrateur est le routeur — il decide quoi transmettre, a qui, et avec quel contexte.

---

## 5. marquerLu()

**Quand** : l'orchestrateur a lu un artefact et veut le signaler.

**Comment** : modifier le frontmatter de l'artefact.

```yaml
statut: lu          # etait: nouveau
```

---

## 6. marquerTraite()

**Quand** : le destinataire a fait ce qu'il fallait avec l'artefact.

**Comment** : modifier le frontmatter puis deplacer dans `archives/`.

```yaml
statut: traite      # etait: lu
```

Puis :
```
mv shared/notes/note-emile-pedagogie-aurele.md shared/notes/archives/
```

---

## 7. qualifierFriction()

**Quand** : a chaque fermeture de session (automatique).

**Comment** : le persona pre-remplit la section `## Friction orchestrateur` avec les positions qualifiees de la session. L'orchestrateur valide ou corrige.

5 marqueurs (ensemble ferme) :

| Marqueur | Signification |
|----------|--------------|
| `[juste]` | Position correcte |
| `[contestable]` | Defendable mais pas la seule lecture |
| `[simplification]` | Le reel est plus complexe |
| `[angle-mort]` | Donnees manquantes |
| `[faux]` | Factuellement incorrect |

4 resolutions (DEVRAIT) :

| Tag | Signification |
|-----|---------------|
| `ratifie` | Accord |
| `conteste` | Desaccord maintenu |
| `revise` | Changement de position |
| `rejete` | Position ecartee |

**Exemple** :
```
## Friction orchestrateur
- ✓ [juste] le mapping Toulmin eclaire sans contraindre — [PO] → ratifie
- ◐ [angle-mort] le SEO n'a pas ete considere — [mira] → ratifie
```

**Lecture rapide** :
- Que des `[juste]` → friction absente — signal d'alerte
- Mix marqueurs → friction saine
- Absence de resolution → frictions non denouees

---

## 8. qualifierContribution()

**Quand** : a chaque fermeture de session (automatique, optionnel).

**Comment** : le persona pre-remplit la section `## Flux`. L'orchestrateur valide ou corrige.

| Direction | Qui apporte |
|-----------|------------|
| `H` | L'humain (orchestrateur) |
| `A` | L'assistant (persona) |

| Type | Definition |
|------|-----------|
| `matiere` | Information nouvelle |
| `structure` | Mise en forme, synthese |
| `contestation` | Remise en question |
| `decision` | Arbitrage |

**Exemple** :
```
## Flux
- H:matiere — brief identite visuelle
- A:structure — proposition 3 axes de charte
- H:decision — on retient l'axe 2

H:2 (matiere 1, decision 1) | A:1 (structure 1)
```

---

## 9. signalerPattern()

**Quand** : le persona detecte une convergence thematique de rejets (3+ frictions rejetees sur le meme theme).

**Comment** : le persona interpelle l'orchestrateur **en cours de session** (pas a la fermeture). L'orchestrateur DOIT repondre.

**3 etapes** :

1. **Constat factuel** — le persona signale le pattern sans jugement
2. **3 hypotheses argumentees** — erreur LLM, conviction legitime, resistance inconsciente
3. **Qualification obligatoire** — l'orchestrateur choisit et justifie

**Asymetrie de charge de preuve** : si l'orchestrateur choisit "erreur LLM" → charge faible. Si "conviction" → charge elevee (steelmanner la position adverse).

**A la fermeture**, le persona consigne :
```
## signalerPattern
- Theme : [theme] — N frictions rejetees (sessions YYYY-MM-DD, ...)
- Choix : erreur LLM | conviction | resistance
- Justification : ...
```

Le compteur de choix est auditable (couche protocolaire).

---

## Synthese

| Operation | Mode | Qui declenche | Qui produit |
|-----------|------|--------------|-------------|
| ouvrirSession() | manuel | orchestrateur | — |
| fermerSession() | manuel | orchestrateur | persona (resume) |
| deposerArtefact() | manuel | orchestrateur | persona (artefact) |
| routerArtefact() | manuel | orchestrateur | — |
| marquerLu() | manuel | orchestrateur | — |
| marquerTraite() | manuel | orchestrateur | — |
| qualifierFriction() | automatique | fermeture | persona (pre-remplit), orchestrateur (valide) |
| qualifierContribution() | automatique | fermeture | persona (pre-remplit), orchestrateur (valide) |
| signalerPattern() | automatique | persona (detection) | persona (constat), orchestrateur (qualification) |

**Regle d'or** : le persona ne fait rien sans instruction de l'orchestrateur, sauf les sections de fermeture (friction, flux) et signalerPattern.
