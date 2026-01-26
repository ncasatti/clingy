"""
Init command - Initialize a new manager project
"""

import shutil
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional

from manager_core.commands.base import BaseCommand
from manager_core.core.emojis import Emojis
from manager_core.core.logger import log_error, log_info, log_success, log_section
from manager_core.core.menu import MenuNode


class InitCommand(BaseCommand):
    """Initialize a new manager project"""

    name = "init"
    help = "Initialize a new manager project in the current directory"
    description = "Creates a new manager project with commands/ directory and config.py"
    epilog = """Examples:
  manager init                    # Initialize in current directory
  manager init --force            # Overwrite existing project
"""

    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific arguments"""
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing project files",
        )
        parser.add_argument(
            "--template",
            default="basic",
            help="Template to use (default: basic)",
        )

    def execute(self, args: Namespace) -> bool:
        """
        Execute the init command

        Returns:
            True on success, False on failure
        """
        log_section("INITIALIZING MANAGER PROJECT")

        current_dir = Path.cwd()

        # Check if project already exists
        commands_dir = current_dir / "commands"
        config_file = current_dir / "config.py"

        if (commands_dir.exists() or config_file.exists()) and not args.force:
            log_error("Project already exists in this directory")
            log_info("Use --force to overwrite existing files")
            return False

        # Get template directory
        template_dir = self._get_template_dir(args.template)
        if template_dir is None:
            log_error(f"Template '{args.template}' not found")
            return False

        # Copy template files
        try:
            log_info(f"Using template: {args.template}")

            # Create commands directory
            if commands_dir.exists() and args.force:
                shutil.rmtree(commands_dir)
            commands_dir.mkdir(exist_ok=True)

            # Copy template files
            template_commands = template_dir / "commands"
            if template_commands.exists():
                for file in template_commands.glob("*.py"):
                    dest = commands_dir / file.name
                    shutil.copy2(file, dest)
                    log_success(f"Created {dest.relative_to(current_dir)}")

            # Copy config.py
            template_config = template_dir / "config.py"
            if template_config.exists():
                if config_file.exists() and args.force:
                    config_file.unlink()
                shutil.copy2(template_config, config_file)
                log_success(f"Created {config_file.relative_to(current_dir)}")

            log_success("Project initialized successfully!")
            log_info("")
            log_info("Next steps:")
            log_info("  1. Edit config.py to customize your project")
            log_info("  2. Add custom commands in commands/")
            log_info("  3. Run 'manager' to start the interactive menu")

            return True

        except Exception as e:
            log_error(f"Failed to initialize project: {e}")
            return False

    def _get_template_dir(self, template_name: str) -> Optional[Path]:
        """
        Get the template directory path

        Args:
            template_name: Name of the template

        Returns:
            Path to template directory, or None if not found
        """
        # Templates are stored in manager_core/templates/
        package_dir = Path(__file__).parent.parent
        template_dir = package_dir / "templates" / template_name

        if template_dir.exists() and template_dir.is_dir():
            return template_dir

        return None

    def get_menu_tree(self) -> Optional[MenuNode]:
        """
        Init command is not available in interactive mode
        (it only makes sense to run from CLI)
        """
        return None
