# AGENTS.md

**AI Coding Agents Guide** for the Serverless Manager CLI project.

---

## Project Overview

**Python CLI tool** for managing AWS Lambda functions with Go runtime. Features modular command discovery, CloudWatch Insights integration, and interactive development workflows.

- **Language:** Python 3.8+
- **Runtime Target:** AWS Lambda (Go 1.19+)
- **Architecture:** Modular command-based CLI with auto-discovery
- **Dependencies:** fzf, serverless, awscli, go, python, pyyaml

---

## Build/Test/Lint Commands

### Run the CLI

```bash
# Interactive mode (recommended)
python manager.py                    # Starts fuzzy-searchable menu system

# CLI mode (traditional)
python manager.py <command> [options]

# Examples
python manager.py build -f status
python manager.py deploy --all
python manager.py logs -f status
```

### Build Commands

```bash
# Build Go functions
python manager.py build                # Build all functions
python manager.py build -f getUsers    # Build specific function

# Create deployment packages
python manager.py zip
python manager.py zip -f status

# Deploy to AWS
python manager.py deploy --all
python manager.py deploy -f status
```

### Testing

**⚠️ No test suite exists yet.** When adding tests:

```bash
# Recommended: pytest
pytest tests/                          # Run all tests
pytest tests/test_commands.py          # Run specific test file
pytest tests/test_build.py::test_name  # Run single test
pytest -v                              # Verbose output
pytest -x                              # Stop on first failure
pytest --pdb                           # Drop into debugger on failure
```

### Linting/Formatting

**⚠️ No linters configured yet.** Recommended setup:

```bash
# Black (code formatter)
black manager/ --check                 # Check formatting
black manager/                         # Auto-format code

# Flake8 (style guide)
flake8 manager/ --max-line-length=100

# MyPy (type checking)
mypy manager/ --strict

# isort (import sorting)
isort manager/ --check-only
isort manager/
```

### Utility Commands

```bash
# Check system dependencies
python manager.py requirements status

# List all functions
python manager.py list

# Clean build artifacts
python manager.py clean

# View CloudWatch logs
python manager.py logs -f status

# Run Insights queries
python manager.py insights -f processContenedor
```

---

## Code Style Guidelines

### 1. General Principles

- **Explicit over implicit**: Type everything, document everything
- **Modular design**: One responsibility per class/function
- **Error handling**: Fail gracefully with clear error messages
- **Logging**: Use `core/logger.py` utilities for all output

### 2. File Organization

```
manager/
├── commands/          # Command implementations (auto-discovered)
│   ├── base.py       # Abstract base class
│   ├── build.py      # Each command is a self-contained module
│   └── ...
├── core/             # Core utilities (shared logic)
│   ├── logger.py     # Logging functions
│   ├── colors.py     # Terminal styling
│   ├── menu.py       # Interactive menu system (fzf)
│   └── ...
├── cli.py            # CLI entry point (orchestrator)
├── config.py         # Project-specific configuration
└── manager.py        # Wrapper script
```

### 3. Imports

**Order:** Standard library → Third-party → Local modules

```python
# Standard library
import os
import sys
from typing import List, Optional

# Third-party
import boto3
from argparse import ArgumentParser, Namespace

# Local
from manager.commands.base import BaseCommand
from manager.core.logger import log_error, log_success
from manager.config import GO_FUNCTIONS
```

**Guidelines:**
- Use absolute imports: `from manager.core.logger import log_info`
- Group imports by category with blank lines
- Sort alphabetically within each group
- Avoid `import *` (always explicit imports)

### 4. Type Hints

**Required for all functions:**

```python
def execute(self, args: Namespace) -> bool:
    """Execute command logic"""
    functions: List[str] = self._resolve_function_list(args)
    return self._process_functions(functions)

def _get_filtered_functions(self, filter: Optional[str]) -> List[str]:
    """Get filtered function list"""
    if filter is None:
        return GO_FUNCTIONS
    return [filter] if filter in GO_FUNCTIONS else []
```

**Common types:**
- `List[str]`, `Dict[str, Any]`, `Optional[str]`
- `Namespace` (from argparse)
- `bool` for success/failure return values

### 5. Docstrings

**Use Google-style docstrings:**

```python
def build_function(self, func_name: str, output_dir: str) -> bool:
    """
    Build a single Go function to binary.

    Args:
        func_name: Name of the function to build
        output_dir: Directory to write the binary

    Returns:
        True if build succeeded, False otherwise

    Raises:
        FileNotFoundError: If main.go doesn't exist
    """
    pass
```

**Required for:**
- All public methods
- All classes (class-level docstring)
- Complex private methods (use judgment)

### 6. Naming Conventions

**Files:** `snake_case.py` (e.g., `list_functions.py`)  
**Classes:** `PascalCase` (e.g., `BuildCommand`, `BaseCommand`)  
**Functions/Variables:** `snake_case` (e.g., `build_function`, `func_name`)  
**Constants:** `UPPER_SNAKE_CASE` (e.g., `GO_FUNCTIONS`, `BIN_DIR`)  
**Private methods:** `_leading_underscore` (e.g., `_validate_function`)

### 7. Command Structure

**All commands inherit from `BaseCommand`:**

```python
from manager.commands.base import BaseCommand
from argparse import ArgumentParser, Namespace

class MyCommand(BaseCommand):
    """One-line description of command"""
    
    name = "mycommand"                    # CLI command name
    help = "Short help text"              # Shown in --help
    description = "Detailed description"  # Optional, defaults to help
    epilog = """Examples:
  manager.py mycommand -f status
"""
    
    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific CLI arguments"""
        parser.add_argument('-f', '--function', help='Function name')
    
    def execute(self, args: Namespace) -> bool:
        """
        Execute the command logic.
        
        Returns:
            True on success, False on failure
        """
        # Use base class helpers
        functions = self._resolve_function_list(args)
        
        # Your logic here
        for func in functions:
            self._process_function(func)
        
        return True
```

**Key patterns:**
- Commands are **auto-discovered** (no registration needed)
- Use `_resolve_function_list(args)` to support both CLI and dev menu
- Return `bool` for success/failure (affects exit code)
- Use `log_*` functions from `core/logger.py` for output

### 7.5. Interactive Menu Support

Commands can optionally support **interactive menu mode** by implementing `get_menu_tree()`:

```python
from manager.core.menu import MenuNode
from typing import Optional

class MyCommand(BaseCommand):
    """Command with interactive menu support"""
    
    name = "mycommand"
    help = "Short help text"
    
    def get_menu_tree(self) -> Optional[MenuNode]:
        """
        Define the interactive menu structure.
        
        Returns None if command doesn't support interactive mode.
        """
        return MenuNode(
            label="My Command",
            emoji="⚙️",
            children=[
                MenuNode(
                    label="Build All",
                    emoji="🔨",
                    action=lambda: self._build_all()
                ),
                MenuNode(
                    label="Build Specific",
                    emoji="🔨",
                    children=[
                        MenuNode(
                            label="status",
                            action=lambda: self._build_function("status")
                        ),
                        MenuNode(
                            label="getUsers",
                            action=lambda: self._build_function("getUsers")
                        ),
                    ]
                ),
            ]
        )
    
    def _build_all(self) -> bool:
        """Build all functions"""
        # Implementation
        return True
    
    def _build_function(self, func_name: str) -> bool:
        """Build specific function"""
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
- **Multi-select**: Use `fzf_select_functions()` for function selection

**Example: Build Command with Menu:**

```python
from manager.core.menu import MenuNode, fzf_select_functions

class BuildCommand(BaseCommand):
    name = "build"
    help = "Build Go functions"
    
    def get_menu_tree(self) -> Optional[MenuNode]:
        return MenuNode(
            label="Build",
            emoji="🔨",
            children=[
                MenuNode(
                    label="Build All Functions",
                    action=lambda: self._build_all()
                ),
                MenuNode(
                    label="Select Functions",
                    action=lambda: self._build_selected()
                ),
            ]
        )
    
    def _build_all(self) -> bool:
        """Build all functions"""
        functions = GO_FUNCTIONS
        return self._build_functions(functions)
    
    def _build_selected(self) -> bool:
        """Let user select functions to build"""
        functions = fzf_select_functions(
            prompt="Select functions to build: ",
            include_all=True
        )
        if not functions:
            return False
        return self._build_functions(functions)
    
    def _build_functions(self, functions: List[str]) -> bool:
        """Build specified functions"""
        # Implementation
        return True
```

### 8. Error Handling

**Fail gracefully with user-friendly messages:**

```python
from manager.core.logger import log_error, log_warning

# Validate input
if func_name not in GO_FUNCTIONS:
    log_error(f"Function '{func_name}' not found")
    log_info(f"Available: {', '.join(GO_FUNCTIONS[:5])}...")
    return False

# Handle subprocess errors
try:
    result = subprocess.run(command, check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    log_error(f"Build failed: {e.stderr.strip()}")
    return False
except FileNotFoundError:
    log_error("Go compiler not found. Install with: brew install go")
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
from manager.core.logger import (
    log_header,   # Major section header
    log_section,  # Subsection header
    log_success,  # Success message (green checkmark)
    log_error,    # Error message (red X)
    log_warning,  # Warning message (yellow !)
    log_info,     # Info message (cyan i)
    print_summary # Final statistics summary
)

# Example
log_section(f"BUILDING {len(functions)} FUNCTIONS")
for func in functions:
    log_info(f"Processing {func}")
    if build_success:
        log_success(f"{func} → {size:,} bytes", duration=1.2)
    else:
        log_error(f"{func} → compilation failed")
print_summary()
```

### 10. Configuration

**Never hardcode values.** Use `config.py`:

```python
from manager.config import (
    GO_FUNCTIONS,      # List of all functions
    BUILD_SETTINGS,    # Go build environment vars
    FUNCTIONS_DIR,     # "functions/"
    BIN_DIR,           # ".bin/"
    AWS_PROFILE,       # AWS profile name
)
```

**When adding new config:**
- Add to `config.py` with comments
- Use UPPER_SNAKE_CASE for constants
- Group related settings with section headers

---

## Common Patterns

### Function Resolution (CLI + Dev Mode)

```python
def execute(self, args: Namespace) -> bool:
    # This works for both CLI (-f flag) and dev menu (function_list)
    functions = self._resolve_function_list(args)
    if not functions:
        return False  # Error already logged
    
    for func in functions:
        self._process_function(func)
    return True
```

### Building with Stats

```python
from manager.core.stats import stats

stats.reset()
stats.total_functions = len(functions)

for func in functions:
    if success:
        stats.add_success()
    else:
        stats.add_failure(func)

print_summary()  # Prints stats automatically
```

### Subprocess Execution

```python
import subprocess

env = os.environ.copy()
env.update(BUILD_SETTINGS)  # Add Go build settings

result = subprocess.run(
    ["go", "build", "-o", output, source],
    check=True,           # Raise on error
    capture_output=True,  # Capture stdout/stderr
    text=True,            # Return strings (not bytes)
    env=env,              # Custom environment
    cwd=source_dir        # Working directory
)
```

### Interactive Menu Navigation

**How fzf integration works:**

```python
from manager.core.menu import MenuRenderer, MenuNode

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
1. User runs `python manager.py` (no args)
2. `cli.py:interactive_mode()` builds menu tree from all commands
3. `MenuRenderer.show()` handles navigation with fzf
4. When user selects a leaf node, its `action()` is called
5. After action completes, menu returns to parent
6. User can navigate back with "← Back" or ESC

**Keyboard Shortcuts in fzf:**
- `↑/↓`: Navigate
- `TAB`: Multi-select (if enabled)
- `ENTER`: Confirm
- `ESC`: Cancel/Go back
- `Ctrl+C`: Exit (exit code 130)

---

## Best Practices

1. **Read before writing:** If modifying a command, read similar commands first
2. **Validate inputs:** Check function names exist, files exist, etc.
3. **Atomic operations:** Each command should do ONE thing well
4. **Interactive support:** Commands should work in both CLI and dev menu
5. **Cross-platform:** Use `os.path.join()`, not hardcoded slashes
6. **Progress feedback:** Log each step (especially in long operations)
7. **Clean state:** Don't leave artifacts on failure
8. **Documentation:** Update README.md when adding new features

---

## Notes for AI Agents

- **No tests exist yet:** When writing tests, use pytest with fixtures
- **Auto-discovery:** New commands are auto-registered (no imports needed)
- **Base class helpers:** Use `_resolve_function_list()` and `_get_filtered_functions()`
- **Interactive menus:** Implement `get_menu_tree()` to add interactive support
- **Menu system:** Uses `MenuNode` (tree structure) + `MenuRenderer` (fzf navigation)
- **Function selection:** Use `fzf_select_functions()` for multi-select in menus
- **Colors/Emojis:** Already handled by logger utilities
- **AWS integration:** Uses `serverless` CLI and `aws` CLI (not boto3)
- **Go functions:** Expected at `functions/<name>/main.go`
- **Output directory:** Binaries go to `.bin/<name>/bootstrap`

---

**Last Updated:** 2026-01-14 (Interactive Menu System)  
**Python Version:** 3.8+  
**Primary Maintainer:** @ncasatti
