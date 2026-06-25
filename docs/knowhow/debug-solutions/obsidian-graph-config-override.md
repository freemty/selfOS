# Obsidian Graph View 配置被覆盖

> 外部修改 .obsidian/graph.json 会被运行中的 Obsidian 立即覆盖

## Problem

通过 Claude Code 或编辑器修改 `~/selfOS/.obsidian/graph.json`（Graph View 的着色/过滤/布局配置），保存后 Obsidian 立即用内存中的状态覆盖回去。配置永远不会生效。

## Cause

Obsidian 运行时持续监控 `.obsidian/` 目录，任何外部文件变更都会被 Obsidian 的内存状态覆盖。这是 Electron 应用的常见行为 — 配置文件是 Obsidian 的"输出"而非"输入"。

## Solution

**不要从外部修改 graph.json。** 必须在 Obsidian UI 内操作：

1. `Cmd+P` → "graph" → 打开 Graph View
2. 点左上角筛选图标
3. **Filter**: 输入 `-path:wiki/sources -path:raw`（隐藏 source 和 raw）
4. **Groups**: New group → `path:wiki/concepts` = 蓝色, `path:wiki/entities` = 橙色
5. **Display**: 打开 Arrows, 调大 Node size

配置会自动保存到 graph.json。

## Notes
- Date: 2026-04-07
- 适用于 Obsidian 1.12.7+
- 同理适用于 workspace.json, appearance.json 等 .obsidian/ 下的文件
