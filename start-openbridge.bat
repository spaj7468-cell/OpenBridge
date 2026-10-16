@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [OpenBridge] Creating a local Python environment...
  py -3 -m venv .venv
  if errorlevel 1 (
    echo Could not create the Python environment. Install Python 3.10+ and try again.
    exit /b 1
  )
)

echo [OpenBridge] Checking/installing dependencies...
".venv\Scripts\python.exe" -m pip install -e .
if errorlevel 1 (
  echo Dependency installation failed. Check your network and Python installation.
  exit /b 1
)

echo [OpenBridge] Starting local MCP service...
".venv\Scripts\python.exe" -m openbridge.server
endlocal
