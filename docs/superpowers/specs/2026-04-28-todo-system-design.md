# selfOS Todo System Design

Date: 2026-04-28

## Overview

为 selfOS 添加双轨 todo 堆栈，管理每日「要做的事」和「要吸收的东西」。Wiki 原生存储 + CLI skill 操作，日计划仪式（每天三件事），未完成自动顺延，月度归档可回看。

## Design Decisions

- **双轨制**：do（行动）和 read（吸收）是两个独立列表，各有各的节奏
- **wiki 原生存储**：文件住在 `wiki/tasks/`，Obsidian 直接可见可编辑
- **CLI skill 入口**：所有操作通过 `/todo` 命令完成，不依赖外部系统
- **日计划仪式**：每天早上 `/todo today` 从池子里挑 items，未完成的自动顺延
- **分层吸收**：read item 完成后自主决定是否 `/wiki ingest`，todo 系统不替用户判断
- **独立归档**：按月归档，可回看历史

## Data Structure

### Directory

```
wiki/tasks/
├── do.md              # 活跃「做」堆栈
├── read.md            # 活跃「读」堆栈
└── archive/
    └── 2026-04.md     # 月度归档
```

### Active Stack Format (`do.md` / `read.md`)

```yaml
---
title: "Do Stack"           # or "Read Stack"
type: tasks
updated: 2026-04-28
next_id: 5                  # 下一个可用 ID 数字部分，避免归档后 ID 碰撞
---
```

```markdown
## Today
- [T001] 写 GPU systems 补课笔记 @2026-04-28 #research
- [T003] 回复导师邮件 @2026-04-27 #admin

## Pool
- [T002] 整理 selfOS public repo demo @2026-04-25 #project
- [T004] 看完 vLLM 源码 scheduler 部分 @2026-04-26 #research
```

### Item Format

```
- [<ID>] <描述> @<添加日期> #<可选tag>
```

- ID 前缀：`T` = do, `R` = read，三位数自增（T001, R042）
- `@YYYY-MM-DD` = 添加日期
- `#tag` = 可选标签（#research, #admin, #paper, #blog, #talk, #project 等）
- `## Today` = 今日选中的 items
- `## Pool` = 待办池

### Archive Format (`archive/YYYY-MM.md`)

```yaml
---
title: "Archive 2026-04"
type: tasks-archive
updated: 2026-04-28
---
```

```markdown
## Completed
- [T001] 写 GPU systems 补课笔记 @2026-04-28 ✓2026-04-28 #research
- [R005] Erta 论文 @2026-04-20 ✓2026-04-25 #paper
```

`✓YYYY-MM-DD` = 完成日期，归档时自动追加。

## Skill Commands

Skill 名称：`todo`，位于 `.claude/skills/todo/`

| 命令 | 用途 | 示例 |
|------|------|------|
| `/todo add do "描述"` | 加一条到 do pool | `/todo add do "回复导师邮件" #admin` |
| `/todo add read "描述"` | 加一条到 read pool | `/todo add read "Erta 论文" #paper` |
| `/todo today` | 日计划仪式 | `/todo today` |
| `/todo done <id>` | 标记完成，移到月度归档 | `/todo done T001` |
| `/todo list` | 展示当前 Today + Pool | `/todo list` |
| `/todo list archive` | 查看归档历史（默认本月） | `/todo list archive 2026-03` |
| `/todo bump` | 日切：Today 未完成退回 Pool 顶部 | 自动触发，一般不手动调 |

### `/todo today` Flow

1. **Auto-bump**：检查 do.md 和 read.md 的 frontmatter `updated` 日期。如果 `updated` < 今天，说明 Today 区是昨天的残留，把所有 Today items 退回 `## Pool` 顶部
2. **展示**：列出两个池子的完整内容（Today 已清空 + Pool 全部）
3. **提问**：「今天挑哪几件？」
4. **选择**：用户回复 ID（如 `T002 R001 R003`），移到对应文件的 `## Today`
5. **更新** frontmatter `updated` 日期

### `/todo done <id>` Flow

1. 从 Today 或 Pool 中移除该 item
2. 追加 `✓完成日期` 写入 `wiki/tasks/archive/YYYY-MM.md`（不存在则创建）
3. 如果是 R 前缀（read 轨），提示：「要 `/wiki ingest` 吗？」——用户拒绝则跳过
4. 追加一行到 `wiki/log.md`
5. 更新 frontmatter `updated` 日期

### `/todo add` Flow

1. 读取对应文件（do.md 或 read.md），取 frontmatter `next_id`
2. 生成 ID（T/R + 三位数零填充），`next_id` 自增 1
3. 追加到 `## Pool` 底部
4. 更新 frontmatter `updated` 日期

## Integration

### wiki/index.md

新增 `## Tasks` 分区（放在 Synthesis 之后）：

```markdown
## Tasks

- [[tasks/do|Do Stack]] — 行动待办
- [[tasks/read|Read Stack]] — 吸收待办
- [[tasks/archive/|Archive]] — 月度归档
```

### wiki/log.md

`/todo done` 完成 item 时追加一行：

```markdown
- 2026-04-28 | done | [T001] 写 GPU systems 补课笔记
```

`/todo add` 和 `/todo today` 不写 log。

### `/digest` 联动

digest skill 展示回顾时，额外读取当月 archive 文件，在回顾末尾追加「本期完成」小结。不改 digest 主流程。

### 不联动

- `/thought`：捕捉想法 ≠ 管理行动，职责不同
- `TODO.md`：项目级长期 roadmap，和每日堆栈是不同层次
- Notion：不同步，输入全在 CC 完成

### Obsidian

`wiki/tasks/` 下的文件是普通 markdown，Obsidian 直接可见可编辑。Graph View 中会自然出现。Dataview 可选用但不依赖。

## Out of Scope

- 自动优先级排序 / 推荐
- 外部系统同步（Notion, Calendar）
- 每条 item 独立 wiki page
- 周期性/重复 task
- 依赖关系追踪
