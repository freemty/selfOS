# selfOS 完整版全量编译 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 ~900 条原始素材（491 Gemini + 108 Claude + ~300 Notion）全量编译进 wiki，形成完整知识图谱。

**Architecture:** 在当前 demo branch 上增量扩展。Phase 1 导入 raw 数据，Phase 2 用现有 `extract-all-sources.py` 提取为 source 页面（修改路径指向 selfOS），Phase 3 批量为每条 source 标注 richness + 提取 concept/entity 候选，Phase 4 扩展 concept/entity 网络，Phase 5 重建 index/overview。

**Tech Stack:** Python 3, Notion MCP API, bash, existing `scripts/extract-all-sources.py`

**Spec:** `docs/superpowers/specs/2026-04-10-full-compilation-design.md`

---

### Task 1: 保护 raw/ 不进 git

**Files:**
- Modify: `/Users/sum_young/selfOS/.gitignore`

- [ ] **Step 1: 添加 raw/ 到 .gitignore**

在 `.gitignore` 末尾添加：
```
# Raw source data — local only, not for GitHub
raw/notion-notes/
raw/gemini-conversations/
raw/claude-conversations/extracted/
```

- [ ] **Step 2: 验证**

Run: `cd /Users/sum_young/selfOS && echo "test" > raw/test-ignore.txt && git status | grep test-ignore; rm raw/test-ignore.txt`
Expected: 无输出（文件被 ignore）

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: gitignore raw/ to protect private data"
```

---

### Task 2: 导入 Gemini 对话到 raw/

**Files:**
- Create: `raw/gemini-conversations/` (491 .md files, 从 iCloud 复制)

- [ ] **Step 1: 创建目录并复制**

```bash
mkdir -p /Users/sum_young/selfOS/raw/gemini-conversations
cp "/Users/sum_young/Library/Mobile Documents/com~apple~CloudDocs/posts/gemini-all/"*.md /Users/sum_young/selfOS/raw/gemini-conversations/
```

- [ ] **Step 2: 验证数量**

Run: `ls /Users/sum_young/selfOS/raw/gemini-conversations/*.md | wc -l`
Expected: 491 (含 _all_conversations.md，提取脚本会自动跳过)

---

### Task 3: 导入 Claude 对话到 raw/

**Files:**
- Create: `raw/claude-conversations/conversations.json` (从 iCloud 复制)

- [ ] **Step 1: 创建目录并复制**

```bash
mkdir -p /Users/sum_young/selfOS/raw/claude-conversations
cp "/Users/sum_young/Library/Mobile Documents/com~apple~CloudDocs/posts/data-b2e261af-6cab-4074-ab20-418537fb2d7e-1775788209-54b68131-batch-0000/conversations.json" /Users/sum_young/selfOS/raw/claude-conversations/
```

- [ ] **Step 2: 验证**

Run: `python3 -c "import json; d=json.load(open('/Users/sum_young/selfOS/raw/claude-conversations/conversations.json')); print(len(d))"`
Expected: 108

---

### Task 4: 导入 Notion Notes 到 raw/

**Files:**
- Create: `raw/notion-notes/` (~300 .md files, 从 Notion API 拉取)
- Create: `scripts/export-notion-notes.py`

- [ ] **Step 1: 写 Notion 导出脚本**

创建 `scripts/export-notion-notes.py`：

```python
#!/usr/bin/env python3
"""
Export all pages from the Notion Notes database to raw/notion-notes/ as markdown.
Uses the Notion MCP approach: query-database → get-page → get-block-children.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DB_ID = "2f6fa7bc-ecd5-80d4-a356-d2335226ffe5"
OUTPUT_DIR = Path(os.path.expanduser("~/selfOS/raw/notion-notes"))


def slugify(text, max_len=80):
    text = text.lower().strip()
    text = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:max_len]


def notion_api(method, endpoint, body=None):
    """Call Notion API via curl (uses token from ~/.config/notion/token)."""
    token_path = Path.home() / ".config" / "notion" / "token"
    if token_path.exists():
        token = token_path.read_text().strip()
    else:
        token = os.environ.get("NOTION_API_KEY", "")

    headers = [
        "-H", f"Authorization: Bearer {token}",
        "-H", "Notion-Version: 2022-06-28",
        "-H", "Content-Type: application/json",
    ]
    url = f"https://api.notion.com/v1/{endpoint}"
    cmd = ["curl", "-s", "-X", method, url] + headers
    if body:
        cmd += ["-d", json.dumps(body)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def get_all_pages():
    """Paginate through database to get all pages."""
    pages = []
    cursor = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        resp = notion_api("POST", f"databases/{DB_ID}/query", body)
        pages.extend(resp.get("results", []))
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
        print(f"  Fetched {len(pages)} pages so far...")
    return pages


def get_page_blocks(page_id):
    """Get all blocks (content) of a page."""
    blocks = []
    cursor = None
    while True:
        endpoint = f"blocks/{page_id}/children?page_size=100"
        if cursor:
            endpoint += f"&start_cursor={cursor}"
        resp = notion_api("GET", endpoint)
        blocks.extend(resp.get("results", []))
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return blocks


def blocks_to_markdown(blocks):
    """Convert Notion blocks to simple markdown."""
    lines = []
    for block in blocks:
        btype = block.get("type", "")
        bdata = block.get(btype, {})

        if btype in ("paragraph", "quote", "callout"):
            rich_text = bdata.get("rich_text", [])
            text = "".join(rt.get("plain_text", "") for rt in rich_text)
            if btype == "quote":
                text = f"> {text}"
            if text.strip():
                lines.append(text)

        elif btype.startswith("heading_"):
            level = int(btype[-1])
            rich_text = bdata.get("rich_text", [])
            text = "".join(rt.get("plain_text", "") for rt in rich_text)
            lines.append(f"{'#' * (level + 1)} {text}")

        elif btype == "bulleted_list_item":
            rich_text = bdata.get("rich_text", [])
            text = "".join(rt.get("plain_text", "") for rt in rich_text)
            lines.append(f"- {text}")

        elif btype == "numbered_list_item":
            rich_text = bdata.get("rich_text", [])
            text = "".join(rt.get("plain_text", "") for rt in rich_text)
            lines.append(f"1. {text}")

        elif btype == "code":
            rich_text = bdata.get("rich_text", [])
            text = "".join(rt.get("plain_text", "") for rt in rich_text)
            lang = bdata.get("language", "")
            lines.append(f"```{lang}\n{text}\n```")

        elif btype == "bookmark":
            url = bdata.get("url", "")
            lines.append(f"- [{url}]({url})")

        elif btype == "embed":
            url = bdata.get("url", "")
            lines.append(f"- [embed]({url})")

        elif btype == "image":
            img = bdata.get("file", bdata.get("external", {}))
            url = img.get("url", "")
            lines.append(f"![image]({url})")

    return "\n\n".join(lines)


def export_page(page):
    """Export a single Notion page to markdown."""
    # Extract metadata
    props = page.get("properties", {})
    title_prop = props.get("Note", {}).get("title", [])
    title = "".join(t.get("plain_text", "") for t in title_prop) or "Untitled"

    date_prop = props.get("Date", {}).get("date", {})
    date = date_prop.get("start", "") if date_prop else ""
    if not date:
        date = page.get("created_time", "")[:10]

    note_type_prop = props.get("Note Type", {}).get("select", {})
    note_type = note_type_prop.get("name", "note") if note_type_prop else "note"

    page_id = page["id"]
    notion_url = page.get("url", "")

    # Get content
    blocks = get_page_blocks(page_id)
    body = blocks_to_markdown(blocks)

    # Build frontmatter
    slug = slugify(title)
    if not slug:
        slug = page_id[:8]
    filename = f"{date}-{slug}.md"

    content = f"""---
title: "{title}"
date: {date}
type: {note_type}
notion_id: "{page_id}"
notion_url: "{notion_url}"
---

{body if body else title}
"""
    return filename, content


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Querying database {DB_ID}...")
    pages = get_all_pages()
    print(f"Found {len(pages)} pages")

    exported = 0
    for i, page in enumerate(pages):
        try:
            filename, content = export_page(page)
            filepath = OUTPUT_DIR / filename
            # Dedup
            counter = 1
            base = filepath.stem
            while filepath.exists():
                filepath = OUTPUT_DIR / f"{base}-{counter}.md"
                counter += 1
            filepath.write_text(content, encoding="utf-8")
            exported += 1
            if (i + 1) % 50 == 0:
                print(f"  Exported {i + 1}/{len(pages)}...")
        except Exception as e:
            print(f"  ERROR on page {page.get('id', '?')}: {e}")

    print(f"\nExported {exported} Notion notes to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 运行导出**

Run: `cd /Users/sum_young/selfOS && python3 scripts/export-notion-notes.py`
Expected: "Exported ~300 Notion notes to .../raw/notion-notes"

- [ ] **Step 3: 验证数量**

Run: `ls /Users/sum_young/selfOS/raw/notion-notes/*.md | wc -l`
Expected: 250-350 range

---

### Task 5: 备份现有 wiki/sources/（保护 Context Recovery）

**Files:**
- No new files, just a safety git commit

- [ ] **Step 1: Commit 当前状态作为安全点**

```bash
cd /Users/sum_young/selfOS
git add -A wiki/
git commit -m "chore: safety checkpoint before full compilation — 70 sources + 6 context recoveries"
```

---

### Task 6: 修改提取脚本适配 selfOS 路径

**Files:**
- Modify: `/Users/sum_young/selfOS/scripts/extract-all-sources.py`

- [ ] **Step 1: 修改 main() 中的路径和去重逻辑**

修改 `extract-all-sources.py` 的 `__main__` 部分：

```python
if __name__ == '__main__':
    kb_root = Path(os.path.expanduser('~/selfOS'))
    output_dir = kb_root / 'wiki' / 'sources'

    # IMPORTANT: Do NOT clean old source pages — preserve existing 70 + Context Recovery
    # Only extract NEW sources that don't already exist
    existing_files = set(f.name for f in output_dir.glob('*.md'))
    print(f"Existing source pages: {len(existing_files)} (will skip duplicates)")
    print()

    total = 0

    # 1. Notion notes
    notion_dir = kb_root / 'raw' / 'notion-notes'
    if notion_dir.exists():
        total += extract_notion(notion_dir, output_dir)
    print()

    # 2. Claude conversations
    claude_dir = kb_root / 'raw' / 'claude-conversations'
    if claude_dir.exists():
        total += extract_claude(claude_dir, output_dir)
    print()

    # 3. Gemini conversations
    gemini_dir = kb_root / 'raw' / 'gemini-conversations'
    if gemini_dir.exists():
        total += extract_gemini(gemini_dir, output_dir)
    print()

    print(f"=== Total new: {total} source pages ===")
    print(f"=== Grand total: {len(list(output_dir.glob('*.md')))} source pages ===")
```

注意：**删除原脚本中 "Clean old source pages" 的 6 行代码**（约 L322-L326），改为上面的去重保护逻辑。

- [ ] **Step 2: 同时修改 extract_claude() 的 JSON 路径**

`extract_claude` 函数的调用参数从 `raw/claude-conversations/2026-04-05-export` 改为直接传 `raw/claude-conversations`（conversations.json 已在该目录下）。

- [ ] **Step 3: 运行提取**

Run: `cd /Users/sum_young/selfOS && python3 scripts/extract-all-sources.py`
Expected:
```
Existing source pages: 70 (will skip duplicates)
[Notion] Created: ~250-300 source pages
[Claude] Created: ~90-108 source pages
[Gemini] Created: ~487-491 source pages
=== Grand total: ~900 source pages ===
```

- [ ] **Step 4: 验证**

Run: `ls /Users/sum_young/selfOS/wiki/sources/*.md | wc -l`
Expected: ~850-950

Run: `head -15 /Users/sum_young/selfOS/wiki/sources/gem-2025-05-25-*.md | head -1` (spot check a Gemini page)

Run: `cat /Users/sum_young/selfOS/wiki/sources/notion-2026-03-19-*给cc造锤子*.md | head -30` (verify Context Recovery preserved)

- [ ] **Step 5: Commit**

```bash
cd /Users/sum_young/selfOS
git add wiki/sources/ scripts/extract-all-sources.py
git commit -m "feat: full compilation — ~900 source pages from Gemini/Claude/Notion"
```

---

### Task 7: 批量标注 richness + 提取 concept/entity 候选

**Strategy:** 用并行 subagent 分批处理。每批 ≤50 条新 source，每条只读 frontmatter + 前 200 行，标注 richness 并提取 concept/entity 关键词。

**Files:**
- Modify: `wiki/sources/*.md` (新增 richness 字段到 frontmatter)
- Create: `docs/compilation-candidates.json` (concept/entity 候选汇总)

- [ ] **Step 1: 写批量标注脚本**

创建 `scripts/batch-richness-tagger.py`：

```python
#!/usr/bin/env python3
"""
Scan wiki/sources/ for pages without richness tag.
Output a list of files grouped into batches of 50 for subagent processing.
"""
import re
import json
from pathlib import Path

sources_dir = Path.home() / "selfOS" / "wiki" / "sources"
files = sorted(sources_dir.glob("*.md"))

untagged = []
for f in files:
    content = f.read_text(encoding="utf-8")[:500]  # only frontmatter
    if "richness:" not in content:
        untagged.append(str(f))

print(f"Total source pages: {len(files)}")
print(f"Already tagged: {len(files) - len(untagged)}")
print(f"Need tagging: {len(untagged)}")

# Output batches
batch_size = 50
batches = [untagged[i:i+batch_size] for i in range(0, len(untagged), batch_size)]
print(f"Batches: {len(batches)}")

output = {"batches": batches, "total": len(untagged)}
Path.home().joinpath("selfOS/docs/richness-batches.json").write_text(
    json.dumps(output, indent=2, ensure_ascii=False)
)
print("Written to docs/richness-batches.json")
```

- [ ] **Step 2: 运行分批**

Run: `python3 /Users/sum_young/selfOS/scripts/batch-richness-tagger.py`
Expected: "Need tagging: ~830" / "Batches: ~17"

- [ ] **Step 3: 用并行 subagent 处理每批**

每个 subagent 的 prompt 模板：

```
读取以下 wiki/sources/ 文件（最多前 200 行）。
对每个文件：
1. 在 frontmatter 中添加 richness: high|medium|low
   - high: 包含独特判断、方向决策、人物评价、methodology、情绪爆发
   - medium: 有实质技术讨论但属于学习/问答性质
   - low: 纯翻译、格式转换、简单问答、无个人 insight
2. 提取可能的 concept 和 entity 关键词（只提取，不创建页面）
3. 输出 JSON 报告: {file: ..., richness: ..., concepts: [...], entities: [...]}

文件列表: [batch N files]
```

每批 50 条，共 ~17 批，可 3-5 个并行。

- [ ] **Step 4: 汇总候选并去重**

合并所有 subagent 输出为 `docs/compilation-candidates.json`：
```json
{
  "concepts": {"concept-name": {"count": N, "sources": [...]}},
  "entities": {"entity-name": {"count": N, "sources": [...]}}
}
```

- [ ] **Step 5: Commit**

```bash
git add wiki/sources/ docs/compilation-candidates.json scripts/batch-richness-tagger.py
git commit -m "feat: richness tagging + concept/entity candidate extraction"
```

---

### Task 8: 扩展 Concept/Entity 网络

**Files:**
- Create/Modify: `wiki/concepts/*.md` (新概念页面)
- Create/Modify: `wiki/entities/*.md` (新实体页面)
- Modify: existing concept/entity pages (补充 sources 列表)

- [ ] **Step 1: 从候选中筛选新概念/实体**

读取 `docs/compilation-candidates.json`，筛选规则：
- 出现 ≥3 次的候选创建新页面
- 已存在的概念/实体只更新 sources 列表
- 现有 16 concepts + 14 entities + 所有 Context Recovery 保持不变

- [ ] **Step 2: 批量创建新 concept 页面**

每个新 concept 用轻量模板：
```yaml
---
title: "Concept Name"
type: concept
created: 2026-04-10
updated: 2026-04-10
sources: ["source-slug-1", "source-slug-2", ...]
tags: [auto-extracted]
summary: "一句话摘要"
---

## Overview

（从 high-richness sources 中提取的概要）

## Related Concepts

- [[existing-concept]] — 关联说明
```

- [ ] **Step 3: 批量创建新 entity 页面**

同上，用 entity 模板。

- [ ] **Step 4: 更新现有页面的 sources 列表**

对现有 16 concepts 和 14 entities，把新 sources 中引用它们的 slug 添加到 frontmatter sources 列表。

- [ ] **Step 5: 织入 cross-references**

扫描所有 concept/entity 页面，补充 `[[link]]` 到相关页面。

- [ ] **Step 6: Commit**

```bash
git add wiki/concepts/ wiki/entities/
git commit -m "feat: expand concept/entity network from full compilation"
```

---

### Task 9: 重建 index + overview

**Files:**
- Modify: `wiki/index.md`
- Modify: `wiki/overview.md`
- Modify: `wiki/log.md`

- [ ] **Step 1: 重建 wiki/index.md**

读取所有 wiki/ 页面，生成完整目录。保持现有的分类结构（研究方法论、研究方向、AI与工具、个人成长），新增类别如需。Sources 部分按类型和时间统计。

- [ ] **Step 2: 重建 wiki/overview.md**

基于扩展后的 concept 网络重写全局综述。保留现有叙事结构，扩展新涌现的主题线。

- [ ] **Step 3: 追加 wiki/log.md**

```markdown
## [2026-04-10] Full compilation — ~900 sources
- **Input**: 491 Gemini (iCloud) + 108 Claude (iCloud export) + ~300 Notion (API)
- **Method**: extract-all-sources.py → batch richness tagging → concept/entity expansion
- **Output**:
  - wiki/sources/: 70 → ~900
  - wiki/concepts/: 16 → N
  - wiki/entities/: 14 → M
  - All 6 Context Recovery sessions preserved
```

- [ ] **Step 4: Final commit**

```bash
git add wiki/index.md wiki/overview.md wiki/log.md
git commit -m "feat: rebuild index/overview for complete knowledge graph (~900 sources)"
```

---

### Task 10: 验证完整性

- [ ] **Step 1: 数量检查**

```bash
echo "sources:" && ls wiki/sources/*.md | wc -l
echo "concepts:" && ls wiki/concepts/*.md | wc -l
echo "entities:" && ls wiki/entities/*.md | wc -l
echo "richness high:" && grep -l "richness: high" wiki/sources/*.md | wc -l
echo "richness medium:" && grep -l "richness: medium" wiki/sources/*.md | wc -l
echo "richness low:" && grep -l "richness: low" wiki/sources/*.md | wc -l
```

- [ ] **Step 2: Context Recovery 完整性**

验证 6 条 Context Recovery 的 source page 都保留了 `## Context Recovery` 段落：
```bash
grep -l "Context Recovery" wiki/sources/notion-2026-03-*.md
```
Expected: 至少 6 个文件

- [ ] **Step 3: 运行 /wiki lint 检查断链**

- [ ] **Step 4: Obsidian Graph View 验证**

打开 Obsidian，检查 Graph View 节点数量和连接密度。
