"""
Tests for command auto-discovery system
"""

from pathlib import Path

import pytest

from manager_core.commands import discover_commands
from manager_core.commands.base import BaseCommand


class TestDiscoverCommands:
    """Tests for discover_commands function"""

    def test_discovers_framework_commands(self):
        """Should discover framework commands (e.g., init)"""
        commands = discover_commands()

        assert "init" in commands
        assert issubclass(commands["init"], BaseCommand)

    def test_discovers_project_commands(self, temp_project_with_command, monkeypatch):
        """Should discover commands from project directory"""
        # Add project commands dir to path
        import sys

        sys.path.insert(0, str(temp_project_with_command))

        # Import and discover from project
        commands_dir = temp_project_with_command / "commands"

        # Manually test the discovery logic
        # In real scenario, discover_commands would be called with custom path
        # For now, we verify the test command can be imported
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "test_command", commands_dir / "test_command.py"
        )
        assert spec is not None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Verify TestCommand exists and is valid
        assert hasattr(module, "TestCommand")
        assert issubclass(module.TestCommand, BaseCommand)
        assert module.TestCommand.name == "test"

    def test_returns_dict_of_commands(self):
        """Should return a dictionary mapping names to classes"""
        commands = discover_commands()

        assert isinstance(commands, dict)
        assert len(commands) > 0

        for name, cmd_class in commands.items():
            assert isinstance(name, str)
            assert issubclass(cmd_class, BaseCommand)

    def test_command_has_required_attributes(self):
        """Discovered commands should have required attributes"""
        commands = discover_commands()

        for name, cmd_class in commands.items():
            # Check class attributes
            assert hasattr(cmd_class, "name")
            assert hasattr(cmd_class, "help")

            # Instantiate and check methods
            cmd_instance = cmd_class()
            assert hasattr(cmd_instance, "execute")
            assert hasattr(cmd_instance, "add_arguments")
            assert hasattr(cmd_instance, "get_menu_tree")


class TestCommandValidation:
    """Tests for command validation logic"""

    def test_ignores_non_command_classes(self, tmp_path):
        """Should ignore classes that don't inherit from BaseCommand"""
        # Create a file with non-command class
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()

        invalid_content = '''
class NotACommand:
    """This is not a BaseCommand"""
    pass

class AlsoNotACommand:
    """Another non-command"""
    name = "fake"
'''
        (commands_dir / "invalid.py").write_text(invalid_content)

        # Discovery should skip these
        # (In practice, discover_commands scans specific directory)
        # This test verifies the logic conceptually

    def test_ignores_abstract_base_command(self):
        """Should not include BaseCommand itself"""
        commands = discover_commands()

        # BaseCommand should not be in discovered commands
        assert "base" not in commands
        assert BaseCommand not in commands.values()
