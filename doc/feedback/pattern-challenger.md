# Retour d'expérience — Pattern challenger

> Un producteur, N challengers. Chacun sur son axe. Chacun avec un droit de bloquant.

---

## Le pattern

Un persona produit. D'autres personas interviennent pour vérifier la
qualité sur leur axe d'expertise, sans produire eux-mêmes. Chaque
challenger a un droit de bloquant sur son axe. L'orchestrateur orchestre et tranche.

C'est distinct de la friction entre pairs (deux personas au même niveau
qui contestent). Le challenge est **asymétrique** : un qui produit,
d'autres qui vérifient.

## Instances observées sur Katen

### Chaîne produit (code)

| Rôle | Persona | Axe |
|------|---------|-----|
| Producteur | Axel | Code, implémentation |
| Challenger | Mira | Architecture, cohérence ADR |
| Challenger | Léa | Invariantes formelles, rigueur |
| Challenger | Nora | UX, flux utilisateur |

Un producteur, trois challengers. Intensité maximale — c'est le produit clé.

### Chaîne éditoriale (livre bleu)

| Rôle | Persona | Axe |
|------|---------|-----|
| Producteur | Winston | Rédaction, narration |
| Challenger | Mira | Structure, cohérence argumentaire |
| Challenger | Léa | Références académiques, faits |
| Challenger | Marc | Positionnement, ton |
| Challenger | Nora | UX des livrables publiés |

### Chaîne production multi-support

| Rôle | Persona | Axe |
|------|---------|-----|
| Producteur | Sofia | PDF, PPTX, web, réseaux |
| Challenger | Nora | UX, accessibilité |

## Propriétés

- **Asymétrie** — le producteur avance, les challengers interviennent.
  Pas l'inverse.
- **Axe unique** — chaque challenger vérifie sur son axe d'expertise,
  pas sur tout. L'architecte ne challenge pas l'UX. L'UX ne challenge
  pas l'archi.
- **Droit de bloquant** — un challenger peut bloquer. L'orchestrateur décide si
  le bloquant est levé ou maintenu.
- **Scalable** — on peut ajouter des challengers sans changer le
  producteur. Le coût est linéaire, pas combinatoire.

## Signal académique

Huang et al. (2025) — *Resilience of Multi-Agent Systems to Untrustworthy Agents* (arXiv:2408.00989) — mesurent la résilience de topologies multi-agents face à des agents non fiables. La **topologie hiérarchique** (coordinateur central + agents spécialisés) ne perd que -5.5% de performance avec des agents défaillants, contre -10% à -24% pour les topologies plates (débat, relais).

**Limite** : l'étude porte sur du multi-agent pur (IA↔IA), sans humain au centre. Le pattern challenger dans SOFIA est une orchestration humain↔IA — l'orchestrateur arbitre, pas un agent coordinateur. C'est un **signal convergent** (la topologie hiérarchique est résiliente), pas une **validation** de notre méthode. Personne n'a mesuré ce pattern avec un humain orchestrateur.

## Pour ton projet

Le pattern challenger émerge naturellement quand un persona commence à
produire des livrables qui impactent plusieurs dimensions. Quelques
règles :

- Identifie le producteur et ses challengers pour chaque chaîne
- Donne à chaque challenger un axe explicite — pas "review en général"
  mais "vérifie la rigueur des références" ou "vérifie l'accessibilité"
- Le droit de bloquant est réel — si un challenger bloque, l'orchestrateur tranche,
  mais le producteur ne passe pas en force
- Documente les droits de challenge dans les fiches personas (section
  "Ce qu'il/elle challenge")
