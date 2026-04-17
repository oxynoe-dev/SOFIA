# Contribution

> Who brought what.

---

## Definition

Contribution captures the direction and nature of inputs during a session: who fed what. It is the epistemic flow of the synchronous human-assistant exchange.

## Dimensions

| Dimension | Values | Required |
|-----------|--------|----------|
| **exchange** | Reference to the exchange (session or artefact) that generated the contribution | MUST |
| **direction** | `[H]` (human brings) or `[A]` (assistant brings) | MUST |
| **type** | `substance`, `structure`, `contestation`, `decision` | MUST |
| **description** | Short summary of the input | MUST |

> **FR retrocompat.** The parser also accepts `matiere` as an alias for `substance`.

**Scope**: a contribution is attached to an exchange (session or artefact), itself attached to a space within an instance.

## Layer

Contribution is entirely **observational**. The distinction between input types (substance vs structure vs contestation) is semantic and non-deterministic. The `## Flux` section is optional (MAY).

## Direction tags

| Tag | Meaning |
|-----|---------|
| `[H]` | The human brings |
| `[A]` | The assistant brings |

## Input types

| Type | Definition |
|------|-----------|
| `substance` | New information — fact, data, reference, insight |
| `structure` | Organization, categorization, synthesis |
| `contestation` | Challenge, counter-example, reframing |
| `decision` | Arbitration, choice retained |

## Format

Each contribution line carries: direction tag, type, short description.

Counting by direction and type is optional (MAY).

> **Example** (Markdown implementation, see `implementation/implementation.md`):
>
> ```
> ## Flux
> - H:substance — Böckeler article, request for opinion
> - A:substance — scaffolding lineage absent from Böckeler
> - A:structure — three levels of harness/SOFIA complementarity
> - H:decision — keep keyword notation
>
> H:2 (substance 1, decision 1) | A:2 (substance 1, structure 1)
> ```

## Contribution / friction distinction

The same exchange MAY appear in both `## Flux` and `## Friction`:

- **Contribution** captures input (who brought what)
- **Friction** captures tension (opposing positions, resistance)

Criterion: a correction accepted without resistance = `H:contestation` in the flux, not a friction. If the assistant resists or resolution requires multiple exchanges, it is also a friction.

## Reading

| Pattern | Interpretation |
|---------|---------------|
| H >> A on substance | The assistant structures/scaffolds, the human brings the substance |
| A >> H on substance | The human steers, the assistant brings the substance |
| H ≈ A | Balanced co-construction |

This is not a value judgment — it is a signal about the active collaboration mode.
