## ADR Decision

![Workflow — ADR Decision](../../doc/figures/fig-workflow-decision-adr.svg)

Structural decision workflow: from identified tension to trace in the index.

---

### When to use it

When a structural tension is identified — a technical choice, an architecture change, an arbitration between two incompatible approaches. Any persona can initiate the process.

### Steps

1. **Tension identified** — a persona observes a problem, an inconsistency, or a choice to make. They formulate the tension in one sentence
2. **Note deposited in shared/** — the persona deposits a note (cf. `protocol/exchange.md`) describing the context, identified options, and their recommendation
3. **Multi-persona review** — each concerned persona produces a review on their axis: architecture (consistency), dev (feasibility), research (rigor), UX (user impact), strategy (positioning)
4. **ADR drafting** — the architect drafts the ADR with **Proposed** status: context, decision, consequences, rejected alternatives
5. **Orchestrator arbitration** — the orchestrator moves the ADR to **Accepted** or **Rejected**. The decision is traced with its context
6. **Trace in the index** — the ADR is added to the index with status, summary, and date

### Roles involved

| Persona | Role |
|---------|------|
| Any persona | Identifies the tension, deposits the note |
| Concerned personas | Review on their axis |
| Architect | Drafts the ADR (Proposed) |
| Orchestrator | Arbitrates (Accepted / Rejected) |

### Artifacts produced

- Initial note (in `shared/notes/`)
- Reviews by axis (in `shared/review/`)
- ADR in standard format: Context, Decision, Consequences, Status
- Entry in the ADR index

### Pitfalls

- **Coding on a Proposed ADR** — a Proposed ADR is not an authorization. Only the Accepted status authorizes implementation. Coding before orchestrator arbitration means investing time on a decision that may be rejected
- **ADR without alternatives** — an ADR that doesn't list rejected alternatives is not an ADR, it's an announcement. The context of alternatives is what makes the decision understandable in 6 months
- **Confusing tension and preference** — a tension is an objective problem (inconsistency, blockage, incompatible choice). A preference is subjective. ADRs address tensions, not preferences
