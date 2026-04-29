# Changelog

## v0.5.0 - 2026-04-29

Initial template release.

### Included
- 11 skills: `/wiki` (ingest/query/lint/compile/sync/status), `/thought`, `/digest`, `/interview`, `/bookmark-chat`, `/complete`, `/todo`
- 3 reference workflow docs per complex skill (selfos: 5, selfos-completion: 1, todo: 3)
- Wiki skeleton: index, log, overview, templates, todo stacks
- Scripts: auto-ingest, interview-questions, wiki-search, extract-all-sources
- Hooks: auto-capture (Stop hook for passive context extraction)
- Viewer: graph visualization web app
- Docs: specs, plans, guides, knowhow runbooks
- Obsidian config: graph view groups, core plugins

### Getting Started
```
git clone <repo-url> ~/selfOS
cd ~/selfOS && ./setup.sh
# Then in Claude Code: /wiki ingest <url>
```
