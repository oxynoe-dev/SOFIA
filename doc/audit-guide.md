# Audit guide

> When to audit, how to run the tools, what the results mean.

---

## When to audit

- **Before a release** — part of the pre-release checklist
- **After a structural change** — new personas, workspace reorganization, conventions update
- **Periodically** — to detect drift (domestication, silent personas, unrouted artifacts)
- **On a new instance** — to verify initial conformity after bootstrapping

---

## Tools

Two tools, two purposes:

| Tool | Purpose | What it reads |
|------|---------|---------------|
| `probe.py` | **Conformity** — structural protocol checks | Instance structure, frontmatter, personas, conventions |
| `analysis.py` | **Analysis** — friction, contribution, trajectory | Session summaries, artifacts, friction markers |

Both live in `binding/filesystem/`.

---

## Running the audit

### Conformity (probe)

```bash
# Full audit — protocol + artifact + instance checks
python binding/filesystem/analysis.py /path/to/instance --only probe

# Protocol checks only (skip artifact and instance checks)
python binding/filesystem/analysis/cli/probe.py /path/to/instance --protocol-only

# Include specific artifact types
python binding/filesystem/analysis/cli/probe.py /path/to/instance --artifacts notes,reviews,features
```

### Analysis (mirror + lens)

```bash
# Full pipeline — scan + mirror + lens + probe
python binding/filesystem/analysis.py /path/to/instance

# Multiple instances
python binding/filesystem/analysis.py /path/to/instance1 /path/to/instance2

# Single view
python binding/filesystem/analysis.py /path/to/instance --only mirror
python binding/filesystem/analysis.py /path/to/instance --only lens

# Launch dashboard server
python binding/filesystem/analysis.py /path/to/instance --serve
```

### Dashboard

```bash
# Start the dashboard (serves analysis.html on localhost)
python binding/filesystem/analysis.py /path/to/instance --serve
```

The dashboard has 5 tabs:
- **Map** — instance topology, persona cards, health indicators
- **Mirror** — orchestrator health KPIs, radar, trajectory
- **Lens** — raw time series, per-persona breakdown
- **Probe** — conformity checks (pass/warn/fail)
- **Legend** — documentation of all metrics and indicators

### Static build

```bash
# Generate a standalone dist/ directory (HTML + CSS + JS + JSON)
python binding/filesystem/build_dist.py /path/to/instance

# For h2a-data repository structure
python binding/filesystem/build_dist.py /path/to/instance --data-dir /path/to/h2a-data/data
```

---

## Reading the results

### Conformity (probe)

Each check has an ID, a rule, and a severity:

| Severity | Meaning | Action |
|----------|---------|--------|
| `fail` | Blocks conformity | Must fix before the instance is considered valid |
| `warn` | Degraded quality | Should fix — the protocol works but with gaps |
| `info` | Informational | No action required — signals for the orchestrator |

Check IDs follow a taxonomy: `{level}{category}{number}`. See `binding/filesystem/audit.md` for the full reference.

**Common issues**:
- `PS1 fail` — missing `sofia.md` at root → run `create-instance.py` or create manually
- `PP3 warn` — persona missing dimensions → review persona file against the 7 dimensions
- `PA1 warn` — artifacts without frontmatter → add YAML frontmatter (from, to, nature, status, date)

### Analysis (mirror + lens)

The analysis produces observational data — no pass/fail, just indicators for the orchestrator's attention.

**Key signals to watch**:
- **Only `[sound]` frictions** → domestication signal, the persona has stopped challenging
- **No friction over consecutive sessions** → friction possibly absent
- **High contested/rejected ratio** → sustained tension to investigate
- **Persona without session for several days** → inactive persona
- **Artifacts not routed** → exchange blocked

**Trajectory** (Mirror tab): tracks challenge % over time. A declining trajectory suggests domestication. A stable trajectory above 20-30% suggests healthy friction.

**Contribution flow** (Mirror tab): stacked bar by persona showing substance/structure/contestation/decision balance. Heavy `substance` from assistant + heavy `decision` from human = healthy asymmetry.

---

## Cost

The audit tools run locally — no API calls, no token cost. They parse Markdown files and produce JSON.

The dashboard (`--serve`) runs a local HTTP server. The static build (`build_dist.py`) produces a self-contained directory.

Sofia's audit mode (mode 4) requires loading the full method context at boot (~100K tokens for the extended boot). This is a provider cost, not an audit tool cost.
