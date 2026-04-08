# LLM Wiki → Knowledge Graph: Scaling to 200K Papers

> 从个人 wiki 到通用知识图谱的架构演进设计

## 动机

当前 LLM Wiki 在个人知识管理场景下运行良好（~900 sources, 43 concepts, 27 entities）。但如果要扩展到学术文献体系（比如 20 万篇论文），核心瓶颈暴露：

**Ingest 一篇新 paper 的成本是 O(n) 还是 O(log n)？**

## 当前架构的复杂度分析

| 步骤 | 当前方案 | 复杂度 | 20万论文时的问题 |
|------|---------|--------|------------------|
| 找相关节点 | LLM 读 index.md | **O(n)** | index 55K 行，超出 context window |
| 语义匹配 | qmd search (BM25+向量) | **O(log n)** | 可扩展，不是瓶颈 |
| 更新节点 | LLM 读+写 concept 页 | **O(k)** | k 很小（5-20），可接受 |
| 维护链接 | LLM 在文本中加 `[[link]]` | **O(k²)** | k 小时可接受 |

**瓶颈在"找相关节点"步骤。** 20 万论文 → ~5000 concepts + ~50000 entities。LLM 在 55K 行 index 里精确找到 10 个相关条目，recall 会显著下降。

## 关键区分

- **新 paper → 找到所有相关 concepts** = 近似最近邻搜索 → qmd embedding 可以 O(log n)
- **新 paper → 精确判断和每个 concept 的关系类型** (extends/contradicts/uses...) = **真 O(n)**，需要逐一判断

## 降到 Sub-linear 的三个必要改进

### 1. 层级化 Index

当前 concepts 是平铺的（43 个同级）。需要改为树状：

```
ML
├── Generative Models
│   ├── Diffusion
│   │   ├── Score-based (DDPM, NCSN)
│   │   ├── Flow Matching (Rectified Flow, OT-CFM)
│   │   └── Noise Scheduling
│   ├── VAE
│   └── GAN
├── Transformer Architecture
│   ├── Attention Mechanisms
│   │   ├── RoPE / Position Encoding
│   │   ├── Attention Sink
│   │   └── Efficient Attention (FlashAttention, Ring)
│   └── Interpretability (SAE, Probing)
├── Agent / AI4AI
│   ├── Agent Training (RLHF, GRPO, Skill RL)
│   ├── Multi-Agent Systems
│   └── Automated Research (FARS, PostTrainBench)
└── ...
```

新 paper 先定位到 subtree（O(log n)），只在 subtree 内搜索关系（O(k)）。

### 2. Typed Edges

当前链接：`[[concepts/flow-matching]]`（无类型，只知道"有关系"）

需要改为有类型的有向边：

```yaml
# 在 concept 页 frontmatter 或专门的 relations 节中
relations:
  extends: ["concepts/ddpm", "concepts/score-sde"]
  contradicts: []
  uses_method: ["concepts/optimal-transport"]
  is_subtopic_of: ["concepts/generative-models"]
  related_to: ["concepts/noise-scheduling"]
```

支持的边类型：
- `extends` — 方法/思想的延伸
- `contradicts` — 矛盾或替代
- `uses_method` — 使用了某个方法
- `is_subtopic_of` — 层级从属
- `preceded_by` / `followed_by` — 时间先后
- `authored_by` — 论文→人
- `affiliated_with` — 人→机构

### 3. 图索引 (`_graph.json`)

不需要 Neo4j。一个 JSON 文件就够：

```json
{
  "nodes": {
    "concepts/flow-matching": {
      "type": "concept",
      "depth": 3,
      "parent": "concepts/generative-models",
      "source_count": 12,
      "last_updated": "2026-04-05"
    }
  },
  "edges": [
    {
      "from": "concepts/flow-matching",
      "to": "concepts/ddpm",
      "type": "extends",
      "sources": ["papers/lipman-2023-flow-matching"],
      "confidence": "high"
    }
  ]
}
```

Ingest 新 paper 时：
1. qmd embedding → 找到 top-10 相关 concepts（O(log n)）
2. 读 `_graph.json` 定位 subtree → 只在 subtree 内建立连接（O(k)）
3. 更新 `_graph.json` 的 edges（O(1) append）

## 预测能力

有了 typed edges + 时间戳，可以做：

| 预测类型 | 查询方式 | 数据基础 |
|----------|---------|---------|
| **热门方向检测** | 某 concept 近期被 `extends` 的频率上升 | edges 的 timestamp 分布 |
| **方法替代预测** | 某 method 被 3+ papers `contradicts` | contradicts 边的聚集 |
| **Gap 检测** | 某 subtree 近 6 个月没有新 paper | subtree 的 last_updated |
| **影响力评估** | 某 concept 的 incoming `extends` 边数 | in-degree of extends |
| **跨领域桥梁** | 两个 distant subtrees 之间出现 `uses_method` 边 | graph shortest path |

## 人类知识 = DAG 的建模

用户的直觉是对的：人类知识本质上是一个 DAG（有向无环图）。

- **有向**：知识有先后依赖（理解 Flow Matching 需要先理解 ODE/SDE）
- **无环**：（大致上）知识不会循环依赖
- **不是树**：一个 concept 可以有多个 parent（Flow Matching 既属于 Generative Models 也属于 Optimal Transport）

当前 wiki 的 `[[wikilinks]]` 已经在隐式地编码这个 DAG，但没有把它显式化。显式化之后：

1. **可以做 topological sort** — 按依赖顺序排列 concepts，自动生成学习路径
2. **可以做 reachability query** — "理解 X 需要先学什么？"
3. **可以做 gap detection** — DAG 中缺失的边 = 应该存在但还没被发现的关系
4. **可以做 temporal prediction** — DAG 的增长模式可以预测下一个热点区域

## 实现路径

### Phase 1: 给当前 wiki 加 typed edges（本周可做）
- 修改 concept 页 frontmatter，加 `relations:` 字段
- 写脚本从已有 `[[wikilinks]]` 自动推断边类型
- 生成 `_graph.json`

### Phase 2: 层级化 index（需要重新编译）
- 设计 concept taxonomy（可以让 LLM 从 43 个现有 concepts 推断）
- 在 index.md 中用树形结构替代平铺列表
- 让 ingest 先定位 subtree 再搜索

### Phase 3: 学术论文场景适配
- 设计 paper 专用的 source page 模板（含 citation graph、method、dataset）
- 集成 Semantic Scholar API 或 arXiv API 自动拉取论文元数据
- 批量 ingest pipeline（处理 .bib 文件或 paper 列表）

### Phase 4: 预测层
- 基于 `_graph.json` 做时序分析
- 热门方向检测、gap 检测、学习路径推荐
- 可视化：D3.js force-directed graph with temporal animation

## 与现有系统的关系

这不是重写，是在现有 wiki 上加层：

```
当前:  raw/ → sources/ → concepts/entities/ (flat, [[wikilinks]])
目标:  raw/ → sources/ → concepts/entities/ (typed edges, hierarchy)
                                    ↓
                              _graph.json (显式图索引)
                                    ↓
                            prediction / inference layer
```

Obsidian 视图不受影响（`[[wikilinks]]` 保留），但多了一个图查询的能力。
