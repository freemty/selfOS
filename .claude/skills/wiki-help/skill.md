---
name: wiki-help
description: "selfOS skill 速查。Triggers: /wiki-help, selfos help, 怎么用, 有哪些命令."
user-invocable: true
---

# selfOS 速查

直接输出下面的内容，不多说废话。

## 输出

```
心智模型：/thought 记 → /todo 管 → /interview 问 → /digest 看 → /wiki 存

┌─────────────┬────────────────────────────────────────────┐
│ /thought    │ 记一句话想法（纯写入，不追问）                    │
│             │ /thought <text>                            │
├─────────────┼────────────────────────────────────────────┤
│ /interview  │ 所有追问（新thought/旧thought/书签/wiki gaps）  │
│             │ /interview          wiki 主动追问            │
│             │ /interview thought  追问刚记的想法             │
│             │ /bookmark-chat      推特书签还原               │
│             │ /complete           旧 Notion thoughts       │
├─────────────┼────────────────────────────────────────────┤
│ /todo       │ 双轨待办                                     │
│             │ /todo add do "xxx"  加行动                   │
│             │ /todo add read "xx" 加阅读                   │
│             │ /todo today         日计划                    │
│             │ /todo done <ID>     完成                     │
│             │ /todo list          查看                     │
├─────────────┼────────────────────────────────────────────┤
│ /digest     │ wiki 动态回顾（纯统计，不追问）                  │
│             │ /digest             今日变化                  │
│             │ /digest week        本周回顾                  │
├─────────────┼────────────────────────────────────────────┤
│ /wiki       │ 知识库 CRUD                                  │
│             │ /wiki ingest <url>  导入源                   │
│             │ /wiki query "问题"   查询                    │
│             │ /wiki compile       批量编译 raw/             │
│             │ /wiki synthesize    写综合                   │
│             │ /wiki lint          健康检查                  │
│             │ /wiki status        统计                     │
└─────────────┴────────────────────────────────────────────┘
```
