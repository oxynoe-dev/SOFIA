---
binding: filesystem
---

# Team organization {Project}

**Project**: {Project}
**Date**: {date}
**Author**: {architect persona or orchestrator}

---

## The team

<!-- Complete list: the orchestrator + all active personas.
     Update on each persona addition/removal. -->

| Persona | Role | Status |
|---------|------|--------|
| **{Orchestrator name}** | Orchestrator | Human — decision maker |
| **{Persona 1}** | {Role} | Specialized AI assistant |
| **{Persona 2}** | {Role} | Specialized AI assistant |

---

## Collaboration flows

<!-- Main flows between personas. Adapt to the team.
     Name the flows, describe the direction, indicate who triggers what.
     Typical flows: decisional, technical, scientific, editorial. -->

### Decisional flow
The Product Owner initiates and validates. {Architect persona} translates into architecture,
{strategist persona} into strategy. Decisions go up to the orchestrator.

### Technical flow
{Architect persona} specifies contracts → {dev persona} implements and surfaces
frictions → {UX persona} specifies UI behaviors.

### Editorial flow
<!-- If the team has a writer and a publication pipeline.
     Specify: who writes, who validates substance, who produces form,
     who challenges before publication, who triggers scripts. -->

{Writer persona} writes the content. Experts validate substance.
{Prod persona} produces form. {UX persona} challenges before publication.
The orchestrator validates before any output.

---

## Operating rules

<!-- Team invariants. Adapt, but these three rules
     are non-negotiable in SOFIA: -->

- **The orchestrator is the sole final decision maker** — personas propose, analyze, challenge. The orchestrator decides.
- **Frictions surface** — any blockage or inconsistency between personas is flagged explicitly, not worked around.
- **Nothing goes out without orchestrator validation** — the orchestrator rereads before any publication.

<!-- Add project-specific rules: -->

---

## Scopes — simplified RACI matrix

<!-- Adapt rows to the project's key decisions.
     R = Responsible · A = Approver · C = Consulted
     The orchestrator is always Approver. -->

| Decision | Orchestrator | {P1} | {P2} | {P3} |
|---|---|---|---|---|
| {Decision 1} | A | R | C | — |
| {Decision 2} | A | C | R | — |
| {Decision 3} | A | — | C | R |
| Publication (all channels) | A | C | C | C |

*R = Responsible · A = Approver · C = Consulted*

---

## Challenge rights

<!-- Each persona has explicit oversight on certain deliverables
     from others. Friction does not rely on goodwill — it is
     structural. Fill in for each active persona. -->

| Persona | Challenge |
|---------|-----------|
| **{Persona 1}** | {what they have oversight on} |
| **{Persona 2}** | {what they have oversight on} |
| **{Persona 3}** | {what they have oversight on} |

---

*{Project} — {date}*
