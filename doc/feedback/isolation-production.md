# Field experience report — Production role isolation

> When personas start producing, boundaries shift.

---

## The problem

The SOFIA method documents thinking role isolation well: the architect
doesn't code, the strategist doesn't touch code, the dev doesn't decide
on architecture. These constraints create productive friction.

But when personas move from thinking to **production** — writing a white
paper, generating a PDF, publishing on social media — scope boundaries
become blurry. Who publishes what on which channel? Who maintains the
build scripts? Who validates before release?

## What we observed

On Katen, publication scripts were scattered across individual workspaces:
`maturation/bin/publish-*.py` under Winston,
`graphisme/tools/build_pptx.py` under Sofia. Result:

- The architect couldn't audit scripts without leaving their scope
- The dev couldn't check code quality
- Nobody had an overview of the publication chain

## The solution

Two decisions:

**1. Separate thinking and production in roles.** A persona who thinks
AND produces the final deliverable is judge and jury. Friction disappears.
On Katen: Sofia produces (all channels), Nora challenges (UX,
accessibility). The one who decides the form is the one who delivers it.
The one who challenges doesn't produce.

**2. Centralize scripts in `shared/tools/`.** Each persona triggers
their scripts, but the code lives in a space visible to all. The
architect audits coherence, the dev audits quality, UX audits the output.

## For your project

When your personas start producing public deliverables:
- Ask "who publishes what on which channel" explicitly
- Separate the producer from the challenger — the one who writes is not
  the one who validates
- Put publication scripts in a space readable by all
- The orchestrator validates before any release (method duty 3)

Thinking isolation is in the persona sheets. Production isolation is in
the publication conventions. Both are necessary.

## Multi-format — when a deliverable exists on multiple channels

The problem worsens when the same content must exist in markdown, PDF,
HTML, and social media visuals. The question is no longer just "who
publishes" but "who owns which transformation".

### What we observed

Without a clear contract on channels, tasks fall through the cracks:
- The writer modifies the markdown, nobody rebuilds the PDF
- The graphic designer produces visuals, nobody integrates them into the site
- The build script exists but nobody knows who triggers it

### The rule

**One channel = one owner.** The persona who produces the deliverable
for a given channel is responsible for triggering, coherence, and
updates. Others challenge via review — they don't produce.

| Channel | Owner | Challengers |
|---------|-------|-------------|
| Markdown source | Writer | Architect (structure), Researcher (sources) |
| Generated PDF/HTML | Graphic designer | UX (accessibility), Writer (content) |
| Social media visuals | Graphic designer | Strategist (message), UX (readability) |
| Website | Dev or Graphic designer | UX (user journey), Architect (coherence) |

The orchestrator validates before any release — regardless of channel.
