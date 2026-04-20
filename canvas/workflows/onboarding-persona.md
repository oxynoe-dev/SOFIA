## Persona Onboarding

![Workflow — Persona onboarding](../../doc/figures/fig-workflow-onboarding.svg)

New persona integration workflow: from observed gap to first productive session.

---

### When to use it

When a domain is not covered by existing personas and this gap generates recurring problems. This workflow is the process version — for the technical checklist, see `doc/onboarding.md`.

### Steps

1. **Gap observed** — a domain emerges that nobody covers, or two personas are in recurring tension on a subject. The gap is documented, not assumed
2. **Persona file definition** — `shared/orga/personas/persona-{name}.md`: role, stance, scope, prohibitions, preferred media. Prohibitions are more important than responsibilities: what the persona doesn't do defines them as much as what they do (cf. `core/principles.md`, isolation principle). Template: `instance/artifacts/persona.md`
3. **Context file definition** — `shared/orga/contextes/contexte-{name}-{product}.md`: key documents, workspace scope, isolation, conventions, workflow. One file per persona×product pair (a same persona can have multiple contexts). Template: `instance/artifacts/product-persona-context.md`
4. **Workspace creation** — `{workspace}/sessions/` + CLAUDE.md with 2 lines pointing to persona + context. The workspace follows instance conventions (cf. `protocol/conventions.md` § "CLAUDE.md — anatomy")
5. **Calibration** — first exchanges with the orchestrator and adjacent personas. Stance, vocabulary, and detail level adjustment. Calibration takes 2-3 sessions
6. **First productive session** — the persona produces a real artifact (review, note, spec) that is used by another persona. This is the validation criterion

### Roles involved

| Persona | Role |
|---------|------|
| Orchestrator | Validates the necessity, arbitrates the scope |
| Adjacent persona | Domain briefing, first exchanges |
| New persona | Produces their first real artifact |

### Artifacts produced

- Persona file — `shared/orga/personas/persona-{name}.md` (draw from archetypes in `instance/archetypes/` and format in `instance/artifacts/persona.md`)
- Context file — `shared/orga/contextes/contexte-{name}-{product}.md` (template: `instance/artifacts/product-persona-context.md`)
- CLAUDE.md — 2-line routing to persona + context
- Complete workspace (`{workspace}/sessions/`)
- Announcement note in `shared/notes/` to inform other personas
- First productive artifact (review, note, spec)

### Pitfalls

- **Creating by symmetry** — "we're missing a persona X to complete the team". A persona must prove its necessity through a real gap, not a theoretical symmetry
- **The catch-all persona** — if you can't say what it doesn't do, it's not calibrated. Prohibitions are the first quality test of a persona file
- **Skipping calibration** — an uncalibrated persona produces unusable artifacts. The first 2-3 sessions are an investment, not a waste of time
- **Forgetting the context file** — without context, the persona doesn't know their workspace. The persona knows who they are, the context tells them where they are
