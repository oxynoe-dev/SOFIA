# Analysis guide — Data pipeline

> Generating, sanitizing, and publishing H2A friction data.
> This guide covers `analysis.py` and the data workflow (`binding/filesystem/`). For conformity checks, see [audit-guide.md](audit-guide.md). For the dashboard, see [dashboard-guide.md](dashboard-guide.md).

---

## Pipeline overview

```
analysis.py <instances>
    │
    ├── scan.py     → records.json     (raw friction + contribution records)
    ├── mirror.py   → mirror.json      (health diagnostics: KPIs, radars, trajectory)
    ├── lens.py     → lens.json        (time series: markers, directions, flux)
    └── probe.py    → probe.json       (conformity checks)
```

Two independent pipelines:
- **Data pipeline** (scan → mirror + lens): reads session summaries and artifacts, extracts friction/contribution records, builds aggregated views
- **Conformity pipeline** (probe): reads instance structure directly, runs checks

---

## Output structure

`analysis.py` writes **per-instance** and **aggregated** JSON:

```
<output>/
├── methodes/           per-instance
│   ├── records.json
│   ├── mirror.json
│   ├── lens.json
│   └── probe.json
├── produits/           per-instance
│   └── ...
├── records.json        aggregated (all instances)
├── mirror.json         aggregated
├── lens.json           aggregated
├── probe.json          aggregated
└── index.json          instance list
```

Default output: `binding/filesystem/analysis/data/` (gitignored).

---

## Usage

### Basic

```bash
# Full pipeline — all views, all instances
python binding/filesystem/analysis.py /path/to/instance1 /path/to/instance2

# Single view
python binding/filesystem/analysis.py /path/to/instance --only mirror
python binding/filesystem/analysis.py /path/to/instance --only lens
python binding/filesystem/analysis.py /path/to/instance --only probe

# Launch dashboard after analysis
python binding/filesystem/analysis.py /path/to/instance --serve
```

### Custom output directory

```bash
# Write to a specific directory
python binding/filesystem/analysis.py /path/to/instance -o /path/to/output
```

When `-o` is set, per-instance subdirectories and aggregated files are written to the specified directory instead of the default `analysis/data/`.

### Sanitization

```bash
# Strip sensitive fields for open-source publication
python binding/filesystem/analysis.py /path/to/inst1 /path/to/inst2 \
    --sanitize -o /path/to/h2a-data/data
```

The `--sanitize` flag strips:
- **Friction/contribution descriptions** — qualitative content
- **Source filenames** — session paths with timestamps
- **Probe check details** — filenames in warn/fail messages
- **Persona role descriptions** — real role text
- **Non-persona identifiers** — replaced with "orchestrator" in matrices

What is preserved: markers, resolutions, directions, types, dates, personas, counters, trajectories, radars.

The standalone script `binding/filesystem/sanitize.py` can also be used independently on existing JSON files:

```bash
python binding/filesystem/sanitize.py input_dir/ output_dir/
```

---

## Static build

Generate a standalone dashboard (HTML + CSS + JS + JSON) that can be served by any static file server:

```bash
# Self-contained dist/
python binding/filesystem/build_dist.py

# For h2a-data repository structure
python binding/filesystem/build_dist.py \
    --output /path/to/h2a-data/dashboard \
    --data-dir /path/to/h2a-data/data
```

The static build excludes the Probe tab and the refresh button (no server to call).

---

## Contributing external data

When a colleague uses SOFIA and wants to contribute their friction data:

```bash
# 1. Run analysis on their instance (with them, sanitized)
python binding/filesystem/analysis.py /path/to/their-instance \
    --sanitize -o /path/to/h2a-data/data

# 2. Aggregate all instances (regenerates index.json + aggregated JSON)
python binding/filesystem/aggregate.py /path/to/h2a-data/data

# 3. Rebuild the dashboard
python binding/filesystem/build_dist.py \
    --output /path/to/h2a-data/dashboard \
    --data-dir /path/to/h2a-data/data
```

`aggregate.py` is idempotent — it scans all subdirectories in the data directory containing `lens.json` or `mirror.json`, merges them, and regenerates the root-level aggregated files. Adding an instance = creating a new subdirectory + re-running.

`aggregate.py` is only needed when adding an external instance without re-running `analysis.py` on all instances. When you run `analysis.py` with multiple instances, it already produces per-instance + aggregated output.

---

## Complete workflow

### Internal use (audit + dashboard)

```bash
python binding/filesystem/analysis.py \
    /path/to/methodes /path/to/produits /path/to/oxynoe \
    --serve
```

### Publication (h2a-data)

```bash
# Generate sanitized data
python binding/filesystem/analysis.py \
    /path/to/methodes /path/to/produits /path/to/oxynoe \
    --sanitize -o /path/to/h2a-data/data

# Build static dashboard
python binding/filesystem/build_dist.py \
    --output /path/to/h2a-data/dashboard \
    --data-dir /path/to/h2a-data/data
```
