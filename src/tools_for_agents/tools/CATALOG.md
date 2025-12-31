# Tools Catalog

Complete list of all available tools in `tools-for-agents`.

## Available Tools

### Google Search
**Path:** `google_search/`
**Class:** `GoogleSearchTool`
**Description:** Search Google and return structured results with titles, URLs, and snippets.
**Requirements:** SerpAPI key (https://serpapi.com/)
**Use Case:** Finding relevant web pages, researching topics, gathering current information
**Documentation:** [google_search/README.md](./google_search/README.md)

---

### Web Fetch
**Path:** `web_fetch/`
**Class:** `WebFetchTool`
**Description:** Fetch web page content as cleaned readable text or raw HTML.
**Requirements:** None (free)
**Use Case:** Reading full page content after finding URLs with search, extracting article text
**Documentation:** [web_fetch/README.md](./web_fetch/README.md)

---

## Adding a New Tool

When adding a new tool, update this catalog with:

1. **Name** - Display name of the tool
2. **Path** - Directory name in `tools/`
3. **Class** - Python class name (e.g., `MyNewTool`)
4. **Description** - One sentence describing what it does
5. **Requirements** - API keys, dependencies, or "None (free)"
6. **Use Case** - When/why to use this tool
7. **Documentation** - Link to tool's README

Also remember to:
- [ ] Create `tools/{tool_name}/` directory
- [ ] Add `{tool_name}_tool.py` with implementation
- [ ] Add `README.md` in tool directory
- [ ] Add `__init__.py` in tool directory
- [ ] Update `tools/__init__.py` to export the tool
- [ ] Update main `README.md` table
- [ ] Update this CATALOG.md

## Tool Count

**Total Tools:** 2
