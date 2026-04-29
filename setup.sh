#!/bin/bash
set -e

SELFOS_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

echo "selfOS Setup"
echo "============"
echo ""

# Ensure ~/.claude/skills exists
mkdir -p "$SKILLS_DIR"

# 1. Global skill symlinks
echo "Registering global skill symlinks..."
for skill in selfos selfos-completion thought digest; do
  target="$SELFOS_DIR/.claude/skills/$skill"
  link="$SKILLS_DIR/$skill"
  if [ ! -d "$target" ]; then
    echo "  skip $skill (not found in repo)"
    continue
  fi
  if [ -L "$link" ] || [ -d "$link" ]; then
    echo "  skip $skill (already exists)"
  else
    ln -s "$target" "$link"
    echo "  + $skill"
  fi
done

# 2. Auto-Capture hook (optional)
echo ""
echo "Auto-Capture hook registers a Stop hook that silently captures"
echo "personal context from Claude Code sessions into your wiki."
echo ""
read -p "Register Auto-Capture hook? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo ""
  echo "Add this to ~/.claude/settings.json under \"Stop\" hooks:"
  echo ""
  echo "  {"
  echo "    \"hooks\": [{"
  echo "      \"command\": \"bash $SELFOS_DIR/hooks/auto-capture.sh\","
  echo "      \"type\": \"command\""
  echo "    }],"
  echo "    \"matcher\": \"\""
  echo "  }"
  echo ""
fi

echo ""
echo "Done. Run '/wiki init' in Claude Code to initialize your wiki."
echo "Then try '/thought your first idea' to get started."
