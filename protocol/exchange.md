# Exchange

> Sessions and artifacts — everything goes through the orchestrator.

---

## Principle

Every exchange between the orchestrator and a persona is either a **session** (synchronous) or an **artifact** (asynchronous deposit). Personas never communicate directly — the orchestrator is the sole router.

Source principle: `core/principles.md` — the orchestrator arbitrates all decisions; `core/model.md` — exchange is a constitutive entity.

## Common dimensions

Every exchange (session or artifact) carries:

| Dimension | Values | Required |
|-----------|--------|----------|
| **instance** | Reference to the instance | MUST |
| **space** | Space of the concerned persona | MUST |
| **datetime** | Date and time of the exchange | MUST |

The session / artifact distinction is structural — a session is synchronous, an artifact is an asynchronous deposit.

Every exchange generates 0..* frictions (see `friction.md`) and 0..* contributions (see `contribution.md`).

---

## Sessions

### Principle

A session is the primary mechanism for human-assistant interaction. The orchestrator initiates, the persona produces, the orchestrator closes.

### Definition

A session is a synchronous exchange between the orchestrator and one persona.

### Specific dimensions

| Dimension | Values | Required |
|-----------|--------|----------|
| **persona** | Persona identifier | MUST |
| **identifier** | Unique | MUST |

### Lifecycle

1. **Opening** — the orchestrator initiates the session. The persona MUST consult the latest session trace in its space before any intervention.
2. **Exchange** — free dialogue. The orchestrator brings context, directives, artifacts from other personas. The persona produces within its scope.
3. **Closing** — the persona MUST produce a structured summary before closure.

### Session summary

Each session MUST produce an identifiable trace carrying the dimensions above.

#### Protocol sections (MUST)

Protocol layer — deterministic and verifiable content.

| Section | Content |
|---------|---------|
| Produced | List of artifacts created or modified |
| Decisions | Choices made during the session |
| Shared notes | Artifacts deposited in the shared space |
| Open | Unresolved questions, pending items |

Each section MUST be present. If nothing to report: "None".

Constraints:
- No prose — short lists only.
- 30 lines max for the entire summary.

#### Observational sections (SHOULD / MAY)

Observational layer — inferential content, subject to human validation.

| Section | Content | Status |
|---------|---------|--------|
| Orchestrator friction | Qualified frictions with resolution tag (see `friction.md`) | SHOULD |
| Flow | Epistemic contributions (see `contribution.md`) | MAY |

The persona pre-fills these sections. The orchestrator MAY correct, complete, or remove content.

### Reviewing exchange rules

The persona MUST reread the instance's exchange rules before:
- any artifact production (note, review, feature)
- any session closure (summary)

This rereading ensures that friction markers, resolution tags, frontmatter, and naming are compliant. Without rereading, the persona drifts — especially in long sessions where initial context fades. The rereading mechanism (conventions file, hook, runtime injection) is an implementation choice.

### Traceability

Each session MUST produce an identifiable trace. The persistence mechanism is defined in `binding/implementation.md`.

---

## Artifacts

### Principle

Personas never communicate directly. All inter-persona exchanges transit through the orchestrator via the shared space.

### Definition

An artifact is an asynchronous deposit in the shared space by a persona, intended for another persona or the team.

### Specific dimensions

| Dimension | Values | Required |
|-----------|--------|----------|
| **from** | Persona depositing the artifact | MUST |
| **to** | Persona or `team` | MUST |
| **nature** | `signal`, `question`, `request`, `response` | MUST |
| **status** | `new` → `read` → `done` | MUST |
| **ref** | Identifier of the artifact this one responds to | SHOULD (when nature = `response`) |

> **FR retrocompat.** The parser also accepts FR fields and values: `de`/`pour`/`statut` (fields), `nouveau`/`lu`/`traite` (statuses), `ratifie`/`conteste`/`revise`/`rejete` (resolutions).

The `nature` field MUST use one of the 4 types above. The `status` field MUST follow the indicated lifecycle.

### Artifact resolution

The resolution MUST live in the artifact that carries the friction — not in a separate artifact (return note, response). The orchestrator annotates each friction point with its resolution tag (`→ ratified`, `→ contested`, `→ revised`, `→ rejected`) directly in the source file, then sets status to `done`.

This rule ensures that a friction line carries the complete cycle (marker + initiative + resolution) in a single file. The parser does not need to join multiple artifacts to reconstruct the cycle.

A return note (response to a review) MAY accompany the resolution to communicate decision context, but it MUST NOT carry friction markers or resolution tags — otherwise the parser would count duplicates. When an artifact responds to another, it SHOULD carry a `ref` dimension pointing to the original artifact identifier, creating an explicit lineage between artifacts.

### Friction in artifacts

An artifact MAY carry friction markers (see `friction.md`). This is typical of reviews and notes that take a position on another persona's work.

Markers follow the same format as in sessions: marker, description, initiative tag. The artifact emitter is the friction emitter.

### Contribution in artifacts

An artifact MAY carry contributions (see `contribution.md`). This is typical of reviews and notes involving input from both parties: the orchestrator brings source material (`[H]`), the persona brings analysis (`[A]`). The `[H]`/`[A]` direction applies as in sessions — the artifact is produced during a session.

### send() and receive()

Artifact exchange is a two-step process:

**send()** — the persona produces and deposits the artifact:
1. The orchestrator instructs Persona A to produce an artifact for Persona B
2. Persona A produces the artifact and deposits it in the recipient's `shared/` (`status: new`)

**receive()** — the orchestrator presents the artifact to the recipient:
3. The orchestrator opens a session with Persona B and presents the artifact (`status: read`)
4. Persona B processes and MAY deposit a response (`nature: response`, `ref:` to the source artifact)
5. The original artifact moves to `status: done`

The orchestrator MUST be the router of all exchanges. A persona MUST NOT directly consult an artifact not intended for them.

### Cross-instance exchanges

When the orchestrator routes an artifact between two instances, send() deposits the artifact in the shared space of the recipient's instance — not the emitter's.

1. The orchestrator instructs Persona A (instance X) to produce an artifact for Persona B (instance Y)
2. Persona A produces the artifact during its session — send() deposits in `shared/` of instance Y (`status: new`)
3. The orchestrator opens a session with Persona B (instance Y) — receive() presents the artifact
4. The lifecycle (resolution, archiving) follows instance Y's rules

The emitting persona does not need to know the recipient's instance. The orchestrator crosses instance boundaries — personas remain isolated.

### Archiving

When an artifact moves to `status: done`, it SHOULD be archived. The archiving mechanism is defined in `binding/implementation.md`.
