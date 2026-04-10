# selfOS

**Compile your notes, conversations, and bookmarks into a structured, queryable knowledge graph.**

A Claude Code skill suite that turns scattered personal data into a three-layer markdown wiki with cross-references and citations.

> [Screenshot: Knowledge graph visualization showing interconnected concepts, entities, and sources]

> Requires [Claude Code](https://claude.ai/claude-code) (`npm install -g @anthropic-ai/claude-code`)

[English](#what-is-selfos) | [中文](#什么是-selfos)

---

## What is selfOS?

Most personal knowledge tools use RAG -- they re-read raw files on every query, burning tokens and losing structure. selfOS takes a different approach: **compilation**.

Each source is processed once into a three-layer wiki:
- **Source** -- one summary per ingested document
- **Concept** -- abstract ideas, methods, patterns (cross-referenced)
- **Entity** -- people, organizations, tools, papers

After compilation, querying costs zero LLM tokens. Just read 2-3 markdown files.

## Key Features

- **Knowledge Compilation** -- Three-layer architecture: source, concept, entity. Process once, query forever. Zero token cost after ingestion.
- **Context Recovery** -- AI interviews YOU to fill gaps. `/interview` surfaces open questions and thin pages. `/bookmark-chat` recovers forgotten context from old bookmarks and terse notes.
- **Quick Thought Capture** -- `/thought` lets you jot down an idea and optionally run a follow-up interview in one command.
- **Wiki Digest** -- `/digest` generates a daily activity summary and recommends questions to deepen your knowledge base.
- **Auto-Capture** -- Stop hook detects valuable personal context in Claude Code conversations and silently saves to wiki. No manual tagging needed.
- **Multi-Source Ingest** -- Notion notes, Claude/Gemini conversations, Twitter bookmarks, PDFs, web pages. One command: `/wiki ingest`.

## Command Reference

### Wiki Operations

| Command | Description |
|---------|-------------|
| `/wiki init` | Scaffold directory structure, create CLAUDE.md, initialize git |
| `/wiki ingest <url-or-path>` | Fetch or copy a source, compile into source + concept + entity pages |
| `/wiki query "<question>"` | Search index, read relevant pages, synthesize answer with citations |
| `/wiki lint` | Health check: orphan pages, broken links, missing frontmatter, uncited claims |
| `/wiki compile` | Batch-ingest all unprocessed files in `raw/` |
| `/wiki status` | Show page counts, word counts, recent log entries |
| `/wiki sync` | Incremental sync from Notion to wiki |

### Context Recovery

| Command | Description |
|---------|-------------|
| `/interview` | Wiki asks YOU questions -- targets open questions, thin pages, timeline gaps |
| `/bookmark-chat` | Pick a random Twitter bookmark or terse thought, recover the context behind it |
| `/complete` | Same as bookmark-chat but draws only from Notion Thoughts lacking context |

### Capture and Review

| Command | Description |
|---------|-------------|
| `/thought <text>` | Jot down a quick thought, optionally triggers a follow-up interview |
| `/digest` | Daily activity summary + recommended deepening questions |
| `/digest week` | Weekly digest across all activity |
| `/digest question` | Generate targeted questions from current wiki state |

## Quick Start

### Explore the Demo

```bash
git clone https://github.com/freemty/selfOS
cd selfOS

# Open in Claude Code
claude

# Query the included demo wiki
/wiki query "What is research taste?"
```

### Start Fresh (Your Own Wiki)

```bash
git clone https://github.com/freemty/selfOS
cd selfOS
rm -rf wiki/sources/ wiki/concepts/ wiki/entities/ wiki/synthesis/  # clear demo content

# Open in Claude Code
claude

# Initialize and ingest your first source
/wiki init
/wiki ingest <your-first-source>
```

Your first source will generate pages in `wiki/sources/`, `wiki/concepts/`, and `wiki/entities/`.

## Documentation

- [Graph Viewer](docs/guides/graph-viewer.md) -- Interactive knowledge graph visualization
- [Importing Conversations](docs/guides/import-conversations.md) -- Claude, Gemini, Notion data import
- [Obsidian Setup](docs/guides/obsidian-setup.md) -- View your wiki in Obsidian

## How It Works

```
raw/ (your data)
  |
  v
/wiki ingest --> wiki/sources/   (one summary per source)
                    |
                    v
               wiki/concepts/  (abstract ideas, cross-referenced)
               wiki/entities/  (people, orgs, tools)
                    |
                    v
               graph.json --> Interactive Visualization
                    |
                    v
               /wiki query --> Cited answers from compiled knowledge
```

## Architecture

selfOS follows a **compilation** philosophy, not retrieval:

1. **Source Layer** (`wiki/sources/`) -- Each raw document is summarized once with metadata, key takeaways, and citations. The raw source is never re-read.

2. **Concept Layer** (`wiki/concepts/`) -- Abstract ideas, methods, and patterns are extracted and cross-referenced using `[[wiki-links]]`. Multiple sources can feed into a single concept page.

3. **Entity Layer** (`wiki/entities/`) -- People, organizations, tools, and papers get their own pages with structured frontmatter and bidirectional links.

All pages use YAML frontmatter for structured metadata, `[[wiki-links]]` for cross-references, and `(source: [[sources/slug]])` for citations. The result is a static knowledge graph that can be browsed in Obsidian, queried by Claude Code, or visualized with the included Flask viewer (`viewer/app.py`).

## Demo Data

The repository includes 9 fictional wiki pages built around "Alex Chen," a PhD student navigating research directions:

- **3 Sources**: a Claude conversation about choosing systems over theory, a Gemini deep-dive on Flash Attention, a Notion note on research taste
- **3 Concepts**: research taste, learning by building, career pivots
- **3 Entities**: Tri Dao, a study group, an academic advisor

Explore them to understand the page format before building your own wiki:

```bash
# Browse demo pages in the viewer
python viewer/app.py    # opens localhost:5001

# Or read them directly
ls wiki/sources/ wiki/concepts/ wiki/entities/
```

## Built With

[Claude Code](https://claude.ai/claude-code) skill system -- HTML5 Canvas -- [Flask](https://flask.palletsprojects.com/)

## License

[MIT](LICENSE)

---

# selfOS -- 中文说明

**将笔记、对话、书签编译成结构化的、可查询的知识图谱。**

一套 Claude Code skill，把零散的个人数据编译成三层 markdown wiki，带交叉引用和来源标注。

## 什么是 selfOS?

大部分个人知识工具使用 RAG -- 每次查询都重新读取原始文件，消耗大量 token，丢失结构。selfOS 走的是另一条路：**编译**。

每个来源只处理一次，生成三层 wiki：
- **Source** -- 每个文档一份摘要
- **Concept** -- 抽象概念、方法论、模式（交叉引用）
- **Entity** -- 人物、组织、工具、论文

编译完成后，查询零 token 消耗。只需读 2-3 个 markdown 文件。

## 核心功能

- **知识编译** -- 三层架构：source、concept、entity。处理一次，永久查询。
- **Context Recovery** -- AI 主动向你提问来填补空白。`/interview` 发现开放问题和薄弱页面。`/bookmark-chat` 从旧书签和简短笔记中恢复遗忘的 context。
- **快速记录** -- `/thought` 随手记下想法，可选触发一轮跟进采访。
- **Wiki Digest** -- `/digest` 生成每日活动摘要，推荐深化知识库的问题。
- **自动捕获** -- Stop hook 自动检测对话中有价值的个人 context，静默保存到 wiki。
- **多源导入** -- Notion 笔记、Claude/Gemini 对话、Twitter 书签、PDF、网页。一条命令：`/wiki ingest`。

## 命令速查

### Wiki 操作

| 命令 | 说明 |
|------|------|
| `/wiki init` | 创建目录结构、CLAUDE.md、初始化 git |
| `/wiki ingest <url-or-path>` | 获取来源，编译为 source + concept + entity 页面 |
| `/wiki query "问题"` | 搜索索引，读取相关页面，生成带引用的回答 |
| `/wiki lint` | 健康检查：孤页、断链、缺失 frontmatter、无引用声明 |
| `/wiki compile` | 批量编译 `raw/` 中未处理的文件 |
| `/wiki status` | 显示页面数、字数、最近日志 |
| `/wiki sync` | 从 Notion 增量同步到 wiki |

### Context Recovery

| 命令 | 说明 |
|------|------|
| `/interview` | Wiki 主动向你提问 -- 针对开放问题、薄弱页面、时间线空白 |
| `/bookmark-chat` | 随机抽一条书签或简短 thought，还原背后的 context |
| `/complete` | 只从缺乏 context 的 Notion Thoughts 中抽取 |

### 捕获与回顾

| 命令 | 说明 |
|------|------|
| `/thought <text>` | 快速记录想法，可选触发跟进采访 |
| `/digest` | 每日活动总结 + 推荐深化问题 |
| `/digest week` | 周度汇总 |
| `/digest question` | 从当前 wiki 状态生成针对性问题 |

## 快速开始

前置要求：[Claude Code](https://claude.ai/claude-code)（`npm install -g @anthropic-ai/claude-code`）

### 体验 Demo

```bash
git clone https://github.com/freemty/selfOS
cd selfOS

# 在 Claude Code 中打开
claude

# 查询内置的 demo wiki
/wiki query "什么是 research taste？"
```

### 从零开始（构建自己的 wiki）

```bash
git clone https://github.com/freemty/selfOS
cd selfOS
rm -rf wiki/sources/ wiki/concepts/ wiki/entities/ wiki/synthesis/  # 清除 demo 内容

# 在 Claude Code 中打开
claude

# 初始化并导入第一个来源
/wiki init
/wiki ingest <你的第一个来源>
```

第一个来源会自动在 `wiki/sources/`、`wiki/concepts/`、`wiki/entities/` 下生成页面。

## 文档

- [Graph Viewer](docs/guides/graph-viewer.md) -- 交互式知识图谱可视化
- [导入对话](docs/guides/import-conversations.md) -- Claude、Gemini、Notion 数据导入
- [Obsidian 配置](docs/guides/obsidian-setup.md) -- 在 Obsidian 中浏览 wiki

## 演示数据

仓库包含 9 个虚构的 wiki 页面，围绕 "Alex Chen"（一个探索研究方向的博士生）展开：

- **3 个 Source**：关于选择系统方向的 Claude 对话、Flash Attention 深入分析、关于 research taste 的 Notion 笔记
- **3 个 Concept**：research taste、learning by building、career pivots
- **3 个 Entity**：Tri Dao、study group、academic advisor

```bash
# 用可视化工具浏览
python viewer/app.py    # localhost:5001

# 或直接查看文件
ls wiki/sources/ wiki/concepts/ wiki/entities/
```

## 许可证

[MIT](LICENSE)
