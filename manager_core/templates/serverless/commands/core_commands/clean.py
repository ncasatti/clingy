"""Clean build artifacts"""

import os
import shutil
from argparse import ArgumentParser, Namespace

from config import BIN_DIR

from manager_core.commands.base import BaseCommand
from manager_core.core.logger import log_error, log_header, log_info, log_success
from manager_core.core.menu import MenuNode


class CleanCommand(BaseCommand):
    """Remove all build artifacts"""

    name = "clean"
    help = "Clean build artifacts"
    description = "Remove all compiled binaries and build artifacts"
    epilog = """Examples:
  manager.py clean              # Clean all build artifacts
"""

    def add_arguments(self, parser: ArgumentParser):
        """No arguments needed for clean"""
        pass

    def execute(self, args: Namespace) -> bool:
        """Execute clean command"""
        log_header("CLEANING BUILD ARTIFACTS")

        if not os.path.exists(BIN_DIR):
            log_info("No artifacts to clean")
            return True

        try:
            shutil.rmtree(BIN_DIR)
            log_success(f"Directory {BIN_DIR} removed successfully")
            return True
        except Exception as e:
            log_error(f"Error removing {BIN_DIR}: {e}")
            return False

    def get_menu_tree(self) -> MenuNode:
        return super().get_menu_tree()
