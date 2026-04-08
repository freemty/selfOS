# Ingest Workflow

You are processing a new source for the LLM Wiki. Follow these steps precisely.

## Context

- Wiki root: {wiki_root}
- Source file: {source_path}
- CLAUDE.md schema: Read `{wiki_root}/CLAUDE.md` for conventions

## Steps

### 1. Read the source
Read the entire source document. Note: many sources (especially from Notion) are very short — sometimes just a title with 1-2 bullet points. That's fine. The title IS the content.

### 2. Create the source summary page
Write `wiki/sources/{slug}.md` using the Source Page Template.
The slug: lowercase, hyphenated, derived from title. Max 60 chars.

### 3. Identify concepts and entities
From the source, identify:
- **Concepts**: Abstract ideas, methods, patterns, frameworks, theories, recurring themes
- **Entities**: Concrete things — people, organizations, tools, papers, datasets, projects

Check `wiki/index.md` to see if pages already exist.

### 4. Create or update concept pages
For each concept:
- If exists: read it, integrate new info, add source to `sources` array, update `updated` date, add to Evolution timeline
- If new: create using Concept Page Template

### 5. Create or update entity pages
Same as concepts, using Entity Page Template.

### 6. Cross-reference
Add `[[wiki-links]]` wherever pages reference each other. Ensure bidirectional linking.

### 7. Update index.md
For every page created or modified, ensure it has an entry in `wiki/index.md`.

### 8. Update log.md
Append: `## [YYYY-MM-DD] ingest | {Source Title}`

### 9. Update overview.md (if needed)
Only if the source materially changes the big picture.
