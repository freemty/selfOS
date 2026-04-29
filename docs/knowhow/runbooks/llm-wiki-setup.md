# LLM Wiki 从零搭建 Runbook

> 基于 Karpathy LLM Wiki 模式搭建个人知识库的完整流程

## 前提

- Claude Code + Opus 4.6
- Node.js (npm)
- git

## Step 1: 创建 Skill

```bash
mkdir -p ~/.claude/skills/llm-wiki/{references,scripts}
# 写 SKILL.md (定义 /wiki 命令)
# 写 references/ (ingest/query/lint workflow + page templates)
# 写 scripts/wiki-search.sh
```

## Step 2: 初始化知识库

```bash
mkdir -p ~/knowledge-base/{raw/assets,wiki/{concepts,entities,sources,synthesis}}
cd ~/knowledge-base
# 写 CLAUDE.md (wiki schema)
# 写 wiki/index.md, wiki/log.md, wiki/overview.md
git init && git add -A && git commit -m "feat(wiki): initialize"
```

## Step 3: 导入数据源

### Notion Notes
```bash
# 通过 Notion MCP 批量查询 → 导出为 markdown
# 存到 raw/notion-notes/
```

### Claude.ai Conversations
```bash
# Claude.ai → Settings → Export → 下载 conversations.json
# 存到 raw/claude-conversations/{date}-export/
```

### Gemini Conversations
```bash
# Google Takeout → Gemini Apps → 下载
# 去重后存到 raw/gemini-conversations/
```

## Step 4: 提取 Source Pages

```bash
cd ~/knowledge-base
python3 scripts/extract-all-sources.py
# 生成 wiki/sources/ (notion- / cc- / gem- 前缀)
```

关键原则: 保留完整对话（用户+AI），不裁剪。

## Step 5: 编译 Concept/Entity Pages

分主题并行编译（避免 context explosion）:
- Research themes: RoPE, diffusion, agent, math
- Personal growth: PhD, 蒸馏, 关系, 健康
- Tools & culture: Claude Code, 政治, 文化, 创业

每个主题用独立 subagent，只读该主题相关的 source pages。

## Step 6: 安装搜索引擎

```bash
npm install -g @tobilu/qmd
qmd collection add ~/knowledge-base/wiki --name wiki
qmd context add qmd://wiki "知识库描述"
qmd embed
```

## Step 7: 安装 Obsidian

```bash
brew install --cask obsidian
# 打开 Obsidian → Open folder as vault → ~/knowledge-base/
# 装插件: Dataview, Marp Slides, Obsidian Git
# Graph View: filter `-path:wiki/sources -path:raw`, 加颜色分组
```

## Step 8: 安全检查

```bash
# .gitignore 排除 PII 文件
# git filter-repo 清除历史中的 PII (如果要 push)
```

## 日常使用

```bash
/wiki ingest <url>       # 添加新来源
/wiki query "问题"       # 查询知识库
/wiki lint               # 健康检查
/wiki compile            # 批量编译新来源
/wiki status             # 查看统计
```

## Notes
- Date: 2026-04-07
- 完整实现历史: ~/knowledge-base/ git log
- Skill 位置: ~/.claude/skills/llm-wiki/
- 参考: Karpathy gist, farzaa wiki-gen-skill
