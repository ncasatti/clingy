"""Files command - Example of hierarchical menu with file operations"""

import os
from argparse import ArgumentParser, Namespace
from typing import Optional

from manager.commands.base import BaseCommand
from manager.core.logger import log_error, log_info, log_success
from manager.core.menu import MenuNode


class FilesCommand(BaseCommand):
    """File operations command"""

    name = "files"
    help = "File operations"
    description = "Perform file operations (list, create, delete)"

    def add_arguments(self, parser: ArgumentParser):
        """Add command arguments"""
        parser.add_argument(
            "operation",
            choices=["list", "create", "delete"],
            help="Operation to perform",
        )
        parser.add_argument("-p", "--path", default=".", help="Path to operate on")

    def execute(self, args: Namespace) -> bool:
        """Execute file operation"""
        if args.operation == "list":
            return self._list_files(args.path)
        elif args.operation == "create":
            return self._create_file(args.path)
        elif args.operation == "delete":
            return self._delete_file(args.path)
        return False

    def get_menu_tree(self) -> Optional[MenuNode]:
        """Interactive menu for file operations"""
        return MenuNode(
            label="File Operations",
            emoji="📁",
            children=[
                MenuNode(
                    label="List Files",
                    emoji="📋",
                    action=lambda: self._list_files("."),
                ),
                MenuNode(
                    label="Create File",
                    emoji="➕",
                    action=lambda: self._create_file_interactive(),
                ),
                MenuNode(
                    label="Delete File",
                    emoji="🗑️",
                    action=lambda: self._delete_file_interactive(),
                ),
            ],
        )

    def _list_files(self, path: str) -> bool:
        """List files in directory"""
        try:
            files = os.listdir(path)
            log_info(f"Files in {path}:")
            for f in files:
                log_info(f"  - {f}")
            log_success(f"Listed {len(files)} files")
            return True
        except Exception as e:
            log_error(f"Failed to list files: {e}")
            return False

    def _create_file(self, path: str) -> bool:
        """Create a new file"""
        try:
            with open(path, "w") as f:
                f.write("# Example file\n")
            log_success(f"Created file: {path}")
            return True
        except Exception as e:
            log_error(f"Failed to create file: {e}")
            return False

    def _delete_file(self, path: str) -> bool:
        """Delete a file"""
        try:
            os.remove(path)
            log_success(f"Deleted file: {path}")
            return True
        except Exception as e:
            log_error(f"Failed to delete file: {e}")
            return False

    def _create_file_interactive(self) -> bool:
        """Create file with user input"""
        filename = input("Enter filename: ")
        if not filename:
            log_error("No filename provided")
            return False
        return self._create_file(filename)

    def _delete_file_interactive(self) -> bool:
        """Delete file with user input"""
        filename = input("Enter filename to delete: ")
        if not filename:
            log_error("No filename provided")
            return False
        return self._delete_file(filename)
