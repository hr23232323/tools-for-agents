# Tools Catalog

Complete reference for all available tools in `tools-for-agents`.

**Total Tools:** 2

---

## Google Search

Search Google and return structured results with titles, URLs, and snippets.

```python
from tools_for_agents import GoogleSearchTool
```

| | |
|---|---|
| **Class** | `GoogleSearchTool` |
| **Path** | `google_search/` |
| **Requirements** | SerpAPI key ([get one →](https://serpapi.com/)) |
| **Use Cases** | Finding web pages, researching topics, gathering current information |
| **Docs** | [google_search/README.md](./google_search/README.md) |

---

## Web Fetch

Fetch web page content as cleaned readable text or raw HTML.

```python
from tools_for_agents import WebFetchTool
```

| | |
|---|---|
| **Class** | `WebFetchTool` |
| **Path** | `web_fetch/` |
| **Requirements** | None (free) |
| **Use Cases** | Reading full page content, extracting article text, following search results |
| **Docs** | [web_fetch/README.md](./web_fetch/README.md) |

---

## Adding a New Tool

Follow the format above. Each tool gets:
- H2 header with tool name
- One-line description
- Import code block
- Metadata table (Class, Path, Requirements, Use Cases, Docs)

**Required updates when adding a tool:**
- [ ] Add entry to this catalog (CATALOG.md)
- [ ] Add row to main README.md table
- [ ] Update tool count at top of this file
- [ ] See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for full checklist
