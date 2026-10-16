@tool
extends EditorPlugin

const MCP_ENDPOINT := "http://127.0.0.1:8765/mcp"

var _panel: VBoxContainer


func _enter_tree() -> void:
	_panel = VBoxContainer.new()
	_panel.name = "OpenBridge"
	_panel.custom_minimum_size = Vector2(260, 120)

	var title := Label.new()
	title.text = "OpenBridge — Godot Agent"
	title.add_theme_font_size_override("font_size", 18)
	_panel.add_child(title)

	var subtitle := Label.new()
	subtitle.text = "AI agent for Godot • GDScript + scenes"
	_panel.add_child(subtitle)

	var endpoint := Label.new()
	endpoint.text = "MCP endpoint:\n" + MCP_ENDPOINT
	endpoint.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_panel.add_child(endpoint)

	var status := Label.new()
	status.text = "Status: adapter not connected"
	status.add_theme_color_override("font_color", Color(0.85, 0.72, 0.35))
	status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_panel.add_child(status)

	var note := Label.new()
	note.text = "Target workflow: inspect project → generate/edit GDScript → preview changes → validate → run and debug. The current build is UI-only: no editor connection, script writes, scene edits, or play-testing yet."
	note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_panel.add_child(note)

	add_control_to_dock(DOCK_SLOT_RIGHT_UL, _panel)


func _exit_tree() -> void:
	if is_instance_valid(_panel):
		remove_control_from_docks(_panel)
		_panel.queue_free()
