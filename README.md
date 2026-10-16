# OpenBridge

**Zero-script creation bridge for Godot, websites, and AI tools.**  
Part of the **OuRi** ecosystem.

OpenBridge is a local-first MCP project that aims to let AI clients work with Godot and browser tools without requiring users to write GDScript or JavaScript for supported tasks. The user describes the result; OpenBridge validates a structured plan, previews changes, and only then applies approved actions.

> **Status: early prototype.** The MCP runtime and data-only scene-spec validator are present. The Godot plugin and browser extension are initial UI scaffolds; they do not yet create scenes or manipulate websites. DeepSeek integration and the complete adapter bridge are planned, not shipped.

## What OpenBridge is

- **MCP server:** provides typed tools to an MCP-compatible host.
- **Godot editor plugin:** planned editor-side adapter for inspecting and building scenes with structured operations.
- **Browser extension:** planned user-controlled adapter for supported browser workflows.
- **DeepSeek workflow:** planned AI setup and structured scene planning, with provider credentials kept outside the repository.
- **Quick launcher:** scripts create a local Python environment and start the MCP server.
- **Zero-script experience:** users should not have to author scripts for supported operations. OpenBridge itself still contains implementation code.

## Architecture

```text
MCP-compatible AI host
        |
        v
 OpenBridge MCP runtime
        |
  schema validation + policy
        |
  approved adapter bridge
     /             \
    v               v
Godot editor     Browser extension
    |               |
structured scene   user-approved
operations         browser actions
```

The runtime is designed to bind to loopback by default. It must not silently upload project files, expose arbitrary local files, or execute arbitrary generated code.

## Current implementation

| Component | Status |
|---|---|
| MCP runtime with Streamable HTTP | Initial prototype |
| Runtime status and capability tools | Implemented in prototype |
| Data-only scene specification validator | Implemented; no project mutation |
| Windows and Unix-like launch scripts | Added; clean-install verification pending |
| Godot editor plugin | UI scaffold only |
| Browser extension | Popup scaffold; requests no website permissions |
| DeepSeek API integration | Planned |
| Godot scene creation / browser actions | Not implemented yet |

## Quick start

See [Quick start](docs/QUICKSTART.md).

- Windows: run `start-openbridge.bat`.
- Linux/macOS: run `sh ./start-openbridge.sh`.
- Configure an MCP-compatible host to use `http://127.0.0.1:8765/mcp` with Streamable HTTP transport.

The first launch requires Python 3.10+ and internet access to install dependencies. Do not expose the local server to a public network. The current prototype is not a finished Godot/browser bridge.

## Example: structured scene description

See [the example JSON](examples/scene-specs/simple-2d-scene.json). The validator checks a bounded data-only format; it does not yet apply the scene to Godot or guarantee that every node/property combination is valid in the target editor.

## Repository map

- [Quick start](docs/QUICKSTART.md)
- [Architecture](docs/ARCHITECTURE.md)
- [MCP and adapter contract](docs/PROTOCOL.md)
- [DeepSeek integration plan](docs/DEEPSEEK_INTEGRATION.md)
- [Documentation index](docs/README.md)
- [Zero-script workflow](docs/ZERO_SCRIPT_WORKFLOW.md)
- [Security requirements](docs/SECURITY.md)
- [Compatibility policy](docs/COMPATIBILITY.md)
- [Roadmap](docs/ROADMAP.md)
- `server/openbridge/` — MCP runtime
- `godot/addons/openbridge/` — Godot editor plugin scaffold
- `browser/extension/` — browser extension scaffold
- `examples/scene-specs/` — data-only scene examples
- `tests/` — automated tests

## Design principles

1. **No scripts required from the user** for supported workflows.
2. **Local-first:** bind local services to loopback by default.
3. **Explicit capabilities:** every tool has a narrow schema and documented side effects.
4. **Preview before mutation:** show intended changes before applying them.
5. **No hidden execution:** no arbitrary shell commands or generated scripts as a shortcut.
6. **Honest status:** distinguish planned, experimental, tested, and stable features.
7. **Open and auditable:** document dependencies, permissions, and network behavior.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please report security issues privately rather than posting exploit details in public issues.

## License

A license has not yet been selected. Until one is added, do not assume that the code is available for unrestricted reuse.
