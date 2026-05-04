# clingy

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Context-aware CLI framework** for building interactive command-line tools with fuzzy search menus and modular command architecture. Works like Git, Poetry, or Terraform—install once, use everywhere.

______________________________________________________________________

## The Problem & The Solution

Building CLI tools often feels like choosing between two extremes: a rigid, complex framework that takes days to learn, or a messy collection of scripts that are impossible to maintain.

**Clingy** was born to bridge that gap. It solves the "CLI fatigue" by providing a framework where **automation meets interaction**.

### Why Clingy?

- **Zero-Boilerplate Discovery:** Just drop a file in your `commands/` folder, and it's instantly available in your CLI. No manual registration, no complex routing.
- **Interactive by Default:** Every command you write automatically gains a, fuzzy-searchable menu (powered by `fzf`). You build the logic once; the framework provides the interface.
- **Submenu Architecture:** Use our intuitive node-based system to build complex, nested menus that feel like professional-grade software.
- **Context-Aware:** Like Git, Clingy automatically detects your project root. Run it from any subdirectory, and it knows exactly where it is.

______________________________________________________________________

## Documentation Hub

See the [Interactive Documentation](https://ncasatti.github.io/clingy/).

Navigate through the project documentation:

### Framework Reference

- [Architecture](docs/architecture.md) — Internal design and execution flow.
- [Creating Commands](docs/commands.md) — Guide for building custom CLI commands.

### Project Templates

- [Basic Template](clingy/templates/basic/README.md) — Simple CLI for prototyping.
- [Konfig Template](clingy/templates/konfig/README.md) — Dotfiles and symlink manager.
- [Serverless Template](clingy/templates/serverless/README.md) — AWS Lambda + Go workflow manager.

______________________________________________________________________

## Showcase

Clingy basic starter template

https://github.com/user-attachments/assets/61247d3c-2900-472d-a4fc-a7b3b551edf7

Clingy konfigs template
 
https://github.com/user-attachments/assets/c11d5731-9a4e-4163-8b86-06463003d677

______________________________________________________________________

## Installation

```bash
# Using uv (recommended)
uv pip install clingy

# Using pip
pip install clingy
```

**Required Dependency:** `fzf` (fuzzy finder). Install via your package manager (`brew`, `apt`, `pacman`, etc.).

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

## License

[MIT](LICENSE)
Maintainer: [@ncasatti](https://github.com/ncasatti)
