#!/usr/bin/env python3
"""recount-index.py — 自动回填 wiki/index.md 的所有括号计数。

为什么存在：index.md 里 `## Sources (N)`、`### People — X (N)` 这类计数过去靠
手工维护，容易滞后，尤其是批量导入或新增 source filename 前缀之后。本脚本按目录文件数 + 命名前缀分桶 + [[]] 条目数自动
重算，杜绝手填。幂等：连续两次运行，第二次应为 0 处改动。

用法（在 wiki root，即含 `wiki/` 的目录运行）：
    python3 scripts/recount-index.py            # dry-run，只打印将改动的计数
    python3 scripts/recount-index.py --write     # 落盘

回填规则：
  - 顶层 `## Sources/Concepts/Entities/Synthesis (N)` → 对应目录 *.md 文件数
  - Sources 来源桶（按文件名前缀）：
      Gemini=gem-*  Notion=notion-*  "Claude Code / Claude.ai"=cc-*+claude-*
      "External Blog Posts & Interviews"=blog-*  Other=其余
      五桶加总 == Sources 总数（自洽校验）
  - `### High Richness Highlights` 下 "N pages tagged" → richness:high 文件数
  - 其余 `### X (N)` 子区（Entities People 各类、Organizations、Tools 等）
    → 该标题到下一个 ##/### 之间的 `- [[` 行数
"""
import os, re, glob, sys

ROOT = "wiki"
WRITE = "--write" in sys.argv


def dir_count(d):
    path = f"{ROOT}/{d}"
    if not os.path.isdir(path):
        return 0
    return len([f for f in os.listdir(path) if f.endswith(".md")])


def main():
    if not os.path.isdir(ROOT):
        sys.exit(f"错误：当前目录下找不到 {ROOT}/ —— 请在 wiki root 运行")

    sources_total = dir_count("sources")

    # sources 命名前缀分桶
    from collections import Counter
    pref = Counter()
    sources_dir = f"{ROOT}/sources"
    if os.path.isdir(sources_dir):
        for f in os.listdir(sources_dir):
            if f.endswith(".md"):
                m = re.match(r"^([a-z]+)", f[:-3])
                pref[m.group(1) if m else "x"] += 1
    gem, notion = pref["gem"], pref["notion"]
    cc = pref["cc"] + pref["claude"]
    blog = pref["blog"]
    other = sources_total - gem - notion - cc - blog

    # richness: high
    rh = sum(
        1 for f in glob.glob(f"{ROOT}/sources/*.md")
        if re.search(r"richness:\s*high", open(f, encoding="utf-8", errors="ignore").read(800))
    )

    top = {
        "Sources": sources_total,
        "Concepts": dir_count("concepts"),
        "Entities": dir_count("entities"),
        "Synthesis": dir_count("synthesis"),
    }
    bucket = {
        "Gemini Conversations": gem,
        "Notion Notes": notion,
        "Other": other,
        "External Blog Posts & Interviews": blog,
    }

    lines = open(f"{ROOT}/index.md", encoding="utf-8").readlines()
    out, changes, i = [], [], 0
    while i < len(lines):
        l = lines[i]
        # 顶层 section
        m = re.match(r"^##\s+(Sources|Concepts|Entities|Synthesis)\s*\((\d+)\)\s*$", l)
        if m:
            n = top[m.group(1)]
            if int(m.group(2)) != n:
                changes.append(f"## {m.group(1)}: {m.group(2)}→{n}")
                l = f"## {m.group(1)} ({n})\n"
            out.append(l); i += 1; continue
        # cc-* 盲区桶（改名 + 计数）
        m = re.match(r"^###\s+Claude Code / Claude\.ai Conversations \(cc-\* \+ claude-\*\)\s*\((\d+)\)\s*$", l)
        if m:
            if int(m.group(1)) != cc:
                changes.append(f"### Claude Code bucket: {m.group(1)}→{cc}")
                l = f"### Claude Code / Claude.ai Conversations (cc-* + claude-*) ({cc})\n"
            out.append(l); i += 1; continue
        # 旧版未改名的 Claude.ai 桶 → 迁移到新桶名
        m = re.match(r"^###\s+Claude\.ai Conversations\s*\((\d+)\)\s*$", l)
        if m:
            changes.append(f"### Claude bucket renamed → cc-*+claude-* ({cc})")
            l = f"### Claude Code / Claude.ai Conversations (cc-* + claude-*) ({cc})\n"
            out.append(l); i += 1; continue
        # 其它 sources 来源桶
        m = re.match(r"^###\s+(.*?)\s*\((\d+)\)\s*$", l)
        if m and m.group(1) in bucket:
            n = bucket[m.group(1)]
            if int(m.group(2)) != n:
                changes.append(f"### {m.group(1)}: {m.group(2)}→{n}")
                l = f"### {m.group(1)} ({n})\n"
            out.append(l); i += 1; continue
        # richness 行
        m = re.match(r"^(\d+) pages tagged", l)
        if m:
            if int(m.group(1)) != rh:
                changes.append(f"richness: {m.group(1)}→{rh}")
                l = re.sub(r"^\d+", str(rh), l, count=1)
            out.append(l); i += 1; continue
        # 其余 ### 子区 → 数 [[ 行
        m = re.match(r"^###\s+(.*?)\s*\((\d+)\)\s*$", l)
        if m:
            j, cnt = i + 1, 0
            while j < len(lines) and not re.match(r"^#{2,3}\s", lines[j]):
                if re.match(r"^- \[\[", lines[j]):
                    cnt += 1
                j += 1
            if cnt > 0 and int(m.group(2)) != cnt:
                changes.append(f"### {m.group(1)}: {m.group(2)}→{cnt}")
                l = f"### {m.group(1)} ({cnt})\n"
            out.append(l); i += 1; continue
        out.append(l); i += 1

    if WRITE:
        open(f"{ROOT}/index.md", "w", encoding="utf-8").writelines(out)
    print(("[WRITTEN] " if WRITE else "[DRY-RUN] ") + f"{len(changes)} 处计数改动"
          + ("（加 --write 落盘）" if changes and not WRITE else ""))
    for c in changes:
        print("  ", c)


if __name__ == "__main__":
    main()
