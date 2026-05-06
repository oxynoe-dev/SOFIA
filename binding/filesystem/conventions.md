# Conventions

> Instance conventions. Extend as the project evolves.

## Artifact types

Declare which artifact types this instance uses. The audit checks only declared types.

| Type | Directory | Naming | Extra fields |
|------|-----------|--------|--------------|
| notes | shared/notes/ | `note-{subject}-{author}.md` | |
| reviews | shared/review/ | `review-{subject}-{author}.md` | subject |

<!-- Add rows for additional types used by this instance, e.g.:
| features | shared/features/ | `feature-{name}.md` | |
| adr | shared/adr/ | `adr-{number}-{title}.md` | |
| team-orga | shared/orga/ | `team-orga.md` | |
-->

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

## Repo ownership (optional)

<!-- Uncomment and fill if your instance spans external repos.

| Repo | Path | Owner |
|------|------|-------|
| product-repo | doc/architecture/ | @architect |
| product-repo | (rest) | @dev |

-->

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
ref: source-artifact     # SHOULD when nature = response (filename without extension)
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

## Consultation

A persona in session MAY propose an inter-persona consultation when an expert opinion outside their scope is needed. The orchestrator authorizes; the recipient is spawned as a one-shot sub-agent. See `protocol/exchange.md` §Consultation, `canvas/workflows/consultation.md`.

### When to propose

Trigger only when the orchestrator's arbitration requires expertise **outside their direct field** (e.g., dev → archi, archi → R&D, archi → terrain). Consultations on subjects within the emitter's own field tend to be wasteful.

### Lifecycle

1. **Propose** — emitter persona deposits a consultation note in `shared/notes/` (`nature: question`) and signals the orchestrator. MUST NOT spawn before authorization.
2. **Authorize** — orchestrator authorizes (or declines) verbally.
3. **Spawn** — once authorized, the emitter spawns the recipient sub-agent with minimal context: persona file, context file, consultation note. No emitter session history, no other artifacts.
4. **Reply** — the sub-agent deposits a reply note (`nature: response`, `ref:` to the consultation note) and a short session summary in its own space.
5. **Arbitrate** — orchestrator annotates each friction with its resolution tag directly in the reply note.

### Constraints (prescriptive)

- **Depth 1** — the recipient sub-agent MUST NOT propose another consultation
- **Minimal context** — only persona, context, consultation note (no other artifacts)
- **Web search authorized** — for external reference verification only
- **Continuity line** — the short summary MUST contain a line in `## Open` pointing to the reply note for next-session reading

### Short session summary (spawn variant)

The recipient persona produces a lighter session summary in `{space}/sessions/`:

```
{YYYY-MM-DD}-{HHmm}-{persona}-spawn.md
```

```yaml
---
persona: recipient-persona
date: YYYY-MM-DD
session: "HHmm-spawn"
trigger: consultation-note-id
---
```

The `-spawn` suffix and the `HHmm-spawn` value distinguish a spawn summary from a regular session summary. The `trigger:` field is mandatory and points to the consultation note (filename without extension).

See `canvas/artifacts/session.md` §Spawn variant for the body format.

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

## Roadmaps

Roadmaps live in `shared/` and follow the naming convention `roadmap-{product}.md`.

### Structure

Each roadmap SHOULD have:
- A `# Roadmap {name}` header
- An owner declaration in the blockquote: `> Owner : @persona`
- Version sections (`### vX.Y.Z`) with metadata comments: `<!-- produit: X | cible: YYYY-MM | statut: todo -->`

### Items

Each item is a markdown list entry (`- [status] description @owner`).

- **Status**: `[done]`, `[running]`, `[todo]`, `[blocked]`, `[ready]`
- **Owner**: `@persona` — who is responsible
- **Cross-instance**: `↔` marker for dependencies on other instances

---

## Cross-instance exchanges

When the orchestrator routes an artifact between two instances, the artifact MUST be deposited in `shared/` of the **recipient's** instance — not the emitter's.

The emitting persona does not need to know the recipient's instance. The orchestrator crosses instance boundaries — personas remain isolated.

See `protocol/exchange.md` §Cross-instance exchanges.
