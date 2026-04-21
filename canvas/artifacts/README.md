# Artifact Formats

> Templates for the artifacts that circulate in a SOFIA instance.

Each artifact has a frontmatter structure and a body structure. These templates define the expected format — adapt the content to your instance.

| Artifact | Purpose | Key fields | File |
|----------|---------|------------|------|
| Persona | Defines a constrained AI role (7 dimensions) | identity, stance, scope, prohibitions | [persona.md](persona.md) |
| Context | Workspace-specific contract for a persona×product | scope, key docs, isolation, workflow | [product-persona-context.md](product-persona-context.md) |
| Session | Structured summary of a session | Produced, Decisions, Shared notes, Open | [session.md](session.md) |
| Note | Message between personas | from, to, nature, status | [note.md](note.md) |
| Review | Persona takes a position on another's work | from, to, subject, friction markers | [review.md](review.md) |
| Feature | Shared functional spec | need, proposal, constraints | [feature.md](feature.md) |
| ADR | Architecture decision record | context, decision, alternatives | [adr.md](adr.md) |
| Roadmap | Product planning with ownership | versions, items, @owner | [product-roadmap.md](product-roadmap.md) |
| Team orga | Team structure, RACI, challenge rights | personas, flows, rules | [team-orga.md](team-orga.md) |
| Instance marker | Identifies a SOFIA deployment | project, version, team | [sofia-instance.md](sofia-instance.md) |

## Frontmatter

Every artifact deposited in `shared/` carries a YAML frontmatter:

```yaml
---
from: persona-name
to: recipient
nature: signal | question | request | response
status: new | read | done
date: YYYY-MM-DD
ref: source-artifact    # when nature = response
---
```

## Lifecycle

`new` → `read` → `done` → moved to `archives/`.
