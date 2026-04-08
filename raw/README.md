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
