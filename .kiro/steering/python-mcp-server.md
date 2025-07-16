# Python MCP Server Development Guidelines

This document provides steering guidelines for developing Python MCP (Model Context Protocol) servers in this project.

## Project Setup

### Package Management with `uv`

- Use `uv` for Python package management instead of pip or conda
- Create and activate virtual environments with `uv venv`
- Install dependencies with `uv pip install`
- Pin dependencies in a `requirements.txt` file or use `pyproject.toml`

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
uv pip install -r requirements.txt
# or
uv pip install -e .
```

### Project Structure

Follow this structure for MCP server projects:

```
mcp_server/
├── pyproject.toml
├── README.md
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py
│       ├── tools/
│       │   ├── __init__.py
│       │   └── tool_implementations.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
└── tests/
    ├── __init__.py
    └── test_tools.py
```

## MCP Server Implementation

### Tool Definition

- Define tools using the FastMCP schema format
- Each tool should have a clear description, parameters with types, and required fields
- Use JSON Schema for parameter validation

```python
tool_definition = {
    "name": "example_tool",
    "description": "This tool does something useful",
    "parameters": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Description of parameter 1"
            },
            "param2": {
                "type": "integer",
                "description": "Description of parameter 2"
            }
        },
        "required": ["param1"]
    }
}
```

### Tool Implementation

- Implement each tool as a separate function
- Use type hints for parameters and return values
- Include comprehensive docstrings
- Handle errors gracefully with appropriate error messages

```python
async def example_tool(param1: str, param2: int = 0) -> dict:
    """
    Example tool implementation.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2, defaults to 0
        
    Returns:
        Dict containing the tool response
        
    Raises:
        ValueError: If parameters are invalid
    """
    try:
        # Tool implementation
        result = {"status": "success", "data": f"Processed {param1} with value {param2}"}
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### Server Configuration

- Use environment variables for configuration
- Provide sensible defaults
- Include logging configuration

```python
import os
import logging
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=os.getenv("FASTMCP_LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Initialize server
server = FastMCP(
    tools=[example_tool],
    server_name="my-mcp-server",
    server_version="0.1.0"
)

# Run server
if __name__ == "__main__":
    server.run()
```

## Testing

- Write unit tests for all tool implementations
- Use pytest for testing
- Mock external dependencies
- Test both success and error cases

```python
import pytest
from mcp_server.tools.tool_implementations import example_tool

async def test_example_tool_success():
    result = await example_tool("test", 42)
    assert result["status"] == "success"
    assert "test" in result["data"]
    assert "42" in result["data"]

async def test_example_tool_error():
    with pytest.raises(ValueError):
        await example_tool("")  # Invalid input
```

## Running the Server

- Use `uvx` for running the server in development
- For production, consider containerization with Docker

```bash
# Development
uvx my_mcp_server

# Or with specific module path
uvx -m mcp_server.server
```

## Best Practices

1. **Error Handling**: Always handle exceptions and provide meaningful error messages
2. **Validation**: Validate all inputs before processing
3. **Documentation**: Document all tools and parameters thoroughly
4. **Logging**: Use appropriate logging levels for different types of messages
5. **Security**: Never hardcode sensitive information; use environment variables
6. **Performance**: Consider asynchronous operations for I/O-bound tasks
7. **Testing**: Maintain high test coverage for all tool implementations