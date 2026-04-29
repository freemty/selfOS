# Obsidian 社区插件调研 — selfOS LLM Wiki 场景

**日期:** 2026-04-07
**场景:** LLM-maintained personal knowledge base，~66 sources / 15 concepts / 10 entities，YAML frontmatter + wikilinks + typed edges 升级中

---

## 总览：安装优先级

| 优先级 | 插件 | 方向 | 一句话理由 |
|--------|------|------|-----------|
| **P0** | Dataview | 结构化查询 | wiki 有完整 frontmatter，不装等于浪费一半元数据 |
| **P0** | Templater | 模板系统 | 标准化 concept/entity/source 页面创建 |
| **P0** | Linter | Frontmatter 校验 | 自动格式化 YAML，防止 LLM 生成的 frontmatter 格式漂移 |
| **P1** | Breadcrumbs | Typed edges | 正在升级到 typed edges，这是唯一成熟的 typed links 方案 |
| **P1** | Extended Graph | Graph 增强 | 核心 Graph View 的直接增强，支持 typed link 过滤 |
| **P1** | Tag Wrangler | Tag 管理 | 91 万下载，tag 重命名/合并的事实标准 |
| **P1** | Omnisearch | 搜索增强 | BM25 搜索，比核心搜索强很多 |
| **P2** | Marp Slides | 幻灯片 | 按需使用，不影响知识库核心流程 |
| **P2** | Strange New Worlds | Backlink 增强 | 好用但非必需，核心 backlinks 够用 |
| **P2** | Graph Analysis | 图算法 | Co-citation / 社区检测，20 万论文规模时才真正有价值 |
| **P2** | Smart Connections | 语义搜索 | 已有 qmd 做向量搜索，功能重叠 |
| **P2** | Metadata Menu | 元数据编辑 | Dataview 已覆盖查询需求，这个偏 GUI 编辑 |

---

## 一、结构化查询：Dataview [P0]

**插件名:** Dataview
**GitHub:** https://github.com/blacksmithgu/obsidian-dataview
**下载量:** ~4M+ | **Stars:** 8.7k | **最新版:** 0.5.70 (2025-04-07)

### 核心功能
把 Obsidian vault 当数据库查询——支持 DQL (Dataview Query Language)、inline 表达式、DataviewJS (完整 JS API) 四种模式。

### 对 selfOS 的具体价值

1. **索引页自动生成** — 替代手动维护的 `wiki/index.md`:
   ```dataview
   TABLE summary, updated, tags
   FROM "wiki/concepts"
   SORT updated DESC
   ```

2. **跨类型关联查询** — 找出引用某 source 的所有 concept:
   ```dataview
   LIST
   FROM "wiki/concepts"
   WHERE contains(sources, "source-slug")
   ```

3. **健康检查** — `/wiki lint` 的可视化版本:
   ```dataview
   LIST
   FROM "wiki"
   WHERE !title OR !type OR !summary
   ```

4. **Timeline 视图** — 按时间线浏览知识积累:
   ```dataview
   TABLE title, type, created
   FROM "wiki"
   SORT created ASC
   ```

### 注意事项
- DQL 查询是沙盒的，安全；DataviewJS 有完整文件系统访问权限，慎用
- 大量 DataviewJS 查询会拖慢打开速度——优先用 DQL
- 与 Templater 配合极好，可以在模板中嵌入 Dataview 查询
- 20 万页面规模下性能未知，需要实测（社区报告 5k+ 笔记仍流畅）

---

## 二、模板系统：Templater [P0]

**插件名:** Templater
**GitHub:** https://github.com/SilentVoid13/Templater
**下载量:** ~3.9M | **Stars:** 4.8k | **最新版:** 2.18.1 (2026-01-29)

### 核心功能
模板语言引擎——支持变量插入、JS 执行、系统命令调用，远超 Obsidian 内置模板。

### 对 selfOS 的具体价值

为四种页面类型创建标准模板：

**concept 模板示例:**
```markdown
---
title: "<% tp.file.title %>"
type: concept
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
sources: []
tags: []
summary: ""
---

# <% tp.file.title %>

## Core Idea

## Key Arguments

## Connections
```

**好处:**
- LLM 生成页面时 frontmatter 格式一致性有模板兜底
- 手动创建页面时一键生成规范结构
- 可配合文件夹触发：在 `wiki/concepts/` 新建文件自动套用 concept 模板

### 注意事项
- 模板文件建议放在 `templates/` 目录，在 Templater 设置中指定
- 文件夹模板（Folder Templates）功能是核心卖点——按目录自动匹配模板
- 与 Dataview 配合良好，模板中可以嵌入 DQL 查询
- 系统命令执行功能默认关闭，按需开启

---

## 三、Frontmatter 校验与格式化：Linter [P0]

**插件名:** Linter
**GitHub:** https://github.com/platers/obsidian-linter
**下载量:** 852,518 | **最新版:** 1.31.2 (2026-03-04)

### 核心功能
自动格式化 Markdown + YAML frontmatter——支持保存时自动修复、批量处理。

### 对 selfOS 的具体价值

1. **YAML frontmatter 规范化:**
   - 自动排序 frontmatter 字段（title -> type -> created -> updated -> sources -> tags -> summary）
   - 强制 YAML 数组格式一致（`["a", "b"]` vs `- a\n- b`）
   - 自动更新 `updated` 时间戳

2. **LLM 输出质量兜底:**
   - LLM 生成的页面偶尔 YAML 格式不规范（引号遗漏、缩进错误）
   - Linter 保存时自动修复，避免 Dataview 查询因格式问题失败

3. **批量修复:**
   - 可对整个 vault 执行 lint，一次性修复所有格式问题
   - 对现有 66+ sources 做格式统一非常有用

### 注意事项
- 规则非常多（100+），建议只开启需要的，避免过度格式化
- `updated` 字段自动更新功能可能与 LLM 写入冲突——如果 LLM 已经设置了正确的 updated，Linter 再改一次可能不符合预期。建议：用 Linter 的 `Update time on edit` 规则，或者禁用这个规则交给 LLM 管理
- 首次对全 vault lint 之前做 git commit，方便回滚

---

## 四、Typed Edges 核心：Breadcrumbs [P1]

**插件名:** Breadcrumbs
**GitHub:** https://github.com/SkepticMystic/breadcrumbs
**下载量:** 264,632 | **Stars:** 755 | **最新版:** 4.4.4 (2026-03-29)

### 核心功能
为笔记间链接添加类型（typed links），支持层级导航、矩阵视图、面包屑路径。v4 完全重写，架构更现代。

### 对 selfOS 的具体价值

这是你 **typed edges 升级方案的核心插件**。当前 selfOS 正从 flat wikilinks 升级到 typed edges（extends, contradicts, uses_method 等），Breadcrumbs 是 Obsidian 生态中唯一成熟的 typed links 解决方案。

**使用方式:**
在 frontmatter 中定义关系：
```yaml
relations:
  extends: [[concepts/agent-scaling]]
  contradicts: [[concepts/xxx]]
  uses_method: [[entities/fars]]
```

Breadcrumbs 读取这些字段，构建 typed graph，提供：
- 面包屑导航（当前页在层级中的位置）
- 矩阵视图（查看某个节点的所有 typed 关系）
- 树形视图（沿某种关系类型展开）

**与 Juggl 的关系:**
- Breadcrumbs 定义关系 + 导航，Juggl 做可视化渲染
- 两者有深度集成，可以在 Juggl 图中显示 Breadcrumbs 定义的 typed edges
- 但 Juggl 最后更新是 2023-11，维护状态不确定
- **建议:** 先装 Breadcrumbs，typed edges 可视化用 Extended Graph 替代 Juggl

### 注意事项
- v4 是完全重写，与 v3 配置不兼容。如果看到旧教程注意版本
- 需要在设置中定义你的关系类型（extends, contradicts, uses_method 等）
- 与 Dataview 可以互补：Breadcrumbs 管关系，Dataview 做查询
- 17 个 open issues，但维护活跃（2026-03-29 最新提交）

---

## 五、Graph 增强：Extended Graph [P1]

**插件名:** Extended Graph
**GitHub:** https://github.com/ElsaTam/obsidian-extended-graph
**下载量:** 44,210 | **Stars:** 180 | **最新版:** 2.7.7 (2025-10-17)

### 核心功能
增强 Obsidian 核心 Graph View——节点图片/自定义形状、按 tag/property 过滤、typed link 过滤、多视图切换、SVG 导出。

### 对 selfOS 的具体价值

1. **按 type 属性分组渲染:**
   - concepts = 蓝色圆形, entities = 橙色方形, sources = 灰色小点
   - 比核心 Graph View 的纯颜色分组更丰富

2. **Typed link 过滤:**
   - 只显示 `extends` 关系、只显示 `contradicts` 关系
   - 在 20 万论文规模下，这种过滤是刚需

3. **多视图保存:**
   - 保存不同配置的 graph 视图（"概念层级图"、"实体关系图"、"源文献网络"）

4. **SVG 导出:**
   - 导出知识图谱用于 build-in-public 分享

### 与其他 Graph 插件的比较

| 插件 | 下载量 | 最后更新 | 核心卖点 | 推荐度 |
|------|--------|---------|---------|--------|
| **Extended Graph** | 44k | 2025-10 | 核心 Graph View 增强，typed link 过滤 | **推荐** |
| **Juggl** | 116k | 2023-11 | 独立交互图，最强可视化，但维护停滞 | 观望 |
| **Graph Analysis** | 65k | 活跃 | 图算法（co-citation, 社区检测） | 大规模时再装 |
| **Neo4j Graph View** | 11k | - | 导出到 Neo4j 做专业图查询 | 20 万论文时考虑 |
| **InfraNodus** | 16k | - | 3D 图 + AI 分析 | 酷但非必需 |

### 注意事项
- **不支持移动端**
- 有已知的设置丢失风险（异常关闭时）——建议 graph 配置做 git 版本控制
- 快速交互可能触发异步错误——大 vault 中避免频繁切换视图
- 与 Breadcrumbs 的 typed links 数据可以配合显示

---

## 六、Tag 管理：Tag Wrangler [P1]

**插件名:** Tag Wrangler
**GitHub:** https://github.com/pjeby/tag-wrangler
**下载量:** 918,943 | **最新版:** 0.6.0

### 核心功能
从 tag pane 右键菜单批量重命名、合并、搜索 tags，支持层级 tag。

### 对 selfOS 的具体价值

1. **Tag 演化管理:**
   - 初期 tag 命名不一致（如 `agent` vs `agents` vs `agent-scaling`）
   - Tag Wrangler 可以全 vault 批量重命名/合并
   
2. **层级 tag 浏览:**
   - 如 `#research/agent`, `#research/scaling`, `#person/researcher`
   - 展开/折叠层级 tag 结构

3. **Tag 页面:**
   - Alt+Click tag 自动创建/打开对应页面
   - 可以为每个核心 tag 维护一个说明页

### 注意事项
- 不支持 Obsidian Canvas 文件中的 tag
- 重命名是全局操作，会修改文件内容——操作前确保 git 已提交
- 纯管理工具，不做可视化——可视化用核心 Tag pane 或 Tags Routes 插件

---

## 七、搜索增强：Omnisearch [P1]

**插件名:** Omnisearch
**GitHub:** https://github.com/scambier/obsidian-omnisearch
**下载量:** 大量 | **Stars:** 1.9k | **最新版:** 1.28.2 (2026-02-28)

### 核心功能
基于 BM25 算法的全文搜索引擎——智能评分、容错、支持 PDF/Office/图片（需 Text Extractor）。

### 对 selfOS 的具体价值

1. **比核心搜索更智能:**
   - BM25 评分 > 简单字符串匹配
   - 容错搜索（typo-resistant）

2. **键盘优先:**
   - 不需要鼠标，搜索结果中直接插入 `[[link]]`
   - 符合 LLM wiki 的快速导航需求

3. **与 qmd 互补:**
   - qmd 是命令行搜索工具（BM25 + 向量）
   - Omnisearch 是 Obsidian 内的搜索体验增强
   - 不冲突，场景不同

### 注意事项
- **中文支持需要额外插件** — 这对 selfOS 是重要限制，wiki 内容大量中文
- PDF 索引需要安装 Text Extractor 插件
- 与 Smart Connections 不同：Omnisearch 是关键词搜索（BM25），Smart Connections 是向量语义搜索
- 建议先测试中文搜索效果，如果不佳可能需要等中文支持插件成熟

---

## 八、幻灯片：Marp Slides [P2]

**插件名:** Marp Slides
**GitHub:** https://github.com/samuele-cozzi/obsidian-marp-slides
**下载量:** 33,827 | **Stars:** 192 | **最新版:** 0.45.6 (2024-05-08)

### 核心功能
在 Obsidian 中用 Marp 写 Markdown 幻灯片——预览、导出 HTML/PDF/PPTX。

### 对 selfOS 的具体价值
- 用 wiki 中的知识直接生成演示文稿
- build-in-public 分享时可以快速出 slides
- 导出 PDF 用于学术汇报

### 注意事项
- **不支持 wikilinks** `[[]]` — 这是核心限制，需要用标准 Markdown 链接
- 非 HTML 导出需要 Chrome/Chromium/Edge
- 移动端 alpha 阶段
- 另一个替代品：JichouP 的 Marp 插件（15k 下载），功能类似但下载量更少

---

## 九、Backlink 增强：Strange New Worlds [P2]

**插件名:** Strange New Worlds (SNW)
**GitHub:** https://github.com/TfTHacker/obsidian42-strange-new-worlds
**下载量:** 118,541 | **Stars:** 554 | **最新版:** 2.3.7 (2026-04-04)

### 核心功能
在编辑器中直接显示链接/块引用/嵌入的引用计数，点击查看详情。

### 对 selfOS 的具体价值
- 写作时立即看到某个 concept 被引用了多少次
- 快速发现高连接度节点（核心概念）和孤立节点（需要丰富的页面）
- 与 `/wiki lint` 的孤页检测互补

### 注意事项
- 轻量级插件，性能影响小
- 是"好用"而非"必需"——核心 backlinks 面板已有类似功能
- 维护活跃（2026-04-04 最新发布）

---

## 十、图算法：Graph Analysis [P2]

**插件名:** Graph Analysis
**GitHub:** https://github.com/SkepticMystic/graph-analysis
**下载量:** 65,014

### 核心功能
四种图算法：Co-Citations（共引分析）、Similarity（Jaccard 相似度）、Link Prediction（链接预测）、Community Detection（社区检测）。

### 对 selfOS 的具体价值
- **Co-Citations:** 找出经常一起被引用但没有直接链接的笔记——发现隐藏关联
- **Link Prediction:** 建议应该建立但尚未建立的链接——对 LLM wiki 扩展有价值
- **Community Detection:** 自动发现概念聚类——20 万论文时非常有用

### 注意事项
- 当前 91 个页面规模，图算法价值有限
- 扩展到 20 万论文的学术知识图谱时，这个插件会成为核心工具
- 与 Breadcrumbs 同作者（SkepticMystic），兼容性好
- 建议 P2 阶段安装，等知识图谱规模上去再用

---

## 十一、语义搜索：Smart Connections [P2]

**插件名:** Smart Connections
**GitHub:** https://github.com/brianpetro/obsidian-smart-connections
**下载量:** 877,965 | **Stars:** ~2k

### 核心功能
本地向量嵌入 + 语义搜索——写作时自动推荐相关笔记，零配置本地模型。

### 对 selfOS 的具体价值
- 写作时自动发现语义相关的笔记
- 不需要 API key，本地运行

### 注意事项
- **与 qmd 的 vsearch 功能高度重叠** — qmd 已提供向量语义搜索
- 本地嵌入模型的中文效果未知
- 87 万下载但社区口碑参差——一些用户报告性能问题
- **建议：** 已有 qmd 的情况下，Smart Connections 优先级低

---

## 十二、元数据 GUI 编辑：Metadata Menu [P2]

**插件名:** Metadata Menu
**GitHub:** https://github.com/mdelobelle/metadatamenu
**下载量:** ~50k+ | **Stars:** 682 | **最新版:** 0.8.12 (2026-02-11)

### 核心功能
右键菜单编辑 frontmatter/inline 字段，支持 20+ 字段类型，fileClass 定义预设值。

### 对 selfOS 的具体价值
- 可以为 concept/entity/source/synthesis 定义不同的 fileClass
- 每种类型有不同的字段预设（如 entity 的 type 字段只能选 person/org/tool）
- 在 Dataview 表格中直接编辑 metadata

### 注意事项
- 维护者精力有限（"I unfortunately can't dedicate much time anymore"）
- 对 LLM wiki 而言，frontmatter 主要由 LLM 生成，GUI 编辑需求不高
- 如果发现手动调整 metadata 频繁，再考虑安装
- 功能与 Dataview 有重叠（查询方面），但编辑方面是独特的

---

## 推荐安装顺序

### 第一批（立即安装）
1. **Dataview** — 解锁 frontmatter 查询能力
2. **Templater** — 标准化页面创建流程
3. **Linter** — 自动修复 YAML 格式问题

### 第二批（typed edges 升级时安装）
4. **Breadcrumbs** — 定义和导航 typed relations
5. **Extended Graph** — 可视化 typed links

### 第三批（日常使用中按需安装）
6. **Tag Wrangler** — tag 重命名/合并
7. **Omnisearch** — 搜索增强（先测试中文效果）

### 第四批（规模扩展时安装）
8. **Graph Analysis** — 20 万论文规模的图算法
9. **Marp Slides** — 演示需求时
10. **Strange New Worlds** — backlink 增强

---

## 特别提醒

### 对 20 万论文规模的考量
当前 Obsidian 社区的性能上限大约在 5k-10k 笔记。20 万论文的学术知识图谱 **不应该全部放在 Obsidian vault 中**。建议架构：

- **Obsidian vault:** 核心知识图谱（concepts + entities + key papers，~1k-5k 页面）
- **外部数据库:** 20 万论文的全量数据（SQLite / Neo4j / Qdrant）
- **桥接层:** qmd 或类似工具连接两层

这意味着 Graph Analysis 和 Neo4j Graph View 等插件在 "全量图谱" 场景下可能需要外部工具替代，而非 Obsidian 插件。

### LLM 写入兼容性
LLM（Claude Code）直接写入 wiki/ 文件。以下插件可能与 LLM 写入冲突：
- **Linter** 的 `updated` 字段自动更新——建议禁用，由 LLM 管理
- **Metadata Menu** 的 fileClass 约束——如果 LLM 生成的字段不符合预设值会报错
- **Templater** 的文件夹模板——LLM 创建文件时不会触发 Templater，这是正常的

### 中文支持
- **Omnisearch** 需要额外中文插件
- **Smart Connections** 本地模型的中文嵌入质量未知
- **Dataview** 完全支持中文内容查询
- **Tag Wrangler** 支持中文 tag
