# selfOS Skill Suite Design

> 目标：围绕 selfOS wiki 构建一套完整的 CC skill 集，让日常和 wiki 的交互形成自然循环。
> 核心理念：从"你记录自己"变成"wiki 理解你，然后来找你确认和补全"。

## 目标用户

- 主要给自己用（深度使用体验优先）
- 将来 fork 分发给朋友和 CC 社区（需要 onboarding 流畅）

## 设计原则

1. **增量交互 > 存量导入** — 重点是日常和 wiki 的对话循环，不是批量喂料
2. **一切提问基于 context** — wiki 的主动提问必须引用已有内容，不能凭空问
3. **入口极简** — 用户只需记住 4 个命令
4. **零配置 fork** — clone + 一条命令就能用

## 三层架构

```
写入层（用户主动输入）
├── /thought <text>     — 快速想法 + 即时 interview
├── /wiki ingest <url>  — 外部 source 导入
└── /wiki sync          — Notion 同步

对话层（wiki 主动找你）
├── /interview          — 统一的 wiki 主动对话入口
├── /bookmark-chat      — 推特书签 context recovery
├── /complete           — 旧 Thoughts context recovery
└── /digest             — 回顾 + 推荐问题

被动层（零摩擦）
├── Auto-Capture hook   — 对话结束静默抽取 context
└── Preference tagging  — 检测未展开偏好/判断，标记为待追问
```

## 用户心智模型

| 你想… | 命令 |
|--------|------|
| 记一个想法 | `/thought` |
| 让 wiki 问我 | `/interview` |
| 看看 wiki 最近怎样了 | `/digest` |
| 导入/查询/管理 | `/wiki` |

## Skill 清单

### 1. `selfos`（已有，不动）

`/wiki ingest/query/lint/compile/sync/status`

Wiki 管理的主入口。无需改动。

### 2. `thought`（已完成）

`/thought <text>`

快速写入一句话想法到 `wiki/sources/thought-YYYY-MM-DD-<slug>.md`，立刻进入 interview 模式补充 context。写入即对话，一步到位。

### 3. `selfos-completion`（需改造）

#### 现有功能保留

- `/bookmark-chat` — 推特书签 context recovery
- `/complete` — Notion Thoughts context recovery

#### `/interview` 升级

从单一的"填 wiki gap"升级为**统一的 wiki 主动对话入口**。三种问题池按优先级混合：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | Pending Questions | Auto-Capture 标记的未展开偏好/判断（frontmatter `pending_questions` 字段） |
| 2 | Open Questions | 概念页底部已有的 Open Questions |
| 3 | Thin Pages / Timeline Gaps | 现有的 gap 分析（< 100 字的页面、时间线空洞） |

`interview-questions.py` 脚本需要扩展：新增扫描所有 wiki source 页面的 `pending_questions` 字段，作为最高优先级问题池。问完后从 frontmatter 中移除该条。

#### 交互原则不变

- 一次问一个问题
- 对话式，不是问卷
- 引用 wiki 已有内容让问题具体
- 回答后静默更新相关 wiki 页面

### 4. `digest`（新建）

#### 命令

```
/digest           → 今日回顾 + 1 个推荐问题
/digest week      → 本周回顾
/digest question  → 只给推荐问题
```

#### 今日回顾内容

从 `wiki/log.md` 最近条目 + `git log --since="today"` 提取：

- 新增页面列表（标题 + 类型）
- 更新页面列表（变更摘要）
- 新建连接（跨页面引用）
- 1 个推荐问题（从 `pending_questions` 池或 Open Questions 中选取，必须引用今天的变化作为 context）

#### 周回顾额外包含

- 本周新增/更新页面数量统计
- 最活跃的概念（被引用/更新最多的 top 3）
- Timeline 覆盖度变化
- 2-3 个推荐问题

#### 实现

纯 skill 指导，不需要新 Python 脚本。LLM 在 skill 中被指导：
1. 读 `wiki/log.md` 最近 N 条
2. `git log --since` 看文件变化
3. 扫描 `pending_questions` 池选推荐问题
4. 综合输出

用户看完 digest 后可以直接回答推荐问题，自然过渡到 interview 模式。

### 5. Preference Tagging（Auto-Capture 增强）

#### 触发

Auto-Capture Stop hook（对话结束时）。在现有 context 抽取之外，增加偏好/判断检测。

#### 检测信号

```
1. 未展开的判断："我觉得 X 比 Y 好" / "X 不行" / "X 没前途"
   → 待追问：为什么？在什么条件下？

2. 模糊想法："我在想 X 会不会..." / "感觉 X 和 Y 有关系"
   → 待追问：具体怎么关联？能展开吗？

3. 情绪信号："被 X 震撼了" / "X 太爽了" / "X 让我很不爽"
   → 待追问：具体是什么触动了你？

4. 未说完的偏好："我比较倾向..." / "以后可能会..."
   → 待追问：基于什么考虑？
```

#### 存储

写入对应的 `wiki/sources/auto-*.md` 的 frontmatter：

```yaml
pending_questions:
  - "你说'agent 时代最大的杠杆是 taste'——具体指什么场景下的 taste？"
  - "你提到不看好 X 方向，是基于什么判断？"
```

#### 消费

`/interview` 优先级 1 池扫描 `pending_questions` 字段。单条问完后从列表中移除该条（不清空整个字段）。字段为空数组时删除字段。

#### 不做什么

- 不在对话中途打断（破坏工作流）
- 不做独立的 `/preference` 命令（统一走 `/interview`）
- 不做复杂 NLP 分类（信号词匹配，宁可漏掉不要误报）

## 分发架构

### 目录结构

```
selfOS/
├── CLAUDE.md                        # wiki schema + 命令文档
├── wiki/                            # wiki 内容
├── scripts/
│   ├── auto-ingest.py               # Auto-Capture + Preference tagging
│   ├── interview-questions.py       # /interview 问题生成（需扩展）
│   └── wiki_utils.py
├── .claude/
│   ├── skills/
│   │   ├── selfos/                  # /wiki 命令
│   │   ├── selfos-completion/       # /interview, /bookmark-chat, /complete
│   │   ├── thought/                 # /thought
│   │   └── digest/                  # /digest（新建）
│   └── settings.local.json          # 项目级配置
├── hooks/
│   └── auto-capture.sh              # Auto-Capture hook 脚本（从 ~/.claude/hooks/ 移入 repo）
└── setup.sh                         # 一键安装
```

### 项目级 vs 全局

| 组件 | 项目级（自动生效） | 全局（需 setup.sh） |
|------|-------|------|
| Skills | `.claude/skills/` 下的所有 skill 在 selfOS 目录自动加载 | `setup.sh` 创建 `~/.claude/skills/` 下的 symlink |
| Hooks | `.claude/settings.local.json` 项目级 hook | `setup.sh` 可选注册全局 Stop hook |
| Scripts | `scripts/` 跟 repo 走 | 无需全局 |
| CLAUDE.md | repo root | 无需全局 |

### `setup.sh`

```bash
#!/bin/bash
set -e

SELFOS_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "selfOS Setup"
echo "============"
echo ""

# 1. 全局 skill symlink（让 /thought 等在任意目录可用）
echo "注册全局 skill symlink..."
for skill in selfos selfos-completion thought digest; do
  target="$SELFOS_DIR/.claude/skills/$skill"
  link="$HOME/.claude/skills/$skill"
  if [ -L "$link" ] || [ -d "$link" ]; then
    echo "  跳过 $skill（已存在）"
  else
    ln -s "$target" "$link"
    echo "  ✓ $skill"
  fi
done

# 2. Auto-Capture hook（可选）
echo ""
read -p "注册 Auto-Capture hook（对话结束时自动抽取 context）？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "请手动将以下内容添加到 ~/.claude/settings.json 的 Stop hooks 中："
  echo ""
  echo "  {\"hooks\": [{\"command\": \"bash $SELFOS_DIR/hooks/auto-capture.sh\", \"type\": \"command\"}], \"matcher\": \"\"}"
  echo ""
fi

echo ""
echo "安装完成。在 Claude Code 中运行 /wiki init 初始化你的 wiki。"
```

### `/wiki init` 重置逻辑

在 selfos skill 中增加 init 处理：

- 清空 `wiki/` 下所有内容页面（concepts/, entities/, sources/, synthesis/）
- 重置 `wiki/index.md`（保留结构，清空条目）
- 重置 `wiki/log.md`（清空，写入 init 记录）
- 重置 `wiki/overview.md`（空模板）
- 保留 CLAUDE.md 不动
- 提示用户开始使用

### Fork 用户流程

```
1. git clone https://github.com/xxx/selfOS.git
2. cd selfOS
3. ./setup.sh          # 可选：全局 skill + hook
4. 在 CC 中：/wiki init  # 清空 demo 内容
5. /thought 我的第一个想法
```

## 实施顺序

| 阶段 | 任务 | 依赖 |
|------|------|------|
| Phase 1 | `/digest` skill 新建 | 无 |
| Phase 2 | `/interview` 升级（3 种问题池） | 无 |
| Phase 3 | Preference tagging（auto-ingest.py 增强） | Phase 2（消费端先就位） |
| Phase 4 | 分发整理（hook 移入 repo, setup.sh, /wiki init 重置） | Phase 1-3 |

Phase 1 和 Phase 2 可并行。
