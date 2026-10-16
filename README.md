# OpenBridge

**A ZeroScript-style AI agent bridge for Godot.**  
Part of the **OuRi** ecosystem.

OpenBridge aims to let an AI work inside the Godot editor from a normal AI chat or MCP-compatible host. The user describes the game and the agent inspects the project, edits GDScript, builds scenes, configures nodes and resources, runs tests, reads errors, and iterates. The user does not need to write code manually for supported tasks — **but the AI absolutely can and often must write GDScript** to implement game logic and interfaces.

> **Status: early prototype.** The MCP runtime and data-only scene-spec validator are present. The Godot plugin and browser extension are UI scaffolds; they do not yet create scenes, edit scripts, run projects, or manipulate websites. The full agent loop described below is the product target, not a claim that every feature is already implemented.

## Product goal

Bring the practical workflow of [ZeroScript-Free](https://github.com/sebattfg/ZeroScript-Free) to Godot: **chat → agent tools → local bridge → editor → verified result**. ZeroScript-Free connects an AI chat to Roblox Studio, including script reading/editing, running code, inspecting the game tree, generating assets, and play-testing. OpenBridge adapts that agent pattern to Godot's scene system, GDScript, resources, debugger, and run/playtest workflow.

## What the Godot agent should do

- **Inspect:** report Godot version, project settings, active scene, scene tree, scripts, resources, errors, and run state within user-approved project boundaries.
- **Build scenes:** create scenes and nodes, set properties, attach resources, connect signals, and organize project files.
- **Write and edit GDScript:** create scripts for player movement, UI, interactions, inventory, dialogue, save systems, AI behaviors, and other requested gameplay.
- **Work with existing code:** read relevant scripts, make focused edits, show diffs, preserve user code, and explain what changed.
- **Run and debug:** launch the project or a scene, collect relevant Godot errors and warnings, use test results to propose fixes, and iterate.
- **Assets and resources:** import or create supported resources and connect them to scenes, while clearly identifying missing assets and placeholders.
- **Agent loop:** plan → inspect → edit → validate → preview → approve where needed → run → read results → repair.
- **Zero-script experience:** the user describes the desired result instead of manually authoring scripts. This does not mean the project contains no scripts.

## Architecture

```text
AI chat / MCP-compatible host
            |
            v
      OpenBridge MCP runtime
            |
  schemas + policy + approvals
            |
    authenticated local bridge
            |
            v
       Godot EditorPlugin
            |
  scenes • nodes • GDScript • resources
            |
  run project • inspect errors • iterate
```

The local bridge binds to loopback by default. It must not silently upload project files, expose arbitrary local files, or execute high-impact actions without an explicit policy. Generated GDScript is a first-class feature, but writing, running, and destructive edits must be distinct, visible operations with review and recovery controls.

## Current implementation

| Component | Status |
|---|---|
| MCP runtime with Streamable HTTP | Initial prototype |
| Runtime status and capability tools | Implemented in prototype |
| Data-only scene specification validator | Implemented; validation only |
| GDScript patch-envelope validator | Implemented; validates paths/size/hash metadata only |
| Windows and Unix-like launch scripts | Added; clean-install verification pending |
| Godot editor plugin | Authenticated local bridge, editor info, bounded scene tree, script reading, preview, opt-in script writes with backups |
| Browser extension | User-triggered active-tab title/URL capture and copy; no page-content scraping or MCP tool execution |
| Godot editor info, bounded scene-tree inspection, script reading | Implemented in bridge; requires Godot 4 manual verification |
| GDScript preview and guarded file application | Implemented prototype; Godot manual verification pending |
| Godot parser validation and run/playtest | Planned |
| GDScript creation/editing and diff preview | Planned |
| Run/playtest and debugger feedback loop | Planned |
| DeepSeek API integration | Planned |

## Quick start

See [Quick start](docs/QUICKSTART.md).

- Windows: run `start-openbridge.bat`.
- Linux/macOS: run `sh ./start-openbridge.sh`.
- Set the same private `OPENBRIDGE_ADAPTER_TOKEN` in the environment for Godot and OpenBridge before launching both.
- Configure an MCP-compatible host to use `http://127.0.0.1:8765/mcp` with Streamable HTTP transport.
- The Godot add-on listens on `127.0.0.1:8766` by default and provides read-only editor info, scene-tree inspection, and script reading. See [Quick start](docs/QUICKSTART.md).

The first launch requires Python 3.10+ and internet access to install dependencies. The authenticated local bridge now supports editor info, bounded scene-tree inspection, script reading, script preview, and opt-in script file writes with stale-hash checks and backups. It still needs manual verification in Godot 4. Scene mutations, parser validation, run/playtest, browser actions, and DeepSeek provider calls remain incomplete. Script writes are disabled by default and require enabling the session toggle in the Godot dock. Do not expose local services to a public network.

## Documentation

- [Quick start](docs/QUICKSTART.md)
- [Architecture](docs/ARCHITECTURE.md)
- [MCP and adapter contract](docs/PROTOCOL.md)
- [Godot agent workflow](docs/GODOT_AGENT_WORKFLOW.md)
- [DeepSeek integration plan](docs/DEEPSEEK_INTEGRATION.md)
- [Documentation index](docs/README.md)
- [Zero-script workflow](docs/ZERO_SCRIPT_WORKFLOW.md)
- [Security requirements](docs/SECURITY.md)
- [Compatibility policy](docs/COMPATIBILITY.md)
- [Roadmap](docs/ROADMAP.md)

## Design principles

1. **No manual coding required** for supported workflows; AI-written GDScript is allowed and expected when needed.
2. **Local-first:** bind local services to loopback by default.
3. **Real tools, real results:** every advertised capability must be implemented and return evidence of its result.
4. **Preview and recover:** show script diffs and planned project changes; back up before risky edits.
5. **Controlled execution:** never run generated code silently; execution must be a separate visible action governed by user approval and project policy.
6. **Least privilege:** keep operations inside the selected project and use narrow, typed tools rather than arbitrary shell access.
7. **Honest status:** distinguish planned, experimental, tested, and stable features.
8. **Open and auditable:** document dependencies, permissions, and network behavior.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please report security issues privately rather than posting exploit details in public issues.

## License

A license has not yet been selected. Until one is added, do not assume that the code is available for unrestricted reuse.
