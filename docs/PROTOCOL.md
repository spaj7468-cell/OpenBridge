# MCP and adapter contract

**Status:** design draft. Tool names and schemas may change before the first alpha.

## Principles

- Use the official Model Context Protocol specification and SDK rather than inventing a competing MCP transport.
- Advertise only implemented capabilities.
- Keep tools small, typed, and narrowly scoped.
- Return machine-readable results plus concise human-readable summaries.
- Separate read-only operations from mutating operations.
- Validate inputs again at the adapter boundary.

## Planned tool groups

### Runtime
- `openbridge_status` — runtime version, health, and registered adapters.
- `openbridge_capabilities` — supported operations and adapter versions.
- `openbridge_diagnostics` — redacted diagnostic information.

### Godot read operations
- `godot_get_editor_info` — editor version and connection state.
- `godot_get_scene_tree` — bounded summary of the active scene.
- `godot_list_node_types` — only node types the adapter supports.

### Godot mutations
- `godot_plan_scene` — validate a structured scene description and return a proposed change plan without applying it.
- `godot_apply_scene_plan` — apply a previously validated plan after user approval.
- `godot_set_node_properties` — update allow-listed properties on known nodes.
- `godot_save_scene` — save only to a path inside the selected project and according to the configured approval policy.

These are planned names, not claims of current implementation.

## Error model

Every error should include a stable code, a safe message, and optional non-sensitive details. Proposed categories:

- `INVALID_ARGUMENT`
- `CAPABILITY_UNAVAILABLE`
- `ADAPTER_DISCONNECTED`
- `PERMISSION_REQUIRED`
- `APPROVAL_REQUIRED`
- `RESOURCE_NOT_FOUND`
- `OPERATION_CONFLICT`
- `TIMEOUT`
- `INTERNAL_ERROR`

Do not include API keys, full environment dumps, or unfiltered browser page content in errors.

## Scene-spec validation

Before applying a scene plan, validate:

1. Schema version and required fields.
2. Allowed Godot class names and parent-child compatibility where known.
3. Property allow-list and property value types.
4. Node-name uniqueness and path references.
5. Resource paths contained within the selected project.
6. Maximum node count and tree depth.
7. Whether the action is destructive or overwrites existing content.
8. The current editor/project state has not changed since the plan was generated.

A plan should be bound to a project identity and a short-lived state/version token so stale plans cannot accidentally modify a different project.

## Official references

- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
- [MCP specification](https://modelcontextprotocol.io/specification/)
- [Godot documentation](https://docs.godotengine.org/en/stable/)
- [Godot EditorPlugin class](https://docs.godotengine.org/en/stable/classes/class_editorplugin.html)
