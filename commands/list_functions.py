"""List all available functions"""

import os
from argparse import ArgumentParser, Namespace

from manager.commands.base import BaseCommand
from manager.config import GO_FUNCTIONS, FUNCTIONS_DIR
from manager.core.logger import log_header
from manager.core.colors import Colors


class ListCommand(BaseCommand):
    """List all available Lambda functions"""

    name = "list"
    help = "List all available functions"
    description = "Display all Lambda functions with their status"
    epilog = """Examples:
  manager.py list                  # List all functions
"""

    def add_arguments(self, parser: ArgumentParser):
        """No additional arguments needed for list command"""
        pass

    def execute(self, args: Namespace) -> bool:
        """Execute the list command"""
        log_header("AVAILABLE FUNCTIONS")

        # Separate original and migrated functions
        functions = GO_FUNCTIONS[:15]  # First 15 are original

        print(
            f"{Colors.BOLD}{Colors.BLUE}📋 Functions ({len(functions)}):{Colors.RESET}"
        )
        for i, func in enumerate(functions, 1):
            status = "✅" if self._function_exists(func) else "❌"
            print(f"  {i:2}. {status} {func}")

        print(f"\n{Colors.BOLD}Total: {len(GO_FUNCTIONS)} functions{Colors.RESET}")
        return True

    @staticmethod
    def _function_exists(func_name: str) -> bool:
        """Check if function's main.go exists"""
        main_go_path = os.path.join(FUNCTIONS_DIR, func_name, "main.go")
        return os.path.exists(main_go_path)
