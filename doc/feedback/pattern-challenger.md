# Field experience report — Challenger pattern

> One producer, N challengers. Each on their axis. Each with blocking rights.

---

## The pattern

One persona produces. Other personas intervene to verify quality on their
axis of expertise, without producing themselves. Each challenger has
blocking rights on their axis. The orchestrator orchestrates and decides.

This is distinct from peer friction (two personas at the same level who
contest). The challenge is **asymmetric**: one produces, others verify.

## Instances observed on Katen

### Product chain (code)

| Role | Persona | Axis |
|------|---------|------|
| Producer | Axel | Code, implementation |
| Challenger | Mira | Architecture, ADR coherence |
| Challenger | Léa | Formal invariants, rigor |
| Challenger | Nora | UX, user flows |

One producer, three challengers. Maximum intensity — it's the key product.

### Editorial chain (blue book)

| Role | Persona | Axis |
|------|---------|------|
| Producer | Winston | Writing, narrative |
| Challenger | Mira | Structure, argumentative coherence |
| Challenger | Léa | Academic references, facts |
| Challenger | Marc | Positioning, tone |
| Challenger | Nora | UX of published deliverables |

### Multi-format production chain

| Role | Persona | Axis |
|------|---------|------|
| Producer | Sofia | PDF, PPTX, web, social media |
| Challenger | Nora | UX, accessibility |

## Properties

- **Asymmetry** — the producer moves forward, challengers intervene.
  Not the other way around.
- **Single axis** — each challenger verifies on their axis of expertise,
  not on everything. The architect doesn't challenge UX. UX doesn't
  challenge architecture.
- **Blocking rights** — a challenger can block. The orchestrator decides
  whether the block is lifted or maintained.
- **Scalable** — you can add challengers without changing the producer.
  The cost is linear, not combinatorial.

## Academic signal

Huang et al. (2025) — *Resilience of Multi-Agent Systems to Untrustworthy Agents* (arXiv:2408.00989) — measure the resilience of multi-agent topologies against untrustworthy agents. The **hierarchical topology** (central coordinator + specialized agents) loses only -5.5% performance with failing agents, versus -10% to -24% for flat topologies (debate, relay).

**Limitation**: the study is about pure multi-agent (AI↔AI), without a human at the center. The challenger pattern in SOFIA is human↔AI orchestration — the orchestrator arbitrates, not a coordinator agent. This is a **convergent signal** (hierarchical topology is resilient), not a **validation** of our method. Nobody has measured this pattern with a human orchestrator.

## For your project

The challenger pattern emerges naturally when a persona starts producing
deliverables that impact multiple dimensions. A few rules:

- Identify the producer and their challengers for each chain
- Give each challenger an explicit axis — not "general review" but
  "verify reference rigor" or "verify accessibility"
- Blocking rights are real — if a challenger blocks, the orchestrator
  decides, but the producer doesn't push through
- Document challenge rights in persona sheets (section "What they challenge")
