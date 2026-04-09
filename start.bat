@echo off
cd /d "%~dp0"

:: Try the Python Launcher first (handles multiple Python versions on Windows),
:: then fall back to the plain 'python' command.
where py >nul 2>&1
if %errorlevel% == 0 (
    py run.py
) else (
    python run.py
)

pause
