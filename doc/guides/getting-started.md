# Getting started with SOFIA

> From prerequisites to your first friction — one document, everything you need.

---

## Prerequisites

**What you need**:
- A machine with a terminal (macOS, Linux, or WSL on Windows)
- A code editor (VS Code recommended — Claude Code integrates as an extension)
- Git installed
- Node.js installed (for Claude Code)

**Install Claude Code** (reference provider):
```bash
npm install -g @anthropic-ai/claude-code
```

SOFIA is provider-agnostic — the method works with any AI tool that can read a persona file and follow system instructions. With another provider (Mistral, Gemini, manual mode): copy the persona and context files as system instructions in your tool.

---

## What SOFIA is — in one minute

A method for orchestrating specialized AI assistants on a project. Each assistant has a role, a scope, and prohibitions. They don't talk to each other — you carry the context between them. Friction between roles produces better decisions.

Five things to know before you start:

1. **One persona = one strict role.** Define what it does NOT do before what it does. Constraint creates useful friction.
2. **Friction is productive.** If all personas agree, they're useless. Disagreements are the mechanism.
3. **The orchestrator decides. Always.** Personas propose, challenge, produce. You decide.
4. **Files are the protocol.** Personas exchange through artifacts (notes, reviews, specs), not chat. Slowness forces clarity.
5. **Start small, iterate.** One persona at launch. Others emerge from the work.

---

## How personas work

### One persona = one strict role

A persona is not a generic assistant. It is a constrained LLM: a name, a tone, a scope, and above all things it is **not allowed to do**.

Constraint changes everything. An architect who doesn't code is forced to specify. A developer who doesn't decide architecture is forced to question. A strategist without code access thinks in value, not implementation.

Define what the persona **does not do** before defining what it does.

### Friction is the mechanism

If all your personas agree, they're useless. Friction — an architect challenging the dev, a strategist questioning the priority — is the mechanism that produces better decisions.

Friction without an arbiter is chaos. The arbiter is you. You listen, question, then decide. A persona never validates its own proposals. A persona never forces acceptance of a decision.

### Isolation — each persona in its space

Each persona operates in its own workspace. It sees only its files. It cannot read or write elsewhere. Isolation forces formal exchanges: to communicate, personas deposit artifacts in a shared space (`shared/`).

![Instance anatomy](../figures/fig-instance-anatomy.svg)

The orchestrator is the only one who crosses boundaries — carrying context, filtering, reformulating.

### Files are the protocol

Personas don't "discuss" — they exchange through **artifacts**: reviews, notes, specs. These artifacts are versioned, traceable, and readable by all. File-based exchange is slower than chat. That's the point. Slowness forces clarity.

### Emergence — personas appear from the work

Subsequent personas are not planned. They emerge from the work. Every persona includes an **Emergence** section:

> *When you deflect a question because it's outside your scope, note the domain. If you deflect 3+ times on the same domain, signal it explicitly.*

The persona doesn't create the new persona — it signals the gap. You decide whether to act on it.

**Concrete example**: you're working with an architect. After a few sessions, it tells you 3 times "I don't code, you'd need someone to implement." That's the signal — a dev persona is needed. Not because you planned it, but because the work revealed the gap.

### Traceability — if it's not traced, it doesn't exist

Every session produces a structured summary (Produced, Decisions, Shared notes, Open). The summary is the bridge to the next session — the persona reads it at opening. Without it, continuity is lost.

Decisions are traced in ADRs (context, decision, alternatives, consequences). Exchanges are traced in artifacts with frontmatter (who, to whom, nature, status, date).

### The "no" test

A well-calibrated persona says "no" regularly:
- "That's not my role, check with [other persona]"
- "The spec isn't precise enough for me to code"
- "This decision needs an ADR before I implement"

If your persona never says no, its constraints are too loose.

---

## Sofia — the built-in guide (optional)

> **Alpha** — Sofia relies on the provider's conversational behavior. Results may vary. If the flow doesn't start, skip to the manual steps below.

Sofia is SOFIA's built-in guide. When you run `claude` in the sofia repo, it guides you to create your first instance:

1. **Your project** — Sofia asks what you're building
2. **First persona** — it proposes a structuring role. Not a list — a direct proposal you validate or adjust
3. **Calibration** — name, stance, scope, prohibitions. Sofia proposes, you adjust
4. **Generation** — Sofia produces the files and gives you starting keys

After generation, Sofia tells you: your persona will say no (by design), other personas will come (when the work makes them emerge), and you can come back anytime.

We recommend manual mode for your first instance — understanding the structure is more valuable than speed.

---

## Instance and project

A **SOFIA instance** is not your project. It's the space where personas think. Your **project** (code, product, site) lives elsewhere.

![Instance and project](../figures/fig-project-instance.svg)

The instance thinks. The project delivers. Personas work in the instance and produce deliverables that land in the project. Commits in the instance are automatic. Commits in the project go through the orchestrator.

Three configurations:

| Config | When |
|--------|------|
| **Single repo** — instance lives in a subfolder of the project | Simple to start, separate when the need arises |
| **Instance repo + project repo** — the standard case | Analysis history doesn't pollute the product repo |
| **Instance repo + multiple projects** — cross-cutting personas | Roadmaps in shared/ make the link |

---

## Step 1 — Clone the SOFIA repo

```bash
git clone https://github.com/oxynoe-dev/sofia
```

This is your reference — templates and documentation. You don't need to keep it in your project.

---

## Step 2 — Create the instance marker

At your project root (or instance root), create `sofia.md`:

```markdown
# SOFIA Instance

This repository is an **instance of the SOFIA method**.

- **Method**: [oxynoe-dev/sofia](https://github.com/oxynoe-dev/sofia)
- **Applied method version**: v0.3.x
- **Project**: {your project}
- **Team**: {number} AI assistants + 1 human orchestrator

## Instance structure

| Directory | Role | Persona |
|-----------|------|---------|
| `{workspace}/` | {description} | {persona} |
| `shared/` | Inter-persona exchange bus | Shared |
```

---

## Step 3 — Create the shared structure

```bash
mkdir -p shared/orga/personas shared/orga/contextes shared/notes shared/review
```

### conventions.md

Create `shared/conventions.md` — the exchange contract between personas:

```markdown
# Conventions

## Inter-persona exchanges

Personas don't talk to each other. They exchange through artifacts in shared/.

### Notes
- Format: `note-{to}-{subject}-{from}.md`
- Location: `shared/notes/`
- When processed: move to `shared/notes/archives/`

### Reviews
- Format: `review-{subject}-{from}.md`
- Location: `shared/review/`
- When processed: move to `shared/review/archives/`

## Commits
- Instance: `{persona}: {short summary} ({date})`
- Product repos: the orchestrator verifies and commits
```

**Artifact types explained**:
- **Note** — a message between personas: a signal, a question, a request. Short, directional (from → to). Example: `note-dev-design-tokens-architect.md`
- **Review** — a persona takes a position on another's work. Carries friction markers. Example: `review-api-spec-v2-dev.md`
- **Feature** — a shared functional spec. Not directional. Example: `feature-export-pipeline.md`

Each artifact carries a YAML frontmatter (`from`, `to`, `nature`, `status`, `date`). When processed, it migrates to `archives/`.

---

## Step 4 — Define your first persona

Start with **one**. Others will come.

### Choose the role

| Your context | First persona |
|-------------|--------------|
| Solo dev, messy code | Architect |
| Team, no specs | Product lead |
| Solo dev, design priority | Design system lead |
| Data/ML, unclear pipeline | Data architect |

The first persona is a **structuring** role — the one that frames your approach.

### Create the persona file

Create `shared/orga/personas/persona-{name}.md`. A persona has 7 dimensions:

```markdown
# {Name} — {Role}

## Profile
{Who this persona is, in one sentence.}

## Stance
{How it relates to you — formal? direct? cautious?}

## Scope
- {domain 1}
- {domain 2}

## What they produce
- {deliverable type 1}
- {deliverable type 2}

## What they do NOT do
- {prohibition 1 — the most important section}
- {prohibition 2}

## What they challenge
- {friction axis 1}

## Collaboration
| With | Mode |
|------|------|
| {other persona} | {how they interact} |
```

The "What they do NOT do" section is **the most important**. It creates the productive constraint. If you can't find a strong prohibition, the role doesn't justify a persona — it's a task, not a tension.

### Create the context file

Create `shared/orga/contextes/contexte-{name}-{product}.md` — the workspace-specific contract:

```markdown
---
persona: {name}
product: {product}
---

# Context {Name} — {Product} ({workspace})

## Scope
This workspace contains: {content description}

## Key documents
| File | Role |
|------|------|
| `{path}` | {description} |

## Isolation
- Never read/write outside `{authorized scope}`

## Workflow
0. Read the latest summary in `sessions/`
1. Read existing documents before any intervention
2. Produce {deliverables}

## Emergence
When you deflect 3+ times on the same domain, signal it.

## Session protocol — mandatory
Summary: `sessions/{YYYY-MM-DD}-{HHmm}-{name}.md`
Sections: Produced, Decisions, Shared notes, Open
```

The persona says **who you are**. The context says **where you are**.

---

## Step 5 — Create the workspace

```bash
mkdir -p {workspace}/sessions
```

### The CLAUDE.md

Create `{workspace}/CLAUDE.md` — a 2-line provider routing:

```markdown
Whatever the user's first message, at session opening, before any response, read these two files:
- `shared/orga/personas/persona-{name}.md`
- `shared/orga/contextes/contexte-{name}-{product}.md`
```

That's it. Content lives in the persona and context, not in the CLAUDE.md.

---

## Step 6 — First session

```bash
cd {workspace}
claude
```

The persona reads its CLAUDE.md, loads the persona and context, and behaves according to the contract. Give it a real task — not a test.

**Calibration signals**:
- **It refuses what's out of scope?** Good — the prohibitions work.
- **It accepts everything?** Tighten the prohibitions.
- **It's too rigid?** Soften the stance.
- **It doesn't know its workspace?** Enrich the context.

Calibration takes 2-3 sessions. That's normal.

### Session closing

When you're done, give the signal ("let's close"). The persona produces a summary:

```
sessions/2026-04-21-1430-architect.md
```

Mandatory sections: `## Produced`, `## Decisions`, `## Shared notes`, `## Open`. No prose — short lists, 30 lines max. Then commit:

```
architect: first session — scope definition + ADR-001 (2026-04-21)
```

The summary is the bridge to the next session. If it's not traced, it doesn't exist.

---

## Step 7 — Adding a second persona

When the need emerges — not before. SOFIA's value starts at 2 personas — a single persona generates no friction.

### Signals that trigger the need

- **Repeated deflection** — the first persona tells you "that's not my role" 3+ times on the same domain. That domain needs its own role.
- **Quality gap** — the persona produces something adequate but shallow. A dedicated role would do better. This signal is silent — you must notice it.
- **Two domains in tension** — you spend time arbitrating between concerns that belong to different axes.

### What to do

Go back to step 4. The new persona must be **in tension** with the existing one — if they agree on everything, one of them is unnecessary.

For the full derivation process, see [Derivation grammar](../concepts/derivation-grammar.md).

---

## Step 8 — First friction

Your two personas are set up. Now the method starts producing value.

1. Open a session with Persona A — get a deliverable
2. Close the session
3. Open a session with Persona B — present Persona A's deliverable
4. Watch what happens — Persona B, with different constraints, sees what Persona A missed

That moment — when Persona B pushes back — is SOFIA working. Not because the AI is smarter, but because the structure forces a different angle.

### You are the message bus

Personas don't talk to each other. You carry the context. Each transmission is a moment where you filter, reformulate, add context, decide what is relevant.

**What you don't delegate**:
- Prioritization — which persona intervenes, in what order
- Consolidation — synthesizing feedback from multiple personas
- Decision — deciding when personas diverge
- Filtering — what is relevant to transmit or not

It's slow. That's the cost of quality.

---

## Anti-patterns

| Pattern | Problem |
|---------|---------|
| The generalist persona | Does everything, therefore nothing well |
| The compliant persona | Says yes to everything, never challenges |
| The double hat | "Architect who also codes" — blurs the constraint |
| Too many personas too early | Start with 1, not 5 |
| The ghost persona | Created but never used — delete it |
| No isolation | Without boundaries, the persona overflows |
| Approving without reading | When you rubber-stamp, you've stopped orchestrating |

---

## Checklist

- [ ] Prerequisites installed (terminal, VS Code, Claude Code, git)
- [ ] `sofia.md` at root
- [ ] `shared/conventions.md`
- [ ] `shared/orga/personas/persona-{name}.md` (7 dimensions)
- [ ] `shared/orga/contextes/contexte-{name}-{product}.md`
- [ ] `{workspace}/CLAUDE.md` (2-line routing)
- [ ] `{workspace}/sessions/`
- [ ] First session launched
- [ ] The persona says "no" when it should

---

## Going further

### The method

- [Principles](../../core/principles.md) — the 7 invariant principles
- [Model](../../core/model.md) — the 7 constitutive entities
- [Duties](../../core/duties.md) — non-delegable orchestrator responsibilities
- [Architecture](../concepts/architecture.md) — 5 layers + canvas
- [Hidden condition](../concepts/hidden-condition.md) — target profile, cognitive trait
- [Derivation grammar](../concepts/derivation-grammar.md) — how personas come into existence

### The protocol

- [H2A](../../protocol/h2a.md) — the coordination protocol
- [Friction](../../protocol/friction.md) — markers, resolutions, lineage
- [Exchange](../../protocol/exchange.md) — sessions, artifacts, routing
- [Contribution](../../protocol/contribution.md) — epistemic flow

### The provider

- [CLAUDE.md anatomy](../../provider/claude-code/claude-md.md) — the 3-layer routing
- [Sessions](../../provider/claude-code/sessions.md) — session summary format
- [Memory](../../provider/claude-code/memory.md) — persistent memory between sessions

### Inspiration

- [Archetypes](../../canvas/archetypes/README.md) — persona templates by role (with prohibition summary)
- [Artifact formats](../../canvas/artifacts/README.md) — note, review, feature, ADR... (with frontmatter reference)
- [Patterns](../../canvas/patterns/) — challenger, inspector, memory, media calibration
- [Workflows](../../canvas/workflows/) — dev, publication, ADR, research, onboarding
- [Field feedback](../feedback/) — experience reports (N=1)
- [Glossary](../reference/lexique.md) — all SOFIA terms defined
