"""Clean output directory"""

import shutil
import os
from argparse import ArgumentParser, Namespace

from manager.commands.base import BaseCommand
from manager.core.logger import log_header, log_success, log_error, log_info
from manager.config import OUTPUT_DIR


class CleanCommand(BaseCommand):
    """Remove all output artifacts"""

    name = "clean"
    help = "Clean output directory"
    description = "Remove all generated files and artifacts"
    epilog = """Examples:
  manager.py clean              # Clean all output artifacts
"""

    def add_arguments(self, parser: ArgumentParser):
        """No arguments needed for clean"""
        pass

    def execute(self, args: Namespace) -> bool:
        """Execute clean command"""
        log_header("CLEANING OUTPUT DIRECTORY")

        if not os.path.exists(OUTPUT_DIR):
            log_info("No artifacts to clean")
            return True

        try:
            shutil.rmtree(OUTPUT_DIR)
            log_success(f"Directory {OUTPUT_DIR} removed successfully")
            return True
        except Exception as e:
            log_error(f"Error removing {OUTPUT_DIR}: {e}")
            return False
