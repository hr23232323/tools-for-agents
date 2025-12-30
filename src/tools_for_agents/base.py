"""Base class for all tools."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel


# Type variables for input/output
InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


class BaseTool(ABC, Generic[InputT, OutputT]):
    """
    Base class for all tools.

    Tools provide discrete, composable operations for LLM agents.
    Contributors implement the execute() method with their tool logic.

    Attributes:
        name: The tool's unique identifier
        description: Detailed description of what the tool does and when to use it
        input_model: Pydantic model defining expected input parameters
        output_model: Pydantic model defining output structure
    """

    name: str
    description: str
    input_model: type[InputT]
    output_model: type[OutputT]

    @abstractmethod
    def execute(self, input: InputT) -> OutputT:
        """
        Execute the tool with validated input.

        This is the core logic that tool implementers must define.
        Input is already validated via Pydantic, output will be validated on return.

        Args:
            input: Validated input conforming to input_model

        Returns:
            Output conforming to output_model

        Raises:
            ToolExecutionError: If tool execution fails
        """
        pass

    def validate_and_execute(self, **kwargs) -> OutputT:
        """
        Public interface: validates input, executes, returns validated output.

        Args:
            **kwargs: Raw input arguments to be validated

        Returns:
            Validated output from tool execution
        """
        validated_input = self.input_model(**kwargs)
        result = self.execute(validated_input)
        return result

    def to_openai_schema(self) -> dict:
        """
        Generate OpenAI function calling schema.

        Returns:
            Dict conforming to OpenAI's function schema format
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_model.model_json_schema(),
            }
        }

    def to_anthropic_schema(self) -> dict:
        """
        Generate Anthropic tool use schema.

        Returns:
            Dict conforming to Anthropic's tool schema format
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_model.model_json_schema()
        }
