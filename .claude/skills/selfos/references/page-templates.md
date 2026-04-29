# Page Templates

## CLAUDE.md Schema Template

Write this to `{wiki-root}/CLAUDE.md` during `/wiki init`:

```markdown
<!-- llm-wiki -->
# Knowledge Base

This is an LLM-maintained wiki. The LLM writes and maintains all content in `wiki/`.
Human curates sources in `raw/` and directs exploration via queries.

## Directory Structure

- `raw/` — Immutable source documents. Never modify these.
  - `raw/assets/` — Downloaded images referenced by sources
- `wiki/` — LLM-generated articles. The LLM owns this layer entirely.
  - `wiki/index.md` — Master catalog of all pages with one-line summaries
  - `wiki/log.md` — Chronological record of all operations
  - `wiki/overview.md` — High-level synthesis of the entire knowledge base
  - `wiki/concepts/` — One article per concept/topic
  - `wiki/entities/` — One page per entity (person, org, tool, paper, dataset)
  - `wiki/sources/` — One summary per ingested source
  - `wiki/synthesis/` — Filed-back query outputs, comparisons, analyses

## Page Conventions

### YAML Frontmatter (required on every wiki page)

Every page MUST start with YAML frontmatter:

    ---
    title: "Page Title"
    type: concept | entity | source | synthesis
    created: YYYY-MM-DD
    updated: YYYY-MM-DD
    sources: ["source-slug-1", "source-slug-2"]
    tags: [tag1, tag2]
    summary: "One-line summary for the index"
    ---

### Cross-References

Use `[[page-name]]` syntax for internal links. When creating or updating a page,
check for opportunities to link to existing pages. Maintain bidirectional links.

### Source Citations

Important claims MUST cite their source: `(source: [[sources/source-slug]])`.
If a claim cannot be traced to a source, mark it: `(unsourced — verify)`.

### Conflict Handling

When new data contradicts existing wiki content:
1. Update the page with the new information
2. Add a `## Revision Notes` section documenting what changed and why
3. If genuine ambiguity, present both views with sources

## Workflows

### On Ingest
1. Read the source completely
2. Create `wiki/sources/<slug>.md` with summary, key takeaways, metadata
3. For each significant concept: create or update `wiki/concepts/<slug>.md`
4. For each significant entity: create or update `wiki/entities/<slug>.md`
5. Update all relevant pages with cross-references
6. Update `wiki/index.md` — add new entries, update summaries of modified pages
7. Append to `wiki/log.md`
8. If the source materially shifts the big picture, update `wiki/overview.md`

### On Query
1. Read `wiki/index.md` to identify relevant pages
2. Read relevant pages
3. Synthesize answer with page citations
4. If filing back: save to `wiki/synthesis/`, update index and log

### On Lint
1. Scan all wiki pages for: orphans, missing pages, stale claims, contradictions,
   missing frontmatter, uncited claims, concepts mentioned but lacking pages
2. Report findings with severity
3. Fix if authorized
```

## Source Page Template

```yaml
---
title: "{Source Title}"
type: source
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
sources: []
tags: []
summary: "{One-line summary}"
original_url: "{url if applicable}"
source_type: "article | paper | repo | dataset | book | video | podcast | note | thought | record"
notion_id: "{notion page id if from Notion}"
---
```

Sections:
- `## Summary` — 2-5 sentence summary
- `## Key Takeaways` — Bulleted list of main points
- `## Concepts` — Links to concept pages touched by this source
- `## Entities` — Links to entity pages mentioned

## Concept Page Template

```yaml
---
title: "{Concept Name}"
type: concept
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
sources: ["source-slug-1", "source-slug-2"]
tags: []
summary: "{One-line summary}"
---
```

Sections:
- `## Overview` — What this concept is, in 2-3 paragraphs
- `## Evolution` — Timeline of how this concept appeared in sources, with dates
- `## Related Concepts` — Links to related concept pages
- `## Open Questions` — Unresolved questions about this concept

## Entity Page Template

```yaml
---
title: "{Entity Name}"
type: entity
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
sources: ["source-slug-1"]
tags: []
summary: "{One-line summary}"
entity_type: "person | organization | tool | paper | dataset | project"
---
```

Sections:
- `## Overview` — Who/what this entity is
- `## Key Facts` — Bulleted factual information
- `## Connections` — Links to other entities and concepts
- `## Mentions` — Timeline of appearances in sources

## Synthesis Page Template

```yaml
---
title: "{Query or Analysis Title}"
type: synthesis
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
sources: ["source-slug-1", "source-slug-2"]
tags: []
summary: "{One-line summary}"
query: "{Original question that prompted this}"
---
```

Sections:
- `## Question` — The original query
- `## Analysis` — The synthesized answer
- `## Evidence` — Key evidence from wiki pages with citations
- `## Follow-up Questions` — Suggested next questions
