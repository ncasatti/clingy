"""Info command - Display system and project information"""

import platform
import sys
from argparse import ArgumentParser, Namespace

from clingy.commands.base import BaseCommand
from clingy.config import PROJECT_NAME, PROJECT_VERSION
from clingy.core.emojis import Emoji
from clingy.core.logger import log_info, log_section
from clingy.core.menu import MenuNode


class InfoCommand(BaseCommand):
    """Display system and project information"""

    name = "info"
    help = "Display system information"
    description = "Show system and project information (CLI only)"

    def add_arguments(self, parser: ArgumentParser):
        """Add command arguments"""
        parser.add_argument("--verbose", action="store_true", help="Show verbose information")

    def execute(self, args: Namespace) -> bool:
        """Display system information"""
        log_section("PROJECT INFORMATION")
        log_info(f"Project: {PROJECT_NAME}")
        log_info(f"Version: {PROJECT_VERSION}")

        log_section("SYSTEM INFORMATION")
        log_info(f"OS: {platform.system()} {platform.release()}")
        log_info(f"Python: {sys.version.split()[0]}")
        log_info(f"Platform: {platform.platform()}")

        if getattr(args, "verbose", False):
            log_section("DETAILED INFORMATION")
            log_info(f"Machine: {platform.machine()}")
            log_info(f"Processor: {platform.processor()}")
            log_info(f"Architecture: {platform.architecture()[0]}")

        return True

    def get_menu_tree(self) -> MenuNode:
        """Interactive menu for info command"""
        return MenuNode(
            label="System Information",
            emoji=Emoji.CMD_INFO,
            action=lambda: self.execute(Namespace()),
        )
