---
from: winston
to: sofia, nora
nature: content
date: 2026-04-05
subject: History of the SOFIA method — site sub-page
source: livre-bleu-voix.md, doc/winston-style.md, orchestrator framing
---

# History

[Olivier Cugnon de Sévricourt](https://www.linkedin.com/in/oliviercds/) — trained as an engineer (ESIEE Paris 2006), enterprise architect by trade. Twenty years of complex systems — from Petri nets in 2008 to LLM pipelines in 2026.

---

## The starting problem — context doesn't hold

Early 2026. I'm working with an LLM on a software project. It's moving. But very quickly, a wall: the context window.

The LLM forgets. Not a little — structurally. A two-hour conversation, and it loses the thread. Decisions made at the start of a session no longer exist by the end. Context evaporates.

The question isn't "how to make the LLM smarter". The question is: how not to lose what we build with it?

---

## Files as memory

The answer is simple, almost banal: take the context out of the conversation. Put it in files. Notes, specs, reviews, decisions. Structured, named, versioned.

The LLM doesn't remember? No matter. The files stay. At each session, we reload what matters. Context is no longer in the machine's head — it's in the repo.

What looked like a hack became a protocol. Artifacts are not a byproduct of work. They are the work. Writing forces clarification. Structuring forces thought. The slowness of files compared to chat isn't a flaw — it's the mechanism that produces clarity.

---

## Separation of responsibilities

The real turning point. A single context for everything — architecture, code, strategy, writing, UX — doesn't hold. Topics contaminate each other. The LLM mixes levels. You're talking architecture and it slides into implementation. You're talking strategy and it drifts into code.

The solution: isolate. One context per domain. Specific instructions. Scopes. Prohibitions.

The architect doesn't code. The developer doesn't decide architecture. The strategist has no access to code. Each in their own space, their own files, their own rules.

This isn't organizational theory. It's dependency management. The same reflex as in software engineering: when everything depends on everything, nothing works. Isolate, define interfaces, control exchanges.

Personas were born from there — not from a desire to simulate a team, but from a technical need to separate concerns.

---

## Friction — what emerges from isolation

When personas are isolated, something unexpected happens. They disagree.

The architect blocks an implementation that moves too fast. The strategist questions a technical priority. The researcher flags a reference that doesn't hold. The designer refuses a theme that doesn't carry the project's identity. UX questions a flow that satisfies the developer but loses the user.

This wasn't planned. It happened because constraints force different angles. A generalist LLM says yes to everything. An LLM constrained by a role and prohibitions — it pushes in its direction.

Friction isn't a problem to solve. It's the mechanism that reveals blind spots. If all personas agree, they're useless.

---

## Emergence — one persona at a time

The method wasn't designed in advance. It grew with the project.

One persona at the start. Two when the first is calibrated. Three when the need is clear. Not by theoretical symmetry — because each identified gap produced a new role.

Each addition has a cost: calibration time, orchestration complexity, context to maintain. This cost is justified only by a real gap — a blind spot nobody covers, a competence the existing personas don't carry.

Hundreds of sessions. Traced ADRs. Documented failures. The method is a byproduct of real work, not a thought experiment.

---

## The thesis — in hindsight

Only by looking at what the method had produced did the thesis formulate itself.

It is possible to go faster and better at constant human resources. Not fewer people. The same people, augmented. Not replaced — amplified.

AI amplifies. It doesn't invent. If you give it nothing, it produces well-phrased nothing. If you give it years of conviction about a real problem, it builds with you.

Intentional friction between constrained roles, with a human who arbitrates — that's what transforms a generation tool into a thinking tool.

This isn't theory. It's what came out of the field when we solved problems one by one: context that doesn't hold, files as memory, separation of dependencies, and friction that emerges from isolation.

The method was born from constraints. The thesis came after.

---

Continue → [The method](methode.html)
