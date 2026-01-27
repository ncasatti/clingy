"""Base command interface that all commands must implement"""

from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Optional

from manager_core.core.logger import log_error, log_info
from manager_core.core.menu import MenuNode


class BaseCommand(ABC):
    """
    Abstract base class for all CLI commands

    Each command must implement:
    - name: Command name (e.g., "greet", "files")
    - help: Short help text
    - description: Detailed description (optional)
    - epilog: Usage examples (optional)
    - add_arguments(): Add command-specific arguments
    - execute(): Run the command logic
    - get_menu_tree(): Return menu tree for interactive mode
    """

    name: str = ""
    help: str = ""
    description: Optional[str] = None
    epilog: Optional[str] = None

    @abstractmethod
    def add_arguments(self, parser: ArgumentParser):
        """
        Add command-specific arguments to the parser

        Args:
            parser: ArgumentParser to add arguments to
        """
        pass

    @abstractmethod
    def execute(self, args: Namespace) -> bool:
        """
        Execute the command

        Args:
            args: Parsed command-line arguments

        Returns:
            True if command executed successfully, False otherwise
        """
        pass

    def get_description(self) -> str:
        """Get command description (fallback to help if not set)"""
        return self.description or self.help

    def get_epilog(self) -> Optional[str]:
        """Get command epilog"""
        return self.epilog

    @abstractmethod
    def get_menu_tree(self) -> MenuNode:
        """
        Return menu tree for interactive mode.

        REQUIRED: All commands must define their menu.

        For simple commands without submenus, use:
            MenuNode(
                label="Command Name",
                emoji=Emojis.ICON,
                action=lambda: self.execute(Namespace())
            )

        Returns:
            MenuNode with menu structure
        """
        pass
