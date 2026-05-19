---
name: digest
description: "Read-only wiki activity recap — what changed, stats, completed tasks. Triggers: /digest, wiki recap, 回顾, what changed, wiki 最近怎样了."
user-invocable: true
---

# /digest — Wiki Activity Digest

Review what changed in your wiki. Pure recap — no questions (use `/interview` for that).

## Wiki Root

**Always resolve to `~/selfOS/` (absolute: `/Users/sum_young/selfOS/`).** All paths (`wiki/`, `docs/`) are relative to this root. If CWD is not selfOS, use absolute paths.

## When to Use

- User says `/digest` or `/digest week`
- User wants to see wiki activity or completed tasks

**Not for:** querying wiki content (`/wiki query`), active interview (`/interview`), thought capture (`/thought`)

## Commands

| Command | What it does |
|---------|-------------|
| `/digest` | Today's wiki changes + completed tasks |
| `/digest week` | This week's changes + top 3 active concepts |

## Daily Digest Flow

### 1. Gather changes

```bash
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

### 3. Gather completed tasks

Read the current month's archive: `wiki/tasks/archive/YYYY-MM.md`

Filter for items completed within the digest period:
- Daily: items with `✓` date == today
- Weekly: items with `✓` date within the last 7 days

If no tasks completed in the period, omit this section.

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
```

## Weekly Digest Flow

Same as daily, but:
- `git log --since="1 week ago"` for changes
- Add **Top 3 active concepts** (most frequently modified/referenced this week)
- Add **Timeline coverage** change ("本周新覆盖了 2025-10 的 N 条记录")

## Common Mistakes

- Showing raw git diff output instead of human-readable summaries
- Not reading the changed files to understand what actually changed (just showing filenames is lazy)
