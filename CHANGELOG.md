# Changelog

## v0.5.0 @freemty - 2026-04-29

### 新增
- **`/todo` skill** — 双轨 todo 堆栈（do/read），日计划仪式（每天三件事），未完成自动顺延，月度归档
  - `wiki/tasks/do.md` + `wiki/tasks/read.md` 活跃池
  - `wiki/tasks/archive/YYYY-MM.md` 月度归档
  - 3 个 reference workflow 文档：add-workflow, today-workflow, done-workflow
  - R-item 完成后提示 `/wiki ingest` 衔接吸收流程
- **digest 联动**：`/digest` 回顾末尾新增「本期完成」小结，读取当月 archive
- **Skill 创建 runbook**：`docs/knowhow/runbooks/selfos-skill-creation.md` — brainstorm → spec → plan → implement → review 全流程

### 变更
- CLAUDE.md 新增 Todo Stack 命令速查表 + 用户心智模型更新（`/thought → /todo → /interview → /digest → /wiki`）
- wiki/index.md 新增 `## Tasks` 分区
- todo skill.md 重构：主文件精简到 96 行，核心 workflow 提取到 `references/`（对齐 selfos SKILL.md 模式）

### 修复
- 5 个 Obsidian/工具 skill 补齐缺失的 `user-invocable: false`（defuddle, obsidian-markdown, obsidian-bases, obsidian-cli, json-canvas）
- `/todo done` 多 R-item 时 ingest 提示改为统一询问（不逐个中断）
- `/todo add` 新增省略 track 参数时的自动推断 fallback
- `/todo today` 展示模板支持 same-day re-run（显示 Today 区已选 items）
- do.md / read.md 补齐缺失的 `created` frontmatter 字段
- digest skill 新增 "0 完成时省略" 的显式指令

### 构建与工具链
- `docs/superpowers/specs/2026-04-28-todo-system-design.md` — todo 系统设计 spec
- `docs/superpowers/plans/2026-04-28-todo-system.md` — 7 task 实施计划
- 全局 symlink `~/.claude/skills/todo` 创建

### 数据统计
- Skills: 10 → 11 (+1: todo)
- Reference files: 11 → 14 (+3: todo add/today/done workflows)
- Skill frontmatter 完整性: 6/11 → 11/11 (100%)

## v0.4.0 @freemty - 2026-04-11

### 新增
- **Physics of AI 概念线**：batch ingest 刘子鸣 ×4 博客 + Allen Zhu Physics of LLMs + 陶哲轩 Dwarkesh 访谈，形成完整的 "AI 理论理解" 概念网络
  - 4 new concepts: structuralism-ai, physics-of-ai, research-knowledge-graph, everything-is-language
  - 3 new entities: ziming-liu, allen-zhu, terence-tao
  - Tycho-Kepler-Newton 框架现有 4 个独立来源（wiki 作者 / 刘子鸣 / Allen Zhu / 陶哲轩）
- **GBrain (Garry Tan) ingest**：compiled truth + timeline 模式与 selfOS source→concept 的本质性对比
- **Stale Concept Detection**：`scripts/interview-questions.py` 新增 `scan_stale_concepts()`，检测"理解落后于证据"的概念页（inspired by GBrain），作为 priority-1 interview 问题
  - 比较 concept `updated` vs 最新 source `updated`，阈值 7 天
  - 输出包含 `concept_path` 和 `latest_source` 方便下游处理
- **Intelligence Density 数据竞赛论** (LI Yikang blog ingest)：new concept + entity
- 张昊 entity 扩展：career timeline + CSE 234 课程结构
- 统一数据导入指南 `docs/guides/import-data.md`

### 变更
- `interview-questions.py` 优先级表新增 stale_concept (priority 1)
- selfos-completion SKILL.md + interview-workflow.md 更新：stale concept 处理流程（重写 Overview 而非追加）
- ziming-liu entity 精简：内联内容替换为 concept 链接索引
- allen-zhu source 精简：移除对比表（已在 physics-of-ai concept 维护）
- physics-of-ai concept 新增"两种实践风格"对比表（Allen Zhu vs 刘子鸣）
- tycho-kepler-newton 概念页新增"多源独立使用"对照表

### 构建与工具链
- `_latest_source_date()` 重构为返回 `(date, slug)` tuple
- 移除未使用的 `_SOURCE_DATE_RE` 正则
- `datetime` import 移至文件顶部（风格一致性）
- source count 阈值从 `< 2` 放宽到 `< 1`

### 数据统计
- Sources: 830 → 837 (+7)
- Concepts: 44 → 49 (+5: structuralism-ai, physics-of-ai, research-knowledge-graph, everything-is-language, intelligence-density-data-strategy)
- Entities: 49 → 53 (+4: ziming-liu, allen-zhu, terence-tao, li-yikang)

## v0.3.0 @freemty - 2026-04-10

### 新增
- 全量编译：829 source pages（Gemini 481 + Claude 88 + Notion 251），从 70 扩展到 829
- Richness 标注系统：829/829 sources 标注 high(226)/medium(344)/low(259)，12 批并行 Opus agent
- 深度内容解析：225 条 high-richness source 逐条读取，提取人物/概念/关系
- Concept 网络扩展：16 → 44 concepts（含探索派vs好学生、Forward KL 社交框架、attention-sink 研究等）
- Entity 网络扩展：14 → 49 entities（含导师网络、学术偶像、历史人物、核心朋友等 35 个新页面）
- 6 条 Notion Thought 口述 Context Recovery（给CC造锤子、不断更meta、AlphaEvolve正交 等）
- KnightNemo life-logging blog ingest + selfOS blog 写作 pending
- Notion API 导出脚本：`scripts/export-notion-notes.py`（分页遍历 + block-to-markdown）
- 3 个用户指南：Graph Viewer / Conversation Import / Obsidian Setup
- 9 个虚构 demo 节点（Alex Chen persona，公开展示用）

### 变更
- Repo 拆分为双轨：main (public template) + demo (private full data, pre-push hook 保护)
- CLAUDE.md public 版：去除 qmd/fieldtheory/个人 hook 引用
- README 全面重写：命令参考表、双路径 Quick Start、Architecture 段落、Documentation links
- 4 个 selfOS skill 加了显式 wiki root (`~/selfOS/` 绝对路径)
- `extract-all-sources.py`：路径改为 selfOS + 去重保护（不删除已有 source）
- wiki/index.md 重构：People 分为 6 个语义子分组

### 修复
- 73 个 -1 后缀重复 source 文件清理（Notion 重新导出碰撞产生的副本）
- Index/overview 数据计数修正（两轮 code review：899→829 sources, richness 226 not 248）
- 16 个 concept + 4 个 entity 空 sources 回填
- 错误日期 2002→2025 修正（transfusion-team source）
- Launch docs 删除（和 "fictional demo" 框架矛盾的旧稿）
- origin/demo 覆盖为干净版（旧的含个人数据的版本已清除）

### 构建与工具链
- `docs/superpowers/specs/2026-04-10-full-compilation-design.md` — 全量编译设计 spec
- `docs/superpowers/plans/2026-04-10-full-compilation.md` — 10 task 实施计划
- 12 batch richness reports + 5 deep-scan reports（concept/entity 候选数据）
- `.git/hooks/pre-push` — 阻止 demo branch 意外 push

## v0.2.0 @freemty - 2026-04-09

### 新增
- `/thought <text>` skill — 快速写入一句话想法 + 立刻 interview 补充 context
- `/digest` skill — 每日/每周 wiki 变化回顾 + 推荐问题（支持 `/digest week`, `/digest question`）
- `/interview` 升级为三池问题系统：pending 偏好追问 (P0) → open questions (P1) → thin pages / timeline gaps (P2-3)
- Preference tagging — auto-ingest.py 自动检测未展开的判断/偏好/情绪，生成 `pending_questions` 写入 frontmatter
- `pending_questions` 扫描器 — interview-questions.py 新增 priority 0 问题池
- `setup.sh` — 一键注册全局 skill symlink + 可选 Auto-Capture hook
- `hooks/auto-capture.sh` — repo 内的 Stop hook 脚本（从全局 ~/.claude/hooks/ 迁入）

### 变更
- `/interview` 问题优先级从 1-3 扩展为 0-3（0 = pending questions, 最高优先）
- Auto-Capture 段落升级为 "Auto-Capture + Preference Tagging"
- CLAUDE.md 新增 Distribution 段落、命令心智模型、`/digest` 文档
- README 新增 `/thought`、`/digest`、Preference Tagging 描述 + 命令速查表

### 修复
- interview-questions.py: `item_re` 限定到 `pending_questions` YAML 块（避免匹配其他列表字段）
- auto-ingest.py: `build_frontmatter` title 双引号转义，防止生成无效 YAML
- auto-ingest.py: 收紧 preference regex（要求主观前缀、句子边界锚定，降低误报率）
- hooks/auto-capture.sh: `echo` 改为 `printf '%s'`（JSON 特殊字符安全）
- selfos-completion skill: SKILL.md 改回 skill.md（CC 小写约定）
- Skill frontmatter: description 改为 CSO 规范的 "Use when..." 格式，selfos 补上 `user-invocable: true`

### 构建与工具链
- `docs/knowhow/toolchain/cc-skill-distribution.md` — CC Skill 分发架构归档

### 其他
- `docs/superpowers/specs/2026-04-09-selfos-skill-suite-design.md` — 三层架构设计 spec
- `docs/superpowers/plans/2026-04-09-selfos-skill-suite.md` — 6 task 实施计划
- README 全面改版：中文 first、砍掉 vs Graphify、feature 压缩、命令速查表

## v0.1.0 @freemty - 2026-04-08

- Project initialized with knowledge compilation wiki
- `/wiki ingest/query/lint/compile/sync/status` skills
- `/interview`, `/bookmark-chat`, `/complete` context recovery
- Auto-Capture Stop hook
- Hybrid search via qmd
- Canvas-based knowledge graph visualization
