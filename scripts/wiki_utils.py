"""Shared utilities for selfOS wiki scripts."""

import os
import re
from pathlib import Path


def slugify(text, max_len=60):
    """Convert text to URL-friendly slug. Preserves CJK characters."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text[:max_len]


def build_frontmatter(title, date, tags, source_type, **extra):
    """Build YAML frontmatter string. Escapes quotes in title."""
    safe_title = title.replace('"', '\\"')
    lines = [
        '---',
        f'title: "{safe_title}"',
        f'type: source',
        f'created: {date}',
        f'updated: {date}',
        'sources: []',
        f'tags: [{tags}]',
        f'summary: "{safe_title}"',
        f'source_type: "{source_type}"',
    ]
    for k, v in extra.items():
        if isinstance(v, str):
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f'{k}: {v}')
    lines.append('---')
    return '\n'.join(lines)


def unique_filepath(output_dir, prefix, date, slug, ext='.md'):
    """Generate a unique filepath, appending counter if needed."""
    filename = f"{prefix}{date}-{slug}{ext}"
    filepath = Path(output_dir) / filename
    counter = 1
    while filepath.exists():
        filename = f"{prefix}{date}-{slug}-{counter}{ext}"
        filepath = Path(output_dir) / filename
        counter += 1
    return filepath


def read_file(path):
    """Read file with error handling. Returns None on failure."""
    try:
        return Path(path).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None


def strip_frontmatter(text):
    """Strip YAML frontmatter from markdown. Returns (frontmatter, body)."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if match:
        return match.group(1), match.group(2).strip()
    return '', text.strip()


def extract_fm_field(frontmatter, field):
    """Extract a field value from YAML frontmatter string."""
    match = re.search(rf'{field}: (.+)', frontmatter)
    if match:
        return match.group(1).strip().strip('"')
    return ''
