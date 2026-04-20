# Conventions

> Instance conventions. Extend as the project evolves.

---

## Structure

> Maintain as you go. When a new directory appears in `shared/` (notes/, review/, etc.), add it here so personas know where to look and where to deposit.

```
instance/
├── sofia.md
├── shared/
│   ├── conventions.md
│   └── orga/
│       ├── personas/
│       └── contextes/
├── {space}/
│   ├── CLAUDE.md
│   └── sessions/
└── ...
```

---

## Sessions

### Session summary

At each closure, the persona creates a file in `{space}/sessions/`:

```
{YYYY-MM-DD}-{HHmm}-{persona}.md
```

`HHmm` is the closure time (not the boot time).

### Session frontmatter

```yaml
---
persona: persona-name
date: YYYY-MM-DD
session: "HHmm"
---
```

### Protocol sections (MUST)

| Section | Content |
|---------|---------|
| `## Produced` | Files created or modified |
| `## Decisions` | Choices made |
| `## Shared notes` | Artifacts deposited in shared/ |
| `## Open` | Unresolved questions |

No prose — short lists. 30 lines max.

### Observational sections

| Section | Status | Content |
|---------|--------|---------|
| `## Orchestrator friction` | SHOULD | Qualified frictions |
| `## Flow` | MAY | Epistemic contributions |

## Commits

```
{persona}: {short summary} ({date})
```

One commit per session.

---

## Artifacts

Every artifact deposited in `shared/` carries a YAML frontmatter.

```yaml
---
from: emitting-persona
to: recipient-persona
nature: signal           # signal | question | request | response
status: new              # new | read | done
date: YYYY-MM-DD
---
```

### Lifecycle

| Status | Meaning |
|--------|---------|
| `new` | Deposited, not yet read by recipient |
| `read` | Read by recipient |
| `done` | Processed by recipient |

### Resolution

When an artifact is processed, each point SHOULD carry a resolution tag in the document body:

`→ ratified` | `→ contested` | `→ revised` | `→ rejected`

---

## Friction

Each line carries: marker + description + initiative + resolution.

```
- [marker] description — [initiative] → resolution
```

### Markers

5 epistemic positions. Closed set — do not add new ones.

| Symbol | Marker | Meaning |
|--------|--------|---------|
| ✓ | `[sound]` | Corroboration — position is correct |
| ~ | `[contestable]` | Underdetermination — defensible but not the only reading |
| ⚡ | `[simplification]` | Reductionism — reality is more complex |
| ◐ | `[blind_spot]` | Incompleteness — missing data |
| ✗ | `[refuted]` | Refutation — factually incorrect or incoherent |

Bracketed keywords are authoritative for the audit.

### Initiative

`[persona]` or `[PO]` — who initiated the friction topic.

### Resolution

| Tag | Meaning |
|-----|---------|
| `ratified` | Agreement — the position is accepted |
| `contested` | Disagreement maintained — no change of position |
| `revised` | Disagreement with change of position |
| `rejected` | Terminal disagreement — the position is discarded |

One tag per friction point.

### Cross-session mutability

A resolution may evolve in a later session. The friction SHOULD carry a `ref:` field pointing to the original friction:

```
- ✓ [sound] description — [persona] → ratified (ref: 2026-04-10-1430-persona/3)
```

### Quick reading

- Only ✓ → absent friction — alert signal
- Mix ✓/~/⚡ → healthy friction
- Presence of ◐ or ✗ → tension to address
- No resolution → unresolved frictions, to address or report in Open

---

## Contribution (epistemic flow)

Section `## Flow` — optional.

```
- {direction}:{type} — description
```

| Direction | Meaning |
|-----------|---------|
| `H` | The human (orchestrator) contributes |
| `A` | The assistant (persona) contributes |

| Type | Definition |
|------|-----------|
| `substance` | New information |
| `structure` | Formatting, categorization, synthesis |
| `contestation` | Challenge, counter-example |
| `decision` | Arbitration, choice made |

Optional counting at end of section.

---

## Cross-instance exchanges

When the orchestrator routes an artifact between two instances, the artifact MUST be deposited in `shared/` of the **recipient's** instance — not the emitter's.

The emitting persona does not need to know the recipient's instance. The orchestrator crosses instance boundaries — personas remain isolated.

See `protocol/exchange.md` §Cross-instance exchanges.
