---
name: interview
description: "All追问 in one place — recover context from old thoughts, bookmark-chat, wiki gaps, or follow up on a just-captured /thought. Triggers: /interview, /bookmark-chat, /complete, context recovery, fill gaps, 追问."
user-invocable: true
---

# /interview — Unified追问

LLM presents a key, human restores the value. Covers all context-recovery and gap-filling use cases.

## Wiki Root

**Resolve the wiki root by finding the current repository folder containing `CLAUDE.md` or `AGENTS.md` with the `<!-- llm-wiki -->` marker. If invoked outside the repo, use the installed selfOS path or ask for it.** All paths below are relative to this root.

## When to Use

- User says `/interview`, `/bookmark-chat`, `/complete`
- Another skill (e.g. `/thought`, `/digest`) hands off for追问
- Wiki has terse thoughts, unprocessed bookmarks, or context gaps

**Not for:** ingesting new sources (`/wiki ingest`), querying wiki (`/wiki query`), capturing a thought (`/thought`), reviewing activity (`/digest`)

## Modes

| Command | Pool | What it picks |
|---------|------|---------------|
| `/interview` | Wiki gaps + pending questions | Pending偏好追问 → Open Questions → Thin pages → Timeline gaps |
| `/interview thought` | Just-captured thought | Follow up on the most recent `/thought` entry |
| `/bookmark-chat` | Twitter bookmarks | Bookmarked tweets missing "why I saved this" |
| `/complete` | Notion Thoughts | One-line thoughts missing context |
| (no args to /bookmark-chat) | Mixed bookmarks + thoughts | Random from either pool |

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

## Interview Mode (Wiki Gaps)

Run `python3 {wiki_root}/scripts/interview-questions.py` → JSON with prioritized gaps:

| Priority | Type | Source |
|----------|------|--------|
| 0 | Pending Questions | Auto-Capture 标记的未展开偏好/判断（`pending_questions` frontmatter） |
| 1 | Stale Concepts | 概念页 `updated` 落后于最新 source 超过 7 天 |
| 1 | Open Questions | 概念页底部的 Open Questions |
| 2 | Thin Pages | 概念/实体页 < 100 词 |
| 2 | Vague Entities | 实体页 Mentions 为空或过短 |
| 3 | Timeline Gaps | 月源少于 5 条 |

**Conduct:** Read `references/interview-workflow.md` for full behavioral guide. Key rules:
- One question at a time, conversational tone
- Reference existing wiki content to make questions specific
- **Silently update** relevant wiki pages after each answer
- For `pending_question` type: after absorbing the answer, **remove that question from the source file's `pending_questions` frontmatter list**
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
