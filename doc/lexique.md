# Glossary — template

> Shared glossary of project terms.

---

## Why a glossary?

When 7 personas work on the same project, words drift.
"Composition" can mean a .kc file, a CVM concept, or a
reusable pattern depending on who's talking.

The glossary fixes terms. Every persona reads it, nobody reinvents.

## Format

```markdown
## {Term}

**Definition**: {one sentence}
**Context**: {where this term is used}
**Not to be confused with**: {related terms}
**Decided on**: {date} — {ADR or session reference}
```

## Conventions

- One term = one entry. No synonyms in the same entry.
- If a term changed meaning (rename, evolution), document the history.
- The orchestrator arbitrates definition conflicts.
- The glossary lives in `shared/orga/lexique.md` at the instance level.

## Example

```markdown
## Kata

**Definition**: a Katen composition — an executable visual program.
**Context**: .kc files, user documentation, UI.
**Not to be confused with**: "composition" (internal CVM concept), "pattern" (reusable template).
**Decided on**: 2026-03-22 — ADR-054.
```
