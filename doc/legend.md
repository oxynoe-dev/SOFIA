# Legend — How to read the SOFIA dashboard

This dashboard instruments a real human-AI collaboration practice. Every number comes from actual session logs and artifacts — nothing is simulated.

---

## Introduction

SOFIA is a method for orchestrating specialized AI personas on a real project. One human orchestrator works with multiple constrained AI agents, each with a defined role (architect, researcher, developer, etc.). They disagree by design.

The H2A protocol (Human-to-Assistant) captures and qualifies this disagreement — called **friction** — as structured data. This dashboard makes the quality of that friction visible.

### What the dashboard shows

Five tabs, each a different lens on the same data:

| Tab | Question | What you see |
|-----|----------|-------------|
| **Map** | What does the organization look like? | Instance cards, trajectory, persona cards |
| **Mirror** | Is the practice healthy? | KPIs, radars, contribution flow, open frictions, silence map |
| **Lens** | What happened over time? | Time series, distributions, counts |
| **Probe** | Is the instance conforming? | Structure checks, context sizes, activity |
| **Legend** | How do I read all this? | You are here |

### How the data is collected

The parser scans all `.md` files (sessions and artifacts) for friction markers. A friction is any line that contains a marker + an initiative tag. Same parser everywhere — no distinction between session summaries and review artifacts.

---

## Map

The entry point. Shows the topology of your SOFIA setup at a glance.

### Instance cards

One card per instance. Each card shows:

| Element | Meaning |
|---------|---------|
| **Health dot** (green/orange/red) | Coverage — percentage of declared personas that have at least one friction |
| **Instance name** | The instance identifier (from `sofia.md`) |
| **Friction count** | Total frictions detected across all files in this instance |
| **Persona list** | Each persona with their role. Greyed-out = no friction data (blind spot) |

Right-click any instance or persona to navigate to Mirror, Lens, or Probe with the filter pre-selected.

### Trajectory — challenge %

A line chart showing how the instance evolves over time.

| Element | Meaning |
|---------|---------|
| **X axis** | Friction windows (w1, w2, w3...) — groups of N consecutive frictions |
| **Y axis** | Challenge % — share of non-sound frictions in each window |
| **Descending line** | The instance is going quiet — less challenge over time |
| **Tooltip** | Hover to see the date range covered by each window |

Windows are not calendar-based. A window may cover 2 days or 2 weeks depending on friction density. This avoids artifacts from variable activity.

### Persona mini cards

Below the trajectory: one small card per persona showing:

| Element | Meaning |
|---------|---------|
| **Friction count** | Green if > 0, red if 0 (blind spot) |
| **Ctx lines** | Context size (persona.md + contexte.md loaded at boot). Green < 150, yellow 150-250, red > 250 |

---

## Mirror

The health diagnostic. The orchestrator sees their own practice reflected back.

### KPI banner

Five indicators at the top.

| KPI | What it measures | Green | Red |
|-----|-----------------|-------|-----|
| **Orchestrator** | Is the orchestrator still pushing back AND resolving? | H→A > 0 or open frictions low | H→A = 0 AND > 10 open — complacent |
| **Recent challenge** | Challenge % of the last N frictions | > 20% | < 10% — rubber-stamping |
| **Open frictions** | Unresolved frictions — piloting debt | Low count | High count — decisions not made |
| **Coverage** | % of declared personas with at least one friction | 100% | ≤ 50% — half the team invisible |
| **PO / A contrib** | Orchestrator vs assistant epistemic contributions | Balanced | Strong imbalance — one side dominates |

### Instance radar (view 1a)

One aggregated radar for the whole instance. Two contours:
- **Grey** = baseline (first N frictions)
- **Teal** = recent (last N frictions)

A shrinking contour = the instance is degrading.

### Persona radars (view 1b)

One radar per persona, displayed side by side. Same baseline/recent contours.

### The 6 radar axes

| Axis | Formula | Meaning |
|------|---------|---------|
| **Challenge %** | (contestable + simplification + blind_spot) / total | How much pushback vs pure validation. Low = rubber-stamping |
| **A→H %** | (AI contests human) / total | Persona pushes back on orchestrator. The return on constraint design |
| **H→A %** | (human contests AI) / total | Orchestrator pushes back on persona. Zero = consumes without questioning |
| **Resolved %** | resolved / total | Frictions with explicit decision. Unresolved = steering debt |
| **Diversity** | distinct resolution types / 4 | 25% = only ratified. 100% = all 4 types used (ratified, contested, revised, rejected) |
| **Contribution %** | A / (A + H) | Persona's share of epistemic exchange. 50% = balanced. > 50% = persona drives |

### Trajectory — challenge % (view 0)

Same as the Map trajectory but affected by the instance/persona filters.

### Trajectory — marker distribution

Stacked bar showing the marker breakdown per window. A monochrome bar (all sound) = domestication visible.

### Contribution flow

Stacked bar chart per persona, broken down by contribution type:

| Type | Meaning |
|------|---------|
| **substance** | New information — fact, data, reference, insight |
| **structure** | Organization, categorization, synthesis |
| **contestation** | Challenge, counter-example, reframing |
| **decision** | Arbitration, choice retained |

H (orchestrator) and A (persona) contributions are summed.

### Delta table

| Column | Meaning |
|--------|---------|
| **Persona** | Name |
| **Baseline challenge %** | Challenge % of the first N frictions |
| **Recent challenge %** | Challenge % of the last N frictions |
| **Delta** | ↑ increasing, ↓ decreasing, = stable |
| **Baseline A→H** | A→H % at the start |
| **Recent A→H** | A→H % now |
| **Diagnostic** | healthy / domesticated / servile / complacent |

### Open frictions

List of frictions without resolution, sorted oldest first. The orchestrator arbitrates in the next session — the friction leaves the list.

| Column | Meaning |
|--------|---------|
| **Date** | When the friction was recorded |
| **Source** | File where the friction was found |
| **Persona** | Who emitted the friction |
| **Marker** | sound, contestable, simplification, blind_spot, refuted |
| **Direction** | a_corroborates_h, a_contests_h, h_corroborates_a, h_contests_a |
| **Description** | First 120 characters of the friction text |

### Silence map

Matrix persona × marker. Each cell = friction count with that marker.

| Signal | Meaning |
|--------|---------|
| **Zero (red)** | Persona present but no friction of this type — blind spot |
| **Row of zeros** | Persona invisible to the protocol |
| **Column of zeros** | Marker never used across all personas |

---

## Lens

Raw data exploration — time series, counts, distributions. What happened over time.

### Score cards

| Card | Meaning |
|------|---------|
| **Frictions** | Total friction markers detected in the selected period |
| **Resolved** | Percentage with a resolution (ratified, contested, revised, rejected) |
| **Ratified** | Count of ratified resolutions |
| **Contested** | Count of contested resolutions |
| **reportPattern** | Number of reportPattern triggers (convergence of rejections) |

### Charts

| Chart | X axis | Y axis | Reading |
|-------|--------|--------|---------|
| **Friction by marker — timeline** | Period (week/day) | Count per marker | Rising line = more friction of that type |
| **Direction — who contests whom** | Personas | Count (right = A, left = H) | Diverging bar — persona positions vs orchestrator positions |
| **Direction — timeline** | Period | Count per direction | A→H rising = personas push back more |
| **Markers by persona** | Personas | Stacked count | Monochrome = domestication |
| **Resolutions by persona** | Personas | Stacked count | All ratified = no real arbitration |
| **Epistemic flow — H vs A** | Personas | % (H vs A) | Who drives the exchange |
| **Frictions per session — timeline** | Period | Average per session | Falling = sessions produce less signal |

### Tables

| Table | Content |
|-------|---------|
| **Directional matrix** | A corroborates H, A contests H, H corroborates A, H contests A per persona. Ratio > 2 = healthy friction |
| **Detail by persona** | Sessions, markers, resolutions, flux ratio, reportPattern count |
| **reportPattern counter** | Triggers, erreur LLM, conviction, resistance per persona |

---

## Probe

Structural audit — is the instance conforming to the protocol?

### Context size

Bar chart per persona showing the total lines of persona.md + contexte.md loaded at boot.

| Threshold | Color | Meaning |
|-----------|-------|---------|
| < 150 lines | Green | Compact — optimal |
| 150-250 lines | Yellow | Attention — risk of compression in long sessions |
| > 250 lines | Red | Danger — context will be compressed, persona will drift |

### Structure checks

Protocol conformity checks: sofia.md marker, shared/ structure, session frontmatter, artifact frontmatter, isolation.

| Status | Meaning |
|--------|---------|
| **Pass** (✓) | Conformant |
| **Warn** (⚠) | Minor issue |
| **Fail** (✗) | Protocol violation |

### Orchestrator friction

Friction markers from session summaries per persona: markers, resolutions, initiative (persona vs PO), reportPattern triggers.

### Activity

Sessions per persona. Zero = inactive persona.

### Exchange flow

Top artifact flows between personas — who sends to whom, ranked by volume.

---

## Glossary

### Friction markers

| Marker | Symbol | Meaning |
|--------|--------|---------|
| **sound** | ✓ | The position is well-founded. Corroboration |
| **contestable** | ~ | The position can be challenged. Weak points exist |
| **simplification** | ⚡ | The position simplifies reality. Something important is lost |
| **blind_spot** | ◐ | Something was missed entirely. An angle nobody considered |
| **refuted** | ✗ | The position is factually wrong or logically broken |

### Resolutions

| Resolution | Meaning |
|------------|---------|
| **ratified** | Position holds. Decision: keep as is |
| **contested** | Acknowledged but deferred or disputed |
| **revised** | Led to a change. Original position modified |
| **rejected** | Dismissed. The challenge did not hold |

### Directions

| Direction | Notation | Meaning |
|-----------|----------|---------|
| **H→A** | Human contests AI | Orchestrator pushes back on a persona |
| **A→H** | AI contests Human | Persona pushes back on the orchestrator |

### Contribution types

| Type | Meaning |
|------|---------|
| **substance** | New information — fact, data, reference, insight |
| **structure** | Organization, categorization, synthesis |
| **contestation** | Challenge, counter-example, reframing |
| **decision** | Arbitration, choice retained |

### Key terms

| Term | Definition |
|------|------------|
| **Orchestrator** | The human who coordinates the AI personas. Makes final decisions |
| **Persona** | A constrained AI agent with a defined role, expertise, and boundaries |
| **Instance** | A project workspace where one orchestrator works with a team of personas |
| **Session** | A single working conversation between the orchestrator and one persona |
| **Artifact** | A structured file deposited in shared/ — note, review, feature spec |
| **Window** | A group of N consecutive frictions, used for trend analysis instead of calendar periods |
| **Baseline** | The first N frictions of an instance or persona — the reference point for detecting change |
| **Domestication** | When a persona stops challenging over time — its friction output converges to pure validation |
| **Lineage** | A chain of frictions linked by the antecedent dimension — one logical friction with its resolution history |
| **H2A** | Human-to-Assistant — the protocol that structures friction, contribution, and exchange |
