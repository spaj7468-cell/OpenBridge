"""Initial OpenBridge MCP runtime.

This first milestone intentionally exposes only status, capability discovery,
adapter health, and safe scene-spec validation. It does not edit Godot projects.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from mcp.server.fastmcp import FastMCP

from openbridge import __version__

HOST = os.getenv("OPENBRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("OPENBRIDGE_PORT", "8765"))
GODOT_BRIDGE_URL = os.getenv("OPENBRIDGE_GODOT_HEALTH_URL", "http://127.0.0.1:8766/health")
MAX_SCENE_NODES = 200
MAX_TREE_DEPTH = 20

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


@mcp.tool()
def openbridge_status() -> dict[str, Any]:
    """Return OpenBridge runtime status and the current implementation stage."""
    return {
        "name": "OpenBridge",
        "version": __version__,
        "status": "foundation",
        "transport": "MCP Streamable HTTP",
        "endpoint": f"http://{HOST}:{PORT}/mcp",
        "godot_mutations_enabled": False,
        "message": "Runtime is available; Godot project editing is not implemented in this milestone.",
    }


@mcp.tool()
def openbridge_capabilities() -> dict[str, Any]:
    """List implemented capabilities separately from planned integrations."""
    return {
        "implemented": [
            "runtime status",
            "capability discovery",
            "Godot adapter health probe",
            "bounded data-only scene specification validation",
        ],
        "planned": [
            "Godot editor plugin and scene-tree inspection",
            "approved scene creation and property editing",
            "browser extension",
            "DeepSeek-guided plan/preview/apply workflow",
            "cross-platform quick launcher",
        ],
    }


@mcp.tool()
def godot_adapter_status() -> dict[str, Any]:
    """Check whether a local Godot editor adapter health endpoint is reachable."""
    request = urllib.request.Request(GODOT_BRIDGE_URL, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=1.5) as response:
            payload = response.read(16_384).decode("utf-8", errors="replace")
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                data = {"response": payload[:1000]}
            return {"connected": True, "endpoint": GODOT_BRIDGE_URL, "adapter": data}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {
            "connected": False,
            "endpoint": GODOT_BRIDGE_URL,
            "code": "ADAPTER_DISCONNECTED",
            "message": "Godot adapter is not connected. This is expected until the editor plugin is implemented and enabled.",
            "detail": type(exc).__name__,
        }


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
    print("This foundation build does not yet mutate Godot projects.")
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
