# 数据导入指南

> 把你的 Claude.ai 对话、Gemini 对话、Twitter 书签导入 selfOS wiki

## 快速开始

```bash
# 1. 放数据到 raw/
#    (具体步骤见下方各数据源说明)

# 2. 提取为 source pages
python3 scripts/extract-all-sources.py

# 3. 编译进 wiki
# 在 Claude Code 中:
/wiki compile
```

## 数据源 1: Claude.ai 对话

### 导出

1. 打开 [claude.ai](https://claude.ai)
2. Settings → Account → Export Data
3. 等邮件，下载 zip
4. 解压后得到 `conversations.json` + `users.json`

### 放置

```bash
cp conversations.json ~/selfOS/raw/claude-conversations/
# ⚠️ 不要提交 users.json（含 PII：邮箱、电话）
```

### 格式说明

`conversations.json` 是 JSON array，每个对话包含：

| 字段 | 说明 |
|------|------|
| `name` | 对话标题 |
| `chat_messages[]` | 消息列表，每条有 `sender` (human/assistant) + `text` |
| `summary` | Claude 自动生成的对话摘要（高价值） |
| `created_at` | 创建时间 |
| `uuid` | 唯一标识 |

### 提取结果

- 输出到 `wiki/sources/cc-{date}-{slug}.md`
- 保留完整对话（`[我]` + `[Claude]`）
- `summary` 放在页面顶部作为 AI Summary
- 跳过无标题且少于 3 条消息的对话

---

## 数据源 2: Gemini 对话

### 导出

使用 Chrome 扩展 **Gemini Exporter**：

1. 安装 Gemini Exporter（Chrome Web Store 搜索）
2. 打开 gemini.google.com，登录
3. 点击扩展图标，选择导出格式为 Markdown
4. 导出全部对话，得到一批 `.md` 文件

### 放置

```bash
cp *.md ~/selfOS/raw/gemini-conversations/
```

### 格式说明

Gemini Exporter 导出的 `.md` 文件结构：

```
============================================================
Conversation: 对话标题
Messages: 消息数
Created: 2025-05-25T11:35:58.000Z
Last message: 2025-05-25T11:23:28.000Z
URL: https://gemini.google.com/app/{hash}
============================================================

--- User ---
用户消息

--- Gemini ---
Gemini 回复
```

文件名格式：`{YYYYMMDD}_{标题}_{hash}.md`

### 已知坑

- **重复条目**：同标题不同 hash 的文件可能是重复的，脚本会自动跳过同名输出
- **空对话**：有些文件没有 `--- User ---` 标记，会被自动跳过

### 提取结果

- 输出到 `wiki/sources/gem-{date}-{slug}.md`
- 保留完整对话（`[我]` + `[Gemini]`）
- 从文件名提取日期

---

## 数据源 3: Twitter 书签

### 前置条件

- Chrome 登录了 x.com
- 网络代理可用（Twitter 需要）

### 安装 fieldtheory

```bash
npm install -g fieldtheory
```

### 同步书签

```bash
# 需要代理
export https_proxy=http://127.0.0.1:7890
ft sync
```

同步后数据在 `~/.ft-bookmarks/`（SQLite + JSONL）。

### 已知坑

- Node.js undici 不认系统代理，必须手动 `export https_proxy` 或用 TUN 模式
- Chrome 必须保持 x.com 登录状态
- 首次同步约 2-3 分钟（2000+ 条）

### 书签不直接 ingest

书签和对话不同——内容是别人写的，直接导入没有意义。正确的处理方式：

1. **分类**：`ft classify` + `ft classify-domains`
2. **逐条对话**：每条展示原文 → 问"为什么收藏"→ 提炼偏好
3. **合并进 wiki**：只记录"我为什么关注这个"，不转述原文

详见 `docs/specs/twitter-bookmarks-ingest.md`

快捷方式：在 Claude Code 中运行 `/bookmark-chat`，自动随机抽取书签并对话还原 context。

---

## 提取脚本详解

`scripts/extract-all-sources.py` 做三件事：

1. 遍历 `raw/notion-notes/*.md` → 输出 `wiki/sources/notion-*.md`
2. 读取 `raw/claude-conversations/conversations.json` → 输出 `wiki/sources/cc-*.md`
3. 遍历 `raw/gemini-conversations/*.md` → 输出 `wiki/sources/gem-*.md`

**行为特点**：
- 不删除已有 source pages（只跳过同名文件）
- 可重复运行，幂等
- 保留完整对话内容，用 `[我]` / `[Claude]` / `[Gemini]` 标注发言者

**运行**：

```bash
cd ~/selfOS
python3 scripts/extract-all-sources.py
```

---

## 提取后：编译进 wiki

Source pages 只是原始对话的 markdown 化。要让内容进入知识图谱，还需要编译：

```
/wiki compile
```

编译会：
1. 扫描 `wiki/sources/` 中未处理的 source pages
2. 为每个 source 提取概念 → `wiki/concepts/`
3. 提取实体 → `wiki/entities/`
4. 更新 cross-references 和 `wiki/index.md`

---

## 安全注意事项

| 文件 | 风险 | 处理 |
|------|------|------|
| `users.json` (Claude) | 含邮箱、电话 | **不要 git 追踪**，`.gitignore` 已配置 |
| `conversations.json` | 含完整对话 | 放在 `raw/` 下，默认不公开 |
| Gemini `.json` | 类似 | `.gitignore` 已排除 |
| `wiki/sources/` | 提取后的对话 | 看你的隐私需求决定是否公开 |

---

## FAQ

**Q: 多次导出会重复吗？**
A: 不会。脚本按文件名去重，同名文件直接跳过。但如果你的新导出包含更多对话，会生成新的 source pages。

**Q: 可以只导入某一个数据源吗？**
A: 可以。脚本会自动跳过不存在的目录。只放 Claude 数据就只处理 Claude。

**Q: 导入后怎么验证？**
A: `ls wiki/sources/ | head -20` 看文件列表，或 `/wiki status` 查看统计。
