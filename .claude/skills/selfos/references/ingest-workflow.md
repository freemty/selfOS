# Ingest Workflow

You are processing a new source for the LLM Wiki. Follow these steps precisely.

## HARD RULE: Source Page First

**NEVER create or update concept/entity pages without a source page.**

Before touching ANY concept or entity page, verify:
1. A `wiki/sources/{slug}.md` file has been written in this session
2. The source page has valid YAML frontmatter with `type: source`
3. The source slug is ready to be cited in `sources: [...]` arrays

This applies to ALL ingest modes — file, URL, or conversation.

## Source Modes

### Mode A: File or URL
- Source file: `{source_path}` or fetched URL content
- The document IS the source — read it, then create source page

### Mode B: Current Conversation (triggered when user says "记到 wiki" / "写入 selfos" / "ingest this" without a file/URL)
- The conversation itself IS the source
- Source page slug: `cc-YYYY-MM-DD-<topic-slug>`
- Source page MUST capture:
  - **User's full input (verbatim)**: 用户的完整原文必须原样保留在 source page 中，放在 `## Raw Input` 段落。不能只摘引用、不能改写、不能省略。这是不可篡改的原始记录。
  - **What happened**: the event/discussion that triggered the write
  - **Motivation layer**: WHY this matters — not just what was said, but the drive behind it
  - **Temporal context**: what was happening at this time (e.g., "3 days after receiving offer")
- Do NOT wait for the user to ask "对话本身存了吗" — this is automatic

## Context

- Wiki root: {wiki_root}
- CLAUDE.md schema: Read `{wiki_root}/CLAUDE.md` for conventions

## Steps

### 1. Read the source
- **Mode A**: Read the entire source document. Many sources (especially from Notion) are very short — sometimes just a title with 1-2 bullet points. That's fine.
- **Mode B**: The conversation up to this point is the source. Identify the key event, quotes, and motivation.

### 2. Create the source summary page (MUST complete before Step 3)
Write `wiki/sources/{slug}.md` using the Source Page Template.
The slug: lowercase, hyphenated, derived from title. Max 60 chars.

### 3. Identify concepts and entities
From the source, identify:
- **Concepts**: Abstract ideas, methods, patterns, frameworks, theories, recurring themes
- **Entities**: Concrete things — people, organizations, tools, papers, datasets, projects

Check `wiki/index.md` to see if pages already exist.

**GATE CHECK**: Confirm source page from Step 2 exists before proceeding.

### 4. Create or update concept pages
For each concept:
- If exists: read it, integrate new info, add source to `sources` array, update `updated` date, add to Evolution timeline
- If new: create using Concept Page Template
- `sources` array MUST include the slug from Step 2

### 5. Create or update entity pages
Same as concepts, using Entity Page Template.
- `sources` array MUST include the slug from Step 2

### 6. Cross-reference
Add `[[wiki-links]]` wherever pages reference each other. Ensure bidirectional linking.

### 7. Update index.md
For every page created or modified, ensure it has an entry in `wiki/index.md`.

### 8. Update log.md
Append: `## [YYYY-MM-DD] ingest | {Source Title}`

### 9. Update overview.md (if needed)
Only if the source materially changes the big picture.
