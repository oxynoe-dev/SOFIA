# SOFIA

> A method for orchestrating specialized AI personas through intentional friction.

---

## Why SOFIA

A single AI assistant can challenge when asked — but nothing in the structure guarantees that the challenge happens. The contestation depends on the practitioner remembering to ask, at the right moment, while the assistant maintains a critical stance across a conversation whose context drifts over time.

SOFIA addresses two structural limitations. First, friction becomes organizational rather than accidental: multiple AI personas with constrained roles, explicit prohibitions, and a human orchestrator who arbitrates. The friction between roles surfaces blind spots and forces clarification — not because any individual persona is better at challenging, but because the structure makes contestation unavoidable. Second, each persona maintains a persistent memory through structured sessions, versioned artifacts, and isolated workspaces. What one session produces, the next session reads. Decisions, frictions, and contributions accumulate across sessions rather than evaporating with the conversation window.

## What SOFIA is

A method for working with multiple AI assistants on the same project, where each assistant has a constrained role and they challenge each other's work. A human orchestrator steers the whole thing — they arbitrate disagreements, route information, and make final decisions.

Give an assistant a strict role, prohibitions, and put it in tension with another role — now you have useful friction. The disagreements between roles force clarity, surface blind spots, and produce better decisions than any single assistant could.

### How it works

You define **personas** — AI roles with a name, a stance, a scope, and prohibitions. An architect who doesn't code. A developer who doesn't decide architecture. A researcher who doesn't simplify. Each persona works in its own isolated workspace and can only communicate through **artifacts** (files deposited in a shared space). The orchestrator is the sole router between personas.

The method traces everything: sessions produce structured summaries, frictions are qualified with epistemic markers, contributions are tagged by direction and type. An audit tool can verify protocol conformity across instances.

### What it contains

- **Core** — the invariant principles and conceptual model (personas, friction, orchestration)
- **H2A protocol** — the coordination protocol between human and assistants (invariants, operations, friction qualification)
- **Binding** — how the protocol materializes in practice (filesystem + Markdown + git today)
- **Provider** — the AI provider layer (Claude Code today, others planned)
- **Canvas** — templates and patterns to get started (persona archetypes, artifact formats, workflows)
- **Documentation** — architecture, guides, field feedback from real projects, ADRs

### What it is not

- Not a framework — no code to install, no dependency
- Not a chatbot wrapper — personas don't assist, they challenge
- Not tool-specific — principles and protocol depend on no tool

---

## Quick start

```bash
git clone https://github.com/oxynoe-dev/sofia
cd sofia
claude
```

The built-in guide (Sofia) walks you through instance creation.

> **Alpha** — Sofia relies on the provider's conversational behavior. Results may vary. If the flow doesn't start, [manual mode](doc/guides/getting-started.md) covers the same steps.

---

## Repository structure

| Directory | Content |
|-----------|---------|
| `core/` | Invariants — principles, model, duties |
| `protocol/` | H2A coordination protocol — exchange, friction, contribution |
| `binding/` | Materialization — filesystem implementation, audit, analysis dashboard |
| `provider/` | AI provider layer — Claude Code (others planned) |
| `canvas/` | Starting points — persona archetypes, artifact formats, patterns, workflows |
| `doc/` | Architecture, guides, field feedback, ADRs |

---

## Origin

SOFIA emerged from the Katen project — an orchestration engine for Data & AI pipelines, built with specialized AI personas across hundreds of sessions. The method is the byproduct of real work, not a thought experiment.

A method extracted from practice — to be confronted with yours.

**Site**: [oxynoe.io/sofia](https://oxynoe.io/sofia/)

## License

MIT
