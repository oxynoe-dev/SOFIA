# Audit rules — binding/filesystem

> Reference for all checks performed by `audit-instance.py`.

---

## Levels

| Level | Meaning |
|-------|---------|
| **protocol** | Required by the H2A protocol (`protocol/exchange.md`, `protocol/friction.md`). Every conformant instance MUST pass these. |
| **instance** | Convention adopted by this instance. Declared in `shared/conventions.md`. The audit checks them only if the instance uses the corresponding artifact type. |

## Severity

| Severity | Meaning |
|----------|---------|
| `fail` | Blocks conformity — the instance is not valid |
| `warn` | Should be fixed — degraded quality |
| `info` | Informational — no action required |

---

## Structure checks (S)

| ID | Rule | Severity | Level | Source |
|----|------|----------|-------|--------|
| S1 | `sofia.md` (or `voix.md`) present at root | fail | protocol | `protocol/exchange.md` — instance marker |
| S2 | `shared/` directory present | fail | protocol | `protocol/exchange.md` — shared space |
| S3 | `shared/conventions.md` present | warn | protocol | `protocol/exchange.md` — exchange rules |
| S4 | `shared/notes/` present with `archives/` | info | instance | Emerges on usage — absent is normal |
| S5 | `shared/review/` present with `archives/` | info | instance | Emerges on usage — absent is normal |
| S6 | `shared/features/` present | info | instance | Emerges on usage — absent is normal |
| S7 | `shared/orga/` present | info | instance | Organization files |
| S8 | At least 1 workspace with `CLAUDE.md` | fail | protocol | `protocol/exchange.md` — persona space |
| S9 | Each workspace has `sessions/` | warn | protocol | `protocol/exchange.md` — session traces |
| S10 | Roadmaps in `shared/` | info | instance | Convention `roadmap-{product}.md` |

## Frontmatter checks (F)

| ID | Rule | Severity | Level | Source |
|----|------|----------|-------|--------|
| F1 | Notes have frontmatter | warn | protocol | `protocol/exchange.md` §Artifacts — frontmatter MUST |
| F2 | Reviews have frontmatter | warn | protocol | `protocol/exchange.md` §Artifacts — frontmatter MUST |
| F3 | Notes have required fields (`from`, `to`, `nature`, `status`, `date`) | warn | protocol | `protocol/exchange.md` §Specific dimensions |
| F4 | Reviews have required fields (`from`, `to`, `nature`, `status`, `date`, `subject`) | warn | protocol | `protocol/exchange.md` §Specific dimensions |
| F5 | No accents in frontmatter values | info | instance | Convention — ASCII identifiers for parsability |
| F6 | Status values are valid (`new`/`read`/`done` or FR equivalents) | warn | protocol | `protocol/exchange.md` §Lifecycle |
| F7 | Sessions have conformant frontmatter (`persona`, `date`) | info | protocol | `protocol/exchange.md` §Sessions |

## Naming checks (N)

| ID | Rule | Severity | Level | Source |
|----|------|----------|-------|--------|
| N1 | Notes follow `note-{subject}-{author}.md` | info | instance | Instance convention |
| N2 | Reviews follow `review-{subject}-{author}.md` | info | instance | Instance convention |
| N3 | Roadmaps follow `roadmap-{product}.md` | info | instance | Instance convention |

## Archiving checks (A)

| ID | Rule | Severity | Level | Source |
|----|------|----------|-------|--------|
| A1 | Files with status `done`/`traite` are in `archives/` | warn | instance | Instance convention — keeps scan lean |
| A2 | Files in `archives/` have status `done`/`traite` | info | instance | Coherence check |

## Roadmap checks (R)

| ID | Rule | Severity | Level | Source |
|----|------|----------|-------|--------|
| R1 | Roadmap has `# Roadmap` header | warn | instance | Convention — structure formelle |
| R2 | Roadmap declares an Owner in blockquote | warn | instance | Convention — ownership |
| R3 | Version sections have metadata comment | info | instance | Convention — frontmatter versions |
| R4 | Items have a status (`[done]`/`[running]`/`[todo]`/`[blocked]`/`[ready]`) | warn | instance | Convention — progress tracking |
| R5 | Items have an `@owner` | warn | instance | Convention — accountability |
| R6 | Roadmaps use `↔` convergence markers | info | instance | Convention — cross-instance dependencies |
| R7 | Roadmaps use `cible:` markers | info | instance | Convention — target dates |
| R8 | Roadmaps use `source:` markers | info | instance | Convention — source references |

---

## Artifact types

By default, the audit scans `notes` and `reviews` in `shared/`. An instance can declare additional artifact types in `shared/conventions.md` using a `## Artifact types` section:

```markdown
## Artifact types

| Type | Directory | Naming | Frontmatter |
|------|-----------|--------|-------------|
| notes | shared/notes/ | note-{subject}-{author}.md | from, to, nature, status, date |
| reviews | shared/review/ | review-{subject}-{author}.md | from, to, nature, status, date, subject |
| features | shared/features/ | feature-{name}.md | from, to, nature, status, date |
```

The `--artifacts` flag lets the user override which types are audited:

```bash
# Audit only protocol checks + notes and reviews (default)
python audit-instance.py /path/to/instance

# Audit with features included
python audit-instance.py /path/to/instance --artifacts notes,reviews,features

# Protocol checks only — skip all instance artifact checks
python audit-instance.py /path/to/instance --protocol-only
```

When `--protocol-only` is set, all instance-level checks (S4-S7, S10, F5, N1-N3, A1-A2, R1-R8) are skipped.

---

## Phase 2 — Exchanges & friction

Phase 2 scans all `.md` files in the declared artifact directories and extracts:

- **Exchange matrix** — who sends to whom (from `from:`/`to:` frontmatter)
- **Friction matrix** — who challenges whom (from friction markers in body)
- **Orchestrator friction** — frictions from session summaries (`## Orchestrator friction`)
- **reportPattern()** — convergence detection across rejected frictions

These are observational — no pass/fail, just data.
