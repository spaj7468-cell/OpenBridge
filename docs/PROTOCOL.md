# MCP and adapter contract

**Status:** design draft. Tool names and schemas may change before alpha. Only tools listed as implemented by the running server should be treated as available.

## Principles

- Use the official Model Context Protocol and SDK.
- Advertise only implemented capabilities.
- Keep tools typed, bounded, and narrow.
- Return structured results plus a concise summary.
- Separate read-only, file-editing, scene-editing, and run/test operations.
- Validate inputs at both the MCP runtime and editor adapter.
- Treat AI-generated GDScript as supported output, but never run it silently.
- Require evidence from the editor/process before reporting success.

## Planned tool groups

### Runtime
- `openbridge_status` — runtime version, health, and registered adapters.
- `openbridge_capabilities` — implemented vs planned capabilities.
- `openbridge_diagnostics` — redacted runtime diagnostics.

### Godot read operations

The following read-only tools are implemented in the current prototype and require the Godot add-on to be enabled with a matching `OPENBRIDGE_ADAPTER_TOKEN`:
- `godot_get_editor_info`
- `godot_get_scene_tree`
- `godot_read_script`

The following additional read operations are planned:
- `godot_get_editor_info` — editor version, project identity, and connection state.
- `godot_get_scene_tree` — bounded summary of the active scene.
- `godot_list_node_types` — supported node types and compatibility information.
- `godot_list_project_files` — bounded listing of relevant files inside the selected project.
- `godot_read_script` — read a selected project-relative GDScript file, with size limits.

### Scene/resource operations
- `godot_plan_scene` — validate a structured scene description and return a change plan.
- `godot_apply_scene_plan` — apply an approved, non-stale plan.
- `godot_set_node_properties` — update allow-listed properties on known nodes.
- `godot_connect_signal` — connect a signal through editor APIs.
- `godot_inspect_resource` — report type, path, and relevant metadata for a project resource.

### GDScript authoring
- `godot_propose_script_patch` — produce a bounded patch proposal without writing files.
- `godot_preview_script_patch` — show the exact diff and validate target path/original file state.
- `godot_apply_script_patch` — apply an approved patch and create a recovery copy where applicable.
- `godot_validate_script` — ask Godot to parse/validate a script and return diagnostics.

### Run and debug
- `godot_run_project` — launch the selected project or scene after policy/approval checks.
- `godot_stop_project` — stop a run started by OpenBridge.
- `godot_get_debug_output` — return bounded, relevant output and errors from the current run.
- `godot_test_status` — report process exit status and test results when available.

These are planned names, not claims of current implementation.

## Error model

Every error should include a stable code, a safe message, and optional non-sensitive details. Categories:
- `INVALID_ARGUMENT`
- `CAPABILITY_UNAVAILABLE`
- `ADAPTER_DISCONNECTED`
- `PERMISSION_REQUIRED`
- `APPROVAL_REQUIRED`
- `RESOURCE_NOT_FOUND`
- `STALE_PLAN`
- `PATH_OUTSIDE_PROJECT`
- `VALIDATION_FAILED`
- `OPERATION_CONFLICT`
- `TIMEOUT`
- `CANCELLED`
- `INTERNAL_ERROR`

Never include API keys, full environment dumps, or unrelated project content in errors.

## Script patch contract

A patch request should include:
- project/session identifier;
- project-relative target path;
- expected original hash (or an explicit “new file” marker);
- patch content and size limit;
- a short explanation of intended behavior;
- whether the change is create/update/delete;
- validation and approval state.

The adapter must reject path traversal, unapproved absolute paths, stale hashes, oversized patches, and writes outside the selected project. Applying a patch must return the changed path, backup/recovery location where applicable, and validation result. Running changed code is a separate tool and approval boundary.

## Scene-spec validation

Before applying a scene plan, validate:
1. Schema version and required fields.
2. Allowed Godot classes and parent-child compatibility.
3. Property allow-list and value types.
4. Unique node names and path references.
5. Resource paths contained within the selected project.
6. Node count and tree-depth limits.
7. Destructive changes and overwrite behavior.
8. Current editor/project state still matches the plan token.

## Official references

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP specification](https://modelcontextprotocol.io/specification/)
- [Godot documentation](https://docs.godotengine.org/en/stable/)
- [Godot EditorPlugin](https://docs.godotengine.org/en/stable/classes/class_editorplugin.html)
