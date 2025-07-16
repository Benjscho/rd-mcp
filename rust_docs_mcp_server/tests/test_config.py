"""
Tests for the configuration module.
"""

import os
import tempfile
from pathlib import Path

import pytest

from rust_docs_mcp_server.utils.config import ServerConfig, load_config


def test_default_config():
    """Test that the default configuration is created correctly."""
    config = ServerConfig()
    
    # Check default values
    assert config.db_path.name == "rust_docs_db"
    assert config.cache_size_limit == 1024 * 1024 * 1024  # 1 GB
    assert config.cache_ttl == 7 * 24 * 60 * 60  # 7 days
    assert config.default_crates == ["std"]
    assert config.max_search_results == 10
    assert config.fuzzy_match_threshold == 0.7


def test_config_validation():
    """Test that configuration validation works correctly."""
    # Test valid configuration
    config = ServerConfig(
        db_path="./test_db",
        cache_size_limit=500 * 1024 * 1024,
        cache_ttl=24 * 60 * 60,
        default_crates=["std", "serde"],
        max_search_results=5,
        fuzzy_match_threshold=0.8
    )
    
    assert config.db_path.name == "test_db"
    assert config.cache_size_limit == 500 * 1024 * 1024
    assert config.cache_ttl == 24 * 60 * 60
    assert config.default_crates == ["std", "serde"]
    assert config.max_search_results == 5
    assert config.fuzzy_match_threshold == 0.8
    
    # Test invalid fuzzy match threshold
    with pytest.raises(ValueError):
        ServerConfig(fuzzy_match_threshold=1.5)


def test_load_config_from_env():
    """Test loading configuration from environment variables."""
    # Set environment variables
    os.environ["RUST_DOCS_DB_PATH"] = "./env_test_db"
    os.environ["RUST_DOCS_CACHE_SIZE_LIMIT"] = "100000000"  # 100 MB
    os.environ["RUST_DOCS_DEFAULT_CRATES"] = "std,serde,tokio"
    
    try:
        # Load configuration
        config = load_config()
        
        # Check that environment variables were applied
        assert config.db_path.name == "env_test_db"
        assert config.cache_size_limit == 100000000
        assert config.default_crates == ["std", "serde", "tokio"]
        
        # Check that other values are defaults
        assert config.cache_ttl == 7 * 24 * 60 * 60
        assert config.max_search_results == 10
        assert config.fuzzy_match_threshold == 0.7
    finally:
        # Clean up environment variables
        del os.environ["RUST_DOCS_DB_PATH"]
        del os.environ["RUST_DOCS_CACHE_SIZE_LIMIT"]
        del os.environ["RUST_DOCS_DEFAULT_CRATES"]


def test_load_config_from_file():
    """Test loading configuration from a file."""
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json") as temp_file:
        temp_file.write("""
        {
            "db_path": "./file_test_db",
            "cache_size_limit": 200000000,
            "default_crates": ["std", "rand"],
            "fuzzy_match_threshold": 0.9
        }
        """)
        temp_file.flush()
        
        # Load configuration from file
        config = load_config(temp_file.name)
        
        # Check that file values were applied
        assert config.db_path.name == "file_test_db"
        assert config.cache_size_limit == 200000000
        assert config.default_crates == ["std", "rand"]
        assert config.fuzzy_match_threshold == 0.9
        
        # Check that other values are defaults
        assert config.cache_ttl == 7 * 24 * 60 * 60
        assert config.max_search_results == 10