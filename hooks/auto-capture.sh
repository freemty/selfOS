#!/bin/bash
# Wiki Auto-Capture Hook (Stop)
# Pipes Claude Code session transcript to auto-ingest.py for wiki capture.
# Runs in background to avoid blocking Claude Code exit.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SELFOS_DIR="$(dirname "$SCRIPT_DIR")"
SCRIPT="$SELFOS_DIR/scripts/auto-ingest.py"

# Guard: script must exist
[ -f "$SCRIPT" ] || exit 0

# Read stdin (Stop hook JSON) and pipe to auto-ingest in background
INPUT=$(cat)
printf '%s' "$INPUT" | python3 "$SCRIPT" 2>/dev/null &

exit 0
