---
name: thought
description: "Use when user wants to jot down a fleeting idea or one-liner thought. Triggers: /thought, 记一个想法, jot down, 记个想法. Args: the thought text (inline or prompted)."
user-invocable: true
---

# /thought — Quick Thought Capture + Interview

One command: write a thought into the wiki, then interview to recover context. Replaces the Notion → raw → compile → /complete pipeline.

## Wiki Root

**Always resolve to `~/selfOS/` (absolute: `/Users/sum_young/selfOS/`).** All paths (`wiki/`, `docs/`) are relative to this root. If CWD is not selfOS, use absolute paths.

## When to Use

- User says `/thought <text>` or "记一个想法"
- User wants to jot down a fleeting idea and immediately flesh it out

**Not for:** ingesting external sources (`/wiki ingest`), reviewing old thoughts (`/complete`), querying wiki (`/wiki query`)

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

Append the new page to `wiki/index.md` under the Sources section (Thoughts subsection if it exists).

### 3. Interview (immediate)

Present the thought back and ask ONE question at a time (not all three at once):

```
### 💭 已记录

> **YYYY-MM-DD**
> <thought text>

**当时的背景是什么？** 发生了什么让你写下这个？
```

After user responds, follow up naturally:
- "怎么展开？"
- "和你现在做的哪些事/概念相关？"

Keep it conversational — 2-3 rounds max unless user wants to go deeper.

### 4. Writeback

After interview, append to the same source file:

```markdown
## Context Recovery (YYYY-MM-DD)

**背景：** ...
**展开：** ...
**关联概念：** [[concept-1]], [[concept-2]]
```

### 5. Cross-link

- Check `wiki/index.md` for related concepts/entities
- Update related wiki pages if the thought adds meaningful context
- Create new concept pages only if the thought introduces a genuinely new idea

### 6. Log

Append to `docs/bookmark-chat-log.jsonl`:

```json
{"id": "thought-YYYY-MM-DD-<slug>", "type": "thought", "date": "YYYY-MM-DD", "tags": [...], "summary": "..."}
```

### 7. Log to wiki/log.md

Append operation record.

## Special Cases

- **User says "跳过" after capture**: Log with `{"skipped": true}`, skip interview. The thought is still saved.
- **Multiple thoughts in one message**: Process one at a time, interview each before moving to next.
- **Thought is actually a long paragraph**: Still save as-is, but the interview can be lighter (context is already rich).

## Common Mistakes

- Asking all interview questions at once instead of one-by-one conversational flow
- Forgetting to update `wiki/index.md`
- Not checking existing concepts for cross-links before creating new ones
- Creating a concept page for every thought — only create if genuinely new
