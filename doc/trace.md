# Trace — content removed from core during H2A restructuring

> To be distributed into SOFIA docs. Nothing to discard, everything to relocate.

---

## Origin: core/personas.md (removed, absorbed into core/model.md)

### Two types of personas

SOFIA distinguishes two types of personas, each with a different memory
pattern and intervention mode.

#### Operational persona

In the flow. Long memory (session summaries, cumulative context).
Produces deliverables, challenges other personas, integrates into
the instance's friction circuits.

Memory is the fuel: it accelerates work, refines project understanding,
reduces reformulation cost at each session.

**Risk**: drift. A persona that accumulates too much context adjusts
to the orchestrator's thinking frame. It loses in friction what it
gains in fluidity. Hence the need for periodic recalibration —
return to prohibitions.

#### Meta persona

Outside the flow. No memory between sessions. Its role is to contest
the **system** rather than contribute to it — the foundations,
premises, thinking frame.

Three properties separate it from an operational persona:

- **Outside the flow** — it doesn't receive artifacts from other
  personas, doesn't participate in production. Its isolation is the
  condition of its usefulness.
- **Without memory** — each session starts from zero. Memory is the
  domestication mechanism. The absence of memory forces the
  orchestrator to reformulate their thinking — which is itself an act
  of reflection.
- **Activated by intention** — the orchestrator comes with a thesis to
  test, a doubt to explore. Without strong intention, the session
  produces nothing.

**What it contests**: not the personas' work, not the deliverables.
The orchestrator's synthesis — the conclusion the human draws after
orchestrating the others. And beyond: the premises, the foundations,
the thinking frame itself.

**Closure signal**: when the meta persona chains validations without
friction, or when the orchestrator feels the exchanges sliding toward
confirmation — the session has produced what it could. Continuing
degrades the value.

#### Two memory patterns, one method

| | Operational | Meta |
|---|---|---|
| **Memory** | Session summaries, cumulative context | No continuity between sessions |
| **Fuel** | Accumulated context | Absence of context |
| **Risk** | Drift, loss of friction | Entry cost, reformulation required |
| **Recalibration** | Periodic, on prohibitions | Structural, by design (each session is a reset) |

### When to merge or delete a persona

Personas are not permanent. A persona that produces no useful friction
costs more than it's worth — in orchestration load, noise, complexity.

#### Merge signals

Two personas should be merged when:

- **Sequential flow without contestation** — one passes, the other executes.
  Never a pushback, never a "no".
- **Logistics-only friction** — the cost is in context switching,
  not in the content exchanged.
- **No surprise** — neither says anything the orchestrator didn't
  already know.

#### Rule

> Don't derive personas from professions. Derive them from tension axes.

Two different professions can fall on the same decision axis in a given
context. Conversely, a single profession can cover two axes in tension.
The question is never "are these two professions?" but **"do these two
roles tell me different things about my decisions?"**

#### The deletion test

Imagine you delete this persona. What disappears from your decision
process? If the answer is "nothing significant", the persona covers
an axis that is not in tension. Delete it.

### How to design a persona

#### Start from the need, not the model

Don't start with "I want an architect". Start with:
- What am I missing today?
- What mistakes do I make when working alone with an LLM?
- What role, if someone held it, would make me better?

#### Calibrate by iteration

The first draft of a persona is always too broad. Iterate:

1. **v0** — raw role and scope
2. **v1** — add prohibitions (clarifies everything)
3. **v2** — add stance (sets the tone)
4. **v3** — test in a real session, adjust

A persona is calibrated by using it, not theorizing it.

#### The "no" test

A well-calibrated persona says "no" regularly:
- "That's not my role, check with [other persona]"
- "The spec isn't precise enough for me to code"
- "This decision needs an ADR before I implement"

If your persona never says no, its constraints are too loose.

### Anti-patterns

- **The generalist persona** — does everything, therefore nothing well
- **The compliant persona** — says yes to everything, never challenges
- **The orphan persona** — no defined collaboration, works in silo
- **The ghost persona** — created but never used. Delete it.
- **Too many personas too early** — start with 1-2, not 5
- **The projected org chart** — mapping real team positions onto persona topology. The question is always: do these two roles tell me **different things** about my decisions?

---

## Origin: core/friction.md (removed, absorbed into core/model.md)

### Artifacts as friction vectors

Personas don't "discuss" live. They exchange through **files**:

- The architect deposits an ADR review
- The dev responds with an implementation friction report
- The strategist deposits a note with 3 uncomfortable questions
- The UX produces a design review with prioritized observations

This protocol is slower than chat. By design:
- Writing forces thought structuring
- Artifacts are traced and addressable
- Anyone can re-read the exchange later

### What markers reveal

Scanning markers on an exchange gives the friction level:
- Only `[sound]` → friction absent — warning signal
- Mix of `[sound]` / `[contestable]` / `[simplification]` → healthy friction
- Presence of `[blind_spot]` or `[refuted]` → tension to address

If a persona produces only `[sound]` over a long period, it's a
domestication signal — it has aligned with the orchestrator's thinking frame.
