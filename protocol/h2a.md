# H2A — Human-to-Assistant Protocol

> The coordination protocol between a human and their assistants.

---

## Positioning

H2A formalizes the coordination layer between a human (orchestrator) and constrained assistants (personas) in a work instance. It replaces neither technical guardrails nor interfaces: it structures the collaboration itself.

| Protocol | Layer | Nature |
|----------|-------|--------|
| MCP (Anthropic) | Agent ↔ Tools | Technical — wire protocol |
| A2A (Google) | Agent ↔ Agent | Technical — communication |
| **H2A** | **Human ↔ Assistant** | **Organizational — coordination** |

H2A is not a technical protocol — it defines the semantics of interactions, not their implementation. See `binding/implementation.md` for current implementation choices.

## Entities

H2A relies on 7 constitutive entities. See `core/model.md` for details.

| Entity | Protocol doc |
|--------|-------------|
| Instance, Space, Persona, Orchestrator | this document |
| Exchange | `exchange.md` |
| Friction | `friction.md` |
| Contribution | `contribution.md` |

## Invariants

Invariants are the constitutive properties of the protocol — without which H2A is no longer H2A. They derive from the method's principles (see `core/principles.md`) but do not cover all of them: principles guide the entire method (persona design, iteration, constraint as tool), invariants cover only the exchange protocol. Invariant 5 is of a different nature — it formalizes a structural limitation, not a capability.

1. **Constitutive friction** — friction is not a defect to fix but a structuring signal. The protocol MUST capture, qualify, and preserve it.
2. **Human arbiter** — the orchestrator MUST resolve divergences between personas. No persona decides for another.
3. **Isolation** — a persona MUST NOT interact outside its space and the shared space. The orchestrator is the only one who crosses boundaries.
4. **Traceability** — every exchange MUST produce an identifiable trace.
5. **Residual opacity** — the protocol cannot guarantee that the orchestrator arbitrates without bias. This limitation is structural, not fixable. The protocol MUST document it and SHOULD provide mitigation mechanisms (cf. `reportPattern()` in `friction.md`), but no mechanism constitutes a guarantee.

## Operations

Implicit operations derived from entities and dimensions. Their explicit formalization (signature, wire format) is planned when a real-time implementation justifies it.

| Operation | Trigger | Involved entities |
|-----------|---------|-------------------|
| openSession() | orchestrator | Exchange (session), Persona |
| closeSession() | orchestrator | Exchange (session), Friction, Contribution |
| send() | persona (on orchestrator instruction) | Exchange (artifact) |
| receive() | orchestrator | Exchange (artifact), Persona (recipient) |
| markRead() | orchestrator | Exchange (artifact) |
| markDone() | orchestrator | Exchange (artifact) — triggers archiving |
| qualifyFriction() | persona (pre-fills), orchestrator (validates) | Friction |
| qualifyContribution() | persona | Contribution |
| reportPattern() | persona | Friction — meta-operation (see `friction.md`) |

## Protocol / observation distinction

The protocol distinguishes two formalization layers:

| Layer | Status | Verification | Examples |
|-------|--------|-------------|----------|
| **Protocol** | Guaranteed | Computational (deterministic, automatable) | Produced artifacts, deposited notes, session traces |
| **Observational** | Best-effort | Inferential (semantic judgment, non-deterministic) | Qualified friction, epistemic flow, contribution tags |

The protocol layer defines what the audit can mechanically verify. The observational layer is filled by the assistant and validated by the human.

## Audit

### Auditability principle

> What is in the protocol is what an audit tool can verify cross-instance without instance-specific configuration.

### Computational checkpoints (MUST)

| Checkpoint | Verification |
|------------|-------------|
| Session traces present | Each session produced an identifiable trace |
| Session metadata | Each trace carries: persona, date, session identifier |
| Protocol sections | Each trace contains: Produced, Decisions, Shared notes, Open |
| Artifact metadata | Each artifact carries: emitter, recipient, nature, status, date |
| Status lifecycle | Values in {new, read, done} |
| Isolation | No persona produced outside its space and the shared space |

> **FR retrocompat.** The parser also accepts FR identifiers (juste, angle-mort, faux, ratifie, conteste, revise, rejete, nouveau, lu, traite, matiere).

### Observational signals (MAY)

| Signal | Interpretation |
|--------|---------------|
| No friction over N consecutive sessions | Friction possibly absent — domestication? |
| Only `[sound]` | Persona in validation mode |
| Artifacts not routed for N exchanges | Exchange blocked |
| Persona without session for N days | Inactive persona |

These signals are not protocol violations — they are indicators for the orchestrator's attention.

## Terminology

The keywords "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY" are to be interpreted as described in RFC 2119.

## Theoretical lineage

| Reference | Contribution to H2A |
|-----------|---------------------|
| Sheridan & Verplank (1978) | 10 levels of autonomy — historical HITL framework |
| Toulmin (1958) | Argumentation model — illuminates the 5 markers |
| Searle (1995) | Constitutive vs regulative rules — core/protocol/doc distinction |
| Böckeler (2026) | Computational vs inferential — protocol/observational layer distinction |
| Wood, Bruner & Ross (1976) | Scaffolding — asymmetric collaboration |
| Elster (1979) | Precommitment — productive constraint |

## Structural limitations

The protocol documents what it cannot guarantee. These limitations are inherent to the model, not bugs to fix.

| Limitation | Nature | Mitigation |
|------------|--------|-----------|
| **Residual opacity** (invariant 5) | The orchestrator cannot arbitrate their own resistance to friction. Local undecidability. | reportPattern() — mitigation, not guarantee |
| **Uninstrumented friction** | A participant can express positions in free text without markers. The signal is lost to the protocol. | Friction template in contexts. Depends on participant discipline. |
| **Silent lineage** | If the `antecedent` field is omitted, the friction chain is broken without signal. The protocol cannot guess that one friction resolves another. | Validation block before commit. Hooks (v0.4). |
| **Cross-instance exchanges** | Cross-instance routing depends entirely on the orchestrator. No automatic discovery or routing mechanism between instances. | Formalized in `exchange.md` §Cross-instance exchanges. Artifact MUST be deposited in the recipient's shared space. |

## Origin

This protocol was formalized empirically across 3 instances (April 2026). The 4 protocol/ documents are the reference.
