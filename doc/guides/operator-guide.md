# Orchestrator Guide

> The operations you perform as orchestrator — opening sessions, exchanging artifacts, qualifying friction.

These operations are constitutive of the SOFIA method. They are not optional features — each one structures the collaboration between you and your personas. Together, they form the H2A protocol ([Human-to-Assistant](../../protocol/h2a.md) — the coordination protocol specification). The implementation details live in [`binding/implementation.md`](../../binding/implementation.md).

---

## Overview

| Operation | Mode | Who triggers | Who produces |
|-----------|------|-------------|-------------|
| openSession() | manual | orchestrator | — |
| closeSession() | manual | orchestrator | persona (summary) |
| send() | manual | orchestrator | persona (artifact) |
| receive() | manual | orchestrator | — |
| markRead() | manual | orchestrator | — |
| markDone() | manual | orchestrator | — |
| qualifyFriction() | automatic | closure | persona (pre-fills), orchestrator (validates) |
| qualifyContribution() | automatic | closure | persona (pre-fills), orchestrator (validates) |
| reportPattern() | automatic | persona (detection) | persona (observation), orchestrator (qualification) |

**Golden rule**: the persona does nothing without orchestrator instruction, except closure sections (friction, flow) and reportPattern.

---

## 1. openSession()

**When**: the orchestrator wants to work with a persona.

**How**: open a terminal in the persona's workspace and launch the assistant (e.g., `claude` in the persona's directory). Say "hello" — the CLAUDE.md routes to the persona and context files, the persona loads its latest session summary and boots.

**Example**:
```
cd {instance}/{workspace}/
claude
> hello
```

The persona reads its CLAUDE.md, loads persona + context, reads the latest session summary, and is ready to work.

---

## 2. closeSession()

**When**: the orchestrator decides the session is over.

**How**: give an explicit verbal signal ("let's close", "we're done"). The persona produces a **new** summary file in `sessions/` with the protocol sections. If using git, the orchestrator executes the commit. Git is recommended for traceability but not required — the method works without it.

**The persona MUST NOT close on its own.**

**Signal**:
```
let's close
```

**The persona produces**:
```
sessions/2026-04-16-1430-mira.md
```

MUST sections: `## Produced`, `## Decisions`, `## Shared notes`, `## Open`.
SHOULD sections: `## Orchestrator friction`.
MAY sections: `## Flow`.

**Commit** (if using git):
```
mira: short session summary (2026-04-16)
```

---

## 3. send()

**When**: the orchestrator wants a persona to produce an artifact for another persona (or for the team).

**How**: instruct the persona with the type, recipient, and subject. The persona writes and deposits in the recipient's `shared/`. Cross-instance: the artifact goes to the recipient instance's `shared/`, not the emitter's.

**The persona MUST NOT send an artifact without instruction.**

**Examples** — always specify the type, recipient, and where to deposit:
```
write a note to emile about the pedagogical pass on the grammar — deposit in shared/notes/

review the architecture.md for garance — deposit in shared/review/

write the spec for the reorganization mode feature — deposit in shared/features/
```

The persona chooses the content. The orchestrator specifies the type, recipient, and location.

**Naming**:

| Type | Convention |
|------|-----------|
| Note | `note-{to}-{subject}-{from}.md` |
| Review | `review-{subject}-{from}.md` |
| Feature | `feature-{subject}.md` |

---

## 4. receive()

**When**: an artifact has been sent and must be presented to its recipient.

**How**: the orchestrator opens a session with the recipient and presents the artifact. They can filter, contextualize, or transmit only a part. The recipient MAY produce a response (`nature: response`, `ref:` to the source artifact).

**Example**:
```
[session with emile]
garance sent you a review of architecture.md.
Here are her points: shared/review/review-architecture-garance.md
Read and tell me what you think for your pedagogical pass.
```

The orchestrator is the router — they decide what to transmit, to whom, and with what context.

---

## 5. markRead()

**When**: the recipient persona has read an artifact (typically during receive()).

**How**: the orchestrator modifies the artifact's frontmatter on behalf of the recipient.

```yaml
status: read          # was: new
```

---

## 6. markDone()

**When**: the recipient persona has processed the artifact — produced a response, integrated the feedback, or acted on the request.

**How**: the orchestrator modifies the frontmatter then moves to `archives/`.

```yaml
status: done          # was: read
```

Then:
```
mv shared/notes/note-emile-pedagogy-aurele.md shared/notes/archives/
```

---

## 7. qualifyFriction()

**When**: at every session closure (automatic).

**How**: the persona pre-fills the `## Orchestrator friction` section with the session's qualified positions. The orchestrator validates or corrects.

5 markers (closed set):

| Marker | Meaning |
|--------|---------|
| `[sound]` | Well-founded position |
| `[contestable]` | Defensible but not the only reading |
| `[simplification]` | Reality is more complex |
| `[blind_spot]` | Missing data |
| `[refuted]` | Factually incorrect |

4 resolutions (SHOULD):

| Tag | Meaning |
|-----|---------|
| `ratified` | Agreement |
| `contested` | Sustained disagreement |
| `revised` | Change of position |
| `rejected` | Position dismissed |

**Example**:
```
## Orchestrator friction
- ✓ [sound] the Toulmin mapping illuminates without constraining — [PO] → ratified
- ◐ [blind_spot] SEO was not considered — [mira] → ratified
```

**Quick reading**:
- Only `[sound]` → friction absent — warning signal
- Mix of markers → healthy friction
- No resolution → unresolved frictions

---

## 8. qualifyContribution()

**When**: at every session closure (automatic, optional).

**How**: the persona pre-fills the `## Flow` section. The orchestrator validates or corrects.

| Direction | Who brings |
|-----------|-----------|
| `H` | The human (orchestrator) |
| `A` | The assistant (persona) |

| Type | Definition |
|------|-----------|
| `substance` | New information |
| `structure` | Organization, synthesis |
| `contestation` | Challenge, reframing |
| `decision` | Arbitration |

**Example**:
```
## Flow
- H:substance — visual identity brief
- A:structure — 3-axis brand proposal
- H:decision — we keep axis 2

H:2 (substance 1, decision 1) | A:1 (structure 1)
```

---

## 9. reportPattern()

**When**: the persona detects a thematic convergence of rejections (3+ rejected frictions on the same theme).

**How**: the persona challenges the orchestrator **during the session** (not at closure). The orchestrator MUST respond.

**3 steps**:

1. **Factual observation** — the persona signals the pattern without judgment
2. **3 argued hypotheses** — LLM error, legitimate conviction, unconscious resistance
3. **Mandatory qualification** — the orchestrator chooses and justifies

**Asymmetric burden of proof**: if the orchestrator chooses "LLM error" → low burden. If "conviction" → high burden (steelman the adverse position).

**At closure**, the persona records:
```
## reportPattern
- Theme: [theme] — N rejected frictions (sessions YYYY-MM-DD, ...)
- Choice: LLM error | conviction | resistance
- Justification: ...
```

The choice counter is auditable (protocol layer).

---

## Summary

| Operation | Mode | Who triggers | Who produces |
|-----------|------|-------------|-------------|
| openSession() | manual | orchestrator | — |
| closeSession() | manual | orchestrator | persona (summary) |
| send() | manual | orchestrator | persona (artifact) |
| receive() | manual | orchestrator | — |
| markRead() | manual | orchestrator | — |
| markDone() | manual | orchestrator | — |
| qualifyFriction() | automatic | closure | persona (pre-fills), orchestrator (validates) |
| qualifyContribution() | automatic | closure | persona (pre-fills), orchestrator (validates) |
| reportPattern() | automatic | persona (detection) | persona (observation), orchestrator (qualification) |

**Golden rule**: the persona does nothing without orchestrator instruction, except closure sections (friction, flux) and reportPattern.
