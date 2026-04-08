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
        wikilink_edges = [e for e in graph["edges"] if e["type"] == "wikilink"]
        assert len(wikilink_edges) == 2
        tag_edges = [e for e in graph["edges"] if e["type"] == "shared_tag"]
        assert len(tag_edges) >= 1
