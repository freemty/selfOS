# Git Orphan Branch 切换导致文件丢失

> `git checkout --orphan` + 修改共享文件 + `git checkout -f` 回原分支会丢失 untracked 文件

## Problem

创建 template 分支时，`wiki/index.md` 等共享文件被改为骨架版。切回 private 分支时因冲突使用了 `git checkout -f`，导致之前 stash 的 untracked 文件（`docs/superpowers/specs/2026-04-28-todo-system-design.md` 等）在 pop 后消失。

## Cause

事件链：
1. `git stash push` — 保存了 modified files，但 untracked files 未被 stash（需要 `-u` 参数）
2. `git checkout --orphan template` → `git rm -rf .` — 清空 staging
3. 在 template 上修改 `wiki/index.md` 为骨架版并 commit
4. `git checkout private` 失败（`wiki/index.md` 冲突）
5. `git checkout -f private` — 强制切换，丢弃本地修改
6. `git stash pop` — 恢复了 modified files，但 untracked 文件不在 stash 里

根因：**`git stash push` 默认不保存 untracked 文件**。需要 `git stash push -u` 才能保存。

## Solution

### 预防

```bash
# 切分支前，stash 时加 -u 包含 untracked 文件
git stash push -u -m "pre-template-branch"
```

### 恢复（如果已丢失）

```bash
# 从 git 历史中找到文件最后存在的 commit
git log --all --oneline -- path/to/lost/file.md

# 从该 commit 恢复
git show <commit>:path/to/lost/file.md > path/to/lost/file.md
```

### 更安全的 orphan branch 工作流

```bash
# 1. stash 包含 untracked
git stash push -u -m "pre-orphan"

# 2. 创建 orphan
git checkout --orphan template
git rm -rf .

# 3. 从原分支 checkout 白名单文件（不修改原分支文件）
git checkout private -- .claude/skills/ scripts/ hooks/ ...

# 4. 创建新文件（骨架版）代替修改共享文件
# 用 Write 创建新的 wiki/index.md 而不是 Edit 原来的

# 5. commit template
git add -A && git commit -m "init: template"

# 6. 切回——不用 -f，因为没有冲突
git checkout private
git stash pop
```

## Commands

```bash
# 检查 stash 是否包含 untracked 文件
git stash show -u stash@{0}

# 列出 stash 中的 untracked 文件
git stash show --include-untracked stash@{0} | grep "^?"

# 从其他分支恢复文件
git show template:path/to/file > path/to/file
```

## Notes

- Date: 2026-04-29
- 发现方式：simplify review 的 quality agent 报告 CLAUDE.md 引用了两个不存在的文件
- 影响文件：`docs/superpowers/specs/2026-04-28-todo-system-design.md`, `docs/superpowers/plans/2026-04-28-todo-system.md`
- 恢复来源：template 分支的 sanitize commit（`0a035fc`）中保留了这些文件
