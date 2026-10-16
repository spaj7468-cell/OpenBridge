# OpenBridge architecture

**Status:** proposed architecture, not yet implemented end-to-end.

## 1. Components

### OpenBridge MCP runtime
The runtime is the boundary between an MCP-compatible host and adapters. It publishes typed tools and resources, validates arguments, checks permissions, dispatches approved operations, and returns structured results.

The runtime must not infer that a tool is safe merely because an AI client requested it. Each operation needs an explicit schema, validation, capability check, and result.

### Godot adapter
A Godot editor plugin runs inside the editor and owns editor-specific operations. The planned first capabilities are:

- report editor and project status;
- read the current scene tree;
- create supported node types;
- set allow-listed properties;
- create a scene from a structured scene description;
- save only after a preview/approval step;
- return errors with the affected node/property and a recovery hint.

The adapter should use Godot editor APIs and structured data, not generate arbitrary GDScript as the normal path.

### Browser adapter
A browser extension provides a user-visible permission boundary. It should request only necessary permissions, act only on supported tabs/origins, and require explicit user action for page mutations or sensitive operations. It should never silently read all pages or send page contents to an AI provider.

### AI provider integration
DeepSeek is the first planned setup guide/provider target. The core tool contract should not depend on one model provider. API keys must be stored using the host's supported secret mechanism or supplied through environment variables; never commit keys into the repository or extension bundle.

### Launcher and health endpoint
The launcher starts the local runtime, verifies configuration, reports the bound address and port, and shuts down cleanly. The service should bind to loopback by default and expose a health/status check that does not reveal secrets.

## 2. Request flow

1. The user configures an MCP-compatible client and starts OpenBridge.
2. The host discovers the advertised tools and their schemas.
3. The model proposes a sequence of structured actions.
4. OpenBridge validates each action and checks the current permission policy.
5. Mutating actions are shown in a preview or require confirmation.
6. The relevant adapter executes only the supported operation.
7. The adapter returns a structured result and any diagnostics.
8. The host can use the result to propose the next step.

## 3. Structured scene description

The planned scene format is data, not executable code. Example:

```json
{
  "format": "openbridge.scene/v1",
  "root": {
    "name": "Main",
    "type": "Node2D",
    "children": [
      {
        "name": "Player",
        "type": "CharacterBody2D",
        "properties": {
          "position": {"x": 160, "y": 120}
        }
      },
      {
        "name": "Camera",
        "type": "Camera2D"
      }
    ]
  }
}
```

This is an illustrative format only; it is not yet a supported input contract. A future implementation must validate node types, property types, resource paths, tree depth, node count, and project boundaries before applying it.

## 4. Boundaries and failure handling

- MCP transport is separate from Godot and browser adapter protocols.
- Adapter versions and capabilities are discoverable.
- Timeouts and disconnects return typed errors; they do not trigger unlimited retries.
- Operations should be idempotent when possible.
- Long tasks return progress or a task identifier instead of blocking forever.
- File paths are canonicalized and constrained to the selected project/workspace.
- Logs redact tokens, credentials, and sensitive page content.

## 5. Proposed repository layout

```text
OpenBridge/
├── README.md
├── CONTRIBUTING.md
├── LICENSE                 # add after license choice
├── docs/
│   ├── ARCHITECTURE.md
│   ├── COMPATIBILITY.md
│   ├── PROTOCOL.md
│   ├── ROADMAP.md
│   ├── SECURITY.md
│   └── ZERO_SCRIPT_WORKFLOW.md
├── server/
│   └── openbridge/         # MCP runtime and adapter registry
├── godot/
│   └── addons/openbridge/  # editor plugin
├── browser/
│   └── extension/          # browser extension source
├── examples/
│   └── scene-specs/
└── tests/
    ├── unit/
    └── integration/
```

## 6. Initial implementation order

Build and test the local runtime and health check first; then add one narrow Godot read-only tool, followed by a previewable node-creation tool. Add browser integration only after the permission model and local bridge contract are defined.
