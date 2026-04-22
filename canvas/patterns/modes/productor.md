## Productor

The basic pattern. A persona produces within their scope, the orchestrator receives.

### Structure

1. The orchestrator opens a session with the persona
2. They give a directive or context
3. The persona produces in their space
4. The orchestrator receives the result

### When to use it

When a persona must produce an artifact (spec, code, analysis, writing) without inter-persona challenge being necessary. This is the default mode of a session.

### Limits

The productor alone has no friction — the persona executes, the orchestrator receives. If all sessions are in productor mode, the method loses its central mechanism. The productor is generally combined with the inspector (the orchestrator verifies before forwarding) or the challenger (another persona contests).
