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


from openbridge.server import _validate_script_patch


def test_valid_new_script_patch_envelope():
    result = _validate_script_patch("scripts/player.gd", "extends CharacterBody2D\n", "create")
    assert result["valid"] is True
    assert result["operation"] == "create"


def test_update_requires_expected_hash():
    result = _validate_script_patch("scripts/player.gd", "extends CharacterBody2D\n", "update")
    assert result["valid"] is False
    assert any(error["path"] == "expected_sha256" for error in result["errors"])


def test_script_patch_rejects_path_traversal():
    result = _validate_script_patch("../outside.gd", "extends Node\n", "create")
    assert result["valid"] is False
    assert any(error["path"] == "script_path" for error in result["errors"])


def test_script_patch_rejects_non_gd_extension():
    result = _validate_script_patch("scripts/main.py", "print('no')", "create")
    assert result["valid"] is False


def test_script_patch_rejects_oversized_content():
    result = _validate_script_patch("scripts/large.gd", "x" * (128 * 1024 + 1), "create")
    assert result["valid"] is False
    assert any(error["path"] == "content" for error in result["errors"])
