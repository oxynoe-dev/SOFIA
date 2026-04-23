---
title: Setting up manually
---

# Setting up manually

## Overview

```
my-project/
├── sofia.md                 ← instance marker
├── shared/
│   ├── conventions.md       ← exchange rules
│   ├── orga/
│   │   ├── personas/        ← persona files (role, stance, prohibitions)
│   │   └── contextes/       ← workspace contexts (key docs, scope, workflow)
│   ├── notes/               ← inter-persona exchanges
│   └── review/              ← cross-reviews
├── {workspace-1}/
│   ├── CLAUDE.md            ← provider routing (2 lines)
│   └── sessions/            ← session summaries
├── {workspace-2}/
│   ├── CLAUDE.md
│   └── sessions/
└── ...
```

## Step 1 — Clone the SOFIA repo

```bash
git clone https://github.com/oxynoe-dev/sofia
```

This is your reference — templates and documentation. You don't need to keep it in your project.

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

## Step 3 — Create the shared structure

```bash
mkdir -p shared/orga/personas shared/orga/contextes shared/notes shared/review
```

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

**Artifact types**:
- **Note** — a message between personas: a signal, a question, a request. Short, directional (from → to). Example: `note-dev-design-tokens-architect.md`
- **Review** — a persona takes a position on another's work. Carries friction markers. Example: `review-api-spec-v2-dev.md`
- **Feature** — a shared functional spec. Not directional. Example: `feature-export-pipeline.md`

Each artifact carries a YAML frontmatter (`from`, `to`, `nature`, `status`, `date`). When processed, it migrates to `archives/`.

## Step 4 — Define your first persona

Start with **one**. Others will come.

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

The "What they do NOT do" section is **the most important**. It creates the productive constraint.

Then create `shared/orga/contextes/contexte-{name}-{product}.md` — the workspace-specific contract:

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

## Step 5 — Create the workspace

```bash
mkdir -p {workspace}/sessions
```

Create `{workspace}/CLAUDE.md` — a 2-line provider routing:

```markdown
Whatever the user's first message, at session opening, before any response, read these two files:
- `shared/orga/personas/persona-{name}.md`
- `shared/orga/contextes/contexte-{name}-{product}.md`
```

That's it. Content lives in the persona and context, not in the CLAUDE.md.

## Step 6 — First session

```bash
cd {workspace}
claude
> hello
```

The persona reads its CLAUDE.md, loads the persona and context, reads the latest session summary, and is ready to work. Give it a real task — not a test.

**Calibration signals**:
- **It refuses what's out of scope?** Good — the prohibitions work.
- **It accepts everything?** Tighten the prohibitions.
- **It's too rigid?** Soften the stance.
- **It doesn't know its workspace?** Enrich the context.

Calibration takes 2-3 sessions. That's normal.

## Session closing

When you're done, give the signal ("let's close"). The persona produces a summary:

```
sessions/2026-04-21-1430-architect.md
```

Mandatory sections: `## Produced`, `## Decisions`, `## Shared notes`, `## Open`. No prose — short lists, 30 lines max.

Commit (if using git):
```
architect: first session — scope definition + ADR-001 (2026-04-21)
```

## Adding a second persona

When the need emerges — not before. SOFIA's value starts at 2 personas — a single persona generates no friction.

**Signals**:
- **Repeated deflection** — the first persona tells you "that's not my role" 3+ times on the same domain.
- **Quality gap** — the persona produces something adequate but shallow. A dedicated role would do better.
- **Two domains in tension** — you spend time arbitrating between concerns that belong to different axes.

Go back to step 4. The new persona must be **in tension** with the existing one.

**Example: onboarding Sofia (Katen, March 2026)**

Sofia (visual production) was onboarded by Nora (UX):
1. Persona file defined with stance "the detail makes the product"
2. Workspace `graphisme/` created with specific CLAUDE.md
3. Brief: targeted reading list (design-principles, design-system, feature-v022)
4. First session: visual exploration, reference board v1

The entire process took one session.

For the full derivation process, see [Derivation grammar](../concepts/derivation-grammar.md).

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
