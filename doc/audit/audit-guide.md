# Audit guide — Conformity

> Running structural conformity checks on a SOFIA instance.
> This guide covers the **probe** tool (`binding/filesystem/`). For friction analysis, see [analysis-guide.md](analysis-guide.md). For the dashboard, see [dashboard-guide.md](dashboard-guide.md).

---

## When to audit

- **Before a release** — part of the pre-release checklist
- **After a structural change** — new personas, workspace reorganization, conventions update
- **Periodically** — to detect drift (wear/usure, silent personas, unrouted artifacts)
- **On a new instance** — to verify initial conformity after bootstrapping

---

## Running the probe

```bash
# Full audit — protocol + artifact + instance checks
python binding/filesystem/analysis.py /path/to/instance --only probe

# Protocol checks only (skip artifact and instance checks)
python binding/filesystem/analysis/cli/probe.py /path/to/instance --protocol-only

# Include specific artifact types
python binding/filesystem/analysis/cli/probe.py /path/to/instance --artifacts notes,reviews,features
```

---

## Reading the results

Each check has an ID, a rule, and a severity:

| Severity | Meaning | Action |
|----------|---------|--------|
| `fail` | Blocks conformity | Must fix before the instance is considered valid |
| `warn` | Degraded quality | Should fix — the protocol works but with gaps |
| `info` | Informational | No action required — signals for the orchestrator |

Check IDs follow a taxonomy: `{level}{category}{number}`. See `binding/filesystem/audit.md` for the full reference.

### ID taxonomy

| Prefix | Level | Category |
|--------|-------|----------|
| `PS` | Protocol | Structure (sofia.md, shared/, CLAUDE.md) |
| `PP` | Protocol | Personas (files, dimensions, contexts) |
| `PA` | Protocol | Artifacts (frontmatter, required fields) |
| `PF` | Protocol | Friction (session structure, markers) |
| `AN/AR/AF/AD` | Artifact type | Notes, reviews, features, ADRs |
| `IS` | Instance | Structure (orga/, roadmaps, archives) |
| `IN/IR` | Instance | Naming, roadmap (ownership, versioning) |

---

## Common issues

| Check | Typical cause | Fix |
|-------|---------------|-----|
| `PS1 fail` | Missing `sofia.md` at root | Run `create-instance.py` or create manually |
| `PP3 warn` | Persona missing dimensions | Review persona file against the 7 dimensions |
| `PA1 warn` | Artifacts without frontmatter | Add YAML frontmatter (from, to, nature, status, date) |
| `PF1 warn` | Sessions without friction section | Add `## Orchestrator friction` to session summaries |

---

## Signals

The probe emits high-level signals when patterns emerge.

### Structural signals

| Signal | What it means |
|--------|---------------|
| Friction holes | A persona emits 0 reviews |
| Pure receiver | A persona receives but never emits |
| No incoming friction | A persona's work is never reviewed |

### Failure mode signals

The 5 instrumented failure modes are detectable from session data. The probe flags early indicators; the [dashboard](dashboard-guide.md) Mirror view provides the full diagnostic.

| Mode | Signal | Threshold |
|------|--------|-----------|
| **Slip** | Non-resolution rate, recurrence without resolution, reflexive ratification | >60% unresolved |
| **Wear** | Challenge % descending, absence of `[refuted]`, marker entropy decreasing | Challenge % <20% over sustained period |
| **Crush** | High density + low revised rate, rejection rate | Density >2x baseline AND revised <10% |
| **Asymmetry** | Direction ratio (A→H vs H→A) | Per-persona: 20/80% threshold |
| **Instability** | Revised dominant, high density, no stabilization | Revised >80% over N windows |

6 silent failure modes (instrumentation bias, factual contamination, validation without reading, scope drift, shared blind spot, load transfer) are not instrumentable — they require human observation. See the [glossary](../reference/lexique.md#failure-modes) for definitions.

These signals appear in the Probe and Mirror tabs of the [dashboard](dashboard-guide.md).
