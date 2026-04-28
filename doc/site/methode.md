---
from: mira
to: sofia, nora
nature: content
date: 2026-04-05
subject: Method page — architectural overview of SOFIA
source: core/*.md, doc/concepts/architecture.md
---

# The SOFIA method

> Specialized roles that think with you. The product emerges from their friction.

An AI assistant that can do everything does nothing well. It agrees too easily, forgets its scope, and produces generic output that reads like it could come from anywhere. The more capable the model, the worse the problem — because a powerful generalist is a convincing generalist.

SOFIA is a method for turning general-purpose AI assistants into a team of specialized roles that constrain each other. Each role has a strict scope, explicit prohibitions, and a stance. They don't talk to each other — a human orchestrator carries the context between them, filters, reformulates, and decides. The friction between roles is not a side effect. It's the mechanism that produces better decisions.

The method works with any AI provider that can read a system prompt. It was developed and validated across hundreds of sessions on real projects, not designed from theory. Everything in it — the principles, the duties, the failure modes — was extracted from observed dysfunction and success.

SOFIA is for people who already use AI assistants and want more from them: sharper output, traceable decisions, and the ability to scale without losing quality. It requires an orchestrator who reads, questions, and decides — the method doesn't work on autopilot.

---

## Anatomy of a persona

A persona is an AI assistant constrained by an **instruction file** (`persona.md`) that defines its identity, stance, scope, and prohibitions.

Each persona operates in its own workspace. It sees only its files. It cannot read or write elsewhere. Isolation forces formal exchanges: to communicate, you must deposit an artifact.

Without isolation, assistants converge. They read each other's work, absorb each other's reasoning, and end up producing the same answer from different angles. Isolation prevents this — it guarantees that when two personas disagree, the disagreement is real.

![Anatomy of a persona](figures/fig-methode-persona.svg)

### What surrounds a persona

**Sessions** — Each conversation produces a summary. It's the bridge between sessions: the next one starts by reading the previous one. Without this, the persona loses its thread and each session starts from zero. Structured format, 30 lines max.

**Deliverables** — Each persona produces typed deliverables according to its role: specs, reviews, code, strategic notes, mockups. Not generic text — named, addressable, versioned artifacts. If you can't name what the persona produced, the session was noise.

**Exchanged artifacts** — Personas don't talk to each other. They deposit files in a shared bus (`shared/`). Notes, reviews, features — each with frontmatter that says who wrote it, for whom, and whether it's been processed. This forces the orchestrator to actively route information instead of letting it flow unfiltered.

**Emergence** — A well-constrained persona detects when a question falls outside its scope. After repeated deflections on the same domain, it signals the gap. The next persona is born from this observation, not from an initial plan. You don't design an org chart — you let the work reveal what's missing.

---

## Orchestration

The orchestrator is the message bus. Nothing flows between personas without them.

![Orchestration — the orchestrator's role](figures/fig-methode-orchestration.svg)

The orchestrator opens a session with a persona, gets a deliverable, closes the session. Opens a session with another persona, transmits the deliverable, collects the reaction. Each transmission is a moment of filtering, reformulation, context addition.

This is where quality happens. When the orchestrator transmits a review from one persona to another, they choose what to include, what to rephrase, what context to add. A raw handoff — "here's what the architect said" — is a missed opportunity. A good handoff is a translation between worldviews.

**What the orchestrator does not delegate**:
- **Prioritization** — which persona intervenes, in what order. The orchestrator sees the whole board; each persona sees only its square.
- **Consolidation** — synthesizing feedback from multiple personas. Three reviews don't add up by themselves.
- **Decision** — deciding when personas diverge. If nobody arbitrates, friction becomes noise.
- **Filtering** — what is relevant to transmit or not. Some deliverables need context stripping before reaching the next persona.

It's slow. That's the cost of quality. If the exchange isn't worth the cost, the subject didn't need multiple personas.

---

## Three pillars

SOFIA rests on three ideas. They don't work without each other.

**Constrain** — An AI assistant without limits says yes to everything and produces nothing good. SOFIA gives each assistant a strict role, a scope, and above all prohibitions — what it must *not* do. It's the limitation that makes it useful. An architect who can also code will code instead of challenging the spec. A researcher who can also write blog posts will drift from sourcing to storytelling. The prohibition is what keeps the persona honest.

**Challenge** — If all roles agree, nobody thinks. The friction between an architect who refuses to code and a developer who refuses to implement a vague spec is a signal, not a bug. Disagreements force clarity. Without challenge, the orchestrator gets confirmation from every angle and mistakes it for validation. The most dangerous output is the one everyone approved without questioning.

**Arbitrate** — Friction without an arbiter is chaos. The orchestrator listens, questions, then decides. Always. No assistant validates its own proposals. No assistant forces acceptance of a decision. Arbitration is what transforms disagreement into a traced decision. Without it, personas either deadlock or one silently wins by volume.

![The three pillars of SOFIA](figures/fig-methode-piliers.svg)

---

## The model

Three interdependent objects. The constrained persona produces artifacts. Artifacts create friction when challenged by other personas. Friction produces better decisions. The orchestrator steers the cycle.

Remove one element and the system degrades. Personas without artifacts produce untraceable conversations. Artifacts without friction produce unchallenged documents. Friction without personas produces generic disagreement — no stance, no expertise, no skin in the game.

![Conceptual model — Persona, Artifact, Friction](figures/fig-triangle-sofia.svg)

### Pillars and concepts

The pillars say *why*, the concepts say *how*.

| Pillar | Concept | Link |
|--------|---------|------|
| **Constrain** | Persona | The persona is the vehicle of constraint — strict role, bounded scope, prohibitions |
| **Challenge** | Friction | Friction arises when constrained personas confront each other on the same subject |
| **Arbitrate** | Artifact | The artifact is the support of arbitration — traced, versioned, addressable. The orchestrator decides on evidence |

---

## Seven principles

| # | Principle | In brief |
|---|-----------|----------|
| 1 | Friction is productive | Disagreements between roles are signals, not problems to suppress |
| 2 | The orchestrator arbitrates | Assistants propose, the orchestrator decides — never the reverse |
| 3 | Every voice counts | An unused role is a role to remove, not a role to keep "just in case" |
| 4 | Constraint forces quality | Define what the role doesn't do before what it does |
| 5 | Artifacts are the protocol | Exchanges go through files, not chat — what isn't written down doesn't exist |
| 6 | Everything is traced | If it's not traced, it didn't happen. Sessions, decisions, friction — all on record |
| 7 | Start small, iterate | One role at the start. The others emerge from the work, not from a plan |

These principles are not aspirational. They are operational constraints — each one exists because its absence was observed to cause a specific failure in practice.

---

## The gradient

The method doesn't deploy as big bang. It grows with the project.

| Threshold | What activates | Why now |
|---|---|---|
| 1 persona | persona.md + sessions/ — the base | Even a single constrained assistant outperforms an unconstrained one |
| 2+ personas | shared/ — the exchange bus (notes, reviews) | Two personas need a way to exchange without reading each other's workspace |
| 3+ personas | per-workspace roadmaps | The orchestrator can no longer hold all priorities in their head |
| 4+ personas | features/ — formalized specs | Informal notes no longer scale — you need structured specs before production |

Start small. Add structure when the orchestrator's cognitive load demands it — not before. Premature structure is overhead that slows you down without protecting you from anything.

---

## Five layers

The method is structured in five independent layers. You can change one without touching the others. This matters because lock-in is the first thing teams worry about — and rightly so.

**Core** — The invariants. Principles, model, friction, duties. What doesn't change when you change tools. If Claude Code disappears tomorrow, core holds. This is the part you can read on paper and still understand the method.

**Protocol** — The interface contract. H2A (Human-to-Assistant — the coordination protocol between a human orchestrator and constrained AI personas), exchanges, friction, contribution. The semantics of interactions, not their materialization. Protocol says *what* a friction marker means. It doesn't say where you store it.

**Binding** — The materialization. How the protocol takes form in a concrete persistence system (filesystem + Markdown + git today, REST API or database tomorrow). If you wanted to run SOFIA with a web app instead of files, you'd rewrite this layer and nothing else.

**Provider** — The AI provider. CLAUDE.md, Claude Code, hooks, persistent memory. Replaceable without touching the rest. It's the only layer that changes when porting SOFIA to another provider (Mistral, Gemini, etc.).

**Canvas** — Tools so you don't start from scratch. Persona archetypes, artifact formats, patterns, workflows. Not prescriptive — inspiration material. Take what fits, ignore the rest.

| Layer | Content | Changes when... |
|---|---|---|
| **Core** | principles, model, friction, duties | ...the method evolves (rare) |
| **Protocol** | H2A, exchanges, friction, contribution | ...the semantics of interactions evolve |
| **Binding** | filesystem stack, conventions, audit, dashboard | ...you change persistence system |
| **Provider** | CLAUDE.md, hooks, sessions, memory | ...you change AI provider |
| **Canvas** | archetypes, artifacts, patterns, workflows | ...you add inspiration |

---

## Six orchestrator duties

Personas produce, challenge, document. But some responsibilities cannot be delegated — not because the AI can't do them, but because delegating them removes the human judgment that makes the system work.

1. **Verify facts** — LLMs don't count. Dates, numbers, references: systematic human verification. A false datum that enters the system propagates through every subsequent document.
2. **Arbitrate** — Listen, question, decide. The decision is traced. An unresolved friction is worse than no friction — it teaches the persona that challenge has no consequence.
3. **Read what goes out** — No document goes out without full review. The moment you approve without reading, you've transferred quality control to the machine.
4. **Calibrate personas** — Adjust constraints continuously. A persona that never challenges is either worn out or miscalibrated. A persona that challenges everything is noise.
5. **Separate reflection and production** — The one who writes is not the one who validates. This applies to personas and to the orchestrator's own work.
6. **Maintain attention** — When you approve without reading, that's the moment to slow down. Fatigue is the most reliable predictor of silent failure.

---

## What can go wrong

Friction is a mechanism. Like any mechanism, it can fail. SOFIA classifies failure modes into two categories based on detectability.

**Instrumented failures** are dysfunctions of the friction mechanism itself — the protocol produces the data to detect them. Five modes: *slip* (friction without arbitration), *wear* (a persona stops challenging), *crush* (one side imposes by force), *asymmetry* (friction flows in one direction only), *instability* (change without convergence). The [dashboard](doc/audit-dashboard-guide.html) flags them automatically from session data.

**Silent failures** are dysfunctions of the environment in which friction operates. No parser detects them. Six modes: *instrumentation bias* (the measurer's biases infect the measurement), *factual contamination* (a false datum stabilizes through repetition), *validation without reading* (sessions become ritual), *scope drift* (a persona absorbs other roles), *shared blind spot* (all personas inherit the orchestrator's biases), *load transfer* (cost shifts to infrastructure).

The two classes are not independent — silent failures cause or mask instrumented ones. Validation without reading produces slip. Scope drift produces wear. Instrumentation bias masks wear. The six orchestrator duties are the governance response.

For detection thresholds, signals, and the causal map between the two classes, see [Failure Modes](doc/concepts-failure-modes.html).

---

## Field

The method was developed and validated on the Katen project — a formally verified orchestration engine for Data & AI pipelines, built with specialized AI personas across hundreds of sessions. The failure modes, the duties, the gradient — none of these were designed upfront. They were extracted from observed dysfunctions and successes over months of daily practice.

[Read the full story →](histoire.md)

---

Continue → [Understand](doc/guides-understand.html)
