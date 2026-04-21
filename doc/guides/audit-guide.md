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

**Terms**: *Mirror* shows orchestrator health (KPIs, radar, trajectory). *Lens* shows raw time series (per-persona, per-week). *Domestication* = a persona progressively aligns with the orchestrator's thinking and stops challenging. *Radar* = a 6-axis chart per persona (challenge %, contribution %, etc.).

#### Recommended workflow

1. **Start with Probe** — fix any `fail` checks first (structural conformity)
2. **Then Mirror** — check trajectory and KPIs (is friction healthy? any domestication?)
3. **Then Lens** — drill into per-persona time series (who contributes what, when?)

#### Signals and actions

| Signal | What it means | What to do |
|--------|---------------|------------|
| Only `[sound]` frictions | Domestication — the persona validates everything | Tighten prohibitions, review stance, consider recalibration |
| No friction over consecutive sessions | Friction absent — the persona may not be challenged | Check if the orchestrator presents enough cross-persona deliverables |
| High contested/rejected ratio | Sustained tension | Healthy if the topics are substantive. Investigate if the same theme recurs → may trigger reportPattern |
| Declining trajectory | Challenge % dropping over time | Domestication signal — recalibrate the persona or introduce a new one |
| Persona without session for several days | Inactive persona | Either the role isn't needed (consider deletion) or the orchestrator forgot to engage it |
| Artifacts not routed | Exchange blocked | Check shared/ for `status: new` artifacts that haven't been presented |
| Heavy `substance` from A + heavy `decision` from H | Healthy asymmetry | The assistant brings material, the human decides — this is the target pattern |
| Heavy `decision` from A | Assistant decides too much | The orchestrator may be rubber-stamping — slow down, read more carefully |

**Trajectory** (Mirror tab): tracks challenge % over time. A stable trajectory above 20-30% suggests healthy friction.

**Contribution flow** (Mirror tab): stacked bar by persona showing substance/structure/contestation/decision balance.

---

## Publishing data (open-source repo)

When publishing analysis data to an open-source repository (e.g., h2a-data), use the `--sanitize` flag to strip sensitive fields before export.

```bash
# Build dashboard + sanitized data for h2a-data
python binding/filesystem/build_dist.py \
    --output ../h2a-data/dashboard \
    --data-dir ../h2a-data/data \
    --sanitize
```

The `--sanitize` flag strips:
- **Friction/contribution descriptions** — qualitative content (what was said, contested, decided)
- **Source filenames** — session paths with timestamps and potentially real names
- **Probe check details** — filenames in warn/fail messages
- **Persona role descriptions** — real role text from persona files
- **Non-persona identifiers** — replaced with "orchestrator" in exchange/friction matrices

What is preserved: markers, resolutions, directions, types, dates, personas, aggregated counters, trajectories, radars.

The standalone script `binding/filesystem/sanitize.py` can also be used independently:

```bash
python binding/filesystem/sanitize.py binding/filesystem/analysis/data/ output/
```

---

## Cost

The audit tools run locally — no API calls, no token cost. They parse Markdown files and produce JSON.

The dashboard (`--serve`) runs a local HTTP server. The static build (`build_dist.py`) produces a self-contained directory.

Sofia's audit mode (mode 4) requires loading the full method context at boot (~100K tokens for the extended boot). This is a provider cost, not an audit tool cost.
