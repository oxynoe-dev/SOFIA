# Persistent memory

> Memory is a supplement to files, not a replacement.

---

## What it is

Claude Code offers a persistent memory system (`MEMORY.md` +
memory files) that survives between conversations. The persona
can store information useful for future sessions.

## Memory types

| Type | Content | Example |
|------|---------|---------|
| **user** | User profile — role, preferences, knowledge | "Go expert, new to React" |
| **feedback** | User corrections and validations | "Don't mock the DB in tests" |
| **project** | Project context not derivable from code | "Merge freeze Thursday for mobile release" |
| **reference** | Pointers to external resources | "Bugs tracked in Linear project INGEST" |

## What to store, what not to

### Store

- What the user prefers and why
- Corrections received (to avoid repeating the same mistake)
- Project context that is not in the code
- Links to external resources

### Do NOT store

- Code patterns, conventions, architecture → readable in the code
- Git history → `git log` is the source of truth
- Debug solutions → the fix is in the code
- What is in the CLAUDE.md → already loaded at each session
- Details of the current session → that is a session summary, not a memory

## Structure

```
.claude/projects/{projet}/memory/
├── MEMORY.md                 ← index (pointers, not content)
├── user_profile.md           ← user profile
├── feedback_testing.md       ← feedback on tests
├── project_deadline.md       ← project context
└── reference_monitoring.md   ← link to dashboard
```

`MEMORY.md` is an index — it contains links to memory files,
not the content itself. Keep it short (< 200 lines).

## Memory vs session summary

| | Memory | Session summary |
|---|--------|-----------------|
| **Lifespan** | Months | Days |
| **Scope** | Cross-session | One session |
| **Content** | What is durably true | What happened today |
| **Example** | "The user prefers a single PR for refactors" | "Created ADR-058, review deposited, 3 open items" |

Simple rule: if it is useful in 3 months, it is a memory.
If it is useful tomorrow, it is a session summary.
