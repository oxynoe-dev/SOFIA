# Retour d'expérience — Katen

> 5 personas, 28 sessions fondatrices, un produit en v0.21.

---

## Le projet

[Katen](https://katen.run) est un moteur de composition visuelle basé
sur les réseaux de Petri. Construit en HTML/JS/SVG pur, zéro dépendance.
Open source MIT.

## L'équipe

| Persona | Rôle | Workspace |
|---------|------|-----------|
| **Mira** | Architecte système & solution | `experiments/katen/architecture/` |
| **Axel** | Développeur full stack | `katen/` (repo produit) |
| **Léa** | Chercheuse & validation scientifique | `experiments/katen/recherche/` |
| **Nora** | Product Designer & UX | `experiments/katen/ux/` |
| **Marc** | Conseil stratégique | `experiments/katen/strategie/` |

Un humain (le PO/créateur du projet) arbitre.

## Ce qui a marché

### La friction produit de meilleures décisions

Mira qui challenge une implémentation d'Axel. Léa qui signale
qu'une affirmation ne tient pas à l'examen de la littérature.
Marc qui demande "qui va payer pour ça ?". Ces frictions ont
évité des erreurs réelles.

### L'isolation force la rigueur

Mira ne code pas → elle est obligée de spécifier clairement.
Axel ne décide pas de l'architecture → il remonte les frictions
au lieu de contourner. Le résultat : 52 ADR, 24 principes
d'architecture, des specs exploitables.

### Les sessions structurent la continuité

Le résumé de session est le pont entre les conversations.
Sans lui, chaque session repart de zéro. Avec lui, le persona
reprend exactement où il s'est arrêté.

### Les artefacts comme protocole

Les reviews croisées (Mira review un ADR, Léa review une
affirmation publique) sont plus utiles que n'importe quel chat.
L'écriture force la clarté.

## Ce qui a cassé

### Session perdue

Une semaine de travail (6-7 sessions) a été perdue suite à un
crash de l'app Claude. Le contexte a été reconstitué partiellement
à partir des fichiers produits, mais les décisions intermédiaires
non tracées ont été perdues.

**Leçon** : les résumés de session ne sont pas optionnels. Les
fichiers produits sont la seule source de vérité qui survit.

### Dérive de scope

Certains personas ont parfois débordé de leur périmètre — l'architecte
qui commence à écrire du pseudo-code, le stratège qui donne des avis
techniques. L'isolation dans le CLAUDE.md fonctionne, mais il faut
la maintenir activement.

**Leçon** : la section "Ce qu'il/elle ne fait pas" est la plus
importante de la fiche persona. Revois-la régulièrement.

### Calibrage initial trop large

Les premiers personas étaient trop généralistes. C'est en les
utilisant qu'on les a resserrés — ajout d'interdits, précision
de la posture, réduction du périmètre.

**Leçon** : le premier draft est toujours trop large. Itère.

## Chiffres

- **5** personas actifs
- **52** ADR produits
- **24** principes d'architecture (3 tiers)
- **28** sessions fondatrices (28/02 → 06/03/2026)
- **666** tests
- **v0.21.6** — version courante
