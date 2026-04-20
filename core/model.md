# Instance Model

> The 7 constitutive entities of a SOFIA instance.

---

## Overview

The SOFIA model defines the entities without which the method does not exist. Remove any of them and it is no longer SOFIA.

7 entities, organized in 3 levels:
1. Topology — Orchestrator, Instance, Space, Persona
2. Interaction — Exchange
3. Observation — Friction, Contribution

---

## Orchestrator

The human. Orchestrates instances, arbitrates conflicts between personas, routes exchanges. Has no space of their own — traverses everything.

The only participant not constrained by isolation. Also the only one who decides.

Responsibilities are non-delegable. See `duties.md`.

| Field | Type | Required | Definition |
|-------|------|----------|-----------|
| **identifier** | text | MUST | Unique orchestrator identifier |
| **instances** | list | MUST | Orchestrated instances |

---

## Instance

A deployment of the method on a project. Contains N spaces + 1 shared space. The instance must be identifiable — the identification mechanism is an implementation choice.

| Field | Type | Required | Definition |
|-------|------|----------|-----------|
| **identifier** | text | MUST | Unique instance identifier |
| **spaces** | list | MUST | Workspaces (1 per persona + 1 shared) |
| **orchestrator** | ref | MUST | The orchestrator who pilots this instance |
| **method_version** | text | MUST | Applied SOFIA version |

---

## Space

Isolated perimeter of a persona. A persona can only see its own space + the shared space.

| Field | Type | Required | Definition |
|-------|------|----------|-----------|
| **identifier** | text | MUST | Unique identifier within the instance |
| **persona** | ref | MUST | The persona operating in this space |
| **shared** | boolean | MUST | Shared space (exchange bus) or persona space |

### Why isolate

Isolation is not a technical constraint — it is what forces the persona to stay in its role.

- **Prevent scope drift** — a persona without boundaries ends up doing everything. The architect with code access ends up coding. The strategist who can read tests ends up giving technical opinions. Isolation makes drift impossible: the persona cannot see what is outside its perimeter.
- **Force formal exchanges** — if the architect cannot modify code, they are forced to produce a spec the developer can read. Isolation creates the need for exchange artifacts.
- **Protect work in progress** — a persona cannot accidentally break another's work.

### Constraint

> A space can only see its own perimeter + the shared space. The shared space is the only channel between personas. The orchestrator has no space — they traverse everything.

---

## Persona

Constrained role. An unconstrained LLM is a generalist — it accepts everything, contests nothing, and produces average content. A persona is a **constrained** LLM: it has a role, a tone, limits, and above all things it is not allowed to do.

Constraint changes everything:
- It asks questions instead of guessing
- It refuses what is outside its scope instead of improvising
- It surfaces frictions instead of working around them
- It produces typed artifacts instead of generic text

### 7 dimensions

| Dimension | Required | Definition |
|-----------|----------|-----------|
| **Identity** | MUST | Name (short, memorable, a first name), role (one sentence), tone |
| **Stance** | MUST | How it behaves, not what it knows |
| **Scope** | MUST | What it works on. Explicit list |
| **Deliverables** | MUST | What it produces |
| **Prohibitions** | MUST | What the persona does NOT do. Prohibitions create productive friction |
| **Right to contest** | MUST | What it is legitimate to challenge in others |
| **Collaboration** | MUST | How it interacts with other personas |

---

## Exchange

A traced interaction within the instance. An exchange is a communication act within the instance.

Personas never talk directly. The orchestrator routes everything. It is slow — by design. Each transmission is a moment where the orchestrator filters, reformulates, adds context, decides what is relevant.

| Field | Type | Required | Definition |
|-------|------|----------|-----------|
| **type** | enum | MUST | `session` (synchronous) or `artifact` (asynchronous deposit) |
| **instance** | ref | MUST | Instance where the exchange takes place |
| **space** | ref | MUST | Space of the concerned persona |
| **datetime** | datetime | MUST | Date and time of the exchange |
| **persona** | ref | MUST | Involved persona |

See `protocol/exchange.md` for type-specific dimensions.

---

## Friction

Qualified epistemic position of a participant on the other's proposition, expressed during an exchange.

| Field | Type | Required | Definition |
|-------|------|----------|-----------|
| **exchange** | ref | MUST | The exchange that generated the friction |
| **emitter** | ref | MUST | Persona or orchestrator emitting the position |
| **marker** | enum | MUST | `[sound]`, `[contestable]`, `[simplification]`, `[blind_spot]`, `[refuted]` |
| **description** | text | MUST | Short summary of the position |
| **initiative** | enum | MUST | `[persona]` or `[PO]` — who initiated the subject |
| **antecedent** | ref | MUST (if lineage) | Reference to a prior friction in the lineage |

See `protocol/friction.md` for marker details and format.

### Why friction is constitutive

Friction is the mechanism that produces better decisions. It **emerges** from the constraints placed on personas:

| Constraint | Friction produced |
|------------|-------------------|
| The architect does not code | Forced to specify clearly — the dev can contest the spec |
| The dev does not decide architecture | Forced to surface frictions — the architect must resolve them |
| The strategist has no code access | Forced to question value — the team must justify its choices |

Friction without an arbiter is chaos. The orchestrator decides. Personas expose tensions, the orchestrator listens, questions, then decides. The decision is traced.

### Signs that friction works

- Personas say "no" or "not my role"
- Disagreements appear between personas
- The orchestrator must regularly decide

### Signs that friction is absent

- All personas agree on everything
- Nobody says no
- The orchestrator never needs to decide

If a persona produces only `[sound]` over a long period, it is a domestication signal.

---

## Contribution

Epistemic input. Captures who brought what during an exchange.

| Field | Type | Required | Definition |
|-------|------|----------|-----------|
| **exchange** | ref | MUST | The exchange that generated the contribution |
| **direction** | enum | MUST | `[H]` (human brings) or `[A]` (assistant brings) |
| **type** | enum | MUST | `substance`, `structure`, `contestation`, `decision` |
| **description** | text | MUST | Short summary of the input |

See `protocol/contribution.md` for type details and format.

Contribution is distinct from friction: friction captures tension (opposing positions, resistance), contribution captures input (who fed what). A correction accepted without resistance is a contribution, not a friction.

---

## Relations

| From | To | Relation | Cardinality |
|------|----|----------|-------------|
| Orchestrator | Instance | orchestrates | 1 → 1..* |
| Instance | Space | contains | 1 → 1..* |
| Space | Persona | operates | 1 → 1 |
| Persona | Exchange | emits / receives | 1 → * |
| Orchestrator | Exchange | participates | 1 → * |
| Exchange | Friction | generates | 1 → * |
| Exchange | Contribution | generates | 1 → * |
| Persona | Persona | challenges | * → * |
| Friction | Friction | amends (antecedent) | 0..1 → 0..1 |
