# OpenBridge documentation

OpenBridge is an early-stage local MCP runtime and planned editor/browser adapter system in the OuRi ecosystem. These pages describe the intended architecture and the current prototype; read the status notes before assuming a feature exists.

## Start here

- [Quick start](QUICKSTART.md) — launch the prototype and connect an MCP host.
- [Architecture](ARCHITECTURE.md) — components and request flow.
- [Godot agent workflow](GODOT_AGENT_WORKFLOW.md) — ZeroScript-style inspect/edit/run/debug loop.
- [Roadmap](ROADMAP.md) — milestones and acceptance criteria.
- [Zero-script workflow](ZERO_SCRIPT_WORKFLOW.md) — the user experience and its limits.

## Integration and development

- [MCP and adapter contract](PROTOCOL.md) — planned tool groups, errors, and scene-spec validation.
- [DeepSeek integration](DEEPSEEK_INTEGRATION.md) — planned provider workflow and official references.
- [Compatibility policy](COMPATIBILITY.md) — intended targets; support is not claimed until tested.
- [Contributing](../CONTRIBUTING.md) — contribution requirements.

## Security

- [Security requirements](SECURITY.md) — threat model, permissions, local service boundaries, and release checklist.

## Status language

- **Implemented in prototype:** code exists, but may not yet be verified in a clean end-to-end setup.
- **Scaffold:** initial UI or file structure exists; integration behavior is not implemented.
- **Planned:** described in the roadmap but not yet implemented.
- **Tested:** an automated or manual test has passed for a named environment/version.
- **Stable:** release-quality behavior with compatibility and security review.

## Source policy

Protocol and API details can change. Prefer official documentation linked from each page, record the date of compatibility checks, and avoid presenting an untested integration as working.
