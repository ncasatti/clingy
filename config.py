"""
Project-specific configuration

CUSTOMIZE THIS FILE FOR YOUR PROJECT
This is the only file that needs to be modified when using this manager in a different project.
"""

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
# Required System Dependencies
# ============================================================================
# Tools required to run this manager
# Add new dependencies here as needed
REQUIRED_DEPENDENCIES = {
    "fzf": {
        "command": "fzf",
        "check": "--version",
        "install": {
            "ubuntu": "sudo apt install fzf",
            "debian": "sudo apt install fzf",
            "macos": "brew install fzf",
            "arch": "sudo pacman -S fzf",
            "fedora": "sudo dnf install fzf",
        },
        "description": "Fuzzy finder for interactive menus",
        "required": True,
    },
    "python": {
        "command": "python",
        "check": "--version",
        "install": {
            "ubuntu": "sudo apt install python3",
            "macos": "brew install python3",
        },
        "description": "Python 3 interpreter",
        "required": True,
    },
}
