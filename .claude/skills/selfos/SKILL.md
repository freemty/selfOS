---
name: selfos
description: "Use when ingesting sources into the personal knowledge base, querying compiled knowledge, running wiki health checks, or batch compiling raw sources. Triggers: /wiki, selfos, knowledge base, ingest, compile, query wiki. For context recovery (/interview, /bookmark-chat, /complete), use selfos-completion instead."
user-invocable: true
---

# selfOS Wiki

Persistent, compounding knowledge base. Raw sources are compiled once into interlinked markdown — not re-derived on every query.

## Architecture

| Layer | Path | Owner |
|-------|------|-------|
| Raw sources | `raw/` | Human (immutable) |
| Wiki articles | `wiki/` | LLM (generated) |
| Schema | `CLAUDE.md` | LLM (contains `<!-- llm-wiki -->` marker) |

## When to Use

- User says `/wiki`, mentions knowledge base, or wants to record/retrieve personal knowledge
- Ingesting articles, PDFs, conversations, or notes
- Querying across compiled knowledge with citations

**Not for:** project-specific docs (use CLAUDE.md), ephemeral task notes (use tasks), code documentation

## Dispatching

Wiki root resolution (in order):
1. Current directory has `CLAUDE.md` with `<!-- llm-wiki -->` marker
2. **`~/selfOS/` (absolute: `/Users/sum_young/selfOS/`)** — the canonical wiki location
3. Suggest `/wiki init`

**Important:** When CWD is not the wiki root, always use absolute paths (`~/selfOS/wiki/...`) or `cd ~/selfOS` before operating. Never assume `wiki/` resolves to the selfOS wiki from other directories.

## Commands

| Command | Summary | Full workflow |
|---------|---------|---------------|
| `/wiki init [path]` | Scaffold dirs + CLAUDE.md + git init | Read `references/page-templates.md` |
| `/wiki ingest <url-or-path>` | Fetch/copy source → compile into wiki | Read `references/ingest-workflow.md` |
| `/wiki query "<question>"` | Search index → read pages → synthesize with citations | Read `references/query-workflow.md` |
| `/wiki lint` | Orphans, missing pages, stale claims, broken frontmatter | Read `references/lint-workflow.md` |
| `/wiki status` | File counts, word count, last 5 log entries | Direct (no reference needed) |
| `/wiki compile` | Batch-ingest all un-processed `raw/` files | Batches of ~10, commit per batch |
| `/wiki sync` | Pull new/updated Notion notes → compile into wiki | Read `references/sync-workflow.md` |
**For every command except status:** read the corresponding `references/` file for the full step-by-step workflow before executing.

**Context recovery** (`/interview`, `/bookmark-chat`, `/complete`): use **selfos-completion** skill instead.

## Quick Reference

- **Source pages**: `wiki/sources/<slug>.md` — one per ingested source
- **Concept pages**: `wiki/concepts/<slug>.md` — abstract ideas, methods, patterns
- **Entity pages**: `wiki/entities/<slug>.md` — people, orgs, tools, papers
- **Synthesis pages**: `wiki/synthesis/<slug>.md` — filed-back query outputs
- **Cross-references**: `[[page-name]]` syntax, bidirectional
- **Citations**: `(source: [[sources/source-slug]])`
- **Commits**: `feat(wiki): <action> <title>`

## Common Mistakes

- Forgetting to update `wiki/index.md` after creating/modifying pages
- Writing source content directly into wiki pages instead of citing `[[sources/...]]`
- Skipping `wiki/log.md` append — every operation must be logged
- Not reading the `references/` workflow file before executing a command
