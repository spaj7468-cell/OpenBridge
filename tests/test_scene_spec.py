from openbridge.server import _validate_scene_spec


def test_valid_simple_scene_spec():
    spec = {
        "format": "openbridge.scene/v1",
        "root": {
            "name": "Main",
            "type": "Node2D",
            "children": [
                {"name": "Player", "type": "CharacterBody2D", "properties": {"visible": True}}
            ],
        },
    }
    result = _validate_scene_spec(spec)
    assert result["valid"] is True
    assert result["node_count"] == 2


def test_rejects_unknown_node_type():
    spec = {"format": "openbridge.scene/v1", "root": {"name": "Root", "type": "ExecuteAnything"}}
    result = _validate_scene_spec(spec)
    assert result["valid"] is False
    assert any(error["path"] == "$.root.type" for error in result["errors"])


def test_rejects_unapproved_property():
    spec = {
        "format": "openbridge.scene/v1",
        "root": {"name": "Root", "type": "Node2D", "properties": {"script": "res://evil.gd"}},
    }
    result = _validate_scene_spec(spec)
    assert result["valid"] is False
    assert any("allow-list" in error["message"] for error in result["errors"])


def test_rejects_wrong_format():
    result = _validate_scene_spec({"format": "other", "root": {"name": "Root", "type": "Node"}})
    assert result["valid"] is False
