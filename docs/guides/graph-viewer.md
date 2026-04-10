# Web Graph Viewer

Interactive visualization of your selfOS knowledge graph in the browser.

## Prerequisites

- Python 3.8+
- Flask: `pip install flask pyyaml`

## Start the Viewer

```bash
python viewer/app.py
```

Open [http://localhost:5001](http://localhost:5001) in your browser.

On first launch, the server automatically builds `viewer/static/graph.json` from your wiki pages.

## Rebuild the Graph

After adding or editing wiki pages, rebuild the graph to reflect changes:

```bash
# Option 1: POST to the API (while server is running)
curl -X POST http://localhost:5001/api/rebuild

# Option 2: Run the build script directly
python viewer/build_graph.py wiki viewer/static/graph.json
```

The rebuild scans `wiki/concepts/`, `wiki/entities/`, and `wiki/synthesis/` for markdown files with YAML frontmatter.

## What You See

- **Nodes** = wiki pages (concepts, entities, synthesis pages)
- **Edges** = `[[wikilinks]]` between pages (solid) and shared tags (faint)
- **Node size** scales with the number of sources citing that page
- **Colors** depend on the active color preset (see below)

Source pages (`wiki/sources/`) are not shown as nodes -- they are the raw material that feeds into concepts and entities.

## Color Presets

Click the preset switcher in the top-right header to change how nodes are colored:

| Preset | Colors by |
|--------|-----------|
| Type | Page type: concept (blue), person (amber), org (green), tool (purple) |
| Tag Cluster | Primary tag -- top 8 tags get distinct colors |
| Timeline | Created date -- older = dark, newer = bright |
| Connections | Edge count -- few = red, many = yellow |
| Source Density | Number of citing sources -- few = dark green, many = bright green |

## Interaction

- **Click** a node to open the detail panel (summary, tags, connections, dates)
- **Click** a linked node in the detail panel to navigate to it
- **Scroll** to zoom in/out
- **Drag** empty space to pan
- **Drag** a node to reposition it
- **Search** by typing in the search box -- the camera animates to the first match
- **Filter** by type using the buttons in the header (Concepts, People, Orgs, Tools)

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the viewer UI |
| `/api/graph` | GET | Returns `graph.json` (auto-builds if missing) |
| `/api/rebuild` | POST | Force rebuilds the graph, returns node/edge counts |
