# clingy

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Context-aware CLI framework** for building interactive command-line tools with fuzzy search menus and modular command architecture. Works like Git, Poetry, or Terraform—install once, use everywhere.

---

## Showcase



---

## Features

- ✅ **Context-Aware** — Automatically finds project root by searching for `.clingy` or `commands/`.
- ✅ **Interactive Menus** — Powered by `fzf` for fast, fuzzy-searchable navigation.
- ✅ **Auto-Discovery** — Commands are automatically registered—no manual imports needed.
- ✅ **Modular** — Build complex CLIs by composing simple, reusable command classes.
- ✅ **Rich Logging** — Built-in utilities for success/error/warning messages with stats.
- ✅ **Template System** — Start with pre-built templates: `basic`, `konfig`, `serverless`.
- ✅ **Dependency Management** — Automatic checking and installation guidance for required tools.

---

## Installation

```bash
# Using uv (recommended)
uv pip install clingy

# Using pip
pip install clingy
```

**Required Dependency:** `fzf` (fuzzy finder). Install via your package manager (`brew`, `apt`, `pacman`, etc.).

---

## Quick Start

### 1. Initialize
```bash
mkdir my-tool && cd my-tool
clingy init
```

### 2. Run
```bash
clingy                # Interactive mode (fzf menu)
clingy greet --name User  # CLI mode
```

### 3. Update Framework
If a template update is available, sync your project files while preserving your configuration:
```bash
clingy --update-template
```

---

## Templates

| Template | Description | Initialize |
|---|---|---|
| **basic** | Simple CLI for prototyping and learning. | `clingy init --template basic` |
| **konfig** | Dotfiles and symlink manager for Linux. | `clingy init --template konfig` |
| **serverless** | AWS Lambda + Go manager with full workflow. | `clingy init --template serverless` |

---

## Development

### Creating a Command
Inherit from `BaseCommand` and implement `execute` and `get_menu_tree`:

```python
from clingy.commands.base import BaseCommand
from clingy.core.menu import MenuNode

class MyCommand(BaseCommand):
    name = "mycmd"
    help = "Description"

    def execute(self, args):
        print("Executing...")
        return True

    def get_menu_tree(self):
        return MenuNode(label="My Command", action=lambda: self.execute(None))
```

### Logging & Stats
```python
from clingy.core.logger import log_success, log_error, print_summary
from clingy.core.stats import stats

log_success("Operation complete", duration=1.5)
stats.add_success()
print_summary()
```

---

## Configuration (`config.py`)
```python
PROJECT_NAME = "My Tool"
PROJECT_VERSION = "1.0.0"
ITEMS = ["item1", "item2"]
DEPENDENCIES = []
```

---

## Contributing & Testing

```bash
# Install in editable mode
pip install -e .

# Run tests
pytest tests/

# Format code
black . --line-length 100
isort . --profile black
```

---

## Acknowledgments

**Inspired by:**
- [Git](https://git-scm.com/) — Context detection and command discovery
- [Poetry](https://python-poetry.org/) — Elegant CLI design
- [Terraform](https://www.terraform.io/) — Modular architecture
- [fzf](https://github.com/junegunn/fzf) — Fuzzy finder magic

**Built with:**
- Python 3.8+
- [argparse](https://docs.python.org/3/library/argparse.html) — CLI argument parsing
- [fzf](https://github.com/junegunn/fzf) — Interactive menu system

**License:** [MIT](LICENSE)
**Maintainer:** [@ncasatti](https://github.com/ncasatti)
