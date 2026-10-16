@tool
extends EditorPlugin

const DEFAULT_BRIDGE_PORT := 8766
const MAX_REQUEST_BYTES := 262144
const MAX_SCRIPT_BYTES := 131072
const MAX_TREE_NODES := 200
const MAX_TREE_DEPTH := 20

var _panel: VBoxContainer
var _status_label: Label
var _tcp_server := TCPServer.new()
var _clients: Array[Dictionary] = []
var _bridge_token := ""
var _bridge_port := DEFAULT_BRIDGE_PORT
var _bridge_started := false
var _script_writes_enabled := false
var _write_button: Button


func _enter_tree() -> void:
	_build_panel()
	_bridge_port = _read_port_setting()
	_bridge_token = OS.get_environment("OPENBRIDGE_ADAPTER_TOKEN").strip_edges()
	if _bridge_token.is_empty():
		_set_status("Adapter stopped: set OPENBRIDGE_ADAPTER_TOKEN in the editor environment.")
	else:
		var err := _tcp_server.listen(_bridge_port, "127.0.0.1")
		if err == OK:
			_bridge_started = true
			_set_status("Connected locally • port %d" % _bridge_port)
		else:
			_set_status("Could not listen on 127.0.0.1:%d (error %d)" % [_bridge_port, err])
	set_process(true)


func _exit_tree() -> void:
	set_process(false)
	for client in _clients:
		var peer: StreamPeerTCP = client.get("peer")
		if is_instance_valid(peer):
			peer.disconnect_from_host()
	_clients.clear()
	if _tcp_server.is_listening():
		_tcp_server.stop()
	_bridge_started = false
	if is_instance_valid(_panel):
		remove_control_from_docks(_panel)
		_panel.queue_free()


func _process(_delta: float) -> void:
	if not _bridge_started:
		return
	while _tcp_server.is_connection_available():
		var peer := _tcp_server.take_connection()
		if peer:
			_clients.append({"peer": peer, "buffer": PackedByteArray(), "created_msec": Time.get_ticks_msec()})
	var index := _clients.size() - 1
	while index >= 0:
		var client: Dictionary = _clients[index]
		var peer: StreamPeerTCP = client.get("peer")
		if not is_instance_valid(peer) or peer.get_status() == StreamPeerTCP.STATUS_ERROR or peer.get_status() == StreamPeerTCP.STATUS_NONE:
			_clients.remove_at(index)
			index -= 1
			continue
		if Time.get_ticks_msec() - int(client.get("created_msec", 0)) > 5000:
			_send_response(peer, 408, {"error": "REQUEST_TIMEOUT"})
			_clients.remove_at(index)
			index -= 1
			continue
		var available := peer.get_available_bytes()
		if available > 0:
			var chunk := peer.get_data(mini(available, MAX_REQUEST_BYTES + 1))
			if chunk[0] == OK:
				var buffer: PackedByteArray = client.get("buffer", PackedByteArray())
				buffer.append_array(chunk[1])
				client["buffer"] = buffer
				_clients[index] = client
				if buffer.size() > MAX_REQUEST_BYTES:
					_send_response(peer, 413, {"error": "REQUEST_TOO_LARGE"})
					_clients.remove_at(index)
					index -= 1
					continue
				var parsed := _parse_http_request(buffer)
				if parsed.get("complete", false):
					var response := _dispatch_request(parsed)
					_send_response(peer, int(response.get("status", 200)), response.get("body", {}))
					_clients.remove_at(index)
					index -= 1
					continue
		index -= 1


func _build_panel() -> void:
	_panel = VBoxContainer.new()
	_panel.name = "OpenBridge"
	_panel.custom_minimum_size = Vector2(280, 180)
	var title := Label.new()
	title.text = "OpenBridge — Godot Agent"
	title.add_theme_font_size_override("font_size", 18)
	_panel.add_child(title)
	var description := Label.new()
	description.text = "Local editor bridge for AI-assisted scene and GDScript workflows."
	description.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_panel.add_child(description)
	_status_label = Label.new()
	_status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_panel.add_child(_status_label)
	var refresh := Button.new()
	refresh.text = "Refresh status"
	refresh.pressed.connect(_refresh_status)
	_panel.add_child(refresh)
	_write_button = Button.new()
	_write_button.text = "Enable script writes (session only)"
	_write_button.toggle_mode = true
	_write_button.button_pressed = false
	_write_button.toggled.connect(_on_write_toggle)
	_panel.add_child(_write_button)
	var security_note := Label.new()
	security_note.text = "Loopback only. Script writes are OFF by default. Enable them only when you trust the connected AI host; this session toggle resets when the editor restarts."
	security_note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_panel.add_child(security_note)
	add_control_to_dock(DOCK_SLOT_RIGHT_UL, _panel)


func _read_port_setting() -> int:
	var raw := OS.get_environment("OPENBRIDGE_GODOT_PORT")
	if raw.is_valid_int():
		var parsed := int(raw)
		if parsed >= 1024 and parsed <= 65535:
			return parsed
	return DEFAULT_BRIDGE_PORT


func _on_write_toggle(enabled: bool) -> void:
	_script_writes_enabled = enabled
	if is_instance_valid(_write_button):
		_write_button.text = "Script writes ENABLED for this session" if enabled else "Enable script writes (session only)"
		_write_button.modulate = Color(1.0, 0.72, 0.45) if enabled else Color(1, 1, 1)


func _refresh_status() -> void:
	if _bridge_started:
		_set_status("Bridge listening on 127.0.0.1:%d" % _bridge_port)
	elif _bridge_token.is_empty():
		_set_status("Adapter stopped: set OPENBRIDGE_ADAPTER_TOKEN in the editor environment.")
	else:
		_set_status("Adapter not listening. Check port %d." % _bridge_port)


func _set_status(value: String) -> void:
	if is_instance_valid(_status_label):
		_status_label.text = value


func _parse_http_request(buffer: PackedByteArray) -> Dictionary:
	var raw := buffer.get_string_from_utf8()
	var split_at := raw.find("\r\n\r\n")
	if split_at < 0:
		return {"complete": false}
	var header_text := raw.substr(0, split_at)
	var lines := header_text.split("\r\n")
	if lines.is_empty():
		return {"complete": true, "status": 400, "body": {"error": "BAD_REQUEST"}}
	var request_line := lines[0].split(" ", false)
	if request_line.size() < 2:
		return {"complete": true, "status": 400, "body": {"error": "BAD_REQUEST"}}
	var headers := {}
	for line in lines.slice(1):
		var colon := line.find(":")
		if colon > 0:
			headers[line.substr(0, colon).strip_edges().to_lower()] = line.substr(colon + 1).strip_edges()
	var content_length := int(headers.get("content-length", "0"))
	if content_length < 0 or content_length > MAX_REQUEST_BYTES:
		return {"complete": true, "status": 413, "body": {"error": "REQUEST_TOO_LARGE"}}
	var body_start := split_at + 4
	var body_bytes := buffer.slice(body_start, buffer.size())
	if body_bytes.size() < content_length:
		return {"complete": false}
	return {
		"complete": true,
		"method": request_line[0].to_upper(),
		"path": request_line[1].split("?")[0],
		"headers": headers,
		"body_text": body_bytes.slice(0, content_length).get_string_from_utf8(),
	}


func _dispatch_request(request: Dictionary) -> Dictionary:
	var method: String = request.get("method", "")
	var path: String = request.get("path", "")
	var headers: Dictionary = request.get("headers", {})
	if headers.get("authorization", "") != "Bearer " + _bridge_token:
		return {"status": 401, "body": {"error": "UNAUTHORIZED"}}
	if method == "GET" and path == "/health":
		return {"status": 200, "body": {"name": "OpenBridge Godot adapter", "connected": true, "protocol": 1, "godot_version": Engine.get_version_info(), "project_name": ProjectSettings.get_setting("application/config/name", "Godot Project")}}
	if method == "GET" and path == "/editor_info":
		var scene_path := ""
		var edited_scene := get_editor_interface().get_edited_scene_root()
		if is_instance_valid(edited_scene):
			scene_path = edited_scene.scene_file_path
		return {"status": 200, "body": {"godot_version": Engine.get_version_info(), "project_name": ProjectSettings.get_setting("application/config/name", "Godot Project"), "active_scene": scene_path, "editor_hint": Engine.is_editor_hint()}}
	if method == "GET" and path == "/scene_tree":
		var root := get_editor_interface().get_edited_scene_root()
		if not is_instance_valid(root):
			return {"status": 409, "body": {"error": "NO_ACTIVE_SCENE", "message": "Open a scene in the Godot editor first."}}
		var count := [0]
		var tree := _serialize_node(root, 1, count)
		return {"status": 200, "body": {"scene_path": root.scene_file_path, "node_count": count[0], "root": tree}}
	if method == "POST" and path in ["/script/read", "/script/preview", "/script/apply"]:
		var payload: Variant = JSON.parse_string(request.get("body_text", ""))
		if not payload is Dictionary:
			return {"status": 400, "body": {"error": "INVALID_JSON"}}
		var script_path := str(payload.get("path", ""))
		if not _is_safe_script_path(script_path):
			return {"status": 400, "body": {"error": "INVALID_SCRIPT_PATH"}}
		var file_exists := FileAccess.file_exists("res://" + script_path)
		if method == "POST" and path == "/script/read":
			if not file_exists:
				return {"status": 404, "body": {"error": "FILE_NOT_FOUND", "path": script_path}}
			var read_file := FileAccess.open("res://" + script_path, FileAccess.READ)
			if read_file == null:
				return {"status": 500, "body": {"error": "FILE_READ_FAILED", "detail": FileAccess.get_open_error()}}
			if read_file.get_length() > MAX_SCRIPT_BYTES:
				read_file.close()
				return {"status": 413, "body": {"error": "SCRIPT_TOO_LARGE", "limit_bytes": MAX_SCRIPT_BYTES}}
			var current_content := read_file.get_as_text()
			read_file.close()
			return {"status": 200, "body": {"path": script_path, "content": current_content, "sha256": current_content.sha256_text(), "bytes": current_content.to_utf8_buffer().size(), "absolute_path_returned": false, "note": "Read-only operation. File was not changed or executed."}}
		if path == "/script/preview":
			var proposed: Variant = payload.get("content", "")
			if not proposed is String or proposed.is_empty() or proposed.to_utf8_buffer().size() > MAX_SCRIPT_BYTES:
				return {"status": 400, "body": {"error": "INVALID_SCRIPT_CONTENT", "limit_bytes": MAX_SCRIPT_BYTES}}
			var existing_content := ""
			var existing_hash := ""
			if file_exists:
				var existing_file := FileAccess.open("res://" + script_path, FileAccess.READ)
				if existing_file == null:
					return {"status": 500, "body": {"error": "FILE_READ_FAILED"}}
				if existing_file.get_length() > MAX_SCRIPT_BYTES:
					existing_file.close()
					return {"status": 413, "body": {"error": "SCRIPT_TOO_LARGE"}}
				existing_content = existing_file.get_as_text()
				existing_file.close()
				existing_hash = existing_content.sha256_text()
			return {"status": 200, "body": {"path": script_path, "exists": file_exists, "current_sha256": existing_hash, "proposed_sha256": proposed.sha256_text(), "current_content": existing_content, "proposed_content": proposed, "write_enabled": _script_writes_enabled, "note": "Preview only; no file was changed and code was not executed."}}
		if path == "/script/apply":
			if not _script_writes_enabled:
				return {"status": 403, "body": {"error": "SCRIPT_WRITES_DISABLED", "message": "Enable script writes in the OpenBridge dock for this editor session."}}
			var proposed_content: Variant = payload.get("content", "")
			var operation := str(payload.get("operation", ""))
			var expected_hash := str(payload.get("expected_sha256", ""))
			if not proposed_content is String or proposed_content.is_empty() or proposed_content.to_utf8_buffer().size() > MAX_SCRIPT_BYTES or proposed_content.to_utf8_buffer().has(0):
				return {"status": 400, "body": {"error": "INVALID_SCRIPT_CONTENT", "limit_bytes": MAX_SCRIPT_BYTES}}
			if operation not in ["create", "update"]:
				return {"status": 400, "body": {"error": "INVALID_OPERATION"}}
			if operation == "create" and file_exists:
				return {"status": 409, "body": {"error": "FILE_ALREADY_EXISTS", "path": script_path}}
			if operation == "update" and not file_exists:
				return {"status": 404, "body": {"error": "FILE_NOT_FOUND", "path": script_path}}
			var old_content := ""
			if file_exists:
				var old_file := FileAccess.open("res://" + script_path, FileAccess.READ)
				if old_file == null:
					return {"status": 500, "body": {"error": "FILE_READ_FAILED"}}
				if old_file.get_length() > MAX_SCRIPT_BYTES:
					old_file.close()
					return {"status": 413, "body": {"error": "SCRIPT_TOO_LARGE"}}
				old_content = old_file.get_as_text()
				old_file.close()
				if old_content.sha256_text() != expected_hash:
					return {"status": 409, "body": {"error": "STALE_SCRIPT", "current_sha256": old_content.sha256_text()}}
			if operation == "create" and not expected_hash.is_empty():
				return {"status": 400, "body": {"error": "INVALID_EXPECTED_HASH"}}
			var backup_path := ""
			if file_exists:
				var backup_dir := "user://OpenBridge/backups"
				DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(backup_dir))
				backup_path = backup_dir.path_join(str(Time.get_unix_time_from_system()) + "_" + script_path.replace("/", "_") + ".bak")
				var backup_file := FileAccess.open(backup_path, FileAccess.WRITE)
				if backup_file == null:
					return {"status": 500, "body": {"error": "BACKUP_FAILED", "detail": FileAccess.get_open_error()}}
				backup_file.store_string(old_content)
				backup_file.close()
			var parent_path := script_path.get_base_dir()
			if parent_path != ".":
				var directory_error := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://" + parent_path))
				if directory_error != OK:
					return {"status": 500, "body": {"error": "DIRECTORY_CREATE_FAILED", "detail": directory_error}}
			var output := FileAccess.open("res://" + script_path, FileAccess.WRITE)
			if output == null:
				return {"status": 500, "body": {"error": "FILE_WRITE_FAILED", "detail": FileAccess.get_open_error(), "backup_path": backup_path}}
			output.store_string(proposed_content)
			output.close()
			return {"status": 200, "body": {"applied": true, "path": script_path, "operation": operation, "sha256": proposed_content.sha256_text(), "backup_path": backup_path, "executed": false, "note": "Script saved but not executed. Run the project separately after reviewing the change."}}
	return {"status": 404, "body": {"error": "NOT_FOUND"}}


func _serialize_node(node: Node, depth: int, count: Array) -> Dictionary:
	count[0] += 1
	var result := {"name": node.name, "type": node.get_class(), "path": str(node.get_path()), "child_count": node.get_child_count()}
	if depth >= MAX_TREE_DEPTH or count[0] >= MAX_TREE_NODES:
		result["truncated"] = node.get_child_count() > 0
		return result
	var children: Array[Dictionary] = []
	for child in node.get_children():
		if count[0] >= MAX_TREE_NODES:
			result["truncated"] = true
			break
		children.append(_serialize_node(child, depth + 1, count))
	result["children"] = children
	return result


func _is_safe_script_path(path: String) -> bool:
	if path.is_empty() or path.begins_with("/") or path.contains("\\") or path.contains(":"):
		return false
	if not path.ends_with(".gd"):
		return false
	for part in path.split("/"):
		if part.is_empty() or part == "." or part == "..":
			return false
	return true


func _send_response(peer: StreamPeerTCP, status: int, body: Variant) -> void:
	var body_text := JSON.stringify(body)
	var reason := "OK"
	if status == 400:
		reason = "Bad Request"
	elif status == 401:
		reason = "Unauthorized"
	elif status == 404:
		reason = "Not Found"
	elif status == 408:
		reason = "Request Timeout"
	elif status == 409:
		reason = "Conflict"
	elif status == 413:
		reason = "Payload Too Large"
	elif status >= 500:
		reason = "Internal Server Error"
	var response := "HTTP/1.1 %d %s\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: %d\r\nConnection: close\r\nCache-Control: no-store\r\n\r\n%s" % [status, reason, body_text.to_utf8_buffer().size(), body_text]
	peer.put_data(response.to_utf8_buffer())
	peer.disconnect_from_host()
