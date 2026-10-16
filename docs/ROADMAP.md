# Roadmap

The roadmap distinguishes intent from shipped functionality. No item is considered complete until its acceptance criteria have been tested.

## M0 — Repository foundation
- [x] Define positioning and system boundaries.
- [x] Define a zero-script user workflow.
- [x] Document planned architecture, protocol, compatibility, and security.
- [x] Add initial runtime package, scene-spec validator, sample specification, and tests.
- [x] Add initial Godot editor-panel scaffold and browser popup scaffold.
- [x] Add a CI workflow definition.
- [ ] Select and add a license.
- [ ] Confirm the CI workflow passes on GitHub Actions.

## M1 — Local runtime
- [x] Implement an initial MCP server using the official MCP Python SDK.
- [x] Add runtime status and capability discovery tools.
- [x] Add a bounded, data-only scene-spec validator.
- [x] Add one-command launch scripts for Windows and Unix-like systems.
- [ ] Verify installation and MCP handshake from a clean checkout.
- [ ] Add authenticated adapter connections and a reviewed local bridge transport.
- [ ] Add stronger tests for invalid payloads, bounds, and permission policy.
- **Acceptance:** a clean checkout can install dependencies, start the service, discover tools, validate a scene specification, and shut down without exposing a network listener to the LAN.

## M2 — Godot read-only integration
- [x] Add a Godot 4 editor plugin UI scaffold.
- [ ] Implement a reviewed local adapter transport and health endpoint.
- [ ] Report Godot version, plugin version, and active scene.
- [ ] Inspect the current scene tree with bounded output.
- [ ] Add connection status and useful diagnostics.
- **Acceptance:** a user can connect the editor to the local runtime without writing GDScript.

## M3 — Structured scene creation
- [x] Draft the versioned scene-spec format and sample.
- [x] Validate a safe subset of node types and properties without mutation.
- [ ] Validate node-parent compatibility against the active Godot version.
- [ ] Show a human-readable action plan before changing the project.
- [ ] Create a scene and nodes using editor APIs.
- [ ] Support undo/recovery and report exactly what changed.
- **Acceptance:** a test project can create a simple 2D scene from structured data; invalid input causes no project mutation.

## M4 — Browser extension
- [x] Add a minimal Manifest V3 popup scaffold with no website permissions.
- [ ] Define supported browser targets and reviewed permissions.
- [ ] Add a user-triggered connection to the local service.
- [ ] Display connected runtime and available actions.
- [ ] Limit actions to explicit host permissions and supported origins.
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
