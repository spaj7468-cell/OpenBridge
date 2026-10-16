# OpenBridge architecture

**Status:** target architecture; current implementation is still an early prototype.

OpenBridge follows the useful agent pattern demonstrated by ZeroScript: an AI chat issues tool calls, a local bridge dispatches them to the editor, and results/errors return to the model so it can continue. Godot-specific parity means the agent can inspect and modify scenes, write GDScript, run the project, and use actual diagnostics to iterate.

## 1. Components

### MCP runtime
The runtime exposes typed tools, validates arguments, checks permission policy, dispatches operations to adapters, and returns structured results. A model request is not itself authorization to perform an action.

### Godot EditorPlugin adapter
The plugin owns editor-aware operations:
- editor/project information and active scene;
- bounded scene-tree and resource inspection;
- create/edit scenes, nodes, properties, resources, and signals;
- read, create, and edit GDScript files;
- run parser/editor validation;
- launch and stop a project/scene and collect relevant diagnostics;
- return exact operation results, errors, and recovery hints.

The plugin is the right place to use Godot editor APIs. File and script operations must remain inside the selected project unless the user explicitly selects another workspace.

### Script authoring and execution
AI-written GDScript is a first-class capability. Many requested features—movement, UI interaction, inventory logic, dialogue flow, save/load, and gameplay systems—cannot be implemented by node creation alone.

Keep these actions separate:
1. **Read** a user-selected/relevant script.
2. **Propose** a new file or patch.
3. **Validate** syntax and project-relative paths.
4. **Preview** a diff and affected files.
5. **Apply** after the configured approval policy.
6. **Run/test** only as a separate visible action.
7. **Inspect diagnostics** and propose a targeted repair.

Godot scripts can perform powerful project-level operations, so do not claim GDScript is sandboxed. Use explicit user approval for running generated or changed code, a clear stop control, project backups/version control, and a narrow local bridge. Never silently execute code merely because a model returned it.

### Local adapter bridge
The runtime and editor plugin need a reviewed localhost protocol with authenticated sessions, origin checks, message-size limits, timeouts, and disconnect handling. Loopback binding alone is not sufficient authentication. Do not advertise an authenticated bridge until the implementation and tests exist.

### Browser adapter
The extension remains a separate future component. It should use minimum permissions, active-tab/user-triggered access, and explicit origins. It is not required for the first useful Godot agent milestone.

### AI provider adapter
DeepSeek is a possible first provider, but tool schemas should remain model-independent. Keep API credentials in a trusted local configuration or environment and never bundle them into the extension or a Godot project.

## 2. Agent loop

1. User describes a desired result.
2. Agent inspects only relevant project context.
3. Model chooses tools and proposes a plan or code patch.
4. OpenBridge validates schemas, paths, permissions, and editor state.
5. OpenBridge previews scene/file changes and asks for approval where required.
6. Adapter applies approved edits and returns structured results.
7. Godot parser/editor validation checks the changes.
8. User-approved run/playtest produces logs and errors.
9. Agent uses those diagnostics to propose a focused repair.
10. Repeat until tests pass or report a clear blocker.

Tool calls must be real operations with observable outcomes, not text pretending that the project changed.

## 3. Scene and script contracts

Structured scene specifications are useful for deterministic node-tree edits. They complement rather than replace GDScript. Script edits should use project-relative paths and a patch/diff representation, not unrestricted file writes. Before applying a patch, validate:
- the selected project root and canonical target path;
- file size and patch bounds;
- expected original content/hash to avoid overwriting concurrent user changes;
- file extension and operation type;
- whether the operation creates, changes, or deletes content;
- the approval requirement and backup/recovery strategy.

A scene plan and a script patch should carry a short-lived project/state token so stale plans cannot accidentally modify another project.

## 4. Error and task handling

- Return stable error codes and safe, actionable messages.
- Distinguish parser errors, runtime errors, missing resources, adapter disconnects, timeouts, and permission denials.
- Use bounded retries; do not loop indefinitely.
- Support cancellation and report partial changes after failure.
- Redact credentials and unrelated project data from logs.
- Never claim success without a result from the editor or test process.

## 5. Initial implementation order

Build a secure read-only editor connection first; then add diff-previewed GDScript editing and scene/resource operations. Add run/debug feedback as a separate milestone. Browser automation is secondary to a working Godot agent.
