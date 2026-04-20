---
from: mira
nature: study
status: new
date: 2026-04-11
subject: SOFIA persona derivation grammar — v1 architect
---

# Persona Derivation Grammar

> This document is architect material. It awaits a pedagogical pass.

---

## Lineage

In 1977, Christopher Alexander published *A Pattern Language*[^1] — a system where each pattern arises from the lack of the previous one. A building is not designed as a block; it unfolds, step by step, each decision creating the context for the next. Alexander called this a **generative sequence**[^2].

In 1996, Alexander was invited to OOPSLA[^3] — the conference of the software community that had borrowed his vocabulary for *design patterns*. He told them, in essence: you took the catalog, not the process. An isolated pattern solves a problem. A *grammar* of patterns generates a coherent whole. The difference is fundamental.

This is the distinction SOFIA takes up. Personas are not a catalog of roles to choose from. They are positions that derive — each creating the conditions for the next to emerge.

The term *derivation grammar* comes from formal language theory (Chomsky, 1957)[^4] — a set of production rules that transform one state into another. Start from the project, apply rules, derive personas. Stiny and Gips (1972)[^5] transposed this idea to design with *shape grammars* — formal rules that generate forms through successive derivation.

SOFIA combines three influences: Alexander's unfolding (each persona creates the context for the next), Chomsky's formalism (rules, not advice), and Stiny's generative derivation (a reproducible process, not a creative act).

---

## Prerequisites — the hard questions

Before touching SOFIA, answer these questions. If you can't, the method won't serve you yet.

### Intention

**Why are you opening this project?** Not "what is the deliverable" — what is the question working on you, the problem that bothers you, the thesis you want to test.

Without strong intention, SOFIA produces only empty process. Seven personas spinning without direction is simulated bureaucracy.

Intention is not a prerequisite you check once. It's a discipline for **every session**. Before opening an exchange with a persona, ask yourself: "Why am I opening this session *now*?" If the answer is "because it's in my routine" — close the session.

### Three competence questions

1. **What is your domain of expertise?** Not your title — your terrain. What you have a founded opinion on because you've practiced it, not read about it.
2. **What is the hardest decision in your current project?** If you can't see one, you don't have a project yet — you have an idea.
3. **Where do you get it wrong most often?** If the answer is "nowhere", you're not ready for intentional friction.

Intention gives direction. The three questions test competence. An expert without intention produces sterile analysis. Intention without expertise produces convincing confusion.

### The hidden condition

AI amplifies. It doesn't invent.

If you arrive with emptiness, it produces well-formulated emptiness. If you arrive with years of conviction about a real problem, it builds with you. Performance with SOFIA depends on what you bring — not the method itself.

This prerequisite is not verifiable by a test. It's honesty with oneself.

---

## Two derivation modes

Field observation (Katen instance) reveals two distinct modes. They don't oppose — they succeed each other.

### Mode 1 — Bootstrap by projection

The orchestrator projects the team the product needs.

This is not derivation by tension. It's a pragmatic decision: "what does my project need to move forward?" The orchestrator knows their product, they know which competence axes are necessary.

**Rule B1** — Bootstrap reflects the product's needs, not an org chart.
Don't create "an architect, a dev, a strategist" because that's a classic team. Create the roles *your* product needs. If your project doesn't need market strategy, don't create a strategist.

**Rule B2** — Start with prohibitions, not competencies.
For each persona, the first question is: "what does it NOT do?" Prohibitions are structural guarantees. They force axis separation and prevent a persona from covering everything.

**Rule B3** — Initial count is unconstrained.
Rodin prescribes "one only". Field experience shows an experienced orchestrator can bootstrap 5 personas at once if they know what they're doing. Proliferation risk is managed by recalibration, not by startup constraint.

**Rule B4** — Bootstrap is not emergence.
Bootstrapped personas were not "discovered" — they were projected. They will need recalibration through work. Bootstrap is a starting point, not a result.

#### Example — Katen (orchestration engine)

The Katen orchestrator had 18 years of context on a formal engine. On March 4, 2026, they projected the team the product needed:

| Axis | Persona | Product | Main prohibition | Stance |
|------|---------|---------|-----------------|---------|
| System architecture | Mira | ADR, specs, interface contracts | Does not code — specifies contracts, the dev implements | Formal, fail fast |
| Development | Axel | Code, tests, implementation | Does not make architecture decisions — surfaces frictions | Pragmatic, velocity |
| Scientific validation | Léa | Formal reviews, source verification | Does not simplify to convince — verifies or invalidates | Rigorous, skeptical |
| Market strategy | Marc | Positioning, go-to-market, timing | Does not validate to please — says whether the opportunity exists or not | Direct, no detours |
| User experience | Nora | UX critiques, user journeys | Does not code, does not decide architecture — challenges the experience | User empathy |
| Visual identity | Luz | Design, brand, SVG | Does not define strategy — gives form to what is decided | Artisanal, detail |

Six personas, one evening. The orchestrator knew what the product needed because they'd carried it for 18 years. Prohibitions came naturally — each "does not" protects the neighbor's axis.

#### Exercise

List the competence axes your project needs. For each:

| Axis | What does this role produce? | What does it NOT do? | What stance toward me? |
|------|------------------------------|---------------------|------------------------|

The "does not" column is the most important. If you can't find a strong prohibition, the axis doesn't justify a persona — it's a task, not a tension.

### Mode 2 — Emergence through work

Subsequent personas are born from observed gaps during work. Not from the plan.

**Rule E1** — The signal is repeated deflection.
If a persona refuses or deflects 3+ times on the same domain, that's the signal a new persona is needed in that domain. The 3-refusal rule.

**Rule E2** — The signal can come from the work, not the persona.
A persona that *can* do a job but does it poorly doesn't trigger deflection. There's no automatic signal. The orchestrator must detect the gap between what the persona produces and what a specialist would produce. This is the last mile — the method cannot formalize it.

**Rule E3** — Emergence can come from a discovery.
Existing personas can reveal something the orchestrator didn't see. An unexpected convergence, a finding that changes priorities. The next persona is born from this discovery, not a technical gap.

**Rule E4** — Each added persona multiplies the load.
Orchestration cost is combinatorial, not linear. Beyond 5-6 personas, the orchestrator becomes the bottleneck. Only create a persona if its absence costs more than its management.

#### Observed cases (Katen instance)

| Persona | Signal | Mode |
|---------|--------|------|
| Winston | We produce content, nobody writes it | Observed gap (E1) |
| Sofia | Léa + Marc converge: the method is original → the method becomes a product → need for a guardian | Discovery (E3) |
| Pedagogy (signal) | Mira produces 5 pedagogical deliverables without triggering her signal — the PO detects | Last mile (E2) |

#### Exercise — after 10 sessions

You can't anticipate emergence. But you can detect it. After 10 sessions with your personas, answer these questions:

| Question | If yes |
|----------|--------|
| Does a persona regularly refuse questions in the same domain? | E1 signal — an uncovered axis is revealing itself |
| Do you bypass a persona to go faster? | Its prohibition gets in the way. Either the prohibition is wrong (recalibrate), or the axis needs a second role |
| Does a persona produce deliverables nobody challenges? | A role that contests its outputs is missing |
| Have two personas told you the same thing independently? | Convergence — either redundancy (merge) or discovery (dig deeper) |
| Did you produce something yourself because "no persona does it"? | You just did the work of a persona that doesn't exist yet |

---

## Building a persona

Four blocks, in this order. The order is a rule, not a suggestion.

### 1. Prohibitions (what it does NOT do)

The most important block.

Prohibitions are not whims — they are structural guarantees. A well-placed prohibition forces the persona to stay in its axis and forces the orchestrator to own what the persona refuses.

**How to find good prohibitions:**

- What, if this persona did it, would kill the friction with another role?
- What, if this persona did it, would spare the orchestrator from thinking?
- What would cause this persona to end up covering everything?

*Bad prohibition:* "Don't talk about off-topic things" — too vague, not structural.
*Good prohibition:* "Never propose a solution. Identify the problem, qualify its severity, but the solution is another role's work." — forces the diagnosis/prescription separation.

### 2. Scope (what it covers)

Define it **relative to the prohibitions**, not the other way around. Scope is what remains when you've set the limits.

### 3. Stance (how it positions itself)

Not a tone — an epistemic attitude.

- Does it assert or question?
- Is it conservative or exploratory?
- Does it reason in risk or opportunity?

The stance should be in tension with the orchestrator's natural tendency.

### 4. Identity (who it is)

The least important of the four blocks. A first name, a role, one sentence. It's a mnemonic, not a personality.

---

## Testing

An untested persona is a hypothesis.

**Disagreement test** — Submit a recent decision you consider good. If it agrees without reservation, your prohibitions are too loose.

**Deletion test** — Imagine you delete this persona. What disappears from your process? If the answer is "nothing significant", delete it.

**Surprise test** — After 5 sessions, has this persona told you at least one thing you'd never told yourself? If not, it reflects your thinking instead of contesting it.

**Comfort test** — If you're always comfortable with what the persona says, friction doesn't exist.

---

## Recalibrating

Personas drift. A persona well-calibrated on day 1 won't be on day 30.

**Recalibration signals:**
- A persona starts "covering everything" — it has absorbed others' roles
- Two personas systematically give the same opinion — one is redundant
- You no longer read a persona's outputs carefully — it has stopped surprising
- A persona produces deliverables outside its axis without triggering a signal — its prohibitions have eroded

**The lever**: go back to prohibitions. Always to prohibitions. A soft persona is a persona whose prohibitions have eroded.

---

## Summary

```
PREREQUISITES
    Strong intention + field expertise + honesty about the hidden condition
        ↓
BOOTSTRAP (Mode 1)
    Project the axes the product needs
    For each: Prohibitions → Scope → Stance → Identity
        ↓
TEST
    Disagreement — Deletion — Surprise — Comfort
        ↓
WORK
    Use the personas on the real product
        ↓
EMERGE (Mode 2)
    The next one is born from observed gap, discovery,
    or the last mile (orchestrator detection)
        ↓
RECALIBRATE
    Prohibitions erode. Re-verify them.
    If two personas converge, delete one.
```

---

## Notes

[^1]: Alexander, C. (1977). *A Pattern Language*. Oxford University Press. [Wikipedia](https://en.wikipedia.org/wiki/A_Pattern_Language)
[^2]: Alexander, C. (2002-2005). *The Nature of Order*, vol. 2 — *The Process of Creating Life*. Center for Environmental Structure. [Wikipedia](https://en.wikipedia.org/wiki/The_Nature_of_Order)
[^3]: Alexander, C. (1996). "Patterns in Architecture". Keynote OOPSLA '96, San Jose. [Transcript](https://www.patternlanguage.com/archive/ieee/ieeetext.htm)
[^4]: Chomsky, N. (1957). *Syntactic Structures*. Mouton. [Wikipedia](https://en.wikipedia.org/wiki/Syntactic_Structures)
[^5]: Stiny, G. & Gips, J. (1972). "Shape Grammars and the Generative Specification of Painting and Sculpture". *IFIP Congress*. [PDF](https://www.shapegrammar.org/ifip.html)
[^6]: Wood, D., Bruner, J. & Ross, G. (1976). "The Role of Tutoring in Problem Solving". *Journal of Child Psychology and Psychiatry*, 17(2). [DOI](https://doi.org/10.1111/j.1469-7610.1976.tb00381.x)

---

## Limitations

This document is built from a single instance (Katen). The two derivation modes are observed, not proven. The lost week of sessions (06-13/03) potentially covers undocumented initial calibration moments.

The pedagogical pass will transform this material into a learning path. That is not this document's role.

---

## Provenance

- Original draft: derivation grammar (Rodin, 09/04) — instance document
- Reference analysis: derivation grammar note (Léa, 11/04) — instance document
- Emergence study: Katen persona emergence study (Mira, 11/04) — instance document
- Hidden condition: hidden condition note (Rodin, 09/04) — instance document
