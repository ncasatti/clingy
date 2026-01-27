"""Interactive logs menu for Lambda functions"""

import subprocess
from argparse import ArgumentParser, Namespace
from typing import Optional

from manager_core.commands.base import BaseCommand
from manager_core.core.logger import (
    log_header,
    log_error,
    log_warning,
    log_info,
    log_success,
)
from manager_core.core.colors import Colors, Emojis
from config import GO_FUNCTIONS, AWS_PROFILE, SERVICE_NAME, SERVERLESS_STAGE


class LogsCommand(BaseCommand):
    """Interactive logs menu for Lambda functions"""

    name = "logs"
    help = "Interactive logs menu"
    description = (
        "View CloudWatch logs for Lambda functions with multiple viewing options"
    )
    epilog = """Examples:
  manager.py logs           # Open interactive logs menu
"""

    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific arguments"""
        parser.add_argument(
            "-f",
            "--function",
            type=str,
            help="Specific function name to view logs (skips function selection menu)",
        )

    def execute(self, args: Namespace) -> bool:
        """Execute logs command"""
        # If function is pre-selected (from dev menu), go directly to logs submenu
        if hasattr(args, "function") and args.function:
            if args.function in GO_FUNCTIONS:
                return self._show_logs_submenu(args.function) or True
            else:
                log_error(
                    f"Function '{args.function}' not found in available functions"
                )
                return False

        # Otherwise, show interactive menu
        return self._logs_menu()

    def _get_log_group_name(self, func_name: str) -> str:
        """
        Build CloudWatch log group name for a Lambda function

        Args:
            func_name: Lambda function name

        Returns:
            Full log group name
        """
        return f"/aws/lambda/{SERVICE_NAME}-{SERVERLESS_STAGE}-{func_name}"

    def _save_logs_to_file(self, func_name: str, logs_output: str) -> None:
        """
        Save logs output to a file in the function's folder

        Args:
            func_name: Lambda function name
            logs_output: Log output to save
        """
        import os

        # Create function folder if it doesn't exist
        func_folder = os.path.join("functions", func_name)
        os.makedirs(func_folder, exist_ok=True)

        # Write logs to file
        log_file_path = os.path.join(func_folder, "function.log")
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(logs_output)

        # Get absolute path for display
        abs_path = os.path.abspath(log_file_path)
        print(f"\n{Colors.CYAN}💾 Logs saved to: {abs_path}{Colors.RESET}")

    def _execute_logs_command(
        self, func_name: str, option: str, query: str = None
    ) -> bool:
        """
        Execute AWS CLI command to get logs based on selected option

        Args:
            func_name: Lambda function name
            option: Log option selected (1-4)
            query: Custom query for filtering (only for option 4)

        Returns:
            True if command executed successfully
        """
        log_group = self._get_log_group_name(func_name)

        # Build base command
        command = ["aws", "logs", "tail", log_group, "--profile", AWS_PROFILE]

        # Add options based on selection
        if option == "1":
            # Logs (last 30 minutes)
            command.extend(["--format", "short", "--since", "30m"])
            log_info(f"Getting logs from the last 30 minutes for {func_name}")
        elif option == "2":
            # Logs (last 5 minutes)
            command.extend(["--format", "short", "--since", "5m"])
            log_info(f"Getting logs with short format for {func_name}")
        elif option == "3":
            # Logs with --follow
            command.extend(["--follow", "--since", "5m"])
            log_info(f"Following logs in real-time for {func_name} (Ctrl+C to stop)")
        elif option == "4":
            # Logs with custom query
            if query:
                command.extend(["--filter-pattern", query, "--since", "30m"])
                log_info(f"Filtering logs with pattern '{query}' for {func_name}")
            else:
                log_error("A query is required for this option")
                return False

        print(f"\n{Colors.CYAN}Executing: {' '.join(command)}{Colors.RESET}\n")
        print(f"{Colors.YELLOW}{'─' * 80}{Colors.RESET}\n")

        # Determine if we should capture output (don't capture for --follow mode)
        capture_output = option != "3"

        try:
            if capture_output:
                # Capture output for saving to file
                result = subprocess.run(
                    command, check=False, capture_output=True, text=True
                )

                # Display output
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr)

                print(f"\n{Colors.YELLOW}{'─' * 80}{Colors.RESET}")

                # Save to file
                combined_output = result.stdout if result.stdout else ""
                if result.stderr:
                    combined_output += "\n" + result.stderr

                if combined_output.strip():
                    self._save_logs_to_file(func_name, combined_output)

                if result.returncode == 0:
                    log_success("Command executed successfully")
                    return True
                else:
                    log_warning(f"Command finished with code {result.returncode}")
                    return True  # Return True anyway to continue menu
            else:
                # Stream output in real-time for --follow mode
                result = subprocess.run(command, check=False)

                print(f"\n{Colors.YELLOW}{'─' * 80}{Colors.RESET}")
                print(
                    f"{Colors.YELLOW}Note: --follow mode output not saved to file{Colors.RESET}"
                )

                if result.returncode == 0:
                    log_success("Command executed successfully")
                    return True
                else:
                    log_warning(f"Command finished with code {result.returncode}")
                    return True  # Return True anyway to continue menu

        except subprocess.CalledProcessError as e:
            log_error(f"Error executing command: {e}")
            return False
        except FileNotFoundError:
            log_error("AWS CLI is not installed or not found in PATH")
            log_info("Install with: pip install awscli or brew install awscli")
            return False
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Command interrupted by user{Colors.RESET}")
            return True

    def _select_log_option_with_fzf(self, func_name: str) -> Optional[str]:
        """
        Use fzf to select a log viewing option

        Args:
            func_name: Lambda function name

        Returns:
            Option number (1-4) or None if cancelled/back
        """
        # Build menu options
        options = []
        option_map = {}  # Map display text to option number

        options.append(f"{Emojis.DOCUMENT} Last 30 minutes")
        option_map[options[-1]] = "1"

        options.append(f"{Emojis.LIST} Last 5 minutes")
        option_map[options[-1]] = "2"

        options.append(f"{Emojis.CIRCULAR}  Real time")
        option_map[options[-1]] = "3"

        options.append(f"{Emojis.SEARCH} Filter logs with custom query")
        option_map[options[-1]] = "4"

        options.append(f"{Emojis.BACK}  Back to function selection")
        option_map[options[-1]] = "0"

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
                    "Select log option: ",
                    "--header",
                    f"Log options for: {func_name}",
                ],
                input=options_text,
                text=True,
                capture_output=True,
            )

            if result.returncode == 0:
                selected = result.stdout.strip()
                return option_map.get(selected)

            return None

        except FileNotFoundError:
            log_error("fzf is not installed")
            return None
        except KeyboardInterrupt:
            return None
        except Exception as e:
            log_error(f"Error using fzf: {e}")
            return None

    def _show_logs_submenu(self, func_name: str) -> bool:
        """
        Show log options submenu for a specific function using fzf

        Args:
            func_name: Selected Lambda function name

        Returns:
            True when exiting the submenu
        """
        while True:
            option = self._select_log_option_with_fzf(func_name)

            if option is None or option == "0":
                # User cancelled or selected back
                break

            # Handle the selected option
            if option in ["1", "2", "3"]:
                self._execute_logs_command(func_name, option)
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            elif option == "4":
                # Custom query - prompt for input
                query = input(
                    f"\n{Colors.BOLD}Enter filter/query (e.g., ERROR, WARN, etc.): {Colors.RESET}"
                ).strip()
                if query:
                    self._execute_logs_command(func_name, option, query)
                    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
                else:
                    log_warning("Empty query, operation cancelled")

        return True

    def _select_function_with_fzf(self) -> Optional[str]:
        """
        Use fzf to select a function interactively with fuzzy search

        Returns:
            Selected function name or None if cancelled
        """
        try:
            # Create function list for fzf
            functions_list = "\n".join(GO_FUNCTIONS)

            # Execute fzf with function list
            result = subprocess.run(
                [
                    "fzf",
                    "--height",
                    "50%",
                    "--reverse",
                    "--border",
                    "--prompt",
                    "🔍 Search function: ",
                    "--header",
                    f"Total: {len(GO_FUNCTIONS)} functions",
                ],
                input=functions_list,
                text=True,
                capture_output=True,
            )

            if result.returncode == 0:
                selected = result.stdout.strip()
                if selected in GO_FUNCTIONS:
                    return selected

            return None

        except FileNotFoundError:
            log_error("fzf is not installed on the system")
            return None
        except KeyboardInterrupt:
            return None
        except Exception as e:
            log_error(f"Error using fzf: {e}")
            return None

    def _logs_menu(self) -> bool:
        """
        Show logs menu with fzf function selection

        Returns:
            True if executed correctly
        """
        log_header("LOGS MENU - LAMBDA FUNCTIONS")

        while True:
            print(
                f"\n{Colors.BOLD}{Colors.CYAN}🔍 Use fzf to search and select a function{Colors.RESET}"
            )
            print(f"{Colors.CYAN}Press ESC or Ctrl+C to exit{Colors.RESET}\n")

            selected_func = self._select_function_with_fzf()

            if selected_func:
                self._show_logs_submenu(selected_func)
            else:
                log_info("Exiting logs menu")
                break

        return True
