# Example Agents

We've built production-ready example agents to help you see `tools-for-agents` in action. Each demonstrates real-world use cases using OpenRouter for model flexibility.

## Why We Use OpenRouter

All our examples use OpenRouter because it gives you:
- **Model flexibility** - Switch between Claude, GPT, Gemini, Llama
- **No vendor lock-in** - Change providers without rewriting code
- **One API key** - Access all providers with a single key
- **Cost optimization** - Pick the best price/performance for your needs

## Structure

Each agent is self-contained with everything you need:

```
agent_name/
├── agent.py          # Agent implementation
├── .env.example      # API key template
├── .env              # Your keys (gitignored)
└── README.md         # Documentation
```

## Quick Start

**1. Navigate to an example:**
```bash
cd company_research_agent
```

**2. Set up your API keys:**
```bash
cp .env.example .env
# Edit .env with your keys
```

**3. Run it:**
```bash
uv run agent.py
```

**Get API keys:**
- SerpAPI: https://serpapi.com/
- OpenRouter: https://openrouter.ai/keys

## Available Agents

### Company Research Agent

This agent researches companies using web search and compiles comprehensive reports.

**What it demonstrates:**
- Multi-turn agent loops
- Multiple tool calls per task
- Information synthesis
- Model switching

**Tools used:** GoogleSearchTool

**Models we've tested:** Claude 3.5 Sonnet, Gemini 2.0 Flash, GPT-4 Turbo, Llama 3.1 70B

[View documentation](./company_research_agent/README.md)

## Learning Path

Here's how we recommend exploring:

1. Read the [Company Research Agent README](./company_research_agent/README.md)
2. Run the agent and see it in action
3. Try different models (just change one line)
4. Read through the code (~150 lines)
5. Customize it for your needs

## Model Comparison

Want to compare how different models perform? Try this:

```python
models = [
    "anthropic/claude-3.5-sonnet",
    "google/gemini-2.0-flash-001",
    "openai/gpt-4-turbo",
]

for model in models:
    agent = CompanyResearchAgent(model=model)
    report = agent.research_company("Anthropic")
```

**Find more models:** https://openrouter.ai/models?supported_parameters=tools

## Contributing

We'd love to see your example agents! We look for agents that:
- Solve a real problem
- Demonstrate interesting tool usage
- Include clear documentation
- Use OpenRouter for model flexibility

Please open an issue to discuss your idea before submitting.
