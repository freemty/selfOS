# Hacker News — Show HN

## Title
Show HN: selfOS – Compile notes, AI conversations, and bookmarks into a personal knowledge graph

## Text
I built a personal knowledge management system that "compiles" scattered personal data (Notion notes, Claude/Gemini conversations, Twitter bookmarks) into a structured, queryable wiki with an interactive knowledge graph.

Key differences from existing tools:

1. **Compilation, not RAG** — Sources are processed once into concept/entity pages with citations. Queries read compiled pages, not raw files.

2. **Context Recovery** — The AI interviews you to fill gaps in your knowledge base. Found a one-line note from 6 months ago? It asks what the context was.

3. **Knowledge graph visualization** — Interactive vis.js graph showing relationships between concepts, people, and tools.

Been using it daily for 11 months (800+ sources → 45 concepts, 27 entities). Built as a Claude Code skill.

Demo branch has sanitized real data you can explore.

MIT licensed: github.com/freemty/selfOS
