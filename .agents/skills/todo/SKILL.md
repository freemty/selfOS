---
name: todo
description: "Use when user wants to manage daily tasks or reading backlog. Triggers: /todo, todo add, todo list, todo today, todo done, 待办, 今天做什么. Args: subcommand + arguments."
user-invocable: true
---

# /todo — Daily Task Stack

Dual-track todo system: **do** (actions) and **read** (things to absorb). Daily planning ritual with auto-rollover.

## Wiki Root

**Resolve the wiki root by finding the current repository folder containing `CLAUDE.md` or `AGENTS.md` with the `<!-- llm-wiki -->` marker. If invoked outside the repo, use the installed selfOS path or ask for it.** All paths (`wiki/tasks/`) are relative to this root.

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

**For each command:** read the corresponding `references/` file for the full step-by-step workflow before executing.

| Command | Summary | Full workflow |
|---------|---------|---------------|
| `/todo add do\|read "<描述>"` | Add item to pool | Read `references/add-workflow.md` |
| `/todo today` | Daily planning ritual | Read `references/today-workflow.md` |
| `/todo done <ID>` | Complete & archive | Read `references/done-workflow.md` |
| `/todo list` | Show current stacks | Direct (see below) |
| `/todo list archive [YYYY-MM]` | View archive | Direct (see below) |
| `/todo bump` | Manual day-switch | Same as today step 1 |

### `/todo list`

1. Read both `do.md` and `read.md`
2. Display every task section present in the files, preserving section order.
   - Do Stack currently uses: `Today`, `Pending`, `Pool`
   - Read Stack currently uses: `Today`, `Completed`, `Abandoned`, `Pool`
   - If a section is empty, omit it unless all active sections are empty.
   - Treat `Pending` as waiting/on-hold, `Abandoned` as intentionally dropped, and `Completed` as reference-only.
3. Use this output shape:

```
### 📋 Do Stack
**Today (N)**
- [T001] xxx @2026-04-28 #research
**Pending (N)**
- [T003] zzz @2026-04-29 #project
**Pool (N)**
- [T002] yyy @2026-04-25 #admin

### 📖 Read Stack
**Today (N)**
- [R001] xxx @2026-04-28 #paper
**Completed (N)**
- [R003] done item @2026-04-29
**Abandoned (N)**
- [R004] dropped item @2026-04-29
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
