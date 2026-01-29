"""
Framework configuration for clingy

This file contains default configuration for the framework itself.
Project-specific configuration should be in the project's config.py.
"""

from clingy.core.dependency import Dependency

# ============================================================================
# Framework Metadata
# ============================================================================
PROJECT_NAME = "clingy"
PROJECT_VERSION = "1.0.0"


# ============================================================================
# Default Items (fallback if project doesn't define ITEMS)
# ============================================================================
ITEMS = []


# ============================================================================
# Framework Dependencies
# ============================================================================
DEPENDENCIES = [
    Dependency(
        name="fzf",
        command="fzf",
        description="Fuzzy finder for interactive menus",
        install_macos="brew install fzf",
        install_linux="sudo pacman -S fzf",
        required=True,
    ),
]
