"""Interactive invoke menu for Lambda functions"""

import subprocess
import os
import glob
import json
import time
from argparse import ArgumentParser, Namespace
from typing import Optional, List, Dict

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from manager_core.commands.base import BaseCommand
from manager_core.core.logger import (
    log_header,
    log_error,
    log_warning,
    log_info,
    log_success,
)
from manager_core.core.colors import Colors, Emojis
from config import (
    GO_FUNCTIONS,
    AWS_PROFILE,
    SERVICE_NAME,
    SERVERLESS_STAGE,
    FUNCTIONS_DIR,
    INVOKE_REMOTE_METHOD,
    INVOKE_AWS_REGION,
    PAYLOADS_DIR,
    PAYLOAD_DEFAULT_STAGE,
    PAYLOAD_SHOW_MERGE_SOURCES,
)
from core.payload_composer import PayloadComposer, ComposedPayload, PayloadError
from core.payload_navigator import PayloadNavigator


class InvokeCommand(BaseCommand):
    """Interactive invoke menu for Lambda functions"""

    name = "invoke"
    help = "Invoke Lambda functions locally or remotely"
    description = (
        "Test Lambda functions with optional payloads from function-specific payload directories"
    )
    epilog = """Examples:
  manager.py invoke                    # Open interactive invoke menu
  manager.py invoke -f status          # Invoke specific function (opens submenu)
  manager.py invoke -f status -p test.json  # Invoke with specific payload
  manager.py invoke -f status --local  # Invoke function locally
"""

    def _format_lambda_response(self, response_text: str, func_name: str) -> None:
        """
        Parse and pretty-print Lambda response with color formatting
        Also saves the formatted response to output.yaml in function folder

        Args:
            response_text: Raw response text from Lambda
            func_name: Lambda function name (for saving to function-specific folder)
        """
        try:
            # Parse the Lambda response
            response = json.loads(response_text)

            # Prepare structured data for YAML export
            yaml_data = {}

            print(f"\n{Colors.BOLD}{Colors.GREEN}📋 Lambda Response:{Colors.RESET}\n")

            # Print status code
            if "statusCode" in response:
                status_code = response["statusCode"]
                color = Colors.GREEN if 200 <= status_code < 300 else Colors.RED
                print(f"{Colors.BOLD}Status Code:{Colors.RESET} {color}{status_code}{Colors.RESET}")
                yaml_data["statusCode"] = status_code

            # Print headers if present
            if "headers" in response and response["headers"]:
                print(f"\n{Colors.BOLD}Headers:{Colors.RESET}")
                for key, value in response["headers"].items():
                    print(f"  {Colors.CYAN}{key}:{Colors.RESET} {value}")
                yaml_data["headers"] = response["headers"]

            # Parse and print body
            if "body" in response:
                print(f"\n{Colors.BOLD}Body:{Colors.RESET}")
                try:
                    # Try to parse body as JSON
                    body_data = json.loads(response["body"])
                    print(json.dumps(body_data, indent=2, ensure_ascii=False))
                    yaml_data["body"] = body_data  # Save parsed body
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, print as-is
                    print(response["body"])
                    yaml_data["body"] = response["body"]  # Save raw body

            # Print other fields if present
            other_fields = {
                k: v
                for k, v in response.items()
                if k not in ["statusCode", "headers", "body", "multiValueHeaders"]
            }
            if other_fields:
                print(f"\n{Colors.BOLD}Other Fields:{Colors.RESET}")
                print(json.dumps(other_fields, indent=2, ensure_ascii=False))
                yaml_data.update(other_fields)

            # Save to YAML file
            self._save_response_to_yaml(yaml_data, func_name)

        except json.JSONDecodeError:
            # If response is not valid JSON, print as-is
            print(f"\n{Colors.YELLOW}Raw Response:{Colors.RESET}")
            print(response_text)
        except Exception as e:
            log_warning(f"Could not format response: {e}")
            print(f"\n{Colors.YELLOW}Raw Response:{Colors.RESET}")
            print(response_text)

    def _save_response_to_yaml(self, data: dict, func_name: str) -> None:
        """
        Save Lambda response to output.yaml file in function folder

        Args:
            data: Parsed Lambda response data
            func_name: Lambda function name
        """
        if not YAML_AVAILABLE:
            log_warning("PyYAML not installed. Install with: pip install pyyaml")
            return

        try:
            # Create function folder if it doesn't exist
            func_folder = os.path.join("functions", func_name)
            os.makedirs(func_folder, exist_ok=True)

            # Save to function-specific output.yaml
            output_file = os.path.join(func_folder, "output.yaml")

            with open(output_file, "w") as f:
                yaml.dump(
                    data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )

            # Get absolute path for display
            abs_path = os.path.abspath(output_file)
            print(f"\n{Colors.CYAN}💾 Response saved to: {Colors.BOLD}{abs_path}{Colors.RESET}")

        except Exception as e:
            log_warning(f"Could not save YAML file: {e}")

    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific arguments"""
        parser.add_argument(
            "-f",
            "--function",
            type=str,
            help="Specific function name to invoke (skips function selection menu)",
        )
        parser.add_argument("-p", "--payload", type=str, help="Path to JSON payload file")
        parser.add_argument(
            "--local", action="store_true", help="Invoke locally (default is remote)"
        )
        parser.add_argument("--remote", action="store_true", help="Invoke remotely (explicit flag)")

    def execute(self, args: Namespace) -> bool:
        """Execute invoke command"""
        # If function and payload are specified, invoke directly
        if hasattr(args, "function") and args.function:
            if args.function not in GO_FUNCTIONS:
                log_error(f"Function '{args.function}' not found in available functions")
                return False

            # Determine if local or remote
            is_local = getattr(args, "local", False)
            payload_path = getattr(args, "payload", None)

            if payload_path:
                # Direct invocation with payload
                return self._invoke_function(args.function, payload_path, is_local)
            else:
                # Show submenu for function
                return self._show_invoke_submenu(args.function) or True

        # Otherwise, show interactive menu
        return self._invoke_menu()

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

    def _discover_legacy_payloads(self, func_name: str) -> List[tuple]:
        """
        Discover legacy JSON payload files from both shared and function-specific locations

        Args:
            func_name: Function name

        Returns:
            List of tuples: (payload_path, label) where label is "SHARED" or "LOCAL"
        """
        payloads = []

        # 1. Discover SHARED payloads from test-payloads/ (root level)
        shared_dir = "test-payloads"
        if os.path.isdir(shared_dir):
            pattern = os.path.join(shared_dir, "*.json")
            shared_payloads = sorted(glob.glob(pattern))
            for payload_path in shared_payloads:
                payloads.append((payload_path, "SHARED"))

        # 2. Discover LOCAL payloads from functions/{function}/payloads/
        local_dir = os.path.join(FUNCTIONS_DIR, func_name, "payloads")
        if os.path.isdir(local_dir):
            pattern = os.path.join(local_dir, "*.json")
            local_payloads = sorted(glob.glob(pattern))
            for payload_path in local_payloads:
                payloads.append((payload_path, "LOCAL"))

        return payloads

    def _discover_payloads(self, func_name: str) -> List[tuple]:
        """
        Discover all payload files (legacy + composable)

        Args:
            func_name: Function name

        Returns:
            List of tuples: (payload_path, label)
        """
        from pathlib import Path

        payloads = []

        # 1. Discover composable payloads using PayloadNavigator
        navigator = PayloadNavigator(Path(PAYLOADS_DIR))
        composable_entries = navigator.discover_all(func_name)

        for entry in composable_entries:
            # Convertir PayloadEntry a tupla (path_str, label)
            label = entry.label if entry.label else "COMPOSABLE"
            payloads.append((str(entry.path), label))

        return payloads

    def _select_payload_with_fzf(self, func_name: str) -> Optional[str]:
        """
        Use fzf to select a payload file interactively with hierarchical navigation

        Args:
            func_name: Function name

        Returns:
            Selected payload file path or None if cancelled
        """
        from pathlib import Path

        try:
            # Use PayloadNavigator for hierarchical navigation
            navigator = PayloadNavigator(Path(PAYLOADS_DIR))
            selected_path = navigator.navigate_with_fzf(func_name)

            if selected_path:
                return str(selected_path)

            return None

        except FileNotFoundError:
            log_error("fzf is not installed on the system")
            return None
        except KeyboardInterrupt:
            return None
        except Exception as e:
            log_error(f"Error using fzf: {e}")
            return None

    def _get_lambda_function_name(self, func_name: str) -> str:
        """
        Build full Lambda function name for AWS CLI

        Args:
            func_name: Short function name

        Returns:
            Full Lambda function name
        """
        return f"{SERVICE_NAME}-{SERVERLESS_STAGE}-{func_name}"

    def _is_legacy_payload(self, payload_path: str) -> bool:
        """
        Detect if payload is legacy (JSON in old locations) or composable (YAML in payloads/)

        Args:
            payload_path: Path to payload file

        Returns:
            True if legacy, False if composable
        """
        from pathlib import Path

        path = Path(payload_path)

        # Legacy: JSON en test-payloads/ o functions/*/payloads/
        if "test-payloads" in str(path) or "functions" in str(path):
            return True

        # Composable: Archivos en payloads/
        if str(path).startswith(PAYLOADS_DIR):
            return False

        # Default: legacy
        return True

    def _process_payload(self, payload_path: str) -> tuple:
        """
        Process payload file (legacy or composable)

        Args:
            payload_path: Path to original payload file

        Returns:
            Tuple: (processed_path, composed_payload_or_none)
            - processed_path: Path to processed file (temp if modified)
            - composed_payload_or_none: ComposedPayload if composable, None if legacy
        """
        from pathlib import Path

        try:
            is_legacy = self._is_legacy_payload(payload_path)

            if is_legacy:
                # LEGACY: Solo convertir body a string si es dict/list
                with open(payload_path, "r") as f:
                    payload_data = json.load(f)

                # Check if body exists and is dict or list
                if "body" in payload_data:
                    body = payload_data["body"]

                    # If body is dict or list, convert to JSON string
                    if isinstance(body, (dict, list)):
                        payload_data["body"] = json.dumps(
                            body, ensure_ascii=False, separators=(",", ":")
                        )

                        # Create temp file with processed payload
                        timestamp = int(time.time() * 1000)
                        temp_path = f"/tmp/manager-invoke-payload-{timestamp}.json"

                        with open(temp_path, "w") as f:
                            json.dump(payload_data, f, indent=2, ensure_ascii=False)

                        log_info(f"Body converted from {type(body).__name__} to JSON string")
                        return (temp_path, None)

                # No modification needed, return original
                return (payload_path, None)

            else:
                # COMPOSABLE: Usar PayloadComposer
                composer = PayloadComposer(Path(PAYLOADS_DIR))

                # Componer payload
                composed = composer.compose(Path(payload_path), PAYLOAD_DEFAULT_STAGE)

                # Mostrar fuentes del merge si está habilitado
                if PAYLOAD_SHOW_MERGE_SOURCES and composed.sources:
                    print(f"\n{Colors.CYAN}📦 Merged from:{Colors.RESET}")
                    for i, source in enumerate(composed.sources, 1):
                        print(f"  {i}. {source.relative_to(Path.cwd())}")

                # Validar payload final
                validation = composer.validate(composed.data)

                # Mostrar warnings de validación
                if validation.warnings:
                    print(f"\n{Colors.YELLOW}⚠️  Validation Warnings:{Colors.RESET}")
                    for warning in validation.warnings:
                        print(f"  - {warning}")

                # Mostrar errores de validación (CRÍTICO)
                if validation.errors:
                    print(f"\n{Colors.RED}❌ Validation Errors:{Colors.RESET}")
                    for error in validation.errors:
                        print(f"  - {error}")
                    raise PayloadError("Payload validation failed. Cannot invoke.")

                # Convertir body a string si es dict/list
                payload_data = composed.data.copy()
                if "body" in payload_data:
                    body = payload_data["body"]
                    if isinstance(body, (dict, list)):
                        payload_data["body"] = json.dumps(
                            body, ensure_ascii=False, separators=(",", ":")
                        )

                # Crear archivo temporal con payload compuesto
                timestamp = int(time.time() * 1000)
                temp_path = f"/tmp/manager-invoke-payload-{timestamp}.json"

                with open(temp_path, "w") as f:
                    json.dump(payload_data, f, indent=2, ensure_ascii=False)

                log_success("Payload composed successfully")
                return (temp_path, composed)

        except PayloadError as e:
            log_error(f"Payload composition failed: {e}")
            raise
        except Exception as e:
            log_warning(f"Could not process payload: {e}")
            return (payload_path, None)

    def _preview_payload(
        self, payload_data: Dict, composed: Optional[ComposedPayload] = None
    ) -> None:
        """
        Display payload preview with formatting

        Args:
            payload_data: Payload dictionary to preview
            composed: ComposedPayload if this is a composable payload (optional)
        """
        from pathlib import Path

        print(f"\n{Colors.BOLD}{Colors.CYAN}📄 Payload Preview:{Colors.RESET}")
        print(f"{Colors.YELLOW}{'─' * 60}{Colors.RESET}")

        # Si es composable, mostrar fuentes del merge
        if composed and composed.sources:
            print(f"{Colors.CYAN}Merged from:{Colors.RESET}")
            for i, source in enumerate(composed.sources, 1):
                print(f"  {Colors.GREEN}{i}.{Colors.RESET} {source.relative_to(Path.cwd())}")
            print(f"{Colors.YELLOW}{'─' * 60}{Colors.RESET}")

        # Mostrar warnings si hay
        if composed and composed.warnings:
            print(f"{Colors.YELLOW}⚠️  Warnings:{Colors.RESET}")
            for warning in composed.warnings:
                print(f"  {Colors.YELLOW}-{Colors.RESET} {warning}")
            print(f"{Colors.YELLOW}{'─' * 60}{Colors.RESET}")

        # Mostrar payload
        print(json.dumps(payload_data, indent=2, ensure_ascii=False))
        print(f"{Colors.YELLOW}{'─' * 60}{Colors.RESET}\n")

    def _invoke_function(
        self, func_name: str, payload_path: Optional[str] = None, local: bool = False
    ) -> bool:
        """
        Execute invoke command (local or remote)

        Args:
            func_name: Lambda function name
            payload_path: Path to JSON payload file (optional)
            local: True for local invocation, False for remote

        Returns:
            True if command executed successfully
        """
        if local:
            return self._invoke_local(func_name, payload_path)
        else:
            return self._invoke_remote(func_name, payload_path)

    def _invoke_local(self, func_name: str, payload_path: Optional[str] = None) -> bool:
        """
        Invoke function locally using Serverless Framework

        Args:
            func_name: Lambda function name
            payload_path: Path to JSON payload file (optional)

        Returns:
            True if command executed successfully
        """
        # Build serverless invoke local command
        command = [
            "serverless",
            "invoke",
            "local",
            "--function",
            func_name,
            "--stage",
            SERVERLESS_STAGE,
            "--aws-profile",
            AWS_PROFILE,
        ]

        if payload_path:
            if not os.path.isfile(payload_path):
                log_error(f"Payload file not found: {payload_path}")
                return False

            # Process payload (convert body if needed, compose if composable)
            processed_payload_path, composed = self._process_payload(payload_path)

            # Preview payload
            with open(processed_payload_path, "r") as f:
                payload_data = json.load(f)
            self._preview_payload(payload_data, composed)

            command.extend(["--path", processed_payload_path])
            log_info(f"Invoking {func_name} locally with payload: {payload_path}")
        else:
            log_info(f"Invoking {func_name} locally without payload")

        print(f"\n{Colors.CYAN}Executing: {' '.join(command)}{Colors.RESET}\n")
        print(f"{Colors.YELLOW}{'─' * 80}{Colors.RESET}\n")

        try:
            # Execute command and capture output
            result = subprocess.run(command, check=False, capture_output=True, text=True)

            # Show stderr (logs, debug info) if present
            if result.stderr:
                print(f"{Colors.YELLOW}Logs:{Colors.RESET}")
                print(result.stderr)

            # Parse and format the response
            if result.stdout:
                self._format_lambda_response(result.stdout.strip(), func_name)

            print(f"\n{Colors.YELLOW}{'─' * 80}{Colors.RESET}")

            if result.returncode == 0:
                log_success("Function invoked successfully")
                return True
            else:
                log_warning(f"Command finished with code {result.returncode}")
                return True  # Return True anyway to continue menu

        except FileNotFoundError:
            log_error("Serverless Framework is not installed or not found in PATH")
            log_info("Install with: npm install -g serverless")
            return False
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Command interrupted by user{Colors.RESET}")
            return True
        except Exception as e:
            log_error(f"Error executing command: {e}")
            return False

    def _invoke_remote(self, func_name: str, payload_path: Optional[str] = None) -> bool:
        """
        Invoke function remotely using configured method (serverless or aws-cli)

        Args:
            func_name: Lambda function name
            payload_path: Path to JSON payload file (optional)

        Returns:
            True if command executed successfully
        """
        if INVOKE_REMOTE_METHOD == "serverless":
            return self._invoke_remote_serverless(func_name, payload_path)
        elif INVOKE_REMOTE_METHOD == "aws-cli":
            return self._invoke_remote_aws_cli(func_name, payload_path)
        else:
            log_error(f"Unknown INVOKE_REMOTE_METHOD: {INVOKE_REMOTE_METHOD}")
            log_info("Valid options: 'serverless' or 'aws-cli'")
            return False

    def _invoke_remote_serverless(self, func_name: str, payload_path: Optional[str] = None) -> bool:
        """
        Invoke remote function using Serverless Framework

        Args:
            func_name: Lambda function name
            payload_path: Path to JSON payload file (optional)

        Returns:
            True if command executed successfully
        """
        # Build serverless invoke command (remote)
        command = [
            "serverless",
            "invoke",
            "--function",
            func_name,
            "--stage",
            SERVERLESS_STAGE,
            "--aws-profile",
            AWS_PROFILE,
        ]

        if payload_path:
            if not os.path.isfile(payload_path):
                log_error(f"Payload file not found: {payload_path}")
                return False

            # Process payload (convert body if needed, compose if composable)
            processed_payload_path, composed = self._process_payload(payload_path)

            # Preview payload
            with open(processed_payload_path, "r") as f:
                payload_data = json.load(f)
            self._preview_payload(payload_data, composed)

            command.extend(["--path", processed_payload_path])
            log_info(f"Invoking {func_name} remotely (serverless) with payload: {payload_path}")
        else:
            log_info(f"Invoking {func_name} remotely (serverless) without payload")

        print(f"\n{Colors.CYAN}Executing: {' '.join(command)}{Colors.RESET}\n")
        print(f"{Colors.YELLOW}{'─' * 80}{Colors.RESET}\n")

        try:
            # Execute command and capture output
            result = subprocess.run(command, check=False, capture_output=True, text=True)

            # Show stderr (logs, debug info) if present
            if result.stderr:
                print(f"{Colors.YELLOW}Logs:{Colors.RESET}")
                print(result.stderr)

            # Parse and format the response
            if result.stdout:
                self._format_lambda_response(result.stdout.strip(), func_name)

            print(f"\n{Colors.YELLOW}{'─' * 80}{Colors.RESET}")

            if result.returncode == 0:
                log_success("Function invoked successfully")
                return True
            else:
                log_warning(f"Command finished with code {result.returncode}")
                return True

        except FileNotFoundError:
            log_error("Serverless Framework is not installed or not found in PATH")
            log_info("Install with: npm install -g serverless")
            return False
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Command interrupted by user{Colors.RESET}")
            return True
        except Exception as e:
            log_error(f"Error executing command: {e}")
            return False

    def _invoke_remote_aws_cli(self, func_name: str, payload_path: Optional[str] = None) -> bool:
        """
        Invoke remote function using AWS CLI

        Args:
            func_name: Lambda function name
            payload_path: Path to JSON payload file (optional)

        Returns:
            True if command executed successfully
        """
        lambda_name = self._get_lambda_function_name(func_name)

        # Build AWS CLI invoke command
        command = [
            "aws",
            "lambda",
            "invoke",
            "--function-name",
            lambda_name,
            "--profile",
            AWS_PROFILE,
            "--region",
            INVOKE_AWS_REGION,
            "--log-type",
            "Tail",  # Include execution logs in response
            "/tmp/invoke-response.json",  # Output file
        ]

        if payload_path:
            if not os.path.isfile(payload_path):
                log_error(f"Payload file not found: {payload_path}")
                return False

            # Process payload (convert body if needed, compose if composable)
            processed_payload_path, composed = self._process_payload(payload_path)

            # Preview payload
            with open(processed_payload_path, "r") as f:
                payload_data = json.load(f)
            self._preview_payload(payload_data, composed)

            command.extend(["--payload", f"file://{processed_payload_path}"])
            log_info(f"Invoking {lambda_name} remotely (aws-cli) with payload: {payload_path}")
        else:
            log_info(f"Invoking {lambda_name} remotely (aws-cli) without payload")

        print(f"\n{Colors.CYAN}Executing: {' '.join(command)}{Colors.RESET}\n")
        print(f"{Colors.YELLOW}{'─' * 80}{Colors.RESET}\n")

        try:
            result = subprocess.run(command, check=False, capture_output=True, text=True)

            # Show response metadata
            if result.stdout:
                print(f"{Colors.GREEN}Response Metadata:{Colors.RESET}")
                print(result.stdout)

            # Show response body
            if os.path.exists("/tmp/invoke-response.json"):
                print(f"\n{Colors.GREEN}Response Body:{Colors.RESET}")
                with open("/tmp/invoke-response.json", "r") as f:
                    response = f.read()
                    print(response)

            print(f"\n{Colors.YELLOW}{'─' * 80}{Colors.RESET}")

            if result.returncode == 0:
                log_success("Function invoked successfully")
                return True
            else:
                log_warning(f"Command finished with code {result.returncode}")
                if result.stderr:
                    print(f"{Colors.RED}Error:{Colors.RESET} {result.stderr}")
                return True

        except FileNotFoundError:
            log_error("AWS CLI is not installed or not found in PATH")
            log_info("Install with: pip install awscli or brew install awscli")
            return False
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Command interrupted by user{Colors.RESET}")
            return True
        except Exception as e:
            log_error(f"Error executing command: {e}")
            return False

    def _select_invoke_option_with_fzf(self, func_name: str) -> Optional[str]:
        """
        Use fzf to select an invoke option

        Args:
            func_name: Lambda function name

        Returns:
            Option number (1-4) or None if cancelled/back
        """
        # Build menu options
        options = []
        option_map = {}  # Map display text to option number

        options.append(f"{Emojis.SERVER_MINUS}  Remote")
        option_map[options[-1]] = "1"

        options.append(f"{Emojis.SERVER_PLUS}  Remote with payload")
        option_map[options[-1]] = "2"

        options.append(f"{Emojis.MONITOR}  Local")
        option_map[options[-1]] = "3"

        options.append(f"{Emojis.MONITOR_IN}  Local with payload")
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
                    "Select invoke option: ",
                    "--header",
                    f"Invoke options for: {func_name}",
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

    def _show_invoke_submenu(self, func_name: str) -> bool:
        """
        Show invoke options submenu for a specific function using fzf

        Args:
            func_name: Selected Lambda function name

        Returns:
            True when exiting the submenu
        """
        while True:
            option = self._select_invoke_option_with_fzf(func_name)

            if option is None or option == "0":
                # User cancelled or selected back
                break

            # Handle the selected option
            if option == "1":
                # Invoke remote without payload
                self._invoke_function(func_name, None, local=False)
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            elif option == "2":
                # Invoke remote with payload - select payload first
                payload_path = self._select_payload_with_fzf(func_name)
                if payload_path:
                    self._invoke_function(func_name, payload_path, local=False)
                    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            elif option == "3":
                # Invoke local without payload
                self._invoke_function(func_name, None, local=True)
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            elif option == "4":
                # Invoke local with payload - select payload first
                payload_path = self._select_payload_with_fzf(func_name)
                if payload_path:
                    self._invoke_function(func_name, payload_path, local=True)
                    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

        return True

    def _invoke_menu(self) -> bool:
        """
        Show main invoke menu with fzf function selection

        Returns:
            True if executed correctly
        """
        log_header("INVOKE MENU - LAMBDA FUNCTIONS")

        while True:
            print(
                f"\n{Colors.BOLD}{Colors.CYAN}🔍 Use fzf to search and select a function to invoke{Colors.RESET}"
            )
            print(f"{Colors.CYAN}Press ESC or Ctrl+C to exit{Colors.RESET}\n")

            selected_func = self._select_function_with_fzf()

            if selected_func:
                self._show_invoke_submenu(selected_func)
            else:
                log_info("Exiting invoke menu")
                break

        return True
