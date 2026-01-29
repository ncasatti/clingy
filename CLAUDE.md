# AGENTS.md

**AI Coding Agents Guide** for the clingy framework project.

---

## Project Overview

**clingy** is a context-aware CLI framework for building interactive command-line tools with fuzzy search menus and modular command architecture. It works like Git/Poetry/Terraform - install once, use everywhere.

- **Language:** Python 3.8+
- **Architecture:** Context-aware framework with auto-discovery
- **Menu System:** Interactive menus powered by `fzf` (fuzzy finder)
- **Dependencies:** fzf, python
- **Use Cases:** DevOps tools, data pipelines, admin dashboards, development utilities

---

## Build/Test/Lint Commands

### Run the CLI

```bash
# Install framework (development mode)
pip install -e .

# Initialize a test project
cd /tmp && mkdir test-project && cd test-project
clingy init

# Interactive mode (recommended)
clingy                              # Starts fuzzy-searchable menu system

# CLI mode (traditional)
clingy <command> [options]

# Examples
clingy greet --language es
clingy info
clingy calculator

# Or run directly (development)
python -m clingy.cli init
python -m clingy.cli
```

### Example Commands

```bash
# Initialize new project
clingy init                           # Create project in current directory
clingy init --force                   # Overwrite existing project

# Greet in different languages
clingy greet                          # Interactive menu
clingy greet --language es            # Spanish

# Calculator
clingy calculator                     # Interactive mode

# System info
clingy info                           # Show system information
```

### Testing

**⚠️ No test suite exists yet.** When adding tests:

```bash
# Recommended: pytest
pytest tests/                          # Run all tests
pytest tests/test_commands.py          # Run specific test file
pytest tests/test_mycommand.py::test_name  # Run single test
pytest -v                              # Verbose output
pytest -x                              # Stop on first failure
pytest --pdb                           # Drop into debugger on failure
```

### Linting/Formatting

**Configured:** Black (line-length: 100)

```bash
# Format code
black . --line-length 100

# Check without modifying
black . --check --line-length 100

# Format specific files
black clingy/
```

**Optional (not configured):**

```bash
# Flake8 (style guide)
flake8 . --max-line-length=100

# MyPy (type checking)
mypy . --strict

# isort (import sorting)
isort . --profile black
```

### Utility Commands

```bash
# Initialize new project
clingy init

# Run from any subdirectory (context-aware)
cd my-project/subdir
clingy  # Automatically finds project root
```

---

## Code Style Guidelines

### 1. General Principles

- **Explicit over implicit**: Type everything, document everything
- **Modular design**: One responsibility per class/function
- **Error handling**: Fail gracefully with clear error messages
- **Logging**: Use `core/logger.py` utilities for all output
- **Configuration**: Never hardcode values, use `config.py`

### 2. File Organization

```
clingy/          # Framework package
├── commands/          # Framework commands
│   ├── base.py       # Abstract base class
│   ├── init.py       # Project initialization
│   └── __init__.py   # Command discovery
│
├── core/             # Core utilities (shared logic)
│   ├── discovery.py  # Context detection
│   ├── logger.py     # Logging functions
│   ├── colors.py     # Terminal styling
│   ├── menu.py       # Interactive menu system (fzf)
│   └── stats.py      # Statistics tracking
│
├── templates/        # Project templates
│   └── basic/        # Default template
│       ├── commands/ # Example commands
│       └── config.py # Example config
│
├── cli.py            # CLI entry point (orchestrator)
├── cli_builder.py    # Context builder
└── config.py         # Framework configuration
```

### 3. Imports

**Order:** Standard library → Third-party → Local modules

```python
# Standard library
import os
import sys
from typing import List, Optional

# Third-party
from argparse import ArgumentParser, Namespace

# Local
from clingy.commands.base import BaseCommand
from clingy.core.logger import log_error, log_success
from clingy.config import ITEMS
```

**Guidelines:**
- Use absolute imports: `from clingy.core.logger import log_info`
- Group imports by category with blank lines
- Sort alphabetically within each group
- Avoid `import *` (always explicit imports)

### 4. Type Hints

**Required for all functions:**

```python
def execute(self, args: Namespace) -> bool:
    """Execute command logic"""
    items: List[str] = self._resolve_item_list(args)
    return self._process_items(items)

def _get_filtered_items(self, filter: Optional[str]) -> List[str]:
    """Get filtered item list"""
    if filter is None:
        return ITEMS
    return [filter] if filter in ITEMS else []
```

**Common types:**
- `List[str]`, `Dict[str, Any]`, `Optional[str]`
- `Namespace` (from argparse)
- `bool` for success/failure return values

### 5. Docstrings

**Use Google-style docstrings:**

```python
def process_item(self, item_name: str, output_dir: str) -> bool:
    """
    Process a single item.

    Args:
        item_name: Name of the item to process
        output_dir: Directory to write output

    Returns:
        True if processing succeeded, False otherwise

    Raises:
        FileNotFoundError: If item doesn't exist
    """
    pass
```

**Required for:**
- All public methods
- All classes (class-level docstring)
- Complex private methods (use judgment)

### 6. Naming Conventions

**Files:** `snake_case.py` (e.g., `my_command.py`)  
**Classes:** `PascalCase` (e.g., `MyCommand`, `BaseCommand`)  
**Functions/Variables:** `snake_case` (e.g., `process_item`, `item_name`)  
**Constants:** `UPPER_SNAKE_CASE` (e.g., `ITEMS`, `OUTPUT_DIR`)  
**Private methods:** `_leading_underscore` (e.g., `_validate_item`)

### 7. Command Structure

**All commands inherit from `BaseCommand`:**

```python
from clingy.commands.base import BaseCommand
from argparse import ArgumentParser, Namespace
from clingy.core.menu import MenuNode
from typing import Optional

class MyCommand(BaseCommand):
    """One-line description of command"""
    
    name = "mycommand"                    # CLI command name
    help = "Short help text"              # Shown in --help
    description = "Detailed description"  # Optional, defaults to help
    epilog = """Examples:
  clingy mycommand --option value
"""
    
    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific CLI arguments"""
        parser.add_argument('--option', help='Option description')
    
    def execute(self, args: Namespace) -> bool:
        """
        Execute the command logic.
        
        Returns:
            True on success, False on failure
        """
        # Use base class helpers
        items = self._resolve_item_list(args)
        
        # Your logic here
        for item in items:
            self._process_item(item)
        
        return True
    
    def get_menu_tree(self) -> MenuNode:
        """
        REQUIRED: Define interactive menu structure.
        
        All commands must implement this method.
        For simple commands without submenus, use:
            MenuNode(
                label="Command Name",
                emoji=Emojis.ICON,
                action=lambda: self.execute(Namespace())
            )
        """
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
        return True
    
    def _execute_option_2(self) -> bool:
        """Execute option 2"""
        return True
```

**Key patterns:**
- Commands are **auto-discovered** (no registration needed)
- Use `_resolve_item_list(args)` to support both CLI and interactive menu
- Return `bool` for success/failure (affects exit code)
- Use `log_*` functions from `core/logger.py` for output
- Implement `get_menu_tree()` for interactive menu support (required)

### 7.5. Interactive Menu Support

All commands **must** support **interactive menu mode** by implementing `get_menu_tree()`:

```python
from manager.core.menu import MenuNode

class MyCommand(BaseCommand):
    """Command with interactive menu support"""
    
    name = "mycommand"
    help = "Short help text"
    
    def get_menu_tree(self) -> MenuNode:
        """
        Define the interactive menu structure.
        
        REQUIRED: All commands must implement this method.
        """
        return MenuNode(
            label="My Command",
            emoji="⚙️",
            children=[
                MenuNode(
                    label="Process All",
                    emoji="🔄",
                    action=lambda: self._process_all()
                ),
                MenuNode(
                    label="Process Specific",
                    emoji="🔄",
                    children=[
                        MenuNode(
                            label="item-1",
                            action=lambda: self._process_item("item-1")
                        ),
                        MenuNode(
                            label="item-2",
                            action=lambda: self._process_item("item-2")
                        ),
                    ]
                ),
            ]
        )
    
    def _process_all(self) -> bool:
        """Process all items"""
        # Implementation
        return True
    
    def _process_item(self, item_name: str) -> bool:
        """Process specific item"""
        # Implementation
        return True
```

**MenuNode Structure:**

```python
@dataclass
class MenuNode:
    label: str                              # Display text
    emoji: str = ""                         # Optional emoji prefix
    children: List[MenuNode] = []           # Submenu items
    action: Optional[Callable[[], bool]] = None  # Function to execute
    data: Dict[str, Any] = {}               # Extra context data
    
    def is_leaf(self) -> bool:              # True if executable (no children)
    def is_submenu(self) -> bool:           # True if has children
    def display_label(self) -> str:         # Formatted label for fzf
```

**Key Points:**
- **Leaf nodes**: Have `action` but no `children` (executable)
- **Submenu nodes**: Have `children` but no `action` (navigable)
- **Emojis**: Automatically prefixed to labels in fzf
- **Navigation**: fzf handles breadcrumb and "← Back" option
- **Multi-select**: Use `fzf_select_items()` for item selection

**Example: Command with Menu:**

```python
from clingy.core.menu import MenuNode, fzf_select_items

class ProcessCommand(BaseCommand):
    name = "process"
    help = "Process items"
    
    def get_menu_tree(self) -> Optional[MenuNode]:
        return MenuNode(
            label="Process",
            emoji="🔄",
            children=[
                MenuNode(
                    label="Process All Items",
                    action=lambda: self._process_all()
                ),
                MenuNode(
                    label="Select Items",
                    action=lambda: self._process_selected()
                ),
            ]
        )
    
    def _process_all(self) -> bool:
        """Process all items"""
        items = ITEMS
        return self._process_items(items)
    
    def _process_selected(self) -> bool:
        """Let user select items to process"""
        items = fzf_select_items(
            prompt="Select items to process: ",
            include_all=True
        )
        if not items:
            return False
        return self._process_items(items)
    
    def _process_items(self, items: List[str]) -> bool:
        """Process specified items"""
        # Implementation
        return True
```

### 8. Error Handling

**Fail gracefully with user-friendly messages:**

```python
from clingy.core.logger import log_error, log_warning, log_info

# Validate input
if item_name not in ITEMS:
    log_error(f"Item '{item_name}' not found")
    log_info(f"Available: {', '.join(ITEMS[:5])}...")
    return False

# Handle subprocess errors
try:
    result = subprocess.run(command, check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    log_error(f"Operation failed: {e.stderr.strip()}")
    return False
except FileNotFoundError:
    log_error("Required tool not found. Install with: brew install tool")
    return False
```

**Guidelines:**
- Catch specific exceptions (not bare `except:`)
- Log errors with `log_error()`, warnings with `log_warning()`
- Provide actionable error messages (how to fix)
- Return `False` on failure (don't raise unless fatal)

### 9. Logging

**Use logger utilities (NOT print):**

```python
from clingy.core.logger import (
    log_header,   # Major section header
    log_section,  # Subsection header
    log_success,  # Success message (green checkmark)
    log_error,    # Error message (red X)
    log_warning,  # Warning message (yellow !)
    log_info,     # Info message (cyan i)
    print_summary # Final statistics summary
)

# Example
log_section(f"PROCESSING {len(items)} ITEMS")
for item in items:
    log_info(f"Processing {item}")
    if success:
        log_success(f"{item} → completed", duration=1.2)
    else:
        log_error(f"{item} → failed")
print_summary()
```

### 10. Configuration

**Never hardcode values.** Use `config.py`:

```python
from clingy.config import (
    ITEMS,           # List of all items
    PROJECT_NAME,    # Project name
    PROJECT_VERSION, # Project version
    DATA_DIR,        # Data directory
    OUTPUT_DIR,      # Output directory
)
```

**When adding new config:**
- Add to `config.py` with comments
- Use UPPER_SNAKE_CASE for constants
- Group related settings with section headers
- Document the purpose of each setting

---

## Common Patterns

### Item Resolution (CLI + Interactive Mode)

```python
def execute(self, args: Namespace) -> bool:
    # This works for both CLI (-i flag) and interactive menu (item_list)
    items = self._resolve_item_list(args)
    if not items:
        return False  # Error already logged
    
    for item in items:
        self._process_item(item)
    return True
```

### Processing with Stats

```python
from clingy.core.stats import stats

stats.reset()
stats.total_items = len(items)

for item in items:
    if success:
        stats.add_success()
    else:
        stats.add_failure(item)

print_summary()  # Prints stats automatically
```

### Subprocess Execution

```python
import subprocess

result = subprocess.run(
    ["command", "arg1", "arg2"],
    check=True,           # Raise on error
    capture_output=True,  # Capture stdout/stderr
    text=True,            # Return strings (not bytes)
    cwd=working_dir       # Working directory
)
```

### Interactive Menu Navigation

**How fzf integration works:**

```python
from clingy.core.menu import MenuRenderer, MenuNode

# Create menu tree
root = MenuNode(
    label="Main Menu",
    emoji="🚀",
    children=[
        MenuNode(label="Option 1", action=lambda: do_something()),
        MenuNode(label="Option 2", action=lambda: do_something_else()),
    ]
)

# Render and show
renderer = MenuRenderer(root, header="My App")
success = renderer.show()
```

**User Flow:**
1. User runs `manager` (no args)
2. Framework detects project and loads commands
3. `cli.py:interactive_mode()` builds menu tree from all commands
4. `MenuRenderer.show()` handles navigation with fzf
5. When user selects a leaf node, its `action()` is called
6. After action completes, menu returns to parent
7. User can navigate back with "← Back" or ESC

**Keyboard Shortcuts in fzf:**
- `↑/↓`: Navigate
- `TAB`: Multi-select (if enabled)
- `ENTER`: Confirm
- `ESC`: Cancel/Go back
- `Ctrl+C`: Exit (exit code 130)

---

## Creating Your Own Manager

### Step 1: Initialize Project

```bash
mkdir my-cli-tool
cd my-cli-tool
clingy init
```

### Step 2: Customize Configuration

Edit `config.py`:

```python
PROJECT_NAME = "My CLI Tool"
PROJECT_VERSION = "1.0.0"

ITEMS = [
    "item-1",
    "item-2",
    "item-3",
]

DATA_DIR = "data"
OUTPUT_DIR = "output"
```

### Step 3: Create Your Commands

Create new files in `commands/`:

```python
# commands/mycommand.py
from clingy.commands.base import BaseCommand
from argparse import ArgumentParser, Namespace
from clingy.core.menu import MenuNode
from clingy.core.logger import log_success
from typing import Optional

class MyCommand(BaseCommand):
    name = "mycommand"
    help = "My custom command"
    
    def execute(self, args: Namespace) -> bool:
        items = self._resolve_item_list(args)
        for item in items:
            log_success(f"Processing {item}")
        return True
    
    def get_menu_tree(self) -> Optional[MenuNode]:
        return MenuNode(
            label="My Command",
            emoji="⚙️",
            children=[
                MenuNode(
                    label="Process All",
                    action=lambda: self.execute(Namespace(item_list=ITEMS))
                ),
            ]
        )
```

### Step 4: Test

```bash
# Interactive mode
python manager.py

# CLI mode
clingy mycommand
```

### Step 5: Update Documentation

Update `README.md` with your project details:
- Project description
- Installation instructions
- Usage examples
- Configuration guide

---

## Best Practices

1. **Read before writing:** If modifying a command, read similar commands first
2. **Validate inputs:** Check item names exist, files exist, etc.
3. **Atomic operations:** Each command should do ONE thing well
4. **Interactive support:** Commands should work in both CLI and interactive menu
5. **Cross-platform:** Use `os.path.join()`, not hardcoded slashes
6. **Progress feedback:** Log each step (especially in long operations)
7. **Clean state:** Don't leave artifacts on failure
8. **Documentation:** Update README.md when adding new features

---

## Notes for AI Agents

- **No tests exist yet:** When writing tests, use pytest with fixtures
- **Auto-discovery:** New commands are auto-registered (no imports needed)
- **Base class helpers:** Use `_resolve_item_list()` and `_get_filtered_items()`
- **Interactive menus:** Implement `get_menu_tree()` to add interactive support
- **Menu system:** Uses `MenuNode` (tree structure) + `MenuRenderer` (fzf navigation)
- **Item selection:** Use `fzf_select_items()` for multi-select in menus
- **Colors/Emojis:** Already handled by logger utilities
- **Configuration:** All settings in `config.py` (never hardcode values)
- **Items:** Defined in `config.py:ITEMS` (not tied to any specific resource type)
- **Linting:** Use black with line-length 100
- **Comments:** All comments must be in English
- **get_menu_tree():** Now mandatory (abstract method), not optional
- **Emojis:** Centralized in `core/colors.py` `Emojis` class

---

## Example Commands Reference

### greet.py (Simple Menu)

```python
# Simple menu with language selection
# Shows: Spanish, English, French, German
# Pattern: Single-level menu with actions
```

### files.py (Hierarchical Menu)

```python
# Hierarchical menu for file operations
# Shows: List Files, Create File, Delete File
# Pattern: Multi-level menu with nested operations
```

### calculator.py (Interactive Input)

```python
# Interactive calculator with user input
# Shows: Operation selection, number input, result
# Pattern: Form-like interface with prompts
```

### info.py (CLI-Only)

```python
# System information display
# Shows: Python version, OS, working directory
# Pattern: No menu, CLI-only command
```

---

**Last Updated:** 2026-01-23 (Black linter + English comments refactor)  
**Python Version:** 3.8+  
**Primary Maintainer:** @ncasatti
