"""Greet command - Example of simple interactive menu"""

from argparse import ArgumentParser, Namespace
from typing import Optional

from manager_core.commands.base import BaseCommand
from manager_core.core.emojis import Emoji
from manager_core.core.logger import log_info, log_success
from manager_core.core.menu import MenuNode


class GreetCommand(BaseCommand):
    """Greet the user in different languages"""

    name = "greet"
    help = "Greet the user"
    description = "Simple greeting command with language selection"

    def add_arguments(self, parser: ArgumentParser):
        """Add command arguments"""
        parser.add_argument(
            "-l",
            "--language",
            choices=["en", "es", "fr", "de"],
            help="Language for greeting",
        )
        parser.add_argument("-n", "--name", default="World", help="Name to greet")

    def execute(self, args: Namespace) -> bool:
        """Execute greeting"""
        greetings = {
            "en": "Hello",
            "es": "Hola",
            "fr": "Bonjour",
            "de": "Guten Tag",
        }

        lang = args.language or "en"
        name = args.name

        greeting = f"{greetings[lang]}, {name}!"
        log_success(greeting)
        return True

    def get_menu_tree(self) -> Optional[MenuNode]:
        """Interactive menu for greet command"""
        return MenuNode(
            label="Greet",
            emoji=Emoji.GREET,
            children=[
                MenuNode(
                    label="English",
                    emoji=Emoji.FLAG_GB,
                    action=lambda: self._greet("en"),
                ),
                MenuNode(
                    label="Spanish",
                    emoji=Emoji.FLAG_ES,
                    action=lambda: self._greet("es"),
                ),
                MenuNode(
                    label="French",
                    emoji=Emoji.FLAG_FR,
                    action=lambda: self._greet("fr"),
                ),
                MenuNode(
                    label="German",
                    emoji=Emoji.FLAG_DE,
                    action=lambda: self._greet("de"),
                ),
            ],
        )

    def _greet(self, language: str) -> bool:
        """Internal greeting method"""
        greetings = {
            "en": "Hello, World!",
            "es": "¡Hola, Mundo!",
            "fr": "Bonjour, le monde!",
            "de": "Guten Tag, Welt!",
        }
        log_success(greetings[language])
        return True
