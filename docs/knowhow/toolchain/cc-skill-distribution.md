# Claude Code Skill 分发架构

> selfOS skill 的源文件管理、全局 symlink、fork 用户 onboarding 模式

## Problem

CC skill 系统要求 skill 放在 `~/.claude/skills/`（全局）或 `.claude/skills/`（项目级）。
当 skill 需要跟 repo 走且对 fork 用户可复现时，需要一套清晰的源/链接分离方案。

## Cause

CC 的 skill 加载机制：
1. 项目级 `.claude/skills/` 在该目录下自动加载（无需配置）
2. 全局 `~/.claude/skills/` 在任何目录都加载
3. 两者可以共存，全局的让 `/thought` 等命令在非 repo 目录也能用

## Solution

### 目录结构

```
repo/
├── .claude/skills/       # 源文件（跟 git 走）
│   ├── skill-a/skill.md
│   └── skill-b/skill.md
└── setup.sh              # 创建全局 symlink
```

### setup.sh 模式

```bash
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
for skill in skill-a skill-b; do
  ln -sf "$REPO_DIR/.claude/skills/$skill" ~/.claude/skills/$skill
done
```

关键点：
- 用 `-sf` 允许覆盖已有 symlink
- 检查 `-L` (symlink) 和 `-d` (directory) 避免覆盖非 symlink 目录
- 路径统一用 repo 的绝对路径（避免 macOS 大小写不敏感导致的路径不一致）

### skill.md frontmatter 规范

```yaml
---
name: skill-name          # 只用字母、数字、连字符
description: "Use when..." # 只描述触发条件，不描述 workflow
user-invocable: true       # 如果用户会直接 /skill-name 调用
---
```

**CSO 规则**：description 不能总结 workflow（"captures thought and interviews"），
只能描述 trigger（"Use when user wants to jot down a fleeting idea"）。
否则 Claude 会走 description shortcut 而不读全文。

### Hook 分发

Hook 脚本放在 `hooks/` 目录（跟 repo 走），setup.sh 打印手动注册指令。
不自动修改 `~/.claude/settings.json`（太危险）。

项目级 hook 可以放在 `.claude/settings.local.json`（只在 repo 目录生效）。

## Commands

```bash
# 创建 symlink
ln -sf /path/to/repo/.claude/skills/my-skill ~/.claude/skills/my-skill

# 检查 symlink 是否正确
readlink ~/.claude/skills/my-skill

# 检查断链
find ~/.claude/skills -maxdepth 1 -type l ! -exec test -e {} \; -print

# 验证 skill 被 CC 识别
# 在 CC 中看 skill 列表是否出现
```

## Notes

- Date: 2026-04-09
- Environment: macOS (APFS, case-insensitive by default)
- macOS 下 `/Users/x/selfos` 和 `/Users/x/selfOS` 指向同一目录，但 symlink 会保留创建时的大小写——统一用实际路径
