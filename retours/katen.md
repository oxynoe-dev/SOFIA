# Retour d'expérience — Katen

> 7 personas, 210+ sessions, un projet réel.

---

## Le projet

[Katen](https://katen.run) est un moteur de composition visuelle basé
sur les réseaux de Petri. Construit en HTML/JS/SVG pur, zéro dépendance.
Open source MIT. 18 ans de réflexion (2008-2026) — de la v1 C++/Qt
à la v2 pur web.

## L'équipe

| Persona | Rôle | Workspace |
|---------|------|-----------|
| **Mira** | Architecte système & solution | `experiments/architecture/` |
| **Axel** | Développeur full stack | `katen/` (repo produit) |
| **Léa** | Chercheuse & validation scientifique | `experiments/recherche/` |
| **Nora** | Product Design & UX | `experiments/ux/` |
| **Marc** | Conseil stratégique | `experiments/strategie/` |
| **Sofia** | Identité visuelle & Production multi-support | `experiments/graphisme/` |
| **Winston** | Écrivain & distillateur éditorial | `experiments/maturation/` |

Un humain (le PO/créateur du projet) arbitre.

## Ce qui a marché

### La friction produit de meilleures décisions

Mira qui challenge une implémentation d'Axel. Léa qui signale
qu'une affirmation ne tient pas à l'examen de la littérature.
Marc qui demande "qui va payer pour ça ?". Sofia qui refuse un
thème visuel qui plaît mais qui ne porte pas l'identité du projet.
Ces frictions ont évité des erreurs réelles.

### L'isolation force la rigueur

Mira ne code pas → elle est obligée de spécifier clairement.
Axel ne décide pas de l'architecture → il remonte les frictions
au lieu de contourner. Sofia produit, Nora challenge — celle qui
décide de la forme est celle qui la livre, celle qui challenge ne
produit pas. Le résultat : 62 ADR, 24 principes d'architecture,
des specs exploitables.

### Les sessions structurent la continuité

Le résumé de session est le pont entre les conversations.
Sans lui, chaque session repart de zéro. Avec lui, le persona
reprend exactement où il s'est arrêté.

### Les artefacts comme protocole

Les reviews croisées (Mira review un ADR, Léa review une
affirmation publique, Nora challenge un livrable de Sofia) sont
plus utiles que n'importe quel chat. L'écriture force la clarté.

### Le pattern challenger

Un producteur, N challengers avec droit de bloquant sur leur axe.
Axel code → Mira challenge l'archi, Léa les invariantes, Nora l'UX.
Winston rédige → Mira challenge la structure, Léa les refs, Marc
le positionnement. Le PO tranche quand un challenger bloque.

### La chaîne éditoriale

Winston rédige, les experts valident le fond, Sofia produit la forme,
Nora challenge avant publication, le PO valide en dernier. Le livre
blanc Voix est le premier produit complet de cette chaîne.

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
importante de la fiche persona. Revois-la régulièrement. La section
"Ce qu'il/elle challenge" rend la friction structurelle.

### Calibrage initial trop large

Les premiers personas étaient trop généralistes. C'est en les
utilisant qu'on les a resserrés — ajout d'interdits, précision
de la posture, réduction du périmètre. Définir par le média
(spec, code, review, PDF) est plus fiable que par la compétence.

**Leçon** : le premier draft est toujours trop large. Itère.

### Contamination factuelle

~30 documents contenaient "15 ans" au lieu de "18 ans" pour la
durée de réflexion du PO. L'erreur venait du PO lui-même, propagée
et stabilisée par l'IA. Détectée par Léa lors d'un audit ciblé.

**Leçon** : le repo n'est pas une source de vérité pour les faits.
Vérification humaine en continu — pas en fin de projet.

### Frontières de production floues

Quand les personas ont commencé à produire (pas juste spécifier),
les frontières de périmètre sont devenues floues. Qui publie quoi
sur quel canal ? Résolu en séparant producteur et challenger, et
en centralisant les scripts dans `shared/tools/`.

**Leçon** : l'isolation de la réflexion est dans les fiches personas.
L'isolation de la production est dans les conventions de publication.
Les deux sont nécessaires.
