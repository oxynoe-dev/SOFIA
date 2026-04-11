## Onboarding Persona

![Workflow — Onboarding persona](../figures/fig-workflow-onboarding.svg)

Workflow d'intégration d'un nouveau persona : du manque constaté à la première session productive.

---

### Quand l'utiliser

Quand un domaine n'est pas couvert par les personas existants et que ce manque génère des problèmes récurrents. Ce workflow est la version processus — pour la checklist technique, voir `doc/onboarding.md`.

### Étapes

1. **Manque constaté** — un domaine émerge que personne ne couvre, ou deux personas sont en tension récurrente sur un sujet. Le manque est documenté, pas supposé
2. **Définition fiche persona** — `shared/orga/personas/persona-{nom}.md` : rôle, posture, périmètre, interdits, média préférés. Les interdits sont plus importants que les responsabilités : ce que le persona ne fait pas le définit autant que ce qu'il fait (cf. `core/principes.md`, principe d'isolation). Template : `instance/artefacts/persona.md`
3. **Définition fichier contexte** — `shared/orga/contextes/contexte-{nom}-{produit}.md` : documents clés, périmètre workspace, isolation, conventions, workflow. Un fichier par couple persona×produit (un même persona peut avoir plusieurs contextes). Template : `instance/artefacts/contexte-persona-produit.md`
4. **Création workspace** — `{workspace}/sessions/` + CLAUDE.md de 2 lignes pointant vers persona + contexte. Le workspace suit les conventions de l'instance (cf. `protocol/conventions.md` § "CLAUDE.md — anatomie")
5. **Calibrage** — premiers échanges avec l'orchestrateur et les personas adjacents. Ajustement de la posture, du vocabulaire, du niveau de détail. Le calibrage prend 2-3 sessions
6. **Première session productive** — le persona produit un artefact réel (review, note, spec) qui est utilisé par un autre persona. C'est le critère de validation

### Rôles impliqués

| Persona | Rôle |
|---------|------|
| Orchestrateur | Valide la nécessité, arbitre le périmètre |
| Persona adjacent | Briefing du domaine, premiers échanges |
| Nouveau persona | Produit son premier artefact réel |

### Artefacts produits

- Fiche persona — `shared/orga/personas/persona-{nom}.md` (s'inspirer des archétypes dans `instance/archetypes/` et du format dans `instance/artefacts/persona.md`)
- Fichier contexte — `shared/orga/contextes/contexte-{nom}-{produit}.md` (template : `instance/artefacts/contexte-persona-produit.md`)
- CLAUDE.md — 2 lignes d'aiguillage vers persona + contexte
- Workspace complet (`{workspace}/sessions/`)
- Note d'annonce dans `shared/notes/` pour informer les autres personas
- Premier artefact productif (review, note, spec)

### Pièges

- **Créer par symétrie** — "il nous manque un persona X pour compléter l'équipe". Un persona doit prouver sa nécessité par un manque réel, pas par une symétrie théorique
- **Le persona fourre-tout** — si on ne peut pas dire ce qu'il ne fait pas, il n'est pas calibré. Les interdits sont le premier test de qualité d'une fiche persona
- **Skipper le calibrage** — un persona non calibré produit des artefacts inutilisables. Les 2-3 premières sessions sont un investissement, pas une perte de temps
- **Oublier le fichier contexte** — sans contexte, le persona ne connaît pas son workspace. Le persona sait qui il est, le contexte lui dit où il est
