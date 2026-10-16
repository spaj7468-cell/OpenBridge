"""Initial OpenBridge MCP runtime.

This first milestone intentionally exposes only status, capability discovery,
adapter health, and safe scene-spec validation. It does not edit Godot projects.
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any

from mcp.server.fastmcp import FastMCP

from openbridge import __version__

HOST = os.getenv("OPENBRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("OPENBRIDGE_PORT", "8765"))
GODOT_BRIDGE_URL = os.getenv("OPENBRIDGE_GODOT_HEALTH_URL", "http://127.0.0.1:8766/health")
GODOT_BRIDGE_BASE_URL = os.getenv("OPENBRIDGE_GODOT_URL", "http://127.0.0.1:8766").rstrip("/")
GODOT_BRIDGE_TOKEN = os.getenv("OPENBRIDGE_ADAPTER_TOKEN", "")
MAX_SCENE_NODES = 200
MAX_TREE_DEPTH = 20
MAX_SCRIPT_BYTES = 128 * 1024
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

mcp = FastMCP("OpenBridge", host=HOST, port=PORT)

_ALLOWED_NODE_TYPES = {
    "Node", "Node2D", "CanvasItem", "Control", "Node3D",
    "CharacterBody2D", "CharacterBody3D", "StaticBody2D", "StaticBody3D",
    "Area2D", "Area3D", "Sprite2D", "Sprite3D", "AnimatedSprite2D",
    "Camera2D", "Camera3D", "CollisionShape2D", "CollisionShape3D",
    "CollisionPolygon2D", "CollisionPolygon3D", "Marker2D", "Marker3D",
    "Label", "RichTextLabel", "Button", "TextureRect", "ColorRect",
    "Panel", "VBoxContainer", "HBoxContainer", "GridContainer",
    "Timer", "AudioStreamPlayer", "AudioStreamPlayer2D", "AudioStreamPlayer3D",
}

_ALLOWED_PROPERTIES = {
    "position", "rotation", "scale", "visible", "z_index",
    "offset_left", "offset_top", "offset_right", "offset_bottom",
    "text", "modulate", "self_modulate", "size",
}




def _godot_request(path: str, method: str = "GET", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Call the loopback Godot editor adapter with a shared bearer token."""
    if len(GODOT_BRIDGE_TOKEN) < 32:
        return {
            "ok": False,
            "error": "ADAPTER_TOKEN_MISSING_OR_WEAK",
            "message": "Set a random OPENBRIDGE_ADAPTER_TOKEN of at least 32 characters in the environment used to start both Godot and OpenBridge.",
        }
    if not path.startswith("/") or ".." in path.split("/"):
        return {"ok": False, "error": "INVALID_ADAPTER_PATH"}
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {GODOT_BRIDGE_TOKEN}",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        GODOT_BRIDGE_BASE_URL + path,
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=3.0) as response:
            raw = response.read(262_144).decode("utf-8", errors="replace")
            data = json.loads(raw)
            if not isinstance(data, dict):
                return {"ok": False, "error": "INVALID_ADAPTER_RESPONSE"}
            return {"ok": True, "data": data}
    except urllib.error.HTTPError as exc:
        try:
            detail = json.loads(exc.read(16_384).decode("utf-8", errors="replace"))
        except (json.JSONDecodeError, OSError):
            detail = {}
        return {
            "ok": False,
            "error": str(detail.get("error", "ADAPTER_HTTP_ERROR")),
            "status": exc.code,
            "detail": detail,
        }
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "error": "ADAPTER_DISCONNECTED",
            "message": "Could not reach the local Godot editor adapter.",
            "detail": type(exc).__name__,
        }


def _validate_scene_spec(scene_spec: dict[str, Any]) -> dict[str, Any]:
    """Validate a bounded, data-only scene tree; never executes code or writes files."""
    errors: list[dict[str, str]] = []
    node_count = 0

    if not isinstance(scene_spec, dict):
        return {"valid": False, "errors": [{"path": "$", "message": "Expected an object."}]}
    if scene_spec.get("format") != "openbridge.scene/v1":
        errors.append({"path": "$.format", "message": "format must be 'openbridge.scene/v1'."})
    root = scene_spec.get("root")
    if not isinstance(root, dict):
        return {"valid": False, "errors": errors + [{"path": "$.root", "message": "root must be an object."}]}

    def visit(node: Any, path: str, depth: int) -> None:
        nonlocal node_count
        if not isinstance(node, dict):
            errors.append({"path": path, "message": "Node must be an object."})
            return
        node_count += 1
        if node_count > MAX_SCENE_NODES:
            errors.append({"path": path, "message": f"Scene exceeds the {MAX_SCENE_NODES}-node limit."})
            return
        if depth > MAX_TREE_DEPTH:
            errors.append({"path": path, "message": f"Scene exceeds the {MAX_TREE_DEPTH}-level depth limit."})
            return

        name = node.get("name")
        node_type = node.get("type")
        if not isinstance(name, str) or not name.strip():
            errors.append({"path": f"{path}.name", "message": "name must be a non-empty string."})
        elif any(char in name for char in "/\\.:"):
            errors.append({"path": f"{path}.name", "message": "name contains a reserved path character."})
        if not isinstance(node_type, str) or node_type not in _ALLOWED_NODE_TYPES:
            errors.append({"path": f"{path}.type", "message": "Node type is not in the current safe allow-list."})

        properties = node.get("properties", {})
        if not isinstance(properties, dict):
            errors.append({"path": f"{path}.properties", "message": "properties must be an object."})
        else:
            for key, value in properties.items():
                prop_path = f"{path}.properties.{key}"
                if key not in _ALLOWED_PROPERTIES:
                    errors.append({"path": prop_path, "message": "Property is not in the current safe allow-list."})
                elif key in {"position", "rotation", "scale", "modulate", "self_modulate", "size"}:
                    if not isinstance(value, dict) or not value or any(
                        component not in {"x", "y", "z", "r", "g", "b", "a"}
                        or not isinstance(number, (int, float)) or isinstance(number, bool)
                        for component, number in value.items()
                    ):
                        errors.append({"path": prop_path, "message": "Expected a numeric component object."})
                elif key == "visible" and not isinstance(value, bool):
                    errors.append({"path": prop_path, "message": "visible must be a boolean."})
                elif key == "z_index" and (not isinstance(value, int) or isinstance(value, bool)):
                    errors.append({"path": prop_path, "message": "z_index must be an integer."})
                elif key in {"text"} and not isinstance(value, str):
                    errors.append({"path": prop_path, "message": "text must be a string."}
                    )
                elif key.startswith("offset_") and (not isinstance(value, (int, float)) or isinstance(value, bool)):
                    errors.append({"path": prop_path, "message": "offset values must be numbers."})

        children = node.get("children", [])
        if not isinstance(children, list):
            errors.append({"path": f"{path}.children", "message": "children must be an array."})
            return
        for index, child in enumerate(children):
            visit(child, f"{path}.children[{index}]", depth + 1)

    visit(root, "$.root", 1)
    return {
        "valid": not errors,
        "node_count": node_count,
        "errors": errors,
        "note": "Schema validation only; this does not confirm Godot runtime compatibility or modify a project.",
    }


def _validate_script_patch(
    script_path: str,
    content: str,
    operation: str,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    """Validate a proposed GDScript file payload without reading or writing files."""
    errors: list[dict[str, str]] = []

    if not isinstance(script_path, str) or not script_path.strip():
        errors.append({"path": "script_path", "message": "script_path must be a non-empty project-relative path."})
    else:
        if script_path.startswith(("/", "\\")) or ":" in script_path:
            errors.append({"path": "script_path", "message": "Absolute paths and drive/resource prefixes are not allowed."})
        if "\\" in script_path:
            errors.append({"path": "script_path", "message": "Use forward slashes in project-relative paths."})
        parts = script_path.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            errors.append({"path": "script_path", "message": "Path segments cannot be empty, '.' or '..'."})
        if not script_path.endswith(".gd"):
            errors.append({"path": "script_path", "message": "Only .gd GDScript files are supported by this validator."})

    if operation not in {"create", "update"}:
        errors.append({"path": "operation", "message": "operation must be 'create' or 'update'."})

    if not isinstance(content, str) or not content.strip():
        errors.append({"path": "content", "message": "content must be a non-empty string."})
    elif "\x00" in content:
        errors.append({"path": "content", "message": "NUL characters are not allowed."})
    elif len(content.encode("utf-8")) > MAX_SCRIPT_BYTES:
        errors.append({"path": "content", "message": f"Script content exceeds the {MAX_SCRIPT_BYTES}-byte limit."})

    if operation == "update":
        if not isinstance(expected_sha256, str) or not _SHA256_PATTERN.fullmatch(expected_sha256):
            errors.append({"path": "expected_sha256", "message": "Updates require the expected SHA-256 of the current file."})
    elif operation == "create" and expected_sha256 is not None:
        errors.append({"path": "expected_sha256", "message": "New-file operations must not provide expected_sha256."})

    return {
        "valid": not errors,
        "operation": operation if operation in {"create", "update"} else None,
        "script_path": script_path if isinstance(script_path, str) else None,
        "content_bytes": len(content.encode("utf-8")) if isinstance(content, str) else 0,
        "errors": errors,
        "note": "Validation only: no project file is read, written, or executed. A real editor adapter and approval flow are still required.",
    }


@mcp.tool()
def godot_validate_script_patch(
    script_path: str,
    content: str,
    operation: str,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    """Validate a proposed GDScript create/update payload without changing project files.

    Use project-relative .gd paths. Updates must include the expected SHA-256
    of the current file to help prevent stale edits. This tool does not write,
    parse, or execute GDScript; it validates the request envelope only.
    """
    return _validate_script_patch(script_path, content, operation, expected_sha256)


@mcp.tool()
def openbridge_status() -> dict[str, Any]:
    """Return OpenBridge runtime status and the current implementation stage."""
    return {
        "name": "OpenBridge",
        "version": __version__,
        "status": "foundation",
        "transport": "MCP Streamable HTTP",
        "endpoint": f"http://{HOST}:{PORT}/mcp",
        "godot_script_writes": "available only when enabled in the Godot editor dock",
        "godot_scene_mutations_enabled": False,
        "godot_code_execution_enabled": False,
        "message": "The editor adapter supports guarded GDScript file writes; it does not execute scripts or mutate scenes yet.",
    }


@mcp.tool()
def openbridge_capabilities() -> dict[str, Any]:
    """List implemented capabilities separately from planned integrations."""
    return {
        "implemented": [
            "runtime status",
            "capability discovery",
            "Godot adapter health probe",
            "authenticated read-only Godot editor info and scene-tree inspection",
            "read-only project-relative GDScript inspection",
            "GDScript preview and opt-in file application with stale-hash checks and backups",
            "Godot-native GDScript parser validation (not execution)",
            "bounded data-only scene specification validation",
            "GDScript patch-envelope validation (no file writes or execution)",
        ],
        "planned": [
            "approved scene creation and property editing",
            "project run/playtest and debugger feedback loop",
            "authenticated browser-to-agent tool execution",
            "DeepSeek provider and iterative plan/preview/apply/verify workflow",
            "Godot parser validation and project run/debug feedback",
            "cross-platform quick launcher",
        ],
    }


@mcp.tool()
def godot_adapter_status() -> dict[str, Any]:
    """Check the authenticated local Godot editor adapter health endpoint."""
    result = _godot_request("/health")
    if result["ok"]:
        return {"connected": True, "endpoint": GODOT_BRIDGE_URL, "adapter": result["data"]}
    return {
        "connected": False,
        "endpoint": GODOT_BRIDGE_URL,
        "code": result.get("error", "ADAPTER_DISCONNECTED"),
        "message": result.get("message", "Godot adapter is not reachable or authentication failed."),
        "detail": result.get("detail", {}),
    }


@mcp.tool()
def godot_get_editor_info() -> dict[str, Any]:
    """Get version and active-scene information from a connected Godot editor."""
    result = _godot_request("/editor_info")
    return result["data"] if result["ok"] else result


@mcp.tool()
def godot_get_scene_tree() -> dict[str, Any]:
    """Inspect a bounded summary of the active scene in the connected Godot editor."""
    result = _godot_request("/scene_tree")
    return result["data"] if result["ok"] else result


@mcp.tool()
def godot_read_script(path: str) -> dict[str, Any]:
    """Read a project-relative .gd file from the selected Godot project; never writes or executes it."""
    if not isinstance(path, str) or not path.strip():
        return {"ok": False, "error": "INVALID_SCRIPT_PATH"}
    validated = _validate_script_patch(path, "# read-only path validation", "create")
    if not validated["valid"]:
        return {"ok": False, "error": "INVALID_SCRIPT_PATH", "details": validated["errors"]}
    result = _godot_request("/script/read", method="POST", payload={"path": path})
    return result["data"] if result["ok"] else result


@mcp.tool()
def godot_preview_script_patch(path: str, content: str) -> dict[str, Any]:
    """Preview a GDScript change against the current project file without writing or executing it."""
    if not isinstance(path, str) or not path.strip() or not isinstance(content, str):
        return {"ok": False, "error": "INVALID_ARGUMENT"}
    operation = "update" if path.endswith(".gd") else "create"
    validated = _validate_script_patch(path, content, operation, "0" * 64 if operation == "update" else None)
    if not validated["valid"]:
        return {"ok": False, "error": "INVALID_SCRIPT_PATCH", "details": validated["errors"]}
    result = _godot_request("/script/preview", method="POST", payload={"path": path, "content": content})
    return result["data"] if result["ok"] else result


@mcp.tool()
def godot_validate_script(content: str) -> dict[str, Any]:
    """Ask the connected Godot editor to parse proposed GDScript without saving or executing it."""
    if not isinstance(content, str):
        return {"ok": False, "error": "INVALID_SCRIPT_CONTENT"}
    validated = _validate_script_patch("validation.gd", content, "create")
    if not validated["valid"]:
        return {"ok": False, "error": "INVALID_SCRIPT_CONTENT", "details": validated["errors"]}
    result = _godot_request("/script/validate", method="POST", payload={"content": content})
    return result["data"] if result["ok"] else result


@mcp.tool()
def godot_apply_script_patch(
    path: str,
    content: str,
    operation: str,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    """Apply a GDScript file change only when script writes are enabled in the Godot dock.

    Updates require the exact current file SHA-256 from preview/read. Creates fail if the file already exists.
    This saves code but never executes it; running a project remains a separate future capability.
    """
    validated = _validate_script_patch(path, content, operation, expected_sha256)
    if not validated["valid"]:
        return {"ok": False, "error": "INVALID_SCRIPT_PATCH", "details": validated["errors"]}
    result = _godot_request(
        "/script/apply",
        method="POST",
        payload={
            "path": path,
            "content": content,
            "operation": operation,
            "expected_sha256": expected_sha256 or "",
        },
    )
    return result["data"] if result["ok"] else result


@mcp.tool()
def godot_validate_scene_spec(scene_spec: dict[str, Any]) -> dict[str, Any]:
    """Validate a data-only Godot scene tree proposal without executing scripts or editing files.

    The expected object has format='openbridge.scene/v1' and a root node with
    name, type, optional properties, and optional children.
    """
    return _validate_scene_spec(scene_spec)


def main() -> None:
    """Start the local MCP Streamable HTTP server."""
    print(f"OpenBridge {__version__} starting at http://{HOST}:{PORT}/mcp")
    print("Read-only Godot tools require the editor plugin and OPENBRIDGE_ADAPTER_TOKEN.")
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
