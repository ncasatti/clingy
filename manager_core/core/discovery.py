"""
Context discovery system for manager-core

This module provides functions to detect and load project-specific configuration
by searching for manager projects in the directory tree.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any


def find_manager_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Search for manager project root by looking for commands/ directory and config.py
    
    Searches upward from start_path until it finds a directory containing both:
    - commands/ directory
    - config.py file
    
    Args:
        start_path: Directory to start searching from (defaults to current directory)
    
    Returns:
        Path to project root, or None if not found
    """
    if start_path is None:
        start_path = Path.cwd()
    
    current = start_path.resolve()
    
    # Search upward until we hit the filesystem root
    while True:
        # Check if this directory has both commands/ and config.py
        commands_dir = current / "commands"
        config_file = current / "config.py"
        
        if commands_dir.is_dir() and config_file.is_file():
            return current
        
        # Move up one directory
        parent = current.parent
        if parent == current:
            # We've reached the filesystem root
            return None
        
        current = parent


def load_project_config(project_root: Path) -> Dict[str, Any]:
    """
    Load project-specific configuration from config.py
    
    Args:
        project_root: Path to project root directory
    
    Returns:
        Dictionary with configuration values
    
    Raises:
        ImportError: If config.py cannot be loaded
    """
    config_path = project_root / "config.py"
    
    if not config_path.exists():
        raise ImportError(f"config.py not found at {config_path}")
    
    # Add project root to sys.path temporarily
    sys.path.insert(0, str(project_root))
    
    try:
        # Import the config module
        import importlib.util
        spec = importlib.util.spec_from_file_location("project_config", config_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Failed to load config from {config_path}")
        
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        
        # Extract configuration values
        config = {}
        for attr in dir(config_module):
            if not attr.startswith("_"):
                config[attr] = getattr(config_module, attr)
        
        return config
    
    finally:
        # Remove project root from sys.path
        sys.path.pop(0)


def get_project_context() -> Optional[Dict[str, Any]]:
    """
    Get complete project context (root path + configuration)
    
    Returns:
        Dictionary with 'root' (Path) and 'config' (Dict), or None if no project found
    """
    project_root = find_manager_root()
    
    if project_root is None:
        return None
    
    try:
        config = load_project_config(project_root)
        return {
            "root": project_root,
            "config": config
        }
    except Exception as e:
        # If config loading fails, return None
        return None
