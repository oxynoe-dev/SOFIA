# Audit rules — binding/filesystem

> Reference for all checks performed by `audit-instance.py`.

---

## Check ID taxonomy

Format: `{level}{category}{number}`

| Prefix | Level | Category | Conditioned by |
|--------|-------|----------|----------------|
| PS | Protocol | Structure | always |
| PA | Protocol | Artifacts | always |
| PF | Protocol | Format | always |
| AN | Artifact | Note | `--artifacts notes` |
| AR | Artifact | Review | `--artifacts reviews` |
| AF | Artifact | Feature | `--artifacts features` |
| IS | Instance | Structure | not `--protocol-only` |
| IN | Instance | Naming | not `--protocol-only` |
| IR | Instance | Roadmap | not `--protocol-only` |

## Severity

| Severity | Meaning |
|----------|---------|
| `fail` | Blocks conformity — the instance is not valid |
| `warn` | Should be fixed — degraded quality |
| `info` | Informational — no action required |

---

## Protocol checks

### Protocol Structure (PS)

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| PS1 | `sofia.md` present at root | fail | `protocol/exchange.md` — instance marker |
| PS2 | `shared/` directory present | fail | `protocol/exchange.md` — shared space |
| PS3 | `shared/conventions.md` present | warn | `protocol/exchange.md` — exchange rules |
| PS4 | At least 1 workspace with `CLAUDE.md` | fail | `protocol/exchange.md` — persona space |
| PS5 | Each workspace has `sessions/` | warn | `protocol/exchange.md` — session traces |

### Protocol Artifacts (PA)

Global checks on ALL `.md` files in `shared/` (excluding `conventions.md`, `roadmap-*.md`, `orga/`, `audits/`).

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| PA1 | All artifacts have frontmatter | warn | `protocol/exchange.md` §Artifacts |
| PA2 | All artifacts have required fields (`from`, `to`, `nature`, `status`, `date`) | warn | `protocol/exchange.md` §Specific dimensions |
| PA3 | All status values are valid (`new`/`read`/`done` or FR equivalents) | warn | `protocol/exchange.md` §Lifecycle |

### Protocol Format (PF)

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| PF1 | Sessions have conformant frontmatter (`persona`, `date`) | info | `protocol/exchange.md` §Sessions |

## Artifact checks

Each declared artifact type gets 5 standard checks. Add `--artifacts notes,reviews,features` to control which types are audited.

### Artifact Note (AN)

| ID | Rule | Severity |
|----|------|----------|
| AN1 | `shared/notes/` present with `archives/` | info |
| AN2 | Notes have frontmatter | warn |
| AN3 | Required fields (`from`, `to`, `nature`, `status`, `date`) | warn |
| AN4 | Naming convention `note-{subject}-{author}.md` | info |
| AN5 | Done files archived | warn |

### Artifact Review (AR)

| ID | Rule | Severity |
|----|------|----------|
| AR1 | `shared/review/` present with `archives/` | info |
| AR2 | Reviews have frontmatter | warn |
| AR3 | Required fields (`from`, `to`, `nature`, `status`, `date`, `subject`) | warn |
| AR4 | Naming convention `review-{subject}-{author}.md` | info |
| AR5 | Done files archived | warn |

### Artifact Feature (AF)

| ID | Rule | Severity |
|----|------|----------|
| AF1 | `shared/features/` present | info |
| AF2 | Features have frontmatter | warn |
| AF3 | Required fields (`from`, `to`, `nature`, `status`, `date`) | warn |

## Instance checks

### Instance Structure (IS)

| ID | Rule | Severity |
|----|------|----------|
| IS1 | `shared/orga/` present | info |
| IS2 | Roadmaps in `shared/` | info |
| IS3 | No accents in frontmatter values | info |
| IS4 | Files in `archives/` have status `done` | info |

### Instance Naming (IN)

| ID | Rule | Severity |
|----|------|----------|
| IN1 | Roadmaps follow `roadmap-{product}.md` | info |

### Instance Roadmap (IR)

| ID | Rule | Severity |
|----|------|----------|
| IR1 | Roadmap has `# Roadmap` header | warn |
| IR2 | Roadmap declares an Owner | warn |
| IR3 | Version sections have metadata comment | info |
| IR4 | Items have a status tag | warn |
| IR5 | Items have an `@owner` | warn |
| IR6 | Uses `↔` convergence markers | info |
| IR7 | Uses `cible:` markers | info |
| IR8 | Uses `source:` markers | info |

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

# Protocol checks only — skip all artifact and instance checks
python audit-instance.py /path/to/instance --protocol-only
```

When `--protocol-only` is set, all artifact checks (AN1-AN5, AR1-AR5, AF1-AF3) and instance checks (IS1-IS4, IN1, IR1-IR8) are skipped.

---

## Phase 2 — Exchanges & friction

Phase 2 scans all `.md` files in the declared artifact directories and extracts:

- **Exchange matrix** — who sends to whom (from `from:`/`to:` frontmatter)
- **Friction matrix** — who challenges whom (from friction markers in body)
- **Orchestrator friction** — frictions from session summaries (`## Orchestrator friction`)
- **reportPattern()** — convergence detection across rejected frictions

These are observational — no pass/fail, just data.
