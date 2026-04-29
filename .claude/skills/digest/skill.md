---
name: digest
description: "Use when user wants to review recent wiki activity or get a recommended question. Triggers: /digest, wiki recap, 回顾, what changed, wiki 最近怎样了."
user-invocable: true
---

# /digest — Wiki Activity Digest

Review what changed in your wiki and get a recommended question to deepen your knowledge base.

## Wiki Root

**Always resolve to `~/selfOS/` (absolute: `/Users/sum_young/selfOS/`).** All paths (`wiki/`, `docs/`) are relative to this root. If CWD is not selfOS, use absolute paths.

## When to Use

- User says `/digest`, `/digest week`, or `/digest question`
- User wants to see wiki activity or get a daily prompt

**Not for:** querying wiki content (`/wiki query`), active interview (`/interview`), thought capture (`/thought`)

## Commands

| Command | What it does |
|---------|-------------|
| `/digest` | Today's wiki changes + 1 recommended question |
| `/digest week` | This week's changes + top 3 active concepts + 2-3 questions |
| `/digest question` | Just a recommended question, no recap |

## Daily Digest Flow

### 1. Gather changes

Run these commands to collect today's wiki activity:

```bash
# Git changes in wiki/ today
git log --since="midnight" --name-status --pretty=format:"%h %s" -- wiki/

# If no changes today, fall back to last 3 days
git log --since="3 days ago" --name-status --pretty=format:"%h %s" -- wiki/
```

Also read the last 10 entries from `wiki/log.md`.

### 2. Categorize changes

Group into:
- **New pages**: files with status `A` (added)
- **Updated pages**: files with status `M` (modified)
- **New connections**: grep added lines for `[[` wikilinks in modified files

For each changed file, read its frontmatter to get title and type.

### 2.5. Gather completed tasks

Read the current month's archive: `wiki/tasks/archive/YYYY-MM.md`

Filter for items completed within the digest period:
- Daily: items with `✓` date == today
- Weekly: items with `✓` date within the last 7 days

If any completed items found, include a section in the output after the changes summary. If no tasks completed in the period, omit this section entirely — do not show "本期完成 (0)".

### 3. Pick a recommended question

Run: `python3 scripts/interview-questions.py`

Pick the highest-priority question. If there are `pending_questions` type entries (priority 0), prefer those — they connect to the user's recent thinking.

Frame the question with reference to today's changes when possible:
- GOOD: "你今天写了关于 X 的想法，wiki 里 [[concepts/Y]] 有个相关的 open question：..."
- BAD: "这是一个推荐问题：..."

### 4. Present

```markdown
### 📊 Wiki 动态 (YYYY-MM-DD)

**新增 (N)**
- [[sources/thought-2026-04-09-xxx]] — 快速想法
- [[concepts/xxx]] — 新概念

**更新 (N)**
- [[concepts/ai4ai]] — 新增 Context Recovery 段落

**新建连接**
- [[concepts/taste与ambition]] ↔ [[concepts/科研路线选择]]

**本期完成 (N)**
- ✅ [T001] xxx (M/D)
- ✅ [R003] yyy (M/D)

---

**推荐问题**
> [基于 context 的具体问题]
```

### 5. Transition to interview

If user answers the recommended question, switch to interview mode:
- Absorb the answer silently (update relevant wiki pages)
- Follow up naturally if the answer opens a thread
- After 1-2 follow-ups, close or ask "还要再来一个问题吗？"

## Weekly Digest Flow

Same as daily, but:
- `git log --since="1 week ago"` for changes
- Add **Top 3 active concepts** (most frequently modified/referenced this week)
- Add **Timeline coverage** change ("本周新覆盖了 2025-10 的 N 条记录")
- 2-3 recommended questions instead of 1

## Common Mistakes

- Showing raw git diff output instead of human-readable summaries
- Recommending a question with no connection to recent activity
- Not reading the changed files to understand what actually changed (just showing filenames is lazy)
