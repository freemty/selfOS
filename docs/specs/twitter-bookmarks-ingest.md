# 推特书签 → Wiki 导入流程

## 背景

推特书签是个人 taste 的高密度信号——收藏行为本身就是一种隐性偏好表达。
但书签全是别人的内容，直接 ingest 没意义。需要通过对话提炼出"为什么收藏"。

灵感来源：[@berryxia 推文](https://x.com/berryxia/status/2040568037385146496) — fieldtheory CLI

## 数据概览

- **工具**: fieldtheory CLI (`ft`)，npm 全局安装
- **总量**: 2096 条书签，1038 个不同作者
- **时间**: 2025-04-03 ~ 2025-09-24（约半年）
- **语言**: 英文 1128 / 中文 849 / 日文 15 / 其他
- **存储**: `~/.ft-bookmarks/` (SQLite + JSONL)
- **Top 作者**: @lidangzzz (114), @_akhaliq (48), @Morris_LT (40), @435hz (34), @janusch_patas (25)

## 流程

### Phase 1: 分类概览
- [ ] 跑 `ft classify` 自动分类（需要 claude CLI）
- [ ] 跑 `ft classify-domains` 按主题域分类
- [ ] `ft categories` + `ft domains` 查看分布
- [ ] 识别 top 5-10 个主题簇

### Phase 2: 逐条对话（核心）
- [ ] 按主题簇分批，每批 10-20 条
- [ ] 每条展示原文 → 问 3 个问题：
  1. 为什么收藏这条？触动了什么？
  2. 它和你的哪些兴趣/项目/想法有关？
  3. 你同意/不同意/想补充什么？
- [ ] 提炼出：偏好标签、观点立场、概念连接
- [ ] 对话产出保存到 `wiki/synthesis/bookmarks-{theme}.md`

### Phase 3: Wiki 合并
- [ ] 新概念 → `wiki/concepts/` 新页面
- [ ] 已有概念 → 更新、补充来源
- [ ] 新实体（人/工具/项目）→ `wiki/entities/`
- [ ] 更新 `wiki/overview.md` 中 taste/偏好相关段落
- [ ] 更新 `wiki/index.md`

### Phase 4: Taste Profile
- [ ] 汇总对话产出，生成 `wiki/synthesis/taste-profile.md`
- [ ] 内容：关注什么、为什么关注、审美偏好、思维倾向
- [ ] 交叉验证：书签偏好 vs wiki 中已有的自我认知

## 常用命令

```bash
# 基础
ft stats                          # 统计概览
ft list --limit 20                # 列出最近 20 条
ft list --author @someone         # 按作者筛选
ft search "关键词"                 # 全文搜索
ft show <id>                      # 查看单条详情

# 分类
ft classify                       # LLM 自动分类
ft classify-domains               # 按主题域分类
ft categories                     # 分类分布
ft domains                        # 主题域分布
ft sample <category>              # 按分类抽样

# 可视化
ft viz                            # 终端仪表盘
```

## 注意事项

- `ft sync` 需要代理（`export https_proxy=http://127.0.0.1:7890`），Node.js undici 不认系统代理
- Chrome 必须登录 x.com 才能 sync
- 书签内容是别人的，wiki 中只记录"我为什么关注这个"而非转述原文
- 尊重原作者，不大段复制推文内容
