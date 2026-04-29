# selfOS Launch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Package selfOS as a publishable open-source "Personal AI OS" with interactive knowledge graph visualization, bilingual README, demo data branch, and launch content — in 4 days.

**Architecture:** Main branch = empty scaffold with all tooling (skills, scripts, viewer). Demo branch = sanitized subset of real data (~50 sources, ~15 concepts, ~10 entities). Viewer uses Flask + vis.js for interactive knowledge graph. README is bilingual (EN/CN) in single file.

**Tech Stack:** Python (Flask, PyYAML), vis.js, HTML/CSS/JS, git branching

**Spec:** `docs/superpowers/specs/2026-04-07-selfos-launch-design.md`

---

## File Structure

### New files to create

| File | Responsibility |
|------|---------------|
| `viewer/build_graph.py` | Scan wiki/ frontmatter + `[[wikilinks]]` → `viewer/static/graph.json` |
| `viewer/static/graph.js` | vis.js rendering: nodes, edges, search, click panel, community filter |
| `viewer/static/style.css` | Graph viewer styling (dark theme, side panel, search bar) |
| `viewer/static/index.html` | Rewrite: knowledge graph viewer (replaces experiment viewer) |
| `viewer/app.py` | Rewrite: serve graph.json + static files |
| `README.md` | Bilingual EN/CN README with hero image, features, quick start |
| `LICENSE` | MIT license |
| `raw/README.md` | Instructions for users on what to put in raw/ |
| `wiki/templates/concept.md` | Template for new concept pages |
| `wiki/templates/entity.md` | Template for new entity pages |
| `wiki/templates/source.md` | Template for new source pages |

### Existing files to modify

| File | Change |
|------|--------|
| `CLAUDE.md` | Generalize: remove personal data references, make it a template |
| `.gitignore` | Add `graph.json` cache, remove personal-data-specific ignores from main |
| `viewer/app.py` | Full rewrite (39 lines → knowledge graph server) |
| `viewer/static/index.html` | Full rewrite (110 lines → graph viewer) |

---

## Day 1: Repo Restructure + Demo Branch

### Task 1: Create `build_graph.py` — wiki frontmatter parser + graph builder

This is the core data pipeline. It scans wiki/ markdown files, extracts frontmatter (YAML) and `[[wikilinks]]`, and outputs `graph.json`.

**Files:**
- Create: `viewer/build_graph.py`
- Read: `scripts/wiki_utils.py` (reuse `strip_frontmatter`, `extract_fm_field`)

- [ ] **Step 1: Write failing test for frontmatter extraction**

Create `tests/test_build_graph.py`:

```python
"""Tests for build_graph.py — wiki → graph.json pipeline."""
import json
import tempfile
from pathlib import Path

from viewer.build_graph import parse_page, build_graph, extract_wikilinks


def _write(tmp: Path, rel: str, content: str):
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_parse_page_concept():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write(tmp, "wiki/concepts/test-concept.md", """\
---
title: "Test Concept"
type: concept
created: 2026-01-01
updated: 2026-04-07
sources: ["source-a", "source-b"]
tags: [ml, research]
summary: "A test concept"
---

Some body with [[concepts/other-concept]] and [[entities/some-person]].
""")
        node = parse_page(tmp / "wiki/concepts/test-concept.md", tmp / "wiki")
        assert node["id"] == "concepts/test-concept"
        assert node["title"] == "Test Concept"
        assert node["type"] == "concept"
        assert node["source_count"] == 2
        assert set(node["tags"]) == {"ml", "research"}
        assert node["summary"] == "A test concept"


def test_extract_wikilinks():
    body = "See [[concepts/foo]] and [[entities/bar]] for details. Also [[concepts/foo]] again."
    links = extract_wikilinks(body)
    assert set(links) == {"concepts/foo", "entities/bar"}


def test_build_graph_edges():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write(tmp, "wiki/concepts/a.md", """\
---
title: "Concept A"
type: concept
created: 2026-01-01
updated: 2026-04-07
sources: []
tags: [ml]
summary: "Concept A"
---

Links to [[concepts/b]].
""")
        _write(tmp, "wiki/concepts/b.md", """\
---
title: "Concept B"
type: concept
created: 2026-01-01
updated: 2026-04-07
sources: []
tags: [ml, nlp]
summary: "Concept B"
---

Links back to [[concepts/a]].
""")
        graph = build_graph(tmp / "wiki")
        assert len(graph["nodes"]) == 2
        # wikilink edges: a→b and b→a
        wikilink_edges = [e for e in graph["edges"] if e["type"] == "wikilink"]
        assert len(wikilink_edges) == 2
        # shared tag edge: a↔b share "ml"
        tag_edges = [e for e in graph["edges"] if e["type"] == "shared_tag"]
        assert len(tag_edges) >= 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/sum_young/selfOS && python -m pytest tests/test_build_graph.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'viewer.build_graph'`

- [ ] **Step 3: Implement `build_graph.py`**

Create `viewer/build_graph.py`:

```python
"""Build knowledge graph JSON from wiki markdown frontmatter and wikilinks."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml


def extract_wikilinks(body: str) -> list[str]:
    """Extract unique [[wikilink]] targets from markdown body."""
    return list(set(re.findall(r'\[\[([^\]]+)\]\]', body)))


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter. Returns (metadata_dict, body)."""
    match = re.match(r'^---\n(.*?)\n---\n?(.*)', text, re.DOTALL)
    if not match:
        return {}, text
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, match.group(2)


def parse_page(filepath: Path, wiki_root: Path) -> dict:
    """Parse a single wiki page into a node dict."""
    text = filepath.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    rel = filepath.relative_to(wiki_root)
    page_id = str(rel.with_suffix(""))

    sources = meta.get("sources", [])
    if isinstance(sources, str):
        sources = [sources]

    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]

    # Determine node subtype for entities
    node_type = meta.get("type", "unknown")
    if node_type == "entity":
        # Infer subtype from path
        if "entities/" in str(rel):
            # Could be person/org/tool — check tags or default to entity
            tag_set = set(t.lower() for t in tags)
            if tag_set & {"person", "people", "researcher"}:
                node_type = "entity-person"
            elif tag_set & {"org", "organization", "company", "lab"}:
                node_type = "entity-org"
            elif tag_set & {"tool", "project", "software"}:
                node_type = "entity-tool"
            else:
                node_type = "entity-person"  # default for entities

    wikilinks = extract_wikilinks(body)

    return {
        "id": page_id,
        "title": meta.get("title", filepath.stem),
        "type": node_type,
        "source_count": len(sources),
        "tags": tags,
        "summary": meta.get("summary", ""),
        "wikilinks": wikilinks,
        "created": str(meta.get("created", "")),
        "updated": str(meta.get("updated", "")),
    }


def build_graph(wiki_root: Path) -> dict:
    """Build complete graph from wiki directory. Returns {nodes, edges}."""
    nodes = []
    edges = []
    node_ids = set()

    # Parse all markdown files in concepts/, entities/, synthesis/
    for subdir in ["concepts", "entities", "synthesis"]:
        dirpath = wiki_root / subdir
        if not dirpath.is_dir():
            continue
        for md_file in sorted(dirpath.glob("*.md")):
            node = parse_page(md_file, wiki_root)
            nodes.append(node)
            node_ids.add(node["id"])

    # Build wikilink edges
    for node in nodes:
        for target in node["wikilinks"]:
            if target in node_ids and target != node["id"]:
                edges.append({
                    "from": node["id"],
                    "to": target,
                    "type": "wikilink",
                })

    # Build shared-tag edges (weak links)
    tag_to_nodes: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        for tag in node["tags"]:
            tag_to_nodes[tag].append(node["id"])

    seen_tag_pairs = set()
    for tag, members in tag_to_nodes.items():
        if len(members) < 2:
            continue
        for i, a in enumerate(members):
            for b in members[i + 1:]:
                pair = tuple(sorted([a, b]))
                if pair not in seen_tag_pairs:
                    seen_tag_pairs.add(pair)
                    edges.append({
                        "from": pair[0],
                        "to": pair[1],
                        "type": "shared_tag",
                        "tag": tag,
                    })

    # Strip wikilinks from node output (only needed for edge building)
    for node in nodes:
        del node["wikilinks"]

    return {"nodes": nodes, "edges": edges}


def main():
    """CLI: python build_graph.py <wiki_root> [output_path]"""
    if len(sys.argv) < 2:
        print("Usage: python build_graph.py <wiki_root> [output.json]")
        sys.exit(1)

    wiki_root = Path(sys.argv[1])
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("viewer/static/graph.json")

    graph = build_graph(wiki_root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Graph built: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges → {output}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/sum_young/selfOS && python -m pytest tests/test_build_graph.py -v`
Expected: all 3 tests PASS

- [ ] **Step 5: Run build_graph on real wiki data to verify**

Run: `cd /Users/sum_young/selfOS && python viewer/build_graph.py wiki viewer/static/graph.json`
Expected: output like `Graph built: 72 nodes, ~200 edges → viewer/static/graph.json`

- [ ] **Step 6: Commit**

```bash
cd /Users/sum_young/selfOS
git add viewer/build_graph.py tests/test_build_graph.py
git commit -m "feat: add build_graph.py — wiki frontmatter → knowledge graph JSON"
```

---

### Task 2: Rewrite viewer — Flask + vis.js knowledge graph

**Files:**
- Rewrite: `viewer/app.py`
- Rewrite: `viewer/static/index.html`
- Create: `viewer/static/graph.js`
- Create: `viewer/static/style.css`

- [ ] **Step 1: Rewrite `viewer/app.py`**

```python
"""selfOS Knowledge Graph Viewer — Flask server."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder="static")
PROJECT_ROOT = Path(__file__).parent.parent
WIKI_ROOT = PROJECT_ROOT / "wiki"
GRAPH_PATH = Path(__file__).parent / "static" / "graph.json"


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/graph")
def get_graph():
    """Return the knowledge graph JSON. Rebuild if stale."""
    if not GRAPH_PATH.exists():
        _rebuild_graph()
    return send_from_directory(app.static_folder, "graph.json")


@app.route("/api/rebuild", methods=["POST"])
def rebuild():
    """Force rebuild the graph."""
    _rebuild_graph()
    data = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    return jsonify({"nodes": len(data["nodes"]), "edges": len(data["edges"])})


def _rebuild_graph():
    subprocess.run(
        [sys.executable, str(Path(__file__).parent / "build_graph.py"),
         str(WIKI_ROOT), str(GRAPH_PATH)],
        check=True,
    )


if __name__ == "__main__":
    if not GRAPH_PATH.exists():
        _rebuild_graph()
    app.run(debug=True, port=5001)
```

- [ ] **Step 2: Create `viewer/static/style.css`**

```css
/* selfOS Knowledge Graph Viewer — dark theme */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #0a0a0a;
    color: #e0e0e0;
    overflow: hidden;
    height: 100vh;
}

#header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 56px;
    background: #111;
    border-bottom: 1px solid #222;
    display: flex;
    align-items: center;
    padding: 0 1.5rem;
    z-index: 100;
    gap: 1rem;
}

#header h1 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #fff;
    white-space: nowrap;
}

#header .stats {
    font-size: 0.8rem;
    color: #666;
}

#search-box {
    flex: 0 1 300px;
    padding: 6px 12px;
    border: 1px solid #333;
    border-radius: 6px;
    background: #1a1a1a;
    color: #e0e0e0;
    font-size: 0.85rem;
    outline: none;
}

#search-box:focus { border-color: #4a9eff; }

#filter-bar {
    display: flex;
    gap: 0.5rem;
    margin-left: auto;
}

.filter-btn {
    padding: 4px 10px;
    border: 1px solid #333;
    border-radius: 4px;
    background: transparent;
    color: #888;
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.15s;
}

.filter-btn.active { border-color: currentColor; color: #fff; }
.filter-btn[data-type="concept"] { --accent: #4a9eff; }
.filter-btn[data-type="entity-person"] { --accent: #f59e0b; }
.filter-btn[data-type="entity-org"] { --accent: #34d399; }
.filter-btn[data-type="entity-tool"] { --accent: #a78bfa; }
.filter-btn.active { border-color: var(--accent); color: var(--accent); }

#graph-container {
    position: fixed;
    top: 56px;
    left: 0;
    right: 320px;
    bottom: 0;
}

#detail-panel {
    position: fixed;
    top: 56px;
    right: 0;
    width: 320px;
    bottom: 0;
    background: #111;
    border-left: 1px solid #222;
    padding: 1.5rem;
    overflow-y: auto;
    transition: transform 0.2s;
}

#detail-panel.hidden { transform: translateX(100%); }

#detail-panel h2 {
    font-size: 1rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0.5rem;
}

#detail-panel .type-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 0.7rem;
    font-weight: 500;
    margin-bottom: 0.75rem;
}

#detail-panel .summary {
    font-size: 0.85rem;
    color: #aaa;
    line-height: 1.5;
    margin-bottom: 1rem;
}

#detail-panel .connections h3 {
    font-size: 0.8rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

#detail-panel .connections ul {
    list-style: none;
    margin-bottom: 1rem;
}

#detail-panel .connections li {
    font-size: 0.85rem;
    padding: 4px 0;
    color: #4a9eff;
    cursor: pointer;
}

#detail-panel .connections li:hover { text-decoration: underline; }

.loading-overlay {
    position: fixed;
    inset: 0;
    background: #0a0a0a;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 200;
    font-size: 0.9rem;
    color: #666;
}
```

- [ ] **Step 3: Create `viewer/static/graph.js`**

```javascript
/* selfOS Knowledge Graph — vis.js renderer */

const TYPE_COLORS = {
    'concept': { bg: '#1a3a5c', border: '#4a9eff', font: '#4a9eff' },
    'entity-person': { bg: '#3a2a0a', border: '#f59e0b', font: '#f59e0b' },
    'entity-org': { bg: '#0a3a2a', border: '#34d399', font: '#34d399' },
    'entity-tool': { bg: '#2a1a3a', border: '#a78bfa', font: '#a78bfa' },
    'synthesis': { bg: '#2a2a1a', border: '#facc15', font: '#facc15' },
};

const DEFAULT_COLOR = { bg: '#222', border: '#555', font: '#888' };

let network = null;
let allNodes = [];
let allEdges = [];
let activeFilters = new Set(['concept', 'entity-person', 'entity-org', 'entity-tool']);

async function init() {
    const overlay = document.querySelector('.loading-overlay');
    try {
        const res = await fetch('/api/graph');
        const graph = await res.json();
        allNodes = graph.nodes;
        allEdges = graph.edges;

        document.querySelector('.stats').textContent =
            `${allNodes.length} nodes · ${allEdges.length} edges`;

        renderGraph();
        setupSearch();
        setupFilters();
    } catch (err) {
        overlay.textContent = 'Failed to load graph: ' + err.message;
        return;
    }
    overlay.style.display = 'none';
}

function renderGraph() {
    const container = document.getElementById('graph-container');

    const visibleIds = new Set(
        allNodes.filter(n => activeFilters.has(n.type)).map(n => n.id)
    );

    const nodes = new vis.DataSet(
        allNodes.filter(n => visibleIds.has(n.id)).map(n => {
            const c = TYPE_COLORS[n.type] || DEFAULT_COLOR;
            const size = Math.max(12, Math.min(40, 12 + (n.source_count || 0) * 2));
            return {
                id: n.id,
                label: n.title,
                size: size,
                color: { background: c.bg, border: c.border, highlight: { background: c.border, border: '#fff' } },
                font: { color: c.font, size: 11, face: 'system-ui' },
                shape: 'dot',
                borderWidth: 1.5,
                _data: n,
            };
        })
    );

    const edges = new vis.DataSet(
        allEdges
            .filter(e => visibleIds.has(e.from) && visibleIds.has(e.to))
            .map((e, i) => ({
                id: 'e' + i,
                from: e.from,
                to: e.to,
                color: { color: e.type === 'shared_tag' ? '#1a1a1a' : '#333', opacity: e.type === 'shared_tag' ? 0.3 : 0.6 },
                width: e.type === 'shared_tag' ? 0.5 : 1,
                dashes: e.type === 'shared_tag',
                smooth: { type: 'continuous' },
            }))
    );

    const options = {
        physics: {
            solver: 'forceAtlas2Based',
            forceAtlas2Based: { gravitationalConstant: -60, centralGravity: 0.005, springLength: 150 },
            stabilization: { iterations: 200 },
        },
        interaction: { hover: true, tooltipDelay: 100, zoomView: true, dragView: true },
        nodes: { chosen: { node: (values) => { values.borderWidth = 3; } } },
        edges: { chosen: false },
    };

    if (network) network.destroy();
    network = new vis.Network(container, { nodes, edges }, options);

    network.on('click', (params) => {
        if (params.nodes.length > 0) {
            showDetail(params.nodes[0]);
        } else {
            hideDetail();
        }
    });

    network.on('hoverNode', (params) => {
        container.style.cursor = 'pointer';
    });

    network.on('blurNode', () => {
        container.style.cursor = 'default';
    });
}

function showDetail(nodeId) {
    const node = allNodes.find(n => n.id === nodeId);
    if (!node) return;

    const panel = document.getElementById('detail-panel');
    panel.classList.remove('hidden');

    const c = TYPE_COLORS[node.type] || DEFAULT_COLOR;

    // Find connections
    const connections = allEdges
        .filter(e => e.from === nodeId || e.to === nodeId)
        .map(e => {
            const targetId = e.from === nodeId ? e.to : e.from;
            const target = allNodes.find(n => n.id === targetId);
            return target ? { id: targetId, title: target.title, type: e.type } : null;
        })
        .filter(Boolean);

    const wikilinks = connections.filter(c => c.type === 'wikilink');
    const tagLinks = connections.filter(c => c.type === 'shared_tag');

    panel.innerHTML = `
        <h2>${node.title}</h2>
        <span class="type-badge" style="background:${c.bg};color:${c.font}">${node.type}</span>
        <p class="summary">${node.summary || 'No summary'}</p>
        <div class="connections">
            ${wikilinks.length > 0 ? `
                <h3>Direct Links (${wikilinks.length})</h3>
                <ul>${wikilinks.map(l => `<li onclick="focusNode('${l.id}')">${l.title}</li>`).join('')}</ul>
            ` : ''}
            ${tagLinks.length > 0 ? `
                <h3>Related by Tag (${tagLinks.length})</h3>
                <ul>${tagLinks.map(l => `<li onclick="focusNode('${l.id}')">${l.title}</li>`).join('')}</ul>
            ` : ''}
        </div>
        <div style="margin-top:1rem;font-size:0.75rem;color:#555">
            Created: ${node.created || '?'} · Updated: ${node.updated || '?'}<br>
            Sources: ${node.source_count || 0} · Tags: ${(node.tags || []).join(', ') || 'none'}
        </div>
    `;
}

function hideDetail() {
    document.getElementById('detail-panel').classList.add('hidden');
}

function focusNode(nodeId) {
    network.focus(nodeId, { scale: 1.5, animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
    network.selectNodes([nodeId]);
    showDetail(nodeId);
}

function setupSearch() {
    const input = document.getElementById('search-box');
    input.addEventListener('input', () => {
        const q = input.value.toLowerCase().trim();
        if (!q) {
            network.unselectAll();
            hideDetail();
            return;
        }
        const match = allNodes.find(n =>
            n.title.toLowerCase().includes(q) ||
            (n.summary || '').toLowerCase().includes(q)
        );
        if (match) focusNode(match.id);
    });
}

function setupFilters() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        const type = btn.dataset.type;
        btn.classList.add('active');
        btn.addEventListener('click', () => {
            btn.classList.toggle('active');
            if (activeFilters.has(type)) {
                activeFilters.delete(type);
            } else {
                activeFilters.add(type);
            }
            renderGraph();
        });
    });
}

document.addEventListener('DOMContentLoaded', init);
```

- [ ] **Step 4: Rewrite `viewer/static/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>selfOS — Knowledge Graph</title>
    <link rel="stylesheet" href="/style.css">
    <script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
</head>
<body>
    <div id="header">
        <h1>selfOS</h1>
        <span class="stats">loading...</span>
        <input type="text" id="search-box" placeholder="Search nodes...">
        <div id="filter-bar">
            <button class="filter-btn" data-type="concept">Concepts</button>
            <button class="filter-btn" data-type="entity-person">People</button>
            <button class="filter-btn" data-type="entity-org">Orgs</button>
            <button class="filter-btn" data-type="entity-tool">Tools</button>
        </div>
    </div>
    <div id="graph-container"></div>
    <div id="detail-panel" class="hidden"></div>
    <div class="loading-overlay">Loading knowledge graph...</div>
    <script src="/graph.js"></script>
</body>
</html>
```

- [ ] **Step 5: Verify viewer runs with real data**

Run:
```bash
cd /Users/sum_young/selfOS
python viewer/build_graph.py wiki viewer/static/graph.json
python viewer/app.py
```
Expected: Server starts on `localhost:5001`, browser shows interactive knowledge graph with colored nodes.

- [ ] **Step 6: Commit**

```bash
cd /Users/sum_young/selfOS
git add viewer/app.py viewer/static/index.html viewer/static/graph.js viewer/static/style.css viewer/build_graph.py
git commit -m "feat: interactive knowledge graph viewer with vis.js"
```

---

### Task 3: Prepare main branch scaffold

Strip personal data to create the public-facing main branch structure.

**Files:**
- Create: `raw/README.md`
- Create: `wiki/templates/concept.md`, `wiki/templates/entity.md`, `wiki/templates/source.md`
- Create: `LICENSE`
- Modify: `CLAUDE.md` (generalize)
- Modify: `.gitignore`

- [ ] **Step 1: Create `raw/README.md`**

```markdown
# Raw Sources

Place your source documents here. selfOS will compile them into the wiki.

## Supported Sources

| Type | How to add |
|------|-----------|
| Notion export | Export as markdown → `raw/notion-notes/` |
| Claude.ai conversations | Export → `raw/claude-conversations/` |
| Gemini conversations | Export → `raw/gemini-conversations/` |
| Twitter bookmarks | Use `ft` CLI → `raw/twitter-bookmarks/` |
| PDFs / papers | Drop into `raw/papers/` |
| Any markdown | Drop into `raw/` |

## Then run

```
/wiki ingest raw/<your-file>
```

Or batch-compile everything:

```
/wiki compile
```
```

- [ ] **Step 2: Create wiki templates**

Create `wiki/templates/concept.md`:
```markdown
---
title: "Concept Title"
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
tags: []
summary: "One-line summary"
---

## Overview

What is this concept and why does it matter?

## Key Insights

-

## Related Concepts

- [[concepts/related-1]]

## Open Questions

-
```

Create `wiki/templates/entity.md`:
```markdown
---
title: "Entity Name"
type: entity
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
tags: [person|org|tool]
summary: "One-line summary"
---

## Overview

Who/what is this entity?

## Key Mentions

-

## Related

- [[entities/related-1]]
```

Create `wiki/templates/source.md`:
```markdown
---
title: "Source Title"
type: source
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
tags: []
summary: "One-line summary"
source_type: "article|conversation|note|paper"
---

## Summary

Brief summary of the source.

## Key Takeaways

-

## Concepts Mentioned

- [[concepts/concept-1]]
```

- [ ] **Step 3: Create `LICENSE`**

```
MIT License

Copyright (c) 2026 selfOS Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 4: Update `.gitignore` for public repo**

Append to existing `.gitignore`:
```
# Graph cache (rebuild with: python viewer/build_graph.py wiki)
viewer/static/graph.json

# Personal data (keep in private branch)
raw/notion-notes/
raw/claude-conversations/
raw/gemini-conversations/
raw/twitter-bookmarks/
wiki/sources/
wiki/concepts/
wiki/entities/
wiki/synthesis/
!wiki/sources/.gitkeep
!wiki/concepts/.gitkeep
!wiki/entities/.gitkeep
!wiki/synthesis/.gitkeep
```

Note: The demo branch will REMOVE these ignores so the demo data is visible.

- [ ] **Step 5: Create `.gitkeep` files for empty wiki dirs**

```bash
cd /Users/sum_young/selfOS
touch wiki/concepts/.gitkeep wiki/entities/.gitkeep wiki/sources/.gitkeep wiki/synthesis/.gitkeep wiki/templates/.gitkeep
```

- [ ] **Step 6: Commit**

```bash
cd /Users/sum_young/selfOS
git add raw/README.md wiki/templates/ LICENSE .gitignore wiki/**/.gitkeep
git commit -m "chore: add public scaffold — templates, LICENSE, raw README"
```

---

### Task 4: Create demo branch with sanitized data

**Files:**
- New branch: `demo`
- Curated subset of wiki/ data (脱敏)

- [ ] **Step 1: Create and switch to demo branch**

```bash
cd /Users/sum_young/selfOS
git checkout -b demo
```

- [ ] **Step 2: Modify `.gitignore` on demo branch — allow wiki data**

Remove the `wiki/sources/`, `wiki/concepts/`, `wiki/entities/`, `wiki/synthesis/` ignores that were added in Task 3. Keep everything else.

- [ ] **Step 3: Curate demo data**

Select ~50 source pages to keep. Criteria:
- Research methodology (公开内容): `人物蒸馏方法论`, `历史现场感`, `形式倒逼行动力`
- Tech concepts (公开): `sink与rope`, `agent-scaling`, `ai4ai`, `test-time-scaling`, `科研路线选择`, `生成模型谱系`
- Tool/AI concepts (公开): `claude-code实践`, `ai-native组织`, `build-in-public`, `lifeos与notion`
- Growth concepts (脱敏): `taste与ambition`, `motivation与直觉`, `自信与自卑`, `眼界与路径依赖`
- Public entities: `ilya-sutskever`, `anthropic`, `analemma`, `claude-code`, `lifeos`, `fars`

Delete everything else from wiki/ and raw/ on this branch. Keep index.md, overview.md, log.md but edit them to only reference retained pages.

**Sanitization rules:**
- Replace specific personal names in concept pages with initials (e.g., "Jiahao" → "J.", "Shangzhan" → "S.")
- Remove emotional diary entries
- Keep all research/methodology/tool content as-is

- [ ] **Step 4: Rebuild graph.json for demo data**

```bash
python viewer/build_graph.py wiki viewer/static/graph.json
```

On demo branch, UN-ignore `viewer/static/graph.json` so it ships with the demo.

- [ ] **Step 5: Commit demo branch**

```bash
cd /Users/sum_young/selfOS
git add -A
git commit -m "feat: demo branch with sanitized knowledge base (~50 sources, 15 concepts, 10 entities)"
```

- [ ] **Step 6: Switch back to main**

```bash
git checkout main
```

---

## Day 2-3: README + Content

### Task 5: Write bilingual README

**Files:**
- Create: `README.md` (overwrite if exists)

- [ ] **Step 1: Write README.md**

Full bilingual README following the structure from the spec:

1. Hero section with project name + tagline + screenshot placeholder `[screenshot]`
2. Language toggle: `[English](#selfos) | [中文](#selfos-中文)`
3. "What is selfOS" — one paragraph, not-RAG-but-compilation pitch
4. Demo GIF placeholder `[demo gif]`
5. Key Features (6 items from spec)
6. Worked Example table (from demo branch stats)
7. Quick Start (clone → demo → main → /wiki init)
8. How It Works (ASCII architecture diagram)
9. vs Graphify comparison table
10. Built With / Contributing / License
11. Full Chinese translation below divider

Note: Screenshot and GIF placeholders get replaced after the viewer is working and screenshots are captured.

- [ ] **Step 2: Commit README**

```bash
cd /Users/sum_young/selfOS
git add README.md
git commit -m "docs: bilingual README with features, quick start, architecture"
```

---

### Task 6: Capture screenshots and demo GIF

**Files:**
- Create: `docs/assets/graph-screenshot.png`
- Create: `docs/assets/demo.gif`

- [ ] **Step 1: Start viewer with demo data**

```bash
cd /Users/sum_young/selfOS
git stash  # if needed
git checkout demo
python viewer/build_graph.py wiki viewer/static/graph.json
python viewer/app.py &
```

- [ ] **Step 2: Capture screenshot of knowledge graph**

Open `http://localhost:5001` in browser. Arrange graph to show a compelling view (concepts clustered, entities orbiting). Take screenshot. Save to `docs/assets/graph-screenshot.png`.

Tools: macOS `Cmd+Shift+4` or `screencapture -w docs/assets/graph-screenshot.png`

- [ ] **Step 3: Record demo GIF**

Record a ~30 second screencast showing:
1. Running `/wiki ingest` on a source
2. Graph updating with new node
3. Running `/wiki query "..."` and getting cited answer
4. Running `/interview` and AI asking a question

Tools: macOS built-in screen recording → convert with `ffmpeg -i input.mov -vf "fps=10,scale=800:-1" docs/assets/demo.gif`

- [ ] **Step 4: Update README with real image paths**

Replace `[screenshot]` and `[demo gif]` placeholders with:
```markdown
![Knowledge Graph](docs/assets/graph-screenshot.png)
![Demo](docs/assets/demo.gif)
```

- [ ] **Step 5: Switch back to main, commit assets**

```bash
git checkout main
mkdir -p docs/assets
# copy screenshots from demo branch or re-capture
git add docs/assets/ README.md
git commit -m "docs: add knowledge graph screenshot and demo GIF"
```

---

## Day 3-4: Launch Content

### Task 7: Write Twitter thread draft

**Files:**
- Create: `docs/launch/twitter-thread.md`

- [ ] **Step 1: Create launch content directory**

```bash
mkdir -p /Users/sum_young/selfOS/docs/launch
```

- [ ] **Step 2: Write Twitter thread**

Create `docs/launch/twitter-thread.md` with the 6-tweet thread from spec:

```markdown
# Twitter/X Thread — selfOS Launch

## Tweet 1 (Hook)
I've been building a Personal AI OS for 11 months.

It compiles my notes, AI conversations, and bookmarks into a knowledge base that understands me better than I do.

Open source today.

[attach: graph-screenshot.png]

## Tweet 2 (Problem)
We have great tools to understand codebases now (shoutout @safishamsi's Graphify).

But who's building tools to understand yourself?

800+ AI conversations. 200+ notes. Scattered bookmarks. They're just... sitting there.

## Tweet 3 (Solution)
selfOS compiles them ONCE into a structured wiki.

source → concept → entity — three layers of knowledge.

No RAG. No re-reading raw files. Zero token cost per query.

[attach: demo.gif]

## Tweet 4 (Killer Feature)
The wildest part: the AI interviews YOU.

It finds gaps in your knowledge base and asks questions to recover context you've already forgotten.

I call it "Reverse DPO" — instead of you training the AI, the AI trains your memory.

[attach: interview-screenshot.png]

## Tweet 5 (Stats)
11 months of real daily usage:
• 800+ sources compiled
• 45 concepts extracted
• 27 entities tracked
• 3 data sources (Notion, Claude.ai, Gemini)
• 1 queryable graph of my intellectual life

[attach: full-graph-screenshot.png]

## Tweet 6 (CTA)
Built as a Claude Code skill. MIT license.

Clone the `demo` branch to explore a real knowledge base.

github.com/[USERNAME]/selfOS

"Graphify for code, selfOS for life."
```

- [ ] **Step 3: Commit**

```bash
git add docs/launch/
git commit -m "docs: draft Twitter thread for launch"
```

---

### Task 8: Write Chinese launch content

**Files:**
- Create: `docs/launch/xiaohongshu.md`
- Create: `docs/launch/jike.md`

- [ ] **Step 1: Write 小红书 post**

Create `docs/launch/xiaohongshu.md`:

```markdown
# 小红书帖子 — selfOS 发布

## 标题
我用 Claude Code 搭了一个个人 AI 操作系统，跑了 11 个月

## 正文
最近 Graphify 很火——把代码变成知识图谱，4天 4000+ star。

但我想做的不一样：不是理解代码，是理解自己。

---

我有 800 多条和 AI 的对话记录，200 多条 Notion 笔记，还有一堆推特书签。它们散落在各处，从来没有被系统整理过。

selfOS 做的事情很简单：把这些碎片一次性「编译」成一个结构化的 wiki。

不是 RAG（每次查询重新读一遍原文），而是真正的编译——源文件 → 概念 → 实体 → 知识图谱。编译完之后查询零成本。

---

最疯狂的功能：AI 会反过来「采访」你。

它会扫描你的知识库，找到缺失的 context，然后主动问你问题来补全。

比如你一年前写了一句"今天想明白了一件事"——它会问你：当时发生了什么？现在回看怎么理解？

我管这个叫「逆向 DPO」——不是你训练 AI，是 AI 训练你的记忆。

---

跑了 11 个月的真实数据：
• 800+ 条源材料
• 45 个概念节点
• 27 个实体节点
• 还有一个交互式知识图谱可视化

开源 MIT，GitHub 链接在评论区。

[配图：知识图谱截图、query 演示截图、interview 截图]
```

- [ ] **Step 2: Write 即刻 post**

Create `docs/launch/jike.md` — shorter version of the 小红书 post, more conversational tone, ~300 characters max body with link.

```markdown
# 即刻帖子 — selfOS 发布

做了一个个人 AI 操作系统 selfOS，跑了 11 个月。

把 Notion 笔记、AI 对话、推特书签「编译」成结构化知识图谱。不是 RAG，是真编译——查询零 token 成本。

最酷的功能：AI 会反过来采访你，找到你知识库里的 gap 然后问你问题来补全。逆向 DPO。

开源 MIT：github.com/[USERNAME]/selfOS

（配图：知识图谱截图）
```

- [ ] **Step 3: Commit**

```bash
git add docs/launch/
git commit -m "docs: draft Chinese launch content (小红书 + 即刻)"
```

---

### Task 9: Write HN / Reddit posts

**Files:**
- Create: `docs/launch/hackernews.md`
- Create: `docs/launch/reddit.md`

- [ ] **Step 1: Write HN post**

Create `docs/launch/hackernews.md`:

```markdown
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

MIT licensed: github.com/[USERNAME]/selfOS
```

- [ ] **Step 2: Write Reddit posts**

Create `docs/launch/reddit.md`:

```markdown
# Reddit Posts

## r/ClaudeAI

**Title:** I built a "Personal AI OS" as a Claude Code skill — it compiles your notes and conversations into a queryable knowledge graph

**Body:** [Same as HN but shorter, emphasize Claude Code integration and skill system]

## r/LocalLLaMA

**Title:** selfOS: Compile your scattered AI conversations into a persistent knowledge graph (open source)

**Body:** [Emphasize the "compilation not RAG" angle, works with any LLM conversations]
```

- [ ] **Step 3: Commit**

```bash
git add docs/launch/
git commit -m "docs: draft HN and Reddit launch posts"
```

---

### Task 10: Final pre-launch checklist

- [ ] **Step 1: Verify main branch is clean**

```bash
cd /Users/sum_young/selfOS
git checkout main
git status
```

Ensure no personal data is tracked. Check that wiki/ only has templates and .gitkeep files.

- [ ] **Step 2: Verify demo branch works end-to-end**

```bash
git checkout demo
python viewer/build_graph.py wiki viewer/static/graph.json
python viewer/app.py
# Open localhost:5001 — verify graph loads, search works, click detail works
```

- [ ] **Step 3: Verify quick start flow works from scratch**

```bash
cd /tmp
git clone /Users/sum_young/selfOS selfos-test
cd selfos-test
git checkout demo
python viewer/app.py
# Verify it works for a fresh clone
```

- [ ] **Step 4: Create GitHub repo (if not exists) and push both branches**

```bash
cd /Users/sum_young/selfOS
# Create repo on GitHub first via gh CLI or web UI
gh repo create selfOS --public --description "Your personal AI operating system" --source=. --push
git push origin demo
```

- [ ] **Step 5: Replace all `[USERNAME]` placeholders in launch content**

Grep and replace across all `docs/launch/*.md` files with actual GitHub username.

- [ ] **Step 6: Final commit**

```bash
git add -A
git commit -m "chore: pre-launch cleanup and placeholder replacement"
git push
```
