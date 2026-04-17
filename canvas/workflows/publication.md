## Publication

![Workflow — Publication](../../doc/figures/fig-workflow-publication.svg)

Publication workflow: from writing to going live.

---

### When to use it

For any published content — web page, public document, white/blue book, external communication. Applies as soon as content leaves the internal scope.

### Steps

1. **Writing** — the writer or expert produces the raw content. Substance takes priority over form at this stage
2. **Substance validation** — concerned experts validate each on their axis (technical, strategic, formal). Each axis produces a review
3. **Formatting** — the producer (designer, integrator) formats. Structure and style follow the target medium's conventions
4. **UX / accessibility challenge** — UX verifies readability, navigation, accessibility. The content must work for the target audience
5. **Orchestrator go** — last gate. The orchestrator verifies factual integrity: what is published is true, sources are correct, positioning is right
6. **Going live** — effective deployment. The orchestrator executes or authorizes

### Roles involved

| Persona | Role |
|---------|------|
| Writer / Expert | Produces the content |
| Experts (architect, research, strategy) | Validate on their axis |
| Designer / Producer | Formatting |
| UX | Challenges accessibility and readability |
| Orchestrator | Last gate — factual integrity, go/no-go |

### Artifacts produced

- Draft (in the writer's workspace)
- Reviews by axis (in `shared/review/`)
- Formatted content (in the target medium)
- Orchestrator validation (implicit: the go is the commit/deployment)

### Pitfalls

- **Publishing without substance validation** — formatting gives an illusion of quality. A well-presented but factually wrong document is worse than a correct draft
- **The orchestrator validates form, not substance** — the orchestrator's role at the last gate is specifically factual integrity. Form was validated before
- **Unverified sources** — a reference cited without having been fully read propagates errors in everything that cites it afterwards (cf. `recherche.md`)
