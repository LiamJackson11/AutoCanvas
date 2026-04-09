#!/usr/bin/env bash
# start.sh — AutoCanvas launcher for macOS and Linux

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Colour support ───────────────────────────────────────────────────────────
if [ -t 1 ] && command -v tput &>/dev/null && tput colors &>/dev/null; then
    R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)"
    C="$(tput setaf 6)" B="$(tput bold)"    N="$(tput sgr0)"
else
    R='' G='' Y='' C='' B='' N=''
fi

# ── Virtual environment ───────────────────────────────────────────────────────
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python3"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "${R}${B}✗ Virtual environment not found.${N}"
    echo "  Run the installer first:"
    echo "  ${C}  bash install.sh${N}"
    echo
    exit 1
fi

# Activate so any subprocesses the Python app spawns also use the venv
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# ── Ollama check ─────────────────────────────────────────────────────────────
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"

if ! curl -sf "$OLLAMA_URL/api/tags" &>/dev/null; then
    echo "${Y}${B}⚠ Ollama is not responding at $OLLAMA_URL${N}"

    if command -v ollama &>/dev/null; then
        echo "  Starting Ollama in the background…"
        # On macOS, 'ollama serve' would conflict with the menu-bar app,
        # so we try opening it as an app first
        if [[ "$(uname -s)" == "Darwin" ]] && open -a Ollama 2>/dev/null; then
            echo "  Waiting for Ollama to start…"
            for i in {1..10}; do
                sleep 1
                curl -sf "$OLLAMA_URL/api/tags" &>/dev/null && break
            done
        else
            ollama serve &>/dev/null &
            OLLAMA_PID=$!
            for i in {1..10}; do
                sleep 1
                curl -sf "$OLLAMA_URL/api/tags" &>/dev/null && break
            done
        fi

        if ! curl -sf "$OLLAMA_URL/api/tags" &>/dev/null; then
            echo "${R}${B}✗ Could not start Ollama automatically.${N}"
            echo "  Start it manually and try again:"
            echo "  ${C}  ollama serve${N}"
            exit 1
        fi
        echo "${G}✓ Ollama is running${N}"
    else
        echo "${R}${B}✗ Ollama is not installed.${N}"
        echo "  Install it from: ${C}https://ollama.com${N}"
        exit 1
    fi
fi

# ── Launch ───────────────────────────────────────────────────────────────────
"$VENV_PYTHON" run.py
