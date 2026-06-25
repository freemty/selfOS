# /todo done — Completion & Archive Workflow Reference

## Syntax

```
/todo done <ID> [<ID2> ...]
```

## Steps

### 1. Parse IDs & Determine Files

- `T` prefix → `wiki/tasks/do.md`
- `R` prefix → `wiki/tasks/read.md`
- Multiple IDs: group by file to minimize reads

### 2. Find & Remove Item Lines

Read each target file **once** (not per-ID). For all IDs grouped to that file:
1. Search all task sections for item lines matching each `[<ID>]`
   - do.md sections: `Today`, `Pending`, `Pool`
   - read.md sections: `Today`, `Completed`, `Abandoned`, `Pool`
2. Remove all matched lines in one edit
3. If any ID not found, report error and skip that ID
4. Write the file back once with all removals applied

### 3. Write to Archive + Log + Frontmatter (parallel)

Steps 3, 4, 5 below are independent writes — execute them in parallel.

**3a. Archive:**

Target: `wiki/tasks/archive/YYYY-MM.md` (current month)

**If file doesn't exist**, create with:
```yaml
---
title: "Archive YYYY-MM"
type: tasks-archive
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## Completed
```

**Append** each completed item:
```
- [T001] 写 GPU systems 补课笔记 @2026-04-28 ✓2026-04-29 #research
```

Format: original item line + ` ✓YYYY-MM-DD` (today's date) inserted before the `#tag`.

Update archive frontmatter `updated` date.

**3b. Log** — append one line per completed item to `wiki/log.md`:
```
- 2026-04-29 | done | [T001] 写 GPU systems 补课笔记
```

**3c. Frontmatter** — for each modified file (do.md / read.md): `updated` = today

### 6. R-Item Ingest Prompt（批量模式）

If ANY completed IDs start with `R`:
- Collect all completed R-items
- Ask **once** (not per item):

```
这几个读完的要 ingest 吗？
- [R002] Erta 论文
- [R003] 刘子鸣 blog

（回复「要」+ URL/内容，或「不用」跳过）
```

- If user says yes → guide them to run `/wiki ingest`
- If user says no → skip

### 7. Confirm

Single item:
```
✅ [T001] 写 GPU systems 补课笔记 → Archive (2026-04)
```

Multiple items:
```
✅ 已归档 3 项到 2026-04:
- [T001] 写 GPU systems 补课笔记
- [R002] Erta 论文
- [R003] 刘子鸣 blog
```

## Edge Cases

- **ID 不存在**：报错「[T999] 不存在，跳过」，继续处理其他 ID
- **同一 ID 出现两次**：只处理一次
- **Archive 文件已有同 ID**：理论上不应发生（ID 全局唯一），但如果发生，仍然追加（保留重复记录比丢失记录好）
- **do.md 和 read.md 同时被修改**（如 `/todo done T001 R002`）：分别读写两个文件，注意不要把 T 的修改写进 R 的文件
