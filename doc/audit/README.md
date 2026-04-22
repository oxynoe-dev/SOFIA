# Audit & Analysis

> Observing and verifying a SOFIA instance — conformity, friction, trajectory.

---

## Scope

The tools documented here are **specific to the filesystem binding** (`binding/filesystem/`). They parse Markdown files, frontmatter, and session logs stored on disk. A different binding (API, database) would require different audit tools — the protocol defines *what* to observe, these guides document *how* to observe it with the filesystem implementation.

See `protocol/h2a.md` for the protocol-level definition of friction, contribution, and conformity.

---

## Two axes

| Axis | Question | Tool | Output |
|------|----------|------|--------|
| **Conformity** | Does the instance respect the protocol structure? | `probe.py` | Pass/warn/fail checks |
| **Analysis** | How is friction evolving? Is the orchestrator healthy? | `analysis.py` (scan + mirror + lens) | JSON data, dashboard |

Conformity is binary — a check passes or fails. Analysis is observational — no judgment, just indicators for the orchestrator's attention.

---

## Guides

| Guide | Content |
|-------|---------|
| [Audit guide](audit-guide.md) | Conformity checks — when to audit, how to run probe, reading results, common issues |
| [Analysis guide](analysis-guide.md) | Data pipeline — analysis.py, workflow, sanitization, contribution |
| [Dashboard guide](dashboard-guide.md) | The 5 views (Map, Mirror, Lens, Probe, Legend) — what each shows, how to read it |

---

## Quick start

```bash
# Conformity check
python binding/filesystem/analysis.py /path/to/instance --only probe

# Full analysis + dashboard
python binding/filesystem/analysis.py /path/to/instance --serve

# Multi-instance, output to h2a-data
python binding/filesystem/analysis.py /path/to/inst1 /path/to/inst2 \
    --sanitize -o /path/to/h2a-data/data
```

---

## Cost

All tools run locally — no API calls, no token cost. They parse Markdown and produce JSON. The dashboard runs a local HTTP server or a static build.

Sofia's audit mode (mode 4) is different: it requires loading the full method context at boot (~100K tokens). That is a provider cost, not an audit tool cost.
