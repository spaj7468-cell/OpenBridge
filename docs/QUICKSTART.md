# Quick start

**Current status:** OpenBridge has a local MCP server and an early Godot 4 EditorPlugin adapter. The adapter can report editor information, inspect the active scene tree, read/preview GDScript, and apply script changes when you explicitly enable script writes in the editor dock. It does not yet create scenes or run the game. A Godot-native parser-validation tool is now implemented in the prototype but still needs manual Godot verification. Browser support currently captures the active tab title/URL; it is not yet connected to MCP tools.

## Requirements

- Python 3.10+
- Godot 4.x editor
- An MCP-compatible AI host
- Internet access for the first Python dependency installation

## 1. Configure the shared local token

The Godot plugin and Python server must use the same secret. In PowerShell, create a random token and keep it private:

```powershell
$env:OPENBRIDGE_ADAPTER_TOKEN = [guid]::NewGuid().ToString("N") + [guid]::NewGuid().ToString("N")
$env:OPENBRIDGE_GODOT_PORT = "8766"
```

Launch Godot and OpenBridge from processes that inherit these environment variables. If your AI host starts the MCP server itself, set the same variables in that host's environment. Restart Godot after changing the token. Do not commit the token or expose port 8766 to a network.

## 2. Install the Godot add-on

1. Copy `godot/addons/openbridge` from this repository into your project's `addons/openbridge` folder.
2. Open the project in Godot.
3. Open **Project → Project Settings → Plugins** and enable **OpenBridge**.
4. Find the OpenBridge dock. It should report that the local adapter is listening on `127.0.0.1:8766`.
5. Open a scene before using the scene-tree tool.

If the dock says the token is missing, launch Godot with `OPENBRIDGE_ADAPTER_TOKEN` set. If the port is busy, set `OPENBRIDGE_GODOT_PORT` to another port and set `OPENBRIDGE_GODOT_URL` to `http://127.0.0.1:<port>` and `OPENBRIDGE_GODOT_HEALTH_URL` to `http://127.0.0.1:<port>/health` for the MCP server.

## 3. Start the MCP server

Windows:

```powershell
.`start-openbridge.bat
```

Linux/macOS:

```sh
sh ./start-openbridge.sh
```

Configure the AI host to use the Streamable HTTP MCP endpoint:

`http://127.0.0.1:8765/mcp`

## Available MCP tools

- `openbridge_status` — runtime and capability status.
- `openbridge_capabilities` — implemented vs planned capabilities.
- `godot_adapter_status` — authenticated local adapter health.
- `godot_get_editor_info` — Godot version, project name, and active scene.
- `godot_get_scene_tree` — bounded tree for the currently edited scene.
- `godot_read_script` — read a project-relative `.gd` file.
- `godot_preview_script_patch` — preview proposed script content without writing it.
- `godot_validate_script` — ask Godot's GDScript parser to validate proposed code without saving or executing it.
- `godot_apply_script_patch` — create or update a script after script writes are enabled in the dock. Updates require the current file's SHA-256. Existing scripts are backed up under `user://OpenBridge/backups`. This saves code but does not execute it.
- `godot_validate_scene_spec` — validate a bounded data-only scene description.
- `godot_validate_script_patch` — validate the shape and bounds of a proposed script patch.

## 4. Use guarded script writing

1. Ask the AI to read the relevant script and propose a change.
2. Call `godot_preview_script_patch` first.
3. Review the proposed content and current file state.
4. In the Godot dock, explicitly enable **Enable script writes (session only)**.
5. Call `godot_apply_script_patch` with `operation="create"` for a new file, or `operation="update"` plus the exact `expected_sha256` returned by reading the current file.
6. Review the saved change in Godot. The adapter does not run the code automatically.

Disable the session toggle when you are done. Generated GDScript is powerful; do not enable writes for an AI host you do not trust.

## Browser extension

Load the unpacked extension from `browser/extension` in a Chromium-based browser's extension developer mode. It currently captures only the active tab's title and URL after you click **Capture current tab**, then lets you copy that context. It does not read page contents, send data to a server, or invoke MCP tools yet.

## Troubleshooting

- **Python dependency install fails:** check internet access and retry.
- **MCP connection fails:** confirm the server is running at `127.0.0.1:8765` and your host uses Streamable HTTP.
- **Adapter token missing:** Godot and OpenBridge must inherit the same `OPENBRIDGE_ADAPTER_TOKEN`.
- **Adapter disconnected:** confirm the plugin is enabled, port 8766 is free, and `OPENBRIDGE_GODOT_URL` matches the plugin port.
- **No active scene:** open a scene in the Godot editor.
- **Script writes disabled:** enable the session-only toggle in the OpenBridge dock.
- **Parser/runtime validation:** not yet implemented; inspect the script in Godot and do not assume that a saved script is error-free.
