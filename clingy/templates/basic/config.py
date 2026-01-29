"""
Project-specific configuration

CUSTOMIZE THIS FILE FOR YOUR PROJECT
This is the only file that needs to be modified when using clingy in your project.
"""

from clingy.core.dependency import Dependency

# ============================================================================
# Project Metadata
# ============================================================================
PROJECT_NAME = "My CLI Tool"
PROJECT_VERSION = "1.0.0"


# ============================================================================
# Core Items List
# ============================================================================
# Example list of items that your CLI will manage
# UPDATE THIS LIST FOR YOUR PROJECT
ITEMS = [
    "example-item-1",
    "example-item-2",
    "example-item-3",
]


# ============================================================================
# Paths
# ============================================================================
# Example paths (adjust as needed)
DATA_DIR = "data"
OUTPUT_DIR = "output"


# ============================================================================
# Required Dependencies
# ============================================================================
DEPENDENCIES = [
    Dependency(
        name="fzf",
        command="fzf",
        description="Fuzzy finder for interactive menus",
        install_macos="brew install fzf",
        install_linux="sudo pacman -S fzf",  # Arch
        required=True,
    ),
    Dependency(
        name="python",
        command="python",
        description="Python 3 interpreter",
        install_macos="brew install python3",
        install_linux="sudo pacman -S python3",  # Arch
        required=True,
    ),
]
