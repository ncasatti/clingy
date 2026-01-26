"""
Command auto-discovery system

This module automatically discovers and registers all command classes in the commands/ directory.
To add a new command, simply create a new file with a class that inherits from BaseCommand.
"""

import importlib
import inspect
from pathlib import Path
from typing import Dict, Type

from manager_core.commands.base import BaseCommand


def discover_commands() -> Dict[str, Type[BaseCommand]]:
    """
    Automatically discover all command classes in the commands directory

    Returns:
        Dictionary mapping command names to command classes
    """
    commands = {}
    commands_dir = Path(__file__).parent

    # Iterate through all Python files in commands directory
    for file_path in commands_dir.glob("*.py"):
        # Skip __init__.py and base.py
        if file_path.stem in ("__init__", "base"):
            continue

        try:
            # Import the module
            module_name = f"manager_core.commands.{file_path.stem}"
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

    return commands


def get_command_names() -> list:
    """
    Get list of all available command names

    Returns:
        Sorted list of command names
    """
    commands = discover_commands()
    return sorted(commands.keys())


def get_command(name: str) -> Type[BaseCommand]:
    """
    Get a specific command class by name

    Args:
        name: Command name

    Returns:
        Command class

    Raises:
        KeyError: If command not found
    """
    commands = discover_commands()
    if name not in commands:
        raise KeyError(
            f"Command '{name}' not found. Available commands: {', '.join(commands.keys())}"
        )
    return commands[name]
