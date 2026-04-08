# Fieldtheory — Twitter/X 书签本地同步

> 用 fieldtheory CLI 把 Twitter 书签同步到本地 SQLite，供 Agent 查询/分类/可视化

## Problem
需要把 Twitter 书签导出到本地，便于 LLM agent 批量处理和分析。Twitter 官方没有书签 API，浏览器插件导出格式不统一。

## Cause
Twitter 书签没有公开 API。fieldtheory 通过读取 Chrome 的登录 session cookies 模拟请求。

## Solution

### 安装
```bash
npm install -g fieldtheory
```

### 同步（需代理）
```bash
export https_proxy=http://127.0.0.1:7890 && ft sync
```

**关键坑**: Node.js 的 `undici`（fieldtheory 底层 HTTP 库）不认 `https_proxy` 环境变量。必须用以下方式之一让流量走代理：
- 方案 A: Clash TUN 模式（全局透明代理）— 最可靠
- 方案 B: 在 shell 中 `export https_proxy` 然后运行（部分版本支持）
- 方案 C: Proxifier 等系统级代理工具

### 常用命令
```bash
ft stats                    # 统计概览（总量、作者、语言分布）
ft list --limit 20          # 列出最近 N 条
ft list --author @someone   # 按作者筛选
ft search "关键词"           # FTS5 全文搜索
ft show <id>                # 查看单条详情
ft classify                 # LLM 自动分类（需 claude CLI）
ft classify --regex         # 快速 regex 分类（无需 LLM）
ft classify-domains         # 按主题域分类
ft categories               # 分类分布
ft domains                  # 主题域分布
ft sample <category>        # 按分类抽样
ft viz                      # 终端仪表盘
```

### 数据位置
```
~/.ft-bookmarks/
├── bookmarks.db      # SQLite 数据库
└── bookmarks.jsonl   # JSONL 缓存
```

## Notes
- Date: 2026-04-07
- 前置条件: Chrome 必须登录 x.com
- macOS 没有 `shuf` 命令，随机抽取用 `python3 -c "import random; ..."`
- 同步是全量的，但支持增量（已有的不重复拉取）
- 2096 条书签约需 2-3 分钟（带代理）
