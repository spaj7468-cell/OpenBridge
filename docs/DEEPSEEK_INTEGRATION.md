# DeepSeek integration

**Status:** design and setup notes. OpenBridge does not yet call the DeepSeek API directly.

## Intended role

DeepSeek is the first planned AI provider for the zero-script workflow. The model should propose a structured scene specification and may request tools, but the OpenBridge runtime—not the model—validates and executes each operation.

The provider adapter should remain separate from the MCP server so users can also connect another MCP-compatible host. Never place an API key in browser extension files, source control, a Godot project, or client-visible logs.

## Planned flow

1. User supplies a request such as “Create a 2D player scene with a camera.”
2. The AI proposes a versioned, data-only scene specification.
3. OpenBridge validates its schema, limits, node types, and properties.
4. The editor adapter checks compatibility against the active Godot version.
5. OpenBridge shows a plan preview and waits for approval.
6. Only approved, allow-listed operations are sent to the editor plugin.
7. Results and errors are returned to the AI host for a concise explanation.

The AI must not be allowed to bypass validation by returning GDScript, JavaScript, shell commands, or arbitrary file contents.

## Tool calls are requests, not execution

DeepSeek's official Tool Calls documentation explains that the model returns a tool name and arguments; the integrating application must provide the tool's actual implementation and return its result to the model. Therefore OpenBridge must validate the tool name, JSON arguments, permissions, and current editor state before dispatch.

## Configuration principles

- Use the API base URL and model IDs currently listed in the official DeepSeek documentation rather than hard-coding assumptions in the UI.
- Keep credentials in an environment variable or a trusted local secret store.
- Do not include API keys in extension manifests, frontend JavaScript, screenshots, crash reports, or Git history.
- Make external API use visible to the user.
- Provide a clear error for missing credentials, network failures, rate limits, malformed output, and unsupported tool calls.
- Bound the size of prompts, scene specifications, and returned data.
- Do not send full project directories or whole browser pages by default.

## Thinking-mode compatibility

DeepSeek documents that when tool calls are used in thinking mode, the relevant reasoning field must be preserved in subsequent API requests. The provider adapter must follow the current official protocol exactly and test both thinking and non-thinking modes instead of assuming they share identical message handling.

## Official references

- [DeepSeek Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/)
- [DeepSeek Chat Completions API](https://api-docs.deepseek.com/api/create-chat-completion/)
- [DeepSeek Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK — v1.x maintenance line](https://py.sdk.modelcontextprotocol.io/v1/)
