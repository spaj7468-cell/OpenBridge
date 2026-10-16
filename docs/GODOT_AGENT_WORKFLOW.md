# Godot agent workflow

**Status:** target design. The current OpenBridge runtime does not yet implement these editor tools.

This document defines the useful ZeroScript-style workflow OpenBridge is working toward: a user describes a game feature in chat, the agent operates Godot through real tools, and the model uses editor/test feedback to iterate. Unlike a no-code-only tool, OpenBridge is expected to write GDScript because gameplay and interactive UI commonly need code.

## Capability groups

### Inspect
- Read Godot version, project/scene status, selected nodes, and bounded scene tree.
- Read relevant project scripts and resource metadata.
- Retrieve parser errors and current run output.
- Ask for only the context needed for the task rather than uploading the whole project.

### Build
- Create and edit scenes, nodes, properties, resources, and signal connections.
- Create GDScript files and apply focused patches to existing scripts.
- Build interactive UI and gameplay systems through a combination of editor APIs and scripts.
- Preserve existing project structure and naming conventions.

### Verify
- Validate target paths and expected original file contents.
- Preview diffs and scene changes.
- Run Godot parser/editor checks.
- Launch and stop the selected project/scene through visible controls.
- Return actual logs, errors, and exit status to the agent.
- Apply focused fixes and re-run bounded tests.

## Agent loop

```text
User request
    ↓
Inspect relevant project state
    ↓
Plan scenes + resources + GDScript patches
    ↓
Validate paths, schemas, permissions, and stale state
    ↓
Preview exact changes
    ↓
User approval
    ↓
Apply changes + parser validation
    ↓
User-approved run/playtest
    ↓
Collect diagnostics
    ↓
Repair loop or clear completion report
```

## Proposed first tool set

These are design names only, not currently implemented MCP tools:

| Tool | Purpose | Side effects |
|---|---|---|
| `godot_get_editor_info` | Editor/project/version information | Read-only |
| `godot_get_scene_tree` | Bounded active scene tree | Read-only |
| `godot_read_script` | Read a selected project script | Read-only |
| `godot_propose_script_patch` | Propose code changes | No write |
| `godot_preview_script_patch` | Validate and display exact diff | No write |
| `godot_apply_script_patch` | Apply an approved patch | Writes project file |
| `godot_plan_scene` | Preview scene/node changes | No write |
| `godot_apply_scene_plan` | Apply approved scene plan | Changes project |
| `godot_validate_script` | Ask Godot to parse a script | Validation |
| `godot_run_project` | Run selected project/scene | Executes project code |
| `godot_get_debug_output` | Collect bounded logs/errors | Read-only |
| `godot_stop_project` | Stop OpenBridge-started run | Stops process |

## Rules that make the loop reliable

1. A tool call is not successful until the adapter returns a result.
2. Script creation/editing and code execution are separate operations.
3. Show diffs before applying; do not overwrite changes made since the plan was created.
4. Keep writes inside the selected project by default.
5. Back up before risky edits and provide a stop/cancel path.
6. Do not claim that generated GDScript is sandboxed.
7. Use parser/runtime diagnostics to repair errors; do not invent test results.
8. Keep operations bounded and stop after repeated failures, asking the user for direction.

## Current limitations

The current prototype connects MCP to an authenticated loopback Godot adapter and supports editor info, bounded active-scene inspection, GDScript reading/preview, and opt-in script writes with stale-hash checks and backups. The adapter still cannot create scenes, validate scripts with Godot's parser, launch a game, or collect debugger output. Manual testing in Godot 4 is still required. This document describes both implemented prototype capabilities and the remaining target workflow.
