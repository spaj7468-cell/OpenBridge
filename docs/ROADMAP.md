# Roadmap

The roadmap distinguishes intent from shipped functionality. No item is considered complete until its acceptance criteria have been tested.

## M0 — Repository foundation
- [x] Define positioning and system boundaries.
- [x] Define a zero-script user workflow.
- [x] Document planned architecture, protocol, compatibility, and security.
- [ ] Select and add a license.
- [ ] Add contribution templates and baseline CI.

## M1 — Local runtime
- [ ] Implement the MCP server using the official MCP SDK.
- [ ] Add configuration validation and a health/status command.
- [ ] Add one-command launch scripts for Windows and Unix-like systems.
- [ ] Bind to loopback by default and report the actual listening address.
- [ ] Add unit tests for validation, errors, and permissions.
- **Acceptance:** a clean checkout can install dependencies, start the service, query status, and shut down without exposing a network listener to the LAN.

## M2 — Godot read-only integration
- [ ] Add a Godot 4 editor plugin with an explicit enable/disable control.
- [ ] Report Godot version, project path (redacted where needed), active scene, and plugin version.
- [ ] Inspect the current scene tree with bounded output.
- [ ] Add connection status and useful diagnostics.
- **Acceptance:** a user can connect the editor to the local runtime without writing GDScript.

## M3 — Structured scene creation
- [ ] Define and version the scene-spec schema.
- [ ] Validate allowed node types, property types, names, resource paths, depth, and node count.
- [ ] Show a human-readable action plan before changing the project.
- [ ] Create a scene and nodes using editor APIs.
- [ ] Support undo/recovery and report exactly what changed.
- **Acceptance:** a test project can create a simple 2D scene from structured data; invalid input causes no project mutation.

## M4 — Browser extension
- [ ] Define supported browser targets and manifest permissions.
- [ ] Add a user-triggered connection to the local service.
- [ ] Display the connected runtime and available actions.
- [ ] Limit actions to explicit host permissions and supported origins.
- [ ] Add a clear disconnect and permission reset flow.
- **Acceptance:** no page is inspected or changed without a user-triggered action and appropriate permission.

## M5 — DeepSeek setup and AI workflow
- [ ] Document the current DeepSeek API setup using official documentation.
- [ ] Keep provider credentials outside source code and extension bundles.
- [ ] Define a model-independent tool contract.
- [ ] Add a plan → validate → preview → approve → execute loop.
- [ ] Show provider/network failures without pretending actions succeeded.
- **Acceptance:** a supported host can propose a structured scene, OpenBridge validates it, and the Godot adapter executes only after approval.

## M6 — Quality and release
- [ ] Automated tests on supported operating systems.
- [ ] Test clean install, upgrade, disconnect, and corrupted configuration.
- [ ] Add signed/reproducible release artifacts where practical.
- [ ] Publish compatibility matrix and known limitations.
- [ ] Tag a first alpha release only after the above acceptance checks pass.

## Out of scope for the first release
- arbitrary shell access;
- arbitrary generated-script execution;
- silent browsing or whole-profile collection;
- automatic destructive edits without approval;
- claims that every browser, editor, or AI host is compatible.
