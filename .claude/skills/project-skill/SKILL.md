---
name: project-skill
description: "Use when advising on project architecture, experiment history, codebase navigation, or research findings."
user-invocable: false
version: "v0 — auto-generated bootstrap, review recommended."
updated: 2026-04-07
---

# selfOS — Project Knowledge

> **LLM Wiki** — Karpathy-style personal knowledge base: three data sources (Notion/Claude/Gemini) compiled into a persistent, cross-referenced, LLM-maintained wiki. Obsidian as IDE, LLM as programmer, wiki as codebase.

---

## Project Overview & Current State

**Name:** selfOS
**Repository:** ~/knowledge-base (git, single branch `main`)
**Stage:** dev — operational but pre-public; no experiments running
**Motivation:** Implement Karpathy's "LLM Wiki" pattern (2026-04-04 gist) for personal knowledge management. The human curates raw source material; the LLM compiles, maintains, and evolves a structured wiki of concepts, entities, and cross-references. The deeper motivation is to externalize the author's implicit cognitive structure — making hidden cross-domain connections explicit, detecting context gaps, and enabling an iterative self-understanding loop.

**Current state (2026-04-07):**
- 44 concept pages, 27 entity pages, 798 source pages, 2 synthesis pages
- 3 data sources ingested: Notion (225 notes), Claude.ai (81 conversations), Gemini (490 conversations)
- ~15 MB wiki layer, ~56 MB raw layer
- Auto-capture Stop hook implemented (cc-session auto-ingest)
- `/wiki interview` gap-filling mode implemented
- qmd hybrid search integrated (BM25 + vector + LLM re-ranking)
- Obsidian vault configured for visualization
- 183 broken source reference links (known debt)
- PII still in git history (conversations.json/users.json) — needs git filter-repo before GitHub push

**Current experiment:** None
**skill_updated_at:** 2026-04-07

---

## Architecture

### Directory Structure

```
~/selfos/
├── CLAUDE.md              # Project schema + wiki conventions + commands
├── CHANGELOG.md           # Changelog (minimal — "Project initialized")
├── TODO.md                # Active task backlog (critical + obsidian + automation)
├── .gitignore             # PII exclusions (conversations.json, users.json, *.json)
│
├── raw/                   # IMMUTABLE source documents (56 MB)
│   ├── notion-notes/      # 227 exported Notion LifeOS notes (.md)
│   ├── gemini-conversations/  # 490 Gemini conversations (.md + .json)
│   ├── claude-conversations/  # Claude.ai exports (JSON, gitignored)
│   └── assets/            # Downloaded images
│
├── wiki/                  # LLM-GENERATED layer (15 MB)
│   ├── index.md           # Master catalog: 44 concepts, 27 entities, 798 sources
│   ├── overview.md        # High-level narrative synthesis
│   ├── log.md             # Chronological operation log
│   ├── concepts/          # 44 concept articles (research, personal, cultural)
│   ├── entities/          # 27 entity pages (18 people, 5 orgs, 4 tools)
│   ├── sources/           # 798 source pages (notion-*, cc-*, gem-*, auto-*)
│   └── synthesis/         # 2 query-driven synthesis pages
│
├── scripts/               # Python tooling
│   ├── extract-all-sources.py   # ETL: 3 data sources → wiki/sources/
│   ├── auto-ingest.py           # Stop hook: CC session → auto source page
│   └── interview-questions.py   # Gap scanner: generates targeted questions
│
├── docs/                  # Documentation & knowhow
│   ├── specs/             # Architecture specs (knowledge-graph-scaling, context-capture)
│   ├── papers/landscape.md # Literature survey: 12+ LLM Wiki implementations
│   ├── knowhow/           # Toolchain tips, debug solutions, runbooks
│   └── superpowers/plans/ # Implementation plans
│
├── viewer/                # Flask skeleton for experiment visualization
│   └── app.py
├── exp/                   # Experiment directory (empty — summary.md only)
├── slides/                # .gitkeep (empty)
├── sources/               # Legacy (1 orphan file)
└── .obsidian/             # Obsidian vault config
```

### Data Flow

```
[Human]
   │
   ├── curates raw/ (Notion exports, chat exports, URLs)
   ├── directs /wiki ingest, /wiki query, /wiki compile
   └── answers /wiki interview questions
   │
   ▼
[LLM (Claude)]
   │
   ├── scripts/extract-all-sources.py → raw/ → wiki/sources/ (ETL)
   ├── /wiki compile → wiki/sources/ → wiki/concepts/ + wiki/entities/ (compilation)
   ├── /wiki ingest <url> → WebFetch → source + concept + entity pages
   ├── /wiki query → index.md + qmd search → synthesis/ (query-driven)
   ├── /wiki interview → scripts/interview-questions.py → gap-filling Q&A
   └── Stop hook → scripts/auto-ingest.py → wiki/sources/auto-* (zero-friction)
   │
   ▼
[Wiki (Obsidian)]
   │
   └── Graph View visualization, Dataview queries, Marp slides
```

### Key Modules

| Module | Files | Purpose |
|--------|-------|---------|
| **ETL pipeline** | `scripts/extract-all-sources.py` | Extracts full conversations from 3 data sources into standardized source pages. Preserves complete dialogue with speaker labels. |
| **Auto-capture** | `scripts/auto-ingest.py` | Stop hook script. Detects personal context signals (regex on Chinese/English keywords, threshold >=2 matches), saves as `auto-*.md`, silent git commit. |
| **Gap scanner** | `scripts/interview-questions.py` | Scans wiki for: open questions (priority 1), thin pages <100 words (priority 2), vague entities (priority 2), timeline gaps <5 entries/month (priority 3). Outputs ranked JSON. |
| **Search** | `qmd` (external) | BM25 + vector + LLM re-ranking. Collection: `wiki`. Replaces grep as primary search. |
| **Viewer** | `viewer/app.py` | Flask skeleton for experiment dashboards (unused — no experiments yet). |

---

## System Cognition

### What Works

1. **Three-source fusion is powerful.** Notion (reflective), Gemini (technical learning), Claude (deep analysis) form complementary "thought strata" — each captures a different mode of thinking. No other LLM Wiki implementation does this.
2. **Full conversation preservation** (15 MB source layer) beats summarization. The raw dialogue contains context that summaries lose — tone, uncertainty, follow-up questions, tangential insights.
3. **Deep concept compilation** — 44 concepts with user's original quotes and cross-references, not mechanical filing. The wiki discovers cross-domain connections the author didn't explicitly make (e.g., "历史现场感" bridging political history and research taste).
4. **Character modeling** — Entity pages reconstruct complete portraits of people who matter to the author, with specific interactions and distilled learnings.
5. **Auto-capture via Stop hook** lowers friction to zero. Personal context flows into the wiki without conscious effort.
6. **Interview mode** inverts the interaction — wiki asks the user, not the other way around. Oral history is lower-friction than writing.

### What Doesn't Work (Yet)

1. **183 broken source reference links** — concept/entity pages reference `[[sources/...]]` slugs that don't match actual filenames. This is the largest known quality debt.
2. **PII in git history** — conversations.json and users.json were committed before .gitignore was set up. Blocks pushing to GitHub.
3. **No incremental compilation** — every recompile is full. No `.manifest.json` delta tracking. Adding one source requires understanding all existing concepts.
4. **Index is flat** — 44 concepts at same level. Will not scale beyond ~200 concepts. Needs hierarchical taxonomy (see knowledge-graph-scaling spec).
5. **Links are untyped** — `[[wikilinks]]` encode "related" but not how (extends? contradicts? uses?). Limits inference power.
6. **Synthesis layer is thin** — only 2 pages. Query-driven knowledge production is underutilized.
7. **Source page PII** — some source pages contain email addresses that need sanitization.

### Validated Hypotheses

- **H1: LLM can discover implicit cognitive structures.** CONFIRMED. The wiki found the "历史现场感" cross-domain bridge pattern autonomously.
- **H2: Multi-source fusion reveals what single sources miss.** CONFIRMED. Gemini extended the timeline 2 months earlier; Claude added political/cultural dimensions absent from Notion.
- **H3: Full dialogue > summaries for knowledge extraction.** CONFIRMED. Complete conversations allow re-extraction at different granularities.
- **H4: Zero-friction capture increases data flow.** CONFIRMED (design-level). Stop hook and interview mode both implemented; production validation pending.

### Active Assumptions

- **A1: qmd search quality is sufficient at 900 sources.** Not stress-tested at 5000+ sources.
- **A2: Obsidian is adequate as the visualization layer.** Graph View works but has no typed-edge support.
- **A3: CJK word count heuristic (~100 words threshold for "thin page") is calibrated correctly.** May need tuning.
- **A4: Personal context signal detection (>=2 regex matches) has acceptable precision.** False positive rate unknown.

---

## Technical Archive

### Key Technical Decisions

| Decision | Choice | Rationale | Alternatives Considered |
|----------|--------|-----------|------------------------|
| **Wiki format** | Markdown + YAML frontmatter in git | Obsidian-compatible, version-controlled, LLM-friendly, grep-able | SQLite DB, Neo4j graph, Notion API |
| **Search engine** | qmd (BM25 + vector + LLM re-ranking) | Best quality among tested options; MCP server mode; Karpathy-endorsed | grep (too crude), Elasticsearch (overkill), embeddings-only (poor recall on keywords) |
| **Source preservation** | Full dialogue with speaker labels | Enables re-extraction; dialogue context > summaries | Summary-only (information loss), User-messages-only (loses AI's structuring) |
| **Source page naming** | `{source}-{date}-{slug}.md` (prefix: notion/cc/gem/auto) | Sortable by date, source-type identifiable at glance | UUID-based (opaque), title-only (collision risk) |
| **Cross-references** | `[[wikilinks]]` Obsidian syntax | Native graph view, human-readable, bidirectional in Obsidian | HTML links (no graph), explicit JSON edges (parallel with text) |
| **Auto-capture** | Python script via Stop hook | Language-agnostic signal detection, silent git commit, zero UI | Claude-native (can't run post-session), Notion webhook (wrong direction) |
| **Gap detection** | Regex-based heuristic scanner | Fast, no LLM cost, runs locally | LLM-based semantic analysis (expensive, slower); manual review (doesn't scale) |
| **Compilation strategy** | Topic-parallel subagents | Avoids context explosion; each subagent reads only relevant sources | Sequential full-scan (context overflow), random batching (loses thematic coherence) |

### Rejected Alternatives with Rationale

- **Neo4j / graph database**: Overkill for <1000 nodes. Adds deployment complexity. A flat `_graph.json` suffices (see knowledge-graph-scaling spec).
- **Notion API as wiki backend**: Vendor lock-in, API rate limits, no git history, harder for LLM to manipulate programmatically.
- **Summary-only source pages**: Lost too much context. The author's exact words ("卧槽太爽了") carry signal that summaries strip away.
- **Real-time Obsidian plugin**: Electron apps override external file changes. Graph.json must be configured in-UI (confirmed debug finding).

### Parameter Choices

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Personal context signal threshold | >= 2 matches | Balance: 1 too noisy, 3 misses brief but meaningful content |
| Thin page threshold | < 100 words (CJK-aware) | Heuristic calibrated against existing pages; sub-100 indicates stub |
| Timeline gap threshold | < 5 sources/month | Based on observed density (~50-100/month for active months) |
| Auto-ingest max chars | 10,000 | Keeps source pages manageable; full conversations preserved in raw/ |
| Slug max length | 60 chars | Filename length constraint; enough for meaningful identification |

### Benchmark Baselines

No formal benchmarks yet. Informal quality metrics:
- Source page count: 798 (target: continuous growth)
- Concept coverage: 44 concepts across research, personal, cultural, political domains
- Broken link ratio: 183/798 = 22.9% (target: <5%)
- Synthesis output: 2 pages (target: 10+ after active querying)

---

## Experiment History Table

| Exp ID | Description | Status | Prediction | Actual | Key Finding | Calibration |
|--------|------------|--------|------------|--------|-------------|-------------|
| (none) | No experiments have been run yet. This is a knowledge management project, not an ML experiment project. | — | — | — | — | — |

*Note: The `exp/` directory and experiment framework (LabMate scaffolding) exist but are unused. The project's "experiments" are operational milestones documented in wiki/log.md and git history.*

### Operational Milestones (in lieu of experiments)

| Milestone | Date | Prediction | Actual | Key Finding |
|-----------|------|------------|--------|-------------|
| Initial compilation (225 Notion notes) | 2026-04-05 | Expect ~20 concepts | 30 concepts, 23 entities | More emergent structure than expected; ~80% of notes are title-only "Thoughts" |
| Claude.ai conversations (81) | 2026-04-05 | Expect incremental updates | 7 new concepts, 4 new entities | Revealed entirely new domains (politics, culture, business) absent from Notion |
| Gemini conversations (493) | 2026-04-05 | Expect mainly technical reinforcement | 5 new concepts, timeline extended 2 months | Gemini = "technical learning process" layer; complementary, not redundant |
| qmd search integration | 2026-04-07 | Expect better recall than grep | Confirmed; hybrid search with re-ranking | BM25 alone insufficient for semantic queries; vector component essential |
| Auto-capture hook | 2026-04-07 | Should capture ~30% of sessions | Not yet validated in production | Implementation complete; precision/recall unknown |
| Interview mode | 2026-04-07 | Should generate 20+ targeted questions | Script generates questions across 4 gap types | Gap scanner works; conversational framing requires LLM at runtime |

---

## Prediction Calibration

### Systematic Biases Observed

1. **Underestimation of emergent structure.** Expected ~20 concepts from 225 notes; got 30. Cross-domain connections (politics↔research, psychology↔ML) were not predicted.
2. **Underestimation of data source complementarity.** Assumed Claude conversations would mostly reinforce Notion. Instead, they opened 7 entirely new concept areas (politics, culture, business, fitness, psychology).
3. **Overestimation of technical homogeneity.** Assumed Gemini conversations would overlap heavily with Notion on technical topics. Instead, Gemini captured the "learning process" while Notion captured the "digested insight" — different layers of the same knowledge.

### Calibration Accuracy Trends

Too few data points for statistical trends. Three milestones show a consistent pattern of **underestimating complexity and richness** of the raw data. Future predictions should adjust upward for emergent structure.

---

## Engineering Lessons

> APPEND-ONLY — new entries go at the bottom.

### L1: Obsidian overrides external file changes (2026-04-07)
**Problem:** Editing `.obsidian/graph.json` via Claude Code or any editor is immediately overwritten by running Obsidian.
**Root cause:** Electron apps use in-memory state as source of truth; filesystem is output, not input.
**Fix:** All `.obsidian/` config must be changed via Obsidian UI.
**Ref:** `docs/knowhow/debug-solutions/obsidian-graph-config-override.md`

### L2: npm package naming trap — `qmd` vs `@tobilu/qmd` (2026-04-07)
**Problem:** `npm install -g qmd` installs an empty/wrong package.
**Fix:** Must use `@tobilu/qmd` (scoped package name).
**Ref:** `docs/knowhow/toolchain/qmd-search-engine.md`

### L3: PII leaks in chat exports (2026-04-05)
**Problem:** `conversations.json` and `users.json` from Claude.ai export contain emails, phone numbers, UUIDs. Committed to git before .gitignore was set up.
**Fix:** Added to .gitignore. Full cleanup requires `git filter-repo` (not yet done — blocks GitHub push).
**Lesson:** Always configure .gitignore BEFORE first commit with new data sources.

### L4: Source page slug collisions across data sources (2026-04-05)
**Problem:** Gemini source pages had two naming formats (`gem-20250525-*` vs `gem-2025-05-25-*`) causing 145 duplicates.
**Fix:** Standardized to `gem-YYYY-MM-DD-slug.md`; cleaned duplicates.
**Lesson:** Define slug format once and enforce it in the extraction script. Add collision counters (implemented: `counter = 1; while out_filepath.exists()`).

### L5: CJK word count is not `len(text.split())` (2026-04-07)
**Problem:** Chinese text has no spaces between words. `split()` treats entire Chinese sentences as single "words."
**Fix:** Count CJK characters individually + English words separately: `cjk_chars = len(re.findall(r'[\u4e00-\u9fff]', text))`.
**Ref:** `scripts/interview-questions.py` `_word_count()` function.

### L6: Python 3.9 compatibility — no `str | None` type hints (2026-04-07)
**Problem:** Scripts used `str | None` union syntax (Python 3.10+). Failed on Python 3.9.
**Fix:** Use `from __future__ import annotations` at top of file or `Optional[str]` from typing.

### L7: Context explosion during compilation (2026-04-05)
**Problem:** Compiling all 798 source pages at once exceeds context window.
**Fix:** Topic-parallel subagent architecture. Each subagent compiles one thematic cluster (research, personal, tools, culture). Merge results afterward.
**Lesson:** For large corpus operations, always partition by topic first.

### L8: Stop hook must never crash (2026-04-07)
**Problem:** Auto-ingest script runs as a Claude Code Stop hook. Any uncaught exception would disrupt the user's workflow.
**Fix:** Wrap entire `main()` in bare `except Exception: sys.exit(0)`. Never crash — silently fail.

---

## Active Prompt Versions & Trade-offs

This project does not use versioned prompts in the traditional `prompts/{component}/_v{NN}.md` sense. The "prompts" are embedded in:

| Component | Location | Current State | Trade-offs |
|-----------|----------|---------------|------------|
| **Wiki skill** | `.claude/skills/selfos/SKILL.md` + `references/` | Active | Defines /wiki commands and compilation workflow. Trade-off: skill references are external to this repo. |
| **CLAUDE.md** | `~/selfos/CLAUDE.md` | Active | Project schema, page conventions, workflow definitions. Trade-off: single file = easy to read but grows large. |
| **Auto-ingest signals** | `scripts/auto-ingest.py` lines 24-59 | v1 | 20 Chinese + 15 English regex patterns. Trade-off: high recall / unknown precision. No ML model — pure heuristic. |
| **Gap detection** | `scripts/interview-questions.py` | v1 | 4 gap types (open questions, thin pages, timeline gaps, vague entities). Trade-off: no cross-source contradiction detection (would require LLM semantic analysis). |
| **Source extraction** | `scripts/extract-all-sources.py` | v1 | Full dialogue preservation. Trade-off: 15 MB wiki/sources/ — large for git but enables re-extraction. |

---

## Quick Reference

### Commands

| Command | Purpose |
|---------|---------|
| `/wiki ingest <url>` | Fetch URL → create source + concept + entity pages |
| `/wiki compile` | Batch-compile unprocessed sources from raw/ |
| `/wiki query "问题"` | Search wiki → synthesize answer → optional file-back |
| `/wiki lint` | Health check: broken links, orphans, missing frontmatter |
| `/wiki status` | Stats: page count, word count, recent activity |
| `/wiki interview` | Oral history mode: wiki asks targeted questions |
| `qmd search "关键词"` | BM25 keyword search (fastest) |
| `qmd vsearch "语义"` | Vector semantic search |
| `qmd query "问题"` | Hybrid BM25 + vector + LLM re-ranking (best quality) |

### Key Paths

| What | Path |
|------|------|
| Project root | `~/selfos/` |
| Wiki layer | `~/selfos/wiki/` |
| Raw sources | `~/selfos/raw/` |
| Scripts | `~/selfos/scripts/` |
| This skill file | `.claude/skills/project-skill/SKILL.md` |
| Wiki skill | `.claude/skills/selfos/` |
| Specs | `docs/specs/` |
| Knowhow | `docs/knowhow/` |
| Literature survey | `docs/papers/landscape.md` |
| TODO backlog | `TODO.md` |

### Key Scripts

| Script | Usage |
|--------|-------|
| `python3 scripts/extract-all-sources.py` | Re-extract all sources from raw/ → wiki/sources/ (destructive: deletes existing) |
| `python3 scripts/interview-questions.py` | Output gap-analysis questions as JSON |
| `python3 scripts/auto-ingest.py` | Called by Stop hook; reads stdin for conversation text |

### Environment

- **Python:** 3.14
- **Node.js:** Required for qmd
- **Obsidian:** Vault at ~/selfos/
- **Git:** Local only (no remote configured; PII blocks push)
- **qmd:** `@tobilu/qmd` (npm global)

### Critical TODO Items

1. **P0:** Fix 183 broken source reference links (slug mismatch)
2. **P0:** git filter-repo to purge PII from history → push to GitHub private repo
3. **P1:** Obsidian plugins: Dataview + Marp Slides + Obsidian Git
4. **P1:** `/wiki lint` auto-fix script (fuzzy match broken links)
5. **P1:** WeChat chat import pipeline
6. **P2:** Incremental compilation (.manifest.json delta tracking)
7. **P2:** Hierarchical concept taxonomy (see knowledge-graph-scaling spec)
8. **P2:** Typed edges in concept frontmatter (extends/contradicts/uses)
