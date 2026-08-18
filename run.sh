#!/bin/bash
# Activate virtual environment and run the Smart Traffic Control System
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
PYTHONPATH="$SCRIPT_DIR/src:$PYTHONPATH" python "$SCRIPT_DIR/src/main.py" "$@"
