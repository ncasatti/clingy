"""Interactive development menu for building, zipping and deploying functions"""

import subprocess
from argparse import ArgumentParser, Namespace
from typing import Optional, List

from manager.commands.base import BaseCommand
from manager.core.logger import (
    log_header,
    log_error,
    log_warning,
    log_info,
    log_success,
)
from manager.core.colors import Colors, Emojis
from manager.config import GO_FUNCTIONS

# Import existing commands to reuse their logic
from manager.commands.build import BuildCommand
from manager.commands.zip import ZipCommand
from manager.commands.deploy import DeployCommand
from manager.commands.logs import LogsCommand
from manager.commands.invoke import InvokeCommand
from manager.commands.insights import InsightsCommand


class DevCommand(BaseCommand):
    """Interactive development menu for functions"""

    name = "dev"
    help = "Interactive development menu"
    description = (
        "Build, zip, and deploy functions with interactive menu and fuzzy search"
    )
    epilog = """Examples:
  manager.py dev           # Open interactive development menu
"""

    def add_arguments(self, parser: ArgumentParser):
        """No arguments needed - interactive menu"""
        pass

    def execute(self, args: Namespace) -> bool:
        """Execute dev command"""
        return self._dev_menu()

    def _execute_action(self, functions: List[str], action: str) -> bool:
        """
        Execute the selected action on the given functions.
        Now delegates iteration to individual commands instead of iterating here.

        Args:
            functions: List of function names to process
            action: Action to perform (1=build, 2=zip, 3=deploy, 4=logs, 5=invoke, 6=all)

        Returns:
            True if action executed successfully
        """
        try:
            if action == "1":
                # Build - pass function list to command
                log_info(f"Building {len(functions)} function(s)...")
                build_cmd = BuildCommand()
                args = Namespace(function=None, function_list=functions)
                success = build_cmd.execute(args)

            elif action == "2":
                # Zip - pass function list to command
                log_info(f"Zipping {len(functions)} function(s)...")
                zip_cmd = ZipCommand()
                args = Namespace(function=None, function_list=functions)
                success = zip_cmd.execute(args)

            elif action == "3":
                # Deploy - pass function list to command
                # Deploy command now handles smart strategy internally
                log_info(f"Deploying {len(functions)} function(s)...")
                deploy_cmd = DeployCommand()
                args = Namespace(
                    debug=False, all=False, function=None, function_list=functions
                )
                success = deploy_cmd.execute(args)

            elif action == "4":
                # Logs (only available for single function)
                if len(functions) != 1:
                    log_error(
                        "Logs option is only available for single function selection"
                    )
                    return False

                log_info(f"Opening logs for function '{functions[0]}'...")
                logs_cmd = LogsCommand()
                # Call logs command with function pre-selected
                args = Namespace(function=functions[0])
                success = logs_cmd.execute(args)

            elif action == "5":
                # Invoke (only available for single function)
                if len(functions) != 1:
                    log_error(
                        "Invoke option is only available for single function selection"
                    )
                    return False

                log_info(f"Opening invoke menu for function '{functions[0]}'...")
                invoke_cmd = InvokeCommand()
                # Call invoke command with function pre-selected
                args = Namespace(
                    function=functions[0], payload=None, local=False, remote=False
                )
                success = invoke_cmd.execute(args)

            elif action == "7":
                # Insights (only available for single function)
                if len(functions) != 1:
                    log_error(
                        "Insights option is only available for single function selection"
                    )
                    return False

                log_info(f"Opening insights menu for function '{functions[0]}'...")
                insights_cmd = InsightsCommand()
                # Call insights command with function pre-selected
                args = Namespace(function=functions[0])
                success = insights_cmd.execute(args)

            elif action == "6":
                # Build + Zip + Deploy - pass function list to all commands
                log_info(
                    f"Building, zipping, and deploying {len(functions)} function(s)..."
                )

                # Step 1: Build
                build_cmd = BuildCommand()
                args = Namespace(function=None, function_list=functions)
                if not build_cmd.execute(args):
                    log_error("Build failed. Stopping pipeline.")
                    return False
                print()

                # Step 2: Zip
                zip_cmd = ZipCommand()
                args = Namespace(function=None, function_list=functions)
                if not zip_cmd.execute(args):
                    log_error("Zip failed. Stopping pipeline.")
                    return False
                print()

                # Step 3: Deploy
                deploy_cmd = DeployCommand()
                args = Namespace(
                    debug=False, all=False, function=None, function_list=functions
                )
                if not deploy_cmd.execute(args):
                    log_error("Deployment failed.")
                    return False

                success = True

            else:
                log_error(f"Unknown action: {action}")
                return False

            if success:
                log_success("Operation completed successfully!")
            else:
                log_warning("Operation failed, but continuing...")

            return True  # Always return True to continue menu

        except Exception as e:
            log_error(f"Error executing action: {e}")
            return False

    def _select_action_with_fzf(self, functions: List[str]) -> Optional[str]:
        """
        Use fzf to select an action for the selected functions

        Args:
            functions: Selected function names

        Returns:
            Action number (1-6) or None if cancelled/back
        """
        is_single_function = len(functions) == 1
        func_display = (
            ", ".join(functions)
            if len(functions) <= 3
            else f"{len(functions)} functions"
        )

        # Build menu options
        options = []
        action_map = {}  # Map display text to action number

        options.append(f"{Emojis.BUILD}  Build only")
        action_map[options[-1]] = "1"

        options.append(f"{Emojis.PACKAGE} Zip only")
        action_map[options[-1]] = "2"

        options.append(f"{Emojis.ROCKET}  Deploy only")
        action_map[options[-1]] = "3"

        if is_single_function:
            options.append(f"{Emojis.DOCUMENT} View Logs")
            action_map[options[-1]] = "4"

            options.append(f"{Emojis.RUN}  Invoke Function")
            action_map[options[-1]] = "5"

            options.append(f"{Emojis.SEARCH} Insights Query")
            action_map[options[-1]] = "7"

            options.append(f"{Emojis.STATS} All (Build → Zip → Deploy)")
            action_map[options[-1]] = "6"
        else:
            options.append(f"{Emojis.STATS} All (Build → Zip → Deploy)")
            action_map[options[-1]] = "6"

        options.append(f"{Emojis.BACK}  Back to function selection")
        action_map[options[-1]] = "0"

        # Create fzf input
        options_text = "\n".join(options)

        try:
            result = subprocess.run(
                [
                    "fzf",
                    "--height",
                    "40%",
                    "--reverse",
                    "--border",
                    "--prompt",
                    "Select action: ",
                    "--header",
                    f"Action menu for: {func_display}",
                ],
                input=options_text,
                text=True,
                capture_output=True,
            )

            if result.returncode == 0:
                selected = result.stdout.strip()
                return action_map.get(selected)

            return None

        except FileNotFoundError:
            log_error("fzf is not installed")
            return None
        except KeyboardInterrupt:
            return None
        except Exception as e:
            log_error(f"Error using fzf: {e}")
            return None

    def _show_action_menu(self, functions: List[str]) -> None:
        """
        Show action menu for selected functions using fzf

        Args:
            functions: Selected function names
        """
        while True:
            action = self._select_action_with_fzf(functions)

            if action is None or action == "0":
                # User cancelled or selected back
                break

            # Execute the selected action
            self._execute_action(functions, action)

    def _select_functions_with_fzf(self) -> Optional[List[str]]:
        """
        Use fzf to select functions interactively with fuzzy search and multi-select

        Returns:
            List of selected function names or None if cancelled
        """
        try:
            # Create function list for fzf (add "ALL FUNCTIONS" option at the top)
            functions_list = "[ALL FUNCTIONS]\n" + "\n".join(GO_FUNCTIONS)

            # Execute fzf with function list and multi-select enabled
            result = subprocess.run(
                [
                    "fzf",
                    "--multi",  # Enable multi-select with TAB
                    "--height",
                    "50%",
                    "--reverse",
                    "--border",
                    "--prompt",
                    "🔍 Search (TAB=select, ENTER=confirm): ",
                    "--header",
                    f"Total: {len(GO_FUNCTIONS)} functions | Multi-select: TAB | ALL: Select first option",
                ],
                input=functions_list,
                text=True,
                capture_output=True,
            )

            if result.returncode == 0:
                selected = result.stdout.strip().split("\n")
                # Filter out empty strings
                selected = [s for s in selected if s]

                if not selected:
                    return None

                # Check if "ALL FUNCTIONS" was selected
                if "[ALL FUNCTIONS]" in selected:
                    return GO_FUNCTIONS

                # Validate all selected functions
                valid_functions = [f for f in selected if f in GO_FUNCTIONS]
                if valid_functions:
                    return valid_functions

            return None

        except FileNotFoundError:
            log_error("fzf is not installed on the system")
            return None
        except KeyboardInterrupt:
            return None
        except Exception as e:
            log_error(f"Error using fzf: {e}")
            return None

    def _dev_menu(self) -> bool:
        """
        Show dev menu with fzf multi-select

        Returns:
            True if executed correctly
        """
        log_header("DEVELOPMENT MENU - INTERACTIVE BUILD, ZIP & DEPLOY")

        while True:
            print(
                f"\n{Colors.BOLD}{Colors.CYAN}🔍 Use fzf to search and select functions{Colors.RESET}"
            )
            print(
                f"{Colors.CYAN}TAB to select multiple | ENTER to confirm | ESC to exit{Colors.RESET}\n"
            )

            selected_funcs = self._select_functions_with_fzf()

            if selected_funcs:
                self._show_action_menu(selected_funcs)
            else:
                log_info("Exiting dev menu")
                break

        return True
