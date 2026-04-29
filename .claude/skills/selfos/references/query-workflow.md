# Query Workflow

You are answering a question against the LLM Wiki.

## Context
- Wiki root: {wiki_root}
- Question: {question}

## Steps

### 1. Search the wiki
Read `wiki/index.md` to identify relevant pages.
Run: `bash ~/.claude/skills/selfos/scripts/wiki-search.sh "{wiki_root}" "{keywords}"`

### 2. Read relevant pages
Read all pages that might contain relevant information. Prioritize:
1. Concept pages directly related to the question
2. Synthesis pages from prior queries on related topics
3. Source pages with detailed information
4. Entity pages for mentioned entities

### 3. Synthesize the answer
Write a thorough answer that:
- Cites specific wiki pages: `(see [[concepts/page-name]])`
- Distinguishes between well-sourced claims and inferences
- Notes gaps: "The wiki doesn't currently cover X"
- Suggests follow-up questions

### 4. Offer to file back
Ask: "File this back into the wiki as a synthesis page?"
If yes: save to `wiki/synthesis/{slug}.md`, update index and log, commit.
