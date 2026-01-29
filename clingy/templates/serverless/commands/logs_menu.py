"""Logs menu - View, Tail, and Insights for Lambda logs"""

from argparse import ArgumentParser, Namespace
from typing import Optional

from commands.core_commands.insights import InsightsCommand
from commands.core_commands.logs import LogsCommand
from config import GO_FUNCTIONS

from clingy.commands.base import BaseCommand
from clingy.core.emojis import Emoji
from clingy.core.logger import log_info, log_section
from clingy.core.menu import MenuNode, fzf_select_items


class LogsMenuCommand(BaseCommand):
    """View and analyze Lambda function logs"""

    name = "logs"
    help = "View Lambda logs"
    description = "View CloudWatch logs, tail live logs, and run Insights queries"

    def execute(self, args: Namespace) -> bool:
        """Execute logs command (not used in interactive mode)"""
        log_info("Use interactive menu to view logs")
        return True

    def add_arguments(self, parser: ArgumentParser):
        return super().add_arguments(parser)

    def get_menu_tree(self) -> Optional[MenuNode]:
        """Interactive menu for logs management"""
        return MenuNode(
            label="Logs & Monitoring",
            emoji=Emoji.SEARCH,
            children=[
                MenuNode(
                    label="View Recent Logs",
                    emoji=Emoji.LOG,
                    children=[
                        MenuNode(
                            label="Select Function",
                            action=lambda: self._view_logs_selected(),
                        ),
                    ],
                ),
                MenuNode(
                    label="Tail Live Logs",
                    emoji=Emoji.LOG_REALTIME,
                    children=[
                        MenuNode(
                            label="Select Function",
                            action=lambda: self._tail_logs_selected(),
                        ),
                    ],
                ),
                MenuNode(
                    label="CloudWatch Insights",
                    emoji=Emoji.STATS,
                    children=[
                        MenuNode(
                            label="Run Insights Query",
                            action=lambda: self._run_insights(),
                        ),
                    ],
                ),
            ],
        )

    # ========================================================================
    # View Logs Actions
    # ========================================================================

    def _view_logs_selected(self) -> bool:
        """View recent logs for selected function"""
        functions = fzf_select_items(
            items=GO_FUNCTIONS,
            prompt="Select function to view logs: ",
            include_all=False,
        )
        if not functions:
            log_info("No function selected")
            return False

        func = functions[0]  # Single selection
        log_section(f"VIEW LOGS - {func}")
        logs_cmd = LogsCommand()
        return logs_cmd.execute(Namespace(function=func, tail=False, filter=None))

    # ========================================================================
    # Tail Logs Actions
    # ========================================================================

    def _tail_logs_selected(self) -> bool:
        """Tail live logs for selected function"""
        functions = fzf_select_items(
            items=GO_FUNCTIONS,
            prompt="Select function to tail logs: ",
            include_all=False,
        )
        if not functions:
            log_info("No function selected")
            return False

        func = functions[0]  # Single selection
        log_section(f"TAIL LOGS - {func}")
        logs_cmd = LogsCommand()
        return logs_cmd.execute(Namespace(function=func, tail=True, filter=None))

    # ========================================================================
    # Insights Actions
    # ========================================================================

    def _run_insights(self) -> bool:
        """Run CloudWatch Insights query"""
        log_section("CLOUDWATCH INSIGHTS")
        insights_cmd = InsightsCommand()
        # Use interactive mode (no function specified)
        return insights_cmd.execute(Namespace(function=None, query=None))
