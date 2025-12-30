"""Custom exceptions for tools."""


class ToolExecutionError(Exception):
    """Base exception for tool execution failures."""
    pass


class AuthenticationError(ToolExecutionError):
    """Raised when authentication fails (invalid API key, etc.)."""
    pass


class RateLimitError(ToolExecutionError):
    """Raised when API rate limit is exceeded."""
    pass


class ValidationError(ToolExecutionError):
    """Raised when input validation fails."""
    pass
