# Pitfalls and classic mistakes

> What doesn't work, so you don't have to find out yourself.

---

## 1. Too many personas too early

You don't need 5 personas on day 1. Start with 1. Calibrate it.
Add the second when the need is clear.

**Sign**: you have personas you never use.
**Solution**: delete unused personas. No regrets.

## 2. The compliant persona

A persona that always says yes is useless. It's an assistant with
a first name.

**Sign**: the persona never says "no", "that's not my role", or
"the spec is too vague".
**Solution**: strengthen the constraints in the persona sheet and the CLAUDE.md.

## 3. Forgetting session summaries

The next session has no context without a summary. You'll waste time
re-explaining, or worse, the persona will head in a direction
inconsistent with the previous session.

**Sign**: you start each session with 10 minutes of explanation.
**Solution**: the summary is mandatory in the CLAUDE.md. Not optional.

## 4. Soft isolation

A CLAUDE.md without an Isolation section is a broken CLAUDE.md.
The persona will read and write everywhere, and friction disappears.

**Sign**: the architect modifies code, the dev rewrites specs.
**Solution**: add explicit boundaries. "Never read/write outside of X."

## 5. The orchestrator who doesn't decide

Personas expose tensions. If the orchestrator doesn't decide, tensions
accumulate and nothing moves forward.

**Sign**: the same open questions come back session after session.
**Solution**: decide. Even if it's imperfect. An "Accepted" ADR is
better than an eternally "Proposed" ADR.

## 6. Confusing persona and assistant

A persona is not a politer assistant. It's a role with constraints
that force it to think differently. If you remove the constraints,
you're back to a generalist assistant.

**Sign**: you give the same instructions to all your personas.
**Solution**: each persona has a posture, constraints, and scope
that are **different**. The difference is what creates value.

## 7. The lost session

Claude Code can crash. The app can freeze. Context can get corrupted.
It will happen.

**Sign**: you've lost a week of work.
**Solution**: files are the only source of truth. Produce artifacts
(ADRs, specs, reviews) continuously. The session summary is the bare
minimum. Files survive crashes.

## 8. The dev who never flushes

The developer persona is different from the others. They code, they're
in the flow, they have a long-running session going continuously.
Stopping for a session summary breaks the rhythm.

Result: no summary, no trace of intermediate decisions. The code is in
git, but the **why** behind implementation choices disappears if the
session crashes.

**Sign**: your dev session never closes and has no summary.
**No silver bullet** — it's a trade-off. A few approaches:
- Ask the dev to flush a quick summary at natural breakpoints
  (end of a feature, before a refactoring)
- Accept that the commit message and the code **are** the dev's trace
- Compensate with more frequent reviews from other personas

"Thinking" personas (architect, strategist, researcher) have short
sessions with file deliverables. The "doing" persona has a long session
with code deliverables. It's not the same rhythm and that's fine — but
you need to know it.

## 9. Copying personas from another project

Katen personas are calibrated for Katen. If you copy them without
adapting, they won't match your project or your way of working.

**Sign**: the persona talks about Petri nets when you're building
a mobile app.
**Solution**: use the examples as **structural reference**, not as
content. The SOFIA guide is there to help you design your own.

## 10. The shared blind spot

All personas are calibrated by the same orchestrator. Their implicit
biases become the biases of the entire team. Friction is real — but
it plays within a thinking space bounded by what the orchestrator knows
they don't know. What they don't know they don't know, no persona will
surface.

**Sign**: all personas converge quickly, nobody questions the premises.
**No simple solution** — this is the structural limit of a single-orchestrator
system. An outside perspective (human peer, user, meta persona outside
the flow) is the only compensation mechanism.

## 11. Signal overproduction

A well-functioning method generates more material than the orchestrator
can absorb. Notes, reviews, sessions, artifacts accumulate. The product
(tight scope) stays under control. Explorations pile up without being
sorted or qualified.

**Sign**: unread notes accumulate, sessions go without follow-up,
the orchestrator skims instead of reading.
**Solution**: archive regularly, distinguish signal from noise, accept
that not everything will be processed. Overproduction is a sign of
system health — provided you govern it.

## 12. Framework ossification

Conventions, constraints, scopes freeze. What was a contextual decision
becomes dogma. Personas apply rules that no longer have a reason to exist
because the context changed but nobody flagged it.

**Sign**: a constraint nobody can justify, a convention everyone works
around, a persona whose scope no longer matches their actual deliverables.
**Solution**: recalibrate periodically. Revisit the constraints — they're
the most powerful calibration lever. A soft persona is a persona whose
constraints have eroded.

## 13. The orchestrator bottleneck

SOFIA relies on a single control point — the orchestrator. That's its
strength (coherence, arbitration, big picture) and its structural limit.
Everything goes through one person: reading, filtering, contextualizing,
transmitting, arbitrating, verifying.

Intentional friction has a cost, borne by a single person. The question
isn't how to eliminate it — it's how to make it sustainable.

**Sign**: the orchestrator approves without reading, sessions become
mechanical, decisions are deferred.
**Approaches**: reduce the number of active personas, space out sessions,
prioritize friction circuits that produce value, accept that some flows
run in degraded mode.
