## Challenger

![Pattern — Challenger](../../../doc/figures/fig-pattern-challenger.svg)

One producer advances, N challengers verify each on their own axis.

### Structure

The pattern is asymmetric: a single persona produces the artifact, the others challenge it without modifying it. Each challenger has blocking authority on their axis only — not on the whole.

The cost is linear (1 producer + N challengers = N interactions), not combinatorial (N personas discussing among themselves = N^2 interactions). This is what allows scaling the number of challengers without exploding coordination overhead.

The producer integrates the feedback or justifies why they don't. The orchestrator arbitrates in case of disagreement.

### When to recognize it

- A persona produces a deliverable (code, spec, document) that touches multiple quality axes.
- Validation is needed without creating a committee or meeting.
- The verification axes are independent from each other.

### Example

Axel codes a feature for the Katen engine. Mira challenges on architectural consistency, Léa on formalism (contracts, invariants), Nora on API ergonomics. Each produces feedback on their axis. Axel integrates.

### Variants

- **Single challenger**: only one axis is needed (e.g. Mira reviews an ADR from Axel on architecture alone).
- **Rotating challenger**: the producer changes depending on the nature of the deliverable, but the mechanism stays the same.
- **Cross-challenge**: two personas challenge each other on distinct deliverables (each is producer of one, challenger of the other).

### Risks

- **Dilution**: too many challengers slows the producer without proportional gain.
- **Abusive blocking**: a challenger blocks on a detail outside their axis.
- **Passivity**: the challenger validates without truly verifying — the pattern loses its value.
