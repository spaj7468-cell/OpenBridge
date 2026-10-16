# Quick start

**Current status:** OpenBridge is an early prototype connecting selected browser AI chats to a local Godot 4 editor plugin. The extension prepares a task for the AI, captures a proposed GDScript response, asks Godot to parse it, then offers an explicit Apply action. Site selectors can change, so each provider still needs manual testing.

## Windows: one launcher

1. Download or clone this repository.
2. Double-click **start-openbridge.bat**.
3. If you want the launcher to start Godot too, paste the folder path of your Godot project when prompted. If Godot is not on PATH, provide the Godot 4 executable path.
4. The launcher creates a local token once, stores it under **%LOCALAPPDATA%\\OpenBridge\\adapter-token.txt**, copies it to the clipboard when supported, and starts the MCP and browser gateway services.
5. If you supplied a project path, the launcher copies the OpenBridge add-on into that project when it is not already installed. In Godot, enable **OpenBridge** under **Project → Project Settings → Plugins** once, and keep the launcher window open.
6. Install the browser extension by opening **chrome://extensions**, enabling Developer mode, choosing **Load unpacked**, and selecting **browser/extension**.
7. Open a supported AI website (initial best-effort support: DeepSeek, ChatGPT, Claude, Gemini, Perplexity, Qwen, Kimi, Poe). Open the extension popup, paste the local token, save it, and check connection.

The token is a local secret. Never paste it into an AI chat or commit it to a repository. Do not expose local services to a public network.

## What the browser workflow does

1. Type a task into the OpenBridge panel injected on the AI chat page.
2. Click **Prepare task for AI**, review the prompt placed in the site's composer, then submit it using the site's normal send button.
3. Ask the AI to return one complete GDScript code block whose first line is a comment such as: **# OpenBridge-Path: res://scripts/main_menu.gd**.
4. Click **Check latest answer in Godot**. OpenBridge extracts the proposed script and asks the connected Godot editor to parse it.
5. If the parser accepts it, review the file path and click **Apply in Godot**. Script writes must also be enabled in the OpenBridge dock for the current Godot session.
6. Check the result in Godot. The bridge does not automatically run generated code.

The extension does not directly run a model or make provider API calls. The AI conversation still happens on the provider's website. The browser adapter is best-effort because AI providers can change their page structure; if a composer or response is not detected, use the provider's normal chat and copy the response manually only after reviewing it.

## Endpoints

- MCP Streamable HTTP: http://127.0.0.1:8765/mcp
- Browser gateway: http://127.0.0.1:8767
- Godot adapter: http://127.0.0.1:8766

The browser gateway accepts only authenticated requests and binds to 127.0.0.1. It uses the same OPENBRIDGE_ADAPTER_TOKEN as the Godot plugin. For manual startup, set the same random token in the environment of both processes before launching them.

## Requirements

- Windows launcher: Python 3.10+ and PowerShell
- Godot 4.x editor
- Chromium-based browser for the initial Manifest V3 extension build
- Internet access for the first dependency installation

## Current limitations

- AI-site DOM selectors are not guaranteed across provider updates or every browser locale.
- Script changes are limited to GDScript files; the bridge does not create scenes or nodes yet.
- Godot parsing is not a guarantee of correct runtime behavior.
- Script writing remains disabled until enabled in the Godot dock; code is not executed automatically.
- Linux/macOS launcher token setup is not yet as automated as the Windows launcher.
