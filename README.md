# OpenBridge

**Zero-script creation bridge for Godot, websites, and AI tools.**  
Part of the **OuRi** ecosystem.

OpenBridge is planned as a local-first integration layer that lets an AI host work with supported tools through MCP, while users control the workflow through extensions and editor plugins instead of writing scripts by hand.

> **Project status: foundation / early development.** The repository is being prepared. Do not treat the planned integrations below as released or production-ready until their implementation and compatibility are tested.

## The idea

One local runtime, several adapters:

- **MCP server** — exposes explicitly supported actions to MCP-compatible AI clients.
- **Godot editor plugin** — a structured, allow-listed bridge for creating and editing scenes, nodes, resources, and project metadata.
- **Browser extension** — a user-controlled bridge for supported website workflows and development tasks.
- **AI provider adapter** — DeepSeek first in the planned roadmap, with provider settings kept separate from the core runtime.
- **Quick launcher** — one command starts the local service and reports its status.
- **Zero-script workflow** — users choose actions, describe a result, review a plan, and approve changes. OpenBridge should generate structured editor operations rather than ask users to write GDScript or JavaScript.

## Planned architecture

```text
MCP-compatible AI client
          |
          v
   OpenBridge MCP server
          |
   permission + validation
          |
     local adapters
       /       \
      v         v
 Godot plugin  Browser extension
      |         |
      v         v
 Godot editor  Allowed browser actions
```

The AI provider is configured by the user in the compatible client or an optional provider adapter. OpenBridge must not silently upload project files, expose arbitrary local files, or execute arbitrary code.

## Planned capabilities

| Area | Goal |
|---|---|
| Godot | Create scenes and nodes, edit safe properties, attach resources, inspect the scene tree, run checks |
| Websites | Inspect the current page when explicitly permitted, assist with supported UI and development workflows |
| MCP | Typed tools, clear schemas, predictable errors, capability discovery |
| AI | DeepSeek-first setup guide; provider-independent tool interface |
| Launcher | One-command startup, health check, readable logs |
| Safety | Local binding, explicit permissions, action preview, confirmation for destructive changes |

## Repository map

- `docs/ARCHITECTURE.md` — components and communication boundaries
- `docs/ROADMAP.md` — milestones and acceptance criteria
- `docs/SECURITY.md` — threat model and safety requirements
- `docs/ZERO_SCRIPT_WORKFLOW.md` — how the no-manual-scripting experience should work
- `docs/COMPATIBILITY.md` — planned host/editor/browser support
- `docs/PROTOCOL.md` — MCP tools and adapter contract
- `server/` — MCP runtime
- `godot/addons/openbridge/` — Godot editor plugin
- `browser/` — browser extension
- `tests/` — automated checks

## Quick start

The launcher and adapters are not implemented yet. For now, follow the [roadmap](docs/ROADMAP.md) to see what is planned and what is not yet available. A working quick-start command will be documented here only after it has been tested from a clean checkout.

## Design principles

1. **No scripts required from the user.** Internal implementation code is still necessary and is maintained by the project.
2. **Local-first.** Bind local services to loopback by default.
3. **Explicit capabilities.** Every tool has a narrow schema and a documented effect.
4. **Preview before mutation.** Show the proposed scene/page changes before applying them where feasible.
5. **No hidden execution.** No arbitrary shell commands or generated script execution as a shortcut.
6. **Honest status.** Mark features as planned, experimental, tested, or stable.
7. **Open and auditable.** Document dependencies, permissions, and network behavior.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please report security issues privately rather than posting exploit details in public issues.

## License

License selection is still pending. Until a license is added, do not assume that the code is available for unrestricted reuse.
