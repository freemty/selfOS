# selfOS

**Your personal AI operating system — compile your notes, conversations, and bookmarks into a queryable knowledge base that understands you.**

<!-- screenshot placeholder -->

[English](#selfos) | [中文](#selfos--个人-ai-操作系统)

## What is selfOS?

Most personal knowledge tools use RAG — they re-read your raw files on every query, burning tokens and losing structure. selfOS takes a different approach: **compilation**. Each source is processed once into a three-layer wiki (source → concept → entity) with cross-references, citations, and frontmatter. After compilation, querying costs zero LLM tokens — just read 2-3 markdown files.

> Graphify turns code into graphs. selfOS turns **YOU** into a graph.

11 months of daily use. Real data. Not a demo.

<!-- demo gif placeholder -->

## Key Features

- 🧠 **Knowledge Compilation** — Three-layer compilation: source → concept → entity. Process once, query forever. Zero token cost after ingestion.

- 🔄 **Context Recovery** — AI interviews YOU to fill gaps. `/interview` finds open questions and thin pages. `/bookmark-chat` recovers forgotten context from old bookmarks and terse notes. We call it "Reverse DPO."

- 🔍 **Hybrid Search** — BM25 keyword + vector semantic + LLM re-ranking via `qmd`. Three search modes for different speed/quality tradeoffs.

- 📊 **Knowledge Graph Visualization** — Interactive vis.js graph with search, filters, and detail panel. See how your ideas connect.

- 🤖 **Auto-Capture** — Stop hook detects valuable personal context in Claude Code conversations and silently saves to wiki. No manual tagging.

- 📎 **Multi-Source Ingest** — Notion notes, Claude/Gemini conversations, Twitter bookmarks, PDFs, web pages. One command: `/wiki ingest`.

## Worked Example

| Metric | Demo Data |
|--------|-----------|
| Raw sources | ~50 |
| Compiled concepts | 15 |
| Compiled entities | 10 |
| Knowledge graph edges | ~120 |
| Query cost | Read 2-3 md files (vs reading all raw) |

## Quick Start

```bash
git clone https://github.com/freemty/selfOS
cd selfOS

# Explore the demo (real sanitized data)
git checkout demo
python viewer/app.py    # → localhost:5001

# Start your own
git checkout main
# In Claude Code:
/wiki init
/wiki ingest <your-first-source>
```

## How It Works

```
raw/ (your data)
  │
  ▼
/wiki ingest ──→ wiki/sources/   (one summary per source)
                    │
                    ▼
               wiki/concepts/  (abstract ideas, cross-referenced)
               wiki/entities/  (people, orgs, tools)
                    │
                    ▼
               graph.json ──→ Interactive Visualization
                    │
                    ▼
               /wiki query ──→ Cited answers from compiled knowledge
```

## vs Graphify

Complementary tools, different domains.

| | Graphify | selfOS |
|---|---------|--------|
| Input | Code + docs | Notes + conversations + bookmarks |
| Goal | Understand codebase | Understand yourself |
| Method | AST + LLM extraction | Three-layer knowledge compilation |
| Output | Knowledge graph | Knowledge graph + queryable wiki |
| Unique | Token compression | Context recovery (Reverse DPO) |
| Position | "Graphify for code" | "selfOS for life" |

## Built With

[Claude Code](https://claude.ai/claude-code) skill system · [vis.js](https://visjs.org/) · [Flask](https://flask.palletsprojects.com/) · [qmd](https://github.com/User/qmd)

## License

[MIT](LICENSE)

---

# selfOS — 个人 AI 操作系统

**将笔记、对话、书签编译成一个真正理解你的知识库。**

<!-- screenshot placeholder -->

[English](#selfos) | [中文](#selfos--个人-ai-操作系统)

## selfOS 是什么?

大部分个人知识工具用 RAG -- 每次查询都重新读取原始文件，消耗大量 token，丢失结构。selfOS 走的是另一条路: **编译**。每个来源只处理一次，生成三层 wiki（source -> concept -> entity），带交叉引用、来源标注和结构化 frontmatter。编译完成后，查询不消耗任何 LLM token -- 只需读 2-3 个 markdown 文件。

> Graphify 把代码变成图谱。selfOS 把**你**变成图谱。

11 个月的日常使用。真实数据。不是 demo。

<!-- demo gif placeholder -->

## 核心功能

- 🧠 **知识编译** -- 三层编译: source -> concept -> entity。处理一次，永久查询。编译后查询零 token 消耗。

- 🔄 **Context Recovery** -- AI 主动向你提问，填补知识空白。`/interview` 发现开放问题和薄弱页面。`/bookmark-chat` 从旧书签和简短笔记中恢复遗忘的 context。我们称之为 "逆向 DPO"。

- 🔍 **混合搜索** -- BM25 关键词 + 向量语义 + LLM re-ranking，通过 `qmd` 实现。三种搜索模式对应不同的速度/质量权衡。

- 📊 **知识图谱可视化** -- 基于 vis.js 的交互式图谱，支持搜索、过滤和详情面板。直观看到你的想法如何连接。

- 🤖 **自动捕获** -- Stop hook 自动检测 Claude Code 对话中有价值的个人 context，静默保存到 wiki。无需手动标记。

- 📎 **多源导入** -- Notion 笔记、Claude/Gemini 对话、Twitter 书签、PDF、网页。一条命令: `/wiki ingest`。

## 实际效果

| 指标 | 演示数据 |
|------|----------|
| 原始来源 | ~50 |
| 编译后的概念 | 15 |
| 编译后的实体 | 10 |
| 知识图谱边数 | ~120 |
| 查询成本 | 读 2-3 个 md 文件 (vs 读全部原始文件) |

## 快速开始

```bash
git clone https://github.com/freemty/selfOS
cd selfOS

# 体验演示 (真实脱敏数据)
git checkout demo
python viewer/app.py    # → localhost:5001

# 开始构建你自己的
git checkout main
# 在 Claude Code 中:
/wiki init
/wiki ingest <your-first-source>
```

## 工作原理

```
raw/ (你的数据)
  │
  ▼
/wiki ingest ──→ wiki/sources/   (每个来源一份摘要)
                    │
                    ▼
               wiki/concepts/  (抽象概念，交叉引用)
               wiki/entities/  (人物、组织、工具)
                    │
                    ▼
               graph.json ──→ 交互式可视化
                    │
                    ▼
               /wiki query ──→ 带引用的知识查询
```

## vs Graphify

互补工具，不同领域。

| | Graphify | selfOS |
|---|---------|--------|
| 输入 | 代码 + 文档 | 笔记 + 对话 + 书签 |
| 目标 | 理解代码库 | 理解你自己 |
| 方法 | AST + LLM 提取 | 三层知识编译 |
| 输出 | 知识图谱 | 知识图谱 + 可查询 wiki |
| 独特之处 | Token 压缩 | Context Recovery (逆向 DPO) |
| 定位 | "Graphify for code" | "selfOS for life" |

## 技术栈

[Claude Code](https://claude.ai/claude-code) skill system · [vis.js](https://visjs.org/) · [Flask](https://flask.palletsprojects.com/) · [qmd](https://github.com/User/qmd)

## 许可证

[MIT](LICENSE)
