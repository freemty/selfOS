#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail() {
  echo "agent parity check failed: $*" >&2
  exit 1
}

grep_cmd() {
  if command -v rg >/dev/null 2>&1; then
    rg "$@"
  else
    local pattern="$1"
    shift
    grep -R -n -E "$pattern" "$@"
  fi
}

required_files=(
  "CLAUDE.md"
  "AGENTS.md"
  ".claude/skills/wiki/skill.md"
  ".agents/skills/wiki/SKILL.md"
  "setup.sh"
  "scripts/recount-index.py"
)

for file in "${required_files[@]}"; do
  [ -f "$file" ] || fail "missing required file: $file"
done

claude_skills="$(find .claude/skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort)"
codex_skills="$(find .agents/skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort)"

[ -n "$claude_skills" ] || fail "no Claude skills found"
[ -n "$codex_skills" ] || fail "no Codex skills found"

if [ "$claude_skills" != "$codex_skills" ]; then
  echo "Claude skills:" >&2
  printf '%s\n' "$claude_skills" | sed 's/^/  /' >&2
  echo "Codex skills:" >&2
  printf '%s\n' "$codex_skills" | sed 's/^/  /' >&2
  fail "Claude and Codex skill sets differ"
fi

for skill in $claude_skills; do
  [ -f ".claude/skills/$skill/skill.md" ] || fail "missing Claude entry for $skill"
  [ -f ".agents/skills/$skill/SKILL.md" ] || fail "missing Codex entry for $skill"
done

if grep_cmd '\.Codex|~/\.Codex|/Users/sum_young|~/knowledge-base|每次 Codex 对话结束时' \
  AGENTS.md setup.sh scripts hooks .agents/skills .claude/skills docs/knowhow docs/specs >/tmp/selfos-parity-grep.raw 2>/dev/null; then
  grep -v '^scripts/check_agent_parity.sh:' /tmp/selfos-parity-grep.raw >/tmp/selfos-parity-grep.txt || true
  if [ -s /tmp/selfos-parity-grep.txt ]; then
    cat /tmp/selfos-parity-grep.txt >&2
    fail "stale Codex path, local user path, or over-broad Codex hook claim found"
  fi
fi

if grep_cmd '~/.claude/skills/wiki/scripts/wiki-search.sh' .agents/skills/wiki/references/query-workflow.md >/tmp/selfos-parity-grep.txt 2>/dev/null; then
  cat /tmp/selfos-parity-grep.txt >&2
  fail "Codex query workflow points at Claude skill path"
fi

if grep_cmd 'AGENTS.md / AGENTS.md|Codex Opus' AGENTS.md CLAUDE.md .agents/skills .claude/skills >/tmp/selfos-parity-grep.txt 2>/dev/null; then
  cat /tmp/selfos-parity-grep.txt >&2
  fail "known parity drift string found"
fi

echo "agent parity check passed"
