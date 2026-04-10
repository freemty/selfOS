# Importing Conversations

How to import your Claude, Gemini, and Notion data into selfOS.

## Claude.ai Conversations

1. Go to [claude.ai](https://claude.ai) -> Settings -> Account -> **Export Data**
2. You will receive an email with a download link. Download and extract the zip.
3. Find `conversations.json` in the extracted folder.
4. Copy it into your raw data directory:
   ```bash
   mkdir -p raw/claude-conversations
   cp /path/to/conversations.json raw/claude-conversations/
   ```
5. Run the extraction script:
   ```bash
   python scripts/extract-all-sources.py
   ```
6. Result: `wiki/sources/cc-YYYY-MM-DD-*.md` pages -- one per conversation, with speaker labels `[me]` / `[Claude]`.

**Note:** The export zip also contains `users.json` with personal info (email, phone). Do not commit this file -- it is already in `.gitignore`.

## Gemini Conversations

1. Go to [takeout.google.com](https://takeout.google.com)
2. Deselect all, then select **Gemini Apps** -> download the archive.
3. Extract the `.md` files into the raw data directory:
   ```bash
   mkdir -p raw/gemini-conversations
   cp /path/to/Takeout/Gemini\ Apps/Conversations/*.md raw/gemini-conversations/
   ```
4. Run the extraction script:
   ```bash
   python scripts/extract-all-sources.py
   ```
5. Result: `wiki/sources/gem-YYYY-MM-DD-*.md` pages -- one per conversation.

## Notion Notes

**Option A: Direct API access (recommended)**

If you have the Notion MCP server configured, selfOS can read your Notion workspace directly:

```bash
# In Claude Code
/wiki sync
```

This performs an incremental sync from Notion to wiki without manual export.

**Option B: Manual export**

1. In Notion, select the pages you want to export -> Export -> **Markdown & CSV**
2. Extract the `.md` files into the raw data directory:
   ```bash
   mkdir -p raw/notion-notes
   cp /path/to/exported/*.md raw/notion-notes/
   ```
3. Run the extraction script:
   ```bash
   python scripts/extract-all-sources.py
   ```
4. Result: `wiki/sources/notion-YYYY-MM-DD-*.md` pages.

## What the Script Does

`scripts/extract-all-sources.py` scans three directories under `raw/`:

| Directory | Format | Output prefix |
|-----------|--------|---------------|
| `raw/claude-conversations/` | `conversations.json` | `cc-` |
| `raw/gemini-conversations/` | Individual `.md` files | `gem-` |
| `raw/notion-notes/` | Individual `.md` files | `notion-` |

For each conversation or note, it creates a source page in `wiki/sources/` with:
- YAML frontmatter (title, date, tags, message counts)
- Full conversation text with speaker labels
- Claude's auto-generated summary (if available)

After extraction, run `/wiki compile` in Claude Code to generate concept and entity pages from the new sources. You can also use `/wiki compile` as an alternative to running the Python script directly -- it does the same extraction plus concept/entity page generation.
