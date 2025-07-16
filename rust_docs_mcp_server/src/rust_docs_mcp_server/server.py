"""
Main server module for the Rust Documentation Search MCP Server.

This module initializes the FastMCP server and registers the MCP tools.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from rust_docs_mcp_server.tools.search_tools import (
    generate_crate_docs,
    get_rust_doc_details,
    search_rust_docs,
)

# Configure logging
logging.basicConfig(
    level=os.getenv("FASTMCP_LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def create_server() -> FastMCP:
    """
    Create and configure the FastMCP server.

    Returns:
        FastMCP: The configured FastMCP server instance.
    """
    logger.info("Initializing Rust Documentation Search MCP Server")

    # Create the FastMCP server
    server = FastMCP(
        tools=[search_rust_docs, get_rust_doc_details, generate_crate_docs],
        server_name="rust-docs-mcp-server",
        server_version="0.1.0",
    )

    logger.info("Server initialized successfully")
    return server


def main() -> None:
    """
    Main entry point for the server.
    """
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()