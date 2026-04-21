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

A small SOFIA instance with two personas working on the same project. By the end, you'll have:

- An instance structure (sofia.md, shared/, two workspaces)
- Two personas with constrained roles, in tension with each other
- A first session producing a structured summary
- An artifact exchanged between the two personas

---

## Prerequisites

- A git repository for your project
- An AI provider that supports system instructions (Claude Code, or manual mode with any LLM)
- A clear project — SOFIA amplifies what you bring, it doesn't replace domain expertise

---

## Two paths

### Path A — With Sofia (guided)

```bash
git clone https://github.com/oxynoe-dev/sofia
cd sofia
claude
```

Sofia guides you through instance creation:
1. She asks about your project — domain, objectives, current challenges
2. She proposes personas in tension (minimum 2)
3. You calibrate together — adjust scope, prohibitions, stance
4. She generates the files — persona sheets, contexts, CLAUDE.md, conventions
5. You start working

> If the flow doesn't start or drifts, switch to Path B.

### Path B — Manual (step by step)

Follow the [Getting started guide](../guides/getting-started.md). You create each file by hand — slower, but you understand every piece.

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
