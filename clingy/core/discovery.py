"""
Context discovery system for clingy

Finds clingy projects by looking for .clingy marker file.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def find_clingy_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Search for clingy project root by looking for .clingy marker file.

    Priority:
    1. CLINGY_ROOT environment variable (if set)
    2. .clingy marker file (searches upward and 1 level down)

    Args:
        start_path: Directory to start searching from (defaults to current directory)

    Returns:
        Path to project root, or None if not found
    """
    # Priority 1: Environment variable override
    env_root = os.getenv("CLINGY_ROOT")
    if env_root:
        path = Path(env_root).resolve()
        if _is_clingy_root(path):
            return path

    # Priority 2: Search for .clingy marker
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    # Search upward until filesystem root
    while True:
        # Check current directory for .clingy
        if _is_clingy_root(current):
            return current

        # Check subdirectories (1 level) for .clingy
        try:
            for subdir in current.iterdir():
                if subdir.is_dir() and _is_clingy_root(subdir):
                    return subdir
        except PermissionError:
            pass  # Skip directories we can't read

        # Move up one directory
        parent = current.parent
        if parent == current:
            return None  # Reached filesystem root
        current = parent


def _is_clingy_root(path: Path) -> bool:
    """
    Check if path is a valid clingy root.

    A valid clingy root must have:
    - .clingy marker file
    - commands/ directory
    - config.py file

    Args:
        path: Path to check

    Returns:
        True if path is a valid clingy root
    """
    marker = path / ".clingy"
    commands_dir = path / "commands"
    config_file = path / "config.py"

    return marker.is_file() and commands_dir.is_dir() and config_file.is_file()


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
    project_root = find_clingy_root()

    if project_root is None:
        return None

    try:
        config = load_project_config(project_root)
        return {"root": project_root, "config": config}
    except Exception:
        return None
