#!/usr/bin/env bash
# install.sh — AutoCanvas installer for macOS and Linux
# Sets up a virtual environment, installs dependencies, and optionally
# registers the app as a desktop application (Linux only).

set -uo pipefail

# ── Directory this script lives in (works even if called from elsewhere) ────
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$INSTALL_DIR"

# ── Colour support ───────────────────────────────────────────────────────────
if [ -t 1 ] && command -v tput &>/dev/null && tput colors &>/dev/null; then
    R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)"
    C="$(tput setaf 6)" B="$(tput bold)"    N="$(tput sgr0)"
else
    R='' G='' Y='' C='' B='' N=''
fi

# ── Helpers ──────────────────────────────────────────────────────────────────
info()    { echo "${C}${B}▸${N} $*"; }
ok()      { echo "${G}${B}✓${N} $*"; }
warn()    { echo "${Y}${B}⚠${N} $*"; }
err()     { echo "${R}${B}✗${N} $*" >&2; }
die()     { err "$*"; exit 1; }
section() { echo; echo "${B}── $* ──────────────────────────────────────────${N}"; }

# ── Detect OS ────────────────────────────────────────────────────────────────
OS_NAME="$(uname -s)"
case "$OS_NAME" in
    Darwin) PLATFORM="macOS" ;;
    Linux)  PLATFORM="Linux" ;;
    *)      die "Unsupported platform: $OS_NAME. Use start.bat on Windows." ;;
esac

# ── Banner ───────────────────────────────────────────────────────────────────
echo
echo "${C}${B}╔══════════════════════════════════════════╗${N}"
echo "${C}${B}║      AutoCanvas — Installer              ║${N}"
echo "${C}${B}║      Platform: ${PLATFORM}$(printf '%*s' $((26 - ${#PLATFORM})) '')║${N}"
echo "${C}${B}╚══════════════════════════════════════════╝${N}"
echo

# ════════════════════════════════════════════════════════════════════════════
section "Python"
# ════════════════════════════════════════════════════════════════════════════

# Find a Python >= 3.10 interpreter
PYTHON=""
for cmd in python3 python python3.14 python3.13 python3.12 python3.11 python3.10; do
    if command -v "$cmd" &>/dev/null; then
        ver_str=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null) || continue
        major="${ver_str%%.*}"
        minor="${ver_str##*.}"
        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    err "Python 3.10 or newer is required but was not found."
    echo
    if [ "$PLATFORM" = "macOS" ]; then
        echo "  Install options:"
        echo "  ${B}Homebrew${N} (recommended):  brew install python@3.12"
        echo "  ${B}Official installer${N}:       https://www.python.org/downloads/"
    else
        echo "  Install options:"
        echo "  ${B}Ubuntu/Debian${N}:  sudo apt install python3"
        echo "  ${B}Fedora${N}:         sudo dnf install python3"
        echo "  ${B}Arch${N}:           sudo pacman -S python"
    fi
    exit 1
fi

PY_VERSION=$("$PYTHON" -c "import sys; print(sys.version.split()[0])")
ok "Found $PYTHON  ($PY_VERSION)"

# ════════════════════════════════════════════════════════════════════════════
section "Ollama"
# ════════════════════════════════════════════════════════════════════════════

if command -v ollama &>/dev/null; then
    OLLAMA_VERSION="$(ollama --version 2>/dev/null | head -1 || echo 'unknown version')"
    ok "Ollama found  ($OLLAMA_VERSION)"
else
    warn "Ollama not found — AutoCanvas needs it to run the local AI model."
    echo
    if [ "$PLATFORM" = "macOS" ]; then
        echo "  Install options:"
        echo "  ${B}Homebrew${N}:         brew install ollama"
        echo "  ${B}Official pkg${N}:     https://ollama.com/download/mac"
    else
        echo "  Quick install:   curl -fsSL https://ollama.com/install.sh | sh"
        echo "  Official page:   https://ollama.com/download/linux"
    fi
    echo
    # Don't block installation — user may install Ollama later
    read -r -p "  Continue anyway? [y/N] " ans
    [[ "${ans,,}" =~ ^y ]] || { echo "  Aborted."; exit 0; }
fi

# ════════════════════════════════════════════════════════════════════════════
section "Virtual Environment"
# ════════════════════════════════════════════════════════════════════════════

VENV_DIR="$INSTALL_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
    warn "Virtual environment already exists at .venv/"
    read -r -p "  Recreate it? [y/N] " ans
    if [[ "${ans,,}" =~ ^y ]]; then
        info "Removing old virtual environment…"
        rm -rf "$VENV_DIR"
    else
        ok "Keeping existing virtual environment"
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment in .venv/…"
    "$PYTHON" -m venv "$VENV_DIR" || die "Failed to create virtual environment"
    ok "Virtual environment created"
fi

VENV_PYTHON="$VENV_DIR/bin/python3"
VENV_PIP="$VENV_DIR/bin/pip"

# ════════════════════════════════════════════════════════════════════════════
section "Dependencies"
# ════════════════════════════════════════════════════════════════════════════

info "Upgrading pip…"
"$VENV_PIP" install --upgrade pip --quiet

info "Installing packages from requirements.txt…"
"$VENV_PIP" install -r "$INSTALL_DIR/requirements.txt" \
    || die "Dependency installation failed. Check the error above."

ok "All packages installed"

# Show installed versions of key packages
echo
echo "  ${B}Key packages:${N}"
for pkg in canvasapi openai rich pypdf; do
    ver=$("$VENV_PIP" show "$pkg" 2>/dev/null | awk '/^Version:/{print $2}')
    printf "  %-16s %s\n" "$pkg" "${ver:-not found}"
done

# ════════════════════════════════════════════════════════════════════════════
section "Scripts"
# ════════════════════════════════════════════════════════════════════════════

chmod +x "$INSTALL_DIR/start.sh"
ok "start.sh is executable"

# macOS: also create start.command so it can be double-clicked in Finder
if [ "$PLATFORM" = "macOS" ]; then
    COMMAND_FILE="$INSTALL_DIR/start.command"
    cat > "$COMMAND_FILE" <<'CMDEOF'
#!/usr/bin/env bash
# start.command — macOS double-click launcher (opens in Terminal automatically)
cd "$(dirname "$0")"
./start.sh
CMDEOF
    chmod +x "$COMMAND_FILE"
    ok "start.command created  (double-click this in Finder to launch)"
fi

# ════════════════════════════════════════════════════════════════════════════
section "Desktop Entry  (Linux only)"
# ════════════════════════════════════════════════════════════════════════════

if [ "$PLATFORM" = "Linux" ]; then
    DESKTOP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
    DESKTOP_FILE="$DESKTOP_DIR/autocanvas.desktop"

    read -r -p "  Install AutoCanvas in your application menu? [Y/n] " ans
    if [[ ! "${ans,,}" =~ ^n ]]; then
        mkdir -p "$DESKTOP_DIR"
        cat > "$DESKTOP_FILE" <<DESKTOPEOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AutoCanvas
GenericName=Homework Assistant
Comment=Local AI Canvas homework assistant — private, no cloud
Exec=bash -c "cd '${INSTALL_DIR}' && ./start.sh"
Terminal=true
Categories=Education;Utility;
Keywords=canvas;homework;ai;school;
StartupNotify=false
DESKTOPEOF
        # Notify the desktop environment about the new entry
        if command -v update-desktop-database &>/dev/null; then
            update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
        fi
        ok "Desktop entry installed at $DESKTOP_FILE"
        info "AutoCanvas will appear in your application launcher after logging out and back in"
    else
        info "Skipped desktop entry"
    fi
fi

# ════════════════════════════════════════════════════════════════════════════
section "Done"
# ════════════════════════════════════════════════════════════════════════════

echo
echo "${G}${B}AutoCanvas is ready.${N}"
echo
echo "  Next steps:"
if [ "$PLATFORM" = "macOS" ]; then
    echo "  ${B}1.${N} Make sure Ollama is running (click it in your menu bar)"
    echo "  ${B}2.${N} Pull a model if you haven't:  ${C}ollama pull mistral-nemo${N}"
    echo "  ${B}3.${N} Double-click ${C}start.command${N} in Finder"
    echo "      or run:  ${C}./start.sh${N}"
else
    echo "  ${B}1.${N} Make sure Ollama is running:   ${C}ollama serve${N}"
    echo "  ${B}2.${N} Pull a model if you haven't:  ${C}ollama pull mistral-nemo${N}"
    echo "  ${B}3.${N} Launch AutoCanvas:             ${C}./start.sh${N}"
fi
echo
