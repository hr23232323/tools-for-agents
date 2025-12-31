# Company Research Agent

An autonomous agent that researches companies by searching the web and reading full page content.

## What It Does

Give it a company name, and it will:
1. Search for relevant pages using Google
2. Fetch and read the full content of key pages
3. Extract detailed information about the company
4. Compile everything into a comprehensive report

**Why this works:** The agent doesn't just rely on search snippets - it reads actual web pages to get complete, accurate information.

## Quick Start

**Navigate here:**
```bash
cd examples/company_research_agent
```

**Set up your API keys:**
```bash
cp .env.example .env
# Edit .env:
#   SERPAPI_API_KEY=your_key
#   OPENROUTER_API_KEY=your_key
```

**Get keys from:**
- SerpAPI: https://serpapi.com/
- OpenRouter: https://openrouter.ai/keys

**Run it:**
```bash
uv run agent.py
```

## How It Works

### The Agent Loop

```
1. Send prompt to LLM with available tools
2. LLM decides if it needs tools
   - Yes: Execute tools, send results → repeat from step 2
   - No: Return final response
```

The agent autonomously decides how many searches to perform and what to search for.

### Key Components

**CompanyResearchAgent Class**
- Manages the agent loop
- Handles tool execution
- Formats results for the LLM
- Includes safety limits (max turns to prevent infinite loops)

**System Prompt**
- Defines the agent's role and goals
- Instructs what information to gather
- Guides the report structure

**Tool Integration**
- Uses `GoogleSearchTool` and `WebFetchTool` from `tools-for-agents`
- Searches for pages, then fetches their content
- Generates OpenAI-compatible schemas automatically
- Handles errors gracefully

## Switching Models

You can easily switch between different LLMs. Edit `DEFAULT_MODEL` in `agent.py`:

```python
DEFAULT_MODEL = "anthropic/claude-3.5-sonnet"
# DEFAULT_MODEL = "google/gemini-2.0-flash-001"
# DEFAULT_MODEL = "openai/gpt-4-turbo"
# DEFAULT_MODEL = "meta-llama/llama-3.1-70b-instruct"
```

Or pass it dynamically:
```python
agent = CompanyResearchAgent(model="google/gemini-2.0-flash-001")
```

## Customization

**Change the research target** in `main()`:
```python
def main():
    company_to_research = "YourCompany"
    agent = CompanyResearchAgent(model="anthropic/claude-3.5-sonnet")
    report = agent.research_company(company_to_research)
    print(report)
```

**Modify the system prompt** to customize:
- Report format and structure
- Information priorities
- Search strategies
- Writing style

## Example Output

```
============================================================
🔍 Starting research on: Anthropic
🤖 Using model: anthropic/claude-3.5-sonnet
============================================================

--- Turn 1 ---
🔧 Tool call: google_search
   Query: 'Anthropic AI company overview founding'
   ✓ Found 5 results

--- Turn 2 ---
🔧 Tool call: google_search
   Query: 'Anthropic recent news 2025'
   ✓ Found 5 results

--- Turn 3 ---
🔧 Tool call: google_search
   Query: 'Anthropic Claude AI products'
   ✓ Found 5 results

--- Turn 4 ---
🔧 Tool call: google_search
   Query: 'Anthropic funding investors'
   ✓ Found 5 results

✓ Agent completed research

============================================================
📊 FINAL RESEARCH REPORT
============================================================

# Anthropic Company Research Report

## Overview
Anthropic is an AI safety company founded in 2021...

## Recent Developments
- Launched Claude 3 family in March 2024...

## Products and Services
- Claude: Family of large language models...

## Funding
- Series C: $450M at $4.1B valuation (2023)...

============================================================
```

## Design Insights

**Search + Fetch = Better reports** - Reading full page content instead of just search snippets gives the agent complete, accurate information to work with.

**Multiple focused searches work better** - Specific queries return better results than broad searches.

**Safety mechanisms matter** - The max turns limit prevents infinite loops, and error handling ensures the agent continues even when tool calls fail.

**Using `tools-for-agents` eliminates boilerplate** - You don't need to write:
- SerpAPI integration code
- Web fetching and HTML parsing logic
- Error handling for network requests
- Schema definitions
- Input/output validation

## Extending the Agent

**Add more tools:**
```python
from tools_for_agents import GoogleSearchTool, WebFetchTool

search = GoogleSearchTool(api_key="...")
fetch = WebFetchTool()

tools = [
    search.to_openai_schema(),
    fetch.to_openai_schema()
]
```

The agent automatically learns to use them - no additional code needed.

**Save reports to disk:**
```python
import json

report = agent.research_company("Anthropic")

with open("research_reports/anthropic.json", "w") as f:
    json.dump({"company": "Anthropic", "report": report}, f)
```

## Comparing Models

Want to see how different models perform? Try this:

```python
models = [
    "anthropic/claude-3.5-sonnet",
    "google/gemini-2.0-flash-001",
    "openai/gpt-4-turbo",
]

for model in models:
    agent = CompanyResearchAgent(model=model)
    report = agent.research_company("Anthropic")
    # Compare quality, cost, and speed
```
