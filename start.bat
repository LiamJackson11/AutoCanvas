@echo off
cd /d "%~dp0"

:: ── Virtual environment ──────────────────────────────────────────────────────
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found.
    echo Run the installer first:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

:: ── Launch ───────────────────────────────────────────────────────────────────
:: Try the Windows Python Launcher first (handles multiple Python versions),
:: then fall back to the plain 'python' command from the venv.
where py >nul 2>&1
if %errorlevel% == 0 (
    py run.py
) else (
    python run.py
)

pause
