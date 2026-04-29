# selfOS

**把笔记、对话、书签编译成一个真正理解你的 knowledge base。**

<!-- screenshot placeholder -->

[中文](#selfos) | [English](#selfos--personal-ai-knowledge-os)

## selfOS 是什么？

大部分个人知识工具用 RAG——每次查询重新读原始文件，烧 token，丢结构。selfOS 反过来：**编译一次，永久查询**。每个 source 只处理一次，生成三层 wiki（source → concept → entity），带交叉引用和来源标注。编译完之后查知识不花一个 LLM token，读 2-3 个 markdown 文件就够了。

> Graphify 把代码变成图谱。selfOS 把**你**变成图谱。

11 个月日常使用。真实数据。

<!-- demo gif placeholder -->

## 核心功能

- **知识编译** — 三层编译 source → concept → entity。处理一次，query forever。

- **Context Recovery** — wiki 主动向你提问。`/interview` 从三个池子里挑问题：你最近没展开的观点（preference tagging 自动标记的）、概念页上的 open questions、薄弱页面和时间线空洞。`/bookmark-chat` 从旧书签和碎片笔记里恢复遗忘的 context。

- **Quick Thought** — `/thought` 一句话记下想法，立刻 interview 补 context。替代 Notion → 导出 → 编译 → 回顾的四步链路，一步到位。

- **Wiki Digest** — `/digest` 看今天 wiki 变了什么 + 一个推荐问题。`/digest week` 看一周。

- **混合搜索** — BM25 + 向量语义 + LLM re-ranking，通过 `qmd` 实现。

- **知识图谱** — Canvas 交互式图谱，5 种配色，搜索，detail panel。

- **Auto-Capture + Preference Tagging** — Stop hook 在每次 CC 对话结束时静默抓取个人 context 写入 wiki。同时检测你说的未展开判断和偏好，生成追问问题等下次 `/interview` 时用。你什么都不用做。

- **多源导入** — Notion、Claude/Gemini 对话、Twitter 书签、PDF、网页。`/wiki ingest` 一条命令。

## Skill 交互展示

### `/thought` — 想到什么，说一句就行

```
> /thought agent时代最大的杠杆是taste

💭 已记录

> 2026-04-09
> agent时代最大的杠杆是taste

当时的背景是什么？发生了什么让你写下这个？

> 今天在看几个开源agent框架，发现做得好的和做得差的
> 差距完全不在技术能力上，而是选择做什么、怎么组合

明白了。你说的taste不是审美，是"在agent能力爆炸的时代，
选择用这些能力做什么"的判断力。

展开一下？和你之前写的 taste与ambition 那个概念有什么区别？

> 那个更偏学术taste，这个是工程taste...
```

wiki 自动创建 `wiki/sources/thought-2026-04-09-agent时代最大的杠杆是taste.md`，interview 的回答写入 Context Recovery 段落，关联概念自动 cross-link。

### `/interview` — wiki 主动来找你聊

```
> /interview

我看了一下 wiki 的状态，有几个地方我很好奇想问你。

你昨天说"我觉得RLVR比SFT有前途多了"，但没有展开。
具体是指哪些场景下RLVR更有优势？是所有任务都适用，
还是特定类型的任务？

> 主要是reasoning类的任务，SFT容易overfitting到
> 表面pattern...

[静默更新 wiki/concepts/ai4ai.md, wiki/concepts/test-time-scaling.md]

有意思。那你觉得 agent 类任务呢？你之前在 FARS 上的
经验是偏向哪边的？
```

三个问题池按优先级混合：你最近没展开的偏好（自动标记的）→ 概念页上的 open questions → 薄弱页面。

### `/digest` — 今天 wiki 怎样了

```
> /digest

📊 Wiki 动态 (2026-04-09)

新增 (3)
- thought-2026-04-09-agent时代最大的杠杆是taste — 快速想法
- auto-2026-04-09-rlvr讨论 — 自动捕获
- concepts/工程taste — 新概念

更新 (2)
- concepts/taste与ambition — 新增工程taste维度
- concepts/ai4ai — 新增 RLVR vs SFT 讨论

推荐问题
> 你今天区分了"学术taste"和"工程taste"，
> wiki 里 [[concepts/科研路线选择]] 也有个 open question：
> "选方向时taste的权重应该多大？" 你怎么看？
```

## 实际规模

| 指标 | Demo 分支 |
|------|-----------|
| Raw sources | ~50 |
| Concepts | 15 |
| Entities | 10 |
| 图谱边数 | ~120 |
| 查询成本 | 读 2-3 个 md（不是全部 raw） |

## 快速开始

```bash
git clone https://github.com/freemty/selfOS
cd selfOS

# 体验 demo（真实脱敏数据）
git checkout demo
python viewer/app.py    # → localhost:5001

# 开始你自己的
git checkout main
./setup.sh              # 注册 skill + 可选 auto-capture hook
# 在 Claude Code 里：
/wiki init
/thought 我的第一个想法
```

### 命令速查

| 你想... | 命令 |
|---------|------|
| 记个想法 | `/thought <text>` |
| 让 wiki 问我 | `/interview` |
| 看 wiki 变化 | `/digest` |
| 导入 source | `/wiki ingest <url>` |
| 查知识 | `/wiki query "问题"` |
| 健康检查 | `/wiki lint` |

## 工作原理

```
raw/（你的数据）
  │
  ▼
/wiki ingest ──→ wiki/sources/   （每个 source 一份摘要）
                    │
                    ▼
               wiki/concepts/  （抽象概念，交叉引用）
               wiki/entities/  （人物、组织、工具）
                    │
                    ▼
               graph.json ──→ 交互式可视化
                    │
                    ▼
               /wiki query ──→ 带引用的回答
```

## 技术栈

[Claude Code](https://claude.ai/claude-code) skill system · HTML5 Canvas · [Flask](https://flask.palletsprojects.com/)

## License

[MIT](LICENSE)

---

# selfOS — Personal AI Knowledge OS

**Compile your notes, conversations, and bookmarks into a knowledge base that actually understands you.**

<!-- screenshot placeholder -->

[中文](#selfos) | [English](#selfos--personal-ai-knowledge-os)

## What is selfOS?

Most personal knowledge tools use RAG — re-reading raw files on every query, burning tokens, losing structure. selfOS does the opposite: **compile once, query forever**. Each source is processed once into a three-layer wiki (source → concept → entity) with cross-references and citations. After compilation, querying costs zero LLM tokens — just read 2-3 markdown files.

> Graphify turns code into graphs. selfOS turns **you** into a graph.

11 months of daily use. Real data.

<!-- demo gif placeholder -->

## Key Features

- **Knowledge Compilation** — Three-layer: source → concept → entity. Process once, query forever.

- **Context Recovery** — Your wiki interviews YOU. `/interview` pulls from three question pools: unexpanded opinions auto-tagged from recent sessions, open questions on concept pages, thin pages and timeline gaps. `/bookmark-chat` recovers forgotten context from old bookmarks and terse notes.

- **Quick Thought** — `/thought` captures a one-liner and immediately interviews you for context. Replaces the Notion → export → compile → review pipeline. One step.

- **Wiki Digest** — `/digest` shows today's wiki changes + a recommended question. `/digest week` for weekly review.

- **Hybrid Search** — BM25 + vector semantic + LLM re-ranking via `qmd`.

- **Knowledge Graph** — Interactive Canvas visualization with 5 color presets, search, and detail panel.

- **Auto-Capture + Preference Tagging** — Stop hook silently captures personal context from every Claude Code session. Also detects unexpanded judgments and preferences, queuing follow-up questions for your next `/interview`. Zero effort.

- **Multi-Source Ingest** — Notion, Claude/Gemini conversations, Twitter bookmarks, PDFs, web pages. One command: `/wiki ingest`.

## Skills in Action

### `/thought` — capture a fleeting idea

```
> /thought the biggest leverage in the agent era is taste

💭 Recorded

> 2026-04-09
> the biggest leverage in the agent era is taste

What was the context? What made you write this down?

> was looking at open source agent frameworks today,
> the gap between good and bad ones isn't technical ability,
> it's choosing what to build and how to compose

Got it. Your "taste" here isn't aesthetics — it's judgment about
what to do when agent capabilities are exploding.

Can you expand? How does this relate to the taste-and-ambition
concept you wrote about before?

> that was more about academic taste, this is engineering taste...
```

Wiki creates `wiki/sources/thought-...md`, interview answers go into Context Recovery, related concepts auto-link.

### `/interview` — your wiki comes to ask you questions

```
> /interview

I looked at the wiki's state. A few things I'm curious about.

Yesterday you said "RLVR is way more promising than SFT" but
didn't elaborate. Which scenarios specifically? All tasks,
or certain types?

> mainly reasoning tasks — SFT tends to overfit on
> surface patterns...

[silently updates wiki/concepts/ai4ai.md, wiki/concepts/test-time-scaling.md]

Interesting. What about agent tasks? Based on your FARS
experience, which side do you lean toward?
```

Three question pools mixed by priority: recent unexpanded opinions (auto-tagged) → open questions from concept pages → thin pages.

### `/digest` — what changed today

```
> /digest

📊 Wiki Activity (2026-04-09)

Added (3)
- thought-2026-04-09-biggest-leverage-is-taste — quick thought
- auto-2026-04-09-rlvr-discussion — auto-captured
- concepts/engineering-taste — new concept

Updated (2)
- concepts/taste-and-ambition — added engineering taste dimension
- concepts/ai4ai — added RLVR vs SFT discussion

Recommended question
> You distinguished "academic taste" from "engineering taste" today.
> [[concepts/research-direction]] has an open question:
> "How much weight should taste have when choosing directions?"
> What do you think?
```

## Scale

| Metric | Demo Branch |
|--------|-------------|
| Raw sources | ~50 |
| Concepts | 15 |
| Entities | 10 |
| Graph edges | ~120 |
| Query cost | Read 2-3 md files (not all raw) |

## Quick Start

```bash
git clone https://github.com/freemty/selfOS
cd selfOS

# Explore the demo (real sanitized data)
git checkout demo
python viewer/app.py    # → localhost:5001

# Start your own
git checkout main
./setup.sh              # Register skills + optional auto-capture hook
# In Claude Code:
/wiki init
/thought my first idea
```

### Commands at a Glance

| You want to... | Command |
|----------------|---------|
| Jot down a thought | `/thought <text>` |
| Let wiki interview you | `/interview` |
| Review wiki changes | `/digest` |
| Ingest a source | `/wiki ingest <url>` |
| Query knowledge | `/wiki query "question"` |
| Health check | `/wiki lint` |

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
               /wiki query ──→ Cited answers
```

## Built With

[Claude Code](https://claude.ai/claude-code) skill system · HTML5 Canvas · [Flask](https://flask.palletsprojects.com/)

## License

[MIT](LICENSE)
