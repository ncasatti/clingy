#!/usr/bin/env python3
"""
Main CLI entry point for the manager

This file orchestrates the command-line interface using the auto-discovery system.
"""

import argparse
import platform
import shutil
import sys

from manager_core.cli_builder import create_cli_context
from manager_core.config import DEPENDENCIES
from manager_core.core.colors import Colors
from manager_core.core.logger import log_error, log_header, log_info


def main():
    """Main CLI entry point"""
    # Create CLI context (detects project and discovers commands)
    ctx = create_cli_context()

    # Allow 'init' command to run even without a project
    is_init_command = len(sys.argv) > 1 and sys.argv[1] == "init"

    # If no project found and not running 'init', show error
    if not ctx.has_project and not is_init_command:
        log_error("No manager project found.")
        log_info("Run 'manager init' to create a new project, or")
        log_info("navigate to a directory with commands/ and config.py")
        sys.exit(1)

    # Allow 'requirements' command to run even if dependencies are missing
    # (it's designed to diagnose dependency issues)
    is_requirements_command = len(sys.argv) > 1 and sys.argv[1] == "requirements"

    if not is_requirements_command:
        # Check required dependencies first
        if not check_required_dependencies():
            sys.exit(1)

    # If no arguments provided, enter interactive mode
    if len(sys.argv) == 1:
        return interactive_mode(ctx)

    # Traditional CLI mode
    return cli_mode(ctx)


def check_required_dependencies() -> bool:
    """
    Check if all required dependencies are installed.

    Returns:
        True if all required dependencies are available, False otherwise.
    """
    # Filter only required dependencies
    required_deps = [dep for dep in DEPENDENCIES if dep.required]

    if not required_deps:
        return True

    # Check which dependencies are missing
    missing = []
    for dep in required_deps:
        if shutil.which(dep.command) is None:
            missing.append(dep)

    # If all dependencies are present, return silently
    if not missing:
        return True

    # Show error message with missing dependencies
    missing_names = ", ".join([dep.name for dep in missing])
    log_error(f"Missing required dependencies: {missing_names}")

    # Show installation commands
    log_info("Install with:")
    system = platform.system()
    for dep in missing:
        if system == "Darwin" and dep.install_macos:
            log_info(f"  - {dep.name}: {dep.install_macos}")
        elif system == "Linux" and dep.install_linux:
            log_info(f"  - {dep.name}: {dep.install_linux}")
        elif dep.install_other:
            log_info(f"  - {dep.name}: {dep.install_other}")

    log_info("Run 'python manager.py requirements' for details")
    return False


def cli_mode(ctx):
    """Traditional CLI mode"""
    # Use commands from context
    commands = ctx.commands

    if not commands:
        log_error("No commands found. Please create command files in commands/")
        sys.exit(1)

    # Create main parser
    parser = argparse.ArgumentParser(
        description="  CLI Manager Template - Modular command-line tool with interactive menus",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Global options
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Register all discovered commands
    command_instances = {}
    for cmd_name, cmd_class in commands.items():
        # Create command instance
        cmd_instance = cmd_class()
        command_instances[cmd_name] = cmd_instance

        # Create subparser for this command
        cmd_parser = subparsers.add_parser(
            cmd_name,
            help=cmd_instance.help,
            description=cmd_instance.get_description(),
            epilog=cmd_instance.get_epilog(),
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Let command add its own arguments
        cmd_instance.add_arguments(cmd_parser)

    # Parse arguments
    args = parser.parse_args()

    # Disable colors if requested
    if args.no_color:
        Colors.disable()

    # Execute the selected command
    try:
        cmd_instance = command_instances[args.command]
        success = cmd_instance.execute(args)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
        sys.exit(130)
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        if "--debug" in sys.argv:
            raise
        sys.exit(1)


def interactive_mode(ctx):
    """Global interactive mode"""
    from manager_core.core.emojis import Emoji
    from manager_core.core.menu import MenuNode, MenuRenderer

    log_header("CLI MANAGER - INTERACTIVE MODE")

    # Use commands from context
    commands = ctx.commands

    # Build main menu
    menu_items = []
    for cmd_name, cmd_class in sorted(commands.items()):
        cmd_instance = cmd_class()
        node = cmd_instance.get_menu_tree()
        if node is not None:
            menu_items.append(node)

    # Add Exit option at the end
    menu_items.append(
        MenuNode(
            label="Exit",
            emoji=Emoji.EXIT,
            action=lambda: False,  # Return False to exit
        )
    )

    root = MenuNode(label="Main Menu", emoji="", children=menu_items)

    renderer = MenuRenderer(root, header="Select a command")

    try:
        renderer.show()
        return 0
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
        sys.exit(130)


if __name__ == "__main__":
    main()
