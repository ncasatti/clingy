"""Color and emoji definitions for terminal output"""


class Colors:
    """ANSI color codes for enhanced terminal output"""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def disable():
        """Disable colors for environments that don't support them"""
        Colors.RED = Colors.GREEN = Colors.YELLOW = Colors.BLUE = ""
        Colors.MAGENTA = Colors.CYAN = Colors.WHITE = Colors.BOLD = Colors.RESET = ""


class Emojis:
    """Emoji icons for better visualization"""

    SUCCESS = " "
    ERROR = ""
    WARNING = ""
    INFO = ""
    ROCKET = ""
    PACKAGE = "📦"
    BUILD = ""
    CLEAN = ""
    LIST = "📋"
    DOCUMENT = "📄"
    TIME = ""
    STATS = "📊"
    CIRCULAR = ""
    SEARCH = "🔍"
    BACK = "󰁭"
    RUN = ""
    SERVER_PLUS = "󰒐"
    SERVER_MINUS = "󰒌"
    MONITOR = "󰍹"
    MONITOR_IN = "󱒃"
    FLOPPY = "💾"
    PENCIL = "󰏫 "
    PLUS = " "
    TRASH = " "
