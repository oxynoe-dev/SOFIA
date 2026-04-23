# Provider — AI provider layer

> The provider layer contains everything specific to the AI tool that runs the personas. Replace this layer to port SOFIA to another provider.

Current provider: **Claude Code** (Anthropic).

---

## What this layer contains

| File | Role |
|------|------|
| `sofia.md` | Sofia — the guide persona that creates and audits SOFIA instances |
| `claude-code/` | Claude Code implementation details |

### sofia.md

The guardian persona of the SOFIA method. Not a regular project persona — she is a meta-persona that guides instance creation, persona addition, recalibration, and audit. She operates on the method itself, not on a product.

4 operational modes:
1. **Create** — design a new SOFIA instance (structure, conventions, personas)
2. **Add** — add a persona to an existing instance
3. **Recalibrate** — adjust an existing persona (wear signals, scope drift)
4. **Audit** — structural compliance + friction diagnosis

### claude-code/

Implementation details specific to the Claude Code runtime:

| File | Content |
|------|---------|
| `claude-md.md` | Anatomy of a CLAUDE.md — the 2-line routing file that connects a workspace to its persona and context |
| `sessions.md` | Session summaries — format, workflow, opening/closing protocol |
| `memory.md` | Persistent memory system — types (user, feedback, project, reference), what to store vs not |
| `hooks.md` | Hooks — shell commands triggered by events, useful hooks for SOFIA, when not to use them |

---

## How it connects to the other layers

```
core/       ← principles, model, duties (provider-agnostic)
protocol/   ← H2A, friction, exchange, contribution (provider-agnostic)
binding/    ← filesystem materialization (provider-agnostic)
provider/   ← THIS LAYER (provider-specific)
canvas/     ← templates, patterns (provider-agnostic)
```

The provider layer is the **only layer that changes** when porting SOFIA to another AI tool. Core, protocol, binding, and canvas remain identical.

### The CLAUDE.md pattern

The key provider mechanism is the `CLAUDE.md` file — a 2-line routing file placed at the root of each persona workspace:

```markdown
Whatever the user's first message, before any response, read these two files:
- `../shared/orga/personas/persona-{name}.md`
- `../shared/orga/contextes/contexte-{name}-{product}.md`
```

This pattern is Claude Code-specific. Another provider would use its own injection mechanism (system prompt, config file, API parameter) to load the same persona + context files.

---

## Porting to another provider

To port SOFIA to a different AI tool:

1. Replace the routing mechanism (CLAUDE.md → provider equivalent)
2. Adapt the session workflow (opening/closing/summary)
3. Adapt persistent memory if available
4. Keep everything else unchanged — personas, contexts, conventions, protocol

### Adding a provider

Create a subdirectory `provider/{provider-name}/` with the equivalent of the Claude Code files:

```
provider/
├── claude-code/     ← current provider
├── {new-provider}/  ← your contribution
│   ├── routing.md       ← how to inject persona + context at boot
│   ├── sessions.md      ← session workflow adaptation
│   └── ...
├── sofia.md         ← shared (provider-agnostic guardian persona)
└── README.md
```

`sofia.md` is provider-agnostic — it describes the guide persona's behavior, not its runtime. New providers reuse it as-is.

Contributions welcome — if you port SOFIA to another AI tool (Cursor, Windsurf, Copilot, custom agent, etc.), open a PR with your provider directory.
