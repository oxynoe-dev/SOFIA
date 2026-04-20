# SOFIA

> A method for orchestrating specialized AI personas through intentional friction.

---

## What SOFIA is

An **agnostic method** for working with constrained AI roles,
steered by a human orchestrator who arbitrates.

Each persona has a name, a stance, a scope, prohibitions.
They don't talk to each other — they exchange through artifacts.
The orchestrator carries context, routes, decides.

Principles and protocol depend on no tool;
`provider/` provides an implementation for Claude Code, others can follow.

### Key concepts

- **Personas** — AI roles with a name, stance, scope, prohibitions
- **Friction** — personas challenge each other, the orchestrator decides
- **Isolation** — each persona has its workspace, instructions, boundaries
- **Orchestration** — the orchestrator is the message bus between personas
- **Traceability** — decisions, sessions, reviews, exchanges are traced
- **Artifacts** — personas communicate through files, not chat

### What SOFIA is not

- Not a framework — no code to install, no dependency
- Not a product — a method, documented in a repo

---

## Quick start

```bash
git clone https://github.com/oxynoe-dev/sofia
cd sofia
claude
```

The built-in guide (Sofia) walks you through instance creation.

> **Alpha** — Sofia relies on the runtime's conversational behavior. Results may vary. If the flow doesn't start, [manual mode](doc/getting-started.md) covers the same steps.

---

## Repository structure

| Directory | Content |
|-----------|---------|
| `core/` | Invariants — principles, model, friction, duties |
| `protocol/` | Interface contract — H2A, exchange, friction, contribution |
| `binding/` | Materialization — filesystem scripts, audit, analysis |
| `provider/` | Provider implementation — Claude Code (others planned) |
| `canvas/` | Inspiration — archetypes, artifacts, patterns, workflows |
| `doc/` | Guides, architecture, field feedback, ADR |

---

## Origin

SOFIA emerged from the Katen project — an orchestration engine
for Data & AI pipelines, built with 7 specialized AI personas
across 280+ sessions.

A method extracted from practice — to be confronted with yours.

**Site**: [oxynoe.io/sofia](https://oxynoe.io/sofia/)

## License

MIT
