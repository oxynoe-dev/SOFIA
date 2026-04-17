# Hooks

> Automate what needs to be automated, nothing more.

---

## What it is

Claude Code allows configuring **hooks** — shell commands
that execute in response to events (before/after a tool call,
on prompt submission, etc.).

## Useful hooks for SOFIA

### Session summary reminder

A hook that reminds the persona to produce a summary when the
conversation exceeds a certain number of exchanges. In practice,
the instruction in the CLAUDE.md is usually sufficient.

### Isolation check

A pre-edit hook that verifies the persona is not writing outside
its authorized scope. Useful if the persona tends to overstep.

### Commit format

A pre-commit hook that verifies the commit message format
according to project conventions.

## When NOT to use hooks

- To reproduce behavior the CLAUDE.md already handles
- For checks the persona can perform itself
- For complex automations that obscure the workflow

Hooks are a safety net, not a primary mechanism.
If you need many hooks, your CLAUDE.md instructions
are probably not clear enough.

## Configuration

Hooks are configured in `settings.json`:

```json
{
  "hooks": {
    "preToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "script-de-verification.sh"
      }
    ]
  }
}
```

See the Claude Code documentation for details.
