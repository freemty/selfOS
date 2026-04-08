# selfOS Launch Design — "Personal AI OS" 开源发布计划

> 目标：4 天内将 selfOS 打造为可传播的开源项目，蹭 Graphify 热度窗口

## 背景

Graphify（4.6k stars，4 天）证明了"知识图谱 + AI coding"品类有市场。selfOS 在知识编译深度上超过 Graphify，但缺乏包装和可达性。本设计覆盖 repo 重构、可视化、README、传播策略四个维度。

## 品牌定位

- **名字**: selfOS
- **Tagline EN**: "Your personal AI operating system — compile your notes, conversations, and bookmarks into a queryable knowledge base that understands you"
- **Tagline CN**: "个人 AI 操作系统 — 将笔记、对话、书签编译成一个真正理解你的知识库"
- **差异化**: "Graphify turns code into graphs. selfOS turns YOU into a graph."
- **定位**: 与 Graphify 互补而非竞品 — "Graphify for code, selfOS for life"

## 目标用户

- **B**: 广义 Claude Code / AI coding 用户 — 任何想把文档变成可查询知识库的人
- **C**: 中文 AI 社区 — build in public，"个人 AI OS" 品牌传播

## 核心差异化（优先级）

1. **C — Personal AI OS**: 不只是工具，是完整的个人操作系统概念（LifeOS + wiki + context recovery + auto-capture）
2. **B — 被动 context 交付**: AI 主动提问补全遗忘 context — /interview, /bookmark-chat, /complete（Graphify 完全没有）
3. **A — 知识编译**: 不是 RAG，一次性编译成结构化 wiki，查询零 token 成本

## 设计 1：Repo 重构 + Branch 结构

### Branch 策略

| Branch | 内容 | Push |
|--------|------|------|
| `main` | 通用工具骨架（空 wiki/，完整 skill + 脚本 + viewer） | ✅ public |
| `demo` | 脱敏缩略版真实数据（~50 sources, ~15 concepts, ~10 entities） | ✅ public |
| 私有 branch | 完整个人数据（799 sources） | ❌ 不 push |

### main branch 目录结构

```
selfOS/
├── .claude/skills/selfos/            # 核心 skill
├── .claude/skills/selfos-completion/ # context recovery skill
├── scripts/                          # 工具脚本
├── viewer/                           # 可视化（vis.js 知识图谱）
├── raw/                              # 空，带 .gitkeep + README
├── wiki/                             # 空骨架 + 模板
│   ├── index.md                      # 空模板
│   ├── log.md
│   ├── overview.md
│   ├── concepts/.gitkeep
│   ├── entities/.gitkeep
│   ├── sources/.gitkeep
│   └── synthesis/.gitkeep
├── CLAUDE.md                         # 通用化版本
├── README.md                         # 中英双语
└── LICENSE                           # MIT
```

### demo branch 脱敏策略

从 799 sources 精选 ~50 条：
- **保留**: 研究方法论、技术概念、工具实践（build-in-public 内容）
- **脱敏**: 个人关系细节、情绪记录、具体人名用首字母替代
- **保留 concepts**: ~15 个（研究方向、方法论、工具相关）
- **保留 entities**: ~10 个（公开人物如 Ilya、公开机构如 Anthropic）

## 设计 2：知识图谱可视化

### 技术方案

替换当前空壳 viewer，基于 vis.js：

```
viewer/
├── app.py                  # Flask API
├── build_graph.py          # wiki frontmatter → graph.json
├── static/
│   ├── index.html          # 交互式知识图谱
│   ├── graph.js            # vis.js 渲染
│   └── style.css
```

### 节点类型 + 视觉映射

| 类型 | 颜色 | 大小规则 |
|------|------|---------|
| concept | 蓝 | 按 source_count 缩放 |
| entity-person | 橙 | 按被引用次数缩放 |
| entity-org | 绿 | 固定中等 |
| entity-tool | 紫 | 固定中等 |
| source | 灰 | 小，默认隐藏，hover 展示 |

### 边的生成（自动提取，无需手动标注）

1. **`[[wikilinks]]`** — 扫描 markdown 中的 `[[page]]` 引用 → 边
2. **frontmatter `sources`** — concept/entity 引用的 sources → concept↔source 边
3. **frontmatter `tags`** — 共享 tag 的 concepts → 弱边（虚线）

### 交互功能

- 搜索框：高亮节点 + 聚焦
- 点击节点：右侧面板显示 summary + 关联页面
- 社区过滤：按 tag 分组，切换显示/隐藏
- 拖拽 + 缩放
- hover：显示 title + one-line summary

## 设计 3：README 结构

中英双语，同一文件内切换（减少维护成本）。

### 英文部分结构

1. **Hero**: 项目名 + tagline + 知识图谱截图
2. **What is selfOS**: 一段话 — 不是 RAG，是编译
3. **Demo GIF**: 30s — ingest → 图谱更新 → query 回答
4. **Key Features**:
   - Knowledge Compilation（三层编译）
   - Context Recovery（被动 context 交付 — /interview, /bookmark-chat）
   - Hybrid Search（BM25 + 向量 + LLM re-ranking）
   - Knowledge Graph Visualization（vis.js 交互图）
   - Auto-Capture（对话结束自动捕获）
   - Multi-Source Ingest（Notion/Claude/Gemini/Twitter/PDF/网页）
5. **Worked Example**: demo branch 数据统计表
6. **Quick Start**: git clone → checkout demo → 查看 → checkout main → 开始
7. **How It Works**: 架构图
8. **vs Graphify**: 互补定位对比表
9. **Built With / License**

### 中文部分

同结构，标题下方 `[English](#selfos) | [中文](#selfos-个人-ai-操作系统)` 切换

## 设计 4：传播策略

### 发布时间线

| 时间 | 动作 |
|------|------|
| Day 1 | repo 重构 + demo branch + 脱敏数据 |
| Day 2 | 可视化 viewer（build_graph.py + vis.js） |
| Day 3 | README 中英双语 + 录 demo GIF/视频 |
| Day 4 上午 | Twitter/X 英文 thread（6-7 条推） |
| Day 4 下午 | 小红书/即刻/知乎中文帖 |
| Day 4 晚上 | HN Show HN + Reddit r/ClaudeAI + r/LocalLLaMA |
| Day 5-7 | 回复评论 + 根据反馈快速迭代 |
| Week 2+ | 如有 traction，做 pip 包 / 一键安装 |

### Twitter/X 英文 Thread（6 条推）

1. **Hook**: "I've been building a Personal AI OS for 11 months. It compiles my notes, AI conversations, and bookmarks into a knowledge base that understands me better than I do." + 知识图谱截图
2. **Problem**: "We have tools to understand codebases (shoutout @graphify). But who's building tools to understand yourself?"
3. **Solution**: "selfOS compiles them ONCE into a structured wiki. No RAG. No re-reading. Zero token cost per query." + ingest→query GIF
4. **Killer feature**: "The AI interviews YOU. It finds gaps in your knowledge base and asks questions to recover context you've forgotten. I call it Reverse DPO." + /interview GIF
5. **Stats**: "11 months of real usage: 800+ sources → 45 concepts, 27 entities. 3 data sources. One queryable graph of my intellectual life." + 全景截图
6. **CTA**: "Open source, MIT license. github.com/xxx/selfOS"

### 小红书/即刻 中文帖

- 标题："我用 Claude Code 搭了一个个人 AI 操作系统，跑了 11 个月"
- Hook → 痛点 → 方案 → 差异化（AI 反过来采访你）→ 截图 → CTA

### 蹭热度策略

- Twitter 正面提到 Graphify（"shoutout" 而非 "vs"），引导 retweet
- 定位互补 — "Graphify for code, selfOS for life"
- 如果 Graphify 作者回复/转发 = 最大传播加速器

## 分发策略（Phase 2，发布后根据反馈）

当前：先不管安装简化，手动 clone 即可。

Week 2+ 如有 traction：
- `pip install selfos && selfos init`
- 自动配好 Claude Code skill + hooks + 目录结构
- 多平台支持（Codex / OpenCode）

## 不做的事

- 不做 AST 代码解析（那是 Graphify 的领域）
- 不做 Neo4j / 重型图数据库（JSON + markdown 够用）
- 不做 embedding（qmd 已有）
- 不在 Day 1-4 做 pip 包
