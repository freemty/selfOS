---
name: de-ai
description: >-
  Strip AI-generated prose of its telltale patterns — overclaiming, hollow structure,
  bullet-point abuse, hedge stacking, and formulaic transitions. Language-agnostic:
  detects structural AI-ness, not just word-level tells. Output is clean neutral prose.
  Triggers: /de-ai, /去味, 去AI味, de-ai, strip AI, 去机器味.
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

# de-ai：去 AI 味

## 1. 定位

这个 skill 做**减法**：把 AI 生成文本中的机械感、虚假权威感、过度结构化去掉，留下干净中性的散文。

不加个人风格（那是 yuanboizer 的活），不精简到 slide 级别（那是 slides-voice 的活）。只做一件事：**让文本读起来像人写的，而不是 LLM 吐的**。

## 2. AI 味的本质

AI 味不是某几个词的问题。它是一组**结构性模式**的叠加：

### 2.1 定式（Formulaic Patterns）

LLM 有一套默认的文档骨架，不管写什么都往上套：

| 定式 | 表现 | 修复 |
|------|------|------|
| 三段式总结开场 | "在当今X快速发展的背景下，Y日益重要。本文将从A、B、C三个方面探讨……" | 删。直接讲第一个论点 |
| 镜像结尾 | 结尾把开头换了个说法重复一遍 | 删，或只保留最后一句有信息的断言 |
| 假提问 | "那么，X到底意味着什么？" 紧跟着自己回答 | 删问句，直接给答案 |
| 按数字列举 | 永远"三个关键因素""五个核心要素" | 如果真是N个就保留数字，但删"核心/关键/重要" |
| 递进堆砌 | "不仅……更……""不仅仅是X，更是Y" | 挑一个最强的说，删另一个 |
| 总分总 | 开头说"下面讨论N点"，结尾"综上所述" | 删框架性的元叙述，保留内容 |

### 2.2 过度表达（Overclaiming）

AI 倾向于用最大号的词修饰最普通的事：

| 杀掉 | 替换为 |
|------|--------|
| 深刻/深入/深度 | （删，或说具体在哪里深） |
| 全面/系统/完整 | （删，或说具体覆盖了什么） |
| 重要/关键/核心/至关重要 | （删——如果真重要，内容会自己说明） |
| 显著/大幅/根本性 | 给数字，或降级为"明显" |
| 独特/创新/突破性 | （删——读者判断） |
| comprehensive/crucial/fundamental/groundbreaking | delete or quantify |
| transformative/paradigm-shifting/revolutionary | delete |
| delve/leverage/utilize/elucidate | dig into / use / use / explain |
| nuanced/multifaceted/holistic | （delete — say what's actually complex） |

**原则**：如果删掉形容词/副词之后句意不变，就删。

### 2.3 Bullet Point 滥用

AI 有 bullet-point 强迫症。并非所有并列关系都需要 list：

**检测**：
- 3+ bullet points 每个只有一句话，且彼此没有并列关系 → 改写成段落
- Bullet 开头是 "Firstly" / "Moreover" / "Additionally" → 纯 AI 味转折
- 嵌套 bullet（二级三级）→ 除非是真正的层级数据，否则扁平化或改段落

**保留 bullet 的条件**：
- 真正的清单（步骤、配料、选项）
- 元素间没有因果关系，只是并列枚举
- 读者需要快速扫描定位

### 2.4 Hedge Stacking（对冲堆叠）

AI 怕说错，所以在每个判断前后加满对冲：

- "it's worth noting that" / "值得注意的是"
- "it's important to recognize" / "需要认识到"
- "while this is not always the case" / "尽管不能一概而论"
- "this may vary depending on context" / "具体情况可能有所不同"

**修复**：一段话最多保留一个 hedge。如果论点本身有限定条件（"在X情况下"），那就是 hedge 了，不需要额外加。

### 2.5 假连贯（Pseudo-Coherence）

AI 用连接词制造逻辑感，但实际上句子之间没有真正的逻辑推进：

| 假连贯标志 | 检测方法 |
|-----------|---------|
| Furthermore / Moreover / Additionally | 删掉连接词后两句话依然独立——说明是假连贯 |
| This demonstrates / This highlights | 上一句已经 demonstrate/highlight 了，这是元叙述 |
| Building on this / In light of this | 检查"this"到底指什么——如果指的就是上一句，删 |
| 由此可见 / 综上所述 / 换言之 | 如果下一句没有新信息，整句删 |

### 2.6 模板化段落结构

AI 段落有一个默认结构：topic sentence → elaboration → example → so-what。四步走。

**人写的段落**不遵守这个结构。它可能：
- 先给例子再给论点
- 两句话说完不需要 so-what
- 一句话就是一段

**修复**：如果每段都是 4-5 句且结构相同 → 打乱。有些段落合并，有些拆成短段，有些删掉 so-what 尾句。

## 3. 处理流程

1. **扫描**：逐段标注 AI 味类型（定式/overclaim/bullet滥用/hedge/假连贯/模板段落）
2. **改写**：对每个标注点做最小修改——删 > 缩 > 换
3. **整体节奏**：检查改完后的文本，段落长短是否有变化（不能全是3-4句齐整段落）
4. **输出**：改写后的全文 + 修改摘要

## 4. 修改原则

- **最小干预**：能删一个词解决的不改整句，能改一句的不重写一段
- **保留信息**：只砍表达方式，不砍内容。如果一句话有独特信息，保留信息，改表达
- **不加东西**：不加类比、不加例子、不加个人风格。只做减法
- **尊重原文结构意图**：如果作者真的想用 list（比如步骤），保留 list

## 5. 输出格式

```markdown
[改写后的全文]

---

## 修改摘要

- 总计：删除 N 处 overclaim，修复 M 处定式，N 处 bullet 改段落
- 典型修改：
  - "在当今AI快速发展的时代……" → （整段删除，直接从第一个论点开始）
  - "这一发现具有深远的意义" → "这说明X会导致Y"
  - 5-bullet list → 2 段散文
```

## 6. 不动的东西

- 专有名词、术语、模型名、数字——原样
- 作者的核心论点和立场——原样
- 引用和出处——原样
- 合理使用的 list（真正的步骤/枚举）——原样
- 代码块——原样

## 7. 语言适配

根据输入语言自动切换检测规则：

- **中文输入**：检测 2.1-2.6 中的中文模式
- **英文输入**：检测 2.1-2.6 中的英文模式
- **中英混合**：两套规则都用，但保留原文的中英比例
