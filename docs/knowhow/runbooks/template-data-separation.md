# Template / Data 分层管理

> 用 git orphan branch 把项目的 template 层（skill, scripts, docs）和 data 层（wiki 内容）分开维护

## Problem

单 repo 里 template 代码和个人数据混在一起，每次 commit 既有 skill 修改又有 wiki 内容变更。发布时无法直接把 repo 给 fork 用户——里面全是个人数据。

## Cause

selfOS 有三个层次的文件：

| 层 | 内容 | 变动频率 |
|---|------|---------|
| Template | `.claude/skills/`, `scripts/`, `hooks/`, `CLAUDE.md`, `setup.sh` | 低 |
| Schema | `wiki/templates/`, `wiki/index.md` 结构 | 极低 |
| Data | `wiki/sources/`, `wiki/concepts/`, `wiki/entities/`, `raw/` | 高 |

## Solution

### 创建 orphan template 分支

```bash
# 1. 保护当前工作
git stash push -m "pre-template-branch"

# 2. 创建无历史的 orphan 分支
git checkout --orphan template

# 3. 清空 staging
git rm -rf .

# 4. 从 private 分支 checkout 白名单文件
git checkout private -- \
  .claude/skills/ \
  scripts/ \
  hooks/ \
  CLAUDE.md \
  .gitignore \
  setup.sh \
  README.md \
  CHANGELOG.md \
  TODO.md \
  LICENSE \
  wiki/templates/ \
  wiki/tasks/ \
  docs/specs/ \
  docs/guides/ \
  docs/knowhow/ \
  docs/superpowers/specs/ \
  docs/superpowers/plans/ \
  viewer/ \
  .obsidian/

# 5. 创建骨架版 wiki 文件（清空数据，保留结构）
# wiki/index.md — 空分区骨架
# wiki/log.md — 空日志
# wiki/overview.md — 引导文案

# 6. template 专用 .gitignore 排除数据目录
cat >> .gitignore << 'EOF'
# Data layer — excluded from template branch
wiki/sources/
wiki/concepts/
wiki/entities/
wiki/synthesis/
raw/
docs/batch-*.json
docs/deep-batch-*.json
docs/*.jsonl
EOF

# 7. 提交
git add -A
git commit -m "init: selfOS template v0.5.0"

# 8. 回到 private
git checkout -f private
git stash pop
```

### 脱敏 checklist

template 分支提交前必须扫描：

```bash
# 扫描个人数据
grep -rn "你的真名\|你的邮箱\|/Users/你的用户名/" --include="*.md" .

# 常见泄漏点
# - skill 文件的 Wiki Root 绝对路径
# - workflow reference 中的示例（导师名/学校名）
# - CHANGELOG 的完整个人项目历史
# - TODO 中的个人邮箱和项目计划
# - specs/plans 中的硬编码路径和人名
# - .obsidian/workspace.json (UI 状态文件)
```

### 日常工作流

```
template 分支（功能开发）      private 分支（日常数据）
         │                              │
         │  新 skill / 改 script        │  /wiki ingest
         │  改 CLAUDE.md               │  /todo add
         │                              │
         └──── cherry-pick ────────────→│
                                        │
```

- 功能开发 → template 分支，cherry-pick 到 private
- 日常数据 → 直接在 private
- 发布 → push template 分支
- **不要 merge**（orphan branch 无共同祖先，会产生大量冲突）

## Commands

```bash
# 检查两个分支的文件数
git ls-tree -r template --name-only | wc -l
git ls-tree -r private --name-only | wc -l

# 比较共享文件一致性
for f in $(git ls-tree -r template --name-only); do
  t=$(git ls-tree template -- "$f" | awk '{print $3}')
  p=$(git ls-tree private -- "$f" 2>/dev/null | awk '{print $3}')
  [ "$t" != "$p" ] && echo "DIFF: $f"
done

# 确认 template 无泄漏
for f in $(git ls-tree -r template --name-only | grep -E '\.(md|sh|py)$'); do
  git show "template:$f" | grep -q "敏感词" && echo "LEAK: $f"
done
```

### 反向同步：private → template 批量更新

当 private 分支积累了大量 skill/script/doc 变更后，需要批量同步到 template。
不要用 cherry-pick（orphan 分支无共同祖先），用 checkout + 脱敏 + commit。

```bash
# 1. 保护当前工作
git stash push -m "pre-template-sync"

# 2. 切到 template
git checkout template

# 3. 从 private 拉取最新基础设施文件（覆盖 template 旧版本）
rm -rf .claude/skills/
git checkout private -- \
  .claude/skills/ \
  setup.sh \
  hooks/ \
  scripts/ \
  CLAUDE.md \
  docs/knowhow/runbooks/

# 4. 脱敏：替换绝对路径
find .claude/skills/ -name "*.md" -exec \
  sed -i '' 's|/Users/<你的用户名>/selfOS/|/Users/<username>/selfOS/|g' {} +
sed -i '' 's|/Users/<你的用户名>/selfOS/|/Users/<username>/selfOS/|g' \
  setup.sh CLAUDE.md

# 5. 脱敏：个人示例泛化（按需）
# grep -rn "你的真名\|导师名\|学校名" --include="*.md" .claude/skills/

# 6. 排除不该进 template 的文件
git rm --cached .playwright-mcp/* 2>/dev/null
echo ".playwright-mcp/" >> .gitignore

# 7. 提交
git add -A
git commit -m "feat: sync template vX.Y.Z — <变更摘要>"

# 8. 回到 private + 恢复
git checkout -f private
git stash pop
```

**频率建议**：每 1-2 周或每次大的 skill 重构后同步一次。

**脱敏 checklist**（每次同步必须跑）：

```bash
grep -rn "你的真名\|你的邮箱\|/Users/你的用户名/" \
  --include="*.md" --include="*.sh" --include="*.py" \
  .claude/skills/ setup.sh hooks/ scripts/ CLAUDE.md
```

## Sync History

| Date | Version | Changes |
|------|---------|---------|
| 2026-04-29 | v0.5.0 | 初始 template 分支创建，85 files |
| 2026-05-04 | v1.0.0 | Skill 重构同步（selfos→wiki, +wiki-help/interview/synthesize），CLAUDE.md 全面更新，删除 6 个 dead skills |

## Notes

- Date: 2026-04-29 (created), 2026-05-04 (updated)
- Case study: selfOS private(1300+ files) → template(~90 files) 分离
- 预期差异文件（by design）：.gitignore, wiki/index.md, wiki/log.md, wiki/overview.md, skill 内的绝对路径
- orphan branch 意味着 `git merge` 不可用，只能 checkout + 脱敏 + commit
- template 分支的 skill 文件路径用 `/Users/<username>/selfOS/` 占位，setup.sh 会在用户机器上自动替换
