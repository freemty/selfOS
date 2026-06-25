#!/bin/bash
set -euo pipefail

SELFOS_DIR="$(cd "$(dirname "$0")" && pwd)"

TARGET="all"
REGISTER_HOOK="ask"

usage() {
  cat <<'EOF'
Usage: ./setup.sh [--target claude|codex|all] [--hook|--no-hook]

Registers selfOS skills as global symlinks.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --target=*)
      TARGET="${1#*=}"
      shift
      ;;
    --hook)
      REGISTER_HOOK="yes"
      shift
      ;;
    --no-hook)
      REGISTER_HOOK="no"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

case "$TARGET" in
  claude|codex|all) ;;
  *)
    echo "Invalid target: $TARGET" >&2
    usage >&2
    exit 1
    ;;
esac

SKILLS=(
  wiki
  interview
  thought
  digest
  todo
  wiki-help
  academic-writing
  paper-plot
  transcribe
  de-ai
)

echo "selfOS Setup"
echo "============"
echo ""

install_links() {
  local source_root="$1"
  local dest_root="$2"
  local entry_file="$3"
  local label="$4"

  mkdir -p "$dest_root"

  echo "Registering $label skill symlinks..."
  for skill in "${SKILLS[@]}"; do
    local target="$source_root/$skill"
    local link="$dest_root/$skill"
    if [ ! -f "$target/$entry_file" ]; then
      echo "  skip $skill (missing $entry_file)"
      continue
    fi
    if [ -L "$link" ]; then
      local current
      current="$(readlink "$link")"
      if [ "$current" = "$target" ]; then
        echo "  ok $skill"
      else
        ln -sfn "$target" "$link"
        echo "  -> $skill"
      fi
    elif [ -e "$link" ]; then
      echo "  skip $skill (real file/dir exists at $link)"
    else
      ln -s "$target" "$link"
      echo "  + $skill"
    fi
  done
}

if [ "$TARGET" = "claude" ] || [ "$TARGET" = "all" ]; then
  install_links "$SELFOS_DIR/.claude/skills" "$HOME/.claude/skills" "skill.md" "Claude"
  echo ""
fi

if [ "$TARGET" = "codex" ] || [ "$TARGET" = "all" ]; then
  install_links "$SELFOS_DIR/.agents/skills" "$HOME/.agents/skills" "SKILL.md" "Codex"
  echo ""
fi

if [ "$TARGET" = "claude" ] || [ "$TARGET" = "all" ]; then
  if [ "$REGISTER_HOOK" = "ask" ]; then
    echo "Auto-Capture hook registers a Stop hook that silently captures"
    echo "personal context from Claude Code sessions into your wiki."
    echo ""
    read -r -p "Register Auto-Capture hook? (y/n) " REPLY
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      REGISTER_HOOK="yes"
    else
      REGISTER_HOOK="no"
    fi
  fi

  if [ "$REGISTER_HOOK" = "yes" ]; then
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
fi

echo "Done."
if [ "$TARGET" = "codex" ] || [ "$TARGET" = "all" ]; then
  echo "Codex users: restart the Codex session if newly installed skills do not appear immediately."
fi
