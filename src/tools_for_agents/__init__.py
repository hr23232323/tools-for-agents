"""Tools for Agents - Runtime tools for LLM agents."""

from .base import BaseTool
from .exceptions import (
    ToolExecutionError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)
from .tools import GoogleSearchTool, WebFetchTool

__version__ = "0.1.0"

__all__ = [
    "BaseTool",
    "ToolExecutionError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "GoogleSearchTool",
    "WebFetchTool",
]
