"""
Pytest configuration and shared fixtures
"""

import pytest
from pathlib import Path


@pytest.fixture
def temp_project(tmp_path):
    """
    Create a temporary manager project structure.

    Returns:
        Path: Root directory of the temporary project
    """
    project = tmp_path / "test-project"
    project.mkdir()

    # Create commands directory
    commands_dir = project / "commands"
    commands_dir.mkdir()
    (commands_dir / "__init__.py").write_text("")

    # Create config.py
    config_content = '''"""Test project configuration"""

PROJECT_NAME = "Test Project"
PROJECT_VERSION = "1.0.0"
ITEMS = ["item-1", "item-2", "item-3"]

from manager_core.core.dependency import Dependency

DEPENDENCIES = [
    Dependency(
        name="fzf",
        command="fzf",
        description="Fuzzy finder",
        required=True,
    ),
]
'''
    (project / "config.py").write_text(config_content)

    return project


@pytest.fixture
def temp_project_with_command(temp_project):
    """
    Create a temporary project with a sample command.

    Returns:
        Path: Root directory of the project with a command
    """
    command_content = '''"""Sample test command"""
from argparse import ArgumentParser, Namespace
from manager_core.commands.base import BaseCommand
from manager_core.core.menu import MenuNode
from manager_core.core.emojis import Emojis


class TestCommand(BaseCommand):
    """Test command for testing"""
    
    name = "test"
    help = "Test command"
    description = "A test command for unit tests"
    
    def add_arguments(self, parser: ArgumentParser):
        """Add command arguments"""
        parser.add_argument("--value", default="default")
    
    def execute(self, args: Namespace) -> bool:
        """Execute the command"""
        return True
    
    def get_menu_tree(self) -> MenuNode:
        """Get menu tree"""
        return MenuNode(
            label="Test Command",
            emoji=Emojis.INFO,
            action=lambda: self.execute(Namespace(value="menu"))
        )
'''

    commands_dir = temp_project / "commands"
    (commands_dir / "test_command.py").write_text(command_content)

    return temp_project


@pytest.fixture
def empty_dir(tmp_path):
    """
    Create an empty temporary directory (no project).

    Returns:
        Path: Empty directory
    """
    empty = tmp_path / "empty"
    empty.mkdir()
    return empty
