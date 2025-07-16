# Rust Documentation Search MCP Server

An MCP server for generating, processing, and searching Rust documentation in a format optimized for LLM consumption.

## Features

- Generate Rust documentation using `cargo doc`
- Process documentation into LLM-friendly formats
- Fuzzy search capabilities for finding relevant documentation
- MCP tools for integration with Kiro

## Installation

```bash
# Using uv
uv pip install -e .
```

## Configuration

Create a `.kiro/settings/mcp.json` file with the following configuration:

```json
{
  "mcpServers": {
    "rust-docs": {
      "command": "uvx",
      "args": ["rust_docs_mcp_server"],
      "env": {
        "FASTMCP_LOG_LEVEL": "INFO"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Usage

The server provides the following MCP tools:

- `search_rust_docs`: Search Rust documentation using fuzzy matching
- `get_rust_doc_details`: Get detailed documentation for a specific Rust item
- `generate_crate_docs`: Generate and process documentation for a specific crate

## Development

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT