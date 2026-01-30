# Basic Template

Simple CLI template for learning clingy and building quick utilities.

## Overview

The basic template includes example commands to demonstrate core framework features:
- **Greet** - Multilingual greeting command
- **Info** - System information display
- **Calculator** - Interactive calculator
- **Files** - File operations menu (create, list, delete)

Perfect for learning the framework or building simple utility scripts.

---

## Quick Start

### 1. Initialize Project

```bash
mkdir my-cli-tool
cd my-cli-tool
clingy init --template basic
```

### 2. Run Interactive Menu

```bash
clingy
```

Navigate with arrow keys, search with fuzzy find, select with ENTER.

### 3. Run CLI Mode

```bash
clingy greet --language es
# Output: ¡Hola! 👋

clingy info
# Output: System information

clingy calculator
# Output: Interactive calculator menu
```

---

## Included Commands

### Greet Command

Greet users in different languages with emoji support.

**Interactive Menu:**
```
Greet
├── Spanish (¡Hola!)
├── English (Hello!)
├── French (Bonjour!)
└── German (Guten Tag!)
```

**CLI Usage:**
```bash
clingy greet --language es
clingy greet --language en
clingy greet --language fr
clingy greet --language de
```

---

### Info Command

Display system information (Python version, OS, working directory).

**Interactive Menu:**
```
Info
└── Show System Info
```

**CLI Usage:**
```bash
clingy info
```

**Output Example:**
```
System Information
==================
Python Version: 3.11.5
Operating System: Linux
Current Directory: /home/user/my-project
```

---

### Calculator Command

Interactive calculator with basic operations.

**Interactive Menu:**
```
Calculator
├── Addition
├── Subtraction
├── Multiplication
└── Division
```

**Workflow:**
1. Select operation
2. Enter first number
3. Enter second number
4. See result

---

### Files Command

File operations with hierarchical menu structure.

**Interactive Menu:**
```
Files
├── List Files
├── Create File
└── Delete File
```

**Features:**
- List files in current directory
- Create new files with custom content
- Delete files with confirmation

---

## Project Structure

```
my-cli-tool/
├── commands/
│   ├── __init__.py
│   ├── greet.py          # Multilingual greeting
│   ├── info.py           # System information
│   ├── calculator.py     # Interactive calculator
│   └── files.py          # File operations
│
├── config.py             # Project configuration
├── .clingy               # Project marker (for context detection)
└── README.md             # This file
```

---

## Customizing

### Update Project Metadata

Edit `config.py`:

```python
PROJECT_NAME = "My CLI Tool"
PROJECT_VERSION = "1.0.0"

# Define items to manage (optional)
ITEMS = [
    "item-1",
    "item-2",
    "item-3",
]
```

### Add Your Own Commands

Create a new file in `commands/`:

```python
# commands/mycommand.py
from clingy.commands.base import BaseCommand
from argparse import ArgumentParser, Namespace
from clingy.core.menu import MenuNode
from clingy.core.logger import log_success

class MyCommand(BaseCommand):
    """My custom command"""
    
    name = "mycommand"
    help = "My custom command"
    
    def execute(self, args: Namespace) -> bool:
        log_success("Hello from my command!")
        return True
    
    def get_menu_tree(self) -> MenuNode:
        return MenuNode(
            label="My Command",
            emoji="⚙️",
            action=lambda: self.execute(Namespace())
        )
```

**No registration needed** - commands are auto-discovered!

---

## Next Steps

### Learn More

- **[Creating Commands](../../docs/commands.md)** - Detailed command development guide
- **[Architecture](../../docs/architecture.md)** - How the framework works
- **[Main README](../../README.md)** - Framework overview

### Try Other Templates

- **[Konfig Template](../konfig/README.md)** - Dotfiles and symlink manager
- **[Serverless Template](../serverless/README.md)** - AWS Lambda + Go manager

### Contribute

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

---

## Example: Building a Task Manager

```python
# commands/tasks.py
from clingy.commands.base import BaseCommand
from clingy.core.menu import MenuNode, fzf_select_items
from clingy.core.logger import log_success, log_info
from argparse import Namespace
from typing import List

class TasksCommand(BaseCommand):
    """Task management command"""
    
    name = "tasks"
    help = "Manage tasks"
    
    def __init__(self):
        super().__init__()
        self.tasks: List[str] = []
    
    def execute(self, args: Namespace) -> bool:
        if hasattr(args, 'action'):
            if args.action == 'add':
                task = input("Enter task: ")
                self.tasks.append(task)
                log_success(f"Added: {task}")
            elif args.action == 'list':
                for i, task in enumerate(self.tasks, 1):
                    log_info(f"{i}. {task}")
        return True
    
    def get_menu_tree(self) -> MenuNode:
        return MenuNode(
            label="Tasks",
            emoji="📝",
            children=[
                MenuNode(
                    label="Add Task",
                    action=lambda: self._add_task()
                ),
                MenuNode(
                    label="List Tasks",
                    action=lambda: self._list_tasks()
                ),
                MenuNode(
                    label="Remove Task",
                    action=lambda: self._remove_task()
                ),
            ]
        )
    
    def _add_task(self) -> bool:
        task = input("Enter task: ")
        self.tasks.append(task)
        log_success(f"Added: {task}")
        return True
    
    def _list_tasks(self) -> bool:
        if not self.tasks:
            log_info("No tasks yet")
            return True
        for i, task in enumerate(self.tasks, 1):
            log_info(f"{i}. {task}")
        return True
    
    def _remove_task(self) -> bool:
        if not self.tasks:
            log_info("No tasks to remove")
            return False
        
        selected = fzf_select_items(
            items=self.tasks,
            prompt="Select task to remove: "
        )
        if selected:
            self.tasks.remove(selected[0])
            log_success(f"Removed: {selected[0]}")
        return True
```

Run it:
```bash
clingy tasks
# → Interactive menu appears
```

---

## Tips

1. **Start Simple** - Begin with a single command and add complexity gradually
2. **Use Loggers** - Never use `print()`, always use `log_*` functions
3. **Type Hints** - Add type hints to all functions for better IDE support
4. **Return Booleans** - Commands should return `True` on success, `False` on failure
5. **Test Both Modes** - Verify your commands work in both CLI and interactive modes

---

## Troubleshooting

### "No clingy project found"

**Solution:**
```bash
# Make sure you initialized the project
clingy init --template basic

# Or check you're in the project directory
cd /path/to/my-cli-tool
clingy
```

### "Command not showing in menu"

**Checklist:**
- ✅ File is in `commands/` directory
- ✅ Class inherits from `BaseCommand`
- ✅ `get_menu_tree()` is implemented
- ✅ File name doesn't start with `_`

### "fzf not found"

**Solution:**
```bash
# macOS
brew install fzf

# Ubuntu/Debian
sudo apt-get install fzf

# Arch
sudo pacman -S fzf
```

---

## License

MIT
