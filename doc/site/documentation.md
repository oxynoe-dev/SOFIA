---
from: aurele
to: nora, alma
nature: content
date: 2026-04-21
subject: Documentation landing — entry point for all SOFIA docs
---

# Documentation

> Everything you need to understand, use, and contribute to SOFIA.

---

## Start here

| You want to... | Read this |
|-----------------|-----------|
| Understand what SOFIA is | [Why SOFIA](intention.html) |
| Set up your first instance | [Tutorial](tutorial.html) |
| Learn the method in depth | [The method](methode.html) |
| Read the thesis | [Blue book](../reference/bluebook.md) |

---

## Guides

Step-by-step documentation for practitioners.

| Guide | Content |
|-------|---------|
| [User guide](../guides/user-guide.md) | Overview — concepts, getting started, anti-patterns |
| [Getting started](../guides/getting-started.md) | Manual instance setup, file by file |
| [Onboarding](../guides/onboarding.md) | Adding a persona to an existing instance |
| [Operator guide](../guides/operator-guide.md) | H2A (Human-to-Assistant) operations — when, how, examples |
| [Audit guide](../guides/audit-guide.md) | Running audits, reading results |

---

## Specification

The method's invariants and protocol — what SOFIA *is*.

| Document | Content |
|----------|---------|
| [Principles](../../core/principles.md) | 7 invariant principles |
| [Model](../../core/model.md) | 7 constitutive entities, 3 levels |
| [Duties](../../core/duties.md) | 6 non-delegable orchestrator responsibilities |
| [H2A](../../protocol/h2a.md) | The coordination protocol — invariants, operations, audit |
| [Friction](../../protocol/friction.md) | Markers, resolutions, lineage, reportPattern |
| [Exchange](../../protocol/exchange.md) | Sessions, artifacts, send/receive |
| [Contribution](../../protocol/contribution.md) | Epistemic flow — direction and type |

---

## Concepts

Foundational ideas behind the method.

| Document | Content |
|----------|---------|
| [Architecture](../concepts/architecture.md) | 5 layers + canvas, design principles |
| [Hidden condition](../concepts/hidden-condition.md) | Target profile, cognitive trait |
| [Derivation grammar](../concepts/derivation-grammar.md) | Two modes of persona creation |

---

## Reference

| Document | Content |
|----------|---------|
| [Glossary](../reference/lexique.md) | All SOFIA terms defined |
| [Blue book](../reference/bluebook.md) | The thesis — friction as value mechanism (EN) |
| [Livre bleu](../reference/livre-bleu-sofia.md) | The thesis (FR) |
| [ADRs](../adr/adrs.md) | Architecture decision records |
| [Field feedback](../feedback/README.md) | Experience reports from real projects |
| [Dashboard legend](../../binding/filesystem/analysis/legend/legend.md) | Dashboard metrics and indicators |

---

## Implementation

How the method materializes — for contributors and tool builders.

| Document | Content |
|----------|---------|
| [Binding spec](../../binding/implementation.md) | Filesystem implementation — stack, operations mapping |
| [Audit rules](../../binding/filesystem/audit.md) | Check taxonomy, severity, rules |
| [Conventions template](../../binding/filesystem/conventions.md) | Standard conventions for new instances |
| [Claude Code provider](../../provider/claude-code/claude-md.md) | CLAUDE.md anatomy |

---

## Canvas

Starting points — not prescriptions.

| Type | Content |
|------|---------|
| [Archetypes](../../canvas/archetypes/) | Persona templates by role |
| [Artifacts](../../canvas/artifacts/) | Artifact format templates |
| [Patterns](../../canvas/patterns/) | Recurring structures |
| [Workflows](../../canvas/workflows/) | Process templates |
| [Example: Katen](../../canvas/examples/katen/) | Reference instance |

---

## History

- [How SOFIA emerged](histoire.html) — from context loss to intentional friction
