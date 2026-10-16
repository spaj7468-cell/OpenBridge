# Roadmap

OpenBridge is being shaped as a **ZeroScript-style AI agent for Godot**. The agent is expected to write and edit GDScript when game logic or UI behavior requires it. “Zero script” means the user does not have to write code manually; it does not mean generated scripts are forbidden.

A roadmap item is complete only when the acceptance criteria have been tested in a real Godot project.

## M0 — Repository foundation
- [x] Define product positioning and system boundaries.
- [x] Add initial MCP runtime, data-only scene-spec validator, sample spec, and tests.
- [x] Add initial Godot editor-panel scaffold and browser popup scaffold.
- [x] Implement authenticated loopback read-only adapter endpoints for editor info, scene tree, and script reading.
- [x] Expose read-only Godot info/tree/script tools through MCP.
- [x] Add CI workflow definition.
- [ ] Select and add a license.
- [ ] Confirm the latest CI workflow passes.

## M1 — Local runtime and bridge security
- [x] Implement initial MCP server and status/capability tools.
- [x] Add bounded scene-spec validation.
- [x] Add quick launch scripts.
- [ ] Verify clean installation and MCP handshake.
- [ ] Implement authenticated local adapter sessions and origin checks.
- [ ] Add request limits, timeouts, disconnect handling, and security tests.
- **Acceptance:** a clean checkout starts locally, exposes only loopback by default, and handles connection failures clearly.

## M2 — Godot read-only agent
- [x] Add Godot editor plugin UI scaffold.
- [ ] Connect plugin to the local bridge with an authenticated session.
- [ ] Report Godot version, project path (redacted where appropriate), active scene, and plugin version.
- [ ] Inspect bounded scene trees and relevant project files.
- [ ] Read selected GDScript files and surface parser/runtime errors.
- [ ] Add connection status, logs, cancellation, and useful diagnostics.
- **Acceptance:** the agent can inspect an open Godot project without changing it and can return accurate editor data.

## M3 — Scene and resource editing
- [ ] Create scenes and nodes through Godot editor APIs.
- [ ] Set allow-listed properties, attach resources, and connect signals.
- [ ] Validate node-parent and property compatibility against the running Godot version.
- [ ] Show a human-readable plan before changes.
- [ ] Add backups, change summaries, undo/recovery, and stale-plan detection.
- **Acceptance:** a test project can be changed from structured plans, invalid input causes no mutation, and recovery is demonstrated.

## M4 — GDScript agent (core ZeroScript parity)
- [x] Add a read-only tool to read a selected project-relative script.
- [ ] Add relevant surrounding context and editor diagnostics.
- [ ] Create a new GDScript file from an AI-produced patch.
- [ ] Edit existing scripts using unified diffs or structured patch operations.
- [ ] Validate paths and prevent edits outside the selected project.
- [ ] Run Godot's parser/editor validation and return precise diagnostics.
- [ ] Show the complete diff and require confirmation for applying edits.
- [ ] Keep script writing separate from running scripts or launching the project.
- **Acceptance:** the agent can preview and apply a small gameplay script, show recoverable changes, pass parser validation, and report errors honestly. Current write/preview operations are implemented in the prototype; parser validation and Godot manual verification remain open.

## M5 — Run, test, and repair loop
- [ ] Launch the current project or selected scene through Godot editor/run APIs.
- [ ] Capture relevant output, parser errors, runtime errors, and exit status.
- [ ] Support stop/cancel and bounded execution time.
- [ ] Return diagnostics to the AI for a targeted repair proposal.
- [ ] Add a repeatable smoke-test project and regression tests.
- **Acceptance:** a deliberately broken test project produces a useful error report; a repair is reviewed, applied, and re-tested.

## M6 — Assets, UI, and reusable components
- [ ] Add safe resource discovery and import-status tools.
- [ ] Support UI node creation and GDScript-driven interactions.
- [ ] Provide reusable, documented templates for movement, camera, menus, dialogue, inventory, save/load, and interaction systems.
- [ ] Support asset insertion only from explicit user-selected sources or permitted libraries.
- [ ] Track placeholders separately from finished assets.
- **Acceptance:** a sample 2D game can be assembled using scenes, scripts, UI, and resources without the user manually writing code.

## M7 — AI provider workflow
- [ ] Document the current DeepSeek API setup using official docs.
- [ ] Keep credentials outside source code, Godot projects, and browser bundles.
- [ ] Define a model-independent tool contract.
- [ ] Implement plan → inspect → patch → validate → preview → approve → run → diagnose.
- [ ] Return tool results to the model and continue the agent loop until completion or a clear blocker.
- **Acceptance:** a supported host can complete a bounded task through real tool calls and verify the result in Godot.

## M8 — Browser extension and release quality
- [ ] Define supported browser targets and minimal permissions.
- [ ] Add a user-triggered connection to OpenBridge.
- [ ] Test clean install, upgrade, disconnect, corrupted config, and supported OSes.
- [ ] Publish compatibility matrix and known limitations.
- [ ] Tag an alpha only after acceptance checks pass.

## Out of scope for the first release
- unrestricted shell or arbitrary computer control;
- silent execution of generated code;
- unreviewed destructive edits;
- reading the entire project or sending it to a provider by default;
- claims that every Godot version, browser, or AI host is compatible.
