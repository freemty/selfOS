# selfOS Todo System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dual-track todo stack to selfOS with wiki-native storage, CLI skill, daily planning ritual, and monthly archive.

**Architecture:** Two markdown files (`wiki/tasks/do.md`, `wiki/tasks/read.md`) as active stacks, a `/todo` CLI skill for all operations, monthly archive files under `wiki/tasks/archive/`. The skill reads/writes markdown directly using Read/Edit tools — no scripts or external dependencies.

**Tech Stack:** Markdown (YAML frontmatter), Claude Code skill (skill.md), existing selfOS wiki conventions.

**Spec:** `docs/superpowers/specs/2026-04-28-todo-system-design.md`

---

## File Map

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `wiki/tasks/do.md` | Active "do" stack with Today/Pool sections |
| Create | `wiki/tasks/read.md` | Active "read" stack with Today/Pool sections |
| Create | `wiki/tasks/archive/.gitkeep` | Ensure archive directory exists in git |
| Create | `.claude/skills/todo/skill.md` | Main skill file — all `/todo` command logic |
| Modify | `wiki/index.md` | Add `## Tasks` section after Synthesis |
| Modify | `.claude/skills/digest/skill.md` | Add archive reading for "completed" summary |
| Modify | `CLAUDE.md` | Add `/todo` commands to quick commands table |

---

### Task 1: Create Wiki Data Files

**Files:**
- Create: `wiki/tasks/do.md`
- Create: `wiki/tasks/read.md`
- Create: `wiki/tasks/archive/.gitkeep`

- [ ] **Step 1: Create the tasks directory and archive subdirectory**

```bash
mkdir -p ~/selfOS/wiki/tasks/archive
```

- [ ] **Step 2: Create `wiki/tasks/do.md`**

```markdown
---
title: "Do Stack"
type: tasks
updated: 2026-04-28
next_id: 1
---

## Today

## Pool
```

- [ ] **Step 3: Create `wiki/tasks/read.md`**

```markdown
---
title: "Read Stack"
type: tasks
updated: 2026-04-28
next_id: 1
---

## Today

## Pool
```

- [ ] **Step 4: Create `wiki/tasks/archive/.gitkeep`**

Empty file to ensure git tracks the directory.

- [ ] **Step 5: Verify files exist and have correct frontmatter**

```bash
head -10 ~/selfOS/wiki/tasks/do.md
head -10 ~/selfOS/wiki/tasks/read.md
ls ~/selfOS/wiki/tasks/archive/.gitkeep
```

Expected: both files show YAML frontmatter with `next_id: 1`, `.gitkeep` exists.

- [ ] **Step 6: Commit**

```bash
git add wiki/tasks/do.md wiki/tasks/read.md wiki/tasks/archive/.gitkeep
git commit -m "feat(wiki): add todo stack data files — do.md + read.md + archive dir"
```

---

### Task 2: Create the `/todo` Skill

**Files:**
- Create: `.claude/skills/todo/skill.md`

This is the core deliverable. The skill file follows the same pattern as `.claude/skills/thought/skill.md` and `.claude/skills/digest/skill.md` — a single `skill.md` with frontmatter, dispatch logic, and per-command workflows.

- [ ] **Step 1: Create `.claude/skills/todo/skill.md`**

```markdown
---
name: todo
description: "Use when user wants to manage daily tasks or reading backlog. Triggers: /todo, todo add, todo list, todo today, todo done, 待办, 今天做什么. Args: subcommand + arguments."
user-invocable: true
---

# /todo — Daily Task Stack

Dual-track todo system: **do** (actions) and **read** (things to absorb). Daily planning ritual with auto-rollover.

## Wiki Root

**Always resolve to `~/selfOS/` (absolute: `~/selfOS/`).** All paths (`wiki/tasks/`) are relative to this root.

## When to Use

- User says `/todo` or any subcommand
- User wants to add, complete, or review daily tasks
- User asks "今天做什么" or mentions 待办

**Not for:** project-level roadmap (use `TODO.md`), capturing thoughts (`/thought`), ingesting sources (`/wiki ingest`)

## Data Files

- `wiki/tasks/do.md` — action items (ID prefix: `T`)
- `wiki/tasks/read.md` — reading/absorption items (ID prefix: `R`)
- `wiki/tasks/archive/YYYY-MM.md` — monthly completed items

## Item Format

```
- [<ID>] <描述> @<YYYY-MM-DD> #<tag>
```

- ID: `T` or `R` + zero-padded 3-digit number (T001, R042)
- `@date` = date added
- `#tag` = optional (e.g. #research, #admin, #paper, #blog, #project)

## Commands

### `/todo add do|read "<描述>" [#tag]`

1. Determine track: `do` → `wiki/tasks/do.md` (prefix `T`), `read` → `wiki/tasks/read.md` (prefix `R`)
2. Read the file, parse frontmatter `next_id`
3. Generate ID: prefix + zero-padded `next_id` to 3 digits
4. Append item to `## Pool` section (at the bottom, before any blank trailing line)
5. Increment `next_id` in frontmatter by 1
6. Update `updated` date in frontmatter to today
7. Confirm:

```
✅ [T003] 回复导师邮件 @2026-04-28 #admin → Pool
```

If user provides multiple items separated by newlines or commas, process each one sequentially.

### `/todo today`

Daily planning ritual — "每天三件事"

1. **Auto-bump**: Read both `do.md` and `read.md`. For each file, check frontmatter `updated` date:
   - If `updated` < today AND `## Today` section has items → move ALL Today items to the TOP of `## Pool` (preserving order). These are yesterday's unfinished items rolling over.
   - If `updated` == today → Today section is current, no bump needed.
2. **Display**: Show both stacks in a clean format:

```
### 📋 Do Stack
**Pool (N items)**
- [T001] xxx @2026-04-25 #research
- [T002] yyy @2026-04-26 #admin
...

### 📖 Read Stack
**Pool (N items)**
- [R001] xxx @2026-04-25 #paper
- [R002] yyy @2026-04-26 #blog
...

---
今天挑哪几件？（输入 ID，如 `T001 R002 T003`）
```

3. **Wait for user response** with IDs
4. **Move** selected items from `## Pool` to `## Today` in their respective files
5. **Update** `updated` date in frontmatter to today for both files
6. **Confirm**:

```
### 🎯 今日计划
**Do:** [T001] xxx, [T003] yyy
**Read:** [R002] zzz
```

### `/todo done <ID> [<ID2> ...]`

1. Determine file from ID prefix: `T` → `do.md`, `R` → `read.md`
2. Read the file, find the item line (search both `## Today` and `## Pool`)
3. Remove the item line from the file
4. Append to `wiki/tasks/archive/YYYY-MM.md` (current month):
   - If file doesn't exist, create it with frontmatter:
   ```yaml
   ---
   title: "Archive YYYY-MM"
   type: tasks-archive
   updated: YYYY-MM-DD
   ---

   ## Completed
   ```
   - Append: `- [ID] 描述 @added-date ✓YYYY-MM-DD #tag`
   - Update archive frontmatter `updated` date
5. Append to `wiki/log.md`:
   ```
   - YYYY-MM-DD | done | [ID] 描述
   ```
6. Update source file frontmatter `updated` date
7. **If ID starts with `R`** (read track), ask: 「要 `/wiki ingest` 吗？」
   - If user says yes/要 → tell them to run `/wiki ingest` with the relevant URL or content
   - If user says no/不用 → skip
8. Confirm:

```
✅ [T001] 写 GPU systems 补课笔记 → Archive (2026-04)
```

Support multiple IDs in one call: `/todo done T001 R002`

### `/todo list`

1. Read both `do.md` and `read.md`
2. Display:

```
### 📋 Do Stack
**Today (N)**
- [T001] xxx @2026-04-28 #research
**Pool (N)**
- [T002] yyy @2026-04-25 #admin

### 📖 Read Stack
**Today (N)**
- [R001] xxx @2026-04-28 #paper
**Pool (N)**
- [R002] yyy @2026-04-26 #blog
```

If both Today sections are empty, note: "还没做今天的计划，试试 `/todo today`"

### `/todo list archive [YYYY-MM]`

1. If month specified, read `wiki/tasks/archive/YYYY-MM.md`
2. If no month specified, read current month's archive
3. If file doesn't exist, say "这个月还没有完成的 items"
4. Display the completed items list

### `/todo bump`

Manual trigger for the auto-bump logic (same as step 1 of `/todo today`).

1. Read both files, move any Today items to top of Pool
2. Update `updated` dates
3. Report what was bumped

Usually not needed manually — `/todo today` auto-bumps.

## Common Mistakes

- Forgetting to increment `next_id` after adding an item
- Not updating `updated` date in frontmatter (breaks bump detection)
- Writing to `wiki/log.md` on add/today (only done triggers log)
- Mixing up T/R prefixes when determining which file to read
- Creating archive file without proper frontmatter
```

- [ ] **Step 2: Verify skill file is well-formed**

```bash
head -5 ~/selfOS/.claude/skills/todo/skill.md
wc -l ~/selfOS/.claude/skills/todo/skill.md
```

Expected: frontmatter starts with `---`, file is roughly 130-160 lines.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/todo/skill.md
git commit -m "feat(skill): add /todo skill — dual-track daily task stack"
```

---

### Task 3: Integrate with wiki/index.md

**Files:**
- Modify: `wiki/index.md` (after the `## Synthesis` section, before EOF)

- [ ] **Step 1: Read the end of wiki/index.md to find insertion point**

Read `wiki/index.md` — the `## Synthesis` section is the last section. Add `## Tasks` after it.

- [ ] **Step 2: Append Tasks section to wiki/index.md**

Using the Edit tool, add after the last synthesis entry:

```markdown

## Tasks

- [[tasks/do|Do Stack]] — 行动待办
- [[tasks/read|Read Stack]] — 吸收待办
- [[tasks/archive/|Archive]] — 月度归档
```

- [ ] **Step 3: Update index.md frontmatter summary**

Update the `summary` field to mention tasks.

- [ ] **Step 4: Verify the section appears correctly**

```bash
tail -15 ~/selfOS/wiki/index.md
```

Expected: `## Tasks` section visible with three wikilinks.

- [ ] **Step 5: Commit**

```bash
git add wiki/index.md
git commit -m "feat(wiki): add Tasks section to index.md"
```

---

### Task 4: Integrate with digest skill

**Files:**
- Modify: `.claude/skills/digest/skill.md`

- [ ] **Step 1: Read the current digest skill**

Read `.claude/skills/digest/skill.md` fully.

- [ ] **Step 2: Add archive reading to the digest flow**

In the "Daily Digest Flow" section, after step 2 ("Categorize changes") and before step 3 ("Pick a recommended question"), add a new step:

```markdown
### 2.5. Gather completed tasks

Read the current month's archive: `wiki/tasks/archive/YYYY-MM.md`

Filter for items completed within the digest period:
- Daily: items with `✓` date == today
- Weekly: items with `✓` date within the last 7 days

If any completed items found, include a section in the output after the changes summary:

**本期完成**
- ✅ [T001] 写 GPU systems 补课笔记 (4/28)
- ✅ [R003] Erta 论文 (4/27)
```

- [ ] **Step 3: Add the "本期完成" section to the presentation template**

In step 4 ("Present"), add after the "新建连接" block:

```markdown
**本期完成 (N)**
- ✅ [T001] xxx (M/D)
- ✅ [R003] yyy (M/D)
```

If no tasks completed in the period, omit this section entirely (don't show "本期完成 (0)").

- [ ] **Step 4: Verify the skill file is still well-formed**

```bash
head -5 ~/selfOS/.claude/skills/digest/skill.md
grep -n "completed\|archive\|本期完成" ~/selfOS/.claude/skills/digest/skill.md
```

Expected: frontmatter intact, new sections present.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/digest/skill.md
git commit -m "feat(skill): add task completion summary to /digest"
```

---

### Task 5: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md` (add `/todo` to the quick commands table)

- [ ] **Step 1: Read the quick commands section of CLAUDE.md**

Find the "Quick commands" or "Wiki Operations" table in `CLAUDE.md`.

- [ ] **Step 2: Add /todo commands to the table**

After the existing Wiki Operations table, add a new subsection:

```markdown
### Todo Stack

| Command | Purpose | Example |
|---------|---------|---------|
| `/todo add do "描述"` | 加行动到 do pool | `/todo add do "回复邮件" #admin` |
| `/todo add read "描述"` | 加阅读到 read pool | `/todo add read "Erta 论文" #paper` |
| `/todo today` | 日计划仪式：从池子里挑今天的 items | `/todo today` |
| `/todo done <id>` | 标记完成，归档 | `/todo done T001` |
| `/todo list` | 查看当前 Today + Pool | `/todo list` |
| `/todo list archive` | 查看月度归档 | `/todo list archive 2026-03` |
```

Also update the user mental model line to include `/todo`:

```
用户心智模型：`/thought` 记想法 → `/todo` 管行动 → `/interview` 让 wiki 问我 → `/digest` 回顾变化 → `/wiki` 管理
```

- [ ] **Step 3: Verify CLAUDE.md changes**

```bash
grep -A 8 "Todo Stack" ~/selfOS/CLAUDE.md
grep "todo" ~/selfOS/CLAUDE.md
```

Expected: new table visible, mental model line updated.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add /todo commands to CLAUDE.md quick reference"
```

---

### Task 6: Smoke Test

No code to write — this is a manual verification task.

- [ ] **Step 1: Test `/todo add`**

Run `/todo add do "测试任务一" #test` and verify:
- Item appears in `wiki/tasks/do.md` under `## Pool`
- ID is `T001`
- `next_id` in frontmatter is now `2`
- `updated` date is today

- [ ] **Step 2: Test `/todo add read`**

Run `/todo add read "测试论文" #paper` and verify:
- Item appears in `wiki/tasks/read.md` under `## Pool`
- ID is `R001`

- [ ] **Step 3: Test `/todo today`**

Run `/todo today` and verify:
- Both pools are displayed
- Pick T001 and R001
- Items move to `## Today` sections

- [ ] **Step 4: Test `/todo done`**

Run `/todo done T001` and verify:
- Item removed from `do.md`
- Item appears in `wiki/tasks/archive/2026-04.md` with `✓2026-04-28`
- Entry appended to `wiki/log.md`

- [ ] **Step 5: Test `/todo list`**

Run `/todo list` and verify:
- Shows remaining items (R001 in Today, do stack empty)

- [ ] **Step 6: Clean up test data**

Remove test items from do.md, read.md, archive, and log.md. Reset `next_id` to 1 in both files.

- [ ] **Step 7: Commit clean state**

```bash
git add wiki/tasks/ wiki/log.md
git commit -m "chore: smoke test todo system — verified and cleaned up"
```

---

### Task 7: Create Symlink (if needed)

**Files:**
- Create: symlink at `~/.claude/skills/todo` → `~/selfOS/.claude/skills/todo`

- [ ] **Step 1: Check if project-level skills are auto-loaded**

The skill lives at `.claude/skills/todo/skill.md` inside the selfOS project. When CWD is selfOS, project-level skills are loaded automatically. A global symlink is only needed if `/todo` should work from other directories.

Check existing symlinks:

```bash
ls -la ~/.claude/skills/ | grep selfOS
```

- [ ] **Step 2: Create symlink if other selfOS skills have global symlinks**

If other selfOS skills (thought, digest, selfos-completion) have global symlinks, create one for todo too:

```bash
ln -s ~/selfOS/.claude/skills/todo ~/.claude/skills/todo
```

- [ ] **Step 3: Verify symlink resolves**

```bash
ls -la ~/.claude/skills/todo/skill.md
```

Expected: file is readable via the symlink path.
