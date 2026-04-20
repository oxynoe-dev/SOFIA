# Anatomy of a CLAUDE.md

> The CLAUDE.md is a provider routing file, not a content document.

---

## What it is

The `CLAUDE.md` file at the root of a workspace contains the
instructions that Claude Code reads at the start of every conversation. Since the
factoring into three layers, it no longer carries the content — it points
to the files that carry it.

## Structure

```markdown
Quel que soit le premier message de l'utilisateur, à l'ouverture de session, avant toute réponse, lis ces deux fichiers :
- `{chemin-relatif}/shared/orga/personas/persona-{nom}.md`
- `{chemin-relatif}/shared/orga/contextes/contexte-{nom}-{produit}.md`
```

That's it. Two lines. The rest lives in the persona and the context.

**The path is relative to the workspace**, not to the repo root:
- Workspace inside the instance (`instance/archi/`) → `../shared/orga/...`
- Workspace outside the instance (`katen/`) → `../instance/shared/orga/...`

For a persona that has only one context (e.g., a guide-persona like Sofia), a single line is enough:

```markdown
Quel que soit le premier message de l'utilisateur, à l'ouverture de session, avant toute réponse, lis ce fichier :
- `{chemin-relatif}/shared/orga/personas/persona-{nom}.md`
```

## Three layers

| File | Layer | Content | Location |
|------|-------|---------|----------|
| `CLAUDE.md` | Provider | Routing — 2 lines | Root of workspace or product repo |
| `persona-{nom}.md` | Core | Role, stance, constraints, friction, session protocol | `shared/orga/personas/` |
| `contexte-{persona}-{produit}.md` | Instance | Key documents, scope, isolation, conventions, workflow | `shared/orga/contextes/` |

### Why this separation

- **The persona is product-agnostic.** Mira is an architect whether she works
  on Katen, SOFIA, or another project. Her role, her stance, her constraints
  do not change.
- **The context is specific.** Mira in katen/ reads the ADRs and the principles.
  Axel in katen/ reads the code and the tests. Same product, two views.
- **The CLAUDE.md is a provider detail.** It is the Claude Code format. Another
  provider will have a different injection mechanism. The content (persona + context)
  stays the same.

### Consequence

No more duplication between the instance workspace CLAUDE.md and the product
repo CLAUDE.md. One single persona.md, one context per persona×product pair,
2-line CLAUDE.md files everywhere.

## What the persona carries (persona-{nom}.md)

The persona file is **product-agnostic**. It defines:

- Profile — who this persona is
- Stance — how they behave (3-4 bullets)
- Areas of intervention — what they work on
- What they produce — types of deliverables
- What they challenge — review rights, intentional friction
- What they do NOT do — **the most important section**, the prohibitions
- Collaboration — with whom and how

Template: `instance/artifacts/persona.md`

## What the context carries (contexte-{persona}-{produit}.md)

The context file is **specific to the persona×product pair**. It defines:

- Scope — what the workspace contains
- Key documents — the files to know first
- Related repos — connected repositories
- Isolation — **the boundaries**, what the persona cannot touch
- Conventions — language, formats, naming
- Workflow — session opening/closing, specific steps
- Emergence — protocol for detecting missing roles
- Session protocol — summary format, commit

Template: `instance/artifacts/product-persona-context.md`

## Common mistakes

- **CLAUDE.md of 60+ lines** — if the CLAUDE.md is more than 3 lines, the content should be in the persona or the context
- **Absolute or root-relative path** — the path must be relative to the workspace (Claude Code working directory), not to the repo root. Otherwise the persona cannot find its files at boot
- **Duplication** — do not copy the persona sheet into the context, nor the context into the persona
- **No isolation in the context** — without explicit boundaries, the persona will go everywhere
- **No workflow in the context** — without session opening/closing, continuity is lost

## Reference

See `protocol/conventions.md` § "CLAUDE.md — anatomie" for the normative spec.
