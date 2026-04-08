# Changelog

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
