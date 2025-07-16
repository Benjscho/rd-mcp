"""
Configuration handling for the Rust Documentation Search MCP Server.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pydantic
from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)


class ServerConfig(BaseModel):
    """
    Configuration for the Rust Documentation Search MCP Server.
    """
    
    # Database configuration
    db_path: Path = Field(
        default=Path("./rust_docs_db"),
        description="Path to the documentation database"
    )
    
    # Cache configuration
    cache_size_limit: int = Field(
        default=1024 * 1024 * 1024,  # 1 GB
        description="Cache size limit in bytes"
    )
    cache_ttl: int = Field(
        default=7 * 24 * 60 * 60,  # 7 days
        description="Cache time-to-live in seconds"
    )
    
    # Documentation configuration
    default_crates: List[str] = Field(
        default=["std"],
        description="Default crates to include in documentation"
    )
    
    # Search configuration
    max_search_results: int = Field(
        default=10,
        description="Maximum number of search results to return"
    )
    fuzzy_match_threshold: float = Field(
        default=0.7,
        description="Threshold for fuzzy matching (0.0 to 1.0)"
    )
    
    @validator("db_path")
    def validate_db_path(cls, v: Path) -> Path:
        """Validate and create the database path if it doesn't exist."""
        v = v.expanduser().resolve()
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @validator("fuzzy_match_threshold")
    def validate_fuzzy_match_threshold(cls, v: float) -> float:
        """Validate the fuzzy match threshold."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Fuzzy match threshold must be between 0.0 and 1.0")
        return v


def load_config(config_path: Optional[Union[str, Path]] = None) -> ServerConfig:
    """
    Load the server configuration from environment variables or a config file.
    
    Args:
        config_path: Optional path to a configuration file
        
    Returns:
        ServerConfig: The loaded configuration
    """
    # Start with default configuration
    config_dict: Dict[str, Any] = {}
    
    # Load from environment variables
    if os.getenv("RUST_DOCS_DB_PATH"):
        config_dict["db_path"] = os.getenv("RUST_DOCS_DB_PATH")
    
    if os.getenv("RUST_DOCS_CACHE_SIZE_LIMIT"):
        try:
            config_dict["cache_size_limit"] = int(os.getenv("RUST_DOCS_CACHE_SIZE_LIMIT", "0"))
        except ValueError:
            logger.warning("Invalid RUST_DOCS_CACHE_SIZE_LIMIT, using default")
    
    if os.getenv("RUST_DOCS_CACHE_TTL"):
        try:
            config_dict["cache_ttl"] = int(os.getenv("RUST_DOCS_CACHE_TTL", "0"))
        except ValueError:
            logger.warning("Invalid RUST_DOCS_CACHE_TTL, using default")
    
    if os.getenv("RUST_DOCS_DEFAULT_CRATES"):
        config_dict["default_crates"] = os.getenv("RUST_DOCS_DEFAULT_CRATES", "").split(",")
    
    if os.getenv("RUST_DOCS_MAX_SEARCH_RESULTS"):
        try:
            config_dict["max_search_results"] = int(os.getenv("RUST_DOCS_MAX_SEARCH_RESULTS", "0"))
        except ValueError:
            logger.warning("Invalid RUST_DOCS_MAX_SEARCH_RESULTS, using default")
    
    if os.getenv("RUST_DOCS_FUZZY_MATCH_THRESHOLD"):
        try:
            config_dict["fuzzy_match_threshold"] = float(os.getenv("RUST_DOCS_FUZZY_MATCH_THRESHOLD", "0"))
        except ValueError:
            logger.warning("Invalid RUST_DOCS_FUZZY_MATCH_THRESHOLD, using default")
    
    # Load from config file if provided
    if config_path:
        try:
            config_path = Path(config_path).expanduser().resolve()
            if config_path.exists():
                import json
                with open(config_path, "r") as f:
                    file_config = json.load(f)
                config_dict.update(file_config)
            else:
                logger.warning(f"Config file not found: {config_path}")
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
    
    # Create and validate the configuration
    try:
        config = ServerConfig(**config_dict)
        logger.info(f"Configuration loaded successfully: {config.model_dump()}")
        return config
    except pydantic.ValidationError as e:
        logger.error(f"Configuration validation error: {e}")
        logger.warning("Using default configuration")
        return ServerConfig()