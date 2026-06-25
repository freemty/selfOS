# Synthesize Workflow

Scan the wiki for concept clusters that have enough source evidence to warrant a synthesis page, recommend the best candidates, and guide the user through writing one.

## When to Use

- User says `/wiki synthesize`
- Wiki has many sources but few synthesis pages (rule of thumb: synthesis count < 5% of source count)

## Steps

### 1. Scan for candidates

Read `wiki/index.md` to get the full concept list. For each concept, use its **frontmatter `sources` array length** as source count (avoid grep-scanning all source files):

```bash
# Fast scan using frontmatter, not full-text grep
for concept in wiki/concepts/*.md; do
  slug=$(basename "$concept" .md)
  title=$(grep "^title:" "$concept" | head -1 | sed 's/title: *"//;s/"$//')
  source_count=$(grep -c "source" <(grep "^sources:" "$concept") 2>/dev/null || echo 0)
  related=$(grep -c "\[\[concepts/" "$concept" 2>/dev/null)
  echo "$source_count $related $slug $title"
done | sort -rn | head -20
```

If `sources` array is empty/missing for many concepts, fall back to `grep -rl "$slug" wiki/sources/` but only for the top 20 by cross-ref count.

### 2. Score candidates

For each concept, compute a synthesis-readiness score:

| Factor | Weight | Measurement |
|--------|--------|-------------|
| Source density | 3x | Number of sources citing this concept |
| Cross-reference density | 2x | Number of `[[concepts/]]` links on the concept page |
| No existing synthesis | 1x | Check if `wiki/synthesis/` already has a page covering this topic |
| Recency | 1x | Has sources from the last 14 days (still active in user's thinking) |
| Multi-entity | 1x | Involves 3+ entities (synthesis is more valuable when it connects people/tools) |

Exclude concepts that already have a synthesis page covering the same ground.

### 3. Present top 5 candidates

```markdown
### 🔬 Synthesis 候选 Top 5

| # | Concept | Sources | Cross-refs | 最近活跃 | 推荐理由 |
|---|---------|---------|------------|---------|---------|
| 1 | [[concepts/post-training]] | 12 | 8 | ✓ | 三代范式演进，横跨 R1/V3/V4，多个 open questions 未综合 |
| 2 | [[concepts/agent-scaling]] | 9 | 6 | ✓ | env scaling + tool use + evaluation 三条线交汇 |
| ... | | | | | |

选一个编号，或者说你想综合什么。
```

### 4. User selects a topic

User picks a number or describes a custom topic.

### 5. Gather material

Read related pages with a budget cap:
1. The concept page itself
2. Sources in its `sources` array — **read Key Takeaways + Q&A 序列 sections only** (not full text). Cap at 15 sources; if more, prioritize `richness: high` tagged ones.
3. Linked `[[concepts/]]` and `[[entities/]]` — read Overview section only. Cap at 10.
4. Any existing synthesis pages that overlap — read in full (these are few).

Build a mental model of what's known, what's contradictory, and what's missing.

### 6. Propose synthesis structure

Present a proposed outline to the user:

```markdown
### 📝 Synthesis 大纲：{Topic}

**切入角度：** {what makes this worth synthesizing — a tension, an evolution, a surprising connection}

1. **{Section 1}** — {what it covers}
2. **{Section 2}** — {what it covers}
3. **{Open Questions}** — {unresolved tensions}

涉及 N 个 sources, M 个 concepts, K 个 entities。

这个角度可以吗？要调整什么？
```

Wait for user confirmation. Adjust if needed.

### 7. Write the synthesis

Create `wiki/synthesis/{slug}.md` using the Synthesis Page Template from `references/page-templates.md`.

Key writing principles:
- **Cross-source evidence**: Every claim cites 2+ sources when possible
- **Tensions and contradictions**: Don't smooth over disagreements — name them
- **Timeline**: If the topic evolved, show the evolution with dates
- **User's voice**: If the user had distinctive questions or reactions in the source material (check Q&A 序列 sections), weave those in — they reveal what matters to the user
- **Connections the user hasn't made**: The synthesis should surface non-obvious links between sources that weren't explicitly connected
- **Open questions**: End with what's still unresolved — these feed back into `/interview`

### 8. Update index + log + cross-references (parallel)

These three writes are independent — do all:
- **index.md**: add to `## Synthesis` section
- **log.md**: append `## [YYYY-MM-DD] synthesize | {Title}` with sub-bullets for sources consulted and key finding
- **concept page(s)**: add `(synthesized: [[synthesis/{slug}]])` near the top of Overview — signals "deeper treatment available"

## Edge Cases

- **Topic too narrow** (only 2-3 sources): Suggest the user wait for more material, or combine with an adjacent concept
- **Topic too broad** (covers half the wiki): Help the user narrow to a specific angle or tension
- **User proposes a custom topic not in candidates**: That's fine — skip the scan, go straight to step 5 (gather material)
- **Synthesis already exists for the topic**: Read it first. Ask: "update the existing one, or write a new angle?"
