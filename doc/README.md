# Documentation

> How to read the SOFIA documentation — structure, entry points, and navigation.

---

## Structure

The documentation follows four sections, mapped to the repo structure:

| Section | Where | What |
|---------|-------|------|
| **Specification** | `core/`, `protocol/` | The method invariants and the H2A protocol — what SOFIA *is* |
| **Documentation** | `doc/guides/`, `doc/concepts/` | How to use the method and the ideas behind it |
| **Reference** | `doc/reference/`, `doc/adr/`, `doc/feedback/` | Glossary, blue book, decision records, field experience |
| **Implementation** | `binding/`, `provider/` | How the method materializes — filesystem binding, Claude Code provider |

Inspiration and starting points live in `canvas/` (archetypes, artifact formats, patterns, workflows).

---

## Guides

Practical documentation — how to do things.

| Document | For whom | Content |
|----------|----------|---------|
| [Getting started](guides/getting-started.md) | New users | From prerequisites to first friction — the complete guide |
| [Onboarding](guides/getting-started.md#part-3--adding-a-persona-to-an-existing-instance) | Existing instances | How to add a new persona |
| [Operator guide](guides/operator-guide.md) | Orchestrators | H2A (Human-to-Assistant) operations — when, how, examples |
| [Audit & Analysis](audit/README.md) | Orchestrators | Conformity checks, data pipeline, dashboard |

---

## Concepts

Foundational ideas — why things are the way they are.

| Document | Content |
|----------|---------|
| [Architecture](concepts/architecture.md) | 5 layers + canvas, conceptual model, design principles |
| [Hidden condition](concepts/hidden-condition.md) | Target profile, cognitive trait, three levels of dependency |
| [Derivation grammar](concepts/derivation-grammar.md) | Two modes of persona creation — bootstrap and emergence |

---

## Reference

Resources to consult, not to read linearly.

| Document | Content |
|----------|---------|
| [Glossary](reference/lexique.md) | All SOFIA terms defined |
| [Blue book](reference/bluebook.md) | The thesis — friction as value mechanism (EN) |
| [Livre bleu](reference/livre-bleu-sofia.md) | The thesis — friction as value mechanism (FR) |
| [Legend](../binding/filesystem/analysis/legend/legend.md) | Dashboard metrics, KPIs, radar axes, glossary |
| [ADRs](adr/adrs.md) | Architecture decision records |
| [Field feedback](feedback/README.md) | Experience reports from Katen and post-split |

---

## Navigation

- **I want to understand and use SOFIA** → [Getting started](guides/getting-started.md)
- **I want to go deeper on the architecture** → [Architecture](concepts/architecture.md)
- **I want to run an audit** → [Audit & Analysis](audit/README.md)
- **I want to understand the protocol** → `protocol/h2a.md`, then [Operator guide](guides/operator-guide.md)
- **I want to look up a term** → [Glossary](reference/lexique.md)
- **I want to understand why a decision was made** → [ADRs](adr/adrs.md)
