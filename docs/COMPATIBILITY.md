# Compatibility policy

This matrix tracks targets the project intends to support. An entry is not supported until it has been tested on a documented version.

| Target | Planned support | Current status |
|---|---|---|
| Godot 4.x editor plugin | Read-only editor info, scene tree, and GDScript access | Implemented prototype; manual version testing pending |
| Godot 4.x editor plugin | Scene/node mutation and run/debug operations | Planned |
| MCP-compatible AI host | MCP tool discovery and invocation | Planned |
| DeepSeek API | Provider setup and structured-output workflow where supported | Planned |
| Chromium browsers with Manifest V3 | Active-tab title/URL capture and copy | Implemented prototype; manual browser testing pending |
| Microsoft Edge | Manifest V3 active-tab helper | Expected compatibility; not yet tested |
| Google Chrome | Manifest V3 active-tab helper | Expected compatibility; not yet tested |
| Firefox | Separate manifest/API compatibility adjustments | Planned |
| Yandex Browser | Verify extension API and packaging compatibility before claiming support | Planned |
| Browser-to-MCP tool execution | Authenticated browser actions through OpenBridge | Planned |
| Windows | One-command launcher | Planned |
| Linux/macOS | Launcher support after Windows MVP | Planned |

## Compatibility rules

- Publish tested versions, not broad assumptions such as “works in every browser.”
- Keep browser-specific manifests and APIs behind an adapter layer.
- Report unsupported capabilities explicitly.
- Test installation, connection, disconnect, update, and permission changes.
- Recheck official platform policies and API changes before each release.

## Reference documentation

- [Godot stable documentation](https://docs.godotengine.org/en/stable/)
- [Microsoft Edge extensions documentation](https://learn.microsoft.com/en-us/microsoft-edge/extensions-chromium/)
- [Chrome extensions documentation](https://developer.chrome.com/docs/extensions/)
- [Firefox WebExtensions documentation](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions)
- [Yandex Browser extension documentation](https://yandex.com/dev/browser/)
- [DeepSeek API documentation](https://api-docs.deepseek.com/)
- [MCP documentation](https://modelcontextprotocol.io/)
