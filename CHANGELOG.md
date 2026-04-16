# Changelog

## v0.3.2 — Protocole H2A, grammaire de derivation & modes operationnels (2026-04-16)

### Protocole H2A
- Formalisation protocole H2A — 5 invariants, 9 operations, distinction protocole/observation
- 5e invariant — Opacite residuelle (limitation structurelle de l'arbitrage orchestrateur)
- signalerPattern() — operation de mitigation, detection convergence rejets, 3 hypotheses, asymetrie charge de preuve
- Tags de resolution PXP — ratifie/conteste/revise/rejete (6e dimension friction, inspire Mestha et al. 2025)
- Mutabilite inter-sessions des resolutions — evolution possible avec champ `ref:`
- Separation exchange.md (artefacts, conventions nommage, flux inter-instances) et contribution.md
- Extraction implementation/ — protocol/tools/ vers implementation/filesystem/ (prepare futures implementations)

### Grammaire & profil cible
- Grammaire de derivation v1 — deux modes (bootstrap B1-B4, emergence E1-E4), exemples Katen, references Alexander/Chomsky/Stiny
- Condition cachee + profil cible — trois niveaux (expertise, intention, trait cognitif), auto-diagnostic
- Archetype inspecteur-methode (type Sofia) — conformite forme vs fond, deux passes, cite-or-drop

### Modes operationnels Sofia
- Mode creation d'instance — 5 phases, scaffolding minimal, conventions depuis template
- Mode ajout persona — 5 phases, generation 3 fichiers, annonce equipe
- Mode recalibrage — 4 phases, table de signaux (domestication, debordement, isolation, friction absente)
- Mode audit — 2 passes (script conformite + interpretation frictions)
- Suppression mode onboarding (absorbe par creation d'instance)

### Outillage
- analysis.py + analysis.html — analyse multi-instance + dashboard interactif, 7 graphiques, 3 tables, 4 filtres. Charte Oxynoe. **En calibration**
- audit-instance.py — aligne sur H2A (resolutions PXP, `ref:`, signalerPattern, scaffolding minimal). 60 tests
- create-instance.py — reecrit (sofia.md, scaffolding minimal, conventions template). 31 tests
- Tag implementation:filesystem sur 10 canvas artefacts

### Documentation
- Test e2e — Sofia from scratch, 3 recalibrages CLAUDE.md, audit concluant
- Tutoriel e2e — instance "laboratoire artistique" (shinoe-lab)
- Boot Sofia en deux temps — onboarding (~80K) vs audit (~200K tokens)
- Livre bleu en .md dans sofia/doc/
- Principes, devoirs et modele coeur restructures
- Canvas isoles (outils d'inspiration, pas de prescription)
- Fix chemins CLAUDE.md — relatifs au workspace

### Decisions
- ADR-010 — Multi-plateforme via couche implementation, in-repo (supersede ADR-004 repos separes)
- ADR-011 — Protocole H2A formalise (5 invariants, 9 operations, 2 couches)
- ADR-012 — Extraction couche implementation (semantique vs materialisation)
- ADR-001 (semver) et ADR-009 (couche Instance) passes en Accepted

### Fixes
- 11 fixes REX split absorbes par H2A et mode creation d'instance

## v0.3.1 — Review, restructuration instance & outillage (2026-04-11)

- ADR-009 amende — couche instance/ (archetypes, artefacts, examples/katen), pas un kit de scaffolding
- Restructuration sofia/ — instance/archetypes/, instance/artefacts/, instance/examples/katen/ (snapshot complet)
- Archetype persona meta-challenger ajoute
- Suppression core/templates/, protocol/templates/, runtime/claude-code/templates/, doc/examples/
- audit-instance.py — script d'audit d'instance SOFIA (implementation/filesystem/), 30 checks structurels, matrices echanges/friction, activite sessions/persona, signaux, 4 formats de sortie (md/json/csv/sqlite), 29 tests
- Factorisation CLAUDE.md 3 couches — boot 2 lignes (persona + contexte)

## v0.3.0 — Intégration Rodin & topologie personas (2026-04-10)

- Deux types de personas : opérationnel (dans le flux, mémoire longue) et méta (hors flux, sans mémoire)
- Signaux de fusion et test de suppression dans core/personas.md
- Anti-pattern "organigramme projeté" — dériver des axes de tension, pas des métiers
- ADR-009 — couche Instance comme 4e couche conceptuelle (Core / Protocol / Runtime / Instance)
- Position de Sofia hors instance — extériorité comme condition d'objectivité
- Instance d'audit formalisée — challengers miroir 1:1, sans mémoire inter-cycles, kill après synthèse
- Sofia et Rodin : tableau comparatif des deux formes d'extériorité
- Pattern verrou de challenge méta dans doc/patterns/verrou-challenge-meta.md
- Pattern deux patterns de mémoire dans doc/patterns/deux-patterns-memoire.md
- Feedback fusion personas dans doc/feedback/fusion-personas.md
- Règle Sofia vérification factuelle continue dans core/sofia.md
- arch-sofia.md mis à jour (4 couches, section Instance, chiffres)

## v0.2.8 — Conventions & formalisation (2026-04-10)

- Spec structure formelle des roadmaps dans protocol/conventions.md (en-tetes version, statuts item, dependances)
- Spec frontmatter universel dans protocol/conventions.md (notes, reviews, features, etudes, personas, sessions)
- Pattern registre livrables de reference dans doc/patterns/registre-livrables.md
- Convention version visible sur les rendus produit (doc, site, livre bleu)
- Regle Sofia — verification factuelle continue
- Marqueurs de friction universels ✓/~/⚡/◐/✗ dans core/friction.md
- 4 nouveaux pieges dans doc/feedback/pieges.md (angle mort partage, surproduction signal, ossification cadre, goulot orchestrateur)
- Isolation production multi-support dans doc/feedback/isolation-production.md
- 3 classes d'erreur de sourcing dans doc/feedback/contamination-factuelle.md
- README finalise (orchestrateur, 280+ sessions, lien site, origine reformulee)

## v0.2.7 — Corrections & renommages (2026-04-10)

- Renommage PO/humain → **orchestrateur** dans toute la methode (~150 occ. .md, ~60 occ. .svg)
- Correction `voix.md` → `sofia.md` dans protocol/conventions.md

## v0.2.6 — Polish + renommage SOFIA (2026-04-08)

- Triple renommage : Diapason → **Sofia**, Sofia (graphiste) → **Luz**, Voix → **SOFIA**
- Persona `core/sofia.md` — gardienne de la methode, dissociee du runtime
- Schemas SVG refaits (flux elementaire, anatomie instance, structure repo)
- `arch-voix.md` → `arch-sofia.md`, `fig-triangle-voix.svg` → `fig-triangle-sofia.svg`
- README — SOFIA presente comme agnostique, `runtime/` = une implementation parmi d'autres
- Disclaimer runtime dans doc (utilisateur.md, orchestration.md)
- Corrections review OCDS : "comportement conversationnel de Claude Code" → "du runtime"
- Exemple Katen : `sofia.md` → `luz.md`

## v0.2.5 — Publication (2026-04-07)

- CONTRIBUTING.md — guide de contribution (branches, commits, PR, code de conduite)
- Templates GitHub — issues (bug, feature), PR template, blank issues désactivées
- Corrections textuelles review OCDS : PO → l'humain, livre blanc → livre bleu, descriptions Katen, rôle stratège
- Guide utilisateur restructuré : §2 "Ce que tu viens de cloner", renumérotation 1→9
- "Pour aller plus loin" reformulé avec liens inter-pages
- Lien mode manuel et isolation cliquables dans le guide
- Note git conseillé mais pas obligatoire
- Note "livrables Katen = exemples, adapter à son contexte"
- SVG revue en étoile refait (personas haut, humain bas, contraste augmenté)
- feedback/pattern-editorial.md renommé chaine-editoriale.md
- Page Architecture retirée du site (première release)
- README.md : description runtime + Mistral

## v0.2.4 — Restructuration Core / Protocol / Runtime (2026-04-06)

- Isolation core/ (principes, personas, friction, devoirs, templates)
- Séparation protocol/ (artefacts, conventions, tracabilité, isolation, orchestration, instance)
- Séparation runtime/ (claude-code/)
- Split templates (core/, protocol/, runtime/)
- ADR-008 — décision Core/Protocol/Runtime
- conventions.md consolidé dans protocol/
- Distillation retours → doc/patterns/ + doc/feedback/
- Workflows documentés (dev, publication, ADR, recherche, onboarding, chaîne produit)
- Patterns documentés (challenger, calibrage, escalade, distillerie, revue en étoile, contamination)
- Mode manuel (demarrer-manuel.md)
- Documentation structurée (doc/ publiable)
- README.md finalisé (disclaimer alpha, mode manuel)

## v0.2.3 — Documentation & tests du Diapason (2026-04-04)

- Nom du guide : Le Diapason
- devoirs.md — 6 devoirs de l'humain orchestrateur
- Template persona — section "Ce qu'il/elle challenge"
- personas.md — 7e dimension persona (droit de challenge)
- Template team-orga — RACI, flux, droits de challenge
- 5 REX terrain remontés (calibrage, isolation, éditorial, challenger, contamination)
- utilisateur.md — guide unifié
- Convention @owner sur chaque item de roadmap
- Fix Diapason (accroche, double casquette, surcharge questions)
- Design onboarding Diapason (flow directif 5 phases)
- Feature émergence dans template CLAUDE.md

## v0.2.2 — Refonte planification (2026-04-01)

- Remplacement des 7 backlogs persona par 7 roadmaps produit avec ownership
- Nouvelles roadmaps : Recherche, Editorial (Regards + Fragments), Site Oxynoe
- Suppression de `roadmap-katen.md` dans shared/ (doublon de `katen/doc/roadmap.md`)
- Boot minimal : lire le dernier resume session, rien d'autre
- Fermeture minimale : resume + commit
- `backlog-archive.md` pour l'historique des items termines
- MAJ conventions.md (roles, ownership, protocole session)
- MAJ 7 CLAUDE.md (boot/fermeture simplifies)
- MAJ methode/artefacts.md (roadmaps par produit, plus de backlog)

## v0.2.1 — Archetypes personas (2026-03-31)

- 7 templates pre-remplis par role : architecte, dev, ux, stratege, redacteur, chercheur, graphiste
- MAJ persona.md template vierge ("Assistant IA specialise")

## v0.2.0 — Produit Voix enrichi (2026-03-31)

- Templates : backlog.md, roadmap-produit.md, note.md, feature.md, voix-instance.md
- Enrichissement methode/artefacts.md — archivage, shared/orga/, features multi-produits
- Exemples Sofia + Winston dans exemples/katen/
- Marqueur voix.md documente (methode/instance.md)
- "Agent IA" → "Assistant IA specialise" dans tous les exemples
- Restructuration templates/ → outillage/templates/
- outillage/onboarding.md, outillage/lexique.md
- methode/isolation.md — multi-instance
- claude-code/sessions.md — archivage en fermeture

## v0.1.5 — Structure (2026-03-31)

- Archivage notes/archives/ et review/archives/ (convention + rollup 103 fichiers)
- shared/orga/ (personas, figures, lexique, team-orga)
- Regards features → shared/features/ avec frontmatter
- voix.md marqueur d'instance

## v0.1.4 — Backlogs & personas (2026-03-30)

- 7/7 backlogs crees, fiches personas a jour, CLAUDE.md a jour

## v0.1.3 — Donnees (2026-03-30)

- Frontmatter normalise sur 114 fichiers shared/
- Roadmaps produit : katen, voix, si-oxynoe, convergence

## v0.1.2 — Migration structure (2026-03-30)

- Aplatir experiments/katen/ → workspaces a la racine
- Absorber team/ dans experiments/ (shared/, personas/)

## v0.1.1 — Protocole de session (2026-03-30)

- Alignement protocole ouverture/fermeture session dans 7 CLAUDE.md
- Creation conventions.md (frontmatter, statuts, commits)
