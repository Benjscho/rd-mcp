# MCP Configuration Guidelines

This document provides guidance on configuring MCP (Model Context Protocol) for this project.

## MCP Configuration Files

There are two configuration files for MCP:

1. **Workspace level**: `.kiro/settings/mcp.json` (project-specific)
2. **User level**: `~/.kiro/settings/mcp.json` (global across workspaces)

When both exist, configurations are merged with workspace-level taking precedence for server name conflicts.

## Basic Configuration Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["package-name@version"],
      "env": {
        "ENV_VAR1": "value1",
        "ENV_VAR2": "value2"
      },
      "disabled": false,
      "autoApprove": ["tool_name1", "tool_name2"]
    }
  }
}
```

## Configuration Options

- **command**: The command to run the MCP server (use `uvx` for Python servers)
- **args**: Arguments to pass to the command
- **env**: Environment variables for the server
- **disabled**: Whether the server is disabled (default: false)
- **autoApprove**: List of tool names to auto-approve (skip confirmation)

## Example Configuration

Here's an example configuration for our Python MCP server:

```json
{
  "mcpServers": {
    "python-mcp-server": {
      "command": "uvx",
      "args": ["my-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "INFO",
        "PYTHONPATH": "${workspaceFolder}"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Setting Up MCP Configuration

To set up the MCP configuration:

1. Create the workspace-level configuration file:
   ```bash
   mkdir -p .kiro/settings
   touch .kiro/settings/mcp.json
   ```

2. Edit the file with your server configuration.

3. For user-level configuration (optional):
   ```bash
   mkdir -p ~/.kiro/settings
   touch ~/.kiro/settings/mcp.json
   ```

## Running and Managing MCP Servers

- Servers reconnect automatically when configuration changes
- Use the MCP Server view in the Kiro feature panel to manage servers
- Search the command palette for "MCP" to find relevant commands

## Installing `uv` and `uvx`

To install `uv` and `uvx`:

```bash
# Using pip
pip install uv

# Using Homebrew on macOS
brew install uv
```

For more installation options, refer to the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Best Practices

1. **Version Pinning**: Pin specific versions of MCP servers for stability
2. **Environment Variables**: Use environment variables for configuration
3. **Auto-Approve**: Only auto-approve tools that are safe and non-destructive
4. **Logging**: Configure appropriate log levels for development and production