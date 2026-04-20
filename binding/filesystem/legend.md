# Legend — How to read the SOFIA dashboard

This dashboard instruments a real human-AI collaboration practice. Every number comes from actual session logs and artifacts — nothing is simulated.

---

## What is this dashboard?

SOFIA is a method for orchestrating specialized AI personas on a real project. One human orchestrator works with multiple constrained AI agents, each with a defined role (architect, researcher, developer, etc.). They disagree by design.

This dashboard makes the quality of that disagreement visible.

---

## The 5 tabs

| Tab | Purpose |
|-----|---------|
| **Map** | What does the organization look like? — Entry point. Functional map of instances, personas, and roles. Right-click to navigate to any other tab with the right context pre-selected. |
| **Mirror** | Am I healthy? — The orchestrator sees their own practice reflected back. KPIs, radars, trajectory. |
| **Lens** | What happened? — Raw data exploration. Time series, counts, distributions. |
| **Probe** | Is the instance conforming? — Structural audit. Checks, missing sections, format compliance. |
| **Legend** | You are here. How to read all of the above. |

---

## Reading the Map

Three elements showing the topology and health of your SOFIA setup.

### Instance cards

One card per instance showing:
- **Health dot** (green/orange/red): percentage of personas with friction data
- **Persona list**: each persona with their role. Greyed-out = no friction (blind spot)
- **Friction count**: total frictions detected for the instance

Right-click any instance or persona to navigate directly to Mirror, Lens, or Probe with the filter pre-selected.

### Trajectory

Challenge % over time, using friction windows (not calendar). A descending line = the instance is going quiet. Hover for date range per window.

### Persona mini cards

Below the trajectory: one small card per persona showing friction count and context size (lines loaded at boot). Color-coded: green = healthy, yellow = attention, red = danger.

---

## The KPI banner

Five indicators at the top of Mirror.

### Orchestrator

**What it measures**: Is the orchestrator still pushing back AND resolving frictions?

- Healthy: the orchestrator contests some persona outputs (H→A > 0) or open frictions are low
- Complacent: H→A = 0 AND frictions pile up unresolved (>10 open)

**Why it matters**: An orchestrator who says yes to everything produces the same output as no orchestrator at all.

### Recent challenge

**What it measures**: Challenge % of the last N frictions — share of non-sound frictions.

**Why it matters**: Low challenge = personas validate without resistance. A healthy instance maintains challenge over time.

### Open frictions

**What it measures**: Frictions without resolution — piloting debt.

**Why it matters**: The orchestrator sees the list, arbitrates in the next session, the friction leaves the list.

### Coverage

**What it measures**: What percentage of declared personas have at least one friction?

- Green: 100% — every persona participates in the friction cycle
- Orange: >50%
- Red: ≤50% — half the team is invisible to the protocol

**Why it matters**: A persona without friction is a blind spot.

### PO / A contrib

**What it measures**: Total epistemic contributions — PO (orchestrator) vs A (assistants).

**Why it matters**: Balanced contributions = co-construction. PO >> A = orchestrator drives. A >> PO = personas drive.

---

## Reading the radars

Each radar has 6 axes. Two contours: grey (baseline — first N frictions) and colored (recent — last N frictions). If the colored contour shrinks, the practice is degrading.

### The 6 axes

| Axis | Formula | What it means |
|------|---------|---------------|
| **Challenge %** | (contestable + simplification + blind_spot) / total | How much of the friction is actual pushback, not just validation. Low = rubber-stamping. |
| **A→H %** | (AI contests human) / total | How often a persona pushes back on the orchestrator. This is the return on constraint design. |
| **H→A %** | (human contests AI) / total | How often the orchestrator pushes back on a persona. Zero = the orchestrator consumes without questioning. |
| **Resolution %** | resolved / total | How many frictions received an explicit decision. Unresolved = steering debt. |
| **Diversity** | distinct resolution types used / 4 | Variety of decisions. 25% = only ratified. 100% = all four types used (ratified, contested, revised, rejected). |
| **Contribution %** | A / (A + H) | Persona's share of the epistemic exchange. 50% = balanced. >50% = persona drives. <50% = orchestrator drives. |

### Instance radar vs persona radars

- **Instance radar** (view 1a): one aggregated contour across all personas. The health of the whole instance at a glance.
- **Persona radars** (view 1b): one radar per persona, displayed side by side. Who challenges, who rubber-stamps, who changed.

---

## Reading the trajectory

### How windowing works

Frictions are sorted by date of appearance and grouped into windows of fixed size (e.g., 15 frictions per window). Windows are not calendar-based — a window may cover 2 days or 2 weeks depending on friction density. Hover over a window to see its date range.

### Challenge % line

- X axis: windows (w1, w2, w3...)
- Y axis: challenge % per window — share of non-sound frictions
- A descending line = the instance is going quiet
- Used on both Map (home) and Mirror

---

## Reading the contribution flow

Stacked bar chart in Mirror showing the epistemic contribution breakdown per persona.

Each bar is split by contribution type:
- **substance** — new information, facts, data, references
- **structure** — organization, categorization, synthesis
- **contestation** — challenge, counter-example, reframing
- **decision** — arbitration, choice made

H contributions (orchestrator) and A contributions (persona) are summed. The Contribution % axis on the radar shows the persona's share (A / total).

---

## Glossary

### Friction markers

| Marker | Symbol | Meaning |
|--------|--------|---------|
| **sound** | ✓ | The position is well-founded. No issue. |
| **contestable** | ~ | The position can be challenged. It holds but has weak points. |
| **simplification** | ⚡ | The position simplifies reality. Something important is lost. |
| **blind_spot** | ◐ | Something was missed entirely. An angle nobody considered. |
| **refuted** | ✗ | The position is factually wrong or logically broken. |

### Resolutions

| Resolution | Meaning |
|------------|---------|
| **ratified** | The friction was examined and the position holds. Decision: keep as is. |
| **contested** | The friction is acknowledged but the decision is deferred or disputed. |
| **revised** | The friction led to a change. The original position was modified. |
| **rejected** | The friction was examined and dismissed. The challenge did not hold. |

### Directions

| Direction | Notation | Meaning |
|-----------|----------|---------|
| **H→A** | Human contests AI | The orchestrator pushes back on a persona's output. |
| **A→H** | AI contests Human | A persona pushes back on the orchestrator's direction. |

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
| **Orchestrator** | The human who coordinates the AI personas. Makes final decisions. |
| **Persona** | A constrained AI agent with a defined role, expertise, and boundaries. |
| **Instance** | A project workspace where one orchestrator works with a team of personas. |
| **Session** | A single working conversation between the orchestrator and one persona. |
| **Window** | A group of N consecutive frictions, used for trend analysis instead of calendar periods. |
| **Baseline** | The first N frictions of an instance or persona — the reference point for detecting change. |
| **Domestication** | When a persona stops challenging over time — its friction output converges to pure validation. |
| **H2A** | Human-to-Assistant — the protocol that structures friction, contribution, and exchange between orchestrator and personas. |
