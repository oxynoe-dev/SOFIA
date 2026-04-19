# Changelog

## v0.3.3 — Documentation, dashboard H2A & EN migration (2026-04-17)

### Migration EN (ADR-013)
- Bilingual parser — analysis.py + audit-instance.py accept FR and EN identifiers, documented mapping
- Protocol identifiers EN — markers (sound, contestable, simplification, blind_spot, refuted), resolutions (ratified, contested, revised, rejected), statuses, frontmatter
- Operations EN — openSession, closeSession, depositArtefact, routeArtefact, markRead, markDone, qualifyFriction, qualifyContribution, reportPattern
- Conventions reread rule — closeSession() and depositArtefact() enforce rereading `shared/conventions.md`
- Friction lineage — `antecedent` dimension in protocol/friction.md, `Friction → Friction (amends)` relation in core/model.md, `ref: {source-id}/{index}` in implementation.md
- Instance conventions aligned (methodes, produits, oxynoe) — EN identifiers + naming + operations

### Dashboard — Map / Mirror / Lens / Probe / Legend
- Tabs renamed: Mirror / Lens / Probe (from Analysis / Audit / Pilotage)
- Dashboard translated to EN
- Map tab (home) — instance cards, trajectory challenge %, persona mini cards (frictions + ctx lines), Oxynoe figure style, callout, GitHub footer, right-click context menu overlay
- Mirror tab — trajectory, instance/persona radar (5 axes), KPIs, open frictions, silence map, delta table
- Style overhaul — fixed header/footer scroll container, dark scrollbar, info icons + tooltips on all charts, axis labels, source filter removed, diversity radar fix, coverage fix
- Legend tab — HTML rendering of `sofia/doc/legend.md` (fetch + JS markdown parser), 5 tabs, 5 KPIs, 6 radar axes, trajectory, contribution flow, full glossary

### Solidification friction
- Inline friction template in all 14 contexts — exact format (EN markers, initiative, resolution, lineage)
- Session close validation block installed in 14 contexts — sections, frictions, frontmatter, commit message check before commit
- Context size audit — persona.md + context.md per persona, color thresholds (<150 green, 150-250 yellow, >250 red), visual bar in Audit view

### Documentation
- h2a-proposal closed — protocol/ absorbed all content (and more: PXP resolutions, friction in artifacts, dimensions). Proposal in architecture/doc/ kept as historical study
- Operator guide H2A — 9 operations from orchestrator perspective (when, how, example), synthesis table mode/trigger/producer
- Conceptual model UML — SVG fig-mcd-h2a.svg (7 entities, 3 levels, relations, formalization layers), integrated in arch-sofia.md §3
- Architecture rewrite (arch-sofia.md) — 5 layers + canvas, triangle as motivation §1, H2A MCD 7 entities §3, elementary flow replaces exchange cycle, 3 SVGs remade
- REX split + context transfer — merged into single REX (granularity diagnosis, transfer protocol, Claude memory)
- Canvas: documentation workflow — 5 steps, practitioner/pedagogue loop, SVG
- SVG MCD — Friction→Friction (amends/antecedent) relation added, EN markers
- Structural limitations documented — uninstrumented artifacts, silent lineage, cross-instance (mitigations by discipline + hooks v0.4)

### Tooling
- analysis.py bulk scan — same parser everywhere (sessions + shared/), no distinction by file type. Marker + initiative = friction. Without frontmatter = fallback on filename
- Unified dashboard — Analysis + Audit menu in nav (SOFIA site style), instance sub-menu. Audit tab: checks, orchestrator friction, activity, exchange flows. serve-analysis.py /audit endpoint. Tolerant friction parser + per-persona time series
- analysis.py — map data extraction, context sizes, real personas filter, lineage resolve
- build_legend.py — static HTML generation from legend.md

### Article Bridle Engineering (H2A)
- Epistemic register correction in conclusion — observation/exercised/instrument
- Build pipeline — CSL author-number [Author, N], fix tables, fix refs
- Empirical section reframing — 6-day window, W12-W14 removed, replication invitation

### Decisions
- ADR-013 — EN identifiers migration (markers, resolutions, operations, frontmatter)

## v0.3.2 — H2A Protocol, derivation grammar & operational modes (2026-04-16)

### H2A Protocol
- Formalization of H2A protocol — 5 invariants, 9 operations, protocol/observation distinction
- 5th invariant — Residual opacity (structural limitation of orchestrator arbitration)
- signalerPattern() — mitigation operation, rejection convergence detection, 3 hypotheses, burden-of-proof asymmetry
- PXP resolution tags — ratified/contested/revised/rejected (6th friction dimension, inspired by Mestha et al. 2025)
- Inter-session mutability of resolutions — possible evolution with `ref:` field
- Separation of exchange.md (artifacts, naming conventions, inter-instance flows) and contribution.md
- Extraction of implementation/ — protocol/tools/ to implementation/filesystem/ (prepares future implementations)

### Grammar & target profile
- Derivation grammar v1 — two modes (bootstrap B1-B4, emergence E1-E4), Katen examples, Alexander/Chomsky/Stiny references
- Hidden condition + target profile — three levels (expertise, intention, cognitive trait), self-diagnosis
- Method-inspector archetype (Sofia type) — form vs substance conformity, two passes, cite-or-drop

### Sofia operational modes
- Instance creation mode — 5 phases, minimal scaffolding, conventions from template
- Persona addition mode — 5 phases, generation of 3 files, team announcement
- Recalibration mode — 4 phases, signal table (domestication, overflow, isolation, absent friction)
- Audit mode — 2 passes (conformity script + friction interpretation)
- Removal of onboarding mode (absorbed by instance creation)

### Tooling
- analysis.py + analysis.html — multi-instance analysis + interactive dashboard, 7 charts, 3 tables, 4 filters. Oxynoe palette. **Under calibration**
- audit-instance.py — aligned with H2A (PXP resolutions, `ref:`, signalerPattern, minimal scaffolding). 60 tests
- create-instance.py — rewritten (sofia.md, minimal scaffolding, template conventions). 31 tests
- Tag implementation:filesystem on 10 artifact canvas files

### Documentation
- End-to-end test — Sofia from scratch, 3 CLAUDE.md recalibrations, successful audit
- End-to-end tutorial — "artistic laboratory" instance (shinoe-lab)
- Two-step Sofia boot — onboarding (~80K) vs audit (~200K tokens)
- Blue book in .md format in sofia/doc/
- Principles, duties and core model restructured
- Canvas isolated (inspiration tools, not prescriptions)
- Fix CLAUDE.md paths — relative to workspace

### Decisions
- ADR-010 — Multi-platform via implementation layer, in-repo (supersedes ADR-004 separate repos)
- ADR-011 — Formalized H2A protocol (5 invariants, 9 operations, 2 layers)
- ADR-012 — Implementation layer extraction (semantics vs materialization)
- ADR-001 (semver) and ADR-009 (Instance layer) moved to Accepted

### Fixes
- 11 REX split fixes absorbed by H2A and instance creation mode

## v0.3.1 — Review, instance restructuring & tooling (2026-04-11)

- ADR-009 amended — instance/ layer (archetypes, artifacts, examples/katen), not a scaffolding kit
- Restructuring of sofia/ — instance/archetypes/, instance/artefacts/, instance/examples/katen/ (full snapshot)
- Meta-challenger persona archetype added
- Removal of core/templates/, protocol/templates/, runtime/claude-code/templates/, doc/examples/
- audit-instance.py — SOFIA instance audit script (implementation/filesystem/), 30 structural checks, exchange/friction matrices, session/persona activity, signals, 4 output formats (md/json/csv/sqlite), 29 tests
- CLAUDE.md factored into 3 layers — 2-line boot (persona + context)

## v0.3.0 — Rodin integration & persona topology (2026-04-10)

- Two types of personas: operational (in the flow, long-term memory) and meta (out of flow, no memory)
- Fusion signals and suppression test in core/personas.md
- Anti-pattern "projected org chart" — derive from axes of tension, not job titles
- ADR-009 — Instance layer as 4th conceptual layer (Core / Protocol / Runtime / Instance)
- Sofia positioned outside the instance — exteriority as a condition of objectivity
- Formalized audit instance — 1:1 mirror challengers, no inter-cycle memory, kill after synthesis
- Sofia and Rodin: comparative table of two forms of exteriority
- Meta challenge lock pattern in doc/patterns/verrou-challenge-meta.md
- Two memory patterns in doc/patterns/deux-patterns-memoire.md
- Persona fusion feedback in doc/feedback/fusion-personas.md
- Sofia continuous factual verification rule in core/sofia.md
- arch-sofia.md updated (4 layers, Instance section, figures)

## v0.2.8 — Conventions & formalization (2026-04-10)

- Formal roadmap structure spec in protocol/conventions.md (version headers, item statuses, dependencies)
- Universal frontmatter spec in protocol/conventions.md (notes, reviews, features, studies, personas, sessions)
- Reference deliverables registry pattern in doc/patterns/registre-livrables.md
- Visible version convention on product deliverables (doc, site, blue book)
- Sofia rule — continuous factual verification
- Universal friction markers ✓/~/⚡/◐/✗ in core/friction.md
- 4 new pitfalls in doc/feedback/pieges.md (shared blind spot, signal overproduction, framework ossification, orchestrator bottleneck)
- Multi-support production isolation in doc/feedback/isolation-production.md
- 3 sourcing error classes in doc/feedback/contamination-factuelle.md
- README finalized (orchestrator, 280+ sessions, site link, reformulated origin)

## v0.2.7 — Fixes & renames (2026-04-10)

- Renaming PO/human → **orchestrator** across the entire method (~150 occ. .md, ~60 occ. .svg)
- Fix `voix.md` → `sofia.md` in protocol/conventions.md

## v0.2.6 — Polish + SOFIA rename (2026-04-08)

- Triple rename: Diapason → **Sofia**, Sofia (graphic designer) → **Luz**, Voix → **SOFIA**
- Persona `core/sofia.md` — method guardian, decoupled from runtime
- SVG diagrams remade (elementary flow, instance anatomy, repo structure)
- `arch-voix.md` → `arch-sofia.md`, `fig-triangle-voix.svg` → `fig-triangle-sofia.svg`
- README — SOFIA presented as agnostic, `runtime/` = one implementation among others
- Runtime disclaimer in doc (user-guide.md, orchestration.md)
- OCDS review fixes: "Claude Code conversational behavior" → "runtime behavior"
- Katen example: `sofia.md` → `luz.md`

## v0.2.5 — Publication (2026-04-07)

- CONTRIBUTING.md — contribution guide (branches, commits, PRs, code of conduct)
- GitHub templates — issues (bug, feature), PR template, blank issues disabled
- OCDS textual review fixes: PO → the human, white paper → blue book, Katen descriptions, strategist role
- User guide restructured: §2 "What you just cloned", renumbered 1→9
- "Going further" reformulated with inter-page links
- Manual mode and isolation links made clickable in the guide
- Note: git recommended but not required
- Note "Katen deliverables = examples, adapt to your context"
- Star review SVG remade (personas top, human bottom, increased contrast)
- feedback/pattern-editorial.md renamed to chaine-editoriale.md
- Architecture page removed from site (first release)
- README.md: runtime description + Mistral

## v0.2.4 — Core / Protocol / Runtime restructuring (2026-04-06)

- Isolation of core/ (principles, personas, friction, duties, templates)
- Separation of protocol/ (artifacts, conventions, traceability, isolation, orchestration, instance)
- Separation of runtime/ (claude-code/)
- Split templates (core/, protocol/, runtime/)
- ADR-008 — Core/Protocol/Runtime decision
- conventions.md consolidated in protocol/
- Feedback distillation → doc/patterns/ + doc/feedback/
- Workflows documented (dev, publication, ADR, research, onboarding, product chain)
- Patterns documented (challenger, calibration, escalation, distillery, star review, contamination)
- Manual mode (demarrer-manuel.md)
- Structured documentation (doc/ publishable)
- README.md finalized (alpha disclaimer, manual mode)

## v0.2.3 — Diapason documentation & testing (2026-04-04)

- Guide name: Le Diapason
- devoirs.md — 6 duties of the human orchestrator
- Persona template — "What they challenge" section
- personas.md — 7th persona dimension (challenge right)
- team-orga template — RACI, flows, challenge rights
- 5 field REX reported (calibration, isolation, editorial, challenger, contamination)
- user-guide.md — unified guide
- @owner convention on each roadmap item
- Diapason fixes (hook, dual role, question overload)
- Diapason onboarding design (directive 5-phase flow)
- Emergence feature in CLAUDE.md template

## v0.2.2 — Planning overhaul (2026-04-01)

- Replacement of 7 persona backlogs by 7 product roadmaps with ownership
- New roadmaps: Research, Editorial (Regards + Fragments), Oxynoe Site
- Removal of `roadmap-katen.md` in shared/ (duplicate of `katen/doc/roadmap.md`)
- Minimal boot: read the latest session summary, nothing else
- Minimal closing: summary + commit
- `backlog-archive.md` for completed item history
- Updated conventions.md (roles, ownership, session protocol)
- Updated 7 CLAUDE.md files (simplified boot/closing)
- Updated methode/artefacts.md (roadmaps per product, no more backlog)

## v0.2.1 — Persona archetypes (2026-03-31)

- 7 pre-filled templates by role: architect, dev, ux, strategist, writer, researcher, graphic designer
- Updated persona.md blank template ("Specialized AI assistant")

## v0.2.0 — Enriched Voix product (2026-03-31)

- Templates: backlog.md, roadmap-produit.md, note.md, feature.md, voix-instance.md
- Enriched methode/artefacts.md — archiving, shared/orga/, multi-product features
- Sofia + Winston examples in exemples/katen/
- voix.md marker documented (methode/instance.md)
- "AI Agent" → "Specialized AI assistant" in all examples
- Restructuring templates/ → outillage/templates/
- outillage/onboarding.md, outillage/lexique.md
- methode/isolation.md — multi-instance
- claude-code/sessions.md — archiving at closing

## v0.1.5 — Structure (2026-03-31)

- Archiving notes/archives/ and review/archives/ (convention + rollup of 103 files)
- shared/orga/ (personas, figures, lexicon, team-orga)
- Regards features → shared/features/ with frontmatter
- voix.md instance marker

## v0.1.4 — Backlogs & personas (2026-03-30)

- 7/7 backlogs created, persona files up to date, CLAUDE.md up to date

## v0.1.3 — Data (2026-03-30)

- Frontmatter normalized on 114 shared/ files
- Product roadmaps: katen, voix, si-oxynoe, convergence

## v0.1.2 — Structure migration (2026-03-30)

- Flatten experiments/katen/ → root-level workspaces
- Absorb team/ into experiments/ (shared/, personas/)

## v0.1.1 — Session protocol (2026-03-30)

- Session open/close protocol alignment across 7 CLAUDE.md files
- Creation of conventions.md (frontmatter, statuses, commits)
