"""Base command interface that all commands must implement"""

from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Optional, List
from manager.config import ITEMS
from manager.core.logger import log_error, log_info
from manager.core.menu import MenuNode


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

    def _resolve_item_list(self, args: Namespace) -> List[str]:
        """
        Resolve item list from args, supporting both interactive mode and CLI mode.

        Priority:
        1. args.item_list (from interactive menu) - takes precedence
        2. args.item (from CLI) - filtered via _get_filtered_items()

        Args:
            args: Parsed command-line arguments

        Returns:
            List of item names to process
        """
        # Interactive mode: item_list is provided directly
        if hasattr(args, "item_list") and args.item_list:
            return args.item_list

        # CLI mode: filter based on item argument
        item_arg = getattr(args, "item", None)
        return self._get_filtered_items(item_arg)

    def _get_filtered_items(self, item_filter: Optional[str]) -> List[str]:
        """
        Get list of items to process, filtered if necessary.

        Args:
            item_filter: Specific item name or None for all

        Returns:
            List of valid item names (empty list if item doesn't exist)
        """
        if item_filter is None:
            return ITEMS

        # Validate item exists
        if item_filter not in ITEMS:
            log_error(f"Item '{item_filter}' does not exist in the available items list")
            log_info(f"Available items: {', '.join(ITEMS[:5])}{'...' if len(ITEMS) > 5 else ''}")
            log_info("Use 'python manager.py list' to see all available items")
            return []

        return [item_filter]

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
