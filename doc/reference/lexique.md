# Glossary

> Shared vocabulary of the SOFIA method. When a term has a specific meaning in SOFIA, it is defined here.

---

## Reading path

New to SOFIA? Read these 10 entries first, in this order:

1. [Orchestrator](#orchestrator) — 2. [Instance](#instance) — 3. [Persona](#persona) — 4. [Artifact](#artifact) — 5. [Friction](#friction)
6. [Contribution](#contribution) — 7. [Isolation](#isolation) — 8. [H2A](#h2a) — 9. [Emergence](#emergence) — 10. [Wear (usure)](#wear-usure)

---

## Artifact

**Definition**: An asynchronous deposit in the shared space by a persona, intended for another persona or the team.
**Context**: `shared/` directory — notes, reviews, features, ADRs. Each artifact carries YAML frontmatter (from, to, nature, status, date).
**Not to be confused with**: deliverable (a persona's production within its workspace, not necessarily shared).
**Ref**: `protocol/exchange.md` §Artifacts.

## Archetype

**Definition**: A reusable persona template organized by role — a starting point, not a prescription.
**Context**: `canvas/archetypes/` — persona-architect, persona-dev, persona-researcher, etc.
**Not to be confused with**: persona (an archetype becomes a persona when instantiated with a name, scope, and prohibitions for a specific project).

## Binding

**Definition**: The materialization layer — how the protocol takes form in a concrete persistence system.
**Context**: `binding/` directory. Current binding: filesystem + Markdown + git. Future bindings: REST API, database.
**Not to be confused with**: provider (the AI tool layer) or protocol (the semantic layer).
**Decided on**: 2026-04-20 — ADR-014.

## Bootstrap

**Definition**: One of two persona derivation modes — the orchestrator projects roles from prior experience before any session.
**Context**: Derivation grammar, modes B1-B4. Typical at instance creation.
**Not to be confused with**: emergence (the other mode, where roles appear from observed gaps during work).
**Ref**: `doc/concepts/derivation-grammar.md`.

## Canvas

**Definition**: The inspiration layer — templates and patterns to avoid starting from scratch.
**Context**: `canvas/` directory — archetypes, artifact formats, patterns, workflows. Not prescriptive.
**Not to be confused with**: core (invariants) or protocol (contract).

## Constitutive

**Definition**: A property that defines what something *is*, not just how it behaves. Removing a constitutive property changes the nature of the entity.
**Context**: In SOFIA, friction is constitutive of the method — without friction, SOFIA is not SOFIA. The 7 entities in the model are constitutive (not optional components). The 5 H2A invariants are constitutive properties of the protocol.
**Not to be confused with**: regulative (a rule that governs behavior but doesn't define identity — e.g., "commit format" is regulative, "friction must be traced" is constitutive).

## Constrain / Challenge / Arbitrate

**Definition**: The three pillars of the SOFIA method — inseparable mechanisms that produce value through friction.
**Context**: Core method design. Constraint creates separation, challenge creates friction, arbitration creates decisions.
**Ref**: `core/principles.md`, `doc/site/methode.md`.

## Contribution

**Definition**: An epistemic input during an exchange — who brought what.
**Context**: `## Flow` section of session summaries. Each contribution has a direction (H or A) and a type (substance, structure, contestation, decision).
**Not to be confused with**: friction (a tension between positions — contribution is an input, friction is a clash).
**Ref**: `protocol/contribution.md`.

## Conventions

**Definition**: The instance-specific rules documented in `shared/conventions.md` — artifact types, naming, frontmatter, session format, friction markers.
**Context**: Each instance has its own conventions file. The template lives in `binding/filesystem/conventions.md`.
**Not to be confused with**: protocol (conventions are local rules, protocol is the universal contract).

## Core

**Definition**: The invariant layer — what doesn't change when you change tools or providers.
**Context**: `core/` directory — principles, model, duties.
**Not to be confused with**: protocol (the interface contract) or binding (the materialization).

## Wear (usure)

**Definition**: The progressive alignment of a persona with the orchestrator's thinking frame, resulting in loss of friction. Surfaces polish each other — the form of friction is preserved, the substance has disappeared. One of 5 instrumented failure modes (slip, wear, crush, asymmetry, instability).
**Context**: Signal: only `[sound]` frictions over a sustained period, challenge % descending, marker entropy decreasing. The persona stops challenging.
**Not to be confused with**: calibration (deliberate adjustment of constraints — wear is unintentional drift).
**Ref**: `binding/filesystem/analysis/cli/mirror.py` (compute_failure_modes)

## Duties

**Definition**: The six non-delegable responsibilities of the human orchestrator — verify facts, arbitrate, read what goes out, calibrate personas, separate reflection and production, maintain attention.
**Context**: `core/duties.md`.
**Not to be confused with**: operations (protocol actions) or principles (method design rules).

## Epistemic

**Definition**: Related to knowledge — how we know what we know, what counts as evidence, what qualifies a claim.
**Context**: In SOFIA, friction markers are epistemic qualifiers (they say something about the *status* of a position: well-founded, contestable, refuted). Contributions are tagged by epistemic type (substance, structure, contestation, decision). The observational layer is epistemic — it requires judgment, not computation.
**Not to be confused with**: operational (what to do) or structural (how things are organized).

## Emergence

**Definition**: One of two persona derivation modes — a new role appears from observed gaps during work (repeated deflections on the same domain).
**Context**: Derivation grammar, modes E1-E4. Typical during ongoing work.
**Not to be confused with**: bootstrap (the other mode, where roles are projected upfront).
**Ref**: `doc/concepts/derivation-grammar.md`.

## Exchange

**Definition**: Any interaction between the orchestrator and a persona — either a session (synchronous) or an artifact (asynchronous).
**Context**: A constitutive entity of the H2A model.
**Ref**: `protocol/exchange.md`.

## Friction

**Definition**: A qualified tension between two positions during an exchange — not a defect to fix but a structuring signal.
**Context**: Qualified with 5 markers (sound, contestable, simplification, blind_spot, refuted), an initiative tag, and a resolution tag. A constitutive entity of the H2A model.
**Not to be confused with**: conflict (friction is productive by design) or contribution (an input, not a tension).
**Ref**: `protocol/friction.md`.

## Frontmatter

**Definition**: The YAML metadata block at the top of every artifact and session summary — carries the protocol dimensions (from, to, nature, status, date, ref).
**Context**: Required by the protocol. No accents in values.
**Ref**: `binding/implementation.md` §Frontmatter.

## H2A

**Definition**: Human-to-Assistant — the coordination protocol between a human orchestrator and constrained AI personas. Organizational, not technical.
**Context**: `protocol/h2a.md`. Defines invariants, operations, the protocol/observational distinction, and audit criteria.
**Not to be confused with**: MCP (agent-tools protocol) or A2A (agent-agent protocol).

## Hidden condition

**Definition**: The prerequisite that SOFIA cannot verify — domain expertise, strong intention, and a cognitive trait that seeks contradiction.
**Context**: `doc/concepts/hidden-condition.md`. Three levels: expertise (visible), intention (discipline), cognitive trait (precedes the method).

## Instance

**Definition**: A concrete deployment of the SOFIA method on a project — a set of personas, a shared space, and conventions.
**Context**: Identified by a `sofia.md` file at its root.
**Not to be confused with**: the sofia/ repository (which contains the method, not an instance).

## Invariant

**Definition**: A constitutive property of the H2A protocol — without which H2A is no longer H2A.
**Context**: 5 invariants: constitutive friction, human arbiter, isolation, traceability, residual opacity.
**Not to be confused with**: principle (method design rules — broader than the protocol).
**Ref**: `protocol/h2a.md` §Invariants.

## Isolation

**Definition**: The structural separation of personas — each works in its own space and can only communicate through artifacts in the shared space.
**Context**: Invariant 3 of H2A. The orchestrator is the only one who crosses boundaries.
**Not to be confused with**: workspace (the physical directory — isolation is the principle, workspace is the implementation).

## Lineage

**Definition**: The chain linking related frictions across sessions via `ref:` fields — a logical friction may span multiple sessions.
**Context**: The current resolution is that of the last link. The trace remains immutable.
**Ref**: `protocol/friction.md` §Lineage.

## Marker

**Definition**: One of 5 epistemic qualifiers for a friction position — sound, contestable, simplification, blind_spot, refuted. Closed set.
**Context**: `## Orchestrator friction` section of session summaries and artifacts.
**Not to be confused with**: resolution (the outcome of the friction — ratified, contested, revised, rejected).
**Ref**: `protocol/friction.md` §Markers.

## Observational layer

**Definition**: The part of the protocol that requires semantic judgment — friction qualification, contribution tagging. Best-effort, not guaranteed.
**Context**: Distinguished from the protocol layer (computationally verifiable).
**Ref**: `protocol/h2a.md` §Protocol/observation distinction.

## Operation

**Definition**: An implicit action derived from H2A entities — openSession, closeSession, send, receive, markRead, markDone, qualifyFriction, qualifyContribution, reportPattern.
**Context**: `protocol/h2a.md` §Operations, `doc/guides/operator-guide.md`.

## Orchestrator

**Definition**: The human who steers the instance — opens sessions, routes artifacts, arbitrates frictions, makes final decisions. Sole passage between personas.
**Context**: A constitutive entity of the H2A model. Cannot be delegated to an AI.
**Not to be confused with**: Sofia (the guide persona that helps set up instances — Sofia doesn't orchestrate).

## Persona

**Definition**: A constrained AI role defined by 7 dimensions — identity, stance, scope, deliverables, prohibitions, right to contest, collaboration.
**Context**: Defined in a persona file (`shared/orga/personas/persona-{name}.md`). Operates in an isolated workspace.
**Not to be confused with**: archetype (a reusable template) or user (the human orchestrator).
**Ref**: `core/model.md` §Persona.

## Protocol layer

**Definition**: The part of H2A that is computationally verifiable — session traces, artifact metadata, status lifecycle, isolation.
**Context**: Distinguished from the observational layer (requires judgment).
**Ref**: `protocol/h2a.md` §Protocol/observation distinction.

## Provider

**Definition**: The AI provider layer — the concrete tool that runs the personas.
**Context**: `provider/` directory. Current provider: Claude Code. Replaceable without touching core or protocol.
**Not to be confused with**: binding (the persistence layer) or protocol (the semantic layer).
**Decided on**: 2026-04-20 — ADR-014.

## receive()

**Definition**: The operation where the orchestrator opens a session with a recipient and presents an artifact.
**Context**: Second step of artifact exchange (after send). The orchestrator filters, contextualizes, or transmits only a part.
**Ref**: `protocol/exchange.md` §send() and receive().

## reportPattern()

**Definition**: A meta-operation that mitigates the residual opacity of the orchestrator — detects thematic convergence of rejections, challenges the orchestrator with 3 argued hypotheses.
**Context**: Triggered when 3+ frictions are rejected on the same theme. The orchestrator must qualify their choice (LLM error, conviction, resistance). Auditable counter.
**Ref**: `protocol/friction.md` §reportPattern.

## Residual opacity

**Definition**: The structural limitation that the orchestrator cannot arbitrate their own resistance to friction — invariant 5 of H2A.
**Context**: Not a bug to fix. Mitigated by reportPattern(), but no mechanism constitutes a guarantee.
**Ref**: `protocol/h2a.md` §Invariants.

## Resolution

**Definition**: One of 4 epistemic outcome tags for a friction — ratified, contested, revised, rejected. Closed set.
**Context**: Set per friction point, after the `→` arrow. Can evolve across sessions via lineage.
**Not to be confused with**: marker (the qualification of the position — resolution is the outcome).
**Ref**: `protocol/friction.md` §Resolution.

## send()

**Definition**: The operation where a persona produces an artifact and deposits it in the recipient's shared space.
**Context**: First step of artifact exchange (before receive). Cross-instance: the artifact goes to the recipient instance's shared/, not the emitter's.
**Ref**: `protocol/exchange.md` §send() and receive().

## Session

**Definition**: A synchronous exchange between the orchestrator and one persona — the primary interaction mechanism.
**Context**: Produces a structured summary (Produced, Decisions, Shared notes, Open). Lifecycle: opening → exchange → closing.
**Not to be confused with**: artifact (asynchronous) or conversation (a session may span multiple conversations if the context is reloaded).
**Ref**: `protocol/exchange.md` §Sessions.

## Shared space

**Definition**: The sole communication channel between personas — a directory (`shared/`) where artifacts are deposited and routed by the orchestrator.
**Context**: Invariant 3 of H2A. Personas cannot access each other's workspaces.
**Not to be confused with**: workspace (a persona's private space).

## sofia.md

**Definition**: The instance marker file — identifies a directory as a SOFIA instance and declares its method version.
**Context**: Required at instance root (check PS1). Contains instance name, project, version, and team.
**Not to be confused with**: Sofia (the guide persona) or the sofia/ repository.

## Space

**Definition**: The isolated perimeter of a persona — one persona, one space.
**Context**: A constitutive entity of the H2A model. Contains the persona's workspace and sessions.
**Not to be confused with**: shared space (the exchange bus) or workspace (the implementation directory).

## Workspace

**Definition**: A persona's working directory containing CLAUDE.md and sessions/.
**Context**: Implementation of the space concept in the filesystem binding.
**Not to be confused with**: space (the protocol concept) or shared space (the exchange bus).
