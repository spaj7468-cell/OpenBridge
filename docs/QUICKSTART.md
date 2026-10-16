# Quick start

**Current status:** the Python MCP runtime and basic scene-spec validator are implemented as an early prototype. Godot and browser integrations are scaffolds and do not yet create or modify scenes/pages.

## Requirements

- Python 3.10 or newer
- Internet access for the first dependency installation
- An MCP-compatible host to connect to the local server

## Windows

1. Download or clone this repository.
2. Double-click `start-openbridge.bat`, or run it from a terminal.
3. The launcher creates `.venv`, installs the package, and starts the MCP Streamable HTTP server.
4. Configure your MCP-compatible host to use `http://127.0.0.1:8765/mcp` with Streamable HTTP transport.

## Linux and macOS

Run:

```sh
sh ./start-openbridge.sh
```

The first launch creates a local virtual environment and installs dependencies. Later launches may still check/install the package to pick up local changes.

## Configuration

| Environment variable | Default | Purpose |
|---|---|---|
| `OPENBRIDGE_HOST` | `127.0.0.1` | Bind address; keep loopback unless you understand the security implications |
| `OPENBRIDGE_PORT` | `8765` | MCP HTTP port |
| `OPENBRIDGE_GODOT_HEALTH_URL` | `http://127.0.0.1:8766/health` | Future Godot adapter health endpoint |

Do not expose the runtime to a public network. The current build does not yet implement adapter authentication or a complete browser/Godot bridge.

## Available tools

- `openbridge_status` — runtime and implementation status.
- `openbridge_capabilities` — implemented vs planned capabilities.
- `godot_adapter_status` — probes the future adapter health endpoint.
- `godot_validate_scene_spec` — validates a bounded data-only scene description. It does not edit files or guarantee runtime compatibility with Godot.

## Example scene spec

See [simple-2d-scene.json](../examples/scene-specs/simple-2d-scene.json).

## Troubleshooting

- **Python not found:** install Python 3.10+ and ensure `py` (Windows) or `python3` (Unix-like systems) is available.
- **Dependency installation fails:** check network access and try launching again.
- **Port already in use:** set `OPENBRIDGE_PORT` to another local port and update your MCP host configuration.
- **No Godot connection:** expected until the Godot adapter protocol is implemented; the current plugin is a UI scaffold only.
