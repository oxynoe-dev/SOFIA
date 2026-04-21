---
title: "SOFIA: One Practitioner, Constrained AI Personas, Structured Disagreement"
type: article
target: dev.to
canonical: https://github.com/oxynoe-dev/sofia/blob/main/doc/article-dev-sofia.md
tags: [ai, methodology, opensource, productivity]
status: draft
date: 2026-04-21
author: winston
---

# SOFIA: One Practitioner, Constrained AI Personas, Structured Disagreement

A single LLM says yes. Always. Give it a flawed direction, it executes enthusiastically. The error from step 2 arrives at step 3 as a valid premise. The cascade is silent. The final output looks correct. It is not.

SOFIA is a method that makes AI personas disagree — on purpose.

---

## Friction in action

Real session, real personas. A developer persona (Axel) proposes an ADR to add concurrent execution via Web Workers to the engine. Solid design — Petri nets, worker pool, opt-in mode.

The architect persona (Mira) reviews and recommends **Deferred**:

```
⚡ [contestable] No measured CPU bottleneck justifies the added
  complexity — [mira] → ratified

✓ [sound] Formal test protocol missing (principle D1)
  — [mira] → ratified

✗ [refuted] eval() in workers — non-negotiable security risk
  — [mira] → ratified
```

Nobody is wrong. The dev anticipated a real need — concurrency will matter when the engine handles heavy compositions. The architect protected the roadmap: *make it work, make it right, make it fast — in that order*. We weren't at "fast" yet.

The orchestrator (the human) reads both sides. Decides: deferred. The ADR is preserved, not rejected. The security issue is flagged. The test protocol will be written before implementation. A benchmark will be the trigger to reactivate.

Without the review, the ADR ships too early. The engine cleanup three months later breaks the player. Everything is reworked. With the review, the design waits. When reactivated, it will be better.

That's friction engineering. The tension between two constrained roles produces a decision that neither would have reached alone.

---

## What's in the repo

```
my-project/
├── sofia.md                 ← instance marker
├── shared/
│   ├── conventions.md       ← exchange rules
│   ├── orga/
│   │   ├── personas/        ← persona files (role, stance, prohibitions)
│   │   └── contextes/       ← workspace contexts (scope, key docs)
│   ├── notes/               ← inter-persona exchanges
│   └── review/              ← cross-reviews
├── {workspace-1}/
│   ├── CLAUDE.md            ← provider routing (2 lines)
│   └── sessions/            ← session summaries
└── ...
```

Each persona is a markdown file. It defines a role, a scope, what it challenges — and what it *cannot do*. The constraint is the mechanism: an architect who can't code is forced to challenge on principles. A dev who can't set strategy is forced to justify against the roadmap.

No framework. No dependency. Markdown files and a convention.

---

## The dashboard

The H2A protocol tracks every friction marker across sessions — who contested what, who arbitrated, what was ratified or rejected.

The live dashboard is at [oxynoe.io/sofia/h2a](https://oxynoe.io/sofia/h2a/).

---

## Fork and go

```bash
git clone https://github.com/oxynoe-dev/sofia
```

- [Getting started](https://github.com/oxynoe-dev/sofia/blob/main/doc/guides/getting-started.md) — set up your first instance
- [H2A dashboard](https://oxynoe.io/sofia/h2a/) — live friction data from a real project
- [The long-form article](https://medium.com/@olivier.cds/35037eb1a5cc) — the thesis behind the method

Start with two personas in tension. A single persona generates no friction — SOFIA's value starts at two.
