# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-01-15

### ⚠️ BREAKING CHANGES

- **Converted from AWS-specific manager to generic CLI template**
  - Removed all AWS Lambda, Serverless Framework, and CloudWatch dependencies
  - This is now a reusable template for building interactive CLI tools
  
- **Configuration changes**
  - Renamed `GO_FUNCTIONS` → `ITEMS` (generic item list)
  - Renamed `AWS_PROFILE`, `SERVICE_NAME`, `ENV` → `PROJECT_NAME`, `PROJECT_VERSION`
  - Removed AWS-specific settings (build flags, deployment config, etc.)
  
- **Command renaming**
  - `list_functions` → `list_items`
  - Base class method: `_resolve_function_list()` → `_resolve_item_list()`
  - Menu helper: `fzf_select_functions()` → `fzf_select_items()`

### Added

- **Example commands** demonstrating different CLI patterns:
  - `greet.py`: Simple menu with language selection (es, en, fr, de)
  - `files.py`: Hierarchical menu for file operations (list/create/delete)
  - `calculator.py`: Interactive input handling (add, subtract, multiply, divide)
  - `info.py`: CLI-only command showing system information

- **Generic configuration structure** in `config.py`:
  - `PROJECT_NAME` and `PROJECT_VERSION` for any project
  - `ITEMS` list for managing generic items
  - `DATA_DIR` and `OUTPUT_DIR` for flexible file organization

- **Documentation for template usage**:
  - Updated README.md with template-focused content
  - Added "How to Extend" section with examples
  - Added "Use Cases" section for different scenarios
  - Added "Menu Types" comparison table

### Removed

- **AWS-specific commands** (8 total):
  - `build.py`: Go compilation for Lambda
  - `deploy.py`: Serverless Framework deployment
  - `logs.py`: CloudWatch log streaming
  - `insights.py`: CloudWatch Logs Insights queries
  - `invoke.py`: Lambda function invocation
  - `zip.py`: Deployment package creation
  - `dev.py`: AWS-specific dev menu
  - `remove.py`: Stack removal

- **CloudWatch utilities**:
  - `core/insights_queries.py`: Predefined query templates
  - `core/insights_formatter.py`: Query result formatting

- **AWS-specific configuration**:
  - `BUILD_SETTINGS` (Go compiler flags)
  - `SERVERLESS_STAGE`, `SERVERLESS_PROFILE`
  - `INVOKE_REMOTE_METHOD`, `INVOKE_AWS_REGION`
  - `FUNCTIONS_DIR`, `BIN_DIR`

### Changed

- **CLI header**: "Serverless Manager CLI" → "CLI Manager Template"
- **Menu system**: Now uses generic `ITEMS` instead of `GO_FUNCTIONS`
- **Base command class**: Updated to work with generic items instead of functions
- **Logger output**: Removed AWS-specific terminology

---

## [1.0.0] - 2026-01-14

### Added

- Initial release as AWS Lambda manager
- Interactive menu system with fzf integration
- Auto-discovery command architecture
- CloudWatch Insights integration
- Build, deploy, and log management for Go Lambda functions
- Multi-select function support in interactive menus
- Comprehensive documentation and examples

---

## Migration Guide (v1.0.0 → v2.0.0)

If you were using this as an AWS Lambda manager, here's how to migrate:

### Step 1: Update Configuration

**Before (v1.0.0):**
```python
GO_FUNCTIONS = ["status", "getUsers", "processPayment"]
AWS_PROFILE = "my-profile"
SERVICE_NAME = "my-service"
```

**After (v2.0.0):**
```python
ITEMS = ["item1", "item2", "item3"]
PROJECT_NAME = "My CLI Tool"
PROJECT_VERSION = "1.0.0"
```

### Step 2: Update Command Code

**Before (v1.0.0):**
```python
functions = self._resolve_function_list(args)
for func in functions:
    self._build_function(func)
```

**After (v2.0.0):**
```python
items = self._resolve_item_list(args)
for item in items:
    self._process_item(item)
```

### Step 3: Update Menu Helpers

**Before (v1.0.0):**
```python
from manager.core.menu import fzf_select_functions
selected = fzf_select_functions(prompt="Select functions: ")
```

**After (v2.0.0):**
```python
from manager.core.menu import fzf_select_items
selected = fzf_select_items(prompt="Select items: ")
```

### Step 4: Remove AWS Dependencies

If you need AWS functionality, you can:
- Keep your own fork with AWS commands
- Create a custom template extending this one
- Use this as a base and add AWS-specific commands back

---

**For detailed information on using this template, see [README.md](README.md)**
