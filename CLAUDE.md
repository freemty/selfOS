<!-- llm-wiki -->
# Knowledge Base

This is an LLM-maintained wiki. The LLM writes and maintains all content in `wiki/`.
Human curates sources in `raw/` and directs exploration via queries.

## Directory Structure

- `raw/` — Immutable source documents. Never modify these.
  - `raw/assets/` — Downloaded images referenced by sources
  - `raw/notion-notes/` — Exported Notion LifeOS notes
- `wiki/` — LLM-generated articles. The LLM owns this layer entirely.
  - `wiki/index.md` — Master catalog of all pages with one-line summaries
  - `wiki/log.md` — Chronological record of all operations
  - `wiki/overview.md` — High-level synthesis of the entire knowledge base
  - `wiki/concepts/` — One article per concept/topic
  - `wiki/entities/` — One page per entity (person, org, tool, paper, dataset)
  - `wiki/sources/` — One summary per ingested source
  - `wiki/synthesis/` — Filed-back query outputs, comparisons, analyses

## Page Conventions

### YAML Frontmatter (required on every wiki page)

Every page MUST start with YAML frontmatter:

```yaml
---
title: "Page Title"
type: concept | entity | source | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["source-slug-1", "source-slug-2"]
tags: [tag1, tag2]
aliases: ["alt-name-1", "alt-name-2"]  # Entity pages only — all known name variants
summary: "One-line summary for the index"
---
```

### Entity Aliases

Entity pages (especially people) MUST include an `aliases` field listing all known name
variants: Chinese name, English name, pinyin, nicknames, GitHub usernames, common
misspellings. When matching unbox profiles or new sources to existing entities, check
aliases in addition to filename and title.

### Cross-References

Use `[[page-name]]` syntax for internal links. When creating or updating a page,
check for opportunities to link to existing pages. Maintain bidirectional links.

### Source Citations

Important claims MUST cite their source: `(source: [[sources/source-slug]])`.
If a claim cannot be traced to a source, mark it: `(unsourced — verify)`.

### Conflict Handling

When new data contradicts existing wiki content:
1. Update the page with the new information
2. Add a `## Revision Notes` section documenting what changed and why
3. If genuine ambiguity, present both views with sources

## Workflows

### On Ingest
1. Read the source completely
2. Create `wiki/sources/<slug>.md` with summary, key takeaways, metadata
3. For each significant concept: create or update `wiki/concepts/<slug>.md`
4. For each significant entity: create or update `wiki/entities/<slug>.md`
5. Update all relevant pages with cross-references
6. Update `wiki/index.md` — add new entries, update summaries of modified pages
7. Append to `wiki/log.md`
8. If the source materially shifts the big picture, update `wiki/overview.md`

### On Query
1. Read `wiki/index.md` to identify relevant pages
2. Read relevant pages
3. Synthesize answer with page citations
4. If filing back: save to `wiki/synthesis/`, update index and log

### On Lint
1. Scan all wiki pages for: orphans, missing pages, stale claims, contradictions,
   missing frontmatter, uncited claims, concepts mentioned but lacking pages
2. Report findings with severity
3. Fix if authorized

## Quick commands

### Wiki Operations

Skill: `.claude/skills/wiki/` → symlink at `~/.claude/skills/wiki`

| Command | Purpose | Example |
|---------|---------|---------|
| `/wiki query "问题"` | 搜索 wiki + 综合回答，可选 file back 到 synthesis/ | `/wiki query "我的科研路线演变"` |
| `/wiki ingest <url>` | 抓取网页/PDF → 编译进 wiki（source + concept + entity） | `/wiki ingest https://arxiv.org/abs/xxx` |
| `/wiki lint` | 健康检查：断链、孤页、缺失引用、frontmatter 错误 | `/wiki lint` |
| `/wiki compile` | 批量编译 raw/ 中未处理的源文件 | `/wiki compile` |
| `/wiki synthesize` | 扫描 synthesis 候选 → 推荐 → 引导写综合 | `/wiki synthesize` |
| `/wiki status` | 统计：页面数、字数、最近活动 | `/wiki status` |

### Todo Stack

Skill: `.claude/skills/todo/` → symlink at `~/.claude/skills/todo`

| Command | Purpose | Example |
|---------|---------|---------|
| `/todo add do "描述"` | 加行动到 do pool | `/todo add do "回复邮件" #admin` |
| `/todo add read "描述"` | 加阅读到 read pool | `/todo add read "Erta 论文" #paper` |
| `/todo today` | 日计划仪式：从池子里挑今天的 items | `/todo today` |
| `/todo done <id>` | 标记完成，归档 | `/todo done T001` |
| `/todo list` | 查看当前 Today + Pool | `/todo list` |
| `/todo list archive` | 查看月度归档 | `/todo list archive 2026-03` |

用户心智模型：`/thought` 记想法 → `/todo` 管行动 → `/interview` 让 wiki 问我 → `/digest` 回顾变化 → `/wiki` 管理 → `/wiki-help` 速查

### Quick Thought Capture

Skill: `.claude/skills/thought/` → symlink at `~/.claude/skills/thought`

| Command | Purpose | Example |
|---------|---------|---------|
| `/thought <text>` | 快速记录想法（纯写入，不追问） | `/thought agent时代最大的杠杆是taste` |

写完后可用 `/interview thought` 追问展开。

### Wiki Digest

Skill: `.claude/skills/digest/` → symlink at `~/.claude/skills/digest`

| Command | Purpose | Example |
|---------|---------|---------|
| `/digest` | 今日 wiki 变化回顾 + 完成任务 | `/digest` |
| `/digest week` | 本周回顾 + 活跃概念 | `/digest week` |

纯统计回顾，不推荐问题（追问用 `/interview`）。

### Interview（统一追问）

Skill: `.claude/skills/interview/` → symlink at `~/.claude/skills/interview`

| Command | Purpose |
|---------|---------|
| `/interview` | wiki 主动追问：pending 偏好 → open questions → thin pages → timeline gaps |
| `/interview thought` | 追问刚记录的 `/thought` |
| `/bookmark-chat` | 随机抽推特书签，对话还原 context |
| `/complete` | 抽缺 context 的 Notion Thoughts |

状态文件：`docs/bookmark-chat-log.jsonl`，产出：`wiki/synthesis/bookmark-chat-YYYY-MM-DD.md`

### Wiki Help（速查）

Skill: `.claude/skills/wiki-help/` → symlink at `~/.claude/skills/wiki-help`

| Command | Purpose |
|---------|---------|
| `/wiki-help` | 输出所有 selfOS 命令速查表 |

### Auto-Capture + Preference Tagging (被动层)

每次 Claude Code 对话结束时，Stop hook 自动：
1. **Context 抽取**：检测对话中的个人 context（中英文信号词匹配），有价值的内容静默保存为 `wiki/sources/auto-*.md`
2. **Preference Tagging**：检测未展开的判断/偏好/情绪反应，生成 `pending_questions` 写入 frontmatter，供下次 `/interview` 优先追问

你不需要做任何事情。Hook 脚本：`hooks/auto-capture.sh` → `scripts/auto-ingest.py`

### Search (qmd)

| Command | Purpose | Example |
|---------|---------|---------|
| `qmd search "关键词"` | BM25 关键词搜索（最快） | `qmd search "RoPE attention"` |
| `qmd vsearch "语义"` | 向量语义搜索 | `qmd vsearch "如何选择研究方向"` |
| `qmd query "问题"` | 混合 BM25 + 向量 + LLM re-ranking（最佳质量） | `qmd query "最重要的方法论"` |
| `qmd search "xxx" -c wiki` | 限定 collection 搜索 | |
| `qmd search "xxx" --json` | JSON 输出（给 LLM 用） | |

### Obsidian

| 操作 | 说明 |
|------|------|
| Graph View | `Cmd+P` → "graph"。Filter: `-path:wiki/sources -path:raw` 隐藏 source 层 |
| 颜色分组 | Groups: `path:wiki/concepts` = 蓝, `path:wiki/entities` = 橙 |
| 快速搜索 | `Cmd+O` 打开文件，`Cmd+Shift+F` 全局搜索 |
| Dataview | 对 frontmatter 做结构化查询（需安装插件） |
| Marp Slides | 在 wiki 内写 slides 并预览（需安装插件） |

## Distribution

### Branch Architecture

| 分支 | 用途 | 包含数据 |
|------|------|---------|
| `template` | 公开发布的骨架——skill, scripts, docs, wiki 结构模板 | 否 |
| `private` | 个人完整知识库（template + wiki 内容） | 是 |

- 功能开发（新 skill、改 script）→ 在 `template` 分支，cherry-pick 到 `private`
- 日常数据操作（ingest、todo）→ 直接在 `private`
- 发布 → push `template` 分支
- **不要 merge**（orphan 分支无共同祖先）
- 详见 `docs/knowhow/runbooks/template-data-separation.md`

### Fork 用户流程

`git clone` → `./setup.sh` → `/wiki init`

| 文件 | 用途 |
|------|------|
| `setup.sh` | 一键注册全局 skill symlink + 可选 Auto-Capture hook |
| `hooks/auto-capture.sh` | repo 内的 Stop hook 脚本 |
| `.claude/skills/` | 所有 skill 源文件（项目级自动加载） |

## Specs

- `docs/specs/twitter-bookmarks-ingest.md` — 推特书签 → wiki 导入流程
- `docs/specs/2026-04-07-knowledge-graph-scaling.md` — 知识图谱扩展方案
- `docs/specs/2026-04-07-context-capture-modes.md` — Chat Mode + Interview Mode
- `docs/superpowers/specs/2026-04-09-selfos-skill-suite-design.md` — selfOS skill 集设计（三层架构 + 分发）⚠️ 已过时：skill 已从 11→7 重构，见 `docs/knowhow/runbooks/selfos-skill-refactor.md`
- `docs/superpowers/specs/2026-04-28-todo-system-design.md` — 双轨 todo 堆栈设计（do/read + 日计划仪式 + 月度归档）
- `docs/superpowers/plans/2026-04-28-todo-system.md` — todo 系统实现计划（7 tasks）

## Guides

- `docs/guides/import-data.md` — 数据导入指南：Claude.ai / Gemini / Twitter 书签 → wiki

## Knowhow

- `docs/knowhow/toolchain/` — qmd, chat export, fieldtheory, Obsidian 插件调研等工具指南
- `docs/knowhow/toolchain/obsidian-cli-integration.md` — Obsidian CLI/API 集成方案调研
- `docs/knowhow/toolchain/cc-skill-distribution.md` — CC Skill 分发架构：源/symlink 分离、CSO 规则、hook 模式
- `docs/knowhow/runbooks/selfos-skill-refactor.md` — Skill 体系审计、清理、重命名、职责正交化 runbook
- `docs/knowhow/debug-solutions/` — Obsidian 配置等问题解决
- `docs/knowhow/runbooks/` — LLM Wiki 搭建等操作手册
