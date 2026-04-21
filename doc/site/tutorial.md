---
from: aurele
to: nora, alma
nature: content
date: 2026-04-21
subject: Tutorial page — step-by-step introduction to SOFIA
---

# Tutorial — Your first SOFIA instance

> From zero to a working instance with two personas in friction.

---

## What you'll build

A small SOFIA instance with two personas working on the same project. Here's what the result looks like:

```
my-project/
├── sofia.md                          ← instance marker (name, version, team)
├── shared/
│   ├── conventions.md                ← exchange rules (frontmatter, naming, friction markers)
│   └── orga/
│       ├── personas/
│       │   ├── persona-architect.md  ← role: specs, ADRs, structure — does NOT code
│       │   └── persona-dev.md        ← role: code, tests, implementation — does NOT decide architecture
│       └── contextes/
│           ├── contexte-architect-myproject.md
│           └── contexte-dev-myproject.md
├── architecture/
│   ├── CLAUDE.md                     ← routes to persona + context
│   └── sessions/
│       └── 2026-04-21-1-architect.md ← first session summary
└── dev/
    ├── CLAUDE.md
    └── sessions/
        └── 2026-04-21-1-dev.md
```

By the end, you'll have:
- Two personas with constrained roles, in tension with each other
- A first session producing a structured summary
- An artifact exchanged between the two personas

---

## Prerequisites

- A git repository for your project
- An AI provider that supports system instructions (Claude Code, or manual mode with any LLM)
- A clear project — SOFIA amplifies what you bring, it doesn't replace domain expertise

---

## Setting up the instance

Follow the [Getting started guide](../guides/getting-started.md) to create each file by hand. You'll understand every piece — what it does, why it's there.

> **Sofia (the built-in guide)** can automate this setup, but we recommend manual mode for your first instance. Understanding the structure is more valuable than speed.

---

## The key moment — first friction

Your instance is set up. Two personas, two workspaces. Now what?

1. **Open a session with Persona A** — give them a real task (not a test — real work)
2. **Get a deliverable** — a spec, a note, a review
3. **Close the session** — the persona produces a structured summary
4. **Open a session with Persona B** — present Persona A's deliverable
5. **Watch what happens** — Persona B, with different constraints and prohibitions, sees what Persona A missed

That moment — when Persona B pushes back on something Persona A validated — is SOFIA working. Not because the AI is smarter, but because the structure forces a different angle.

---

## What to expect

**First sessions**: calibration. The personas are too broad, too compliant, or too rigid. This is normal — calibration takes 2-3 sessions per persona. Adjust prohibitions, tighten scope, sharpen stance.

**After calibration**: friction. The personas start saying "no", deflecting questions outside their scope, challenging each other's work. The orchestrator's job shifts from generating content to arbitrating disagreements.

**The trap to avoid**: approving without reading. When you rubber-stamp a session summary, you've stopped orchestrating. That's the moment to slow down.

---

## Next steps

- [User guide](../guides/user-guide.md) — the full picture
- [Operator guide](../guides/operator-guide.md) — H2A operations in detail
- [Glossary](../reference/lexique.md) — SOFIA terms defined
- [Canvas](../../canvas/) — persona archetypes, artifact formats, patterns to draw from
