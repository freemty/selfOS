# /todo add — Workflow Reference

## Syntax

```
/todo add do|read "<描述>" [#tag]
/todo add "<描述>" [#tag]     ← 省略 track 时自动推断
```

## Steps

1. **Determine track**
   - `do` → `wiki/tasks/do.md`，ID 前缀 `T`
   - `read` → `wiki/tasks/read.md`，ID 前缀 `R`
   - 省略时推断：描述含论文/blog/talk/paper/书/播客 → `read`；否则 → `do`，并告知用户

2. **Read file**, parse frontmatter `next_id`

3. **Generate ID**: prefix + zero-padded `next_id` to 3 digits
   - 例：`next_id: 7` + track `do` → `T007`

4. **Construct item line**:
   ```
   - [T007] 回复导师邮件 @2026-04-29 #admin
   ```
   - `@日期` = 今天
   - `#tag` = 用户提供的 tag，可选

5. **Append** to `## Pool` section (at the bottom)

6. **Update frontmatter**:
   - `next_id` += 1
   - `updated` = 今天

7. **Confirm**:
   ```
   ✅ [T007] 回复导师邮件 @2026-04-29 #admin → Pool
   ```

## Batch Add

用户用逗号或换行分隔多个 items 时，逐个处理，每个独立生成 ID。统一确认：

```
✅ 已添加 3 项到 Do Pool:
- [T007] 回复导师邮件 @2026-04-29 #admin
- [T008] 写 weekly report @2026-04-29 #admin
- [T009] 提交 housing form @2026-04-29 #admin
```

## Edge Cases

- **描述为空**：提示用户输入
- **`next_id` 超过 999**：继续自增（T1000 等），不重置
- **文件不存在**：不应发生（初始化时创建），但如果发生，创建并填入标准 frontmatter + 空 Today/Pool
