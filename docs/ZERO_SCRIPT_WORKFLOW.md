# Zero-script workflow

“Zero script” means the user does not need to manually write code. It does **not** mean the AI must avoid scripts. In Godot, custom gameplay and interactive interfaces often require GDScript, so OpenBridge should generate and edit it as part of the agent workflow.

The product target follows the practical pattern of ZeroScript for Roblox Studio: AI chat → browser/local bridge → editor tools → actual result → diagnostics returned to AI.

## User journey

1. **Connect:** install the Godot add-on and start the local OpenBridge runtime.
2. **Choose a project:** the user selects the Godot project and relevant scene.
3. **Describe the result:** for example, “Make a 2D character that moves with WASD, has a camera, and shows a health bar.”
4. **Inspect:** the agent checks the current scene, scripts, resources, and relevant errors instead of blindly replacing files.
5. **Plan:** it lists scene changes, new scripts, edits, resources, and tests.
6. **Preview:** show a scene-tree summary and exact GDScript diffs.
7. **Approve:** the user confirms the changes according to the configured policy.
8. **Apply:** the editor adapter creates nodes/resources and writes approved script patches.
9. **Validate:** run parser checks and inspect project diagnostics.
10. **Test:** launch the scene/project only through a visible run action; collect relevant logs and errors.
11. **Repair:** the AI proposes focused fixes based on actual results.
12. **Recover:** keep backups/version-control diffs and allow stopping the agent.

## Example request

> Create a 2D player scene with movement, collision, camera follow, and a clean health-bar UI. Write the GDScript needed, connect everything, run the scene, and fix any errors. Show me the changes before applying them.

Expected plan preview:
- Create or update the player scene and required nodes.
- Add a movement script and health/UI logic if the project does not already contain equivalent systems.
- Configure collision and camera nodes.
- Show exact files and diffs.
- Validate scripts before running.
- Ask for approval before applying and launching changed code.
- Return Godot errors and test outcome rather than claiming the scene works without testing.

## Core behavior

- The user describes desired functionality in natural language.
- The AI may generate GDScript, scene specifications, UI layouts, and resource configuration.
- OpenBridge validates file paths, patch bounds, target state, and tool permissions.
- Script editing and script execution are distinct actions.
- The adapter returns actual parser/runtime output so the AI can iterate.
- Existing project code is inspected and preserved where possible.
- Unsupported operations are reported honestly; no fake “done” responses.

## Safety and reliability boundaries

- Never run generated or changed scripts silently.
- Show diffs before applying edits; use backups or version control.
- Require approval for execution, destructive edits, overwrites, and operations outside the selected project.
- Keep file access inside the chosen project by default.
- Do not execute arbitrary shell commands as a shortcut.
- A local Godot project is not a sandbox; generated GDScript can have significant effects, so review and visible controls matter.
