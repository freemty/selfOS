# Knowledge Base

This is an LLM-maintained wiki. The LLM writes and maintains all content in `wiki/`.
Human curates sources in `raw/` and directs exploration via queries.

## Directory Structure

- `raw/` — Immutable source documents. Never modify these.
  - `raw/assets/` — Downloaded images referenced by sources
  - `raw/notion-notes/` — Exported Notion notes
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

```yaml
---
title: "Page Title"
type: concept | entity | source | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["source-slug-1", "source-slug-2"]
tags: [tag1, tag2]
summary: "One-line summary for the index"
---
```

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

## Quick commands

### Wiki Operations

| Command | Purpose | Example |
|---------|---------|---------|
| `/wiki query "question"` | Search wiki + synthesize answer, optionally file back to synthesis/ | `/wiki query "evolution of my research direction"` |
| `/wiki ingest <path-or-url>` | Fetch webpage/PDF and compile into wiki (source + concept + entity) | `/wiki ingest https://arxiv.org/abs/xxx` |
| `/wiki lint` | Health check: broken links, orphan pages, missing citations, frontmatter errors | `/wiki lint` |
| `/wiki compile` | Batch compile unprocessed source files in raw/ | `/wiki compile` |
| `/wiki status` | Stats: page count, word count, recent activity | `/wiki status` |

### selfOS Completion (context recovery)

Skill: `.claude/skills/selfos-completion/`

| Command | Purpose |
|---------|---------|
| `/bookmark-chat` | Mixed mode — randomly pick a Twitter bookmark or a terse thought, recover context via conversation |
| `/complete` | Extract from context-poor notes only |
| `/interview` | Wiki asks you questions: open questions, thin pages, timeline gaps |
| `/bookmark-chat status` | Check progress |

### Auto-Capture (Chat Mode)

Stop hook automatically detects personal context in each Claude Code conversation
and silently saves valuable content as `wiki/sources/auto-*.md`.

### Search (qmd)

| Command | Purpose | Example |
|---------|---------|---------|
| `qmd search "keyword"` | BM25 keyword search (fastest) | `qmd search "attention mechanism"` |
| `qmd vsearch "semantic"` | Vector semantic search | `qmd vsearch "how to choose research direction"` |
| `qmd query "question"` | Hybrid BM25 + vector + LLM re-ranking (best quality) | `qmd query "key methodologies"` |
| `qmd search "xxx" -c wiki` | Search within a specific collection | |
| `qmd search "xxx" --json` | JSON output (for LLM consumption) | |

### Obsidian

| Action | Description |
|--------|-------------|
| Graph View | `Cmd+P` -> "graph". Filter: `-path:wiki/sources -path:raw` to hide source layer |
| Color Groups | Groups: `path:wiki/concepts` = blue, `path:wiki/entities` = orange |
| Quick Search | `Cmd+O` open file, `Cmd+Shift+F` global search |
| Dataview | Structured queries on frontmatter (requires plugin) |

## Specs

- `docs/specs/twitter-bookmarks-ingest.md` — Twitter bookmarks -> wiki import pipeline
- `docs/specs/2026-04-07-knowledge-graph-scaling.md` — Knowledge graph scaling plan

## Knowhow

- `docs/knowhow/toolchain/` — qmd, chat export, fieldtheory, Obsidian plugin guides
- `docs/knowhow/toolchain/obsidian-cli-integration.md` — Obsidian CLI/API integration survey
- `docs/knowhow/debug-solutions/` — Obsidian config and other debug solutions
- `docs/knowhow/runbooks/` — LLM wiki setup and operational runbooks
