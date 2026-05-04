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

## Notes

- Date: 2026-04-29
- Case study: selfOS private(1219 files) → template(85 files) 分离
- 预期差异文件（by design）：.gitignore, wiki/index.md, wiki/log.md, wiki/overview.md
- orphan branch 意味着 `git merge` 不可用，只能 cherry-pick 单向同步
