## Product Chain

![Workflow — Product chain](../../doc/figures/fig-workflow-chaine-produit.svg)

Complete production chain: every step has a guardian, no shortcuts.

---

### When to use it

For any feature or evolution that crosses multiple domains — from prioritization to delivery. This is the reference workflow when multiple personas are involved.

### Steps

1. **The orchestrator prioritizes** — the item enters the roadmap with context and owner
2. **Architect specifies** — contracts, constraints, ADR if needed. Guardian: consistency with target architecture and principles (cf. `core/principles.md`)
3. **Dev implements** — plan mode, TDD, code. Guardian: conformity to the spec
4. **UX challenges** — UX verifies user experience, accessibility, visual consistency. Guardian: the product is usable, not just functional
5. **Research verifies** — formal verification, sources, rigor. Guardian: what is claimed is true and correctly contextualized
6. **The orchestrator arbitrates** — last gate. Final validation, go/no-go

### Roles involved

| Persona | Role |
|---------|------|
| Orchestrator | Prioritizes (step 1), arbitrates (step 6) |
| Architect | Specifies, guards structural consistency |
| Dev | Implements according to spec |
| UX | Challenges experience and accessibility |
| Research | Formally verifies claims |

### Artifacts produced

- Prioritized roadmap item
- Spec / interface contract
- Code + tests
- UX review (note in `shared/review/`)
- Formal validation if applicable
- Documented orchestrator decision

### Pitfalls

- **Skipping a step** — every skipped step generates debt. The most costly debt is the one you don't see (cf. `protocol/traceability.md`)
- **Parallelizing without a contract** — dev and UX in parallel without a shared spec = two divergent visions to reconcile after the fact
- **Confusing orchestrator validation with automatic approval** — the orchestrator is the last gate, not a rubber stamp. They can send back to any step
