"""
CLI context builder for manager-core

This module handles context detection and command discovery for both
framework commands and project-specific commands.
"""

import importlib
import inspect
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Type

from manager_core.commands.base import BaseCommand
from manager_core.core.discovery import find_manager_root, load_project_config


@dataclass
class CLIContext:
    """
    Context information for CLI execution

    Attributes:
        has_project: Whether a manager project was detected
        project_root: Path to project root (None if no project)
        project_config: Project configuration dict (None if no project)
        commands: Dictionary of available commands
    """

    has_project: bool
    project_root: Optional[Path]
    project_config: Optional[Dict]
    commands: Dict[str, Type[BaseCommand]]


def _discover_framework_commands() -> Dict[str, Type[BaseCommand]]:
    """
    Discover commands bundled with manager-core framework

    Returns:
        Dictionary mapping command names to command classes
    """
    from manager_core.commands import discover_commands

    return discover_commands()


def _discover_project_commands(project_root: Path) -> Dict[str, Type[BaseCommand]]:
    """
    Discover commands in a manager project

    Args:
        project_root: Path to project root directory

    Returns:
        Dictionary mapping command names to command classes
    """
    commands = {}
    commands_dir = project_root / "commands"

    if not commands_dir.is_dir():
        return commands

    # Add project root to sys.path temporarily
    sys.path.insert(0, str(project_root))

    try:
        # Iterate through all Python files in commands directory
        for file_path in commands_dir.glob("*.py"):
            # Skip __init__.py and base.py
            if file_path.stem in ("__init__", "base"):
                continue

            try:
                # Import the module
                module_name = f"commands.{file_path.stem}"
                module = importlib.import_module(module_name)

                # Find all classes that inherit from BaseCommand
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Check if it's a BaseCommand subclass and not BaseCommand itself
                    if (
                        issubclass(obj, BaseCommand)
                        and obj is not BaseCommand
                        and hasattr(obj, "name")
                        and obj.name
                    ):
                        commands[obj.name] = obj

            except Exception as e:
                print(f"Warning: Failed to load command from {file_path}: {e}")
                continue

    finally:
        # Remove project root from sys.path
        sys.path.pop(0)

    return commands


def create_cli_context() -> CLIContext:
    """
    Create CLI context by detecting project and discovering commands

    Returns:
        CLIContext with project info and available commands
    """
    # Try to find a manager project
    project_root = find_manager_root()

    if project_root is None:
        # No project found - only framework commands available
        return CLIContext(
            has_project=False,
            project_root=None,
            project_config=None,
            commands=_discover_framework_commands(),
        )

    # Project found - load config and discover project commands
    try:
        project_config = load_project_config(project_root)
        project_commands = _discover_project_commands(project_root)

        # Merge framework and project commands (project commands take precedence)
        framework_commands = _discover_framework_commands()
        all_commands = {**framework_commands, **project_commands}

        return CLIContext(
            has_project=True,
            project_root=project_root,
            project_config=project_config,
            commands=all_commands,
        )

    except Exception as e:
        # If project loading fails, fall back to framework-only mode
        print(f"Warning: Failed to load project at {project_root}: {e}")
        return CLIContext(
            has_project=False,
            project_root=None,
            project_config=None,
            commands=_discover_framework_commands(),
        )
