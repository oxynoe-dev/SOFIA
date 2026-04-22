## Inspector

The orchestrator intercepts and verifies before forwarding. Not a persona — a responsibility.

### Structure

The pattern is complementary to the Challenger. The Challenger operates after production (peer review). The Inspector operates during circulation — they intercept artifacts between personas, verify, correct if necessary, then forward.

In SOFIA, the Inspector is the orchestrator. It's implicit in the orchestrator's role: they read everything, filter, contextualize, correct before forwarding. Three functions combined in one person: orchestrator, arbiter, inspector.

This is the most attention-costly mechanism — and the first to fail when fatigue sets in.

### When to recognize it

- The orchestrator forwards an artifact from one persona to another without having reread it → inspection is absent.
- A factual error propagates across 3+ documents without being detected → the inspection chain is broken.
- The orchestrator approves sessions without reading the summaries → the inspector role has been abandoned.

### What the inspector verifies

| Moment | Verification |
|--------|-------------|
| Before forwarding | Does the artifact say what the producer thinks it says? |
| Before forwarding | Is the context sufficient for the recipient? |
| After reception | Does the response address the question asked? |
| Continuously | Are the facts (dates, numbers, references) correct? |

### Relationship with the Challenger

The Challenger and the Inspector cover two different moments:

- **Challenger** → after production, between peers. Horizontal.
- **Inspector** → during circulation, by the orchestrator. Vertical.

Combined, they catch the vast majority of errors. Separately, each lets through what the other would catch. The Inspector catches factual errors that personas cannot verify (they have no reliable memory). The Challenger catches substantive errors that the orchestrator may miss due to fatigue.

### Risks

- **Overload**: the orchestrator combines orchestration + arbitration + inspection. This is the primary dropout factor (duty #6: maintain attention).
- **False sense of security**: inspection exists in the process but is not executed — the orchestrator scans instead of reading.
- **No backup**: if the orchestrator drops out, no one takes over. Personas continue producing with the same confidence.

### Mitigation

- Reduce the inspection surface: fewer active personas in parallel = fewer artifacts to inspect.
- Make inspection moments explicit in the session protocol (duty #3: reread what goes out).
- Track missed inspections: when an artifact is forwarded without rereading, note it. The trace makes the gap visible.

### Reference

Huang, J.-T. et al. (2025). "On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents." *ICML 2025*. https://arxiv.org/abs/2408.00989
