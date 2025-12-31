# Web Fetch Tool

Fetch web page content as cleaned readable text or raw HTML.

## Usage

```python
from tools_for_agents import WebFetchTool

fetch = WebFetchTool()

# Get clean, readable text (default)
result = fetch.validate_and_execute(
    url="https://example.com",
    mode="text"
)
print(result.title)
print(result.content)

# Or get raw HTML
result = fetch.validate_and_execute(
    url="https://example.com",
    mode="html"
)
```

## Parameters

**Input:**
- `url` (str, required): The URL to fetch
- `mode` (str, optional): Output mode - "text" or "html" (default: "text")
- `timeout` (int, optional): Request timeout in seconds (5-120, default: 30)

**Output:**
- `url` (str): Final URL after redirects
- `content` (str): Page content (cleaned text or raw HTML)
- `mode` (str): Mode used ("text" or "html")
- `title` (str | None): Page title if available

## Modes

**text mode:**
- Strips scripts, styles, navigation, footers
- Returns clean, readable text content
- Removes excessive whitespace
- Perfect for LLM analysis

**html mode:**
- Returns complete HTML markup
- No processing or filtering
- Use when you need full page structure

## Perfect Pairing

Combine with GoogleSearchTool for powerful research workflows:

```python
# Search → Fetch → Analyze
search = GoogleSearchTool(api_key="...")
fetch = WebFetchTool()

# Find pages
results = search.validate_and_execute(query="Python tutorials")

# Read the top result
page = fetch.validate_and_execute(url=results.results[0].url)
print(page.content)
```

## Error Handling

Raises:
- `ToolExecutionError`: If fetch fails or content is invalid
- Handles HTTP errors, timeouts, and parsing errors gracefully
