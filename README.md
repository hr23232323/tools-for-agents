# Tools for Agents

Open-source runtime tools for LLM agents. We built this to be framework-agnostic and production-ready.

## Quick Start

```bash
git clone https://github.com/yourusername/tools-for-agents.git
cd tools-for-agents/examples/company_research_agent
cp .env.example .env
# Edit .env with your API keys
uv run agent.py
```

## Why We Built This

We kept rewriting the same API wrappers, schemas, and error handling for every agent project. This library provides reusable tools so you don't have to.

## What We Believe

- **Simple & pragmatic** - We avoid over-abstraction
- **Framework agnostic** - Works with OpenAI, Anthropic, or any LLM
- **Production ready** - Error handling and validation included
- **MIT licensed** - Use it however you'd like

## Installation

```bash
pip install tools-for-agents
```

## Usage

### With OpenRouter

```python
import json
from openai import OpenAI
from tools_for_agents import GoogleSearchTool

search = GoogleSearchTool(api_key="your-serpapi-key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-openrouter-key",
    default_headers={
        "HTTP-Referer": "https://github.com/youruser/yourproject",
        "X-Title": "Your Project Name"
    }
)

response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Search for Python tutorials"}],
    tools=[search.to_openai_schema()]
)

message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        result = search.validate_and_execute(**json.loads(tool_call.function.arguments))
```

<details>
<summary>Platform-specific examples</summary>

**OpenAI:**
```python
from openai import OpenAI
from tools_for_agents import GoogleSearchTool

search = GoogleSearchTool(api_key="your-serpapi-key")
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    tools=[search.to_openai_schema()],
    input=[{"role": "user", "content": "Search for Python tutorials"}]
)

for item in response.output:
    if item.type == "function_call":
        result = search.validate_and_execute(**json.loads(item.arguments))
```

**Anthropic:**
```python
from anthropic import Anthropic
from tools_for_agents import GoogleSearchTool

search = GoogleSearchTool(api_key="your-serpapi-key")
client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    tools=[search.to_anthropic_schema()],
    messages=[{"role": "user", "content": "Search for Python tutorials"}]
)

for block in response.content:
    if block.type == "tool_use":
        result = search.validate_and_execute(**block.input)
```

</details>

## Available Tools

### Google Search
Let's search Google and get structured results back:

```python
from tools_for_agents import GoogleSearchTool

search = GoogleSearchTool(api_key="serpapi-key")
result = search.validate_and_execute(
    query="Python asyncio tutorial",
    num_results=5
)

for r in result.results:
    print(f"{r.position}. {r.title} - {r.url}")
```

**Note:** You'll need a SerpAPI key from https://serpapi.com/

## Creating Custom Tools

You can extend `BaseTool` to create your own tools:

```python
from pydantic import BaseModel, Field
from tools_for_agents import BaseTool

class MyToolInput(BaseModel):
    param: str = Field(description="Parameter description")

class MyToolOutput(BaseModel):
    result: str

class MyTool(BaseTool[MyToolInput, MyToolOutput]):
    name = "my_tool"
    description = "What this tool does and when to use it"
    input_model = MyToolInput
    output_model = MyToolOutput

    def __init__(self, api_key: str):
        self.api_key = api_key

    def execute(self, input: MyToolInput) -> MyToolOutput:
        # Your tool logic here
        return MyToolOutput(result="...")
```

**What you get automatically:**
- Input/output validation via Pydantic
- Schema generation for OpenAI and Anthropic
- Type safety

## Example Agents

We've built production-ready examples in `/examples` to help you get started:

### Company Research Agent
This autonomous agent researches companies using web search. It demonstrates:

- Multi-turn agent loops
- Autonomous planning and reasoning
- OpenRouter for model flexibility

[View documentation](./examples/company_research_agent/)

## Running Examples

```bash
cd examples/company_research_agent
cp .env.example .env
# Add your API keys to .env
uv run agent.py
```

Each example is self-contained with its own `.env` configuration.

## Architecture

```
tools-for-agents/
├── src/tools_for_agents/
│   ├── base.py              # BaseTool abstract class
│   ├── exceptions.py        # Standard exceptions
│   └── tools/
│       └── google_search.py # Tool implementations
└── examples/
    └── company_research_agent/
        ├── agent.py
        ├── .env.example
        └── README.md
```

## Project Status

We're in the early stages. Right now we ship with Google Search, and we're looking for:
- Contributors to add new tools
- Feedback on the API design
- Bug reports and feature requests

## Contributing

We'd love your help! Please open an issue to discuss before starting work on a new tool.

**What we look for in contributions:**
- Clear documentation
- Error handling
- Pydantic for validation
- Usage examples

## License

MIT - use it however you'd like.
