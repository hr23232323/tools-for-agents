# Google Search Tool

Search Google and return structured results with titles, URLs, and snippets.

## Usage

```python
from tools_for_agents import GoogleSearchTool

search = GoogleSearchTool(api_key="your-serpapi-key")
result = search.validate_and_execute(
    query="Python asyncio tutorial",
    num_results=5
)

for r in result.results:
    print(f"{r.position}. {r.title}")
    print(f"   {r.url}")
    print(f"   {r.snippet}\n")
```

## Parameters

**Input:**
- `query` (str, required): The search query to execute
- `num_results` (int, optional): Number of results to return (1-10, default: 5)

**Output:**
- `results` (list): List of search results with title, url, snippet, and position
- `total_results` (int): Approximate total number of results found

## Requirements

Requires a SerpAPI key. Get one at: https://serpapi.com/

Set via environment variable:
```bash
export SERPAPI_API_KEY=your_key_here
```

Or pass directly:
```python
tool = GoogleSearchTool(api_key="your_key_here")
```

## Error Handling

Raises:
- `AuthenticationError`: Invalid API key
- `RateLimitError`: API rate limit exceeded
- `ToolExecutionError`: Search fails for other reasons
