# Changelog

## v1.1.0 @freemty - 2026-05-19

### 新增
- **`/transcribe`** — 音频文件 → wiki source page。使用火山引擎 ASR 转写，输出带时间戳和说话人的转录，自动 ingest 进 wiki
- **`/de-ai`** — 脱 AI 味。去除过度声称、filler、hedge words 等 AI 典型语言痕迹
- **`/academic-writing`** — 21 条英文学术写作规则 (Strunk & White / Orwell / Pinker) + 9 条 LLM 反模式。论文草稿 context-triggered
- **`/paper-plot`** — 出版级 matplotlib 图表模板，共享 style.py (Palatino + STIX Math + 5 级配色)
- **`scripts/transcribe.py`** — 火山引擎 ASR 转写脚本（异步轮询 + 说话人分离 + 后处理）
- **`docs/knowhow/toolchain/volcengine-asr.md`** — 火山引擎语音识别配置指南
- **`docs/knowhow/runbooks/audio-transcribe-to-wiki.md`** — 录音 → wiki 全流程 runbook
- **`docs/blog-template/`** — 博客文章 HTML 模板

### 变更
- README 更新：skill 数量 7→11，新增 /transcribe + Writing 分区
- 所有现有 skill 微调路径和措辞

### 数据统计
- Skills: 7 → 11 (+4: transcribe, de-ai, academic-writing, paper-plot)
- Sources: 904 → 923
- Concepts: 80 → 88
- Entities: 96 → 108

---

## v1.0.0 @freemty - 2026-05-04

### 新增
- **Skill 重构**：`selfos` → `wiki`，`selfos-completion` → `interview`，`/thought` 变纯写入（追问移到 `/interview thought`），`/digest` 变纯统计（不推荐问题），新增 `wiki-help` 速查
- **`/wiki synthesize`** — 扫描 concept cluster synthesis-readiness，推荐候选，引导写综合
- **Q&A 序列** — ingest 对话类 source 时提取用户问题+回答序列作为一等内容
- **格式保真** — ASCII 图/代码块/等宽表格 code block 原样保留
- **Template 分支 v1.0.0** — 同步 skill 重构 + CLAUDE.md 全面更新，删除 6 个 dead skills
- **小红书 MCP** — Docker + mcp-remote stdio 桥接 + cookie 注入，首次打通
- **2 个 unbox** — Xiaolong Wang + Sifei Liu 研究者画像（双非起点 cluster 发现）
- **Synthesis** — 双非起点×Embodied AI 结构性匹配（5 人 cluster 分析）
- **Eric Xing entity** — CMU 教授，张昊 advisor，三代精神 DNA 传承
- **语言风格社会经济框架** — 三变量（经济模式×流动性×权力距离）+ L1/L2/L3 表达道德层级
- **配色审美理论** — 对比度+pop-out+对称性+约束优雅，红色作为 identity 投射
- **Neuroscience First Principles** — 视觉层级→World Model 生物学根基，D.F. 案例证明 VLM/VLA 应分离
- **张昊涌现 Lab 万字访谈归档** — 五条价值观共振 + 招生标准 + L3 personality role model

### 变更
- Skill 目录从 11 个精简为 5 个（wiki/interview/thought/digest/todo）
- CLAUDE.md 全面重写：Interview 统一追问、Digest 纯统计、Todo Stack、Branch Architecture
- template-data-separation runbook 新增反向同步流程 + 脱敏 checklist + sync history
- wiki/index.md 计数更新：80 concepts, 96 entities, 904 sources, 22 syntheses

### 修复
- lint: 修复 11 个断链 + 补 10 个遗漏 index 条目
- `[[projects/agentic-datapipe]]` 无效链接（改为纯文本描述）

### 数据统计
- Sources: 890 → 904 (+14)
- Concepts: 74 → 80 (+6: flashattention, continual-pretraining, benign-overfitting, vintage-lm, color-aesthetics, language-style)
- Entities: 80 → 96 (+16: eric-xing, nvidia, jensen-huang, tri-dao, shuning-shang, + tool stubs)
- Synthesis: 14 → 22 (+8: 5 batch + double-non-cluster + 2 others)
- Skills: 11 → 5 (restructured, not lost — merged into wiki/interview)

## v0.5.0 @freemty - 2026-04-29

### 新增
- **`/todo` skill** — 双轨 todo 堆栈（do/read），日计划仪式（每天三件事），未完成自动顺延，月度归档
  - `wiki/tasks/do.md` + `wiki/tasks/read.md` 活跃池
  - `wiki/tasks/archive/YYYY-MM.md` 月度归档
  - 3 个 reference workflow 文档：add-workflow, today-workflow, done-workflow
  - R-item 完成后提示 `/wiki ingest` 衔接吸收流程
- **`/wiki synthesize`** — 扫描 concept cluster 的 synthesis-readiness（source 密度 × cross-ref × 活跃度），推荐 Top 5 候选，引导写综合
- **Q&A 序列** — ingest 对话类 source 时提取用户问题+回答序列作为一等内容（`## Q&A 序列`），3+ 实质性问题触发
- **格式保真** — ingest 时 ASCII 图/代码块/等宽表格包在 code block 里原样保留
- **digest 联动**：`/digest` 回顾末尾新增「本期完成」小结，读取当月 archive
- **Template 分支**：orphan `template` 分支（85 文件），脱敏后的纯骨架，fork 即用
- **2 个 runbook**：skill 创建全流程 + template/data 分层管理

### 变更
- CLAUDE.md 新增 Todo Stack 命令速查表 + Branch Architecture + 用户心智模型更新
- wiki/index.md 新增 `## Tasks` 分区
- todo skill.md 重构：主文件精简到 96 行，核心 workflow 提取到 `references/`
- ingest-workflow 移除 `{wiki_root}` 占位符，合并 index+log 为并行步骤
- page-templates entity 模板新增 `aliases` 字段
- synthesize-workflow 用 frontmatter 替代 grep 扫描，加读取上限（15 sources, 10 linked）
- done-workflow 同文件批量读 + archive/log/frontmatter 标记并行

### 修复
- 5 个 Obsidian/工具 skill 补齐缺失的 `user-invocable: false`
- `/todo done` 多 R-item ingest 提示改为统一询问
- `/todo add` 省略 track 参数时自动推断
- `/todo today` 支持 same-day re-run
- do.md / read.md 补齐 `created` frontmatter
- digest "0 完成时省略" 显式指令
- template 分支脱敏：5 个 skill 路径泛化、示例去个人化、CHANGELOG/TODO 精简

### 构建与工具链
- `docs/superpowers/specs/2026-04-28-todo-system-design.md` — todo 系统设计 spec
- `docs/superpowers/plans/2026-04-28-todo-system.md` — 7 task 实施计划
- 全局 symlink `~/.claude/skills/todo` 创建
- Codex adversarial challenge + code-reviewer + 3-agent simplify review

### 数据统计
- Skills: 10 → 11 (+1: todo), commands: +2 (/todo, /wiki synthesize)
- Reference files: 11 → 15 (+3 todo workflows, +1 synthesize-workflow)
- Synthesis: 9 → 14 (+5 batch synthesis)
- Skill frontmatter 完整性: 6/11 → 11/11 (100%)
- Template branch: 85 files, 0 personal data leaks

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
