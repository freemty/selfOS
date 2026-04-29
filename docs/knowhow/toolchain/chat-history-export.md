# AI 聊天记录导出方法

> Claude.ai / Gemini / Claude Code 的聊天记录导出与归档

## Claude.ai

- Web 版 (claude.ai): Settings → Account → Export Data → 邮件下载
- 导出格式: `conversations.json` (JSON array, 含 chat_messages)
- 每条消息有 `sender` (human/assistant), `text`, `created_at`
- `summary` 字段是 Claude 自动生成的对话摘要（高价值）
- **注意**: `users.json` 含 PII（邮箱、电话），不要 git 追踪

## Gemini

- 工具: Chrome 扩展 **Gemini Exporter**（Chrome Web Store 搜索安装）
- 打开 gemini.google.com → 点击扩展图标 → 导出为 Markdown
- 导出格式: 每个对话一个 `.md` 文件，文件名 `{YYYYMMDD}_{标题}_{hash}.md`
- `.md` 格式: `====` 分隔的 header (title/messages/created/url) + `--- User ---` / `--- Gemini ---` 交替
- 可能有重复条目（同标题不同 hash），需要去重

## Claude Code CLI

- 本地已有记录: `~/.claude/projects/` 下的 session 数据
- 不需要导出，但格式不是 markdown

## 提取脚本

统一提取脚本: `~/knowledge-base/scripts/extract-all-sources.py`

处理原则:
- **保留完整对话**（用户 + AI），不裁剪
- 用 `[我]` / `[Claude]` / `[Gemini]` 标注发言者
- Claude 的 `summary` 放在页面顶部作为 metadata
- Source page 保存到 `wiki/sources/` (前缀: `cc-` / `gem-` / `notion-`)

```bash
cd ~/knowledge-base
python3 scripts/extract-all-sources.py
# 自动处理三个数据源，输出到 wiki/sources/
```

## 归档位置

```
~/knowledge-base/raw/
├── claude-conversations/2026-04-05-export/  # Claude 原始导出
├── gemini-conversations/                     # Gemini .md + .json
└── notion-notes/                             # Notion 导出
```

## Notes
- Date: 2026-04-07
- Claude 导出建议每月一次（已设 cron 每月5号提醒）
- Gemini 需要手动 Google Takeout
- .gitignore 已配置排除 conversations.json / users.json / *.json (Gemini)
