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

    node_type = meta.get("type", "unknown")
    if node_type == "entity":
        tag_set = set(t.lower() for t in tags)
        if tag_set & {"person", "people", "researcher"}:
            node_type = "entity-person"
        elif tag_set & {"org", "organization", "company", "lab"}:
            node_type = "entity-org"
        elif tag_set & {"tool", "project", "software"}:
            node_type = "entity-tool"
        else:
            node_type = "entity-person"

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

    for subdir in ["concepts", "entities", "synthesis"]:
        dirpath = wiki_root / subdir
        if not dirpath.is_dir():
            continue
        for md_file in sorted(dirpath.glob("*.md")):
            node = parse_page(md_file, wiki_root)
            nodes.append(node)
            node_ids.add(node["id"])

    for node in nodes:
        for target in node["wikilinks"]:
            if target in node_ids and target != node["id"]:
                edges.append({
                    "from": node["id"],
                    "to": target,
                    "type": "wikilink",
                })

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
