"""Remove stack from AWS"""

import subprocess
import time
from argparse import ArgumentParser, Namespace

from manager.commands.base import BaseCommand
from manager.core.logger import (
    log_header,
    log_section,
    log_success,
    log_error,
    log_warning,
    log_info,
)
from manager.config import SERVERLESS_STAGE, SERVERLESS_PROFILE


class RemoveCommand(BaseCommand):
    """Remove serverless stack from AWS"""

    name = "remove"
    help = "Remove stack from AWS"
    description = "Remove the serverless stack from AWS using Serverless Framework"
    epilog = """Examples:
  manager.py remove         # Remove stack from AWS
  manager.py remove --debug # Remove with debug output
"""

    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific arguments"""
        parser.add_argument(
            "--debug", action="store_true", help="Enable debug mode for removal"
        )

    def execute(self, args: Namespace) -> bool:
        """Execute remove command"""
        log_header("REMOVING STACK FROM AWS")
        log_section(
            f"REMOVING STACK FROM AWS (stage: {SERVERLESS_STAGE}, profile: {SERVERLESS_PROFILE})"
        )

        # Warning about permanent deletion
        log_warning("This action will permanently delete the stack from AWS")

        # Build serverless command
        command = [
            "serverless",
            "remove",
            "--stage",
            SERVERLESS_STAGE,
            "--aws-profile",
            SERVERLESS_PROFILE,
        ]

        if args.debug:
            command.append("--debug")
            log_info("Debug mode enabled for removal")

        log_info(f"Executing: {' '.join(command)}")
        start_time = time.time()

        try:
            result = subprocess.run(
                command, check=True, capture_output=False, text=True
            )

            duration = time.time() - start_time

            if result.returncode == 0:
                log_success("Stack removed successfully from AWS", duration)
                return True
            else:
                log_error(f"Removal failed with code {result.returncode}", duration)
                return False

        except subprocess.CalledProcessError as e:
            duration = time.time() - start_time
            log_error("Error during removal", duration)
            return False

        except FileNotFoundError:
            log_error("Serverless Framework is not installed or not found in PATH")
            log_info("Install with: npm install -g serverless")
            return False
