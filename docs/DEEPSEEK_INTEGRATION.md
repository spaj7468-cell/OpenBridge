# DeepSeek integration

**Status:** design and setup notes. OpenBridge does not yet call the DeepSeek API directly.

## Intended role

DeepSeek is a possible first AI provider for the Godot agent. The model should inspect relevant project context, request tools, write or edit GDScript when needed, build scenes, run approved tests, and use real diagnostics to repair failures. The core tool contract remains provider-independent.

Never place an API key in browser extension files, source control, a Godot project, or client-visible logs.

## Planned agent loop

1. User requests a feature, such as a player controller and main menu.
2. The agent inspects relevant scenes, scripts, project settings, and errors.
3. The model proposes a plan and script patches.
4. OpenBridge validates tool arguments, target paths, patch size, expected file state, and permissions.
5. OpenBridge shows a diff and scene/resource change preview.
6. The user approves edits under the configured policy.
7. The Godot adapter applies changes and runs parser/editor validation.
8. The user approves running the changed project/scene.
9. Godot returns actual logs, errors, and test results.
10. The agent proposes focused repairs and repeats within bounded limits.

Generated GDScript is expected and supported. It must not bypass path validation, preview, approval, or execution policy. Tool calls are requests, not permission to perform every requested action.

## Tool calls are requests, not execution

DeepSeek's official Tool Calls documentation explains that the model returns a tool name and arguments; the integrating application must provide the tool implementation and return results to the model. OpenBridge must validate the tool name, JSON arguments, permissions, and current editor state before dispatch.

## Configuration principles

- Use API base URL and model IDs currently listed in official DeepSeek documentation.
- Keep credentials in an environment variable or trusted local secret store.
- Never include API keys in extension manifests, frontend JavaScript, screenshots, crash reports, or Git history.
- Make external API use visible to the user.
- Provide clear errors for missing credentials, network failures, rate limits, malformed output, and unsupported tool calls.
- Bound prompt size, patch size, and returned diagnostics.
- Do not send full project directories by default; request only relevant files/context.

## Thinking-mode compatibility

DeepSeek documents that when tool calls are used in thinking mode, the relevant reasoning field must be preserved in subsequent API requests. The provider adapter must follow the current official protocol exactly and test both thinking and non-thinking modes.

## Official references

- [DeepSeek Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/)
- [DeepSeek Chat Completions API](https://api-docs.deepseek.com/api/create-chat-completion/)
- [DeepSeek Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK — v1.x maintenance line](https://py.sdk.modelcontextprotocol.io/v1/)
