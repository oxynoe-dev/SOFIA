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
| [User guide](guides/user-guide.md) | New users | Overview of the method, key concepts, getting started |
| [Getting started](guides/getting-started.md) | New users | Manual instance setup, step by step |
| [Onboarding](guides/onboarding.md) | Existing instances | How to add a new persona |
| [Operator guide](guides/operator-guide.md) | Orchestrators | H2A operations — when, how, examples |
| [Audit guide](guides/audit-guide.md) | Orchestrators | Running the audit tools, reading results |

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

- **I want to understand SOFIA** → start with [User guide](guides/user-guide.md), then [Architecture](concepts/architecture.md)
- **I want to set up an instance** → [Getting started](guides/getting-started.md) or run `claude` in the repo (Sofia guides you)
- **I want to run an audit** → [Audit guide](guides/audit-guide.md)
- **I want to understand the protocol** → `protocol/h2a.md`, then [Operator guide](guides/operator-guide.md)
- **I want to look up a term** → [Glossary](reference/lexique.md)
- **I want to understand why a decision was made** → [ADRs](adr/adrs.md)
