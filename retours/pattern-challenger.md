# Retour d'experience — Pattern challenger

> Un producteur, N challengers. Chacun sur son axe. Chacun avec un droit de bloquant.

---

## Le pattern

Un persona produit. D'autres personas interviennent pour verifier la
qualite sur leur axe d'expertise, sans produire eux-memes. Chaque
challenger a un droit de bloquant sur son axe. Le PO orchestre et tranche.

C'est distinct de la friction entre pairs (deux personas au meme niveau
qui contestent). Le challenge est **asymetrique** : un qui produit,
d'autres qui verifient.

## Instances observees sur Katen

### Chaine produit (code)

| Role | Persona | Axe |
|------|---------|-----|
| Producteur | Axel | Code, implementation |
| Challenger | Mira | Architecture, coherence ADR |
| Challenger | Lea | Invariantes formelles, rigueur |
| Challenger | Nora | UX, flux utilisateur |

Un producteur, trois challengers. Intensite maximale — c'est le produit cle.

### Chaine editoriale (livre blanc)

| Role | Persona | Axe |
|------|---------|-----|
| Producteur | Winston | Redaction, narration |
| Challenger | Mira | Structure, coherence argumentaire |
| Challenger | Lea | References academiques, faits |
| Challenger | Marc | Positionnement, ton |
| Challenger | Nora | UX des livrables publies |

### Chaine production multi-support

| Role | Persona | Axe |
|------|---------|-----|
| Producteur | Sofia | PDF, PPTX, web, reseaux |
| Challenger | Nora | UX, accessibilite |

## Proprietes

- **Asymetrie** — le producteur avance, les challengers interviennent.
  Pas l'inverse.
- **Axe unique** — chaque challenger verifie sur son axe d'expertise,
  pas sur tout. L'architecte ne challenge pas l'UX. L'UX ne challenge
  pas l'archi.
- **Droit de bloquant** — un challenger peut bloquer. Le PO decide si
  le bloquant est leve ou maintenu.
- **Scalable** — on peut ajouter des challengers sans changer le
  producteur. Le cout est lineaire, pas combinatoire.

## Pour ton projet

Le pattern challenger emerge naturellement quand un persona commence a
produire des livrables qui impactent plusieurs dimensions. Quelques
regles :

- Identifie le producteur et ses challengers pour chaque chaine
- Donne a chaque challenger un axe explicite — pas "review en general"
  mais "verifie la rigueur des references" ou "verifie l'accessibilite"
- Le droit de bloquant est reel — si un challenger bloque, le PO tranche,
  mais le producteur ne passe pas en force
- Documente les droits de challenge dans les fiches personas (section
  "Ce qu'il/elle challenge")
