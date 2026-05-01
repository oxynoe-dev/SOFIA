# Implementation

> How H2A is implemented today — and how it could be implemented tomorrow.

---

## Principle

H2A defines the semantics of interactions (entities, invariants, protocol/observational layers). This document describes the current implementation. A different implementation would be H2A-conformant as long as it respects the semantics defined in `h2a.md`, `friction.md`, `contribution.md`, and `exchange.md`.

## Current implementation

### Stack

| Component | Choice | Role |
|-----------|--------|------|
| Artifact format | Markdown + YAML frontmatter | Human-readable and audit-readable, no software dependency |
| Persistence | git | Immutable history, diff, blame — trace per session |
| Space structure | Filesystem directories | One directory = one space. Natural isolation |
| Shared space | `shared/` at instance root | Sole channel between personas |
| Instance marker | `sofia.md` file at root | Identifies a SOFIA deployment and its version |
| AI provider | Claude Code | CLAUDE.md as persona instruction, hooks, project memory |

### Traceability conventions

**Commits** (recommended):
```
{persona}: {short summary} ({date})
```
One commit per session.

**Session summaries**:
```
{space}/sessions/{YYYY-MM-DD}-{HHmm}-{persona}.md
```
At each closure, the persona creates a **new** file. The `HHmm` is the closure time (not the boot time). A long session with multiple closures produces multiple files.

### Instance structure

Scaffolding is **minimal** — only elements necessary for the protocol are created at initialization. The internal organization of `shared/` (subdirectories, artifact naming conventions, archiving) is an instance convention, not standard implementation.

```
instance/                        ← scaffolding (create-instance)
├── sofia.md                     ← instance marker
├── shared/                      ← shared space (exchange bus)
│   ├── conventions.md           ← instance-specific conventions
│   └── orga/                    ← team organization
│       ├── personas/            ← persona files
│       └── contextes/           ← contexts per persona-product
├── {space}/                     ← one per persona
│   ├── CLAUDE.md                ← persona instructions (provider)
│   └── sessions/                ← session summaries
└── ...
```

The protocol requires `shared/` as the sole channel and artifacts with frontmatter. How the instance organizes its artifacts in `shared/` (subdirectories, naming, archiving) is a local decision documented in `conventions.md`.

### Repo ownership (MAY)

When an instance spans multiple repositories, `conventions.md` MAY declare a `## Repo ownership` section mapping external repo paths to persona owners.

```markdown
## Repo ownership

| Repo | Path | Owner |
|------|------|-------|
| product-repo | doc/architecture/ | @architect |
| product-repo | (rest) | @dev |
```

This is useful when personas from the same instance work in different parts of the same external repo. The workspace field in persona files covers the instance-internal space; repo ownership covers external repos.

### Installing the protocol on a persona

The H2A protocol is installed via the **context** (`shared/orga/contextes/contexte-{persona}-{product}.md`), not via the persona file. The persona file defines the role (instance-agnostic). The context installs the instance rules.

Each context MUST contain an `## H2A Protocol` section that:
- Points to `shared/conventions.md` (read at first boot, reread before each artifact and closure)
- Recalls the mandatory session summary sections (Produced, Decisions, Shared notes, Open)
- Recalls the observational sections (Orchestrator friction SHOULD, Flow MAY)
- Recalls the commit convention
- Contains the **inline friction template** — the exact expected format, directly visible in the context

Without this section, the persona will not trace friction — this is the most common prescription/usage gap.

**Inline friction template** (to include in each context):

```
Friction format: {symbol} [{marker}] {description} — [{initiative}] → {resolution}
Markers: ✓ [sound], ~ [contestable], ⚡ [simplification], ◐ [blind_spot], ✗ [refuted]
Initiative: [persona] or [PO]
Resolution (SHOULD): → ratified, → contested, → revised, → rejected
Lineage: if amending a prior friction, add (ref: {source-id}/{index})
```

The template is a safety net — the persona has the format in view when producing, without rereading an external file.

### Frontmatter

Every artifact deposited in the shared space carries a YAML frontmatter. No accents in values.

**Artifacts**:
```yaml
---
from: persona-emitter
to: persona-recipient
nature: signal           # signal | question | request | response
status: new              # new | read | done
date: YYYY-MM-DD
ref: artifact-identifier # SHOULD when nature = response
---
```

The `ref` field links a response to its source artifact. The identifier is the filename without extension (e.g., `note-aurele-localisation-doc-site-livia`). For cross-instance artifacts, the `instance-source` field indicates the originating instance.

**Sessions**:
```yaml
---
persona: persona-name
date: YYYY-MM-DD
session: "HHmm"
---
```

### Archiving

When an artifact moves to `status: done`, it is moved to `archives/` in the parent directory.

### Status lifecycle

| Status | Meaning |
|--------|---------|
| `new` | Deposited, not yet read by the recipient |
| `read` | Read by the recipient |
| `done` | The recipient has acted on it |

> **Retrocompat**: the parser also accepts FR values (`nouveau`, `lu`, `traite`).

### Artifact resolution

When an artifact is processed, each point SHOULD carry a resolution tag in the document body (not in the frontmatter — an artifact often contains multiple points).

Convention: the recipient annotates each point with `→ ratified`, `→ contested`, `→ revised`, or `→ rejected` before archiving.

**Example**:
```markdown
## Proposition A
→ ratified

## Proposition B
→ rejected (short justification)

## Proposition C
→ revised (detail on what changes)
```

> **Retrocompat**: the parser also accepts FR tags (`ratifie`, `conteste`, `revise`, `rejete`).

### Friction in session summaries

Section `## Orchestrator friction` (SHOULD — see `exchange.md` §Sessions, observational layer).

Each line carries the dimensions defined in `friction.md`, rendered as:

```
## Orchestrator friction
- [marker] description — [initiative] → resolution
```

**Markers**: rendered as bracketed keywords + visual symbol in instance conventions.

| Protocol (`friction.md`) | Markdown rendering |
|--------------------------|-------------------|
| `[sound]` | ✓ or `[sound]` |
| `[contestable]` | ~ or `[contestable]` |
| `[simplification]` | ⚡ or `[simplification]` |
| `[blind_spot]` | ◐ or `[blind_spot]` |
| `[refuted]` | ✗ or `[refuted]` |

> **Retrocompat**: the parser also accepts FR brackets (`[juste]`, `[angle-mort]`, `[faux]`).

Visual symbols (✓/~/⚡/◐/✗) are an instance convenience. Bracketed keywords are authoritative for audit.

**Initiative**: `[persona]` or `[PO]` — who initiated the friction subject.

**Resolution**: epistemic gesture tag after the arrow `→`. See `protocol/friction.md` §Resolution.

| Protocol (`friction.md`) | Markdown rendering |
|--------------------------|-------------------|
| `ratified` | `→ ratified` |
| `contested` | `→ contested` |
| `revised` | `→ revised` |
| `rejected` | `→ rejected` |

The resolution tag is set per friction point, not per section.

**Example**:
```
## Orchestrator friction
- ✓ [sound] the Toulmin mapping illuminates without constraining — [PO] → ratified
- ~ [contestable] the Toulmin mapping is suggestive, not established — [PO] → revised
- ◐ [blind_spot] scaffolding absent from the Böckeler review — [aurele] → ratified
```

### Lineage (`antecedent` dimension)

When a friction amends a prior friction (see `protocol/friction.md` §Lineage), the `antecedent` dimension is materialized by a `ref:` field at the end of the line:

```
- ✓ [sound] the protocol/observational distinction covers the case — [aurele] → ratified (ref: 2026-04-10-1430-aurele/3)
```

**Format**: `ref: {source-id}/{index}` where:
- `{source-id}` = filename (without extension) — session summary or artifact
- `{index}` = friction position in the source file (1-based, order of appearance)

**Implementation rules**:
- The parser MUST follow `ref:` links and propagate the resolution from the last link to the source friction.
- A friction referenced by a `ref:` does not appear in the open frictions list if the referencing link carries a resolution.
- Counters count the logical friction once, with the original marker and the final resolution.

The `exchange` and `emitter` dimensions are implicit: the exchange is the current session, the emitter is the persona authoring the summary.

### reportPattern in session summaries

Section `## reportPattern` (MAY — observational layer for the observation, protocol layer for the counter).

The persona records the trigger and the orchestrator's choice:

```
## reportPattern
- Theme: [theme] — N rejected frictions (sessions YYYY-MM-DD, ...)
- Choice: LLM error | conviction | resistance
- Justification: ...
```

The audit counts triggers and the distribution of choices (protocol counter).

### Contribution in session summaries

Section `## Flow` (MAY — see `exchange.md` §Sessions, observational layer).

Each line carries the dimensions defined in `contribution.md`, rendered as:

```
## Flow
- {direction}:{type} — description
```

**Direction**: `H` (human brings) or `A` (assistant brings).
**Type**: `substance`, `structure`, `contestation`, `decision`.

**Counting** (optional): a summary line at the end of the section.

**Example**:
```
## Flow
- H:substance — Böckeler article, request for opinion
- A:substance — scaffolding lineage absent from Böckeler
- A:structure — three levels of harness/SOFIA complementarity
- H:decision — keep keyword notation

H:2 (substance 1, decision 1) | A:2 (substance 1, structure 1)
```

The `session` dimension is implicit: it is the current session.

### Operations — filesystem implementation

Mapping of H2A operations (see `protocol/h2a.md`) to the current implementation.

| Operation | Mode | Concrete gesture |
|-----------|------|-----------------|
| openSession() | manual | The orchestrator launches a terminal in the persona's workspace (or resumes an existing Claude Code session) |
| closeSession() | manual | The orchestrator gives the signal. The persona **rereads `shared/conventions.md`**, then produces the summary, prepares the commit. The orchestrator executes the commit |
| send() | manual | The orchestrator instructs the persona. The persona **rereads `shared/conventions.md`**, then produces the artifact (note, review, feature) and deposits in the recipient's `shared/`. **Cross-instance**: the artifact goes to the recipient instance's `shared/`, not the emitter's |
| receive() | manual | The orchestrator opens a session with the recipient and presents the artifact. The recipient reads, processes, and MAY produce a response (with `ref:` to the source artifact) |
| markRead() | manual | The orchestrator sets `status: read` in the artifact's frontmatter |
| markDone() | manual | The orchestrator sets `status: done` in the frontmatter — the artifact is then moved to `archives/` |
| qualifyFriction() | automatic | The persona pre-fills the `## Orchestrator friction` section at closure. The orchestrator validates or corrects |
| qualifyContribution() | automatic | The persona pre-fills the `## Flow` section at closure. The orchestrator validates or corrects |
| reportPattern() | automatic | The persona detects a thematic convergence of rejections during the session. It challenges the orchestrator with the observation + 3 argued hypotheses. The orchestrator responds with their choice + justification. At closure, the persona records in a `## reportPattern` section of the summary |

**Manual** = the orchestrator triggers with an explicit gesture.
**Automatic** = the persona produces at session closure, the orchestrator validates.

The persona MUST NOT close on its own or deposit an artifact without orchestrator instruction.

### Tooling

| Tool | Role |
|------|------|
| `binding/filesystem/analysis.py --only probe` | Verifies instance protocol conformity |
| `binding/filesystem/create-instance.py` | Scaffolds a new instance |
| `sofia.md` | Meta persona — instantiates, audits. Protocol operator |

---

## What is implementation vs protocol

| Element | Protocol (h2a.md) | Implementation (this doc) |
|---------|-------------------|--------------------------|
| "Each session produces a trace" | ✓ | |
| "The trace is a .md file committed in git" | | ✓ |
| "The markers are [sound] [contestable] etc." | ✓ | |
| "The markers are in a Markdown file" | | ✓ |
| "The shared space is the sole channel" | ✓ | |
| "The shared space is a shared/ directory" | | ✓ |
| "The instance is identifiable" | ✓ | |
| "The instance is identified by a sofia.md file" | | ✓ |
| "Friction carries 5 dimensions" | ✓ | |
| "Friction is a Markdown line with symbol + keyword + initiative" | | ✓ |
| "Contribution carries direction and type" | ✓ | |
| "Contribution is a `{H\|A}:{type} — description` line" | | ✓ |
| "Friction carries a resolution tag" | ✓ | |
| "The resolution tag is rendered `→ ratified` at end of Markdown line" | | ✓ |
| "A resolution can evolve between sessions with ref:" | ✓ | |
| "The ref: is rendered `(ref: session-id/n)` at end of Markdown line" | | ✓ |
| "reportPattern() produces an observation + 3 hypotheses + qualification" | ✓ | |
| "reportPattern is a `## reportPattern` section in the summary" | | ✓ |
| "The reportPattern choice counter is auditable" | ✓ | |

---

## Perspectives

### HTTP API

H2A could be implemented as a REST API:
- Each entity (Instance, Space, Persona, Exchange, Friction, Contribution) becomes a resource
- YAML frontmatter becomes JSON schemas
- Statuses (`new` → `read` → `done`) become state transitions
- Audit becomes a verification endpoint

### Database

Session summaries, artifacts, and friction markers could live in a relational or document database. Git history would be replaced by an event log.

### MCP / A2A interoperability

H2A covers the human-assistant layer. MCP and A2A cover the agent-tools and agent-agent layers. A complete system could combine all three:
- H2A for human-assistant coordination
- MCP for resource access by assistants
- A2A for inter-assistant coordination (if the human routing invariant is relaxed)

### Wire format

If H2A evolves toward a technical protocol, a wire format (JSON, protobuf, etc.) and an interoperability spec will be needed. This is not in the current scope.
