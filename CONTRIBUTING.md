# Contributing to SOFIA

SOFIA is in **alpha**. Contributions are welcome — field feedback, corrections, pattern proposals.

Before contributing, read the user guide: [`doc/user-guide.md`](doc/user-guide.md).

## How to contribute

1. **Open an issue first** — bug, question, feature proposal. This allows discussion before coding.
2. **If relevant, propose a PR** — a validated issue can lead to a pull request.
3. **Field experience matters** — a friction report, a pattern that works, a limitation encountered: everything is useful.

## Repo structure

| Directory | Role | Stability |
|-----------|------|-----------|
| `core/` | Invariants (principles, model, friction, duties) | Stable — rare and deliberate changes |
| `protocol/` | Interface contract (H2A, exchange, friction, contribution) | Semi-stable — evolves with feedback |
| `provider/` | Concrete implementation (Claude Code today, others tomorrow) | Volatile — adapts to tools |
| `doc/` | Guides, workflows, patterns, feedback, architecture, ADR | Open to contributions |

## Conventions

- **Source language**: English.
- **File naming**: kebab-case, no accents in filenames. E.g., `getting-started.md`.
- **Format**: Markdown. No inline HTML unless necessary.

## Branches

- `main` — protected branch, no direct push.
- `feature/{subject}` — new feature or content.
- `fix/{subject}` — correction.

All contributions go through a PR against `main`.

## Commits

Messages in English, format:

```
{type}: {short description}
```

Types:
- `feat` — new content or feature
- `fix` — correction
- `doc` — documentation, guides, examples
- `refactor` — reorganization without meaning change

Examples:
```
feat: add inter-persona delegation pattern
fix: broken link in user guide
doc: clarify isolation protocol
refactor: move ADR to doc/adr/
```

## Pull requests

- One PR = one subject. Keep PRs focused.
- Describe context and motivation in the description.
- Review required before merge.
- If the PR touches `core/` or `protocol/`, explain why the invariant or contract needs to evolve.

## Code of conduct

- **Kindness** — we build together, we learn together.
- **Clarity** — no unnecessary jargon. If a term isn't obvious, explain it.
- **Honesty** — saying what doesn't work is as useful as saying what does.
- **Scope respect** — SOFIA is a method, not a software product. Contributions stay within this frame.

## License

SOFIA is under [MIT](LICENSE) license. All contributions are subject to the same license.
