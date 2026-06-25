# Ingest Workflow

You are processing a new source for the LLM Wiki. Follow these steps precisely.

## Context

- Wiki root: resolve via wiki skill.md Wiki Root rules (typically `~/selfOS/`)
- CLAUDE.md schema: Read `CLAUDE.md` in wiki root for page conventions

## Steps

### 1. Read the source
Read the entire source document. Note: many sources (especially from Notion) are very short — sometimes just a title with 1-2 bullet points. That's fine. The title IS the content.

### 2. Create the source summary page
Write `wiki/sources/{slug}.md` using the Source Page Template.
The slug: lowercase, hyphenated, derived from title. Max 60 chars.

**Format preservation rules:**
- ASCII diagrams, box-drawing art, alignment tables → wrap in ` ```text ` code block, preserve exact whitespace
- Code blocks with language tags → keep language tag and all content verbatim
- Multi-column layouts, monospace tables → keep as-is inside code blocks
- Never "describe" a diagram in prose when the original has the actual diagram — include both if needed
- For conversation-type sources: include user's full input in `## 完整原文`, preserving all formatting

**Q&A sequence extraction (conversation-type sources):**

Quick check: Is this a conversation-type source with 3+ substantive user questions? If no → skip this entire block, use `## Key Takeaways` instead.

When the source is a conversation where the user asks questions about a topic (paper, concept, event, etc.), the Q&A flow IS the main content — replace `## Key Takeaways` with `## Q&A 序列`. Don't have both.

Format — natural dialogue, separated by `---`:

```markdown
## Q&A 序列

[optional opening context — what triggered the conversation, first observation before questions started]

---

**用户：** [user's exact question, verbatim — keep the oral tone]

[answer in conversational tone, with tables/diagrams/code inline]

---

**用户：** [follow-up question]

[answer]

---
```

Rules:
- **`**用户：**` not `**Q1:**`** — use a dialogue speaker label, not numbered labels
- Preserve the user's exact phrasing — their questions reveal cognitive gaps and thinking patterns
- Keep questions that seem "off-topic" — tangential questions often expose the deepest learning needs
- **Answers: keep the conversational tone.** Don't rewrite into formal bullet points. Preserve vivid expressions (metaphors, analogies like "弹药库 vs 弹匣"), the natural "先问→追深→恍然大悟" flow, and any user insight/follow-up annotations. Only trim pure filler (repeated "那个"/"嗯"), never trim personality or surprise.
- If the answer included a diagram or code block, include it inline
- Order must match the original conversation flow — the sequence itself tells a story of deepening understanding
- **Don't restructure into Section→Subsection→Bullet format.** The dialogue flow IS the structure. No `### N. Title` numbered sections.
- **No separate summary section** (like "用户的核心追问" or "核心洞察") at the end — insights should appear where they naturally occurred in the dialogue
- Not every conversation needs this — only when the user is actively interrogating a topic (asking 3+ substantive questions). Short conversations still use `## Key Takeaways`.

### 3. Identify concepts and entities
From the source, identify:
- **Concepts**: Abstract ideas, methods, patterns, frameworks, theories, recurring themes
- **Entities**: Concrete things — people, organizations, tools, papers, datasets, projects

Check `wiki/index.md` to see if pages already exist. For entities (especially people),
also check the `aliases` field in existing entity frontmatter — names may appear as
Chinese, English, pinyin, nicknames, or GitHub usernames.

### 4. Create or update concept pages
For each concept:
- If exists: read it, integrate new info, add source to `sources` array, update `updated` date, add to Evolution timeline
- If new: create using Concept Page Template

### 5. Create or update entity pages
Same as concepts, using Entity Page Template.

### 6. Cross-reference
Add `[[wiki-links]]` wherever pages reference each other. Ensure bidirectional linking.

### 7. Update index.md + log.md (parallel)

These two writes are independent — do both:
- **index.md**: ensure every created/modified page has an entry. **Do NOT hand-edit the `(N)` counts** — after adding entries, run `python3 scripts/recount-index.py --write` from the wiki root to auto-backfill every bracket count (top-level sections, source buckets, People sub-groups). Idempotent; a second run reports 0 changes.
- **log.md**: append `## [YYYY-MM-DD] ingest | {Source Title}` with sub-bullets for created/updated pages and key insights

### 9. Update overview.md (if needed)
Only if the source materially changes the big picture.
