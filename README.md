# CLI Manager Template

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Template](https://img.shields.io/badge/Type-Template-purple.svg)](#)

> A reusable Python template for building interactive CLI tools with fuzzy search menus and modular command architecture.

A flexible, production-ready template for creating command-line interfaces with:
- **Interactive menus** powered by `fzf` (fuzzy finder)
- **Auto-discovery** command system (no registration needed)
- **Multiple menu types** (simple, hierarchical, interactive, CLI-only)
- **Type-safe** Python 3.8+ with full type hints
- **Extensible** architecture for any use case

---

## What is This?

This is a **template**, not a finished application. It's designed to be cloned and customized for your specific needs.

**Original use case:** AWS Lambda manager with CloudWatch integration
**Current form:** Generic template for building interactive CLIs
**Your use case:** Whatever you need! (DevOps tools, data pipelines, admin dashboards, etc.)

### Why Use This Template?

- ✅ **No boilerplate**: Start with a working CLI structure
- ✅ **Interactive by default**: Users get fuzzy search menus automatically
- ✅ **Modular design**: Add commands without touching core code
- ✅ **Production-ready**: Error handling, logging, and validation included
- ✅ **Well-documented**: Examples for every pattern you'll need

---

## Features

### Interactive Menu System

```
┌─ CLI Manager Template ──────────────────┐
│ 👋 Greet                                │
│ 📁 Files                                │
│ 🧮 Calculator                           │
│ ℹ️  Info                                 │
└─────────────────────────────────────────┘
```

- **Fuzzy search**: Type to filter options
- **Multi-select**: Use `TAB` to select multiple items
- **Hierarchical menus**: Nested submenus with breadcrumb navigation
- **Keyboard shortcuts**: Arrow keys, TAB, ENTER, ESC
- **Fallback to CLI**: Commands work with or without interactive mode

### Command Types

| Type | Example | Use Case |
|------|---------|----------|
| **Simple Menu** | `greet.py` | Language selection, yes/no prompts |
| **Hierarchical** | `files.py` | File operations, nested workflows |
| **Interactive Input** | `calculator.py` | User input, form-like interfaces |
| **CLI-Only** | `info.py` | System info, read-only operations |

### Auto-Discovery Architecture

```
manager/commands/
├── base.py          # Abstract base class
├── greet.py         # Automatically discovered
├── files.py         # Automatically discovered
├── calculator.py    # Automatically discovered
└── info.py          # Automatically discovered
```

Just add a new file inheriting from `BaseCommand` — no registration needed!

### Modular Core

```
manager/core/
├── logger.py        # Colored output & logging
├── colors.py        # Terminal styling
├── menu.py          # Interactive menu system (fzf)
└── stats.py         # Statistics tracking
```

---

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Menu Types](#menu-types)
- [How to Extend](#how-to-extend)
- [Use Cases](#use-cases)
- [Configuration](#configuration)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## 🛠️ Installation

### Prerequisites

- **Python 3.8+**
- **fzf** (fuzzy finder for interactive menus)

Optional:
- **PyYAML** (for YAML output formatting)

### Install Dependencies

**macOS:**
```bash
brew install python fzf
pip install pyyaml
```

**Ubuntu/Debian:**
```bash
sudo apt install python3 fzf
pip install pyyaml
```

**Verify Installation:**
```bash
python manager.py requirements status
```

---

## ⚡ Quick Start

### 1. Clone and Customize

```bash
# Clone this template
git clone <this-repo> my-cli-tool
cd my-cli-tool

# Edit config.py with your project details
nano config.py
```

**Edit `config.py`:**
```python
PROJECT_NAME = "My CLI Tool"
PROJECT_VERSION = "1.0.0"

ITEMS = [
    "item-1",
    "item-2",
    "item-3",
]
```

### 2. Interactive Mode (Recommended)

```bash
# Start interactive menu (no arguments)
python manager.py
```

Navigate with arrow keys, select with ENTER, multi-select with TAB.

**Navigation:**
- `↑/↓`: Navigate menu items
- `TAB`: Select/deselect (in multi-select menus)
- `ENTER`: Confirm selection
- `ESC` or `Ctrl+C`: Go back or exit
- Type to filter options (fuzzy search)

### 3. CLI Mode (Traditional)

```bash
# List all items
python manager.py list-items

# Greet with a language
python manager.py greet --language es

# Show system info
python manager.py info

# Calculate something
python manager.py calculator
```

### 4. Example Workflows

**Workflow 1: Interactive File Management**
```bash
python manager.py
→ Select "Files"
→ Select "List Files"
→ View directory contents
```

**Workflow 2: CLI-based Calculation**
```bash
python manager.py calculator
→ Select operation (add, subtract, multiply, divide)
→ Enter numbers
→ Get result
```

**Workflow 3: Batch Greetings**
```bash
python manager.py greet --language es
python manager.py greet --language en
python manager.py greet --language fr
```

---

## 📚 Commands

### Built-in Example Commands

#### `greet`
Simple menu with language selection.

```bash
# Interactive mode
python manager.py greet

# CLI mode
python manager.py greet --language es
python manager.py greet --language en
```

**Supported languages:** es (Spanish), en (English), fr (French), de (German)

---

#### `files`
Hierarchical menu for file operations.

```bash
# Interactive mode
python manager.py files

# CLI mode (list files)
python manager.py files --action list
python manager.py files --action list --path /tmp
```

**Operations:**
- List files in directory
- Create new file
- Delete file

---

#### `calculator`
Interactive calculator with basic operations.

```bash
# Interactive mode
python manager.py calculator

# CLI mode
python manager.py calculator --operation add --a 5 --b 3
```

**Operations:** add, subtract, multiply, divide

---

#### `info`
Display system information (CLI-only command).

```bash
python manager.py info
```

Shows:
- Python version
- Operating system
- Current working directory
- Environment variables

---

#### `list-items`
List all configured items.

```bash
python manager.py list-items
```

Displays all items from `config.py:ITEMS`.

---

#### `clean`
Remove output artifacts.

```bash
python manager.py clean
```

Deletes the `OUTPUT_DIR` directory.

---

#### `requirements`
Check system dependencies.

```bash
python manager.py requirements status
```

Verifies installation of required tools.

---

## 🎨 Menu Types

### Type 1: Simple Menu

**Use case:** Language selection, yes/no prompts, single choice

```python
from manager.core.menu import MenuNode

def get_menu_tree(self) -> Optional[MenuNode]:
    return MenuNode(
        label="Select Language",
        emoji="🌐",
        children=[
            MenuNode(label="Spanish", action=lambda: self._greet_es()),
            MenuNode(label="English", action=lambda: self._greet_en()),
            MenuNode(label="French", action=lambda: self._greet_fr()),
        ]
    )
```

---

### Type 2: Hierarchical Menu

**Use case:** Multi-level workflows, nested operations

```python
def get_menu_tree(self) -> Optional[MenuNode]:
    return MenuNode(
        label="Files",
        emoji="📁",
        children=[
            MenuNode(
                label="Read Operations",
                emoji="📖",
                children=[
                    MenuNode(label="List Files", action=lambda: self._list()),
                    MenuNode(label="Show File", action=lambda: self._show()),
                ]
            ),
            MenuNode(
                label="Write Operations",
                emoji="✏️",
                children=[
                    MenuNode(label="Create File", action=lambda: self._create()),
                    MenuNode(label="Delete File", action=lambda: self._delete()),
                ]
            ),
        ]
    )
```

---

### Type 3: Interactive Input

**Use case:** Forms, user input, dynamic prompts

```python
def execute(self, args: Namespace) -> bool:
    """Interactive calculator"""
    operation = input("Select operation (add/subtract/multiply/divide): ")
    a = float(input("First number: "))
    b = float(input("Second number: "))
    
    result = self._calculate(operation, a, b)
    log_success(f"Result: {result}")
    return True
```

---

### Type 4: CLI-Only

**Use case:** Read-only operations, system info, no menu needed

```python
def get_menu_tree(self) -> Optional[MenuNode]:
    # Return None to disable interactive mode
    return None

def execute(self, args: Namespace) -> bool:
    """Show system information"""
    log_info(f"Python: {sys.version}")
    log_info(f"OS: {platform.system()}")
    return True
```

---

## 🔧 How to Extend

### Creating Your Own Command

1. **Create a new file** in `manager/commands/`:

```python
# manager/commands/mycommand.py
from manager.commands.base import BaseCommand
from argparse import ArgumentParser, Namespace
from manager.core.menu import MenuNode
from manager.core.logger import log_success, log_info
from typing import Optional

class MyCommand(BaseCommand):
    """Description of what this command does"""
    
    name = "mycommand"                    # CLI command name
    help = "Short help text"              # Shown in --help
    description = "Detailed description"  # Optional
    epilog = """Examples:
  manager.py mycommand --option value
"""
    
    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific arguments"""
        parser.add_argument('--option', help='Option description')
    
    def execute(self, args: Namespace) -> bool:
        """Execute the command logic"""
        log_info("Executing my command...")
        log_success("Command completed!")
        return True
    
    def get_menu_tree(self) -> Optional[MenuNode]:
        """Optional: Define interactive menu structure"""
        return MenuNode(
            label="My Command",
            emoji="⚙️",
            children=[
                MenuNode(
                    label="Option 1",
                    action=lambda: self._execute_option_1()
                ),
                MenuNode(
                    label="Option 2",
                    action=lambda: self._execute_option_2()
                ),
            ]
        )
    
    def _execute_option_1(self) -> bool:
        """Execute option 1"""
        log_success("Option 1 executed")
        return True
    
    def _execute_option_2(self) -> bool:
        """Execute option 2"""
        log_success("Option 2 executed")
        return True
```

2. **That's it!** The command is automatically discovered and registered.

3. **Test it:**
```bash
# CLI mode
python manager.py mycommand --help

# Interactive mode (if get_menu_tree() is implemented)
python manager.py
```

### Customizing Configuration

Edit `config.py` to customize your project:

```python
# Project metadata
PROJECT_NAME = "My CLI Tool"
PROJECT_VERSION = "1.0.0"

# Items to manage
ITEMS = [
    "item-1",
    "item-2",
    "item-3",
]

# Directories
DATA_DIR = "data"
OUTPUT_DIR = "output"

# Add custom dependencies
from manager.config import Dependency

DEPENDENCIES = [
    Dependency(
        name="my-tool",
        command="my-tool",
        description="My custom tool",
        install_macos="brew install my-tool",
        install_linux="sudo apt install my-tool",
        required=True,
    ),
]
```

### Using Base Class Helpers

The `BaseCommand` class provides utilities:

```python
from manager.commands.base import BaseCommand

class MyCommand(BaseCommand):
    def execute(self, args: Namespace) -> bool:
        # Resolve items from CLI args or dev menu
        items = self._resolve_item_list(args)
        
        # Get filtered items
        filtered = self._get_filtered_items("item-1")
        
        for item in items:
            self._process_item(item)
        
        return True
```

---

## 💡 Use Cases

### 1. DevOps Tool

Manage infrastructure, deployments, and monitoring:

```python
ITEMS = [
    "web-server",
    "database",
    "cache",
    "load-balancer",
]

# Commands: deploy, rollback, status, logs, scale
```

### 2. Data Pipeline Manager

Orchestrate ETL workflows:

```python
ITEMS = [
    "extract-raw-data",
    "transform-data",
    "load-to-warehouse",
    "validate-results",
]

# Commands: run, schedule, monitor, retry
```

### 3. Admin Dashboard

Manage users, permissions, and system settings:

```python
ITEMS = [
    "users",
    "roles",
    "permissions",
    "audit-logs",
]

# Commands: list, create, update, delete, export
```

### 4. Development Tool

Manage local development environment:

```python
ITEMS = [
    "database",
    "cache",
    "message-queue",
    "search-engine",
]

# Commands: start, stop, reset, logs, shell
```

### 5. Testing Framework

Run and manage test suites:

```python
ITEMS = [
    "unit-tests",
    "integration-tests",
    "e2e-tests",
    "performance-tests",
]

# Commands: run, report, coverage, benchmark
```

---

## ⚙️ Configuration

### `config.py` Structure

```python
# ============================================================================
# Project Metadata
# ============================================================================
PROJECT_NAME = "My CLI Tool"
PROJECT_VERSION = "1.0.0"

# ============================================================================
# Core Items List
# ============================================================================
ITEMS = [
    "example-item-1",
    "example-item-2",
    "example-item-3",
]

# ============================================================================
# Paths
# ============================================================================
DATA_DIR = "data"
OUTPUT_DIR = "output"

# ============================================================================
# Dependency Definition
# ============================================================================
from typing import NamedTuple, Optional

class Dependency(NamedTuple):
    """System dependency definition"""
    name: str
    command: str
    description: str
    check_arg: str = "--version"
    install_macos: Optional[str] = None
    install_linux: Optional[str] = None
    install_other: Optional[str] = None
    required: bool = True

# ============================================================================
# Required Dependencies
# ============================================================================
DEPENDENCIES = [
    Dependency(
        name="fzf",
        command="fzf",
        description="Fuzzy finder for interactive menus",
        install_macos="brew install fzf",
        install_linux="sudo apt install fzf",
        required=True,
    ),
    # Add more dependencies as needed
]
```

### Adding Custom Configuration

```python
# Custom settings for your project
CUSTOM_SETTING = "value"
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3

# Import in your commands
from manager.config import CUSTOM_SETTING, TIMEOUT_SECONDS
```

---

## 🔧 Development

### Project Structure

```
manager/
├── commands/          # Command implementations (auto-discovered)
│   ├── base.py       # Abstract base command
│   ├── greet.py      # Example: simple menu
│   ├── files.py      # Example: hierarchical menu
│   ├── calculator.py # Example: interactive input
│   ├── info.py       # Example: CLI-only
│   ├── list_items.py # List configured items
│   ├── clean.py      # Clean artifacts
│   └── requirements.py
│
├── core/             # Core utilities (shared logic)
│   ├── logger.py     # Logging functions
│   ├── colors.py     # Terminal styling
│   ├── menu.py       # Interactive menu system (fzf)
│   └── stats.py      # Statistics tracking
│
├── cli.py            # CLI entry point (orchestrator)
├── config.py         # Project configuration
├── manager.py        # Wrapper script
└── README.md         # This file
```

### Code Style Guidelines

**Type Hints:**
```python
def execute(self, args: Namespace) -> bool:
    items: List[str] = self._resolve_item_list(args)
    return self._process_items(items)
```

**Docstrings (Google style):**
```python
def process_item(self, item: str) -> bool:
    """
    Process a single item.

    Args:
        item: Name of the item to process

    Returns:
        True if successful, False otherwise
    """
    pass
```

**Logging (not print):**
```python
from manager.core.logger import log_info, log_success, log_error

log_info("Processing item...")
log_success("Item processed!")
log_error("Failed to process item")
```

**Naming Conventions:**
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Testing

**⚠️ No test suite exists yet.** When adding tests:

```bash
# Recommended: pytest
pytest tests/
pytest tests/test_commands.py
pytest tests/test_mycommand.py::test_name -v
```

### Linting

**Recommended setup:**

```bash
# Black (code formatter)
black manager/ --check
black manager/

# Flake8 (style guide)
flake8 manager/ --max-line-length=100

# MyPy (type checking)
mypy manager/ --strict

# isort (import sorting)
isort manager/ --check-only
```

---

## 🐛 Troubleshooting

### `fzf: command not found`

Install fzf:
```bash
# macOS
brew install fzf

# Ubuntu/Debian
sudo apt install fzf
```

### `ModuleNotFoundError: No module named 'manager'`

Ensure you're running from the project root:
```bash
cd /path/to/manager
python manager.py
```

### Menu not showing (interactive mode)

Check that fzf is installed:
```bash
which fzf
fzf --version
```

### PyYAML import error

Install PyYAML (optional):
```bash
pip install pyyaml
```

### Check Requirements

Verify all dependencies:
```bash
python manager.py requirements status
```

---

## 📖 Best Practices

### 1. Command Organization

Keep commands focused and single-purpose:

```python
# ✅ Good: One responsibility
class GreetCommand(BaseCommand):
    """Greet users in different languages"""
    # ...

# ❌ Bad: Multiple responsibilities
class GreetAndCalculateCommand(BaseCommand):
    """Greet users AND do math"""
    # ...
```

### 2. Error Handling

Fail gracefully with helpful messages:

```python
from manager.core.logger import log_error, log_info

if item not in ITEMS:
    log_error(f"Item '{item}' not found")
    log_info(f"Available items: {', '.join(ITEMS)}")
    return False
```

### 3. Interactive Support

Commands should work in both CLI and interactive modes:

```python
def execute(self, args: Namespace) -> bool:
    # Works for both modes
    items = self._resolve_item_list(args)
    return self._process_items(items)

def get_menu_tree(self) -> Optional[MenuNode]:
    # Optional: add interactive menu support
    return MenuNode(...)
```

### 4. Configuration

Never hardcode values:

```python
# ✅ Good
from manager.config import ITEMS, OUTPUT_DIR

# ❌ Bad
ITEMS = ["hardcoded", "values"]
OUTPUT_DIR = "/tmp/output"
```

### 5. Logging

Use logger utilities, not print:

```python
# ✅ Good
from manager.core.logger import log_success
log_success("Operation completed")

# ❌ Bad
print("Operation completed")
```

---

## 🤝 Contributing

### Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-command`)
3. Add your command in `manager/commands/`
4. Test thoroughly
5. Update README.md if adding new features
6. Submit a pull request

### Adding New Commands

See [How to Extend](#how-to-extend) section above.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **fzf**: Interactive fuzzy finder
- **Python**: Programming language
- **Keep a Changelog**: Changelog format standard

---

## 📬 Support

For issues, questions, or contributions:

- **Issues**: [GitHub Issues](https://github.com/yourusername/yourrepo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/yourrepo/discussions)

---

**Built with ❤️ for CLI developers**
