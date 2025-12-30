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
from tools_for_agents import GoogleSearchTool

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
    Agent that researches companies using Google Search.

    The agent performs multiple searches to gather:
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

        # Get tool schema - OpenRouter uses OpenAI-compatible format
        self.tools = [self.search_tool.to_openai_schema()]

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
        system_prompt = """You are a company research analyst. Your job is to research companies thoroughly using web search.

For each company, you should:
1. Search for general information about the company (what they do, when founded, etc.)
2. Search for recent news and developments
3. Search for their main products or services
4. Search for funding, revenue, or financial information

After gathering information, compile a well-structured research report with clear sections.

Use the google_search tool multiple times to gather comprehensive information."""

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
                args = json.loads(tool_call.function.arguments)
                print(f"🔍 Searching: {args.get('query', '')}")

                # Execute the search
                try:
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

                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(formatted_results)
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
