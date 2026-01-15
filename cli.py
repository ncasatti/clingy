#!/usr/bin/env python3
"""
Main CLI entry point for the manager

This file orchestrates the command-line interface using the auto-discovery system.
"""

import argparse
import sys
from argparse import Namespace
from manager.commands import discover_commands
from manager.core.colors import Colors
from manager.core.logger import log_error, log_header


def main():
    """Main CLI entry point"""
    # Si no hay argumentos, modo interactivo
    if len(sys.argv) == 1:
        return interactive_mode()

    # Modo CLI tradicional
    return cli_mode()


def cli_mode():
    """Modo CLI tradicional"""
    # Discover all available commands
    commands = discover_commands()

    if not commands:
        log_error("No commands found. Please create command files in manager/commands/")
        sys.exit(1)

    # Create main parser
    parser = argparse.ArgumentParser(
        description="🚀 CLI Manager Template - Modular command-line tool with interactive menus",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Global options
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands", required=True
    )

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


def interactive_mode():
    """Modo interactivo global"""
    from manager.core.menu import MenuNode, MenuRenderer

    log_header("CLI MANAGER - INTERACTIVE MODE")

    # Discover commands
    commands = discover_commands()

    # Construir menú principal
    menu_items = []
    for cmd_name, cmd_class in sorted(commands.items()):
        cmd_instance = cmd_class()

        # Si el comando tiene menú interactivo, usarlo
        if cmd_instance.supports_interactive():
            node = cmd_instance.get_menu_tree()
            if node:
                menu_items.append(node)
        else:
            # Si no, crear nodo simple que ejecuta el comando
            menu_items.append(
                MenuNode(
                    label=f"{cmd_instance.help}",
                    emoji=_get_command_emoji(cmd_name),
                    action=lambda c=cmd_instance: c.execute(Namespace()),
                )
            )

    root = MenuNode(label="Main Menu", emoji="🚀", children=menu_items)

    renderer = MenuRenderer(root, header="Select a command")
    renderer.show()
    return 0


def _get_command_emoji(cmd_name: str) -> str:
    """Mapea nombres de comando a emojis"""
    emoji_map = {
        "build": "🔨",
        "deploy": "🚀",
        "zip": "📦",
        "logs": "📋",
        "list": "📝",
        "clean": "🧹",
        "dev": "💻",
        "invoke": "▶️",
        "insights": "🔍",
        "requirements": "📌",
        "remove": "🗑️",
    }
    return emoji_map.get(cmd_name, "⚙️")


if __name__ == "__main__":
    main()
