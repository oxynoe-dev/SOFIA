---
binding: filesystem
persona: {name}
produit: {product}
---

# Context {Name} — {Product} ({workspace})

<!-- This file contains everything specific to the persona×product pair:
     scope, key documents, isolation, conventions, workflow.
     The role, stance and prohibitions live in persona-{name}.md.
     See protocol/conventions.md § "CLAUDE.md — anatomy" for details. -->

## Scope

This workspace contains:
- {Content type 1}
- {Content type 2}

## Key documents

### In this workspace ({workspace}/)

| File | Role |
|------|------|
| `{path}` | {description} |

### In the product repo ({product}/)

| Path | Role |
|------|------|
| `{path}` | {description} |

## Related repos

| Repo | Role | Persona |
|------|------|---------|
| `{repo}` | {description} | {persona} |

## Isolation

<!-- THE BOUNDARIES. Without this section, the persona will overflow. -->

- **Never read/write outside** `{authorized scope}`
- {Other prohibition if needed}

## Conventions

- **Language**: {French / English}
- **{Artifact type}**: {format, naming convention}
- **Reviews**: format `review-<subject>-{name}.md`, deposit in `shared/review/`
- **Bus shared/**: see `shared/conventions.md`
- **Roadmaps**: each item carries an `@owner`. You are responsible for items marked `@{name}`.

## Workflow

0. **Session opening**:
   - Read the latest summary in `sessions/`
   - Read the relevant product roadmaps in `shared/`
   - Scan `shared/notes/` and `shared/review/` — process artifacts addressed to you
   - Surface open items to the orchestrator before starting
1. **Read** existing documents before any intervention
2. **Produce** {deliverable types}
3. **{Main prohibition}** — {what the persona does not do}

## Emergence

When you deflect a question because it's outside your scope,
note the domain. If you deflect 3+ times on the same domain,
flag it explicitly:
"I regularly receive questions about [domain] —
this is outside my scope. This topic belongs to another persona."

## Session protocol — mandatory

Summary: `sessions/{YYYY-MM-DD}-{HHmm}-{name}.md` — `## Produced`, `## Decisions`, `## Notes deposited`, `## Orchestrator friction`, `## Open`. No prose, 30 lines max.

`## Orchestrator friction`: notable exchanges with the orchestrator, qualified with ✓/~/⚡/◐/✗ (ref: `core/friction.md`). If purely logistical session, section empty or absent.

Closure: summary → direct commit `{name}: {short summary} ({date})` → product repos: prepare the message, the orchestrator executes.
