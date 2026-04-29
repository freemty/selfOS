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

# Preference / judgment signals for pending_questions generation
# These indicate unexpanded opinions, preferences, or reactions
PREFERENCE_SIGNALS = [
    # Unexpanded judgments (require subjective prefix to avoid technical chatter)
    (r"我觉得(.{5,40}?)(?:比|不如|好于|强于)", "judgment",
     "你说'{match}'——具体指什么场景下？基于什么判断？"),
    (r"(?:我觉得|我认为|我看)(.{3,30}?)(?:不行|没前途|没戏|废了)", "judgment",
     "你提到'{match}'——是基于什么观察？在什么条件下？"),

    # Vague ideas
    (r"(?:我在想|我想|感觉)(.{5,50}?)(?:会不会|是不是|可能)", "vague_idea",
     "你说'{match}'——能展开说说吗？具体怎么关联的？"),
    (r"感觉(.{5,40}?)(?:和|跟)(.{3,20}?)有关系", "vague_idea",
     "你觉得'{g1}'和'{g2}'有关——具体怎么关联？"),

    # Emotional reactions (require subjective prefix)
    (r"(?:被|让)(.{3,30}?)(?:震撼|震惊|感动|启发)", "emotional",
     "你说被'{match}'震撼——具体是什么触动了你？"),
    (r"(?:真的|确实|简直|真是)(.{0,30}?)(?:太爽了|太牛了|太强了|太厉害)", "emotional",
     "你说'{match}'——具体是哪个点让你这么觉得？"),

    # Unexpanded preferences (anchor to sentence boundary)
    (r"(?:我比较倾向|我偏向|我更喜欢)(.{5,40}?)(?:[，。！；\n]|$)", "preference",
     "你说倾向'{match}'——基于什么考虑？"),
    (r"(?:以后|之后|未来)(?:可能会|打算|想)(.{5,40}?)(?:[，。！；\n]|$)", "preference",
     "你提到未来可能'{match}'——目前是什么推动了这个想法？"),
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


def extract_pending_questions(text):
    """Extract pending questions from preference/judgment signals in text.

    Returns a list of question strings, or empty list if none found.
    Keeps only user messages for scanning (lines starting with [User]).
    """
    # Only scan user messages
    user_lines = []
    for line in text.split("\n"):
        if line.startswith("[User]"):
            user_lines.append(line[6:].strip())
    user_text = "\n".join(user_lines)

    if not user_text:
        return []

    questions = []
    seen = set()

    for pattern, _signal_type, template in PREFERENCE_SIGNALS:
        for m in re.finditer(pattern, user_text):
            # Build question from template
            match_text = m.group(1).strip() if m.lastindex >= 1 else ""
            if not match_text or match_text in seen:
                continue
            seen.add(match_text)

            question = template.replace("{match}", match_text)
            if m.lastindex and m.lastindex >= 2:
                question = question.replace("{g1}", m.group(1).strip())
                question = question.replace("{g2}", m.group(2).strip())

            questions.append(question)

    # Cap at 3 questions per session to avoid noise
    return questions[:3]


def build_frontmatter(title, date_str, pending_questions=None):
    """Build YAML frontmatter for the source page."""
    safe_title = title.replace('"', '\\"')
    lines = [
        '---',
        f'title: "{safe_title}"',
        'type: source',
        f'created: {date_str}',
        f'updated: {date_str}',
        'sources: []',
        'tags: [auto-captured, cc-session]',
        'summary: "Auto-captured from Claude Code session"',
        'source_type: "cc-session"',
        'confidence: low',
    ]
    if pending_questions:
        lines.append('pending_questions:')
        for q in pending_questions:
            safe_q = q.replace('"', '\\"')
            lines.append(f'  - "{safe_q}"')
    lines.append('---')
    return '\n'.join(lines)


def save_source(text, date_str, slug):
    """Save conversation as a wiki source page. Returns filepath or None."""
    time_str = datetime.now().strftime("%H%M")
    filename = f"auto-{date_str}-{time_str}-{slug}.md"
    filepath = SOURCES_DIR / filename

    # Idempotency: skip if file already exists
    if filepath.exists():
        return None

    # Extract pending questions before truncating
    pending_qs = extract_pending_questions(text)

    # Truncate to max chars
    truncated = text[:MAX_CHARS]
    if len(text) > MAX_CHARS:
        truncated += "\n\n(truncated at 10000 chars)"

    # Build title from slug
    title = slug.replace("-", " ")

    frontmatter = build_frontmatter(title, date_str, pending_qs)
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
