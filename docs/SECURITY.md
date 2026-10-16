# Security and privacy requirements

OpenBridge connects AI hosts to a local editor and browser. Treat this as a security-sensitive boundary, even when the project is free and runs locally.

## Threat model

Potential risks include:
- a malicious or compromised AI host requesting unexpected actions;
- prompt injection in a website, project file, README, or imported asset;
- a browser page attempting to reach or abuse a local service;
- a forged local request or cross-origin request;
- an unsafe scene specification or path traversal;
- accidental disclosure of DeepSeek or other provider credentials;
- destructive edits, resource overwrites, or excessive project reads.

## Required safeguards

### Local service
- Bind to loopback by default, not `0.0.0.0`.
- Do not assume that a local port is private or trusted.
- Authenticate adapter connections with a per-session secret or another reviewed mechanism.
- Validate the request origin where applicable and use an explicit allowed-origin policy.
- Do not expose administrative endpoints to the public network.
- Use bounded request sizes, timeouts, and rate limits.

### Permissions and approvals
- Separate read-only tools from mutations.
- Require user approval for destructive operations, overwrites, saves outside a new-file flow, and actions with external side effects.
- Provide a preview of the exact intended changes.
- Keep a visible audit log of actions without secrets.
- Provide a stop/disconnect control.

### Project files
- Canonicalize paths and verify they remain inside the selected workspace.
- Reject traversal paths, unexpected symlinks, and unapproved absolute paths.
- Never execute generated GDScript, JavaScript, shell commands, or project scripts as a shortcut.
- Limit scene-spec size, tree depth, node count, and resource references.

### Browser extension
- Request minimum manifest permissions.
- Prefer user-triggered active-tab access over broad host permissions.
- Never collect all browsing history or silently read every tab.
- Show what information will be sent to the AI provider.
- Do not treat webpage text as trusted instructions.

### Credentials and telemetry
- Never commit API keys, tokens, session secrets, or real user data.
- Do not place provider keys in browser extension source or client-side bundles.
- Make telemetry opt-in; the initial design should work without analytics.
- Redact secrets from logs and error messages.

## Release security checklist

- [ ] Threat model reviewed for each new tool.
- [ ] Permissions documented next to each capability.
- [ ] Input validation and boundary tests added.
- [ ] Destructive actions require approval.
- [ ] No secrets in repository, logs, or test fixtures.
- [ ] Dependency versions and licenses reviewed.
- [ ] Local endpoint tested against unauthorized and cross-origin requests.
- [ ] Recovery behavior tested after disconnect or partial failure.

## Reporting a vulnerability

Please do not publish exploit details in a public issue before maintainers have had a chance to assess the report. Add a private security contact before the project is distributed to external users.
