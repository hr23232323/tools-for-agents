"""Google Search tool using SerpAPI."""

import os
from typing import List
import requests
from pydantic import BaseModel, Field

from ..base import BaseTool
from ..exceptions import AuthenticationError, RateLimitError, ToolExecutionError


class GoogleSearchInput(BaseModel):
    """Input parameters for Google Search."""

    query: str = Field(description="The search query to execute")
    num_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of results to return (1-10)"
    )


class SearchResult(BaseModel):
    """A single search result."""

    title: str = Field(description="Title of the search result")
    url: str = Field(description="URL of the search result")
    snippet: str = Field(description="Brief description/snippet from the result")
    position: int = Field(description="Position in search results (1-indexed)")


class GoogleSearchOutput(BaseModel):
    """Output from Google Search."""

    results: List[SearchResult] = Field(description="List of search results")
    total_results: int = Field(description="Approximate total number of results found")


class GoogleSearchTool(BaseTool[GoogleSearchInput, GoogleSearchOutput]):
    """
    Search Google and return top results.

    Uses SerpAPI to perform Google searches and returns structured results
    including title, URL, snippet, and position for each result.

    Authentication:
        Requires SERPAPI_API_KEY environment variable or api_key parameter.
        Get your API key at: https://serpapi.com/

    Example:
        >>> tool = GoogleSearchTool(api_key="your-key")
        >>> result = tool.validate_and_execute(
        ...     query="Python asyncio tutorial",
        ...     num_results=3
        ... )
        >>> for r in result.results:
        ...     print(f"{r.position}. {r.title}")
    """

    name = "google_search"
    description = (
        "Search Google for information. Returns the top search results with "
        "titles, URLs, and snippets. Use this when you need to find current "
        "information, research topics, or look up facts online."
    )
    input_model = GoogleSearchInput
    output_model = GoogleSearchOutput

    def __init__(self, api_key: str | None = None):
        """
        Initialize the Google Search tool.

        Args:
            api_key: SerpAPI API key. If not provided, will use SERPAPI_API_KEY env var.

        Raises:
            ValueError: If no API key is provided
        """
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "SERPAPI_API_KEY is required. Get one at https://serpapi.com/"
            )

    def execute(self, input: GoogleSearchInput) -> GoogleSearchOutput:
        """
        Execute Google search via SerpAPI.

        Args:
            input: Validated search parameters

        Returns:
            Structured search results

        Raises:
            AuthenticationError: If API key is invalid
            RateLimitError: If API rate limit is exceeded
            ToolExecutionError: If search fails for other reasons
        """
        try:
            params = {
                "q": input.query,
                "num": input.num_results,
                "api_key": self.api_key,
                "engine": "google"
            }

            response = requests.get(
                "https://serpapi.com/search",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            # Check for API errors
            if "error" in data:
                error_msg = data["error"]
                if "Invalid API key" in error_msg:
                    raise AuthenticationError(f"Invalid SerpAPI key: {error_msg}")
                else:
                    raise ToolExecutionError(f"SerpAPI error: {error_msg}")

            # Transform to standard format
            results = []
            organic_results = data.get("organic_results", [])

            for idx, item in enumerate(organic_results[:input.num_results]):
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("link", ""),
                        snippet=item.get("snippet", ""),
                        position=idx + 1
                    )
                )

            total = data.get("search_information", {}).get("total_results", 0)
            # Handle string total_results
            if isinstance(total, str):
                total = int(total.replace(",", ""))

            return GoogleSearchOutput(
                results=results,
                total_results=total
            )

        except requests.HTTPError as e:
            if e.response.status_code == 429:
                raise RateLimitError("SerpAPI rate limit exceeded") from e
            elif e.response.status_code == 401:
                raise AuthenticationError("Invalid SerpAPI key") from e
            else:
                raise ToolExecutionError(f"HTTP error: {e}") from e
        except requests.RequestException as e:
            raise ToolExecutionError(f"Request failed: {e}") from e
        except (KeyError, ValueError) as e:
            raise ToolExecutionError(f"Failed to parse response: {e}") from e
