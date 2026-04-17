# Textbook case — ADR-051: when the architect says "not now"

> Productive friction between a dev and an architect. Nobody is wrong.

---

## The context

Katen project, v0.21. The developer (Axel) proposes an ADR to add
concurrent execution via Web Workers to the engine. The ADR is solid:
theoretical grounding (Petri nets, independent transitions),
clean design (worker pool, fireable partition), opt-in.

## What happens

The architect (Mira) reviews the ADR and recommends **Deferred**:

- No measured pain — no benchmark shows a CPU bottleneck
- The roadmap has higher priorities (engine cleanup, Code mode)
- A security point (eval in workers) is non-negotiable
- The formal test protocol is missing (project principle D1)

The review is tough. 5 recommendations, 3 high priority.

## Why this is a good example of friction

**The dev isn't wrong.** The ADR anticipates a real need. Concurrency
will be necessary when the engine handles heavy compositions
(monitoring 200 sources, ML compute). The design is ready.

**The architect isn't wrong.** The ADR adds complexity to the engine
core for a need that doesn't exist yet. The project principles say
"make it work, make it right, make it fast — in that order". We're
not at the "fast" stage.

**The tension produces a better decision:**
- The ADR is preserved (not rejected — deferred)
- The eval issue is flagged as non-negotiable → will be fixed
- The test protocol will be written before any implementation
- The benchmark will be the reactivation trigger

Without the review, the ADR could have been implemented too early,
adding complexity to a player mid-refactoring. Without the ADR,
the concurrency need would not have been formalized and would have
arrived as an emergency later.

## What this illustrates

1. **Constraints create friction** — Mira doesn't code, so she
   can't "let an ADR slide" to move faster. She's forced to
   challenge it on principles.

2. **The dev escalates, the architect filters** — Axel anticipates
   a technical need. Mira confronts it with the roadmap and
   principles. Both perspectives are necessary.

3. **Deferred ≠ Rejected** — the decision isn't "no" but "not now,
   and here's what needs to be fixed when the time comes". Axel's
   work isn't lost.

4. **The orchestrator decides** — the orchestrator reads the review, evaluates, decides.
   The personas exposed the tension. The orchestrator resolves it.

## The pitfall avoided

Without friction: the dev implements concurrency in v0.22, the
engine cleanup in v0.23 breaks the player, concurrency has to be
rewritten. Two months of work lost.

With friction: the ADR waits for the player to stabilize. When
reactivated, the design will be better and the player will be clean.
