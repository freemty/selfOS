# Lint Workflow

You are running a health check on the LLM Wiki.

## Context
- Wiki root: {wiki_root}

## Steps

### 1. Scan all pages
Read every `.md` file in `wiki/`. For each page, check:

**Critical:**
- Has valid YAML frontmatter with all required fields
- No broken `[[wiki-links]]`

**Warning:**
- Orphan pages (no inbound links from any other page)
- Concepts mentioned in text but lacking their own page
- Missing cross-references
- Pages with very short content (< 50 words)

**Info:**
- Sources in `raw/` not yet ingested
- Potential duplicate pages (similar titles or overlapping content)
- Suggested new questions based on gaps and connections

### 2. Generate report
Output a structured report with stats, issues by severity, and suggested actions.

### 3. Fix if authorized
Ask: "Fix issues automatically?"
If yes: fix missing frontmatter, create stub pages, add cross-references, commit.

### 4. Log
Append to `wiki/log.md`.
