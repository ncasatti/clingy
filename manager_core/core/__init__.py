"""
Core utilities for manager-core framework
"""

from manager_core.core.discovery import (
    find_manager_root,
    load_project_config,
    get_project_context,
)

__all__ = [
    "find_manager_root",
    "load_project_config",
    "get_project_context",
]
