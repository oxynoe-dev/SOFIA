# Context transfer post-reorganization

> Creating personas isn't enough. You need to transfer what they need to know.

---

## The case

Split of a 7-persona instance into 3 instances. The diagnosis: the problem wasn't the bus saturating — it was persona granularity (two professions in the same context). The split fixes granularity. But the 6 new personas start without context — no history of decisions, studies, or failures.

This is exactly the onboarding problem for a human joining an existing team.

## What we observed

1. **The first transfer worked.** Mira produced a structured note (9 studies + figures, with what/where/why/priorities). Aurele was able to start immediately.

2. **The transfer wasn't planned in the migration plan.** The target study described the topology, personas, scripts. Not the context transfer. We discovered it after the fact.

3. **The mapping isn't 1:1.** One sender can feed multiple recipients (Mira → Aurele + Emile + Livia). The orchestrator identified a missing transfer that the architect hadn't seen.

4. **Self-transfer is a special case.** When a persona changes instance but keeps their name (Marc), they must document what changes in their scope themselves. No external note — reflective work.

## Transfer protocol

When a scope changes hands:

1. **The former owner produces a structured note** — what, where, why, what stays with them. Free format, mandatory content.
2. **The orchestrator checks completeness** — are all knowledge flows covered? The sender/recipient mapping isn't obvious.
3. **Distinguish operational context from history** — files transfer. The "why we made this choice" is harder to capture. Sessions contain this context but aren't structured for transfer.

## Claude memory

Claude project memory (`~/.claude/projects/`) doesn't transfer automatically during a split. After a reorg:

- **Clean up** — remove memories that concern the former scope
- **Differentiate** — each new instance has its own memory, even if the persona keeps the same name
- **Don't copy in bulk** — the old instance's memory mixes the domains you just separated

**Sign**: a persona who "remembers" decisions made in a scope that's no longer theirs. The memory has become noise.

## The rule

**Context transfer is an explicit step in any reorganization**, on par with creating personas and conventions. Not planning for it = letting new personas navigate blind.
