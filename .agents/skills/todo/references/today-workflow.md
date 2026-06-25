# /todo today — Daily Planning Ritual Workflow Reference

## Syntax

```
/todo today
```

## Steps

### 1. Auto-Bump（日切）

Read both `wiki/tasks/do.md` and `wiki/tasks/read.md`. For each file:

- Parse frontmatter `updated` date
- If `updated` < today AND `## Today` has items:
  - Move ALL Today items to the **TOP** of `## Pool`（preserving order）
  - These are yesterday's unfinished items rolling over
- If `updated` == today:
  - Today section is current, no bump needed
- Never move `## Pending`, `## Completed`, or `## Abandoned` items during auto-bump.

**Why top of Pool**: 顺延的 items 应该在池子最上面，因为它们已经被用户选过一次——比新加的 items 优先级更高。

### 2. Display

Show both stacks:

```
### 📋 Do Stack
**Today (N)** ← only show if non-empty (same-day re-run)
- [T005] zzz @2026-04-29 #admin
**Pool (N items)**
- [T001] xxx @2026-04-25 #research
- [T002] yyy @2026-04-26 #admin

### 📖 Read Stack
**Today (N)** ← only show if non-empty
- [R004] www @2026-04-29 #paper
**Pool (N items)**
- [R001] xxx @2026-04-25 #paper
- [R002] yyy @2026-04-26 #blog

---
今天挑哪几件？（输入 ID，如 `T001 R002 T003`）
```

**Empty pool**: 如果两个 Pool 都空，说「Pool 是空的，先用 `/todo add` 加点东西」。

### 3. Wait for User Selection

用户回复 IDs（空格分隔），如 `T001 R002 T003`。

### 4. Move Selected Items

- 从 `## Pool` 中移除选中的 item lines
- 追加到对应文件的 `## Today` section
- T 前缀 items 操作 `do.md`，R 前缀操作 `read.md`

### 5. Update Frontmatter

- Both files: `updated` = today

### 6. Confirm

```
### 🎯 今日计划
**Do:** [T001] xxx, [T003] yyy
**Read:** [R002] zzz
```

## Same-Day Re-Run

如果用户当天再次运行 `/todo today`：
- `updated` == today → 不触发 bump
- Today 区已有内容 → 展示 Today 和 Pool
- 用户可以继续从 Pool 中追加 items 到 Today
- 已在 Today 的 items 不会重复出现在 Pool 中

## Edge Cases

- **用户输入了不存在的 ID**：提示「ID 不存在，请检查」
- **用户输入了已在 Today 的 ID**：忽略并告知「已经在今天的计划中了」
- **Pool 和 Today 都为空**：引导用户先 `/todo add`
