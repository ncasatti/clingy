# manager-core

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Type-Framework-purple.svg)](#)

> Context-aware CLI framework with fuzzy search menus and auto-discovery

A flexible, production-ready framework for creating command-line interfaces with:
- **Context detection** - Automatically finds and loads project configuration
- **Interactive menus** powered by `fzf` (fuzzy finder)
- **Auto-discovery** command system (no registration needed)
- **Project templates** - Initialize new projects with `manager init`
- **Type-safe** Python 3.8+ with full type hints
- **Extensible** architecture for any use case

---

## What is This?

**manager-core** is a CLI framework that works like Git, Poetry, or Terraform:
- Install once globally: `pip install manager-core`
- Initialize projects: `manager init`
- Run from anywhere: `manager` automatically detects your project

### Why Use This Framework?

- ✅ **No boilerplate**: `manager init` creates a working project
- ✅ **Context-aware**: Works from any subdirectory (like Git)
- ✅ **Interactive by default**: Users get fuzzy search menus automatically
- ✅ **Modular design**: Add commands without touching core code
- ✅ **Production-ready**: Error handling, logging, and validation included

---

## Quick Start

### Installation

```bash
# Install framework globally
pip install manager-core

# Or install from source
git clone <this-repo>
cd manager
pip install -e .
```

### Create Your First Project

```bash
# Create a new directory for your project
mkdir my-cli-tool
cd my-cli-tool

# Initialize project
manager init

# Run interactive menu
manager

# Or use CLI mode
manager greet --language es
manager info
```

### Project Structure

After `manager init`, you'll have:

```
my-cli-tool/
├── commands/           # Your custom commands
│   ├── __init__.py
│   ├── greet.py       # Example: simple menu
│   ├── info.py        # Example: CLI-only
│   └── calculator.py  # Example: interactive input
└── config.py          # Project configuration
```

---

## Usage

### Interactive Mode (Recommended)

```bash
# Run from project directory (or any subdirectory)
manager
```

This opens a fuzzy-searchable menu with all available commands.

### CLI Mode

```bash
# Run specific commands
manager greet --language es
manager info
manager calculator

# Get help
manager --help
manager greet --help
```

---

## Creating Commands

### Simple Command

Create `commands/hello.py`:

```python
from argparse import ArgumentParser, Namespace
from manager_core.commands.base import BaseCommand
from manager_core.core.emojis import Emojis
from manager_core.core.logger import log_success
from manager_core.core.menu import MenuNode

class HelloCommand(BaseCommand):
    name = "hello"
    help = "Say hello"
    
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--name", default="World")
    
    def execute(self, args: Namespace) -> bool:
        log_success(f"Hello, {args.name}!")
        return True
    
    def get_menu_tree(self) -> MenuNode:
        return MenuNode(
            label="Say Hello",
            emoji=Emojis.GREET,
            action=lambda: self.execute(Namespace(name="World"))
        )
```

That's it! The command is automatically discovered and added to the menu.

### Hierarchical Menu

```python
def get_menu_tree(self) -> MenuNode:
    return MenuNode(
        label="Process",
        emoji="🔄",
        children=[
            MenuNode(
                label="Process All",
                action=lambda: self._process_all()
            ),
            MenuNode(
                label="Process Specific",
                children=[
                    MenuNode(label="Item 1", action=lambda: self._process("item-1")),
                    MenuNode(label="Item 2", action=lambda: self._process("item-2")),
                ]
            ),
        ]
    )
```

---

## Configuration

Edit `config.py` to customize your project:

```python
# Project metadata
PROJECT_NAME = "My CLI Tool"
PROJECT_VERSION = "1.0.0"

# Items your CLI manages
ITEMS = [
    "example-item-1",
    "example-item-2",
    "example-item-3",
]

# Paths
DATA_DIR = "data"
OUTPUT_DIR = "output"

# Dependencies
DEPENDENCIES = [
    Dependency(
        name="fzf",
        command="fzf",
        description="Fuzzy finder for interactive menus",
        install_macos="brew install fzf",
        install_linux="sudo pacman -S fzf",
        required=True,
    ),
]
```

---

## How It Works

### Context Detection

When you run `manager`, the framework:
1. Searches upward from current directory for `commands/` and `config.py`
2. Loads project configuration dynamically
3. Discovers commands from project's `commands/` directory
4. Merges with framework commands (like `init`)

This means you can run `manager` from any subdirectory of your project, just like Git.

### Command Discovery

Commands are auto-discovered by:
1. Scanning `commands/*.py` files
2. Finding classes that inherit from `BaseCommand`
3. Registering them by their `name` attribute

No imports or registration needed!

---

## Examples

See the template commands created by `manager init`:
- **greet.py** - Simple menu with language selection
- **info.py** - CLI-only command (no interactive menu)
- **calculator.py** - Interactive input with user prompts

---

## Development

### Project Structure

```
manager-core/
├── manager_core/           # Framework code
│   ├── commands/           # Framework commands
│   │   ├── base.py        # Abstract base class
│   │   └── init.py        # Project initialization
│   ├── core/              # Core utilities
│   │   ├── discovery.py   # Context detection
│   │   ├── menu.py        # Interactive menu system
│   │   ├── logger.py      # Logging utilities
│   │   └── colors.py      # Terminal styling
│   ├── templates/         # Project templates
│   │   └── basic/         # Default template
│   ├── cli.py             # CLI entry point
│   ├── cli_builder.py     # Context builder
│   └── config.py          # Framework config
├── pyproject.toml         # Package metadata
└── README.md
```

### Running Tests

```bash
# Create test project
cd /tmp
mkdir test-manager
cd test-manager

# Initialize and test
python -m manager_core.cli init
python -m manager_core.cli
python -m manager_core.cli greet --language es
```

---

## Requirements

- **Python 3.8+**
- **fzf** (for interactive menus)
  - macOS: `brew install fzf`
  - Linux: `sudo pacman -S fzf` (Arch) or `sudo apt install fzf` (Debian/Ubuntu)

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Contributing

This is a template/framework project. Feel free to:
- Fork and customize for your needs
- Submit PRs for framework improvements
- Share your use cases!

---

**Last Updated:** 2026-01-26 (manager-core refactor)  
**Python Version:** 3.8+  
**Primary Maintainer:** @ncasatti
