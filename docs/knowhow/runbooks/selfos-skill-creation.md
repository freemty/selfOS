# selfOS Skill 创建 Runbook

> 从 brainstorm 到上线一个新 selfOS CLI skill 的完整流程（以 /todo 为例）

## Problem

需要给 selfOS 加新功能时，如何系统性地设计、实现、验证一个 Claude Code skill，确保与现有 wiki 体系一致。

## Cause

selfOS skill 是 instruction-driven 的 markdown 文件（不是可执行代码），但设计不当会导致 LLM 执行时出错：漏步骤、状态不一致、与现有系统冲突。需要一套结构化流程。

## Solution

### Phase 1: Brainstorm（/brainstorming）

1. 探索项目上下文——了解现有 skill 模式、wiki 结构、已有命令
2. 逐一问需求问题（每次一个，选择题优先）
3. 提出 2-3 种方案 + 权衡分析 + 推荐
4. 分段呈现设计，逐段确认
5. 写 spec → `docs/superpowers/specs/YYYY-MM-DD-<name>-design.md`
6. Spec 自审（placeholder scan, 内部一致性, 歧义检查）
7. 用户审阅 spec

### Phase 2: Plan（/writing-plans）

1. 读 spec + 现有 skill 模式（thought/digest/selfos 作为参考）
2. 输出 file map + task 分解
3. 每个 task 包含：文件路径、完整内容、验证命令、commit 消息
4. 写 plan → `docs/superpowers/plans/YYYY-MM-DD-<name>.md`
5. Plan 自审（spec 覆盖度、placeholder、类型一致性）

### Phase 3: Implement（/subagent-driven-development）

1. 数据文件先行（wiki/tasks/ 等）——最简单，建立基础
2. 核心 skill 文件（.claude/skills/<name>/skill.md）——主交付
3. 集成修改并行派发（index.md, digest, CLAUDE.md）——三个独立文件
4. 每个 task 后快速验证（文件内容 + git log）
5. Symlink 创建（如需全局可用）

### Phase 4: Review

1. **Code review**（superpowers:code-reviewer）——检查 spec 对齐、edge case、集成正确性
2. **Codex challenge**（/codex challenge）——对抗性审查，找故障模式
3. 修复 review findings → 额外 commit
4. CLAUDE.md 索引 spec + plan

### 关键模式

**skill.md 结构（参考现有 thought/digest）：**
```
---
name: <name>
description: "Use when..."
user-invocable: true
---

# /<name> — 标题

## Wiki Root
## When to Use / Not for
## Data Files
## Item Format
## Commands（每个子命令一个 ### 段）
## Common Mistakes
```

**frontmatter 必须包含的字段（per wiki page convention）：**
- title, type, created, updated
- 特殊字段视 skill 需要（如 next_id）

**集成点 checklist：**
- [ ] wiki/index.md — 新增分区
- [ ] CLAUDE.md — 命令速查表 + 心智模型行
- [ ] digest — 如果新数据源应出现在回顾中
- [ ] 全局 symlink — 如果需要在 selfOS 目录外使用

**常见 review findings（instruction-driven skill 特有）：**
- 多 item 批处理时的交互时机（统一问一次 vs 每次中断）
- 参数省略时的 fallback 行为
- 同日重复调用同一命令的展示逻辑
- frontmatter 日期更新遗漏（影响下游 bump 检测等）

## Commands

```bash
# 检查 skill 被 CC 识别
# 在 CC session 中观察 skill list 是否包含新 skill

# 验证 symlink
ls -la ~/.claude/skills/<name>
readlink ~/.claude/skills/<name>

# 检查 spec/plan 索引
grep "<name>" CLAUDE.md
```

## Notes

- Date: 2026-04-28
- Case study: /todo skill（双轨 do/read 堆栈，7 tasks，6 commits + 1 review fix commit）
- 全流程耗时：约 1 个 session（brainstorm → spec → plan → implement → review → fix）
