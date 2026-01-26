"""Check system requirements and dependencies"""

import subprocess
import shutil
import platform
from argparse import ArgumentParser, Namespace

from manager.commands.base import BaseCommand
from manager.core.logger import (
    log_header,
    log_error,
    log_warning,
    log_info,
    log_success,
)
from manager.core.colors import Colors
from manager.core.emojis import Emojis
from manager.config import DEPENDENCIES, Dependency
from manager.core.menu import MenuNode
from typing import Optional


class RequirementsCommand(BaseCommand):
    """Check system requirements and dependencies"""

    name = "requirements"
    help = "Check system requirements status"
    description = "Verify that all required system dependencies are installed"
    epilog = """Examples:
  manager.py requirements    # Check all dependencies
"""

    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific arguments"""
        pass

    def execute(self, args: Namespace) -> bool:
        """Execute requirements command"""
        return self._check_status()

    def _check_dependency(self, dep: Dependency) -> tuple:
        """
        Check if a dependency is installed

        Args:
            dep: Dependency configuration

        Returns:
            Tuple of (installed: bool, version: str or None)
        """
        command = dep.command
        check_arg = dep.check_arg

        try:
            # Check if command exists
            if not shutil.which(command):
                return (False, None)

            # Try to get version
            result = subprocess.run(
                [command] + check_arg.split(), capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                # Extract version from output (first line, stripped)
                version = result.stdout.strip().split("\n")[0]
                if not version and result.stderr:
                    version = result.stderr.strip().split("\n")[0]
                return (True, version)
            else:
                # Command exists but check failed (might still be installed)
                return (True, "installed")

        except subprocess.TimeoutExpired:
            return (True, "timeout")
        except Exception:
            return (False, None)

    def _detect_os(self) -> str:
        """
        Detect the operating system

        Returns:
            OS identifier (ubuntu, debian, macos, arch, fedora, etc.)
        """
        system = platform.system().lower()

        if system == "darwin":
            return "macos"
        elif system == "linux":
            # Try to detect Linux distribution
            try:
                with open("/etc/os-release", "r") as f:
                    content = f.read().lower()
                    if "ubuntu" in content:
                        return "ubuntu"
                    elif "debian" in content:
                        return "debian"
                    elif "arch" in content:
                        return "arch"
                    elif "fedora" in content:
                        return "fedora"
            except FileNotFoundError:
                pass
            return "linux"
        else:
            return system

    def _get_install_command(self, dep: Dependency) -> str:
        """
        Get installation command for current OS

        Args:
            dep: Dependency configuration

        Returns:
            Installation command string
        """
        os_type = self._detect_os()

        # Try OS-specific command
        if os_type == "macos" and dep.install_macos:
            return dep.install_macos
        elif os_type in ["linux", "ubuntu", "debian"] and dep.install_linux:
            return dep.install_linux
        elif dep.install_other:
            return dep.install_other

        return "See documentation for installation instructions"

    def _check_status(self) -> bool:
        """
        Check status of all dependencies

        Returns:
            True if all required dependencies are installed, False otherwise
        """
        log_header("SYSTEM REQUIREMENTS STATUS")

        print(f"\n{Colors.BOLD}Checking system dependencies...{Colors.RESET}\n")

        all_installed = True
        required_missing = []
        optional_missing = []

        # Check each dependency
        for dep in DEPENDENCIES:
            is_required = dep.required
            description = dep.description
            installed, version = self._check_dependency(dep)

            # Format output
            status_icon = (
                f"{Colors.GREEN}{Emojis.SUCCESS}{Colors.RESET}"
                if installed
                else f"{Colors.RED}{Emojis.ERROR}{Colors.RESET}"
            )
            required_badge = (
                f"{Colors.YELLOW}[REQUIRED]{Colors.RESET}"
                if is_required
                else f"{Colors.CYAN}[OPTIONAL]{Colors.RESET}"
            )

            print(f"{status_icon} {required_badge} {Colors.BOLD}{dep.name}{Colors.RESET}")
            print(f"   {description}")

            if installed:
                version_text = version if version and version != "installed" else "installed"
                print(f"   {Colors.GREEN}✓ {version_text}{Colors.RESET}")
            else:
                install_cmd = self._get_install_command(dep)
                print(f"   {Colors.RED}✗ Not installed{Colors.RESET}")
                print(f"   {Colors.CYAN}Install: {install_cmd}{Colors.RESET}")

                # Track missing dependencies
                if is_required:
                    all_installed = False
                    required_missing.append(dep.name)
                else:
                    optional_missing.append(dep.name)

            print()  # Empty line between dependencies

        # Summary
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'═' * 60}{Colors.RESET}")

        if all_installed and not optional_missing:
            print(f"{Colors.GREEN}{Emojis.SUCCESS} All dependencies are installed!{Colors.RESET}")
            return True
        elif all_installed:
            print(
                f"{Colors.GREEN}{Emojis.SUCCESS} All required dependencies are installed!{Colors.RESET}"
            )
            if optional_missing:
                print(
                    f"{Colors.CYAN}{Emojis.INFO} Optional dependencies missing: {', '.join(optional_missing)}{Colors.RESET}"
                )
            return True
        else:
            print(
                f"{Colors.RED}{Emojis.ERROR} Missing required dependencies: {', '.join(required_missing)}{Colors.RESET}"
            )
            print(
                f"\n{Colors.YELLOW}Please install the missing dependencies before using this manager.{Colors.RESET}"
            )
            return False

    def get_menu_tree(self) -> Optional[MenuNode]:
        """Interactive menu for greet command"""
        return MenuNode(
            label="Check Requirements",
            emoji=Emojis.FLOPPY,
            action=lambda: self.execute(Namespace()),
        )
