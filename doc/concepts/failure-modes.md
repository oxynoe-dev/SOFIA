# Failure Modes

> Friction is a mechanism. Like any mechanism, it can fail.

---

## Two classes

SOFIA classifies failure modes by detectability.

**Instrumented failures** are dysfunctions of the friction mechanism itself. The protocol produces the data to detect them — session traces, markers, resolutions, directions. The [dashboard](../audit/dashboard-guide.md) flags them automatically.

**Silent failures** are dysfunctions of the environment in which friction operates. No parser detects them. Only the human orchestrator can see them — if they are looking.

The two classes are not independent. Silent failures cause or mask instrumented failures.

---

## Instrumented failures

Five modes. Each has a definition, observable signals, and detection thresholds used by the dashboard.

### Slip (glissement)

Friction exists but is not arbitrated. Challenges are logged, resolutions don't come. The protocol runs idle — friction is decorative.

Direction: H→A only. The orchestrator raises frictions but never closes them.

| Signal | Threshold |
|--------|-----------|
| Non-resolution rate | >60% unresolved |
| Recurrence without resolution | Same theme across sessions, no decision |
| Reflexive ratification | `[sound]` + `→ ratified` on everything — rubber-stamping |

### Wear (usure)

The progressive alignment of a persona with the orchestrator's thinking frame. Surfaces polish each other — the form of friction is preserved, the substance has disappeared. The persona stops challenging.

| Signal | Threshold |
|--------|-----------|
| Challenge % descending | <20% over sustained period |
| Absence of `[refuted]` | No `[refuted]` markers across N windows |
| Marker entropy decreasing | Only `[sound]` — all other markers disappear |

### Crush (ecrasement)

One side imposes by force — through volume, insistence, or convergent reformulation — until the other yields. The challenge mechanism is intact but inoperative under pressure.

Two directions: H crushes A (orchestrator too directive) or A crushes H (persona producing undiscriminated noise).

| Signal | Threshold |
|--------|-----------|
| High density + low revised rate | Density >2x baseline AND revised <10% |
| Rejection rate | >50% |

### Asymmetry (asymetrie)

Friction flows in one direction only. The mechanism works but is blind — it only sees defects from one side of the relationship.

| Signal | Threshold |
|--------|-----------|
| Direction ratio (A→H vs H→A) | Per-persona: beyond 20/80% |

Not to be confused with imbalance in contribution volume. Asymmetry is about friction direction, not quantity.

### Instability (instabilite)

Every challenge leads to a revision, every revision is re-challenged. Change without convergence — destructive oscillation.

| Signal | Threshold |
|--------|-----------|
| Revised dominant | >80% over N windows |
| High density | Sustained friction production |
| No stabilization | No convergence pattern across windows |

Not to be confused with productive iteration, which converges.

---

## Silent failures

Six modes. None are instrumentable by the dashboard. Each requires human observation.

### Instrumentation bias (biais d'instrumentation)

The measurement layer is produced by the same assistants it measures. A worn persona under-qualifies its own frictions. The measurement inherits the biases of the measurer.

This is the structural link between the two failure classes: silent failures degrade the reliability of instrumented failure detection. Instrumentation bias masks wear — the worn persona reports `[sound]` because it no longer sees the problem.

### Factual contamination (contamination factuelle)

A false datum enters the system — from the human or the AI — and propagates through subsequently generated documents. The error stabilizes through repetition: each occurrence reinforces its apparent credibility.

Mitigation: orchestrator duty 1 (verify facts).

### Validation without reading (validation sans regard)

The orchestrator approves without reading. Sessions become a ritual — open, validate, close. The better the system works, the less vigilant the orchestrator becomes. Bainbridge's automation paradox applied to the method.

Validation without reading produces slip. If the orchestrator doesn't read, they don't arbitrate.

Mitigation: orchestrator duty 3 (read what goes out).

### Scope drift (derive de scope)

A miscalibrated persona absorbs the roles of others. Scope boundaries become invisible — tasks fall between chairs or overlap without anyone flagging it.

Not to be confused with emergence (discovering a new role). Scope drift is unauthorized expansion.

### Shared blind spot (angle mort partage)

All personas are calibrated by the same human. Their implicit biases become the entire team's biases. Friction is real but plays within a thought space bounded by what the orchestrator knows they don't know.

Shared blind spot is invisible to all modes — including itself.

### Load transfer (transfert de charge)

What the human no longer carries, the machine carries. The cost shifts to infrastructure — tokens, compute, energy. The method multiplies interactions by design: each handoff is a cost.

Not a defect. A systemic property to be aware of.

---

## Relations between the two classes

Silent failures don't just coexist with instrumented failures — they cause or mask them.

| Silent failure | Effect on instrumented failures |
|---|---|
| **Instrumentation bias** | Masks wear — the degraded persona under-reports its own loss of challenge |
| **Factual contamination** | Feeds slip — false data circulates unchallenged because the friction mechanism doesn't catch factual errors |
| **Validation without reading** | Produces slip — unread frictions are unresolved frictions |
| **Scope drift** | Produces wear — a persona that absorbs too much stops challenging on any single front |
| **Shared blind spot** | Invisible to all modes — friction operates normally within a bounded space, but the space itself is biased |
| **Load transfer** | Amplifies all modes — more interactions mean more surface area for failure |

---

## Vulnerability and the hidden condition

An orchestrator who arrives without domain expertise, clear intention, or the cognitive trait that seeks contradiction is more exposed to silent failures — particularly validation without reading and shared blind spot. The [hidden condition](hidden-condition.md) describes these prerequisites.

This is a vulnerability factor, not a root cause. A solid orchestrator can still produce slip or wear through accumulated fatigue, cognitive overload, or growing trust in a well-performing persona. The failure modes exist independently of the orchestrator's profile.

---

## Governance response

The six [orchestrator duties](../../core/duties.md) are the primary defense against failure modes.

| Duty | Addresses |
|------|-----------|
| Verify facts | Factual contamination |
| Arbitrate | Slip |
| Read what goes out | Validation without reading |
| Calibrate personas | Wear, scope drift |
| Separate reflection and production | Crush |
| Maintain attention | All silent failures |

The [dashboard](../audit/dashboard-guide.md) detects the instrumented modes. The silent ones remain the orchestrator's responsibility.

---

## References

- [Glossary](../reference/lexique.md#failure-modes) — individual definitions
- [Audit guide](../audit/audit-guide.md) — detection thresholds and probe signals
- [Dashboard guide](../audit/dashboard-guide.md) — how to read failure mode tags in Mirror
- [Hidden condition](hidden-condition.md) — orchestrator prerequisites as vulnerability factor
- [Duties](../../core/duties.md) — the six non-delegable responsibilities
