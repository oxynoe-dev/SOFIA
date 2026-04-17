## Dev Spec-First

![Workflow — Dev spec-first](../../doc/figures/fig-workflow-dev.svg)

Development workflow: never code without a validated target.

---

### When to use it

For every feature, fix, or refactoring that touches product code. Applies as soon as an item is prioritized by the orchestrator.

### Steps

1. **The orchestrator prioritizes** — the item exists in the roadmap with an explicit owner
2. **Architect specifies** — interface contract, constraints, ADR if structural decision (cf. `protocol/exchange.md` for formats). The spec is the contract: it defines the what, not the how
3. **Dev plans in plan mode** — feature-by-feature decomposition, each step confronted with principles and existing ADRs
4. **Tests first (TDD)** — write tests before code, by layer: engine/operators = strict TDD, CLI/UI = tests after implementation
5. **Code** — implement following module responsibilities and project conventions
6. **Architecture review** — the architect verifies consistency with the spec and principles. Gaps documented, not ignored
7. **Commit** — the dev prepares the message, the orchestrator executes

### Roles involved

| Persona | Role |
|---------|------|
| Orchestrator | Prioritizes, arbitrates, commits |
| Architect | Specifies the contract, post-implementation review |
| Dev | Plans, tests, codes |

### Artifacts produced

- Spec or interface contract (in the architect's workspace)
- ADR if structural decision (cf. `decision-adr.md`)
- Unit / integration tests
- Code + commit

### Pitfalls

- **Coding before the spec** — "I know what needs to be done" leads to avoidable refactoring. The spec forces laying out constraints before touching code
- **Confusing plan and spec** — a plan decomposes steps, a spec defines a contract. A plan without a spec produces code without a target
- **Skipping the architecture review** — the review is not a formality. It detects gaps between spec and implementation before they propagate
