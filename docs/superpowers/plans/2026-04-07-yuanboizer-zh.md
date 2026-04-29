# yuanboizer-zh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a personal style polishing skill that rewrites Yuanbo's drafts into readable text while preserving his voice.

**Architecture:** Single skill with two files — SKILL.md (rules + flow + scoring) and examples.md (real before→after pairs from selfOS). Lives in yuanbo-skills repo alongside flipradio-write/polish.

**Tech Stack:** Claude Code skill (markdown-only, no code dependencies)

---

### Task 1: Create examples.md with real before→after pairs

**Files:**
- Create: `/Users/sum_young/code/projects/yuanbo-skills/yuanboizer-zh/examples.md`

- [ ] **Step 1: Create the examples file with 4 pairs (2 oral + 2 structured)**

Write the file with this exact content. The before texts are real Notion thoughts from selfOS; the after texts are hand-crafted rewrites that demonstrate the target style.

```markdown
# yuanboizer-zh 示例对

SKILL.md 引用此文件。每组示例展示：输入（渊博的压缩草稿）→ 输出（展开为可读文本，保留渊博的声音）。

---

## 口语帖示例

### 示例 1：Failure Case 的价值

**输入：**
> failure case是最宝贵的事情，他打破你简单的直觉，也提供了一个anchor强迫你深入，修正直觉，进而做出真正solid的工作

**输出：**
> 做研究这么久，我越来越觉得 failure case 才是最值钱的东西。
>
> 你本来觉得 A 导致 B，挺自洽的——然后一个 failure case 砸过来，告诉你不是这么回事。这个时候你的第一反应可能是烦，但其实它给了你一个极其具体的 anchor：不是"大概哪里有问题"，而是"就是这个 case 告诉我问题在哪"。
>
> 从这个 anchor 出发的深入分析，才是真正 solid 的工作的起点。Sink/RoPE 的研究就是这样——那些"不该出现却出现了"的现象，反而推动了对 attention 机制更深层的理解。
>
> 所以别嫌 failure case 烦。它打破直觉、提供锚点、强迫深入——这三件事比十个"符合预期"的实验结果都有价值。

### 示例 2：Scaling Law 反思

**输入：**
> 不要用所谓scaling law这样的宏大叙事来抹杀细微insight的价值 → 所谓Scaling Law是无数天才研究人员用尽自己智力铺就的curve，不是一个天然存在的物理定律

**输出：**
> 最近总看到有人拿 Scaling Law 当万能解释——"反正堆算力就行了"。这话听着就来气。
>
> Scaling Law 那条 curve 看着光滑，但 curve 上的每个点都是某个研究者用具体的 insight 手动放上去的。没有 KV-cache 优化就没有长上下文，没有 Flash Attention 就没有高效训练，没有 RoPE 就没有可泛化的位置编码。哪一个是"堆算力"堆出来的？
>
> 说到底，Scaling Law 不是物理定律，它不会自动延伸。拿宏大叙事来抹杀这些细微 insight 的价值，是对真正做事的人的不尊重。

---

## 结构化文章示例

### 示例 3：形式倒逼行动力

**输入：**
> 这两年在科研方面获得的最重要应用经验：要用形式倒逼行动力和内容迭代，fake it until make it
>
> - 先搭slides框架再填内容
> - TISI revision拖了两个月认真写一天就写完了 → 还是不能畏难
> - 告诉Jun组要讲CC实践 → 逼自己准备
> - Notion的空database template也是形式倒逼

**输出：**
> ### 形式倒逼行动力
>
> 这两年做科研，我觉得学到的最管用的一招就是：fake it until make it——用形式倒逼行动力。
>
> 什么意思呢？就是别等想清楚了再动手。先把 slides 框架搭出来，先把 paper 的 section headings 写上，先跟别人说"我下周讲一个 CC 实践的分享"。形式一旦存在，它就会逼着你往里填内容。
>
> 最典型的例子：TISI 那篇 revision 我拖了整整两个月，真正坐下来认真写，一天就搞完了。两个月 vs 一天——差的不是能力也不是时间，是心理门槛。形式（deadline 的逼近）打破了这个门槛。
>
> 这个方法论其实到处都在起作用：
> - **Build in public** 就是最强的形式——你公开承诺了，就必须交付
> - **Notion 的空 database template** 也是形式——它在那里等着被填充，你看着空格就手痒
> - **先做出来哪怕粗糙** 比"想清楚了再动手"强一万倍——飞轮得先转起来
>
> 说白了，大部分拖延不是能力问题，是畏难。形式就是打破畏难的锤子。

### 示例 4：自信的来源

**输入：**
> 我为什么自信 → 因为我深知从杭电到海宁到yiyi这里，我走过的距离已经比之后从zju到Michigan，从Michigan到mit到openai都要远了，成为ilya又有什么不可能的呢
>
> - 对困难的蔑视和具体做事的踏实 → 魅力的来源
> - 但也有自卑：抗拒给陌生人发邮件reachout → 底层是把自己和善于reachout的人比较
> - "要直面自己的自卑与一点点的羡慕嫉妒，明明白白的学"
> - hhhh我的宽容也是假的

**输出：**
> ### 我为什么自信
>
> 有时候别人问我怎么能这么自信，我的答案其实很简单：看看自己走过的距离。
>
> 从杭电到海宁到 yiyi 老师这里，这段路的长度和难度，比从浙大到 Michigan、从 Michigan 到 MIT 到 OpenAI 都要远得多。既然这段最难的路已经走过来了，成为 Ilya 又有什么不可能的呢？
>
> 我觉得真正有魅力的状态是这样的：对困难有一种蔑视感，但做具体事情的时候又极其踏实。不是盲目的"我最牛"，而是"我知道这有多难，但我不怕"。
>
> ### 但也得说说自卑
>
> 自信和自卑在我身上不是二选一，它们同时存在。比如我发现自己特别抗拒给陌生人发邮件 reachout——挖到底层，其实是在把自己和那些善于社交的人比较，觉得自己没有拿得出手的代表作。
>
> 蒸馏何泰然的时候我跟自己说了一句话："要直面自己的自卑与一点点的羡慕嫉妒，明明白白的学。"不是否认嫉妒，不是合理化嫉妒，而是承认它、然后把它转化成精确的学习方向。
>
> hhhh 说到底我的宽容也是假的——自己谦虚自嘲没问题，别人要是顺杆爬，面部表情马上就管理不住了。
```

- [ ] **Step 2: Verify file was created**

Run: `ls -la /Users/sum_young/code/projects/yuanbo-skills/yuanboizer-zh/examples.md`
Expected: file exists, ~4KB

- [ ] **Step 3: Commit**

```bash
cd /Users/sum_young/code/projects/yuanbo-skills
git add yuanboizer-zh/examples.md
git commit -m "feat(yuanboizer-zh): add before→after example pairs from selfOS"
```

---

### Task 2: Create SKILL.md main file

**Files:**
- Create: `/Users/sum_young/code/projects/yuanbo-skills/yuanboizer-zh/SKILL.md`

- [ ] **Step 1: Write the complete SKILL.md**

```markdown
---
name: yuanboizer-zh
description: |
  个人风格润色 skill。将渊博的草稿（Notion thoughts、微信、小红书、笔记）
  改写为"像渊博写的、别人能读懂"的文本。保留思维内核（中英嵌套、跨域类比、
  情感极性），展开压缩句为可读形态。自动判断语域（口语帖/结构化文章）。
  触发词：润色、yuanboize、帮我改改、改成小红书。
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

# yuanboizer-zh：渊博风格润色

## 1. 你的角色

你是渊博的个人文字编辑。你的工作不是"写得更好"，而是"写得像渊博，但别人也能读懂"。

核心原则：
- 保留渊博的声音，展开他的压缩
- 原文的观点和情绪是圣经，不改立场
- 不添加原文没有的信息或类比（除非用户要求）

## 2. 风格维度

### 2.1 中英嵌套

概念性词汇保留英文，叙事和情绪用中文。英文词以词/短语形式嵌入，不写完整英文句子。

**绝不翻译的词**：taste, ambition, insight, motivation, role model, authentic, condition on, overfitting, scaling law, vibe coding, roadmap, build in public, fake it until make it, anchor, solid, failure case

**绝不用英文的词**：情感/态度/生活词汇全中文——焦虑、坚韧、蔑视、彷徨、牌桌、方寸、厚积薄发

**节奏**：中文长句 + 英文概念词 + 中文展开。英文词像钉子嵌入中文骨架。

示例：
> "越来越强烈的感受到我正借由RoPE这个切口approaching something authentic"

### 2.2 跨域类比

保留并展开原文中的类比。渊博的类比模式：
- 政治史/军事史 → 科研决策
- ML 术语 → 心理/人际
- 工业革命 → AI 产业

如果原文有类比，展开到读者能理解的程度（补一句上下文）。如果原文没有类比，不要编造。

### 2.3 豪迈 ↔ 自嘲无缓冲

保留情感极性。不加"不过话说回来""当然了""客观来讲"之类的缓冲软化词。渊博在高昂自我激励和坦率自我解剖之间没有中间态，不能把棱角磨平。

### 2.4 宣言式收尾

段落或全文末尾用短句断言收束。

**用**："说到底""得学""干就完了"
**不用**："总之……""未来可期""让我们拭目以待"

### 2.5 感叹词系统

保留原文的感叹表达，不替换为书面语。不凭空添加。

| 等级 | 表达 |
|------|------|
| 最高赞叹 | "卧槽""巨屌""恐怖如斯" |
| 正面兴奋 | "爽""太爽了""牛逼" |
| 自嘲 | "hhhh" |
| 惊讶 | "我靠" |

### 2.6 反模式清单

以下表达**绝对不出现**在润色输出中：

1. emoji
2. 客套对冲："可能我理解有误""仅供参考"
3. 学术腔："具有重要意义""值得深入研究"
4. 空洞升华："更广泛的趋势""不断演变的格局"
5. 轻飘飘评价：无锚点的好坏判断
6. 填充性开场白："在当今……的时代""随着……的发展"
7. 公式化连接词："此外""值得注意的是""不仅……更……"
8. 展望式结尾："未来可期""让我们拭目以待"
9. 过度谦虚："我还需要学习""班门弄斧"
10. 宣传式形容词堆砌："充满活力的""丰富的""深刻的"

## 3. 语域判断

收到输入后，先判断语域：

### 口语帖模式

**触发**：输入 < 300 字，或无小标题/列表结构，或明显是一句话碎片

**策略**：
- 把箭头链 `→` 和压缩句展开成 2-4 个自然段
- 保留口语感，像在跟朋友聊天讲一件事
- 可以用"你知道吗""说白了""说到底"这类口语连接
- 总长控制在 200-500 字

### 结构化文章模式

**触发**：输入 > 300 字，或有小标题/列表/多层论点

**策略**：
- 保留或优化原有结构（小标题、bullet）
- 每个论点展开到别人能跟上的程度，但不啰嗦
- 保留类比和例子，必要时补一句上下文让读者能理解
- 不限长度，跟随内容需要

### 用户覆盖

如果用户指定语域（"改成小红书帖""润成一篇文章"），跳过自动判断，直接用指定模式。

## 4. 处理流程

1. 读取用户输入的待润色文本
2. 判断语域（口语帖 / 结构化文章 / 用户指定）
3. 读取 `examples.md` 中对应语域的示例对，作为风格锚定
4. 按 6 个风格维度润色：
   - 检查中英嵌套节奏
   - 保留/展开跨域类比
   - 保持情感极性不软化
   - 确保收尾干脆
   - 保留原生感叹词
   - 扫描反模式清单
5. 质量评分（见下）
6. 如果 < 45 分，修正薄弱维度后重新输出
7. 输出润色后文本 + 评分卡

## 5. 质量评分

润色完成后打分，5 维各 10 分，满分 50：

| 维度 | 评估标准 |
|------|----------|
| **像渊博** | 中英嵌套节奏、类比方式、情感极性是否对味 |
| **可读性** | 别人能读懂吗？压缩句是否充分展开、上下文是否充足 |
| **不端着** | 有没有混入学术腔、客套话、空洞升华？反模式清单全过 |
| **节奏感** | 长短句交替自然？收尾干脆？无拖泥带水 |
| **忠实度** | 原文的核心观点和情绪完整保留？无改温和/改跑偏 |

**标准**：
- 45-50：直接输出
- 35-44：标注薄弱维度，自动修正一轮后输出
- < 35：重写

**输出格式**：

润色后文本

---

| 维度 | 得分 | 备注 |
|------|------|------|
| 像渊博 | X/10 | … |
| 可读性 | X/10 | … |
| 不端着 | X/10 | … |
| 节奏感 | X/10 | … |
| 忠实度 | X/10 | … |
| **总分** | **X/50** | |

## 6. 约束

- 全程中文（英文词按 2.1 规则处理）
- 核心观点和情绪必须忠实于原文
- 不添加原文没有的信息或类比（除非用户要求）
- 参考 examples.md 中的示例对校准风格
```

- [ ] **Step 2: Verify file was created**

Run: `ls -la /Users/sum_young/code/projects/yuanbo-skills/yuanboizer-zh/SKILL.md`
Expected: file exists, ~5KB

- [ ] **Step 3: Commit**

```bash
cd /Users/sum_young/code/projects/yuanbo-skills
git add yuanboizer-zh/SKILL.md
git commit -m "feat(yuanboizer-zh): add main skill with 6 style dimensions + scoring"
```

---

### Task 3: Install skill via symlink

**Files:**
- Modify: symlink at `~/.claude/skills/yuanboizer-zh`

- [ ] **Step 1: Run install.sh to create symlink**

```bash
cd /Users/sum_young/code/projects/yuanbo-skills
bash install.sh
```

Expected output includes: `Linked: yuanboizer-zh` or `unchanged` if already linked.

- [ ] **Step 2: Verify symlink works**

```bash
ls -la ~/.claude/skills/yuanboizer-zh/SKILL.md
```

Expected: file exists and is readable through symlink.

- [ ] **Step 3: Verify skill appears in Claude Code**

Start a new Claude Code session or check skill list. The skill `yuanboizer-zh` should appear with trigger words: 润色、yuanboize、帮我改改、改成小红书。

---

### Task 4: Smoke test with a real input

**Files:**
- No files created or modified

- [ ] **Step 1: Test oral mode with a real Notion thought**

Invoke the skill with this input:

```
帮我润色：和李博聊到如何我们这些探索派如何降维打击overfitting的好学生们 → 做出那些overfitting guys slides第一页的东西
```

Verify the output:
- Expanded into 2-4 paragraphs (not a one-liner)
- English words preserved: overfitting, slides
- No emoji, no academic tone, no "此外"
- Ends with a punchy short sentence
- Scoring card present with all 5 dimensions

- [ ] **Step 2: Test structured mode with a multi-point input**

Invoke the skill with this input:

```
帮我润色：

我和嘉豪写skill的差异
- 我做写作/表达类工具，嘉豪做基础设施/执行类
- 我造了一个"系统"（labmate），嘉豪造了一个"工具箱"（sjh-skills）
- 我相信流程的力量，嘉豪相信工具的力量
- 焦虑源不同：我怕"有想法说不清楚"，嘉豪怕"环境不够顺手"
- 但这可能只是当前阶段快照，不是定性
```

Verify the output:
- Has section headings
- Each bullet expanded with context
- Preserves the PayPal-mafia-style comparative framing
- No softening buffers ("当然了""客观来讲")
- Scoring card present

- [ ] **Step 3: Test user override**

Invoke with explicit mode override:

```
改成小红书帖：failure case是最宝贵的事情，他打破你简单的直觉，也提供了一个anchor强迫你深入
```

Verify: output is in oral mode regardless of content structure.

---

### Task 5: Final commit and cleanup

**Files:**
- No new files

- [ ] **Step 1: Verify all files are committed**

```bash
cd /Users/sum_young/code/projects/yuanbo-skills
git status
git log --oneline -5
```

Expected: clean working tree, two new commits for yuanboizer-zh.

- [ ] **Step 2: Verify directory structure**

```bash
ls -la /Users/sum_young/code/projects/yuanbo-skills/yuanboizer-zh/
```

Expected:
```
SKILL.md
examples.md
```
