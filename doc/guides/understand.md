---
title: Understanding the method
---

## Prerequisites

**What you need**:
- A machine with a terminal (macOS, Linux, or WSL on Windows)
- A code editor (VS Code recommended — Claude Code integrates as an extension)
- Git installed

**Install Claude Code** (reference provider):
```bash
curl -fsSL https://claude.ai/install.sh | sh
```

SOFIA is provider-agnostic — the method works with any AI tool that can read a persona file and follow system instructions. With another provider (Mistral, Gemini, manual mode): copy the persona and context files as system instructions in your tool.

---

# Understanding the method

## What SOFIA is — in one minute

A method for orchestrating specialized AI assistants on a project. Each assistant has a role, a scope, and prohibitions. They don't talk to each other — you carry the context between them. Friction between roles produces better decisions.

Five things to know before you start:

1. **One persona = one strict role.** Define what it does NOT do before what it does. Constraint creates useful friction.
2. **Friction is productive.** If all personas agree, they're useless. Disagreements are the mechanism.
3. **The orchestrator decides. Always.** Personas propose, challenge, produce. You decide.
4. **Files are the protocol.** Personas exchange through artifacts (notes, reviews, specs), not chat. Slowness forces clarity.
5. **Start small, iterate.** One persona at launch. Others emerge from the work.

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

## Orchestration — the orchestrator's role

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
