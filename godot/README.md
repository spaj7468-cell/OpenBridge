# Godot adapter smoke-test project

This folder is a small Godot 4 project that loads the OpenBridge add-on. It is useful for checking whether the plugin parses and appears in the editor.

## Open it

1. Open Godot 4.
2. Import/open this folder's `project.godot`.
3. Open `scenes/SmokeTest.tscn`.
4. The OpenBridge dock should appear. Without `OPENBRIDGE_ADAPTER_TOKEN`, the adapter intentionally does not listen on a port.
5. To test the local bridge, set a random `OPENBRIDGE_ADAPTER_TOKEN` of at least 32 characters before launching Godot and the OpenBridge MCP server.

The smoke-test project does not prove compatibility with every Godot 4 release. CI uses a pinned Godot version for a repeatable syntax/import check; test on the Godot version you use before relying on it for real projects.
