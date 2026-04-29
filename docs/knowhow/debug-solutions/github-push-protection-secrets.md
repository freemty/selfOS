# GitHub Push Protection: Secrets in Git History

> 当 git 历史中包含 AWS keys 等 secrets 时，即使 orphan branch 也可能被 GitHub Push Protection 拦截

## Problem
`git push` 被 GitHub Push Protection (GH013) 拦截，报告 Amazon AWS Access Key ID 和 Secret Access Key 泄露。即使创建了 orphan branch（无历史），当前文件中仍包含明文 secrets。

## Cause
1. 对话导出文件（Gemini conversations）中包含了 AWS credentials 的讨论内容
2. Wiki source pages 引用了这些对话，也包含了 credentials
3. Orphan branch 只清除 git 历史，不清除当前文件内容中的 secrets

## Solution

### 方案 1：替换 secrets 为 REDACTED（推荐）
```bash
# 定位包含 secrets 的文件
grep -rn "AKIA" wiki/ raw/ --include="*.md" --include="*.json"
grep -rn "aws_secret" wiki/ raw/ --include="*.md"

# 替换 Access Key ID
sed -i '' 's/AKIA[A-Z0-9]\{16\}/AKIA**REDACTED**/g' <file>

# 替换 Secret Key（需要知道具体值）
sed -i '' 's/<secret-key-value>/**REDACTED**/g' <file>
```

### 方案 2：删除包含 secrets 的文件
如果文件本身不需要公开，直接删除比 REDACTED 更干净。

### 方案 3：Orphan branch 重建
如果 secrets 在历史 commit 中：
```bash
# 创建无历史的 orphan branch
git checkout --orphan clean-branch
git add -A
git commit -m "clean: no secrets in history"
git branch -D main
git branch -m main
git push origin main --force
```

### 完整清理流程
```bash
# 1. 定位所有 secrets
grep -rn "AKIA\|sk-proj\|sk-ant\|aws_secret" . --include="*.md" --include="*.json" --include="*.py"

# 2. 替换或删除
sed -i '' 's/具体密钥值/**REDACTED**/g' <files>

# 3. Orphan branch（清历史）
git checkout --orphan clean
git add -A
git commit -m "clean commit"
git branch -D main && git branch -m main

# 4. Push
git push origin main --force

# 5. 验证 remote
gh api "repos/OWNER/REPO/git/trees/main?recursive=1" \
  --jq '[.tree[].path]' | grep -i "secret\|key\|credential"
```

## Notes
- Date: 2026-04-08
- GitHub Push Protection 会扫描文件内容，不只是文件名
- 即使 orphan branch 也会被扫描当前 commit 的文件内容
- 旧 commit 中的 secrets 在 force push 后仍可能被 GitHub 缓存，需要联系 GitHub 支持彻底清除
- 建议在 `.gitignore` 中预防性地 ignore conversation export 目录
