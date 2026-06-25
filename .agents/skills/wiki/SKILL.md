---
name: wiki
description: "Wiki CRUD — ingest sources, query compiled knowledge, lint, compile, synthesize. Triggers: /wiki, ingest, compile, query wiki, lint, synthesize, wiki status."
user-invocable: true
---

# /wiki — Wiki CRUD

Persistent, compounding knowledge base. Raw sources are compiled once into interlinked markdown — not re-derived on every query.

## Architecture

| Layer | Path | Owner |
|-------|------|-------|
| Raw sources | `raw/` | Human (immutable) |
| Wiki articles | `wiki/` | LLM (generated) |
| Schema | `AGENTS.md` | LLM (contains `<!-- llm-wiki -->` marker) |

## When to Use

- User says `/wiki`, mentions knowledge base, or wants to record/retrieve personal knowledge
- Ingesting articles, PDFs, conversations, or notes
- Querying across compiled knowledge with citations

**Not for:** capturing thoughts (`/thought`), managing tasks (`/todo`), context recovery/追问 (`/interview`), reviewing activity (`/digest`)

## Dispatching

Wiki root resolution (in order):
1. Current directory has `AGENTS.md` with `<!-- llm-wiki -->` marker
2. the nearest repo root containing the matching instruction file
3. Suggest `/wiki init`

**Important:** When CWD is not the wiki root, use paths relative to the resolved wiki root, or cd there before operating. Never assume `wiki/` resolves to the selfOS wiki from other directories.

## Commands

| Command | Summary | Full workflow |
|---------|---------|---------------|
| `/wiki init [path]` | Scaffold dirs + AGENTS.md + git init | Read `references/page-templates.md` |
| `/wiki ingest <url-or-path>` | Fetch/copy source → compile into wiki | Read `references/ingest-workflow.md` |
| `/wiki query "<question>"` | Search index → read pages → synthesize with citations | Read `references/query-workflow.md` |
| `/wiki lint` | Orphans, missing pages, stale claims, broken frontmatter | Read `references/lint-workflow.md` |
| `/wiki status` | File counts, word count, last 5 log entries | Direct (no reference needed) |
| `/wiki compile` | Batch-ingest all un-processed `raw/` files | Batches of ~10, commit per batch |
| `/wiki synthesize` | Scan for synthesis-worthy clusters → recommend → write | Read `references/synthesize-workflow.md` |
| `/wiki sync` | Pull new/updated Notion notes → compile into wiki | Read `references/sync-workflow.md` |
**For every command except status:** read the corresponding `references/` file for the full step-by-step workflow before executing.

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
