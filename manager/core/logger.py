"""Logging functions for enhanced terminal output"""

from datetime import datetime
from manager.core.colors import Colors
from manager.core.emojis import Emojis
from manager.core.stats import stats


def log_header(title: str):
    """Print a nice header for sections"""
    border = "=" * 50
    print(f"\n{Colors.BOLD}{Colors.CYAN}{Emojis.ROCKET} {border}")
    print(f"   {title}")
    print(f"   {border}{Colors.RESET}\n")


def log_section(title: str):
    """Print a section title"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{Emojis.PACKAGE} {title}{Colors.RESET}")
    print(f"{Colors.BLUE}{'─' * (len(title) + 4)}{Colors.RESET}")


def log_success(message: str, duration: float = None):
    """Log success with timestamp and optional duration"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    duration_str = f" ({duration:.1f}s)" if duration else ""
    print(f"{Colors.GREEN}{Emojis.SUCCESS} [{timestamp}] {message}{duration_str}{Colors.RESET}")


def log_error(message: str, duration: float = None):
    """Log error with timestamp and optional duration"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    duration_str = f" ({duration:.1f}s)" if duration else ""
    print(f"{Colors.RED}{Emojis.ERROR} [{timestamp}] {message}{duration_str}{Colors.RESET}")


def log_warning(message: str):
    """Log warning"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.YELLOW}{Emojis.WARNING} [{timestamp}] {message}{Colors.RESET}")


def log_info(message: str):
    """Log informational message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.CYAN}{Emojis.INFO} [{timestamp}] {message}{Colors.RESET}")


def print_summary():
    """Print final summary with statistics"""
    total_time = stats.get_duration()

    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{Emojis.STATS} OPERATION SUMMARY:{Colors.RESET}")
    print(f"{'─' * 30}")

    if stats.total_functions > 0:
        success_rate = stats.get_success_rate()
        print(
            f"{Colors.GREEN}{Emojis.SUCCESS} Successful: {stats.successful}/{stats.total_functions} ({success_rate:.1f}%){Colors.RESET}"
        )

        if stats.failed > 0:
            print(
                f"{Colors.RED}{Emojis.ERROR} Failed:  {stats.failed}/{stats.total_functions}{Colors.RESET}"
            )
            if stats.failed_functions:
                print(
                    f"{Colors.YELLOW}   Failed functions: {', '.join(stats.failed_functions)}{Colors.RESET}"
                )

    print(f"{Colors.CYAN}{Emojis.TIME} Total time: {total_time:.1f}s{Colors.RESET}")

    if stats.failed == 0 and stats.total_functions > 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Operation completed successfully!{Colors.RESET}")
    elif stats.failed > 0:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Operation completed with errors{Colors.RESET}")
