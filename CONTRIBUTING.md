# Contributing to Tools for Agents

We'd love your help! This guide shows you how to contribute tools, examples, and improvements.

## Adding a New Tool

We follow a structured approach to keep the project organized and maintainable.

### 1. Check If It Fits

Before building, ask yourself:
- Does this tool solve a real problem for agents?
- Is it framework-agnostic (works with any LLM)?
- Can it be used in production?

If yes, open an issue to discuss your idea first.

### 2. Structure

Each tool lives in its own directory:

```
src/tools_for_agents/tools/
└── your_tool_name/
    ├── __init__.py
    ├── your_tool_name_tool.py
    ├── README.md
    └── test_your_tool_name_tool.py (optional but encouraged)
```

**Naming convention:** `{tool_name}_tool.py`

### 3. Implementation

Your tool should extend `BaseTool`:

```python
from pydantic import BaseModel, Field
from ...base import BaseTool

class YourToolInput(BaseModel):
    """Input parameters."""
    param: str = Field(description="Description of parameter")

class YourToolOutput(BaseModel):
    """Output structure."""
    result: str

class YourToolName(BaseTool[YourToolInput, YourToolOutput]):
    name = "your_tool_name"
    description = "Clear description of what it does and when to use it"
    input_model = YourToolInput
    output_model = YourToolOutput

    def __init__(self, api_key: str | None = None):
        # Initialize your tool
        pass

    def execute(self, input: YourToolInput) -> YourToolOutput:
        # Tool logic here
        return YourToolOutput(result="...")
```

**What you get automatically:**
- Input/output validation via Pydantic
- OpenAI and Anthropic schema generation
- Type safety

### 4. Documentation

Create `README.md` in your tool directory:

```markdown
# Your Tool Name

One-sentence description of what it does.

## Usage

[Code example]

## Parameters

**Input:**
- List parameters

**Output:**
- List output fields

## Requirements

API keys, dependencies, or "None (free)"

## Error Handling

What errors it raises
```

### 5. Required Updates

**You MUST update these files when adding a tool:**

- [ ] Create `tools/{tool_name}/` directory
- [ ] Add `{tool_name}_tool.py`
- [ ] Add `README.md` in tool directory
- [ ] Add `__init__.py` in tool directory:
  ```python
  from .your_tool_name_tool import YourToolName
  __all__ = ["YourToolName"]
  ```
- [ ] Update `tools/__init__.py`:
  ```python
  from .your_tool_name import YourToolName
  __all__ = [..., "YourToolName"]
  ```
- [ ] Update `src/tools_for_agents/__init__.py`:
  ```python
  from .tools import ..., YourToolName
  __all__ = [..., "YourToolName"]
  ```
- [ ] Add entry to `tools/CATALOG.md`
- [ ] Add row to main `README.md` table

### 6. Submit PR

**PR Title:** `Add {ToolName}`

**PR Description:**
- What the tool does
- Why it's useful for agents
- Any dependencies added
- Example usage

## Code Standards

- Use Pydantic v2 for all models
- Include docstrings for classes and methods
- Handle errors gracefully (use our exception classes)
- Follow existing naming patterns
- Keep dependencies minimal

## Questions?

Open an issue or discussion. We're here to help!
