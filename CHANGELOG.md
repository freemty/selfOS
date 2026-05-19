# Changelog

## v0.6.0 - 2026-05-19

### New Skills
- `/transcribe` — Audio file → wiki source page. Uses Volcengine ASR for speech-to-text, outputs timestamped transcript, auto-ingests into wiki.
- `/de-ai` — Strip AI-flavored language (overclaiming, filler, hedge words) from any text.
- `/academic-writing` — 21 prose rules (Strunk & White / Orwell / Pinker) + 9 LLM anti-patterns. Context-triggered on paper drafts.
- `/paper-plot` — Publication-quality matplotlib templates with shared style (Palatino + STIX Math + 5-tier color palette).

### New Infrastructure
- `scripts/transcribe.py` — Volcengine ASR transcription script (async polling, speaker diarization, post-processing)
- `docs/knowhow/toolchain/volcengine-asr.md` — Volcengine ASR setup guide
- `docs/knowhow/runbooks/audio-transcribe-to-wiki.md` — End-to-end audio → wiki workflow
- `docs/blog-template/` — Blog article HTML template (index.html + style.css + script.js)

### Improvements
- All existing skills: minor path and wording fixes
- `CLAUDE.md`: updated command table with new skills

---

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
