---
de: winston
pour: sofia, nora
type: contenu
date: 2026-04-05
objet: Contenu landing voix/ — cadrage Marc 5 sections
source: shared/notes/note-marc-restructuration-landing-voix-sofia-nora.md
---

# Contenu landing — voix/

5 sections + CTA. Pas de cartes personas, pas de principes detailles, pas de quotes multiples. Tout ca va dans les sous-pages.

---

## 1. Hero

Conserve tel quel — deja en place sur voix2.html.

```
label:    Methode IA
titre:    Voix
sous-titre: Des personas IA contraints qui pensent ensemble.
            Une methode, pas un prompt kit.
mention:  Agnostique par design. La methode tourne sur le LLM de ton choix.
CTA:      GitHub →  |  Livre bleu →
```

---

## 2. Illustration prompt

Position : juste apres le hero, visible sans scroll.
Style : bloc terminal/code, palette littoral.

Extrait stylise d'un CLAUDE.md reel — montre ce qu'est une contrainte de persona en une seconde.

```
# Winston — Ecrivain & distillateur

## Posture
- Voix du PO — ecrire dans son style, pas a sa place
- Honnetete radicale — ne pas embellir ce qui ne l'est pas
- Controle humain — rien ne sort sans validation explicite du PO

## Perimetre
Ce workspace est la distillerie editoriale du projet.

## Isolation
- Ne pas intervenir dans les workspaces produit, architecture ou UX
- Les echanges avec les autres personas passent par shared/notes/
```

**Note Sofia** : c'est un extrait, pas un screenshot. Le visiteur doit lire les mots "posture", "perimetre", "isolation", "ne pas intervenir" — c'est ca qui ancre "methode, pas prompt kit". Style terminal sobre, pas de decorations inutiles.

---

## 3. Le probleme

```
label:  Le probleme
titre:  Tout le monde multiplie les agents. Personne ne les contraint.

paragraphe 1:
L'IA genere a la demande. Sans friction, elle produit du rien en masse.
Sans perimetre, chaque persona derive vers le meme centre mou.
Sans interdit, la qualite est un accident.

paragraphe 2:
Voix part du principe inverse : c'est la contrainte qui cree la valeur.
```

---

## 4. Comment ca marche

3 blocs visuels. Pas de prose — des mots-cles et une phrase.

```
label:  Comment ca marche
titre:  Trois mecanismes. Un produit.

bloc 1 — Isoler
Chaque voix a son perimetre, ses conventions, ses interdits.
Le developpeur ne touche pas a la strategie. Le stratege ne code pas.

bloc 2 — Contraindre
Les voix ne se parlent pas directement. Elles echangent par artefacts :
notes, reviews, specs. Le signal circule sans bruit.

bloc 3 — Converger
L'humain pose la vision. Les voix challengent depuis leur angle.
Ce qui emerge n'est pas un compromis — c'est une pensee distribuee.
```

---

## 5. Preuve terrain

```
label:  Terrain
titre:  Teste, pas theorise.

paragraphe 1:
210+ sessions. 62 ADR documentees. Des echecs traces.
Un produit livre — Katen, de zero a la production en 18 mois,
par un humain et sept voix.

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

| Contenu retire | Destination |
|---------------|-------------|
| Grille 8 cartes personas | voix/personas.html |
| 7 principes detailles | voix/principes.html |
| Citations intercalees (x3) | une seule conservee si besoin dans le hero ou supprimees |
| Sections 01/02/03 en extenso | condensees dans "Comment ca marche" (section 4) |

---

## Navigation premier niveau

```
Voix    Principes    Personas    Livre bleu    GitHub
```

Presente sur toutes les pages voix/. Page active marquee visuellement.
