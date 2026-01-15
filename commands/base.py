"""Base command interface that all commands must implement"""

from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Optional, List
from manager.config import GO_FUNCTIONS
from manager.core.logger import log_error, log_info
from manager.core.menu import MenuNode


class BaseCommand(ABC):
    """
    Abstract base class for all CLI commands

    Each command must implement:
    - name: Command name (e.g., "build", "deploy")
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

    def _resolve_function_list(self, args: Namespace) -> List[str]:
        """
        Resolve function list from args, supporting both dev mode and CLI mode.

        Priority:
        1. args.function_list (from dev command) - takes precedence
        2. args.function (from CLI) - filtered via _get_filtered_functions()

        Args:
            args: Parsed command-line arguments

        Returns:
            List of function names to process
        """
        # Dev mode: function_list is provided directly
        if hasattr(args, "function_list") and args.function_list:
            return args.function_list

        # CLI mode: filter based on function argument
        function_arg = getattr(args, "function", None)
        return self._get_filtered_functions(function_arg)

    def _get_filtered_functions(self, function_filter: Optional[str]) -> List[str]:
        """
        Get list of functions to process, filtered if necessary.

        Args:
            function_filter: Specific function name or None for all

        Returns:
            List of valid function names (empty list if function doesn't exist)
        """
        if function_filter is None:
            return GO_FUNCTIONS

        # Validate function exists
        if function_filter not in GO_FUNCTIONS:
            log_error(
                f"Function '{function_filter}' does not exist in the available functions list"
            )
            log_info(
                f"Available functions: {', '.join(GO_FUNCTIONS[:5])}{'...' if len(GO_FUNCTIONS) > 5 else ''}"
            )
            log_info("Use 'python manager.py list' to see all available functions")
            return []

        return [function_filter]

    def get_menu_tree(self) -> Optional[MenuNode]:
        """
        Retorna árbol de menús para modo interactivo.

        Si retorna None, el comando no tiene modo interactivo
        y solo funciona via CLI tradicional.

        Returns:
            MenuNode con estructura de menús o None
        """
        return None

    def supports_interactive(self) -> bool:
        """True si el comando soporta modo interactivo"""
        return self.get_menu_tree() is not None
