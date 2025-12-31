"""Web Fetch tool for retrieving web page content."""

from typing import Literal
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, HttpUrl

from ...base import BaseTool
from ...exceptions import ToolExecutionError


class WebFetchInput(BaseModel):
    """Input parameters for Web Fetch."""

    url: str = Field(description="The URL to fetch")
    mode: Literal["text", "html"] = Field(
        default="text",
        description="Output mode: 'text' for cleaned readable text, 'html' for raw HTML"
    )
    timeout: int = Field(
        default=30,
        ge=5,
        le=120,
        description="Request timeout in seconds (5-120)"
    )


class WebFetchOutput(BaseModel):
    """Output from Web Fetch."""

    url: str = Field(description="The fetched URL (may differ from input due to redirects)")
    content: str = Field(description="Page content (cleaned text or raw HTML)")
    mode: str = Field(description="Mode used: 'text' or 'html'")
    title: str | None = Field(description="Page title if available")


class WebFetchTool(BaseTool[WebFetchInput, WebFetchOutput]):
    """
    Fetch web page content as cleaned text or raw HTML.

    Retrieves content from any URL and returns either:
    - Clean readable text (strips scripts, styles, navigation)
    - Raw HTML (complete markup)

    Use text mode for content analysis, HTML mode when you need full structure.

    Example:
        >>> tool = WebFetchTool()
        >>> result = tool.validate_and_execute(
        ...     url="https://example.com",
        ...     mode="text"
        ... )
        >>> print(result.content)
    """

    name = "web_fetch"
    description = (
        "Fetch content from a URL. Returns either cleaned readable text or raw HTML. "
        "Use 'text' mode for reading and analysis, 'html' mode when you need the "
        "full page structure. Automatically handles redirects and common web formats."
    )
    input_model = WebFetchInput
    output_model = WebFetchOutput

    def __init__(self):
        """Initialize the Web Fetch tool."""
        pass

    def execute(self, input: WebFetchInput) -> WebFetchOutput:
        """
        Fetch content from a URL.

        Args:
            input: Validated fetch parameters

        Returns:
            Page content as text or HTML

        Raises:
            ToolExecutionError: If fetch fails or content is invalid
        """
        try:
            # Fetch the page
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; tools-for-agents/0.1.0; +https://github.com/yourusername/tools-for-agents)"
            }

            response = requests.get(
                input.url,
                headers=headers,
                timeout=input.timeout,
                allow_redirects=True
            )
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title_tag = soup.find("title")
            title = title_tag.get_text(strip=True) if title_tag else None

            # Get content based on mode
            if input.mode == "html":
                content = str(soup)
            else:
                # Remove scripts, styles, and other non-content elements
                for element in soup(["script", "style", "nav", "footer", "header"]):
                    element.decompose()

                # Get text with reasonable formatting
                content = soup.get_text(separator="\n", strip=True)

                # Clean up excessive newlines
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                content = "\n".join(lines)

            return WebFetchOutput(
                url=response.url,  # Final URL after redirects
                content=content,
                mode=input.mode,
                title=title
            )

        except requests.HTTPError as e:
            raise ToolExecutionError(
                f"HTTP error fetching {input.url}: {e.response.status_code}"
            ) from e
        except requests.RequestException as e:
            raise ToolExecutionError(f"Failed to fetch {input.url}: {e}") from e
        except Exception as e:
            raise ToolExecutionError(f"Error processing content: {e}") from e
