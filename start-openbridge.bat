@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title OpenBridge Local AI Bridge

echo.
echo  ============================================
echo   OpenBridge ^| Browser AI ^> Godot
echo  ============================================
echo.

if not exist ".venv\Scripts\python.exe" (
  echo [1/5] Creating local Python environment...
  py -3 -m venv .venv
  if errorlevel 1 (
    echo ERROR: Install Python 3.10+ and retry.
    pause
    exit /b 1
  )
) else (
  echo [1/5] Python environment found.
)

echo [2/5] Installing/checking OpenBridge dependencies...
".venv\Scripts\python.exe" -m pip install -e .
if errorlevel 1 (
  echo ERROR: Dependency installation failed. Check internet and Python.
  pause
  exit /b 1
)

set "OB_DIR=%LOCALAPPDATA%\OpenBridge"
set "OB_TOKEN_FILE=%OB_DIR%\adapter-token.txt"
if not exist "%OB_DIR%" mkdir "%OB_DIR%"
if not exist "%OB_TOKEN_FILE%" (
  echo [3/5] Creating a private local connection token...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "$b=New-Object byte[] 32; [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b); [BitConverter]::ToString($b).Replace('-','').ToLower()" > "%OB_TOKEN_FILE%"
)
set /p OPENBRIDGE_ADAPTER_TOKEN=<"%OB_TOKEN_FILE%"
if "%OPENBRIDGE_ADAPTER_TOKEN:~31,1%"=="" (
  echo ERROR: Token file is missing or invalid: %OB_TOKEN_FILE%
  pause
  exit /b 1
)
set "OPENBRIDGE_GODOT_PORT=8766"
set "OPENBRIDGE_BROWSER_PORT=8767"
set "OPENBRIDGE_HOST=127.0.0.1"

echo [4/5] Preparing connection settings...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-Clipboard -Value '%OPENBRIDGE_ADAPTER_TOKEN%'" >nul 2>nul
if errorlevel 1 echo NOTE: Clipboard copy failed. Token is stored in "%OB_TOKEN_FILE%".
echo Local token saved to: %OB_TOKEN_FILE%
echo The token has been copied to your clipboard when supported.
echo Paste it into the OpenBridge browser extension settings.
echo.

if not "%~1"=="" set "GODOT_PROJECT=%~1"
if "%GODOT_PROJECT%"=="" (
  set /p "GODOT_PROJECT=Optional: paste your Godot project folder path, or press Enter to skip: "
)
if not "%GODOT_PROJECT%"=="" (
  if not exist "%GODOT_PROJECT%\project.godot" (
    echo WARNING: No project.godot found at "%GODOT_PROJECT%".
    echo Starting the MCP service only.
  ) else (
    set "GODOT_EXE="
    for /f "delims=" %%G in ('where godot.exe 2^>nul') do if not defined GODOT_EXE set "GODOT_EXE=%%G"
    for /f "delims=" %%G in ('where godot 2^>nul') do if not defined GODOT_EXE set "GODOT_EXE=%%G"
    if not defined GODOT_EXE set /p "GODOT_EXE=Paste full path to Godot 4 executable: "
    if exist "%GODOT_EXE%" (
      echo [5/5] Launching Godot with the same connection token...
      start "Godot - OpenBridge" "%GODOT_EXE%" --editor --path "%GODOT_PROJECT%"
    ) else (
      echo WARNING: Godot executable not found. Start Godot from this environment to share the token.
    )
  )
) else (
  echo NOTE: Godot was not launched. If Godot is already open, restart it with this launcher
  echo       or set OPENBRIDGE_ADAPTER_TOKEN to the same token before enabling the plugin.
)

echo.
echo OpenBridge MCP:     http://127.0.0.1:8765/mcp
echo Browser gateway:    http://127.0.0.1:8767
echo Keep this window open while using OpenBridge.
echo Do not expose these local services to your network.
echo.
".venv\Scripts\python.exe" -m openbridge.server
endlocal
