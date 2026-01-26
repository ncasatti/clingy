"""
System dependency definition and management

Provides a type-safe model for defining system dependencies (binaries, tools, etc.)
that the CLI manager requires to function properly.
"""

from typing import NamedTuple, Optional


class Dependency(NamedTuple):
    """
    System dependency definition.

    Attributes:
        name: Dependency identifier (e.g., "fzf", "python")
        command: Command to check (e.g., "fzf", "python")
        description: Human-readable description
        check_arg: Argument for version check (default: "--version")
        install_macos: Installation command for macOS (optional)
        install_linux: Installation command for Linux (optional)
        install_other: Generic installation command (optional)
        required: Whether this dependency is required (default: True)

    Example:
        >>> dep = Dependency(
        ...     name="fzf",
        ...     command="fzf",
        ...     description="Fuzzy finder",
        ...     install_macos="brew install fzf",
        ...     install_linux="sudo apt install fzf",
        ...     required=True
        ... )
    """

    name: str
    command: str
    description: str
    check_arg: str = "--version"
    install_macos: Optional[str] = None
    install_linux: Optional[str] = None
    install_other: Optional[str] = None
    required: bool = True
