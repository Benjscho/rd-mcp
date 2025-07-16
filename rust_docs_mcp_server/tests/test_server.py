"""
Tests for the server module.
"""

import pytest

from rust_docs_mcp_server.server import create_server
from rust_docs_mcp_server.tools.search_tools import (
    generate_crate_docs,
    get_rust_doc_details,
    search_rust_docs,
)


async def test_server_initialization():
    """Test that the server initializes correctly."""
    # Create the server
    server = create_server()
    
    # Check that the server is initialized
    assert server is not None


async def test_tool_registration():
    """Test that the tools are registered with their implementations."""
    # Check that each tool has a name and description
    assert hasattr(search_rust_docs, "name")
    assert hasattr(search_rust_docs, "description")
    assert hasattr(get_rust_doc_details, "name")
    assert hasattr(get_rust_doc_details, "description")
    assert hasattr(generate_crate_docs, "name")
    assert hasattr(generate_crate_docs, "description")
    
    # Check that the names are correct
    assert search_rust_docs.name == "search_rust_docs"
    assert get_rust_doc_details.name == "get_rust_doc_details"
    assert generate_crate_docs.name == "generate_crate_docs"


async def test_search_tool_parameters():
    """Test that the search tool has the expected parameters."""
    # Check that the search tool function has the expected parameters
    import inspect
    sig = inspect.signature(search_rust_docs)
    
    # Check parameters
    assert "query" in sig.parameters
    assert "crate" in sig.parameters
    assert "max_results" in sig.parameters
    assert "include_std" in sig.parameters
    
    # Check that query is required and others are optional
    assert sig.parameters["query"].default == inspect.Parameter.empty
    assert sig.parameters["crate"].default is None
    assert sig.parameters["max_results"].default == 5
    assert sig.parameters["include_std"].default is True