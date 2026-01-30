# clingy

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Framework](https://img.shields.io/badge/Type-Framework-purple.svg)](#)

> A context-aware CLI framework for building interactive command-line tools with fuzzy search menus and modular command architecture. Works like Git, Poetry, or Terraform—install once, use everywhere.

<!-- TODO: Add demo GIF showing interactive menu navigation -->

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Templates](#templates)
- [Logging & Output](#logging--output)
- [Configuration](#configuration)
- [Development](#development)
- [Examples & Use Cases](#examples--use-cases)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

✅ **Context-Aware Detection** — Automatically finds your project (like Git) by searching for `commands/` and `config.py` up the directory tree

✅ **Interactive Menus** — Powered by `fzf` for fast, fuzzy-searchable navigation with breadcrumb support

✅ **Auto-Discovery** — Commands are automatically discovered and registered—no manual imports needed

✅ **Modular Architecture** — Build complex CLIs by composing simple, reusable commands

✅ **Rich Logging** — Built-in utilities for success/error/warning messages with timestamps and statistics

✅ **Template System** — Start with pre-built templates: `basic`, `konfig` (dotfiles), `serverless` (AWS Lambda)

✅ **Type-Safe** — Full type hints and Google-style docstrings throughout

✅ **Dependency Management** — Automatic checking and installation guidance for required tools

✅ **Stats Tracking** — Built-in success/failure counters with summary reports

✅ **Cross-Platform** — Works on macOS, Linux, and Windows (with WSL)

---

## Installation

### From PyPI (Recommended)

```bash
pip install clingy
```

### From Source

```bash
git clone https://github.com/ncasatti/clingy.git
cd clingy
pip install -e .
```

### Verify Installation

```bash
clingy --version
```

### Dependencies

**Required:**
- Python 3.8+
- `fzf` (fuzzy finder) — [Install guide](https://github.com/junegunn/fzf#installation)

**Installation by OS:**

```bash
# macOS
brew install fzf

# Ubuntu/Debian
sudo apt-get install fzf

# Fedora
sudo dnf install fzf

# Arch
sudo pacman -S fzf
```

---

## Quick Start

### 1. Initialize a New Project

```bash
mkdir my-cli-tool
cd my-cli-tool
clingy init
```

This creates a project structure:

```
my-cli-tool/
├── commands/
│   ├── __init__.py
│   └── greet.py          # Example command
├── config.py             # Project configuration
├── .clingy               # Project marker (for context detection)
└── README.md
```

### 2. Run Interactive Mode

```bash
clingy
```

This launches an interactive menu where you can:
- Navigate with arrow keys (↑/↓)
- Search with fuzzy find (type to filter)
- Select with ENTER
- Go back with ESC or "← Back"

### 3. Run CLI Mode

```bash
clingy greet --language es
```

### 4. Create Your First Command

See [Creating Commands](docs/commands.md) for detailed guide.

---

## Documentation

**Guides:**
- [Creating Commands](docs/commands.md) - Build custom commands
- [Architecture](docs/architecture.md) - How clingy works

**Templates:**
- [Basic Template](clingy/templates/basic/README.md) - Simple CLI
- [Konfig Template](clingy/templates/konfig/README.md) - Dotfiles manager
- [Serverless Template](clingy/templates/serverless/README.md) - AWS Lambda manager

**Contributing:**
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [AGENTS.md](AGENTS.md) - AI agent guidelines

---

## Templates

clingy comes with three production-ready templates. Each includes complete documentation, example commands, and best practices.

### 🎓 [Basic Template](clingy/templates/basic/README.md)

Simple CLI for learning and prototyping.

**Includes:**
- Multilingual greeting command
- System information display
- Interactive calculator
- File operations menu

**Best for:**
- Learning the framework
- Quick utility scripts
- Proof of concepts

**Initialize:**
```bash
clingy init --template basic
```

---

### 🔗 [Konfig Template](clingy/templates/konfig/README.md)

Dotfiles and symlink manager for Linux configurations.

**Features:**
- Manage symlinks for dotfiles (`.bashrc`, `.vimrc`, `.config/`, etc.)
- Status tracking (linked, unlinked, broken)
- Sync configurations across machines
- Interactive browsing with quick actions

**Best for:**
- Managing dotfiles across machines
- Synchronizing Linux configurations
- System config backups

**Initialize:**
```bash
clingy init --template konfig
```

---

### ☁️ [Serverless Template](clingy/templates/serverless/README.md)

AWS Lambda + Go manager with full serverless workflow.

**Features:**
- Build, deploy, invoke Lambda functions (local & remote)
- CloudWatch Logs (view, tail, filter) & Insights queries
- **Interactive Payload Builder** - Compose payloads from reusable snippets
- Full pipeline (Build → Zip → Deploy)
- Status & monitoring dashboard

**Best for:**
- AWS Lambda development
- Serverless applications
- Multi-function deployments

**Initialize:**
```bash
clingy init --template serverless
```

---

📖 **Each template includes:**
- Complete README with setup instructions
- Example commands demonstrating best practices
- Configuration guide
- Troubleshooting section

👉 **Get started:** `clingy init --template <name>`

---

## Logging & Output

### Logger Functions

```python
from clingy.core.logger import (
    log_header,    # Major section header
    log_section,   # Subsection header
    log_success,   # Success message (green ✓)
    log_error,     # Error message (red ✗)
    log_warning,   # Warning message (yellow !)
    log_info,      # Info message (cyan ℹ)
    print_summary  # Final statistics summary
)

# Example usage
log_header("DEPLOYMENT STARTED")
log_section("Building services")

for service in services:
    log_info(f"Building {service}...")
    if build_success:
        log_success(f"{service} → built", duration=1.2)
    else:
        log_error(f"{service} → failed")

log_warning("Some services skipped")
print_summary()  # Shows stats: ✓ 5 | ✗ 1 | ⏭ 2
```

### Stats Tracking

```python
from clingy.core.stats import stats
from clingy.core.logger import print_summary

stats.reset()
stats.total_items = len(items)

for item in items:
    try:
        process_item(item)
        stats.add_success()
    except Exception as e:
        stats.add_failure(item)
        log_error(f"{item} → {str(e)}")

print_summary()
# Output:
# ✓ 8 succeeded | ✗ 2 failed | Success rate: 80%
```

### Output Examples

```python
# Header
log_header("PROCESSING ITEMS")
# Output: ╔════════════════════════════════════════╗
#         ║     PROCESSING ITEMS                   ║
#         ╚════════════════════════════════════════╝

# Section
log_section("Building Docker images")
# Output: ▶ Building Docker images

# Success with duration
log_success("Image built", duration=2.5)
# Output: ✓ Image built (2.5s)

# Error
log_error("Build failed: Out of disk space")
# Output: ✗ Build failed: Out of disk space

# Warning
log_warning("Using cached version (may be outdated)")
# Output: ⚠ Using cached version (may be outdated)

# Info
log_info("Downloading dependencies...")
# Output: ℹ Downloading dependencies...
```

---

## Configuration

### config.py Structure

```python
from clingy.core.dependency import Dependency

# Project metadata
PROJECT_NAME = "My CLI Tool"
PROJECT_VERSION = "1.0.0"

# Items to manage (can be anything: services, files, functions, etc.)
ITEMS = [
    "service-1",
    "service-2",
    "service-3",
]

# Directories
DATA_DIR = "data"
OUTPUT_DIR = "output"

# Dependencies (tools required by your commands)
DEPENDENCIES = [
    Dependency(
        name="Docker",
        command="docker",
        required=True,
        install_macos="brew install docker",
        install_linux="sudo apt-get install docker.io",
        install_windows="choco install docker"
    ),
    Dependency(
        name="AWS CLI",
        command="aws",
        required=False,  # Optional dependency
        install_macos="brew install awscli",
        install_linux="pip install awscli",
    ),
]
```

### Dependency Objects

```python
from clingy.core.dependency import Dependency

# Required dependency
Dependency(
    name="fzf",                    # Display name
    command="fzf",                 # Command to check (via `which`)
    required=True,                 # Fail if missing
    install_macos="brew install fzf",
    install_linux="sudo apt-get install fzf",
    install_windows="choco install fzf"
)

# Optional dependency
Dependency(
    name="AWS CLI",
    command="aws",
    required=False,                # Warn if missing, don't fail
    install_macos="brew install awscli",
    install_linux="pip install awscli",
)
```

### Accessing Configuration

```python
from clingy.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    ITEMS,
    DATA_DIR,
    OUTPUT_DIR,
    DEPENDENCIES,
)

# Use in your commands
for item in ITEMS:
    process_item(item)

output_file = os.path.join(OUTPUT_DIR, f"{item}.json")
```

---

## Development

### Clone and Setup

```bash
git clone https://github.com/ncasatti/clingy.git
cd clingy

# Install in editable mode
pip install -e .

# Verify installation
clingy --version
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_commands.py

# Run with verbose output
pytest -v

# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb
```

**Note:** Test suite is currently minimal. Contributions welcome!

### Code Style

The project uses **Black** with line-length 100:

```bash
# Format code
black . --line-length 100

# Check without modifying
black . --check --line-length 100

# Format specific directory
black clingy/ --line-length 100
```

### Type Checking (Optional)

```bash
# Install mypy
pip install mypy

# Run type checker
mypy . --strict
```

### Import Sorting (Optional)

```bash
# Install isort
pip install isort

# Sort imports
isort . --profile black
```

---

## Examples & Use Cases

### DevOps Tools

Manage infrastructure, deployments, and monitoring:

```bash
clingy deploy --service api
clingy logs --function my-lambda --tail
clingy status --all
```

### System Configuration

Manage dotfiles, symlinks, and system settings:

```bash
clingy link --file ~/.bashrc
clingy sync --all
clingy status
```

### Data Pipelines

Orchestrate data processing workflows:

```bash
clingy extract --source database
clingy transform --pipeline etl-v2
clingy load --destination warehouse
```

### Development Utilities

Build custom tools for your team:

```bash
clingy scaffold --template service
clingy test --coverage
clingy lint --fix
```

### Admin Dashboards

Create interactive admin interfaces:

```bash
clingy users --list
clingy users --create --email user@example.com
clingy audit --date 2024-01-01
```

---

## Troubleshooting

### "No clingy project found"

**Problem:** You're not in a clingy project directory.

**Solution:**
```bash
# Initialize a new project
clingy init

# Or navigate to an existing project
cd /path/to/my-project
clingy
```

### "fzf not found"

**Problem:** The `fzf` tool is not installed.

**Solution:**
```bash
# macOS
brew install fzf

# Ubuntu/Debian
sudo apt-get install fzf

# Fedora
sudo dnf install fzf

# Arch
sudo pacman -S fzf
```

### "ModuleNotFoundError: No module named 'clingy'"

**Problem:** The framework is not installed.

**Solution:**
```bash
# Install from PyPI
pip install clingy

# Or install from source in editable mode
git clone https://github.com/ncasatti/clingy.git
cd clingy
pip install -e .
```

### "Command not found in interactive menu"

**Problem:** Your command's `get_menu_tree()` is not implemented or returns `None`.

**Solution:**
```python
def get_menu_tree(self) -> MenuNode:
    """All commands must implement this method"""
    return MenuNode(
        label="My Command",
        emoji="⚙️",
        action=lambda: self.execute(Namespace())
    )
```

### "Import errors in custom commands"

**Problem:** Commands can't import from your project.

**Solution:**
```python
# Use absolute imports from project root
from config import ITEMS, PROJECT_NAME
from commands.utils import helper_function

# Not relative imports
# from ..config import ITEMS  # ❌ Don't do this
```

### "Context detection not working"

**Problem:** clingy can't find your project from subdirectories.

**Solution:**
1. Ensure `.clingy` marker file exists in project root:
   ```bash
   touch .clingy
   ```

2. Or ensure `commands/` directory exists:
   ```bash
   mkdir -p commands
   ```

3. Or ensure `config.py` exists:
   ```bash
   touch config.py
   ```

---

## Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Make** your changes following the [code style guidelines](AGENTS.md#code-style-guidelines)
4. **Test** your changes: `pytest tests/`
5. **Commit** with clear messages: `git commit -m "feat: add new feature"`
6. **Push** to your fork: `git push origin feature/my-feature`
7. **Open** a Pull Request

### Code of Conduct

Be respectful, inclusive, and constructive. We're all here to learn and build great tools.

### Development Guidelines

- **Type hints**: Required for all functions
- **Docstrings**: Google-style for public methods
- **Tests**: Add tests for new features
- **Code style**: Black with line-length 100
- **Comments**: English only
- **Logging**: Use `log_*` functions, not `print()`

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

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

---

**Last Updated:** January 2026  
**Python Version:** 3.8+  
**Maintainer:** [@ncasatti](https://github.com/ncasatti)

<!-- TODO: Add screenshot of interactive menu -->
<!-- TODO: Add demo GIF showing 'manager init' and usage -->
<!-- TODO: Add screenshot of konfig template in action -->
<!-- TODO: Add screenshot of serverless template -->
