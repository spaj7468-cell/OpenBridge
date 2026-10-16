#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python" ]; then
  echo "[OpenBridge] Creating a local Python environment..."
  python3 -m venv .venv
fi

echo "[OpenBridge] Checking/installing dependencies..."
".venv/bin/python" -m pip install -e .

echo "[OpenBridge] Starting local MCP service..."
exec ".venv/bin/python" -m openbridge.server
