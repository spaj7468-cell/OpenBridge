# Zero-script workflow

The goal is not to claim that software contains no code. The goal is that a user can complete supported development tasks without personally writing scripts.

## User journey

1. **Connect:** install the Godot add-on or browser extension and start the local OpenBridge runtime.
2. **Choose a target:** select the Godot project, active scene, or permitted browser tab.
3. **Describe the result:** for example, “Create a simple 2D player scene with a camera and collision.”
4. **Generate a structured plan:** the AI proposes nodes, properties, resources, and file changes as typed data.
5. **Review:** OpenBridge shows what will be created, changed, or overwritten.
6. **Approve:** the user confirms the plan.
7. **Apply:** the editor plugin uses supported editor APIs; the browser adapter performs only approved operations.
8. **Verify:** run validation and report success, warnings, or failures with actionable explanations.
9. **Undo or recover:** offer undo where supported and keep changes easy to inspect in version control.

## Example request

> Create a 2D player scene with a CharacterBody2D root, a Sprite2D child, a CollisionShape2D child, and a Camera2D. Do not generate scripts. Show me the node tree before applying it.

Expected plan preview:

```text
Player (CharacterBody2D)
├── Sprite2D
├── CollisionShape2D
└── Camera2D
```

The MVP should not invent a sprite, collision resource, or script if the user did not provide one. It should clearly show which resources are placeholders and which tasks require manual input.

## What “zero script” means

- The user does not need to write GDScript or JavaScript for supported operations.
- AI output is converted into structured data and validated.
- The system uses known editor APIs and approved commands.
- Unsupported tasks are reported honestly rather than silently falling back to generated code.

## Limits

Some Godot behaviors require custom logic that cannot be represented by a node tree and properties alone. The product should explain the limitation and offer safe visual configuration or a clearly marked future capability, rather than claiming every possible game feature can be created without code.
