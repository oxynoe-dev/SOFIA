---
title: Setting up with Sofia
---

# Setting up with Sofia

> **Alpha** — Sofia relies on the provider's conversational behavior. Results may vary.

```bash
git clone https://github.com/oxynoe-dev/sofia
cd sofia
claude
> hello
```

Sofia presents a menu with 4 modes:

> 1. **Create an instance** — I guide the setup (structure, conventions, personas)
> 2. **Add a persona** — a new voice in an existing instance
> 3. **Recalibrate** — adjust an existing persona
> 4. **Audit** — compliance diagnostic + frictions

## Creating an instance (mode 1)

Choose **1. Create an instance**. Sofia then:

1. **Locates the instance** — asks where to create it, and where your project repo lives
2. **Understands your project** — asks what you're building (1-2 turns)
3. **Proposes personas in tension** — at least 2, directly proposed based on your project's axes of tension. Not a list of choices — a proposal you validate or adjust
4. **Calibrates** — name, stance, scope, prohibitions for each persona. Sofia proposes, you adjust
5. **Generates the files** — persona sheets, contexts, CLAUDE.md, conventions, workspace structure

After generation: your personas will say no (by design), other personas will come (when the work makes them emerge), and you can relaunch Sofia anytime.

## Adding a persona (mode 2)

Relaunch Sofia and choose **2. Add a persona**. Sofia then:

1. **Reads the existing team** — personas, contexts, conventions
2. **Asks what triggers the need** — a persona that deflects? a recurring tension? a domain nobody covers?
3. **Proposes a persona in tension** — in tension with at least one existing persona (otherwise no friction)
4. **Calibrates** — name, stance, scope, prohibitions
5. **Generates 3 files** — persona sheet, context, CLAUDE.md + workspace
6. **Announces** — deposits a note in shared/notes/ so other personas discover the new one at their next boot

> If Sofia flags "that looks like a task, not a role" — listen. A persona is a permanent role with prohibitions, not a one-off executor.

> If the flow doesn't start or drifts, switch to manual setup below.
