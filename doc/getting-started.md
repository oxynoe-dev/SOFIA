# Getting started without Sofia — manual mode

> Install personas by hand, file by file.

---

## When to use manual mode

- You want to understand each piece before assembling
- You already have a precise idea of the roles you need
- You prefer to keep control over the structure
- You want to adapt the method to another provider

Manual mode produces exactly the same result as Sofia. There is no "lite" version — just a different path to get there.

---

## Overview

```
my-project/
├── sofia.md                 ← instance marker
├── shared/
│   ├── conventions.md       ← exchange rules
│   ├── orga/
│   │   ├── personas/        ← persona files (role, posture, prohibitions)
│   │   └── contextes/       ← workspace contexts (key docs, scope, workflow)
│   ├── notes/               ← inter-persona exchanges
│   ├── review/              ← cross-reviews
│   └── roadmap-{product}.md ← planning
├── {workspace-1}/
│   ├── CLAUDE.md            ← runtime routing (2 lines)
│   └── sessions/            ← session summaries
├── {workspace-2}/
│   ├── CLAUDE.md
│   └── sessions/
└── ...
```

---

## Before you start: instance and project

A SOFIA instance is not your project — it's the workshop where personas think. The project (code, product) lives in a separate repo. See the [Isolation > Instance and project](user-guide.md#instance-and-project) section of the user guide for details and the three possible configurations.

---

## Step 1 — Clone the SOFIA repo

```bash
git clone https://github.com/oxynoe-dev/sofia
```

This is your reference. Templates and documentation are inside. You don't need to keep it in your project — just consult it.

---

## Step 2 — Create the instance marker

At your project root, create `sofia.md`:

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

Create `shared/conventions.md`. This is the exchange contract between personas. At minimum:

```markdown
# Conventions

## Inter-persona exchanges

Personas don't talk to each other. They exchange through artefacts deposited in shared/.

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

The first persona is a **structuring** role — the one that will frame your approach.

### Create the persona file

Create `shared/orga/personas/persona-{name}.md`. Draw from the format in `canvas/artifacts/persona.md` and archetypes in `canvas/archetypes/`. Essential fields:

```markdown
# {Name} — {Role}

## Profile
{In one sentence: who this persona is and their posture.}

## Scope
- {domain 1}
- {domain 2}

## What they do NOT do
- {prohibition 1}
- {prohibition 2}

## What they challenge
- {friction axis 1}
```

The "What they do NOT do" section is **the most important**. It creates the productive constraint.

### Create the context file

Create `shared/orga/contextes/contexte-{name}-{product}.md`. Draw from the template in `canvas/artifacts/product-persona-context.md`. Essential fields:

```markdown
---
persona: {name}
product: {product}
---

# Context {Name} — {Product} ({workspace})

## Scope
This workspace contains:
- {content type}

## Key documents
| File | Role |
|------|------|
| `{path}` | {description} |

## Isolation
- Never read/write outside `{authorized scope}`

## Conventions
- **Language**: english
- **Reviews**: `review-{subject}-{name}.md` in `shared/review/`

## Workflow
0. Read the latest summary in `sessions/`
1. Read existing documents before any intervention
2. Produce {deliverables}

## Emergence
When you deflect 3+ times on the same domain, signal it.

## Session protocol — mandatory
Summary: `sessions/{YYYY-MM-DD}-{HHmm}-{name}.md`
Sections: Produit, Decisions, Notes deposees, Friction orchestrateur, Ouvert
```

The persona says **who you are**. The context says **where you are**.

---

## Step 5 — Create the workspace

```bash
mkdir -p {workspace}/sessions
```

### The CLAUDE.md

Create `{workspace}/CLAUDE.md`. This is a runtime routing — 2 lines pointing to the persona and context:

```markdown
Whatever the user's first message, at session opening, before any response, read these two files:
- `shared/orga/personas/persona-{name}.md`
- `shared/orga/contextes/contexte-{name}-{product}.md`
```

That's it. Content lives in the persona and context, not in the CLAUDE.md.

See `runtime/claude-code/claude-md.md` for details on the three layers.

---

## Step 6 — First session

Launch Claude Code in the workspace:

```bash
cd {workspace}
claude
```

The persona will read its CLAUDE.md, load the persona and context, and behave according to the contract. Ask it something within its scope. Observe:

- **It refuses what's out of scope?** Good sign.
- **It accepts everything?** Tighten the prohibitions in the persona.
- **It's too rigid?** Soften the posture in the persona.
- **It doesn't know its workspace?** Enrich the context.

Calibration takes 2-3 sessions. That's normal.

---

## Adding a second persona

When the need emerges — not before. The signals:

- The first persona regularly tells you "that's not my role"
- You spend time doing work a persona could structure
- Two distinct domains are in tension

Go back to step 4. Create the persona file, context file, workspace, launch a first session.

---

## Checklist

- [ ] `sofia.md` at root
- [ ] `shared/conventions.md`
- [ ] `shared/orga/personas/persona-{name}.md`
- [ ] `shared/orga/contextes/contexte-{name}-{product}.md`
- [ ] `{workspace}/CLAUDE.md` (2-line routing)
- [ ] `{workspace}/sessions/`
- [ ] First session launched
- [ ] The persona says "no" when it should
