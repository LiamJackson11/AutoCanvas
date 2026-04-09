#!/usr/bin/env bash
# AutoCanvas launcher for macOS and Linux
cd "$(dirname "$0")"

# Prefer python3; fall back to python if not found
if command -v python3 &>/dev/null; then
    python3 run.py
elif command -v python &>/dev/null; then
    python run.py
else
    echo "Python not found. Install it from https://www.python.org/downloads/"
    exit 1
fi
