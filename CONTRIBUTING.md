# Contributing to clingy

Thank you for your interest in contributing to clingy! This document will guide you through the development process.

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ncasatti/clingy.git
cd clingy
```

### 2. Install Dependencies

```bash
# Install project in development mode
pip install -e ".[dev]"

# Install formatters
pip install black isort

# (Optional) Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### 3. Verify Installation

```bash
# Test the CLI
clingy --help

# Run a test command
clingy init --help
```

## Code Style

This project enforces strict code formatting using **Black** (line-length: 100) and **isort** (profile: black).

### Before Every Commit

**REQUIRED:** Run these commands before committing:

```bash
# Format your code
black clingy/ tests/ --line-length 100
isort clingy/ tests/ --profile black

# Verify formatting (same checks as CI)
black clingy/ tests/ --check --line-length 100
isort clingy/ tests/ --check-only --profile black

# Run tests
pytest tests/ -v
```

**⚠️ GitHub Actions will automatically reject PRs that don't pass these checks.**

### Editor Integration

**VS Code:**
- Install "Black Formatter" extension
- Install "isort" extension
- Add to `.vscode/settings.json`:
  ```json
  {
    "[python]": {
      "editor.defaultFormatter": "ms-python.black-formatter",
      "editor.formatOnSave": true
    }
  }
  ```

**PyCharm:**
- Go to Settings → Tools → Black
- Enable "Run Black on file save"
- Go to Settings → Tools → isort
- Enable "Run isort on file save"

**Vim/Neovim:**
- Use ALE or coc-pyright with Black/isort integration

### Code Style Guidelines

See [AGENTS.md](AGENTS.md) for detailed guidelines on:
- Type hints (required for all functions)
- Docstrings (Google-style format)
- Naming conventions (snake_case, PascalCase, UPPER_SNAKE_CASE)
- Error handling (fail gracefully)
- Logging (use `core/logger.py` utilities)
- Command structure (inherit from `BaseCommand`)
- Interactive menu support (implement `get_menu_tree()`)

## Testing

All new features and bug fixes should include tests.

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_commands.py -v

# Run specific test
pytest tests/test_commands.py::test_init -v

# Run with coverage report
pytest tests/ -v --cov=clingy --cov-report=term-missing

# Stop on first failure
pytest tests/ -x

# Drop into debugger on failure
pytest tests/ --pdb
```

### Writing Tests

Tests should be placed in the `tests/` directory with the naming convention `test_*.py`:

```python
import pytest
from clingy.commands.mycommand import MyCommand
from argparse import Namespace

class TestMyCommand:
    def setup_method(self):
        """Setup before each test"""
        self.command = MyCommand()
    
    def test_execute_success(self):
        """Test successful execution"""
        args = Namespace(item_list=["item-1"])
        assert self.command.execute(args) is True
    
    def test_execute_empty_list(self):
        """Test with empty item list"""
        args = Namespace(item_list=[])
        assert self.command.execute(args) is False
```

**Current coverage:** ~42% (aim for 50-70% on new code)

## Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-awesome-feature
```

Branch naming convention:
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### 2. Make Your Changes

- Follow the code style guidelines (see [AGENTS.md](AGENTS.md))
- Add tests for new functionality
- Update documentation if needed

### 3. Run Pre-commit Checks

```bash
# Format code
black clingy/ tests/ --line-length 100
isort clingy/ tests/ --profile black

# Verify formatting
black clingy/ tests/ --check --line-length 100
isort clingy/ tests/ --check-only --profile black

# Run tests
pytest tests/ -v
```

### 4. Commit with Conventional Commits

```bash
git commit -m "feat: add awesome feature"
```

See [Commit Message Format](#commit-message-format) below.

### 5. Push to Your Fork

```bash
git push origin feature/my-awesome-feature
```

### 6. Open a Pull Request

- Go to GitHub and create a PR from your fork
- Fill in the PR template with a clear description
- Reference any related issues (e.g., "Closes #123")

### PR Requirements

- ✅ Code is formatted with Black and isort
- ✅ All tests pass (`pytest tests/ -v`)
- ✅ Commit messages follow [Conventional Commits](https://conventionalcommits.org/)
- ✅ New features include tests (if applicable)
- ✅ Documentation is updated (if applicable)
- ✅ No merge conflicts with `main` branch

## Commit Message Format

We use [Conventional Commits](https://conventionalcommits.org/) for clear, semantic commit history.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code formatting (no functional changes)
- **refactor**: Code refactoring without feature changes
- **test**: Adding or updating tests
- **ci**: CI/CD configuration changes
- **chore**: Dependency updates, tooling changes

### Scope (Optional)

The scope specifies what part of the codebase is affected:
- `menu` - Menu system
- `commands` - Command framework
- `cli` - CLI entry point
- `logger` - Logging utilities
- `discovery` - Context discovery
- `templates` - Project templates

### Subject

- Use imperative mood ("add" not "added")
- Don't capitalize first letter
- No period at the end
- Max 50 characters

### Body (Optional)

- Explain **what** and **why**, not **how**
- Wrap at 72 characters
- Separate from subject with blank line

### Footer (Optional)

- Reference issues: `Closes #123`
- Breaking changes: `BREAKING CHANGE: description`

### Examples

```bash
# Simple feature
git commit -m "feat: add fuzzy search to menu"

# Bug fix with scope
git commit -m "fix(menu): handle empty item list"

# Feature with body
git commit -m "feat(commands): add interactive menu support

Implement get_menu_tree() method for all commands.
This allows commands to define custom menu structures
for interactive mode.

Closes #42"

# Breaking change
git commit -m "refactor(cli): change command interface

BREAKING CHANGE: Commands now require get_menu_tree() method"
```

## Project Structure

```
clingy/
├── clingy/           # Main package
│   ├── commands/           # Framework commands
│   │   ├── base.py        # Abstract base class
│   │   ├── init.py        # Project initialization
│   │   └── __init__.py    # Command discovery
│   ├── core/              # Core utilities
│   │   ├── discovery.py   # Context detection
│   │   ├── logger.py      # Logging functions
│   │   ├── colors.py      # Terminal styling
│   │   ├── menu.py        # Interactive menu system
│   │   └── stats.py       # Statistics tracking
│   ├── templates/         # Project templates
│   │   └── basic/         # Default template
│   ├── cli.py             # CLI entry point
│   ├── cli_builder.py     # Context builder
│   └── config.py          # Framework configuration
├── tests/                 # Test suite
├── setup.py               # Package configuration
├── AGENTS.md              # Development guidelines
├── CONTRIBUTING.md        # This file
└── README.md              # Project documentation
```

## Development Workflow

### Adding a New Command

1. Create a new file in `clingy/commands/`:
   ```python
   # clingy/commands/mycommand.py
   from clingy.commands.base import BaseCommand
   from argparse import ArgumentParser, Namespace
   from clingy.core.menu import MenuNode
   from typing import Optional
   
   class MyCommand(BaseCommand):
       name = "mycommand"
       help = "Short help text"
       
       def add_arguments(self, parser: ArgumentParser):
           parser.add_argument('--option', help='Option description')
       
       def execute(self, args: Namespace) -> bool:
           items = self._resolve_item_list(args)
           # Your logic here
           return True
       
       def get_menu_tree(self) -> Optional[MenuNode]:
           return MenuNode(
               label="My Command",
               emoji="⚙️",
               action=lambda: self.execute(Namespace())
           )
   ```

2. Add tests in `tests/test_mycommand.py`
3. Update `README.md` with usage examples
4. Commit with: `git commit -m "feat(commands): add mycommand"`

### Modifying Existing Code

1. Read the existing code first (see [AGENTS.md](AGENTS.md))
2. Make your changes
3. Run formatters and tests
4. Commit with appropriate type (feat/fix/refactor)

## Questions or Issues?

- **Bug reports:** Open an issue with the "bug" label
- **Feature requests:** Open an issue with the "enhancement" label
- **Questions:** Open a discussion on GitHub Discussions
- **Security issues:** Email security@example.com (do NOT open public issues)

## Code of Conduct

Be respectful and constructive. We're all here to build something awesome together.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing opinions
- Accept constructive criticism gracefully
- Focus on what is best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal attacks
- Publishing private information

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Questions?** Check [AGENTS.md](AGENTS.md) for detailed development guidelines, or open an issue on GitHub.
