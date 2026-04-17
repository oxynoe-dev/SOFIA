# Field experience report — Product chain

> Specify, implement, challenge. Three roles, one cycle, zero shortcuts.

---

## The pattern

The product chain is Katen's core cycle. It's the oldest, most battle-tested
pattern, and the most revealing of the SOFIA method in action.

```
The orchestrator identifies a need or friction
  → opens architect session

Architect specifies
  → ADR, interface contracts, formal specs
  → doesn't code — if the spec is vague, the dev will say so

Dev implements
  → code, tests, friction reports
  → doesn't reinterpret — if the spec is ambiguous, they escalate

UX challenges
  → review of flows, visual states, accessibility
  → doesn't produce the code — she specifies expected behaviors

Researcher verifies
  → formal invariants, consistency with the Petri-net model
  → doesn't decide on architecture — she validates the theory

The orchestrator arbitrates and decides
  → when personas diverge, the orchestrator decides
  → the decision is traced (ADR, note, session)
```

## What we observed on Katen

### The spec forces clarity

Mira doesn't code. That's the most productive constraint on the team.
Because she can't "show it in the code", she's forced to specify
clearly — interface contracts, expected states, edge cases. The result:
62 ADRs, 24 architecture principles. Specs that Axel can implement
without guessing.

Without that constraint, the architect jumps straight to pseudo-code.
The spec stays vague. The dev interprets. Bugs are structural,
not technical.

### Implementation friction surfaces the real problems

Axel doesn't work around issues. When an interface contract generates
unexpected complexity, he flags it rather than patching. These escalations
changed ADRs — not because the spec was bad, but because the field
reveals what theory can't see.

Concrete case: operator parallelization. Mira blocks ("not now, the
roadmap has higher priorities"). Léa confirms from an orthogonal angle
("no research interest"). Two refusals, two independent reasons. The
topic is deferred. Three weeks later, the design comes back — better
than it would have been.

### UX challenges what the dev doesn't see

Nora questions onboarding flows that satisfy the developer but lose
the user. She doesn't code — she specifies expected behaviors. Axel
escalates technical constraints. The friction between them produces
interfaces that hold up both technically AND humanly.

### The researcher anchors in the formal

Léa doesn't decide on architecture. But when an implementation touches
the Petri-net model's invariants — firing policy, connection states,
reversibility — she verifies. Her "that doesn't hold" carries the same
authority as a failing test: you don't push through.

### The orchestrator carries the context

The orchestrator is the only one who sees all sessions. They filter,
reformulate, contextualize. When Mira deposits a review for Axel,
the orchestrator adds: "we decided yesterday with Marc to delay
publication — that changes the priority of this spec." No persona
has that context alone.

## ADRs as the backbone

Every structural decision produces an ADR. The format is standard:
context, decision, consequences, status. The ADR isn't bureaucracy
— it's memory.

An unwritten ADR is a decision that will be questioned three sessions
later by someone who didn't know about it. Over 210+ sessions, that
happens fast.

ADRs potentially go through 4 challengers:
- **Mira** — consistency with target architecture
- **Axel** — implementation feasibility
- **Léa** — formal rigor (when the topic touches the model)
- **Marc** — strategic impact (when the topic touches positioning)

The orchestrator decides. The ADR is accepted, rejected, or deferred. Status is traced.

## For your project

The product chain is SOFIA's fundamental use case. A few rules:

- **The architect doesn't code.** That's constraint number one. If your architect can code, they'll never specify clearly.
- **The dev doesn't reinterpret.** If the spec is vague, they escalate. They don't guess. Friction is the signal, not noise.
- **UX doesn't produce the code.** She specifies behaviors. The dev escalates constraints. The friction between them produces good interfaces.
- **Trace everything.** ADRs, sessions, reviews. If it's not traced, it doesn't exist.
- **The orchestrator arbitrates.** When two personas diverge, the orchestrator decides. Not the most eloquent persona.
