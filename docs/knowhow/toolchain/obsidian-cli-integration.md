# Obsidian CLI 工具与集成方案调研

**日期:** 2026-04-07
**场景:** selfOS — LLM-maintained wiki，Claude Code 通过命令行读写 wiki/ 目录下的 markdown 文件
**痛点:** (1) 外部写入后 Obsidian 不立即刷新 (2) 无法从 CLI 触发 Obsidian 操作 (3) 想从 CLI 利用 Obsidian 能力

---

## 1. Obsidian URI Protocol（原生）

### 核心能力

Obsidian 内置 `obsidian://` URI scheme，支持以下 action：

| Action | 功能 | 关键参数 |
|--------|------|----------|
| `open` | 打开笔记 | `vault`, `file`, `path`, `paneType` |
| `new` | 创建笔记 | `name`, `file`, `content`, `silent`, `append`, `overwrite` |
| `daily` | 打开/创建日记 | 同 `new` |
| `unique` | 创建唯一笔记 | `content`, `clipboard` |
| `search` | 打开搜索 | `query` |
| `choose-vault` | 打开 vault 管理器 | - |
| `hook-get-address` | Hook 集成 | `x-success`, `x-error` |

**macOS CLI 调用方式：**
```bash
# 打开特定笔记
open "obsidian://open?vault=selfOS&file=wiki%2Findex"

# 创建笔记（静默模式，不打开编辑器）
open "obsidian://new?vault=selfOS&file=wiki%2Fconcepts%2Fnew-concept&content=Hello&silent=true"

# 追加内容到已有笔记
open "obsidian://open?vault=selfOS&file=wiki%2Flog&append=true&content=New%20entry"

# 打开搜索
open "obsidian://search?vault=selfOS&query=attention"
```

**快捷格式：**
```bash
open "obsidian://vault/selfOS/wiki/index"
open "obsidian://~/selfOS/wiki/index"
```

**支持 `x-callback-url`：** `new` 和 `hook-get-address` 支持 `x-success` 回调。

### 对 Claude Code 集成的价值

- **直接可用：** 无需安装任何插件，macOS 上 `open` 命令即可调用
- **导航：** Claude Code 写完文件后自动在 Obsidian 中打开对应笔记
- **创建：** 可通过 URI 创建笔记（但 Claude Code 直接写文件更可靠）
- **搜索：** 可打开 Obsidian 搜索面板

### 局限

- **单向通信：** 只能触发 Obsidian 动作，无法获取返回值（除 x-callback-url）
- **无法读取内容：** 不能通过 URI 获取笔记内容
- **无法执行插件命令：** 不支持 Dataview 查询等高级操作
- **文件操作有限：** 无删除、移动、重命名能力

### 成熟度与推荐度

- **成熟度：** 官方内置，极其稳定
- **推荐度：** ★★★★☆ — 作为基础层使用，用于"写完后自动在 Obsidian 打开"

---

## 2. Obsidian Local REST API 插件

### 核心能力

社区插件，在 localhost:27124 暴露完整的 RESTful API。

| 端点 | 方法 | 功能 |
|------|------|------|
| `/vault/{path}` | GET/PUT/PATCH/POST/DELETE | 笔记 CRUD（全量和定向编辑） |
| `/active/` | GET/PUT/PATCH/POST/DELETE | 操作当前打开的笔记 |
| `/periodic/{period}/` | GET/PUT/PATCH/POST/DELETE | 日记/周记/月记 |
| `/search/simple/` | POST | 全文模糊搜索 |
| `/search/` | POST | **Dataview DQL 查询** 或 JsonLogic 查询 |
| `/commands/` | GET | 列出所有可用的 Obsidian 命令 |
| `/commands/{commandId}/` | POST | **执行任意 Obsidian 命令** |
| `/tags/` | GET | 获取所有标签及使用计数 |
| `/open/{path}` | POST | 在 Obsidian UI 中打开文件 |

**定向编辑能力：** 支持按 `heading`、`block`、`frontmatter` 定位，支持 `append`、`prepend`、`replace` 操作。

**认证方式：** Bearer Token（`Authorization: Bearer <api-key>`），API key 在插件设置中生成。

**使用示例：**
```bash
# 读取笔记
curl -s https://127.0.0.1:27124/vault/wiki/index.md \
  -H "Authorization: Bearer YOUR_API_KEY" -k

# 写入笔记
curl -X PUT https://127.0.0.1:27124/vault/wiki/concepts/new.md \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: text/markdown" \
  -d "# New Concept" -k

# 追加内容到特定 heading
curl -X POST https://127.0.0.1:27124/vault/wiki/log.md \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: text/markdown" \
  -H "Heading: Operations Log" \
  -d "- 2026-04-07: Updated index" -k

# 执行 Dataview 查询
curl -X POST https://127.0.0.1:27124/search/ \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/vnd.olrapi.dataview.dql+txt" \
  -d 'TABLE tags, updated FROM "wiki/concepts" SORT updated DESC' -k

# 列出所有命令
curl -s https://127.0.0.1:27124/commands/ \
  -H "Authorization: Bearer YOUR_API_KEY" -k

# 执行特定命令（如刷新 Dataview）
curl -X POST https://127.0.0.1:27124/commands/dataview:dataview-force-refresh-views/ \
  -H "Authorization: Bearer YOUR_API_KEY" -k

# 全文搜索
curl -X POST https://127.0.0.1:27124/search/simple/ \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: text/plain" \
  -d "attention mechanism" -k
```

### 对 Claude Code 集成的价值

这是 **最关键的集成方案**，几乎解决了所有痛点：

1. **双向通信：** Claude Code 可以读取 Obsidian 视角下的笔记内容（经过 Obsidian 处理）
2. **Dataview 查询：** 可以从 CLI 执行 Dataview DQL 查询，获取结构化数据
3. **命令执行：** 可以触发任何 Obsidian 命令，包括强制刷新、重建索引等
4. **精准编辑：** 可以按 heading/block 定位编辑，比直接文件操作更安全
5. **搜索：** 全文搜索 + Dataview 查询 = 强大的检索能力

### 注意事项

- 使用自签名 HTTPS 证书（curl 需要 `-k` 参数，或手动信任证书）
- 仅监听 localhost（安全，但无法远程访问）
- **Obsidian 必须运行** 才能使用 API
- Dataview 查询需要安装 Dataview 插件

### 成熟度与推荐度

- **Stars:** ~2,000 | **最新版本:** v3.6.0 (2026-04-06) | **Issues:** 仅 4 个 open
- **成熟度：** 非常活跃，持续维护
- **推荐度：** ★★★★★ — **核心推荐方案**，Claude Code 集成的首选

---

## 3. Obsidian Advanced URI 插件

### 核心能力

大幅扩展原生 URI scheme，增加 `obsidian://adv-uri` handler：

| 功能类别 | 能力 |
|----------|------|
| 导航 | 打开文件/工作区/书签/heading/block |
| 写入 | 创建/编辑文件，追加/前插内容 |
| 搜索替换 | 在文件中执行自动化搜索替换 |
| 命令执行 | 通过 `commandid` 参数执行 Obsidian 命令 |
| Frontmatter | 读取和修改 YAML frontmatter |
| Canvas | Canvas 文件操作 |
| 日记 | 创建/打开日记，支持剪贴板集成 |

**使用示例：**
```bash
# 向日记追加剪贴板内容
open "obsidian://adv-uri?vault=selfOS&daily=true&clipboard=true&mode=append"

# 执行特定命令
open "obsidian://adv-uri?vault=selfOS&filepath=wiki/index&commandid=workspace%3Aexport-pdf"

# 导航到 heading
open "obsidian://adv-uri?vault=selfOS&filepath=wiki/concepts/attention&heading=Key%20Takeaways"

# 文件中搜索替换
open "obsidian://adv-uri?vault=selfOS&filepath=wiki/index&search=old-text&replace=new-text"

# 写入 frontmatter
open "obsidian://adv-uri?vault=selfOS&filepath=wiki/concepts/attention&frontmatterkey=updated&data=2026-04-07"
```

### 对 Claude Code 集成的价值

- **命令执行：** 可以通过 URI 触发任何 Obsidian 命令（包括 Dataview 刷新）
- **Frontmatter 操作：** 直接修改 YAML metadata
- **搜索替换：** 自动化文本替换
- **比原生 URI 更强大：** 但仍是单向的，无法获取返回数据

### 局限

- 仍然是单向通信（只能触发，不能读取结果）
- 不支持 Dataview 查询返回结果
- 不支持 Graph View 截图

### 成熟度与推荐度

- **Stars:** 1.1k | **版本:** v1.46.1 (2026-01) | **87 个 releases**
- **成熟度：** 稳定且活跃
- **推荐度：** ★★★★☆ — 作为 Local REST API 的轻量替代，不需要 HTTP 服务

---

## 4. Obsidian Actions URI 插件

### 核心能力

提供增强的 `x-callback-url` 端点，面向自动化工作流：

- 日记操作
- 笔记管理
- 搜索结果获取
- 标准化的 x-callback-url 协议

**重点：** 专为 macOS/iOS Shortcuts 和外部自动化工具设计，使用 `x-callback-url` 协议意味着 **可以获取返回数据**。

### 对 Claude Code 集成的价值

- 可配合 macOS Shortcuts 实现复杂工作流
- x-callback-url 支持意味着一定程度的双向通信
- 但相比 Local REST API 的 HTTP 请求，使用起来更复杂

### 成熟度与推荐度

- **Stars:** 187 | **版本:** v1.8.4 (2025-11) | 672 commits
- **成熟度：** 稳定，作者标注 "Active"
- **推荐度：** ★★★☆☆ — 对 macOS Shortcuts 用户价值高，但 Claude Code 场景下 Local REST API 更优

---

## 5. NotesMD CLI（原 Obsidian CLI）

### 核心能力

Go 语言编写的独立 CLI 工具（不需要 Obsidian 运行）：

| 命令 | 功能 |
|------|------|
| `notesmd list-vaults` | 列出所有 vault |
| `notesmd open <note>` | 在编辑器中打开笔记 |
| `notesmd create <note>` | 创建新笔记 |
| `notesmd print <note>` | 输出笔记内容 |
| `notesmd move <src> <dst>` | 移动/重命名（自动更新内链） |
| `notesmd delete <note>` | 删除笔记 |
| `notesmd daily` | 创建/打开日记 |
| `notesmd search <query>` | 模糊搜索文件名 |
| `notesmd search-content <query>` | 搜索文件内容 |
| `notesmd frontmatter <note>` | YAML frontmatter 操作 |

**工作方式：** 直接操作文件系统，读取 `.obsidian/` 配置文件获取设置。

**安装：**
```bash
brew tap yakitrak/yakitrak && brew install notesmd
```

### 对 Claude Code 集成的价值

- **不需要 Obsidian 运行：** 适合 CI/CD 或 headless 环境
- **移动文件时自动更新内部链接：** 这是直接文件操作做不到的
- **尊重 Obsidian 配置：** 日记格式、默认文件夹等
- **搜索能力：** 文件名和内容搜索

### 局限

- 不能执行 Obsidian 插件命令
- 不能触发 Dataview 查询
- 不了解 Obsidian 的实时状态

### 成熟度与推荐度

- **Stars:** 1.3k | **语言:** Go | **最近更新:** 活跃
- **成熟度：** 成熟，社区广泛使用
- **推荐度：** ★★★☆☆ — 对 selfOS 场景价值有限（Claude Code 已直接操作文件），但 `move` 命令的链接更新能力有用

---

## 6. Obsidian Shell Commands 插件

### 核心能力

**反向集成** —— 从 Obsidian 内部执行系统命令：

**事件触发器：**
- `Obsidian starts` / `Obsidian quits`
- `File content modified` / `File created` / `File deleted`
- `File moved` / `File renamed`
- `Folder created` / `Folder deleted` / `Folder moved` / `Folder renamed`
- `Switching the active pane`
- `Every n seconds`（定时器）
- `File menu` / `Folder menu` / `Editor menu`（右键菜单）

**变量系统：**
```
{{file_name}}, {{file_path}}, {{folder_name}}, {{folder_path}}
{{title}}, {{tags}}, {{selection}}, {{clipboard}}
{{date}}, {{time}} (可自定义格式)
```

**URI 执行：** 支持从外部通过 URI 触发预定义的 shell 命令：
```bash
open "obsidian://shell-commands/?vault=selfOS&execute=COMMAND_ID"
# 还支持通过自定义变量传参：
open "obsidian://shell-commands/?vault=selfOS&execute=0&_my_var=value"
```

**输出通道：** 命令输出可以写入通知、状态栏、当前文件、剪贴板。

### 对 Claude Code 集成的价值

**关键场景 —— 文件变更自动响应：**

可以配置 Shell Commands 在检测到文件变化时自动执行脚本。例如：
- 当 `wiki/` 下有文件变化时，触发 Obsidian 刷新
- 当 Claude Code 写入文件后，自动执行验证脚本
- 定时执行 wiki lint 检查

**重要发现：** Shell Commands 文档明确指出：
> File/folder moves/renames done by external applications are seen as *deletions* and *creations*.

这意味着 Obsidian **确实能检测到外部文件变更**，只是将其视为"删除+创建"而非"修改"。Shell Commands 插件可以利用这些事件。

### 局限

- 仅桌面端（无移动端支持）
- 命令需要在 Obsidian 内预先配置
- 不能动态创建新命令

### 成熟度与推荐度

- **Stars:** 496 | **版本:** v0.23.0 (2024-11) | 1,463 commits
- **成熟度：** 成熟，文档丰富
- **推荐度：** ★★★★☆ — 对于"Obsidian 响应外部变更"这个痛点非常有价值

---

## 7. kepano/obsidian-skills（Agent Skills）

### 核心能力

由 Obsidian CEO kepano 维护的 **AI Agent 专用 skill 集**，面向 Claude Code、Codex CLI、OpenCode 等 LLM 编程助手。

**提供的 skill：**
- Obsidian Flavored Markdown 编写指南（wikilinks, embeds, callouts, properties）
- Obsidian Bases 操作（views, filters, formulas, summaries）
- JSON Canvas 文件操作
- CLI 命令参考

**安装：** 复制到 `~/.claude/skills/` 或项目 `.claude/` 目录。

### 对 Claude Code 集成的价值

- **官方推荐的 LLM 集成方式：** kepano 亲自维护
- **确保 Claude Code 写出正确的 Obsidian 格式：** wikilinks、callouts 等
- **21.4k stars：** 社区强烈认可

### 成熟度与推荐度

- **Stars:** 21.4k | **Forks:** 1.3k | **最近更新:** 5 天前
- **推荐度：** ★★★★★ — **必须安装**，与我们的场景完美匹配

---

## 8. 文件监控与热重载

### Obsidian 的文件监控机制

**核心事实：**
1. Obsidian 使用 Node.js 的文件系统监控（Electron 底层）
2. Obsidian **能检测到外部文件变更**，但行为取决于：
   - 应用是否在前台
   - 文件是否正在编辑中
   - 操作系统的 fs.watch 实现

**已知行为（macOS）：**
- Obsidian 在前台时，外部修改通常在 1-2 秒内反映
- Obsidian 在后台时，可能延迟到窗口获取焦点时才刷新
- 外部移动/重命名被视为"删除 + 创建"

**Vault API 事件（供插件开发者参考）：**
```typescript
app.vault.on('modify', (file) => { /* 文件内容变化 */ })
app.vault.on('create', (file) => { /* 文件创建 */ })
app.vault.on('delete', (file) => { /* 文件删除 */ })
app.vault.on('rename', (file, oldPath) => { /* 文件重命名 */ })
```

### 解决"外部修改不即时刷新"的方案

**方案 A：Local REST API 强制刷新**
```bash
# 写完文件后，通过 REST API 打开该文件，强制 Obsidian 加载最新内容
curl -X POST https://127.0.0.1:27124/open/wiki/concepts/new-concept.md \
  -H "Authorization: Bearer YOUR_API_KEY" -k
```

**方案 B：URI 触发打开**
```bash
# 写完文件后打开
open "obsidian://open?vault=selfOS&file=wiki%2Fconcepts%2Fnew-concept"
```

**方案 C：Shell Commands 定时刷新**
配置 Shell Commands 的 "Every n seconds" 事件，定期执行 `app:reload` 命令。

**方案 D：AppleScript / osascript**
```bash
# 激活 Obsidian 窗口（触发文件重新扫描）
osascript -e 'tell application "Obsidian" to activate'
```

---

## 综合推荐方案

### 第一优先级：必装

| 方案 | 用途 | 安装方式 |
|------|------|----------|
| **Local REST API** | CLI 双向通信的核心 | Obsidian 社区插件 |
| **obsidian-skills** | 确保 Claude Code 写出正确格式 | 复制到 `~/.claude/skills/` |

### 第二优先级：强烈推荐

| 方案 | 用途 | 安装方式 |
|------|------|----------|
| **Advanced URI** | 从 CLI 触发 Obsidian 命令 | Obsidian 社区插件 |
| **Shell Commands** | Obsidian 响应文件变更 + 从 URI 执行 shell 命令 | Obsidian 社区插件 |

### 第三优先级：按需

| 方案 | 用途 | 何时需要 |
|------|------|----------|
| **NotesMD CLI** | 移动文件时更新内链 | 需要批量重组 wiki 结构时 |
| **Actions URI** | macOS Shortcuts 集成 | 想用 Shortcuts 自动化时 |

### selfOS 推荐集成架构

```
Claude Code (写文件)
    |
    v
wiki/ 目录 (直接文件操作)
    |
    +--> Obsidian 文件监控 (自动检测变更)
    |       |
    |       +--> Shell Commands 插件 (触发自定义响应)
    |
    +--> Local REST API (主动交互通道)
    |       |
    |       +--> Dataview 查询
    |       +--> 命令执行
    |       +--> 搜索
    |       +--> 强制刷新/打开文件
    |
    +--> obsidian:// URI (轻量触发)
            |
            +--> 打开特定笔记
            +--> Advanced URI 命令
            +--> Shell Commands URI 执行
```

### 关键工作流

**Claude Code 写入后刷新 Obsidian：**
```bash
# 1. Claude Code 直接写文件
echo "content" > wiki/concepts/new.md

# 2. 通过 REST API 通知 Obsidian 打开/刷新
curl -X POST https://127.0.0.1:27124/open/wiki/concepts/new.md \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" -k
```

**Claude Code 查询 Dataview：**
```bash
curl -X POST https://127.0.0.1:27124/search/ \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: application/vnd.olrapi.dataview.dql+txt" \
  -d 'TABLE tags, summary FROM "wiki/concepts" WHERE contains(tags, "attention") SORT updated DESC' -k
```

**从 CLI 触发 Graph View 刷新：**
```bash
curl -X POST https://127.0.0.1:27124/commands/graph:open/ \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" -k
```
