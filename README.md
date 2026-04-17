# SOFIA

> Specialized roles that think with you. The product emerges from their friction.

---

## The problem

A generalist LLM does everything. Poorly.

It codes, advises, writes, reviews — in the same conversation,
with the same tone, no scope constraints. It says yes to everything.
It challenges nothing. It remembers nothing.

The result: a servile assistant producing average content,
without friction, without trace, without progression.

## The thesis

**Constrained roles produce better than a free agent.**

An architect who doesn't code is forced to specify clearly.
A developer who doesn't decide architecture is forced to
surface frictions. A strategist without code access is forced
to think in value, not implementation.

Constraint is not a limit — it's what forces quality.

## What SOFIA is

An **agnostic method** for working with specialized AI personas,
in intentional friction, steered by a human orchestrator who arbitrates.
Principles and protocol depend on no tool;
`runtime/` provides an implementation for Claude Code, others can follow.

Concretely:
- **Personas** — AI roles with a name, posture, scope, prohibitions
- **Friction** — personas challenge each other, the orchestrator decides
- **Isolation** — each persona has its workspace, instructions, boundaries
- **Orchestration** — the orchestrator is the message bus, carrying context between personas
- **Traceability** — everything is traced: decisions, sessions, reviews, exchanges
- **Artefacts** — personas communicate through files, not chat

## What SOFIA is not

- Not a framework — no code to install, no dependency
- Not a product — it's a method, documented in a repo

## Quick start

```bash
git clone https://github.com/oxynoe-dev/sofia
cd sofia
claude
```

Claude Code opens the repo, loads the built-in guide (Sofia) and asks
the right questions. In 10 minutes, you have your first persona
calibrated for your project.

> **Alpha preview** — Sofia relies on the runtime's conversational behavior. Results may vary depending on the environment. If the flow doesn't start, the [manual mode](doc/getting-started.md) covers the same thing step by step.

## Learn more

| | |
|---|---|
| `core/` | The invariants — principles, model, friction, duties |
| `protocol/` | The interface contract — H2A, exchange, friction, contribution |
| `runtime/` | The concrete implementation — Claude Code today, Mistral tomorrow, others after |
| `doc/` | Guides, workflows, patterns, field feedback, architecture, ADR |

## Origin

SOFIA was born from the Katen project — a formally verified
orchestration engine for Data & AI pipelines, built with 7 specialized
AI assistants (architect, dev, UX, researcher, strategist, designer,
writer) across 280+ sessions.

A method that emerged from personal practice — to be confronted
with your expertise.

**Site**: [oxynoe.io/sofia](https://oxynoe.io/sofia/)

## License

MIT
