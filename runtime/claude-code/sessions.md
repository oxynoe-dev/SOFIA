# Session summaries

> The next session will not have your context. The summary is its only memory.

---

## Why it is mandatory

Claude Code compresses older messages when the conversation
grows long. The context from the beginning of the session disappears. And between two
conversations, everything is lost except persistent memory.

The session summary is the **bridge** between conversations.
It is the first file the persona reads when opening a session.

## Format

**Name**: `{YYYY-MM-DD}-{HHmm}-{persona}.md`

**Content**:

```markdown
# Session {YYYY-MM-DD} ~{HH}h{mm} — {Persona}

## Produit
- `chemin/fichier.md` — créé : description courte
- `chemin/autre.md` — modifié : ce qui a changé

## Décisions
- **{Sujet}** — ce qui a été tranché

## Notes déposées
- `shared/review/review-xyz-persona.md`
- `shared/notes/note-dest-sujet-persona.md`

## Ouvert
Points en suspens, a reprendre en prochaine session.
```

## Rules

- **Always** — even if the session is short, even if "nothing structural"
- **No prose** — short lists, 30 lines max
- **Relative paths** — so it is readable out of context
- **One summary per session** — no cumulative summary

## Workflow

### Opening

1. Read the latest summary in `sessions/`
2. The orchestrator decides what to look at. No systematic recitation.

### Closing

1. Produce the summary in `sessions/`
2. **Instance** (`experiments/` or equivalent): auto commit
   - Format: `{persona}: {short summary} ({date})`
   - Scope: only files modified/created during the session
3. **Product repos** (code, method, etc.): prepare the commit message, the orchestrator executes

The persona does not need to be reminded — it is in its
CLAUDE.md. If you notice it forgets, reinforce the instruction.

## Statuses

Roadmaps use 5 normalized statuses:

| Status | Meaning |
|--------|---------|
| `[done]` | Completed |
| `[running]` | In progress |
| `[ready]` | Ready to start |
| `[todo]` | To do |
| `[blocked]` | Blocked — reason after `⊘` |

Example: `- [blocked] Naming 3e mode ⊘ décision orchestrateur — 3 options ouvertes`

The `↔` marker signals a cross-voice convergence (the topic concerns multiple personas).
