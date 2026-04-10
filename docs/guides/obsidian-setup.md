# Using with Obsidian

selfOS produces standard markdown with YAML frontmatter and `[[wikilinks]]`, which makes it fully compatible with [Obsidian](https://obsidian.md).

## Open as a Vault

1. Open Obsidian
2. Click **Open folder as vault** (or File -> Open Vault -> Open folder)
3. Select the selfOS repository directory
4. Obsidian will index all markdown files automatically

## Graph View

Obsidian has a built-in graph view that visualizes `[[wikilinks]]` between pages.

1. Press `Cmd+P` (Mac) or `Ctrl+P` (Windows/Linux) to open the command palette
2. Type "graph" and select **Graph view: Open graph view**

### Recommended Filters

By default the graph includes every markdown file in the repo (scripts, docs, raw data). To focus on just the wiki:

In the Graph View settings panel (gear icon), add these path filters:

```
-path:raw -path:docs -path:viewer -path:scripts -path:node_modules
```

This shows only pages under `wiki/`.

### Color Groups

Set up color groups to distinguish page types at a glance:

| Group | Query | Suggested Color |
|-------|-------|----------------|
| Concepts | `path:wiki/concepts` | Blue |
| Entities | `path:wiki/entities` | Orange |
| Sources | `path:wiki/sources` | Gray |
| Synthesis | `path:wiki/synthesis` | Green |

## Useful Plugins

These community plugins work well with selfOS wiki pages:

- **Dataview** -- Query YAML frontmatter across pages (e.g., list all entities with a specific tag, find pages updated in the last week)
- **Calendar** -- Timeline view of pages by their `created` date in frontmatter

Install plugins via Settings -> Community plugins -> Browse.

## Important Note

selfOS is **not** an Obsidian plugin. It is a Claude Code skill that produces Obsidian-compatible markdown. You edit and maintain the wiki through Claude Code commands (`/wiki ingest`, `/wiki query`, `/interview`, etc.), then view the results in Obsidian.

The two tools complement each other:
- **Claude Code** -- writes and maintains wiki content
- **Obsidian** -- reads, browses, and visualizes the wiki
