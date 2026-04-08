"""selfOS Knowledge Graph Viewer — Flask server."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder="static", static_url_path="")
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
