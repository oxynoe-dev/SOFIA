---
de: winston
pour: sofia, nora
type: contenu
date: 2026-04-05
objet: Contenu landing voix/ — cadrage Marc 5 sections
source: shared/notes/note-marc-restructuration-landing-voix-sofia-nora.md
---

# Contenu landing — voix/

5 sections + CTA. Pas de cartes personas, pas de principes détaillés, pas de quotes multiples. Tout ça va dans les sous-pages.

---

## 1. Hero

Conservé tel quel — déjà en place sur voix2.html.

```
label:    Methode IA
titre:    SOFIA
sous-titre: Des personas IA contraints qui pensent avec vous.
            Une methode, pas un prompt kit.
mention:  Agnostique par design. La methode tourne sur le LLM de ton choix.
CTA:      GitHub →  |  Livre bleu →
```

---

## 2. Illustration prompt

Position : juste après le hero, visible sans scroll.
Style : bloc terminal/code, palette littoral.

Extrait stylisé d'un CLAUDE.md réel — montre ce qu'est une contrainte de persona en une seconde.

```
# Winston — Ecrivain & distillateur

## Posture
- Voix de l'humain — ecrire dans son style, pas a sa place
- Honnetete radicale — ne pas embellir ce qui ne l'est pas
- Controle humain — rien ne sort sans validation explicite

## Perimetre
Ce workspace est la distillerie editoriale du projet.

## Isolation
- Ne pas intervenir dans les workspaces produit, architecture ou UX
- Les echanges avec les autres personas passent par shared/notes/
```

**Note Luz** : c'est un extrait, pas un screenshot. Le visiteur doit lire les mots "posture", "périmètre", "isolation", "ne pas intervenir" — c'est ça qui ancre "méthode, pas prompt kit". Style terminal sobre, pas de décorations inutiles.

---

## 3. Le problème

```
label:  Le probleme
titre:  Tout le monde multiplie les agents. Personne ne les contraint.

paragraphe 1:
L'IA genere a la demande. Sans friction, elle produit du rien en masse.
Sans perimetre, chaque persona derive vers le meme centre mou.
Sans interdit, la qualite est un accident.

paragraphe 2:
SOFIA part du principe inverse : c'est la contrainte qui cree la valeur.
```

---

## 4. Comment ca marche

3 blocs visuels. Pas de prose — des mots-clés et une phrase.

```
label:  Comment ca marche
titre:  Trois mecanismes. Un produit.

bloc 1 — Contraindre
Chaque voix a son perimetre, ses conventions, ses interdits.
Le developpeur ne touche pas a la strategie. Le stratege ne code pas.
C'est la limitation qui rend utile.

bloc 2 — Eprouver
Les voix ne se parlent pas — elles s'eprouvent par artefacts :
notes, reviews, specs. Les desaccords sont des signaux, pas des bugs.

bloc 3 — Arbitrer
L'humain ecoute, questionne, puis tranche. Toujours.
Ce qui emerge n'est pas un compromis — c'est une decision tracee.
```

---

## 5. Preuve terrain

```
label:  Terrain
titre:  Teste, pas theorise.

paragraphe 1:
210+ sessions. 62 ADR documentées. Des échecs tracés.
Un produit en cours — Katen, construit depuis zéro en 5 semaines,
par un humain et sept voix. Pas livré. En route.

paragraphe 2:
Ce n'est pas un exercice de pensee. C'est un retour d'experience.
```

---

## 6. CTA de sortie

Position : bas de page, avant le footer.

```
label:  Et maintenant
titre:  Lire le livre bleu. Voir le code. Essayer.

CTA 1:  Livre bleu →   (lien PDF)
CTA 2:  GitHub →        (lien repo)
```

---

## Ce qui sort de la landing → sous-pages

| Contenu retiré | Destination |
|---------------|-------------|
| Grille 8 cartes personas | voix/personas.html |
| 7 principes détaillés | voix/principes.html |
| Citations intercalées (x3) | une seule conservée si besoin dans le hero ou supprimées |
| Sections 01/02/03 en extenso | condensées dans "Comment ça marche" (section 4) |

---

## Navigation premier niveau

```
SOFIA    Principes    Personas    Livre bleu    GitHub
```

Présente sur toutes les pages voix/. Page active marquée visuellement.
