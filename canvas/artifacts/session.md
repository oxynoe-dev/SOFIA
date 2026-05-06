---
binding: filesystem
---

# Session {YYYY-MM-DD} ~{HH}h{mm} — {Persona}

## Produced
- `{path/file}` — created: {short description}
- `{path/file}` — modified: {what changed}

## Decisions
- **{Subject}** — {what was decided}

## Notes deposited
- `shared/review/{file}`
- `shared/notes/{file}`

## Open
- **{Subject}** — {what remains to be handled}

---

## Spawn variant

When a recipient persona is spawned for a one-shot consultation (see `protocol/exchange.md` §Consultation, `canvas/workflows/consultation.md`), the short summary uses this lighter format. Filename carries a `-spawn` marker.

**Path**: `{recipient-space}/sessions/{YYYY-MM-DD}-{HHmm}-{persona}-spawn.md`

```yaml
---
persona: {recipient}
date: {YYYY-MM-DD}
session: "{HHmm}-spawn"
trigger: {consultation-note-id}
---
```

The `trigger:` field is mandatory — it points to the consultation note that initiated the spawn (filename without extension).

```markdown
# Spawn {YYYY-MM-DD} ~{HH}h{mm} — {Persona}

## Produced
- `shared/notes/{reply-note}` — reply to `{consultation-note-id}`

## Friction
- ref: deposited note (or "none")

## Open
- {pending items}
- **To revisit at next real session**: read arbitrations + complementary actions in `shared/notes/{reply-note}` (note may or may not be arbitrated yet — verify state)
```

The last line in `## Open` is mandatory. Without it, the recipient persona cannot see — at next real-session boot — that a spawn happened and that the arbitrated reply must be consulted. Continuity is broken otherwise.

Sections `## Decisions` and `## Notes deposited` are typically not needed in a spawn summary (the only decision is the reply itself, captured under `## Produced`). They MAY be added if the consultation triggered side-effects worth tracing.
