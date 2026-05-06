## Consultation by spawn

When a persona in session needs an expert opinion outside their scope, they propose a consultation. The orchestrator authorizes, a short one-shot sub-agent of the recipient persona is spawned, and the orchestrator arbitrates the reply afterwards.

### Structure

1. The emitter persona, mid-session, identifies a need for expert input outside their direct field (e.g., archi → R&D, dev → archi, archi → terrain).
2. They deposit a consultation note in `shared/notes/` (`nature: question`) framing the question concretely.
3. They signal to the orchestrator that a consultation is needed. They do **not** spawn before authorization.
4. The orchestrator reads the note, decides whether the consultation is warranted, and authorizes (or declines) verbally.
5. Once authorized, the emitter persona spawns the recipient sub-agent with the minimal context: recipient persona file, recipient context file, and the consultation note. No emitter session history, no other artifacts.
6. The sub-agent produces a reply note (`nature: response`, `ref:` to the consultation note) and a short session summary in its own space (with `-spawn` marker and `trigger:` field).
7. The orchestrator reads the reply, annotates each friction with its resolution tag, decides on follow-up actions.

The orchestrator remains the sole boundary-crosser — the proposal-authorization sequence preserves invariant 3 (Isolation). See `protocol/h2a.md` invariant 3 and `doc/adr/adr-015.md`.

### When to recognize it

- The orchestrator's arbitration on a question requires expertise outside their direct field.
- The expected input is short and self-contained — a full session of the recipient persona would be heavier than necessary.
- The emitter persona can frame the question concretely without needing the recipient's full context to be re-deployed.

If the input requires the recipient's deep judgment over time, prefer escalation by note (full session) — see `note-escalation.md`.

### Example

Aurele (architect, in session) drafts a new exchange mechanism. They need an R&D opinion: how does this position relative to the existing literature on multi-agent coordination? They deposit `note-solene-spawn-mechanism-aurele.md` (consultation question), signal the orchestrator. The orchestrator authorizes. A sub-agent Solene (researcher) is spawned, reads the persona file, context, and note, performs a targeted web check, and deposits `note-aurele-spawn-mechanism-solene.md` (reply with anchoring suggestion, two new risks identified, frictions on the framing) plus a short summary in `recherche/sessions/{date}-{HHmm}-solene-spawn.md`. The orchestrator reads, annotates each friction with its resolution, may add complementary actions in the reply note. Aurele resumes their session with the input.

### Distinction from escalation by note

| Axis | Escalation by note | Consultation by spawn |
|------|-------------------|----------------------|
| Recipient mode | Full session opened by the orchestrator | Short one-shot sub-agent spawned by the emitter under authorization |
| Initiative | Orchestrator routes after reading the note | Emitter proposes, orchestrator authorizes |
| Recipient context | Full persona context, prior sessions readable | Minimal — persona, context, consultation note only |
| Cost | Heavier (full boot + session arc) | Lighter (one-shot, minimal context) |
| When to prefer | Recipient's deep judgment needed over time | Short focused expert input |

Both remain valid. Choose based on the depth of input required.

### Constraints

- **Depth 1** — the recipient sub-agent MUST NOT propose another consultation. If further expertise is needed, signal it in the short summary's `Open` section.
- **Context minimal** — only persona, context, and consultation note. No emitter session history.
- **Web search authorized** — for external reference verification only. Relaxes the context-minimal rule for external sources.
- **Continuity line** — the short summary MUST contain a line in `## Open` instructing the recipient to read the arbitrated reply at the next real session.

### Risks

- **Emitter capture**: the emitter formulates the question; alternative framings are not visible to the recipient. The orchestrator MAY augment the consultation note before authorization.
- **Persona performativity**: a short-spawned persona may over-perform its persona compared to a long real session (cited references, displayed rigor). Comparative audit (post-tracking) should be considered.
- **Token cost asymmetry**: each spawn re-boots the recipient's persona context. At high consultation volume, the cumulative cost may exceed the gain. Apply the opportunity rule strictly.
- **Silent recursion**: depth-1 is prescriptive, not technically enforced. A non-compliant sub-agent could spawn further. The protocol documents this as a structural limitation (see `protocol/h2a.md`).

### Opportunity rule

Trigger the consultation only when the orchestrator's arbitration requires expertise **outside their direct field**. Typical cases: dev → archi, archi → R&D, archi → terrain. Consultations on subjects within the emitter's own field tend to add cost without changing the decision.
