---
name: thought
description: "Capture a fleeting idea into wiki — pure write, no interview. Triggers: /thought, 记一个想法, jot down, 记个想法. Args: the thought text (inline or prompted)."
user-invocable: true
---

# /thought — Quick Thought Capture

One command: write a thought into the wiki as a source page. Pure capture — no interview (use `/interview thought` to follow up).

## Wiki Root

**Always resolve to `~/selfOS/` (absolute: `/Users/<username>/selfOS/`).** All paths (`wiki/`, `docs/`) are relative to this root. If CWD is not selfOS, use absolute paths.

## When to Use

- User says `/thought <text>` or "记一个想法"
- User wants to jot down a fleeting idea quickly

**Not for:** ingesting external sources (`/wiki ingest`), reviewing old thoughts (`/complete`), querying wiki (`/wiki query`), following up on thoughts (`/interview`)

## Flow

### 1. Capture

Parse the thought text from args or ask the user if empty.

Create `wiki/sources/thought-YYYY-MM-DD-<slug>.md`:

```yaml
---
title: "<thought text, truncated to 60 chars>"
type: source
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
tags: [Thoughts]
summary: "<thought text>"
source_type: "thought"
---
```

Body:

```markdown
# <thought text>

<thought text>
```

Slug rules: lowercase, CJK kept as-is, spaces → `-`, max 80 chars, no special chars.

### 2. Index

Append the new page to `wiki/index.md` under the Sources section.

### 3. Cross-link

- Check `wiki/index.md` for related concepts/entities
- Update related wiki pages if the thought adds meaningful context
- Create new concept pages only if the thought introduces a genuinely new idea

### 4. Log

Append to `docs/bookmark-chat-log.jsonl`:

```json
{"id": "thought-YYYY-MM-DD-<slug>", "type": "thought", "date": "YYYY-MM-DD", "tags": [...], "summary": "..."}
```

### 5. Log to wiki/log.md

Append operation record.

### 6. Present + Offer Interview

```
### 💭 已记录

> **YYYY-MM-DD**
> <thought text>

输入 `/interview thought` 可以追问展开。
```

## Special Cases

- **Multiple thoughts in one message**: Process one at a time.
- **Thought is actually a long paragraph**: Still save as-is.
- **User says "跳过"**: Log with `{"skipped": true}`, done.

## Common Mistakes

- Asking interview questions (that's `/interview`'s job now)
- Forgetting to update `wiki/index.md`
- Not checking existing concepts for cross-links before creating new ones
- Creating a concept page for every thought — only create if genuinely new
