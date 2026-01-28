"""Calculator command - Example of interactive input with fzf"""

from argparse import ArgumentParser, Namespace
from typing import Optional

from manager_core.commands.base import BaseCommand
from manager_core.core.emojis import Emoji
from manager_core.core.logger import log_error, log_success
from manager_core.core.menu import MenuNode, fzf_select


class CalculatorCommand(BaseCommand):
    """Simple calculator with interactive operation selection"""

    name = "calculator"
    help = "Simple calculator"
    description = "Perform basic arithmetic operations"

    def add_arguments(self, parser: ArgumentParser):
        """Add command arguments"""
        parser.add_argument("num1", type=float, nargs="?", help="First number")
        parser.add_argument("operation", nargs="?", choices=["+", "-", "*", "/"], help="Operation")
        parser.add_argument("num2", type=float, nargs="?", help="Second number")

    def execute(self, args: Namespace) -> bool:
        """Execute calculation"""
        if not all([args.num1, args.operation, args.num2]):
            log_error("Missing arguments. Usage: calculator <num1> <operation> <num2>")
            return False

        return self._calculate(args.num1, args.operation, args.num2)

    def get_menu_tree(self) -> Optional[MenuNode]:
        """Interactive menu for calculator"""
        return MenuNode(
            label="Calculator",
            emoji=Emoji.CALCULATOR,
            children=[
                MenuNode(
                    label="Add",
                    emoji=Emoji.ADD,
                    action=lambda: self._calculate_interactive("+"),
                ),
                MenuNode(
                    label="Subtract",
                    emoji=Emoji.SUBTRACT,
                    action=lambda: self._calculate_interactive("-"),
                ),
                MenuNode(
                    label="Multiply",
                    emoji=Emoji.MULTIPLY,
                    action=lambda: self._calculate_interactive("*"),
                ),
                MenuNode(
                    label="Divide",
                    emoji=Emoji.DIVIDE,
                    action=lambda: self._calculate_interactive("/"),
                ),
            ],
        )

    def _calculate(self, num1: float, operation: str, num2: float) -> bool:
        """Perform calculation"""
        try:
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    log_error("Division by zero")
                    return False
                result = num1 / num2
            else:
                log_error(f"Invalid operation: {operation}")
                return False

            log_success(f"{num1} {operation} {num2} = {result}")
            return True
        except Exception as e:
            log_error(f"Calculation failed: {e}")
            return False

    def _calculate_interactive(self, operation: str) -> bool:
        """Calculate with user input"""
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            return self._calculate(num1, operation, num2)
        except ValueError:
            log_error("Invalid number input")
            return False
