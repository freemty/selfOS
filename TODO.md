# selfOS — TODO

> 上次更新: 2026-04-10 session 结束时

## 当前状态

- **Private (demo branch)**: 829 sources, 44 concepts, 49 entities, richness 全标注
- **Public (main/origin)**: 9 虚构 demo 节点 + 骨架 + 3 user guides

## 高优先级

### Public Repo
- [ ] 扩展 demo 到 ~100 虚构节点（Alex Chen persona, 涵盖科研/生活/职业/文化）
- [ ] README 截图：Obsidian Graph View + Web Viewer + 终端交互动画
- [ ] 终端交互动画（参考 https://www.liruilong.cn/prope/ 或 asciinema）

### 写作
- [ ] selfOS blog — 回应 KnightNemo life-logging 论述（https://knightnemo.github.io/blog/posts/life_logging/），核心论点："怎么把 context 暴露进去"不是"给 AI 更多 context"。聚焦自我论述/自白这种抽象 context 的提取方法论。详见 `wiki/sources/thought-2026-04-10-selfos-blog-and-skill-as-context.md`

### 知识图谱质量
- [ ] 把 ~/.claude/skills/ 所有 skill.md 作为 source 导入 wiki（skill 反映个人风格/品味）
- [ ] richness=high 的 226 条增量深编译（目前只有轻量 frontmatter + 原文，按需扩充 Key Insights + Related Concepts）
- [ ] Cross-reference 密度不均：新 concept/entity 平均 3-6 links vs 旧页面 10-22 links，需要加厚
- [ ] 9 个 source 文件含 email 地址（yangyuanbo04@gmail.com），考虑脱敏

## 中优先级

### 数据源
- [ ] 推特书签导入：2096 条已同步到本地 SQLite（fieldtheory CLI），详见 `docs/specs/twitter-bookmarks-ingest.md`
- [ ] 微信聊天记录导入
- [ ] 定期 Claude.ai / Gemini 导出 cron

### 自动化
- [ ] `/wiki lint` 自动修复脚本（模糊匹配断裂链接）
- [ ] Source page PII 自动过滤

### Obsidian
- [ ] 装 3 个插件：Dataview + Marp Slides + Obsidian Git
- [ ] 配置 Graph View 着色分组

## 已完成 ✅

- [x] 全量编译 829 sources（Gemini 481 + Claude 88 + Notion 251）— 2026-04-10
- [x] Richness 标注 829/829 — 2026-04-10
- [x] 深度解析 226 条 high-richness → 20 entity + 8 concept 新建 — 2026-04-10
- [x] 6 条 Notion Thought Context Recovery — 2026-04-09/10
- [x] Repo 拆分: main (public) + demo (private, pre-push hook) — 2026-04-10
- [x] 4 个 selfOS skill 加绝对 wiki root — 2026-04-10
- [x] 3 个 user guides (graph viewer / import / obsidian) — 2026-04-10
- [x] CLAUDE.md public 版清理 — 2026-04-10
- [x] 73 个重复文件清理 — 2026-04-10
- [x] 两轮 code review + fix — 2026-04-10
