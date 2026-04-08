#!/usr/bin/env python3
"""Scan the LLM Wiki for context gaps and generate targeted interview questions.

Gap types (by priority):
  1. Open Questions  — unresolved bullets in concept pages
  2. Thin Pages       — concept/entity pages with < 100 body words
  2. Vague Entities   — entity pages with empty/thin Mentions section
  3. Timeline Gaps    — months with < 5 source entries

Note: Gap type 5 (cross-source contradictions) from the spec is intentionally
omitted — it requires LLM semantic understanding, not regex scanning.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

WIKI_ROOT = Path(__file__).resolve().parent.parent / "wiki"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_TITLE_RE = re.compile(r'^title:\s*["\']?(.*?)["\']?\s*$', re.MULTILINE)
_DATE_PREFIX_RE = re.compile(r"^(?:notion|cc|gem|auto)-(\d{4}-\d{2})")


def _read_file(path: Path) -> str | None:
    """Read a file, returning None on any I/O error."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _strip_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_block, body) from a markdown file."""
    m = _FRONTMATTER_RE.match(text)
    if m:
        return m.group(1), text[m.end():]
    return "", text


def _extract_title(frontmatter: str) -> str:
    """Pull the title value out of YAML frontmatter (simple regex, no PyYAML)."""
    m = _TITLE_RE.search(frontmatter)
    return m.group(1).strip() if m else ""


def _word_count(text: str) -> int:
    """Count words in a body string. CJK characters counted individually."""
    cleaned = re.sub(r"[#\[\]()>*_~`|]", " ", text)
    cjk_chars = len(re.findall(r'[\u4e00-\u9fff]', cleaned))
    non_cjk = re.sub(r'[\u4e00-\u9fff]', ' ', cleaned)
    en_words = len(non_cjk.split())
    return cjk_chars + en_words


def _section_text(body: str, heading: str) -> str | None:
    """Extract text under a ## heading until the next ## or EOF.

    Returns None if the heading does not exist.
    """
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(body)
    if m:
        return m.group(1).strip()
    return None


# ---------------------------------------------------------------------------
# Gap scanners
# ---------------------------------------------------------------------------


def scan_open_questions(questions: list[dict]) -> None:
    """Gap Type 1: Open Questions from concept pages."""
    concepts_dir = WIKI_ROOT / "concepts"
    if not concepts_dir.is_dir():
        return

    for path in sorted(concepts_dir.glob("*.md")):
        text = _read_file(path)
        if text is None:
            continue

        _, body = _strip_frontmatter(text)
        section = _section_text(body, "Open Questions")
        if section is None:
            continue

        for line in section.splitlines():
            line = line.strip()
            # Accept lines starting with - or *
            if not (line.startswith("- ") or line.startswith("* ")):
                continue
            bullet = line[2:].strip()
            if len(bullet) < 10:
                continue
            questions.append({
                "type": "open_question",
                "source": path.stem,
                "question": bullet,
                "priority": 1,
            })


def scan_thin_pages(questions: list[dict]) -> None:
    """Gap Type 2: Pages with fewer than 100 words."""
    for subdir in ("concepts", "entities"):
        directory = WIKI_ROOT / subdir
        if not directory.is_dir():
            continue

        for path in sorted(directory.glob("*.md")):
            text = _read_file(path)
            if text is None:
                continue

            fm, body = _strip_frontmatter(text)
            title = _extract_title(fm) or path.stem
            wc = _word_count(body)

            if wc < 100:
                questions.append({
                    "type": "thin_page",
                    "source": path.stem,
                    "question": (
                        f"Wiki 里关于'{title}'的记录很少（{wc} 词）。"
                        f"你能多讲讲这个话题吗？"
                    ),
                    "priority": 2,
                })


def scan_timeline_gaps(questions: list[dict]) -> None:
    """Gap Type 3: Months with fewer than 5 source entries."""
    sources_dir = WIKI_ROOT / "sources"
    if not sources_dir.is_dir():
        return

    month_counts: dict[str, int] = {}
    try:
        entries = list(sources_dir.iterdir())
    except OSError:
        return

    for entry in entries:
        if not entry.name.endswith(".md"):
            continue
        m = _DATE_PREFIX_RE.match(entry.name)
        if m:
            month = m.group(1)  # "YYYY-MM"
            month_counts[month] = month_counts.get(month, 0) + 1

    for month in sorted(month_counts):
        count = month_counts[month]
        if count < 5:
            questions.append({
                "type": "timeline_gap",
                "source": f"sources/{month}",
                "question": (
                    f"{month} 这个月的记录比较少（只有 {count} 条）。"
                    f"那段时间你在做什么？"
                ),
                "priority": 3,
            })


def scan_vague_entities(questions: list[dict]) -> None:
    """Gap Type 4: Entity pages with empty/thin Mentions section."""
    entities_dir = WIKI_ROOT / "entities"
    if not entities_dir.is_dir():
        return

    for path in sorted(entities_dir.glob("*.md")):
        text = _read_file(path)
        if text is None:
            continue

        fm, body = _strip_frontmatter(text)
        title = _extract_title(fm) or path.stem

        mentions = _section_text(body, "Mentions")
        # If section doesn't exist or is very short
        if mentions is not None and len(mentions) >= 50:
            continue
        # Only flag if there IS a Mentions heading but it's thin,
        # OR if there's no Mentions heading at all
        questions.append({
            "type": "vague_entity",
            "source": path.stem,
            "question": (
                f"你多次提到 {title}，但 wiki 里关于你们关系的描述不太详细。"
                f"你们是怎么认识的？"
            ),
            "priority": 2,
        })


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    questions: list[dict] = []

    scan_open_questions(questions)
    scan_thin_pages(questions)
    scan_timeline_gaps(questions)
    scan_vague_entities(questions)

    # Stable sort by priority (ascending — 1 = highest priority)
    questions.sort(key=lambda q: q["priority"])

    json.dump(questions, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
