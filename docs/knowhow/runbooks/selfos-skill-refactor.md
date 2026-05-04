# selfOS Skill 重构 Runbook

> Skill 体系膨胀后的审计、清理、重命名、职责正交化流程

## Problem

Skill 随时间自然膨胀：demo 遗留未清理、命名不统一（品牌前缀 vs 通用名）、职责交叉（多个 skill 做同一件事）。不及时整理会让 LLM 的 skill routing 变差——description 越多越模糊。

## Cause

三类常见债务：
1. **Demo 遗留** — 初始搭建时批量塞入的参考 skill，之后从未触发
2. **命名漂移** — 先建的用品牌前缀（selfos-xxx），后建的用通用名（thought/todo）
3. **职责耦合** — 一个 skill 塞了多个关注点（如 thought 同时做捕获+追问）

## Solution

### Step 1: 审计现有 skill

```bash
# 列出 repo 内所有 skill
ls .claude/skills/

# 对比全局 symlink
for skill in .claude/skills/*/; do
  name=$(basename "$skill")
  [ -L "$HOME/.claude/skills/$name" ] && echo "✅ $name" || echo "❌ $name — NO SYMLINK"
done

# 查找断链
find ~/.claude/skills -maxdepth 1 -type l ! -exec test -e {} \; -print
```

### Step 2: 检查使用记录

```bash
# 每个 skill 的 git history（创建+修改次数）
for skill in .claude/skills/*/; do
  name=$(basename "$skill")
  echo "--- $name ---"
  git log --oneline --follow -- ".claude/skills/$name/" | head -3
done

# wiki log 中的触发记录
grep -c "skill_name" wiki/log.md
```

判断标准：只有初始 commit + 全局 fix commit = 从未真正使用。

### Step 3: 决定动作

| 情况 | 动作 |
|------|------|
| 从未使用 + 不属于核心功能 | 删除（repo 文件 + 全局 symlink） |
| 命名不一致 | `mv` 重命名目录 + 更新 symlink |
| 职责交叉 | 划清边界：从 A 中移除属于 B 的逻辑 |
| 缺全局 symlink | `ln -s` 补上 |

### Step 4: 执行重命名

```bash
# 1. 重命名 repo 目录
cd .claude/skills && mv old-name new-name

# 2. 更新 skill.md 的 name 和 description 字段
# 3. 更新全局 symlink
cd ~/.claude/skills && rm old-name && ln -s /path/to/repo/.claude/skills/new-name new-name

# 4. 更新 references/ 子目录中的旧名引用
grep -rn "old-name" .claude/skills/new-name/references/
```

### Step 5: 更新下游引用

必须检查的地方：
- `CLAUDE.md` — skill 命令速查表、路径引用
- `references/*.md` — workflow 文件中的旧 skill 名/路径
- 其他 skill 的 "Not for" 段落
- 旧的大写 `SKILL.md` 残留（如果同时存在 skill.md 和 SKILL.md，删大写的）

```bash
# 全面扫描旧名残留
grep -rn "old-name" .claude/skills/ --include="*.md"
grep -n "old-name" CLAUDE.md
```

### Step 6: 验证

```bash
# 确认所有 skill 都有 symlink
for skill in .claude/skills/*/; do
  name=$(basename "$skill")
  [ -L "$HOME/.claude/skills/$name" ] && echo "✅ $name" || echo "❌ $name"
done

# 确认无断链
find ~/.claude/skills -maxdepth 1 -type l ! -exec test -e {} \; -print

# 确认无旧名残留
grep -rn "old-name" .claude/skills/ --include="*.md"
```

### Step 7: /simplify review

运行 `/simplify` 让三个 review agent 并行检查遗漏。

## Commands

```bash
# 核心三步
mv .claude/skills/old new                    # 重命名
rm ~/.claude/skills/old                       # 清旧 symlink
ln -s $(pwd)/.claude/skills/new ~/.claude/skills/new  # 建新 symlink
```

## Notes

- Date: 2026-04-29
- Case study: selfos(11 skills) → 5 skills（删 6 demo 遗留 + 重命名 selfos→wiki / selfos-completion→interview + 从 thought 和 digest 中移除交叉职责）
- 关键教训：重命名目录后 references/ 子目录里的旧名引用最容易遗漏，必须 grep 扫一遍
