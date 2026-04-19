# Friction

> Qualify positions, don't count them.

---

## Definition

Friction is a position taken by a participant (persona or orchestrator) on the other's proposition. It qualifies the nature of an agreement or disagreement.

Friction is a productive mechanism, not a defect. See `core/model.md` for why.

## Dimensions

| Dimension | Values | Required |
|-----------|--------|----------|
| **exchange** | Reference to the exchange (session or artefact) that generated the friction | MUST |
| **emitter** | Persona or orchestrator emitting the position | MUST |
| **marker** | `[sound]`, `[contestable]`, `[simplification]`, `[blind_spot]`, `[refuted]` | MUST |
| **description** | Short summary of the position | MUST |
| **initiative** | `[persona]` or `[PO]` — who initiated the friction subject | MUST |
| **resolution** | `ratified`, `contested`, `revised`, `rejected` — epistemic resolution gesture | SHOULD |
| **antecedent** | Reference to a prior friction in the lineage | MUST (if lineage) |

**Scope**: a friction is attached to an exchange, itself attached to a space within an instance.

## Markers

5 epistemic positions. These are positions, not an intensity scale. The set is closed — an instance MUST NOT add markers.

| Marker | Meaning |
|--------|---------|
| `[sound]` | Corroboration — well-founded position |
| `[contestable]` | Underdetermination — defensible but not the only reading |
| `[simplification]` | Reductionism — reality is more complex |
| `[blind_spot]` | Incompleteness — missing data |
| `[refuted]` | Refutation — factually incorrect or logically incoherent |

Markers MUST be expressed as bracketed keywords.

> **FR retrocompat.** The parser also accepts FR identifiers (juste, angle-mort, faux, ratifie, conteste, revise, rejete).

> **Theoretical note.** These 5 positions are compatible (without strict equivalence) with Toulmin's argumentation model (1958): `[sound]` ≈ absence of rebuttal, `[contestable]` ≈ qualifier challenge, `[simplification]` ≈ warrant challenge, `[blind_spot]` ≈ data challenge, `[refuted]` ≈ claim refutation. This is an illumination, not a protocol constraint.

## Resolution

4 epistemic gestures. Each friction SHOULD carry a resolution tag qualifying what happened after qualification — not the content, but the outcome.

| Tag | Meaning |
|-----|---------|
| `ratified` | Agreement — the position is accepted by the other party |
| `contested` | Sustained disagreement — no change of position |
| `revised` | Disagreement with a change of position by one party |
| `rejected` | Terminal disagreement — the position is dismissed |

The set is closed — an instance MUST NOT add resolution tags.

The resolution tag is set by the summary author (persona for sessions, emitter for artefacts). It reflects the author's perception of the outcome, not an objective verdict. The orchestrator MAY correct.

### Inter-session mutability and lineage

A resolution can evolve in a later session (`contested` → `revised`, `rejected` → `ratified`, etc.). The session trace remains an immutable historical document — the new session carries the revision.

When a friction amends a prior resolution, it MUST carry a `ref:` field pointing to the original friction:

```
ref: <session-id>/<friction-id>
```

> **Example**:
>
> ```
> - [sound] the protocol/observational distinction covers the case — [aurele] → ratified (ref: 2026-04-10-1430-aurele/3)
> ```

The `ref:` creates a **lineage**: a chain of linked frictions (initial position → contestation → resolution). A chain constitutes a single logical friction. The current resolution is that of the last link.

**Lineage rules**:

1. A chain of frictions linked by `ref:` = one logical friction, not N independent frictions.
2. The current resolution is that of the last link in the chain.
3. A friction is **open** if it has no resolution AND no subsequent friction resolves it via `ref:`.

This mutability is consistent with the defeasible nature of plausible reasoning (Rescher 1976): what is ratified today can be contested tomorrow with new data.

> **Theoretical note.** These 4 gestures are inspired by the PXP protocol (Mestha et al. 2025 — RATIFY, REFUTE, REVISE, REJECT). PXP qualifies gestures in a multi-turn human-LLM exchange. H2A applies them to friction resolution, not to individual messages. This is an illumination, not a protocol constraint.

## Format

Each friction line MUST carry:
1. The marker in brackets
2. A short description
3. An initiative tag: `[persona]` or `[PO]`
4. A resolution tag (SHOULD): `→ ratified`, `→ contested`, `→ revised`, `→ rejected`

> **Example** (Markdown implementation, see `implementation/implementation.md`):
>
> ```
> ## Orchestrator friction
> - [contestable] the Toulmin mapping is suggestive, not established — [PO] → revised
> - [blind_spot] scaffolding absent from the Böckeler review — [aurele] → ratified
> ```

## Interpretation

| Signal | Reading |
|--------|---------|
| Only `[sound]` | Friction absent — warning signal. The persona may be in validation mode rather than collaboration. |
| Mix of `[sound]` / `[contestable]` / `[simplification]` | Healthy friction — diverse positions, productive collaboration. |
| Presence of `[blind_spot]` or `[refuted]` | Tension to address — the orchestrator SHOULD arbitrate explicitly. |
| Only `ratified` | Resolution without tension — not necessarily problematic, but worth monitoring. |
| No resolution on N frictions | Frictions raised but unresolved — items to address or defer to Open. |
| High `contested`/`rejected` ratio | Persistent divergences — the orchestrator SHOULD investigate. |

## Layer

Friction is **observational**. Qualifying a position (resistance vs correction, blind spot vs omission) requires semantic judgment. The persona pre-fills, the orchestrator validates.

The audit MAY verify the presence of the section and marker compliance (computational), but not the correctness of qualifications (inferential).

## reportPattern()

Meta-operation on friction. Mitigation of the orchestrator's residual opacity (invariant 5, see `h2a.md`).

### Problem

Faced with repeated friction rejection, three hypotheses are phenomenologically identical from the inside: persona error (LLM bias), legitimate orchestrator conviction, unconscious resistance. The orchestrator cannot arbitrate their own resistance to friction. This problem is unsolvable in the strict sense (applied version of the Münchhausen Trilemma), but mitigable.

### Trigger

The persona detects a **thematic convergence of rejections** — N rejections bearing on the same axis, the same hypothesis, the same unexamined presupposition. Detection is observational: the persona analyzes, not a mechanical count.

### Mechanism

**Step 1 — Factual observation.** The persona signals the pattern without judgment. Purely descriptive, verifiable.

**Step 2 — Three argued hypotheses.** The persona argues each:

- **LLM error**: why the frictions might be miscalibrated (repetitive pattern, lack of context, possible hallucination)
- **Legitimate conviction**: why the orchestrator's position might be correct despite objections (coherence reconstruction)
- **Resistance**: why the orchestrator might have a blind spot (what systematic rejection protects, what it costs to consider)

The persona does not decide — compatible with the "human arbiter" invariant.

**Step 3 — Mandatory qualification.** The orchestrator MUST qualify their response by articulating why they choose the hypothesis they choose. This justification is traced.

### Safeguards

**Asymmetric burden of proof.** If the orchestrator chooses "LLM error" → low burden (show why the friction is unfounded). If the orchestrator chooses "conviction" → high burden (steelman the adverse position and explain why it falls short).

**Visible counter.** The distribution of hypothesis choices is maintained and made visible. This counter belongs to the protocol layer (computational, verifiable).

### Layer

Thematic convergence detection belongs to the **observational** layer. The choice counter belongs to the **protocol** layer.

---

## Rendering

Keyword markers and resolution tags are the protocol format. Implementations MUST render them legibly. See `implementation/implementation.md` for Markdown rendering.
