# Field experience report — Factual contamination

> The repo is not a source of truth for facts. It never was.

---

## The problem

LLMs don't count, don't calculate durations, and favor internal
coherence over external truth. An approximate data point entered
once — sometimes by the orchestrator, sometimes hallucinated by the AI —
will be propagated into every document generated afterwards.

The larger the repo grows, the more invisible the error becomes. It
*looks like* coherence because each contaminated document reinforces
the others. The AI doesn't doubt a data point it finds in 10 repo files.
The fact that it wrote it in those 10 files itself doesn't enter its
reasoning.

## Real case — Katen

The orchestrator used "15 years" to describe his duration of reflection on the project.
It was an approximation — the real duration is 18 years (2008-2026).
The AI picked up the figure, propagated it across ~30 documents, and stabilized it.

Audit:
- ~30 active documents contained "14 years" or "15 years" instead of "18 years"
- ~12 documents dated the original concept "2010-2012" instead of "2008-2012"
- 2 files dated the arXiv "(2010)" instead of "(2011)"

The error came from the orchestrator himself. The AI amplified it and made it invisible.

## The mechanism

1. An approximate data point enters a session
2. The AI picks it up without checking, phrases it nicely, propagates it
3. Each contaminated document becomes a source for subsequent sessions
4. The error stabilizes — it looks correct because it's consistent
   with the other contaminated documents

This is a **mutual reinforcement effect**. The same phenomenon exists at
web scale (model collapse, Habsburg AI) — but at web scale, it's
irreversible. In a SOFIA repo, it's traceable and fixable. Provided the
orchestrator checks.

## What is vulnerable

- **Dates and durations** — LLMs don't calculate time spans
- **Numbers** — counters, metrics, quantities
- **Proper nouns** — spelling variations, wrong attributions
- **Bibliographic references** — years, authors, titles, usage context

## Three classes of sourcing errors

Contamination isn't limited to raw facts. Sources themselves can be
problematic in three ways:

**Class 1 — Assertion without source.** The text states something as
fact, no source supports it. The AI produced a plausible assertion
from its distribution, not from data.

**Class 2 — Source contradicts the assertion.** The source exists and
is cited — but it says something different from what the text claims.
The AI "summarized" with distortion, or confused two sources.

**Class 3 — Correct source, incoherent usage.** The source is correct
and faithfully cited — but it doesn't say what the usage context
requires. Example: citing a study on AI agents to justify human
behavior, without a caveat about the transfer.

Class 3 is the most dangerous: everything looks correct, the source
is verifiable, the summary is faithful. Only someone who understands
the usage context can detect the incoherence.

## Safeguards

### 1. Continuous factual verification

Not at the end of the project — continuously. Every session that handles
facts (dates, numbers, refs) should include a verification pass.
That's duty 1 of the method.

### 2. Decontamination passes

Targeted audits on the most sensitive data, at regular intervals. On
Katen, an audit identified ~55 occurrences across ~42 files in a single
session. It's doable — provided you plan for it.

### 3. Explicit source of truth

Critical project facts must be declared once, in a reference document,
and always verified against that source. Not against the repo — against
the source.

## For your project

This is not a flaw of the method. It's a property of the underlying
technology. Precision errors are normal — LLMs favor plausibility
over truth.

The orchestrator is the only safeguard. The method must state this
explicitly, and the orchestrator must integrate it as practice, not
as an abstract principle.

And it's one of the strongest arguments in favor of the SOFIA method:
in a world where the web contaminates itself irreversibly, a structured
repo with cross-reviews is one of the rare spaces where decontamination
remains possible.
