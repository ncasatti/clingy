"""Invoke menu - Local and Remote Lambda invocation with payload composer"""

from argparse import Namespace
from typing import Optional

from commands.core_commands.invoke import InvokeCommand
from config import GO_FUNCTIONS

from manager_core.commands.base import BaseCommand
from manager_core.core.emojis import Emojis
from manager_core.core.logger import log_info, log_section
from manager_core.core.menu import MenuNode, fzf_select_items


class InvokeMenuCommand(BaseCommand):
    """Invoke Lambda functions locally or remotely"""

    name = "invoke"
    help = "Invoke Lambda functions"
    description = "Invoke Lambda functions locally or remotely with composable payloads"

    def execute(self, args: Namespace) -> bool:
        """Execute invoke command (not used in interactive mode)"""
        log_info("Use interactive menu to invoke functions")
        return True

    def get_menu_tree(self) -> Optional[MenuNode]:
        """Interactive menu for function invocation"""
        return MenuNode(
            label="Invoke Functions",
            emoji=Emojis.PLAY,
            children=[
                MenuNode(
                    label="Local Invocation",
                    emoji=Emojis.COMPUTER,
                    children=[
                        MenuNode(
                            label="Select Function (Local)",
                            action=lambda: self._invoke_local_selected(),
                        ),
                    ],
                ),
                MenuNode(
                    label="Remote Invocation (AWS)",
                    emoji=Emojis.CLOUD,
                    children=[
                        MenuNode(
                            label="Select Function (Remote)",
                            action=lambda: self._invoke_remote_selected(),
                        ),
                    ],
                ),
                MenuNode(
                    label="Payload Navigator",
                    emoji=Emojis.DOCUMENT,
                    children=[
                        MenuNode(
                            label="Browse Payloads",
                            action=lambda: self._browse_payloads(),
                        ),
                    ],
                ),
            ],
        )

    # ========================================================================
    # Local Invocation Actions
    # ========================================================================

    def _invoke_local_selected(self) -> bool:
        """Invoke function locally"""
        functions = fzf_select_items(
            items=GO_FUNCTIONS,
            prompt="Select function to invoke locally: ",
            include_all=False,
        )
        if not functions:
            log_info("No function selected")
            return False

        func = functions[0]  # Single selection
        log_section(f"LOCAL INVOKE - {func}")
        invoke_cmd = InvokeCommand()
        return invoke_cmd.execute(
            Namespace(
                function=func,
                local=True,
                remote=False,
                payload=None,
                payload_file=None,
            )
        )

    # ========================================================================
    # Remote Invocation Actions
    # ========================================================================

    def _invoke_remote_selected(self) -> bool:
        """Invoke function remotely on AWS"""
        functions = fzf_select_items(
            items=GO_FUNCTIONS,
            prompt="Select function to invoke remotely: ",
            include_all=False,
        )
        if not functions:
            log_info("No function selected")
            return False

        func = functions[0]  # Single selection
        log_section(f"REMOTE INVOKE - {func}")
        invoke_cmd = InvokeCommand()
        return invoke_cmd.execute(
            Namespace(
                function=func,
                local=False,
                remote=True,
                payload=None,
                payload_file=None,
            )
        )

    # ========================================================================
    # Payload Navigator Actions
    # ========================================================================

    def _browse_payloads(self) -> bool:
        """Browse and compose payloads"""
        log_section("PAYLOAD NAVIGATOR")
        log_info("Payload navigator will be launched in interactive mode")

        # The InvokeCommand has built-in payload navigation
        # When no payload is specified, it will show the PayloadNavigator
        invoke_cmd = InvokeCommand()
        return invoke_cmd.execute(
            Namespace(
                function=None,  # Will prompt for function
                local=False,
                remote=False,
                payload=None,
                payload_file=None,
            )
        )
