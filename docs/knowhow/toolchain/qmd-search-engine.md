# qmd 搜索引擎

> 本地 markdown 搜索引擎：BM25 + 向量 + LLM re-ranking，替代 grep

## 安装

```bash
npm install -g @tobilu/qmd
# 注意：不是 `qmd`（那是空壳包），是 `@tobilu/qmd`
qmd --version  # 确认安装
```

## 创建 Collection

```bash
qmd collection add ~/selfOS/wiki --name wiki
qmd context add qmd://wiki "描述你的知识库内容"
qmd embed  # 生成向量（首次较慢，后续增量）
```

## 搜索命令

```bash
qmd search "关键词" -n 10           # BM25 关键词（最快）
qmd vsearch "语义查询" -n 10        # 向量语义搜索
qmd query "自然语言问题" -n 10      # 混合 + re-ranking（最佳质量）
qmd search "xxx" -c wiki            # 限定 collection
qmd search "xxx" --json             # JSON 输出（给 LLM 用）
qmd search "xxx" --all --files      # 列出所有匹配文件
```

## 集成到 Claude Code Skill

在 `wiki-search.sh` 中优先用 qmd，fallback 到 grep：
```bash
if command -v qmd &> /dev/null; then
  qmd search "$QUERY" -n 10 -c wiki
else
  grep -r -i -F -l "$QUERY" "$WIKI_DIR" --include="*.md"
fi
```

## MCP Server 模式

```bash
qmd serve  # 启动 MCP server，可在 claude settings.json 中配置
```

## Notes
- Date: 2026-04-07
- 包名: `@tobilu/qmd` (npm), 作者 tobi (Shopify CEO)
- GitHub: tobi/qmd (18.8K stars)
- Karpathy 在 LLM Wiki gist 中推荐
