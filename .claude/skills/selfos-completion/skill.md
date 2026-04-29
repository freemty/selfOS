---
name: selfos-completion
description: "Use when recovering latent context from past fragments — terse Notion thoughts missing context, Twitter bookmarks without rationale, or wiki pages with open questions and timeline gaps. Triggers: /bookmark-chat, /complete, /interview, context recovery, fill gaps."
user-invocable: true
---

# selfOS Completion

Recover latent context from past fragments. Three modes, one principle: **LLM presents a key, human restores the value.**

## Wiki Root

**Always resolve wiki root to `~/selfOS/`.** All relative paths below (`wiki/`, `docs/`, `scripts/`) are relative to this root, NOT to the current working directory. If CWD is not selfOS, `cd ~/selfOS` first or use absolute paths.

## When to Use

- User says `/bookmark-chat`, `/complete`, or `/interview`
- Wiki has terse thoughts, unprocessed bookmarks, or context gaps
- User wants to enrich past records with recovered context

**Not for:** ingesting new sources (use `/wiki ingest`), querying wiki (use `/wiki query`)

## Modes

| Command | Pool | What it picks |
|---------|------|---------------|
| `/bookmark-chat` | Twitter bookmarks | Bookmarked tweets missing "why I saved this" |
| `/complete` or `/bookmark-chat thoughts` | Notion Thoughts | One-line thoughts missing context |
| `/interview` | Wiki gaps + pending questions | Pending偏好追问 → Open Questions → Thin pages → Timeline gaps |
| (no args) | Mixed bookmarks + thoughts | Random from either pool |

## Quick Reference

| Item | Detail |
|------|--------|
| State file | `docs/bookmark-chat-log.jsonl` |
| Output | `wiki/synthesis/bookmark-chat-YYYY-MM-DD.md` |
| Thought writeback | Appends `## Context Recovery` to original source page |
| Interview script | `python3 scripts/interview-questions.py` (JSON output) |
| Git commit | After each session |

## Bookmark Mode

### Pick
1. Read `docs/bookmark-chat-log.jsonl` → extract processed IDs
2. `ft list --limit 2096` → all bookmark IDs
3. Exclude processed, random pick one
4. `ft show <id>` → content. If thin, try `xreach tweet <url> --json` or Jina Reader

### Present
```
### 🔖 Bookmark #N (剩余 M 条)

> **@author** · date
> content...

1. **为什么收藏这条？**
2. **和你的哪些兴趣/项目有关？**
3. **你同意/不同意/想补充？**
```

## Thoughts Mode

### Pick
1. Read log → extract processed notion IDs
2. Grep `wiki/sources/notion-*.md` for `source_type: "notion-Thoughts"`
3. Filter to body ≤1 non-empty line
4. Exclude processed, random pick one

### Present
```
### 💭 Thought #N (剩余 M 条)

> **YYYY-MM-DD**
> 一句话...

1. **当时的背景是什么？** 发生了什么让你写下这个？
2. **现在回看，怎么展开？**
3. **和你现在的理解有变化吗？**
```

### Writeback
把还原的 context 追加到原 `wiki/sources/notion-*.md`：
```markdown
## Context Recovery (YYYY-MM-DD)

**背景：** ...
**展开：** ...
**关联概念：** [[concept-1]], [[concept-2]]
```

## Interview Mode

Run `python3 {wiki_root}/scripts/interview-questions.py` → JSON with prioritized gaps:

| Priority | Type | Source |
|----------|------|--------|
| 0 | Pending Questions | Auto-Capture 标记的未展开偏好/判断（`pending_questions` frontmatter） |
| 1 | Stale Concepts | 概念页 `updated` 落后于最新 source 超过 7 天——理解没追上证据 |
| 1 | Open Questions | 概念页底部的 Open Questions |
| 2 | Thin Pages | 概念/实体页 < 100 词 |
| 2 | Vague Entities | 实体页 Mentions 为空或过短 |
| 3 | Timeline Gaps | 月源少于 5 条 |

**Conduct:** Read `references/interview-workflow.md` for full behavioral guide. Key rules:
- One question at a time, conversational tone
- Reference existing wiki content to make questions specific
- **Silently update** relevant wiki pages after each answer
- For `pending_question` type: after absorbing the answer, **remove that question from the source file's `pending_questions` frontmatter list**. If the list becomes empty, remove the `pending_questions` field entirely.
- 3-5 questions per session, then commit

## Shared: Dialogue → Write

After user responds in any mode:

1. **Extract**: preference tags, stance, concept connections
2. **Confirm**: 1-2 sentence summary, user approves
3. **Write synthesis**: append to `wiki/synthesis/bookmark-chat-YYYY-MM-DD.md`
4. **Log**: append to `docs/bookmark-chat-log.jsonl`
   ```json
   {"id": "...", "type": "bookmark|thought|interview", "date": "...", "tags": [...], "summary": "..."}
   ```
5. **Ask**: "还要再来一条吗？"

Special: "跳过" / "没感觉" → log with `{"skipped": true}`, pick next.

## Common Mistakes

- Forgetting to write back to original source page in thoughts mode
- Asking all 3 questions at once instead of letting conversation flow
- Not checking wiki index for related concepts before presenting
- Skipping the log append (breaks dedup on next run)
