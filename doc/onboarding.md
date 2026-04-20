# Onboarding a new persona

> How to integrate a new persona into an existing SOFIA instance.

---

## When to add a persona?

A persona is justified when:
- A **domain** emerges that nobody covers correctly
- Two existing personas are in **tension** on a recurring subject
- The orchestrator spends time doing work a persona could structure

A persona is **not** justified when:
- It's a task, not a role (use a note or backlog item)
- The domain is covered but "not well enough" (improve the existing persona)

## Steps

### 1. Define the role

Before naming the persona, define:
- **What** — what types of deliverables it produces
- **Not what** — what it explicitly does not do (the most important)
- **With whom** — its main interactions

### 2. Create the persona file

Draw from the format in `canvas/artifacts/persona.md` and archetypes in `canvas/archetypes/`. Key fields:
- Profile, stance, scope
- Collaboration (with/mode table)
- What it does not do

### 3. Create the workspace

```
{instance}/
├── shared/orga/
│   ├── personas/persona-{name}.md       ← persona file (role, stance, prohibitions)
│   └── contextes/contexte-{name}-{product}.md  ← workspace context (docs, isolation, workflow)
└── {workspace}/
    ├── CLAUDE.md      ← runtime routing (2 lines → persona + context)
    └── sessions/      ← empty, the persona will write its first summary
```

The CLAUDE.md is a 2-line routing (see `runtime/claude-code/claude-md.md`). Content lives in two files:
- **persona-{name}.md** — role, stance, prohibitions, collaboration (template: `canvas/artifacts/persona.md`)
- **contexte-{name}-{product}.md** — scope, key documents, isolation, workflow (template: `canvas/artifacts/product-persona-context.md`)

### 4. Brief the persona

At the first session, the persona must:
1. Read its persona file
2. Read key documents in its domain
3. Scan `shared/notes/` for any messages
4. Deposit a first session summary

### 5. Introduce to the rest of the team

Deposit a note in `shared/notes/`:

```
note-team-new-persona-{author}.md
```

Content: who, why, what scope, who it interacts with.
Other personas will discover it at their next session opening.

## Example: onboarding Sofia (Katen, March 2026)

Sofia was onboarded by Nora (UX):
1. Persona file defined with stance "the detail makes the product"
2. `graphisme/` workspace created with specific CLAUDE.md
3. Brief: targeted reading list (design-principles, design-system, feature-v022)
4. First session: visual exploration, reference board v1

The brief was a dedicated document (`onboarding-sofia.md`) — short, ordered,
with references to existing docs rather than duplicated content.

## Anti-patterns

- **The catch-all persona** — "it does a bit of everything". If you can't
  say what it doesn't do, it's not calibrated.
- **The orphan persona** — no interaction with others. An isolated persona
  generates no useful friction.
- **The mirror persona** — it does the same thing as another with a different
  name. Merge rather than duplicate.
