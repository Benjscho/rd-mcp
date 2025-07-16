"""
Main server module for the Rust Documentation Search MCP Server.

This module initializes the FastMCP server and registers the MCP tools.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from rust_docs_mcp_server.tools.search_tools import (
    generate_crate_docs,
    get_rust_doc_details,
    search_rust_docs,
)
from rust_docs_mcp_server.utils.config import ServerConfig, load_config

# Configure logging
logging.basicConfig(
    level=os.getenv("FASTMCP_LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def create_server(config: Optional[ServerConfig] = None) -> FastMCP:
    """
    Create and configure the FastMCP server.
    
    Args:
        config: Optional server configuration
        
    Returns:
        FastMCP: The configured FastMCP server instance.
    """
    logger.info("Initializing Rust Documentation Search MCP Server")
    
    # Load configuration if not provided
    if config is None:
        config = load_config()
    
    # Make configuration available to tool functions
    # We're using a global variable here for simplicity
    import sys
    this_module = sys.modules[__name__]
    this_module.config = config
    
    # Create the FastMCP server
    server = FastMCP(
        tools=[search_rust_docs, get_rust_doc_details, generate_crate_docs],
    )
    
    logger.info("Server initialized successfully")
    return server


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: The parsed arguments
    """
    parser = argparse.ArgumentParser(description="Rust Documentation Search MCP Server")
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=os.getenv("FASTMCP_LOG_LEVEL", "INFO"),
        help="Logging level",
    )
    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the server.
    """
    # Parse command line arguments
    args = parse_args()
    
    # Configure logging
    logging.getLogger().setLevel(args.log_level)
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Create and run the server
        server = create_server(config)
        server.run()
    except Exception as e:
        logger.critical(f"Error starting server: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()