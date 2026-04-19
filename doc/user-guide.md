# SOFIA User Guide

> Specialized roles that think with you. The product emerges from their friction.

---

## In one minute

SOFIA is a method for orchestrating specialized AI assistants on a project. Each assistant has a role, a scope, and prohibitions. They don't talk to each other — you carry the context between them. Friction between roles produces better decisions.

To start: clone the repo, run `claude`, and Sofia — the built-in guide — proposes your first persona. If the flow doesn't start, the [manual mode](getting-started.md) covers the same thing step by step.

> **Alpha preview** — Sofia relies on the runtime's conversational behavior. Results may vary depending on the environment.

```
git clone https://github.com/oxynoe-dev/sofia
cd sofia
claude
```

> Git is not required to use SOFIA, but strongly recommended. Session summaries, notes, and reviews are files — git gives you traceability and context persistence between sessions.

---

## 1. The essentials

### One persona = one strict role

A persona is not a generic assistant. It is a constrained LLM: a name, a tone, a scope, and above all things it is **not allowed to do**.

Constraint changes everything. An architect who doesn't code is forced to specify. A developer who doesn't decide architecture is forced to question. A strategist without code access thinks in value, not implementation.

Define what the persona **does not do** before defining what it does.

### Friction is productive

If all your personas agree, they're useless. Friction — an architect challenging the dev, a strategist questioning the priority — is the mechanism that produces better decisions.

Friction without an arbiter is chaos. The arbiter is you.

### The orchestrator decides. Always.

Personas propose, challenge, produce. The orchestrator decides. A persona never validates its own proposals. A persona never forces acceptance of a decision. This is SOFIA's non-negotiable rule.

### Files are the protocol

Personas don't "discuss" — they exchange through **artefacts**: reviews, notes, specs. These artefacts are versioned, traceable, and readable by all. File-based exchange is slower than chat. That's the point. Slowness forces clarity.

### Start small, iterate

One persona at launch. Two when the first is calibrated. Three when the need is clear. The method doesn't deploy as a big bang. It grows with the project.

---

## 2. What you just cloned

The SOFIA repo is not your project — it's the **method**. It contains:

- `core/` — the invariants: principles, model, friction, duties
- `protocol/` — the interface contract: artefacts, conventions, isolation, orchestration
- `runtime/` — the concrete implementation for Claude Code (other providers will follow)
- `doc/` — guides, workflows, patterns, field feedback

Your project will live elsewhere, in its own repo. SOFIA helps you organize the AI assistants working on it. The [Isolation](#instance-and-project) section details the possible configurations.

---

## 3. Getting started with Sofia

> **Alpha preview** — Sofia relies on the runtime's conversational behavior. Results may vary depending on the provider, model version, and environment. If the flow doesn't start or drifts, switch to manual mode (see next section).

Sofia is SOFIA's built-in guide. When you run `claude` in the repo, it guides you to create your first persona.

### The flow

1. **Your project** — Sofia asks what you're building (1-2 turns)
2. **First persona** — it proposes a structuring role adapted to your context. Not a list of choices — a direct proposal you validate or adjust
3. **Calibration** — name, tone, scope (what it does and doesn't). Sofia proposes, you adjust
4. **Generation** — Sofia produces the CLAUDE.md and gives you three starting keys

### The first persona heuristic

| Your profile | Proposed first persona |
|-------------|----------------------|
| Solo dev, MVP, messy code | Architect |
| Team, no specs | Product lead |
| Solo dev, design priority | Design system lead |
| Data/ML, unclear pipeline | Data architect |

The first persona is always a structuring role — never an executor. It frames your approach. Others will come later.

### The starting briefing

After generating your first CLAUDE.md, Sofia tells you three things:

- **Your persona will say no.** That's by design. When it refuses a request because it's out of scope, that's a signal — not a bug.
- **Other personas will come.** Not now. When the work makes them emerge.
- **You can come back.** Relaunch Sofia anytime to add a persona or adjust this one.

---

## 4. Working with a persona

### The CLAUDE.md

It's the contract between you and your persona. It contains:

- **Who** — name, role, posture
- **What** — scope of intervention, expected deliverables
- **Where** — which files/directories are accessible
- **Forbidden** — what is out of scope (read AND write)
- **How** — conventions, formats, session workflow

Aim for 60-100 lines. Beyond that, context dilutes.

### Session opening

The persona reads the latest summary in `sessions/`. The orchestrator decides what to look at. No systematic recitation.

### Session closing

1. Summary in `sessions/` — Produced, Decisions, Shared notes, Open
2. Direct commit in the instance — `{persona}: {short summary} ({date})`
3. If the persona produced changes for your project (code, site, etc.) — prepare the commit message, the orchestrator verifies and executes

No prose. Short lists. 30 lines max.

### The "no" test

A well-calibrated persona says "no" regularly:
- "That's not my role, check with [other persona]"
- "The spec isn't precise enough for me to code"
- "This decision needs an ADR before I implement"

If your persona never says no, its constraints are too loose.

---

## 5. Emergence — subsequent personas

Subsequent personas are not planned. They emerge from the work.

### The mechanism

Every CLAUDE.md generated by Sofia includes an **Emergence** section:

```
## Emergence
When you deflect a question because it's outside your scope,
note the domain. If you deflect 3+ times on the same domain,
signal it explicitly:
"I regularly receive questions about [domain] —
it's outside my scope. You might need
a dedicated persona. Relaunch Sofia if you want to create one."
```

The persona doesn't create the new persona — it signals the gap. You return to Sofia who resumes the flow.

### Concrete example

You're working with an architect. After a few sessions:
- It tells you 3 times "I don't code, you'd need someone to implement"
- It signals: "You might need a dedicated dev persona"
- You relaunch Sofia, which proposes a dev calibrated for your project

This is exactly what happened on the Katen project: the first persona (architect) was set. The 6 others emerged by necessity through the work. Nobody had planned them.

---

## 6. Isolation

### Instance and project

A **SOFIA instance** is not your project. It's the space where your personas think, plan, and exchange. Your **project** (the code, the product, the site) lives elsewhere, in its own repo.

![Instance and project](figures/fig-project-instance.svg)

The instance thinks. The project delivers. Personas work in the instance and produce deliverables that land in the project. Commits in the instance are automatic. Commits in the project go through the orchestrator.

Three possible configurations:

- **Single repo** — the instance lives in a subfolder of the project. Simple to start, you'll separate when the need arises.
- **One instance repo + one project repo** — the standard case. Analysis history doesn't pollute the product repo. If the project is public, internal tooling stays private.
- **One instance repo + multiple projects** — personas have a cross-cutting view. Roadmaps in `shared/` make the link. CLAUDE.md files reference product repos via absolute paths.

### Instance anatomy

An instance contains **workspaces** (one per persona) and a **shared zone** (`shared/`). Each workspace is isolated — a persona cannot read or write in another's workspace. The only communication goes through `shared/`.

![Instance anatomy](figures/fig-instance-anatomy.svg)

### The shared zone — shared/

The only space all personas can read and write. Exchanges go through artefacts deposited here:

| Type | Convention | Location |
|------|-----------|----------|
| Notes | `note-{to}-{subject}-{from}.md` | `shared/notes/` |
| Reviews | `review-{subject}-{from}.md` | `shared/review/` |
| Features | `feature-{subject}.md` | `shared/features/` |

Each artefact carries a frontmatter (`from`, `to`, `nature`, `status`, `date`). When processed, it migrates to `archives/`.

### Roadmaps

Planning lives in `shared/roadmap-{product}.md`. Each roadmap has an **owner** (coherence guardian) and each item carries an **@owner** (execution responsible).

There is no per-persona backlog. All items live in roadmaps.

---

## 7. Orchestration — the orchestrator's role

### You are the message bus

Personas don't talk to each other. You carry the context. You can open multiple terminals in parallel — one per persona — to accelerate exchanges:

1. You open a session with a persona
2. It produces a deliverable
3. You close the session
4. You open a session with another persona
5. You transmit the deliverable
6. You collect the reaction

Each transmission is a moment where you filter, reformulate, add context, decide what is relevant to transmit.

### What you don't delegate

- **Prioritization** — which persona intervenes, in what order
- **Consolidation** — synthesizing feedback from N personas
- **Decision** — deciding when personas diverge
- **Filtering** — what is relevant to transmit or not

### The cost

Orchestration takes time. It's the price of quality. If the exchange isn't worth the cost, the subject didn't need multiple personas.

---

## 8. Traceability

### Traceability artefacts

1. **Session summaries** — each session produces a summary. It's the bridge between conversations. Format: `sessions/{YYYY-MM-DD}-{HHmm}-{persona}.md`

2. **Notes** — inter-persona messages deposited in `shared/notes/`. Format: `note-{to}-{subject}-{from}.md`

3. **Cross-reviews** — when a persona intervenes on another's work, it produces a review with factual observations, prioritized recommendations, and open questions. Format: `review-{subject}-{from}.md`

4. **Features** — shared functional specs. Format: `feature-{subject}.md` in `shared/features/`

5. **ADR** — structural decisions are traced: context, decision, alternatives, consequences, status. The ADR is written before implementation.

### If it's not traced, it doesn't exist

The next session won't have your context in mind. Summaries are its memory.

---

## 9. Anti-patterns

| Pattern | Problem |
|---------|---------|
| The generalist persona | Does everything, therefore nothing well |
| The compliant persona | Says yes to everything, never challenges |
| The double hat | "Architect who also codes" — blurs the posture |
| Too many personas too early | Start with 1, not 5 |
| The ghost persona | Created but never used — delete it |
| Open questions at startup | The user doesn't know what they need |
| No isolation | Without boundaries, the persona overflows |
| No traceability | Without summaries, continuity is lost |

---

## Going further

### The method in depth

- [Principles](../core/principles.md) — the 7 principles in detail
- [Model](../core/model.md) — entity anatomy, relationships
- [Duties](../core/duties.md) — non-delegable orchestrator responsibilities

### The protocol

- [H2A](../protocol/h2a.md) — the coordination protocol
- [Friction](../protocol/friction.md) — markers, resolutions, lineage
- [Exchange](../protocol/exchange.md) — sessions, artefacts, routing
- [Contribution](../protocol/contribution.md) — epistemic flow

### The Claude Code implementation

- [CLAUDE.md](../runtime/claude-code/claude-md.md) — anatomy of a CLAUDE.md
- [Sessions](../runtime/claude-code/sessions.md) — session summary format
- [Memory](../runtime/claude-code/memoire.md) — persistent memory between sessions

### Learn by example

> The examples below come from the Katen project. The deliverables mentioned (ADR, design system, research notes...) are project-specific — adapt to your context. What transfers is the structure: constrained roles, isolation, traced artefacts.

- Workflows — standard processes (dev, publication, ADR, research...)
- Patterns — recurring structures (challenger, distillery, escalation...)
- [Field feedback](feedback/) — Katen returns, pattern identification context (N=1)
- Manual mode — install SOFIA without Sofia, step by step
