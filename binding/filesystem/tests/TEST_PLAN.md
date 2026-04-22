# Test plan — binding/filesystem

> Couverture actuelle, trous identifies, cahier de tests cible.
>
> Specific to the filesystem binding. Tests run with Python stdlib unittest (zero dependencies).

---

## Current coverage

### What's tested (62 tests, 2 files)

| File | Tests | Covers |
|------|-------|--------|
| `test_audit_instance.py` | 38 | parser (frontmatter, normalization, friction markers, persona discovery), probe (structure checks, artifact scanning, matrices, session friction, signals) |
| `test_create_instance.py` | 24 | create-instance.py (scaffolding, per-persona files, content validation, helpers) |

### What's NOT tested

| Module | Gap |
|--------|-----|
| `analysis.py` | Orchestration, --output, --sanitize, per-instance + aggregated output |
| `scan.py` | Session/artifact parsing, record extraction |
| `mirror.py` | Health aggregation, radars, trajectory, KPI, cross-instance "all" |
| `lens.py` | Time series, per-persona breakdown, cross-instance "all" |
| `sanitize.py` | Field stripping, matrix anonymization |
| `aggregate.py` | Instance discovery, JSON merge, index.json generation |
| `build_dist.py` | Selective cleanup, JS patching, HTML stripping |
| `serve.py` | Out of scope (local dev server) |

### Fixture

`tests/fixtures/mini-instance/` — 2 personas (alice, bob), 5 artifacts, 2 sessions. Minimal but functional.

---

## Test plan — target

### How to run

```bash
cd binding/filesystem
python -m unittest discover tests -p "test_*.py" -v
```

---

### T1 — Pipeline unit tests (`test_pipeline.py`)

Unit tests for the data pipeline modules. Use mini-instance fixture.

| ID | Test | Module | Status |
|----|------|--------|--------|
| T1.1 | scan produces friction_records from sessions | scan.py | todo |
| T1.2 | scan produces contribution_records from sessions | scan.py | todo |
| T1.3 | scan produces signaler_patterns from sessions | scan.py | todo |
| T1.4 | scan extracts meta (personas, sessions_scanned, artifacts_scanned) | scan.py | todo |
| T1.5 | mirror produces per-persona flux (flux_h, flux_a, flux_types) | mirror.py | todo |
| T1.6 | mirror produces radars (6 axes, baseline vs recent) | mirror.py | todo |
| T1.7 | mirror produces trajectory (challenge %, density) | mirror.py | todo |
| T1.8 | mirror produces KPI (friction_density, resolution_rate, challenge_pct) | mirror.py | todo |
| T1.9 | mirror produces open_frictions (unresolved, last 20) | mirror.py | todo |
| T1.10 | mirror cross-instance "all" when 2+ instances | mirror.py | todo |
| T1.11 | lens produces time_series (week + day) with correct labels | lens.py | todo |
| T1.12 | lens produces per-persona markers/directions/resolutions | lens.py | todo |
| T1.13 | lens produces flux_h_pct / flux_a_pct / direction_ratio | lens.py | todo |
| T1.14 | lens cross-instance "all" merges time series by date | lens.py | todo |

---

### T2 — Sanitize tests (`test_sanitize.py`)

Verify sensitive fields are stripped, non-sensitive fields preserved.

| ID | Test | Status |
|----|------|--------|
| T2.1 | sanitize_records strips description, source, source_type, ref, is_amendment | todo |
| T2.2 | sanitize_records preserves persona, date, marker, initiative, direction, resolution | todo |
| T2.3 | sanitize_mirror strips friction_records descriptions + persona_roles from meta | todo |
| T2.4 | sanitize_mirror preserves radars, trajectory, KPI | todo |
| T2.5 | sanitize_lens preserves time_series, personas, totals | todo |
| T2.6 | sanitize_probe strips check details, removes signals | todo |
| T2.7 | sanitize_probe anonymizes non-persona keys in matrices → "orchestrator" | todo |
| T2.8 | sanitize handles wrapped shape (instances + default + all) | todo |
| T2.9 | sanitize handles flat shape (instance dict without wrapper) | todo |

---

### T3 — Aggregate tests (`test_aggregate.py`)

Verify multi-instance aggregation from per-instance JSON files.

| ID | Test | Status |
|----|------|--------|
| T3.1 | discover_instances finds subdirs with lens.json or mirror.json | todo |
| T3.2 | discover_instances ignores subdirs without JSON | todo |
| T3.3 | discover_instances ignores files (not dirs) | todo |
| T3.4 | aggregate_mirror merges per-instance data under instances key | todo |
| T3.5 | aggregate_mirror produces "all" with merged friction_records when 2+ instances | todo |
| T3.6 | aggregate_mirror no "all" when single instance | todo |
| T3.7 | aggregate_mirror sums flux_h/flux_a/flux_types across instances | todo |
| T3.8 | aggregate_lens merges time series by date label (sum values) | todo |
| T3.9 | aggregate_lens merges persona data (sum counts, recompute ratios) | todo |
| T3.10 | aggregate_lens no "all" when single instance | todo |
| T3.11 | build_index lists instances + generated timestamp | todo |
| T3.12 | aggregate is idempotent (2 runs produce same output) | todo |

---

### T4 — Build dist tests (`test_build_dist.py`)

Verify static dashboard build.

| ID | Test | Status |
|----|------|--------|
| T4.1 | build_dist creates index.html, css/, js/, data/, legend/ | todo |
| T4.2 | build_dist does NOT destroy non-generated files (canary test) | todo |
| T4.3 | build_dist patches fetch paths in app.js (data/lens.json, etc.) | todo |
| T4.4 | build_dist removes probe tab + refresh button from HTML | todo |
| T4.5 | build_dist copies data to external --data-dir when set | todo |
| T4.6 | build_dist with --sanitize strips fields via sanitize.py | todo |

---

### T5 — Analysis orchestration tests (`test_analysis.py`)

Verify analysis.py end-to-end orchestration.

| ID | Test | Status |
|----|------|--------|
| T5.1 | run_pipeline writes per-instance JSON in output/<instance>/ | todo |
| T5.2 | run_pipeline writes aggregated JSON at output/ root | todo |
| T5.3 | run_pipeline writes index.json with instance list | todo |
| T5.4 | run_pipeline with --only mirror skips lens and probe | todo |
| T5.5 | run_pipeline with --sanitize strips sensitive fields | todo |
| T5.6 | run_pipeline with 2+ instances produces "all" aggregation | todo |

---

### E2E-1 — End-to-end: Sofia guide (getting-started)

Test the user journey: follow the getting-started guide from scratch, use Sofia (the persona) to create an instance, add personas, run first session with friction. Manual test — Sofia is a conversational persona, not a script.

| ID | Step | Verification | Status |
|----|------|--------------|--------|
| E2E-1.1 | Clone sofia/, follow getting-started.md prerequisites | Claude Code installed, CLAUDE.md points to Sofia | todo |
| E2E-1.2 | Boot Sofia, request instance creation (mode 1) | Sofia walks through the 5 phases (understand, propose personas, calibrate, generate, briefing) | todo |
| E2E-1.3 | Verify created instance structure | sofia.md, shared/conventions.md, shared/orga/personas/, workspaces with sessions/ | todo |
| E2E-1.4 | Run probe on the created instance | All protocol checks pass (PS1-PS5, PP1-PP4) | todo |
| E2E-1.5 | Boot a persona, run a first session with friction | Session summary with ## Orchestrator friction, markers detected | todo |
| E2E-1.6 | Close session (closeSession protocol) | Summary file created, frontmatter valid, friction format correct | todo |
| E2E-1.7 | Run full analysis pipeline on the instance | records.json, mirror.json, lens.json, probe.json produced | todo |
| E2E-1.8 | Verify analysis output | Per-instance subdir + aggregated root + index.json, frictions from E2E-1.5 visible | todo |

### E2E-1b — End-to-end: create-instance.py (script)

Automated test: create instance via script, verify structure and audit.

| ID | Step | Verification | Status |
|----|------|--------------|--------|
| E2E-1b.1 | Run create-instance.py with 2 personas in tmpdir | Instance directory created with expected structure | todo |
| E2E-1b.2 | Run probe on the created instance | All protocol checks pass (PS1-PS5, PP1-PP4) | todo |
| E2E-1b.3 | Simulate a session (write a session summary with friction) | Session file parseable, friction markers detected | todo |
| E2E-1b.4 | Run full analysis pipeline on the instance | records.json, mirror.json, lens.json, probe.json produced | todo |
| E2E-1b.5 | Verify analysis output structure | Per-instance subdir + aggregated root + index.json | todo |
| E2E-1b.6 | Clean up (tmpdir) | All removed | todo |

---

### E2E-2 — End-to-end: Pipeline data + h2a contribution

Full workflow: analysis → aggregate → build_dist with adding an external instance.

| ID | Step | Verification | Status |
|----|------|--------------|--------|
| E2E-2.1 | Create tmpdir simulating h2a-data structure (data/ + dashboard/) | Dirs exist | todo |
| E2E-2.2 | Run analysis.py on mini-instance with --sanitize -o tmpdir/data | Per-instance JSON in data/mini-instance/, aggregated at data/ root, index.json | todo |
| E2E-2.3 | Verify sanitization | No description/source fields in friction_records | todo |
| E2E-2.4 | Create a second instance (mini-instance-2) with different personas | Instance exists | todo |
| E2E-2.5 | Run analysis.py on instance-2 with --sanitize -o tmpdir/data | data/mini-instance-2/ created | todo |
| E2E-2.6 | Run aggregate.py on tmpdir/data | index.json lists 2 instances, lens.json + mirror.json have "all" key | todo |
| E2E-2.7 | Run build_dist.py --output tmpdir/dashboard --data-dir tmpdir/data | dashboard/ contains index.html, css/, js/, data/, legend/ | todo |
| E2E-2.8 | Verify dashboard/data/ contains aggregated JSON | lens.json + mirror.json present with 2 instances | todo |
| E2E-2.9 | Verify non-generated files survive rebuild (canary) | Canary file in dashboard/ still present after build | todo |
| E2E-2.10 | Clean up (tmpdir) | All removed | todo |

---

## Fixtures needed

| Fixture | For | Status |
|---------|-----|--------|
| `mini-instance/` | T1, T5, E2E-1, E2E-2 | exists |
| `mini-instance-2/` | E2E-2 (second instance, different personas) | todo — create with 2 different personas (charlie, diana) |
| Sample JSON (records, mirror, lens, probe) | T2, T3 | todo — generate from mini-instance or create minimal stubs |

---

## Priority

1. **E2E-1** (Sofia guide) — highest value, validates the user journey end-to-end (manual)
2. **E2E-1b + E2E-2** — automated e2e, validates script + pipeline + h2a workflow
3. **T3** (aggregate) — new code, no coverage
4. **T4** (build_dist) — new behavior (selective cleanup)
5. **T2** (sanitize) — critical for publication
6. **T1** (pipeline) — largest gap but modules are stable
7. **T5** (analysis orchestration) — partially covered by E2E
