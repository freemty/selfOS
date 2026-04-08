#!/usr/bin/env python3
"""
Auto-ingest personal context from Claude Code sessions into the LLM Wiki.

Reads conversation text from stdin (Stop hook JSON with transcript_path,
or raw text). Checks for personal context signals, saves as a wiki source
page if found.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WIKI_ROOT = Path.home() / "knowledge-base"
SOURCES_DIR = WIKI_ROOT / "wiki" / "sources"
LOG_PATH = WIKI_ROOT / "wiki" / "log.md"
MAX_CHARS = 10000

# Personal context signals — need >= 2 matches
PERSONAL_SIGNALS_ZH = [
    r"我觉得",
    r"我发现",
    r"今天",
    r"最近",
    r"感觉",
    r"震撼",
    r"反思",
    r"我认为",
    r"我想",
    r"让我",
    r"我在",
    r"我的",
    r"我们",
    r"我做",
    r"对我",
    r"我决定",
    r"我尝试",
    r"我打算",
    r"我意识到",
    r"我学到",
]

PERSONAL_SIGNALS_EN = [
    r"\bI think\b",
    r"\bI found\b",
    r"\bI realized\b",
    r"\bI feel\b",
    r"\btoday\b",
    r"\brecently\b",
    r"\bmy experience\b",
    r"\bI decided\b",
    r"\bI noticed\b",
    r"\bI learned\b",
    r"\bI tried\b",
    r"\bI want\b",
    r"\bI plan\b",
    r"\bI struggle\b",
    r"\bI believe\b",
]


def read_input():
    """Read conversation text from stdin.

    Handles both:
    - Stop hook JSON (with transcript_path pointing to JSONL)
    - Raw text piped directly
    """
    raw = sys.stdin.read().strip()
    if not raw:
        return ""

    # Try parsing as Stop hook JSON
    try:
        data = json.loads(raw)
        transcript_path = data.get("transcript_path", "")
        if transcript_path and os.path.exists(transcript_path):
            return _read_transcript(transcript_path)
        # If JSON but no transcript_path, treat as raw text
        return raw
    except (json.JSONDecodeError, TypeError):
        pass

    return raw


def _read_transcript(path):
    """Read a Claude Code JSONL transcript file and extract text."""
    lines = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    role = entry.get("role", "")
                    content = entry.get("content", "")
                    if isinstance(content, list):
                        parts = []
                        for block in content:
                            if isinstance(block, dict):
                                text = block.get("text", "")
                                if text:
                                    parts.append(text)
                            elif isinstance(block, str):
                                parts.append(block)
                        content = "\n".join(parts)
                    if content and role in ("user", "assistant"):
                        prefix = "[User]" if role == "user" else "[Assistant]"
                        lines.append(f"{prefix} {content}")
                except (json.JSONDecodeError, TypeError):
                    continue
    except (OSError, IOError):
        return ""

    return "\n\n".join(lines)


def has_personal_context(text):
    """Check if text contains personal context (>= 2 signal matches)."""
    min_len = 20 if re.search(r'[\u4e00-\u9fff]', text) else 50
    if len(text) < min_len:
        return False

    matches = 0
    for pattern in PERSONAL_SIGNALS_ZH:
        if re.search(pattern, text):
            matches += 1
        if matches >= 2:
            return True

    for pattern in PERSONAL_SIGNALS_EN:
        if re.search(pattern, text, re.IGNORECASE):
            matches += 1
        if matches >= 2:
            return True

    return False


def generate_slug(text):
    """Generate a URL-friendly slug from the first meaningful line."""
    # Try to find a meaningful title from the text
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Skip role prefixes like [User] or [Assistant]
    title_candidates = []
    for line in lines[:10]:
        cleaned = re.sub(r"^\[(User|Assistant)\]\s*", "", line)
        cleaned = cleaned.strip()
        if len(cleaned) > 5:
            title_candidates.append(cleaned)

    title = title_candidates[0] if title_candidates else "session"

    # Truncate to reasonable length
    title = title[:60]

    # For Chinese text, keep Chinese characters
    # For mixed text, keep alphanumeric and Chinese
    slug = re.sub(r"[^\w\u4e00-\u9fff-]", "-", title)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-").lower()

    if not slug:
        slug = "session"

    return slug


def build_frontmatter(title, date_str):
    """Build YAML frontmatter for the source page."""
    return f"""---
title: "{title}"
type: source
created: {date_str}
updated: {date_str}
sources: []
tags: [auto-captured, cc-session]
summary: "Auto-captured from Claude Code session"
source_type: "cc-session"
confidence: low
---"""


def save_source(text, date_str, slug):
    """Save conversation as a wiki source page. Returns filepath or None."""
    time_str = datetime.now().strftime("%H%M")
    filename = f"auto-{date_str}-{time_str}-{slug}.md"
    filepath = SOURCES_DIR / filename

    # Idempotency: skip if file already exists
    if filepath.exists():
        return None

    # Truncate to max chars
    truncated = text[:MAX_CHARS]
    if len(text) > MAX_CHARS:
        truncated += "\n\n(truncated at 10000 chars)"

    # Build title from slug
    title = slug.replace("-", " ")

    frontmatter = build_frontmatter(title, date_str)
    content = f"""{frontmatter}

# {title}

## Session Content

{truncated}
"""

    filepath.write_text(content, encoding="utf-8")
    return filepath


def append_log(date_str, slug, filepath):
    """Append entry to wiki/log.md."""
    entry = (
        f"\n## [{date_str}] auto-ingest | cc-session\n"
        f"- **Source**: Claude Code session (auto-captured)\n"
        f"- **File**: `{filepath.relative_to(WIKI_ROOT)}`\n"
    )

    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(entry)
    except (OSError, IOError):
        pass


def git_commit(filepath):
    """Silently git add + commit the new source page."""
    try:
        subprocess.run(
            ["git", "add", str(filepath), str(LOG_PATH)],
            cwd=str(WIKI_ROOT),
            capture_output=True,
            timeout=10,
        )
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"auto: ingest cc-session {filepath.name}",
            ],
            cwd=str(WIKI_ROOT),
            capture_output=True,
            timeout=10,
        )
    except (subprocess.TimeoutExpired, OSError):
        pass


def main():
    try:
        text = read_input()
        if not text:
            sys.exit(0)

        if not has_personal_context(text):
            sys.exit(0)

        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = generate_slug(text)

        filepath = save_source(text, date_str, slug)
        if filepath is None:
            # File already exists (idempotent)
            sys.exit(0)

        append_log(date_str, slug, filepath)
        git_commit(filepath)

    except Exception:
        # Never crash — this is a background hook
        sys.exit(0)


if __name__ == "__main__":
    main()
