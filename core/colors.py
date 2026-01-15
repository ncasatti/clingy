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
    """
    Emoji/Icon definitions for terminal output
    
    Customize these icons based on your terminal's font support.
    Common options:
    - Nerd Fonts: Use  icons (require patched fonts)
    - Unicode Emoji: Use 🚀 🎯 📦 (work in most terminals)
    - ASCII fallback: Use plain text like [OK] [!!] etc.
    """
    
    # ============================================================================
    # Status Indicators
    # ============================================================================
    SUCCESS = " "
    ERROR = ""
    WARNING = ""
    INFO = ""
    
    # ============================================================================
    # Actions
    # ============================================================================
    ROCKET = ""
    BUILD = ""
    CLEAN = ""
    RUN = ""
    SEARCH = "🔍"
    BACK = "󰁭"
    
    # ============================================================================
    # Objects
    # ============================================================================
    PACKAGE = "📦"
    DOCUMENT = "📄"
    LIST = "📋"
    FLOPPY = "💾"
    
    # ============================================================================
    # Time & Stats
    # ============================================================================
    TIME = ""
    STATS = "📊"
    CIRCULAR = ""
    
    # ============================================================================
    # Server/Monitor
    # ============================================================================
    SERVER_PLUS = "󰒐"
    SERVER_MINUS = "󰒌"
    MONITOR = "󰍹"
    MONITOR_IN = "󱒃"
    
    # ============================================================================
    # Edit Operations
    # ============================================================================
    PENCIL = "󰏫 "
    PLUS = " "
    TRASH = " "
    
    # ============================================================================
    # Commands - Main Menu Icons
    # ============================================================================
    FILES = "📁"
    CALCULATOR = "🔢"
    GREET = "👋"
    CMD_INFO = ""
    REQUIREMENTS = "📌"
    
    # ============================================================================
    # Math Operations
    # ============================================================================
    ADD = "➕"
    SUBTRACT = "➖"
    MULTIPLY = "✖️"
    DIVIDE = "➗"
    
    # ============================================================================
    # File Operations
    # ============================================================================
    FILE_LIST = "📋"
    FILE_CREATE = "➕"
    FILE_DELETE = "🗑️"
    
    # ============================================================================
    # Languages/Flags
    # ============================================================================
    FLAG_GB = "🇬🇧"
    FLAG_ES = "🇪🇸"
    FLAG_FR = "🇫🇷"
    FLAG_DE = "🇩🇪"
    FLAG_BR = "🇧🇷"
    FLAG_IT = "🇮🇹"
