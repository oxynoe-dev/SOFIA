# Persona Archetypes

> Starting points for persona design — not prescriptions. Adapt to your project.

Each archetype is a template with the 7 persona dimensions filled for a common role. Use them as inspiration when bootstrapping personas, not as rigid definitions.

| Archetype | Role | Key prohibition | File |
|-----------|------|-----------------|------|
| Architect | System architecture, specs, ADRs | Doesn't code | [persona-architect.md](persona-architect.md) |
| Designer | UI design, visual craft, design system | Doesn't code | [persona-designer.md](persona-designer.md) |
| Developer | Code, tests, implementation | Doesn't decide architecture | [persona-dev.md](persona-dev.md) |
| Meta-challenger | Anti-echo-chamber, challenges premises | No operational artifact, no memory | [persona-meta-challenger.md](persona-meta-challenger.md) |
| Method inspector | Method conformity, structural audit | Doesn't make product decisions | [persona-method-inspector.md](persona-method-inspector.md) |
| Researcher | Scientific validation, sourcing | Doesn't code | [persona-researcher.md](persona-researcher.md) |
| Strategist | Positioning, risk, messaging | Doesn't code | [persona-strategist.md](persona-strategist.md) |
| UX | User flows, behaviors, acceptance criteria | Doesn't code | [persona-ux.md](persona-ux.md) |
| Writer | Editorial distillation, long-form content | Doesn't decide architecture | [persona-writer.md](persona-writer.md) |

## How to use

1. Pick the archetype closest to your need
2. Copy the file into your instance (`shared/orga/personas/persona-{name}.md`)
3. Replace `{Name}` with your persona's name
4. **Adjust the prohibitions** — they must create tension with your other personas
5. Create the matching context file (`shared/orga/contextes/contexte-{name}-{product}.md`)

The prohibition column is the most important. If two personas have no prohibitions in tension, they won't produce useful friction.
