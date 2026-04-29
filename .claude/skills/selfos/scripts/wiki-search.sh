#!/bin/bash
# wiki-search.sh — Search wiki using qmd (hybrid) or grep (fallback)
# Usage: wiki-search.sh <wiki-root> <query>

WIKI_ROOT="$1"
QUERY="$2"

if [ -z "$WIKI_ROOT" ] || [ -z "$QUERY" ]; then
  echo "Usage: wiki-search.sh <wiki-root> <query>"
  exit 1
fi

WIKI_DIR="$WIKI_ROOT/wiki"

if [ ! -d "$WIKI_DIR" ]; then
  echo "Error: wiki directory not found at $WIKI_DIR"
  exit 1
fi

# Try qmd first (hybrid BM25 + semantic search)
if command -v qmd &> /dev/null; then
  echo "=== qmd search: $QUERY ==="
  echo ""
  qmd search "$QUERY" -n 10 -c wiki 2>/dev/null
  exit_code=$?
  if [ $exit_code -eq 0 ]; then
    echo ""
    echo "=== End of qmd results ==="
    exit 0
  fi
  echo "(qmd failed, falling back to grep)"
  echo ""
fi

# Fallback: grep-based search
echo "=== grep search: $QUERY ==="
echo ""

grep -r -i -F -l "$QUERY" "$WIKI_DIR" --include="*.md" 2>/dev/null | while read -r file; do
  rel_path="${file#$WIKI_DIR/}"
  title=$(grep -m1 "^title:" "$file" 2>/dev/null | sed 's/^title: *"*//;s/"*$//')
  if [ -z "$title" ]; then
    title="$rel_path"
  fi
  count=$(grep -c -i -F "$QUERY" "$file" 2>/dev/null)
  echo "[$count matches] $rel_path — $title"
done | sort -t'[' -k2 -rn

echo ""
echo "=== End of grep results ==="
