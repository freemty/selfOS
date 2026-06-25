# Open Source Launch Checklist

> 从私有项目到公开 repo 的完整检查流程，确保无 PII/secrets 泄露

## Problem
将包含个人数据的项目开源时，容易遗漏敏感信息（secrets、PII、私人实体引用）。

## Cause
私有 repo 转公开时，开发者往往只关注代码而忽略数据文件、对话导出、wiki 内容中的敏感信息。

## Solution

### Pre-push Security Scan
```bash
# 1. Secrets 扫描
grep -rn "AKIA\|sk-proj\|sk-ant\|aws_secret\|api_key\|password\|token" . \
  --include="*.md" --include="*.json" --include="*.py" --include="*.yaml" \
  --exclude-dir=.git --exclude-dir=node_modules

# 2. PII 扫描（个人姓名、邮箱）
grep -rn "你的真名\|个人邮箱\|手机号" . --include="*.md" --exclude-dir=.git

# 3. 私人实体扫描
grep -rn "具体人名列表" . --include="*.md" --exclude-dir=.git

# 4. 本地路径扫描
grep -rn "/Users/\|/home/" . --include="*.md" --include="*.py" --exclude-dir=.git
```

### Branch 策略
```
main    — 纯工具骨架，空数据目录 + .gitkeep
demo    — 脱敏数据子集，展示系统运行效果
private — 完整个人数据，不 push（本地 branch 或 .gitignore）
```

### Main Branch 清理
```bash
# 用 orphan branch 创建干净的 main
git checkout --orphan clean-main
# 选择性添加文件（不要 git add -A）
git add viewer/ scripts/ tests/ README.md LICENSE requirements.txt .claude/skills/ .agents/skills/ CLAUDE.md AGENTS.md .gitignore
git add wiki/templates/ wiki/index.md wiki/log.md wiki/overview.md
git add docs/specs/ docs/knowhow/
git add setup.sh hooks/
git add wiki/tasks/
git add scripts/check_agent_parity.sh scripts/recount-index.py
bash scripts/check_agent_parity.sh
git commit -m "feat: clean scaffold-only main branch"
git branch -D main && git branch -m main
git push origin main --force
```

### Demo Branch 脱敏
1. 从 main 创建 demo branch
2. 添加脱敏数据子集
3. 替换私人姓名为首字母（"Alice Chen" → "A.C."）
4. 删除情绪日记、私人关系记录
5. 保留公开人物和技术内容
6. 用 orphan branch 确保历史干净

### Post-push 验证
```bash
# 验证 remote 无敏感文件
gh api "repos/OWNER/REPO/git/trees/main?recursive=1" \
  --jq '[.tree[].path] | map(select(test("敏感关键词"))) | length'
# 应该返回 0
```

### README 检查
- [ ] 截图/GIF placeholder 已替换
- [ ] GitHub username placeholder 已替换
- [ ] 无假链接（检查所有 URL 可达性）
- [ ] 技术栈描述准确（不引用未使用的库）
- [ ] 依赖声明完整（requirements.txt / package.json）

## Commands
```bash
# 完整一键验证
grep -rn "AKIA\|sk-proj\|aws_secret" . --include="*.md" --include="*.json" --exclude-dir=.git && echo "SECRETS FOUND!" || echo "clean"
grep -rn "/Users/" . --include="*.md" --include="*.py" --exclude-dir=.git && echo "LOCAL PATHS FOUND!" || echo "clean"
bash scripts/check_agent_parity.sh
```

## Notes
- Date: 2026-04-08
- GitHub Push Protection 会自动拦截已知 secret 格式（AWS keys, API tokens）
- 但不会检测 PII（姓名、邮箱）— 这需要手动扫描
- Orphan branch 替换后，旧 commit 在 GitHub GC 前仍可被特定 SHA 访问
