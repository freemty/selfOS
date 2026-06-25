# Sync Workflow

Pull new/updated notes from Notion LifeOS → compile into wiki.

## Context

- Wiki root: resolve from the current repo root
- Sync state file: `docs/sync-state.json` (contains `database_id`, `last_sync`, `synced_notion_ids`)

## Steps

### 1. Read sync state

Read `docs/sync-state.json`. If missing, create with:
```json
{
  "database_id": "2f6fa7bc-ecd5-80d4-a356-d2335226ffe5",
  "last_sync": "2026-04-05T00:00:00Z",
  "synced_notion_ids": {}
}
```

### 2. Query Notion for new/updated notes

Use `mcp__notion__query-database` with:
- database_id: from sync state `database_id` field
- filter: `last_edited_time` after `last_sync`
- sorts: `last_edited_time` ascending
- page_size: 100

If response has `has_more: true`, continue with `start_cursor` from previous response until all pages are fetched.

### 3. Filter out already-synced notes

Compare returned page IDs against `synced_notion_ids` keys in state file.
Also grep `wiki/sources/notion-*.md` for existing `notion_id` fields as a fallback check.
Keep only pages that are genuinely new or have been edited since their last sync date.

### 4. For each new/updated note, fetch content

Use `mcp__notion__get-block-children` with the page ID to get the full body.
Reconstruct markdown from blocks:
- `paragraph` → plain text
- `heading_1/2/3` → `#/##/###`
- `bulleted_list_item` → `- `
- `numbered_list_item` → `1. `
- `code` → fenced code block
- `quote` → `> `
- `to_do` → `- [ ]` / `- [x]`
- Other block types (`callout`, `toggle`, `table`, `embed`, etc.) → best-effort or skip with a comment

Also extract page properties:
- `Note Type` → `source_type: "notion-{type}"` (fallback: `"notion-Note"`)
- `Tags` → `tags` array
- `Date` → `created` date
- `Last edited time` → `updated` date

### 5. Save raw source

Write to `raw/notion-notes/{title-slug}.md` with the original content.
This preserves the immutable source layer.

### 6. Compile into wiki

**Triage first**: separate notes into two groups:
- **Thin notes** (body empty or < 3 non-empty lines — title-only Thoughts):
  Create minimal `wiki/sources/notion-{date}-{slug}.md` with frontmatter only.
  Skip concept/entity identification and cross-referencing.
  Batch up to 30 per round.
- **Substantive notes** (3+ lines of body content):
  Run the full ingest workflow (read `references/ingest-workflow.md`).
  Batch ~5-10 per round.

For each note:
1. Create/update `wiki/sources/notion-{date}-{slug}.md` with YAML frontmatter including `notion_id` and `notion_url`
2. (Substantive only) Identify concepts and entities
3. (Substantive only) Create or update concept/entity pages with `[[wikilinks]]`
4. Update `wiki/index.md`
5. Append to `wiki/log.md`

### 7. Log

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] sync: Notion LifeOS → wiki
- **New notes**: {count}
- **Updated notes**: {count}
- **New concepts**: [list if any]
- **Updated concepts**: [list if any]
```

### 8. Update sync state

Update `docs/sync-state.json`:
- Set `last_sync` to current ISO timestamp
- Add processed page IDs to `synced_notion_ids` as `{"page-id": "YYYY-MM-DD"}` entries

### 9. Commit

```
git add wiki/ raw/notion-notes/ docs/sync-state.json
git commit -m "feat(wiki): sync {N} notes from Notion"
```

## Notes

- Short "Thoughts" notes (title-only or 1-2 lines) are valid — the title IS the content.
  They may be enriched later via `/complete` (interview skill).
- If a note was already synced but updated in Notion, update the existing `wiki/sources/` page
  rather than creating a duplicate. Add a `## Revision Notes` section.
- Deleted Notion pages are NOT detected by this workflow (Notion API does not return them).
  Use `/wiki lint` periodically to find orphaned source pages.
