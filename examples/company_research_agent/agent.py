"""
Company Research Agent - OpenRouter Implementation

This agent researches companies by performing multiple Google searches
and compiling findings into a comprehensive report.

Uses OpenRouter to support any model that supports tool calling.
Switch models by changing the MODEL constant.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from tools_for_agents import GoogleSearchTool, WebFetchTool

# Load environment variables from .env file in this directory
# .env should be in the same directory as this script
load_dotenv(Path(__file__).parent / ".env")


# Available models on OpenRouter (examples):
# - "anthropic/claude-3.5-sonnet"
# - "google/gemini-2.0-flash-001"
# - "openai/gpt-4-turbo"
# - "meta-llama/llama-3.1-70b-instruct"
# Find more at: https://openrouter.ai/models?supported_parameters=tools

DEFAULT_MODEL = "anthropic/claude-3.5-sonnet"


class CompanyResearchAgent:
    """
    Agent that researches companies using Google Search and web page fetching.

    The agent searches for relevant pages, fetches their full content, and analyzes:
    - General company information
    - Recent news and developments
    - Products and services
    - Funding and financial information

    Then compiles everything into a structured research report.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        openrouter_api_key: str | None = None,
        serpapi_key: str | None = None
    ):
        """
        Initialize the research agent.

        Args:
            model: OpenRouter model to use (e.g., "anthropic/claude-3.5-sonnet")
            openrouter_api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
            serpapi_key: SerpAPI key (defaults to SERPAPI_API_KEY env var)
        """
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_api_key or os.getenv("OPENROUTER_API_KEY"),
        )
        self.search_tool = GoogleSearchTool(api_key=serpapi_key or os.getenv("SERPAPI_API_KEY"))
        self.fetch_tool = WebFetchTool()

        # Get tool schemas - OpenRouter uses OpenAI-compatible format
        self.tools = [
            self.search_tool.to_openai_schema(),
            self.fetch_tool.to_openai_schema()
        ]

    def research_company(self, company_name: str) -> str:
        """
        Research a company and generate a comprehensive report.

        Args:
            company_name: Name of the company to research

        Returns:
            A formatted research report
        """
        print(f"\n{'='*60}")
        print(f"🔍 Researching: {company_name}")
        print(f"{'='*60}\n")

        # System message for the agent
        system_prompt = """You are a company research analyst. Your job is to research companies thoroughly using web search and content fetching.

Your research workflow:
1. Use google_search to find relevant pages about the company
2. Use web_fetch to read the full content of the most relevant URLs (usually 2-3 key pages)
3. Analyze the full content to extract detailed, accurate information

For each company, gather:
- General information (what they do, when founded, leadership)
- Recent news and developments
- Main products or services
- Funding, revenue, or financial information

After gathering information from actual web pages, compile a well-structured research report with clear sections and specific details."""

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Research {company_name} and create a comprehensive company report."
            }
        ]

        # Agent loop - continue until no more tool calls
        turn_count = 0
        max_turns = 10  # Safety limit

        while turn_count < max_turns:
            turn_count += 1

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
            )

            message = response.choices[0].message
            messages.append(message.model_dump())

            # Check if any tools were called
            if not message.tool_calls:
                # No more tool calls - agent is done
                print("\n✓ Research complete\n")
                return message.content

            # Execute each tool call
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                try:
                    if tool_name == "google_search":
                        print(f"🔍 Searching: {args.get('query', '')}")
                        result = self.search_tool.validate_and_execute(**args)
                        print(f"   → Found {len(result.results)} results\n")

                        # Format results for the model
                        formatted_results = {
                            "total_results": result.total_results,
                            "results": [
                                {
                                    "position": r.position,
                                    "title": r.title,
                                    "url": r.url,
                                    "snippet": r.snippet
                                }
                                for r in result.results
                            ]
                        }

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(formatted_results)
                        })

                    elif tool_name == "web_fetch":
                        url = args.get('url', '')
                        # Truncate long URLs for display
                        display_url = url if len(url) < 50 else url[:47] + "..."
                        print(f"📄 Fetching: {display_url}")

                        result = self.fetch_tool.validate_and_execute(**args)
                        content_preview = result.content[:100] + "..." if len(result.content) > 100 else result.content
                        print(f"   → Got {len(result.content)} chars ({result.mode} mode)\n")

                        # Format result for the model
                        formatted_result = {
                            "url": result.url,
                            "title": result.title,
                            "content": result.content,
                            "mode": result.mode
                        }

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(formatted_result)
                        })

                    else:
                        print(f"   ✗ Unknown tool: {tool_name}")
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"error": f"Unknown tool: {tool_name}"})
                        })

                except Exception as e:
                    print(f"   ✗ Error: {e}")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps({"error": str(e)})
                    })

        # Hit max turns
        print(f"\n⚠ Reached maximum turns ({max_turns})")
        return "Research incomplete - reached maximum turns"


def main():
    """Run the company research agent."""
    # Customize these variables
    company_to_research = "VIA Science"
    model = DEFAULT_MODEL  # Change to any model from https://openrouter.ai/models

    agent = CompanyResearchAgent(model=model)
    report = agent.research_company(company_to_research)

    print("="*60)
    print("📊 REPORT")
    print("="*60 + "\n")
    print(report)
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
