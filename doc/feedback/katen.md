# Field experience report — Katen

> 7 personas, 210+ sessions, a real project.

---

## The project

[Katen](https://katen.run) is a formally verified orchestration engine
for Data & AI pipelines, based on Petri nets. Built in pure HTML/JS/SVG, zero dependencies.
Open source MIT. 18 years of reflection (2008-2026) — from the v1 C++/Qt
to v2 pure web.

## The team

| Persona | Role | Workspace |
|---------|------|-----------|
| **Mira** | System & solution architect | `experiments/architecture/` |
| **Axel** | Full stack developer | `katen/` (product repo) |
| **Léa** | Researcher & scientific validation | `experiments/recherche/` |
| **Nora** | Product Design & UX | `experiments/ux/` |
| **Marc** | Strategic advisor | `experiments/strategie/` |
| **Sofia** | Visual identity & Multi-format production | `experiments/graphisme/` |
| **Winston** | Writer & editorial distiller | `experiments/maturation/` |

One human (the orchestrator/project creator) arbitrates.

## What worked

### Friction produces better decisions

Mira challenging an Axel implementation. Léa flagging that a claim
doesn't hold up to the literature. Marc asking "who's going to pay
for this?". Sofia refusing a visual theme that looks good but doesn't
carry the project identity. These frictions prevented real mistakes.

### Isolation forces rigor

Mira doesn't code → she's forced to specify clearly. Axel doesn't
decide on architecture → he escalates frictions instead of working
around them. Sofia produces, Nora challenges — the one who decides
the form is the one who delivers it, the one who challenges doesn't
produce. The result: 62 ADRs, 24 architecture principles, usable specs.

### Sessions structure continuity

The session summary is the bridge between conversations. Without it,
each session starts from zero. With it, the persona picks up exactly
where they left off.

### Artifacts as protocol

Cross-reviews (Mira reviews an ADR, Léa reviews a public claim,
Nora challenges a Sofia deliverable) are more useful than any chat.
Writing forces clarity.

### The challenger pattern

One producer, N challengers with blocking rights on their axis.
Axel codes → Mira challenges architecture, Léa the invariants, Nora the UX.
Winston writes → Mira challenges structure, Léa the refs, Marc
the positioning. The orchestrator decides when a challenger blocks.

### The editorial chain

Winston writes, experts validate substance, Sofia produces format,
Nora challenges before publication, the orchestrator validates last. The
SOFIA blue book is the first complete product of this chain.

## What broke

### Lost session

A week of work (6-7 sessions) was lost following a Claude app crash.
Context was partially reconstructed from produced files, but untraced
intermediate decisions were lost.

**Lesson**: session summaries are not optional. Produced files are the
only source of truth that survives.

### Scope drift

Some personas occasionally overstepped their scope — the architect
starting to write pseudo-code, the strategist giving technical opinions.
Isolation in the CLAUDE.md works, but it must be actively maintained.

**Lesson**: the "What they don't do" section is the most important
in the persona sheet. Review it regularly. The "What they challenge"
section makes friction structural.

### Initial calibration too broad

The first personas were too generalist. It was by using them that we
narrowed them down — adding constraints, sharpening stance, reducing
scope. Defining by medium (spec, code, review, PDF) is more reliable
than by skill.

**Lesson**: the first draft is always too broad. Iterate.

### Factual contamination

~30 documents contained "15 years" instead of "18 years" for the
orchestrator's duration of reflection. The error came from the orchestrator himself,
propagated and stabilized by the AI. Detected by Léa during a targeted audit.

**Lesson**: the repo is not a source of truth for facts. Continuous
human verification — not at the end of the project.

### Blurry production boundaries

When personas started producing (not just specifying), scope boundaries
became blurry. Who publishes what on which channel? Resolved by
separating producer and challenger, and centralizing scripts in
`shared/tools/`.

**Lesson**: thinking isolation is in the persona sheets. Production
isolation is in the publication conventions. Both are necessary.
