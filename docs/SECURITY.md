# Security and privacy requirements

OpenBridge connects an AI host to a local Godot editor and potentially a browser. Treat this as a security-sensitive boundary.

## Threat model

Potential risks include:
- a malicious or compromised AI host requesting unexpected actions;
- prompt injection in project files, documentation, imported assets, or browser content;
- a browser page attempting to reach or abuse a local service;
- forged local requests or cross-origin requests;
- unsafe scene specifications, script patches, or path traversal;
- accidental disclosure of provider credentials or project source;
- destructive edits, resource overwrites, or excessive project reads;
- generated GDScript performing actions the user did not expect.

## Required safeguards

### Local service
- Bind to loopback by default, not `0.0.0.0`.
- Do not assume a local port is private or trusted.
- Authenticate adapter connections with a per-session secret or another reviewed mechanism.
- Validate request origin where applicable and use an explicit allowed-origin policy.
- Apply bounded request sizes, timeouts, and rate limits.

### Permissions and approvals
- Separate read-only tools, file edits, scene mutations, and run/test operations.
- Show exact script diffs and scene changes before applying.
- Keep script writes disabled by default; require the user to enable the editor-session write toggle.
- Require the expected SHA-256 for updates and save a backup before overwriting existing scripts.
- Require approval for destructive operations, overwrites, deletes, execution of changed/generated code, and actions outside the selected project.
- Provide a visible stop/disconnect control and a non-secret audit log.
- Never claim code is safe simply because it parses.

### Project files and GDScript
- Canonicalize paths and verify they remain inside the selected workspace.
- Reject traversal paths, unexpected symlinks, and unapproved absolute paths.
- Use size limits and expected-original hashes for patches to avoid overwriting concurrent edits.
- Back up changed files or clearly rely on user-enabled version control.
- Keep script editing separate from project execution.
- Godot GDScript is powerful and must not be described as sandboxed. Run changed code only through a visible, approved action.
- Do not provide unrestricted shell access as a shortcut for editor features.

### Browser extension
- Request minimum manifest permissions.
- Prefer user-triggered active-tab access over broad host permissions.
- Never collect all browsing history or silently read every tab.
- Show what information will be sent to an AI provider.
- Treat webpage text as untrusted content, not instructions that override user intent.

### Credentials and telemetry
- Never commit API keys, tokens, session secrets, or real user data.
- Do not place provider keys in browser extension source or client-side bundles.
- Make telemetry opt-in; the initial design should work without analytics.
- Redact secrets and unrelated project data from logs and errors.

## Release security checklist

- [ ] Threat model reviewed for each new tool.
- [ ] Permissions documented next to each capability.
- [ ] Input validation and boundary tests added.
- [ ] Destructive edits and execution require approval.
- [ ] No secrets in repository, logs, or test fixtures.
- [ ] Dependency versions and licenses reviewed.
- [ ] Local endpoint tested against unauthorized and cross-origin requests.
- [ ] Recovery behavior tested after disconnect or partial failure.
- [ ] Generated-script workflow tested with backups, diffs, cancellation, and error reporting.

## Reporting a vulnerability

Please do not publish exploit details in a public issue before maintainers have had a chance to assess the report. Add a private security contact before distributing the project.
