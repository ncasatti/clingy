# Creating Commands

This guide shows you how to create custom commands for your clingy project.

## Table of Contents

- [Command Structure](#command-structure)
- [Basic Command](#basic-command)
- [Command with Submenus](#command-with-submenus)
- [Command with Multi-Select](#command-with-multi-select)
- [MenuNode API](#menunode-api)
- [Helper Functions](#helper-functions)
- [Best Practices](#best-practices)

## Command Structure

All commands inherit from `BaseCommand` and are automatically discovered.

### Required Components

| Component | Required | Purpose |
|-----------|----------|---------|
| `name` | ✅ | CLI command name (e.g., `clingy greet`) |
| `help` | ✅ | Short help text for `--help` |
| `execute()` | ✅ | Main command logic, returns `bool` |
| `get_menu_tree()` | ✅ | Interactive menu structure (required) |
| `description` | ❌ | Detailed description (defaults to `help`) |
| `add_arguments()` | ❌ | CLI argument definitions |

---

## Basic Command

```python
from clingy.commands.base import BaseCommand
from argparse import ArgumentParser, Namespace
from clingy.core.menu import MenuNode
from clingy.core.logger import log_success, log_error

class GreetCommand(BaseCommand):
    """Greet users in different languages"""
    
    name = "greet"
    help = "Greet in different languages"
    description = "Greet users with multilingual support"
    
    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific arguments"""
        parser.add_argument(
            '--language',
            choices=['en', 'es', 'fr'],
            default='en',
            help='Language for greeting'
        )
    
    def execute(self, args: Namespace) -> bool:
        """Execute the command"""
        greetings = {
            'en': 'Hello! 👋',
            'es': '¡Hola! 👋',
            'fr': 'Bonjour! 👋',
        }
        
        message = greetings.get(args.language, greetings['en'])
        log_success(message)
        return True
    
    def get_menu_tree(self) -> MenuNode:
        """Define interactive menu structure"""
        return MenuNode(
            label="Greet",
            emoji="👋",
            children=[
                MenuNode(
                    label="English",
                    action=lambda: self._greet('en')
                ),
                MenuNode(
                    label="Spanish",
                    action=lambda: self._greet('es')
                ),
                MenuNode(
                    label="French",
                    action=lambda: self._greet('fr')
                ),
            ]
        )
    
    def _greet(self, language: str) -> bool:
        """Greet in specified language"""
        args = Namespace(language=language)
        return self.execute(args)
```

---

## Command with Submenus

```python
from clingy.core.menu import MenuNode, fzf_select_items
from clingy.config import ITEMS

class ProcessCommand(BaseCommand):
    """Process items with hierarchical menu"""
    
    name = "process"
    help = "Process items"
    
    def execute(self, args: Namespace) -> bool:
        items = self._resolve_item_list(args)
        if not items:
            return False
        
        for item in items:
            log_success(f"Processed {item}")
        return True
    
    def get_menu_tree(self) -> MenuNode:
        """Create hierarchical menu with item selection"""
        return MenuNode(
            label="Process",
            emoji="🔄",
            children=[
                MenuNode(
                    label="Process All Items",
                    action=lambda: self.execute(Namespace(item_list=ITEMS))
                ),
                MenuNode(
                    label="Select Items",
                    action=lambda: self._process_selected()
                ),
                MenuNode(
                    label="Process by Category",
                    emoji="📂",
                    children=[
                        MenuNode(
                            label="Category A",
                            action=lambda: self._process_category('a')
                        ),
                        MenuNode(
                            label="Category B",
                            action=lambda: self._process_category('b')
                        ),
                    ]
                ),
            ]
        )
    
    def _process_selected(self) -> bool:
        """Let user select items interactively"""
        items = fzf_select_items(
            prompt="Select items to process: ",
            include_all=True
        )
        if not items:
            return False
        return self.execute(Namespace(item_list=items))
    
    def _process_category(self, category: str) -> bool:
        """Process items in a category"""
        filtered = [item for item in ITEMS if item.startswith(category)]
        return self.execute(Namespace(item_list=filtered))
```

---

## Command with Multi-Select

```python
from clingy.core.menu import fzf_select_items

class DeployCommand(BaseCommand):
    """Deploy with multi-select support"""
    
    name = "deploy"
    help = "Deploy services"
    
    def execute(self, args: Namespace) -> bool:
        services = self._resolve_item_list(args)
        if not services:
            return False
        
        for service in services:
            log_info(f"Deploying {service}...")
            # Deployment logic
            log_success(f"Deployed {service}")
        
        return True
    
    def get_menu_tree(self) -> MenuNode:
        return MenuNode(
            label="Deploy",
            emoji="🚀",
            children=[
                MenuNode(
                    label="Deploy All",
                    action=lambda: self.execute(Namespace(item_list=ITEMS))
                ),
                MenuNode(
                    label="Deploy Selected",
                    action=lambda: self._deploy_selected()
                ),
            ]
        )
    
    def _deploy_selected(self) -> bool:
        """Multi-select deployment"""
        services = fzf_select_items(
            prompt="Select services to deploy: ",
            include_all=False,
            multi_select=True
        )
        if not services:
            return False
        return self.execute(Namespace(item_list=services))
```

---

## MenuNode API

```python
from clingy.core.menu import MenuNode
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass

@dataclass
class MenuNode:
    label: str                              # Display text
    emoji: str = ""                         # Optional emoji prefix
    children: List[MenuNode] = []           # Submenu items
    action: Optional[Callable[[], bool]] = None  # Function to execute
    data: Dict[str, Any] = {}               # Extra context data
    
    def is_leaf(self) -> bool:              # True if executable
    def is_submenu(self) -> bool:           # True if has children
    def display_label(self) -> str:         # Formatted label for fzf
```

**Key Points:**
- **Leaf nodes**: Have `action`, no `children` (executable)
- **Submenu nodes**: Have `children`, no `action` (navigable)
- **Emojis**: Automatically prefixed to labels
- **Navigation**: fzf handles breadcrumbs and "← Back"

---

## Helper Functions

### fzf Selection

```python
from clingy.core.menu import fzf_select_items

# Single selection
item = fzf_select_items(
    prompt="Select an item: ",
    include_all=False
)[0]

# Multi-select
items = fzf_select_items(
    prompt="Select items: ",
    include_all=True,      # Show "All" option
    multi_select=True      # Allow multiple selections
)

# With custom items
items = fzf_select_items(
    items=["option-1", "option-2", "option-3"],
    prompt="Select: ",
    include_all=True
)
```

### BaseCommand Helpers

```python
from clingy.commands.base import BaseCommand

class MyCommand(BaseCommand):
    def execute(self, args: Namespace) -> bool:
        # Resolve items from CLI (-i flag) or interactive menu
        items = self._resolve_item_list(args)
        
        # Get filtered items
        filtered = self._get_filtered_items(filter_name)
        
        # Both return List[str] or empty list on error
        return True
```

---

## Best Practices

### 1. Return Booleans
Commands should return `True` on success, `False` on failure:
```python
def execute(self, args: Namespace) -> bool:
    try:
        # Your logic
        return True
    except Exception as e:
        log_error(f"Failed: {e}")
        return False
```

### 2. Use Logger Functions
Never use `print()` directly:
```python
from clingy.core.logger import log_success, log_error, log_info, log_warning

log_success("Operation completed")
log_error("Something failed")
log_info("Processing...")
log_warning("Deprecated feature")
```

### 3. Support Both CLI and Interactive
Use `_resolve_item_list()` to work in both modes:
```python
def execute(self, args: Namespace) -> bool:
    items = self._resolve_item_list(args)  # Works for CLI and menu
    for item in items:
        process(item)
    return True
```

### 4. Add Type Hints
Always use type hints:
```python
def execute(self, args: Namespace) -> bool:
    items: List[str] = self._resolve_item_list(args)
    return self._process_items(items)

def _process_items(self, items: List[str]) -> bool:
    # ...
```

### 5. Write Docstrings
Use Google-style docstrings:
```python
def execute(self, args: Namespace) -> bool:
    """
    Execute the command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        True if successful, False otherwise
    """
```

### 6. Handle Errors Gracefully
```python
from clingy.core.logger import log_error

def execute(self, args: Namespace) -> bool:
    if not validate_input(args):
        log_error("Invalid input")
        return False
    
    try:
        result = risky_operation()
    except FileNotFoundError:
        log_error("File not found")
        return False
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        return False
    
    return True
```

### 7. Use Stats Tracking
```python
from clingy.core.stats import stats
from clingy.core.logger import print_summary

def execute(self, args: Namespace) -> bool:
    stats.reset()
    stats.total_items = len(items)
    
    for item in items:
        try:
            process(item)
            stats.add_success()
        except Exception as e:
            stats.add_failure(item)
            log_error(f"{item}: {e}")
    
    print_summary()
    return stats.success_count > 0
```

---

## See Also

- [Architecture](architecture.md) - Framework internals
- [Main README](../README.md) - Project overview
- [CONTRIBUTING](../CONTRIBUTING.md) - Contribution guidelines
