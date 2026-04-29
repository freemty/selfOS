# selfOS 完整版全量编译设计

## 目标

将散落在 iCloud、Notion API、git history 中的 ~900 条原始素材全量编译进 wiki，形成完整的个人知识图谱。在当前 demo branch 基础上增量扩展，保留已有的 16 concepts + 14 entities + 6 条 Context Recovery。

## 数据源清单

| 数据源 | 位置 | 数量 | 格式 |
|--------|------|------|------|
| Gemini 对话 | `~/Library/Mobile Documents/.../gemini-all/` | 491 .md | YYYYMMDD_标题_hash.md |
| Claude 对话 | `~/Library/Mobile Documents/.../data-b2e261af-.../conversations.json` | 108 | JSON (需提取) |
| Notion Notes | Notion API, DB `2f6fa7bc-ecd5-80d4-a356-d2335226ffe5` | ~300+ | API 拉取 |
| **已有** | `wiki/sources/` (demo branch) | 70 | 已编译 |
| **合计** | | **~900** | |

## 架构

```
demo branch (基底)
├── raw/                          ← 导入全部原始素材 (不进 git)
│   ├── notion-notes/             ← ~300 条 (Notion API 批量拉取)
│   ├── gemini-conversations/     ← 491 条 (.md 从 iCloud 复制)
│   ├── claude-conversations/     ← 108 条 (从 JSON 提取为 .md)
│   └── exports/                  ← 已有 (conversations.json, memories.json)
├── wiki/
│   ├── sources/                  ← 70 → ~900 (全量编译)
│   ├── concepts/                 ← 16 → 30-50 (新素材涌现)
│   ├── entities/                 ← 14 → 25-40
│   ├── synthesis/                ← 保留 Context Recovery 等
│   ├── index.md                  ← 重建
│   ├── overview.md               ← 重建
│   └── log.md                    ← 追加
└── .gitignore                    ← 加入 raw/ 防止意外 push
```

## 编译策略：轻量优先 + richness 标记

### 第一遍：全量轻量编译

每条 source 只生成轻量页面：

```yaml
---
title: "对话/笔记标题"
type: source
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
tags: [auto-extracted-tags]
summary: "一句话摘要"
source_type: "gemini|claude|notion-Notes|notion-Thoughts|..."
richness: high|medium|low    # 新增字段
notion_id: "..."              # Notion 专用
---

# 标题

原文内容（Notion）或对话摘要（Gemini/Claude）
```

### richness 分级标准

| 等级 | 标准 | 后续处理 |
|------|------|----------|
| **high** | 包含独特判断、方向决策、人物评价、methodology 讨论、情绪爆发 | 优先深编译 |
| **medium** | 有实质技术讨论但属于学习/问答性质 | 按需深编译 |
| **low** | 纯翻译、格式转换、简单问答、无个人 insight | 不深编译 |

### 第二遍：按需深编译 (后续)

对 richness=high 的 source 增量扩充：
- Key Insights 段落
- Related Concepts 交叉引用
- 涌现新 concept/entity 页面

## 执行步骤

### Phase 1: 导入 raw (~5 min)

1. `.gitignore` 加入 `raw/` 规则
2. 从 iCloud 复制 Gemini 491 个 .md 到 `raw/gemini-conversations/`
3. 从 iCloud 复制 Claude JSON 到 `raw/claude-conversations/`，提取为独立 .md
4. 从 Notion API 批量拉取 Notes 到 `raw/notion-notes/`（分页遍历 DB，每页 100 条）

### Phase 2: 去重 (~2 min)

对比 raw/ 和现有 wiki/sources/：
- 按 source_type + 日期 + 标题模糊匹配
- 已有 70 条标记为 skip
- 输出待编译清单

### Phase 3: 批量编译 — 分批防 context 爆炸

**核心策略：每批 ≤50 条，每条独立编译，不在单个 agent context 中累积。**

#### Batch 处理流程

```
for each batch of 50 raw files:
    spawn subagent:
        for each file in batch:
            1. 读取 raw 文件 (≤2000 行)
            2. 提取: title, date, tags, summary, richness
            3. 写入 wiki/sources/<slug>.md (轻量格式)
            4. 收集 concept/entity 候选列表
        输出: 编译报告 (新 source 列表 + concept/entity 候选)
```

#### 批次分配

| Batch | 数据源 | 数量 | 预估批次 |
|-------|--------|------|----------|
| Notion | Notion API → raw → compile | ~300 | 6 批 x 50 |
| Gemini | iCloud .md → compile | ~487 (去重后) | 10 批 x 50 |
| Claude | JSON → extract → compile | ~92 (去重后) | 2 批 x 50 |
| **合计** | | **~879** | **18 批** |

#### Context 爆炸防护

- 每个 subagent 处理 ≤50 条后结束，释放 context
- 长对话（Gemini/Claude）只读前 500 行提取摘要，不全文载入
- 编译产出（wiki/sources/*.md）写入磁盘后不回传到 parent context
- 每批完成后 parent 只接收编译报告（~50 行），不接收原文

### Phase 4: Concept/Entity 网络扩展

编译完成后，汇总所有批次的 concept/entity 候选列表：

1. **保留锚点**：现有 16 concepts + 14 entities + 6 条 Context Recovery 不动
2. **去重合并**：候选列表中与现有概念重复的，更新现有页面的 sources 列表
3. **创建新页面**：出现 ≥3 次的新概念/实体，创建 wiki/concepts/ 或 wiki/entities/ 页面
4. **织入 cross-references**：新旧页面之间补充 `[[link]]`

### Phase 5: 重建 index + overview

- `wiki/index.md`：重新生成完整目录（~900 sources + 30-50 concepts + 25-40 entities）
- `wiki/overview.md`：基于扩展后的 concept 网络重写全局综述
- `wiki/log.md`：追加本次操作记录

## 关键约束

1. **Context Recovery 不能丢** — 今天的 6 条 thought writeback + concept 更新 + synthesis 全部保留为锚点
2. **raw/ 不进 git** — .gitignore 保护，避免 push 到 public repo
3. **幂等** — 已有 70 条 source 不重新编译，只补充缺失的 cross-references
4. **编译质量** — 每条 source 至少有准确的 title + date + tags + 一句话 summary + richness 标记
5. **可恢复** — 每批编译前 git commit，出错可回滚到上一批

## 产出

- `raw/`: ~900 条原始素材（本地，不进 git）
- `wiki/sources/`: ~900 条轻量编译页面
- `wiki/concepts/`: 30-50 个概念页面（含现有 16 个 + 新涌现）
- `wiki/entities/`: 25-40 个实体页面（含现有 14 个 + 新涌现）
- `wiki/index.md`: 完整目录
- `wiki/overview.md`: 全局综述
- Obsidian Graph View 从 ~100 节点 → ~1000 节点
