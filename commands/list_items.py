"""List all available items"""

from argparse import ArgumentParser, Namespace

from manager.commands.base import BaseCommand
from manager.config import ITEMS
from manager.core.logger import log_header, log_info
from manager.core.colors import Colors


class ListCommand(BaseCommand):
    """List all available items"""

    name = "list"
    help = "List all available items"
    description = "Display all configured items"
    epilog = """Examples:
  manager.py list                  # List all items
"""

    def add_arguments(self, parser: ArgumentParser):
        """No additional arguments needed for list command"""
        pass

    def execute(self, args: Namespace) -> bool:
        """Execute the list command"""
        log_header("AVAILABLE ITEMS")

        print(f"{Colors.BOLD}{Colors.BLUE}📋 Items ({len(ITEMS)}):{Colors.RESET}")
        for i, item in enumerate(ITEMS, 1):
            print(f"  {i:2}. {item}")

        print(f"\n{Colors.BOLD}Total: {len(ITEMS)} items{Colors.RESET}")
        return True
