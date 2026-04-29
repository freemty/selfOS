#!/usr/bin/env python3
"""
Extract ALL user messages from conversations into rich source pages.

Principle: Preserve every word the user said, verbatim.
Remove AI responses. Keep chronological order.
The user's voice IS the data. Summaries are secondary.

Handles three data sources:
1. Notion notes — already markdown, mostly title-is-content
2. Claude conversations — JSON with chat_messages
3. Gemini conversations — markdown with --- User --- / --- Gemini --- blocks
"""

import json
import os
import re
import sys
from pathlib import Path


def slugify(text, max_len=60):
    text = text.lower().strip()
    text = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text[:max_len]


# ============================================================
# Gemini extraction
# ============================================================

def extract_gemini(gemini_dir, output_dir):
    """Extract user messages from Gemini conversations."""
    gemini_path = Path(gemini_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    files = sorted([f for f in gemini_path.glob('*.md') if f.name != '_all_conversations.md'])
    print(f"[Gemini] Processing {len(files)} conversations...")

    created = 0
    for f in files:
        content = f.read_text(encoding='utf-8')

        # Extract metadata
        title_match = re.search(r'Conversation: (.+)', content)
        title = title_match.group(1).strip() if title_match else f.stem

        msg_count_match = re.search(r'Messages: (\d+)', content)
        msg_count = int(msg_count_match.group(1)) if msg_count_match else 0

        url_match = re.search(r'URL: (.+)', content)
        url = url_match.group(1).strip() if url_match else ''

        # Date from filename
        fname_date_match = re.match(r'(\d{8})_', f.name)
        date = ''
        if fname_date_match:
            d = fname_date_match.group(1)
            date = f"{d[:4]}-{d[4:6]}-{d[6:8]}"

        # Extract the FULL conversation — both user and Gemini, with speaker labels
        # Skip the header block (everything before first --- User ---)
        conversation_body = content.split('--- User ---', 1)
        if len(conversation_body) < 2:
            continue

        raw_dialogue = '--- User ---' + conversation_body[1]
        # Convert to markdown-friendly format with bold speaker labels
        raw_dialogue = raw_dialogue.replace('--- User ---', '\n**[我]**\n')
        raw_dialogue = raw_dialogue.replace('--- Gemini ---', '\n**[Gemini]**\n')
        raw_dialogue = raw_dialogue.strip()

        # Count user messages
        user_msg_count = content.count('--- User ---')

        slug = slugify(title)
        if not slug:
            slug = f.stem[:50]

        out_filename = f"gem-{date}-{slug}.md"
        out_filepath = output_path / out_filename

        counter = 1
        while out_filepath.exists():
            out_filename = f"gem-{date}-{slug}-{counter}.md"
            out_filepath = output_path / out_filename
            counter += 1

        page = f"""---
title: "{title}"
type: source
created: {date}
updated: {date}
sources: []
tags: [gemini-conversation]
summary: "{title}"
source_type: "gemini-conversation"
gemini_url: "{url}"
message_count: {msg_count}
user_message_count: {user_msg_count}
---

# {title}

{raw_dialogue}
"""
        out_filepath.write_text(page, encoding='utf-8')
        created += 1

    print(f"[Gemini] Created: {created} source pages")
    return created


# ============================================================
# Claude extraction
# ============================================================

def extract_claude(export_dir, output_dir):
    """Extract user messages from Claude conversations JSON."""
    conv_file = Path(export_dir) / 'conversations.json'
    if not conv_file.exists():
        print(f"[Claude] conversations.json not found at {conv_file}")
        return 0

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(conv_file) as f:
        conversations = json.load(f)

    print(f"[Claude] Processing {len(conversations)} conversations...")

    created = 0
    for conv in conversations:
        name = conv.get('name', '').strip()
        messages = conv.get('chat_messages', [])
        summary = conv.get('summary', '').strip()
        created_date = conv.get('created_at', '')[:10]
        uuid = conv.get('uuid', '')

        # Skip unnamed with < 3 messages
        if not name and len(messages) < 3:
            continue

        # Generate name from first message if needed
        if not name:
            human_msgs = [m for m in messages if m.get('sender') == 'human']
            if human_msgs:
                name = human_msgs[0].get('text', '')[:60].replace('\n', ' ').strip()
            if not name:
                continue

        # Extract the FULL conversation — both human and assistant, with speaker labels
        dialogue_parts = []
        user_msg_count = 0
        for m in messages:
            sender = m.get('sender', '')
            text = m.get('text', '').strip()
            if not text:
                continue
            if sender == 'human':
                dialogue_parts.append(f'**[我]**\n\n{text}')
                user_msg_count += 1
            elif sender == 'assistant':
                dialogue_parts.append(f'**[Claude]**\n\n{text}')

        if not dialogue_parts:
            continue

        slug = slugify(name)
        if not slug:
            slug = f"conv-{uuid[:8]}"

        out_filename = f"cc-{created_date}-{slug}.md"
        out_filepath = output_path / out_filename

        counter = 1
        while out_filepath.exists():
            out_filename = f"cc-{created_date}-{slug}-{counter}.md"
            out_filepath = output_path / out_filename
            counter += 1

        raw_dialogue = '\n\n---\n\n'.join(dialogue_parts)

        # Claude's conversation summary at the top as context
        summary_section = ""
        if summary:
            summary_section = f"""## AI Summary

{summary}

---

"""

        page = f"""---
title: "{name}"
type: source
created: {created_date}
updated: {created_date}
sources: []
tags: [claude-conversation]
summary: "{name}"
source_type: "claude-conversation"
uuid: "{uuid}"
message_count: {len(messages)}
user_message_count: {user_msg_count}
---

# {name}

{summary_section}## Full Conversation

{raw_dialogue}
"""

        out_filepath.write_text(page, encoding='utf-8')
        created += 1

    print(f"[Claude] Created: {created} source pages")
    return created


# ============================================================
# Notion extraction (re-process to ensure consistency)
# ============================================================

def extract_notion(notion_dir, output_dir):
    """Re-extract Notion notes — these are already the user's own words."""
    notion_path = Path(notion_dir)
    output_path = Path(output_dir)

    files = sorted([f for f in notion_path.glob('*.md') if f.name != '_manifest.md'])
    print(f"[Notion] Processing {len(files)} notes...")

    created = 0
    for f in files:
        content = f.read_text(encoding='utf-8')

        # Parse existing frontmatter
        fm_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if not fm_match:
            continue

        frontmatter = fm_match.group(1)
        body = fm_match.group(2).strip()

        # Extract fields
        title_match = re.search(r'title: "(.+?)"', frontmatter)
        title = title_match.group(1) if title_match else f.stem

        date_match = re.search(r'date: (.+)', frontmatter)
        date = date_match.group(1).strip().strip('"') if date_match else ''

        type_match = re.search(r'type: (.+)', frontmatter)
        note_type = type_match.group(1).strip().strip('"') if type_match else 'note'

        notion_id_match = re.search(r'notion_id: (.+)', frontmatter)
        notion_id = notion_id_match.group(1).strip().strip('"') if notion_id_match else ''

        notion_url_match = re.search(r'notion_url: (.+)', frontmatter)
        notion_url = notion_url_match.group(1).strip().strip('"') if notion_url_match else ''

        # The body IS the user's voice — keep it all
        # If body is empty, the title IS the content
        user_voice = body if body else title

        slug = slugify(title)
        if not slug:
            slug = f.stem[:50]

        # Use original filename date prefix
        fname_date = f.name[:10]  # e.g., "2025-09-09"

        out_filename = f"notion-{fname_date}-{slug}.md"
        out_filepath = output_path / out_filename

        counter = 1
        while out_filepath.exists():
            out_filename = f"notion-{fname_date}-{slug}-{counter}.md"
            out_filepath = output_path / out_filename
            counter += 1

        page = f"""---
title: "{title}"
type: source
created: {date if date else fname_date}
updated: {date if date else fname_date}
sources: []
tags: [{note_type}]
summary: "{title}"
source_type: "notion-{note_type}"
notion_id: "{notion_id}"
notion_url: "{notion_url}"
---

# {title}

{user_voice}
"""
        out_filepath.write_text(page, encoding='utf-8')
        created += 1

    print(f"[Notion] Created: {created} source pages")
    return created


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    kb_root = Path(os.path.expanduser('~/selfOS'))
    output_dir = kb_root / 'wiki' / 'sources'

    # Count existing source pages (preserved, not deleted)
    existing_files = list(output_dir.glob('*.md'))
    print(f"Preserving {len(existing_files)} existing source pages (skip if filename collision)")
    print()

    total = 0

    # 1. Notion notes
    notion_dir = kb_root / 'raw' / 'notion-notes'
    if notion_dir.exists():
        total += extract_notion(notion_dir, output_dir)
    print()

    # 2. Claude conversations
    claude_dir = kb_root / 'raw' / 'claude-conversations'
    if claude_dir.exists():
        total += extract_claude(claude_dir, output_dir)
    print()

    # 3. Gemini conversations
    gemini_dir = kb_root / 'raw' / 'gemini-conversations'
    if gemini_dir.exists():
        total += extract_gemini(gemini_dir, output_dir)
    print()

    print(f"=== Total: {total} source pages ===")
