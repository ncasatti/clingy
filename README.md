# Serverless Manager CLI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)

> Professional CLI tool for managing AWS Lambda serverless applications with Go runtime

A comprehensive command-line interface for building, deploying, and managing AWS Lambda functions written in Go. Features interactive menus, CloudWatch Insights integration, and automated deployment workflows.

---

## 🚀 Features

- **🔨 Build Management**: Compile Go functions to AWS Lambda-compatible binaries
- **📦 Deployment**: Deploy individual functions or entire stacks with Serverless Framework
- **🔍 CloudWatch Insights**: Query and analyze Lambda logs with custom queries
- **📊 Interactive Menus**: Fuzzy search-powered function selection with `fzf`
- **🧪 Function Invocation**: Test functions locally or remotely with custom payloads
- **📝 Logs Streaming**: Real-time log viewing with filtering and saving
- **🎯 Modular Architecture**: Auto-discovery command system for easy extension

---

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Commands](#commands)
- [Configuration](#configuration)
- [CloudWatch Insights](#cloudwatch-insights)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🛠️ Installation

### Prerequisites

Required dependencies:
- **Python 3.8+**
- **Go 1.19+** (for building Lambda functions)
- **AWS CLI** (configured with credentials)
- **Serverless Framework** (`npm install -g serverless`)
- **fzf** (fuzzy finder for interactive menus)

Optional but recommended:
- **PyYAML** (for YAML output formatting)

### Install Dependencies

**macOS:**
```bash
brew install python go awscli serverless fzf
pip install pyyaml
```

**Ubuntu/Debian:**
```bash
sudo apt install python3 golang awscli fzf
npm install -g serverless
pip install pyyaml
```

### Verify Installation

```bash
python manager.py requirements status
```

This will check all required dependencies and show their installation status.

---

## ⚡ Quick Start

### 1. Configure Your Project

Edit `manager/config.py` with your AWS settings:

```python
# AWS Configuration
ENV = "dev"
AWS_PROFILE = "your-aws-profile"
SERVICE_NAME = "your-service-name"

# Function List
GO_FUNCTIONS = [
    "status",
    "getUsers",
    "createOrder",
    # ... add your functions
]
```

### 2. Interactive Mode (Recommended)

```bash
# Start interactive menu (no arguments)
python manager.py
```

This opens a **fuzzy-searchable menu system** where you can:
- Navigate through command menus with arrow keys
- Select functions with `TAB` (multi-select)
- Build, zip, and deploy in one step
- View logs in real-time
- Invoke functions with test payloads
- Run CloudWatch Insights queries

**Navigation:**
- `↑/↓`: Navigate menu items
- `TAB`: Select/deselect (in multi-select menus)
- `ENTER`: Confirm selection
- `ESC` or `Ctrl+C`: Go back or exit

### 3. CLI Mode (Traditional)

```bash
# Build all functions
python manager.py build

# Build specific function
python manager.py build -f status

# Deploy all functions
python manager.py deploy --all

# Deploy specific function
python manager.py deploy -f status
```

### 4. Hybrid Workflow

You can mix interactive and CLI modes:

```bash
# Start interactive menu
python manager.py

# Or use CLI directly
python manager.py build -f status
python manager.py deploy -f status
python manager.py logs -f status
```

---

## 🏗️ Architecture

### Directory Structure

```
manager/
├── commands/          # Command implementations
│   ├── base.py       # Abstract base command
│   ├── build.py      # Build Go binaries
│   ├── clean.py      # Clean artifacts
│   ├── deploy.py     # Deploy to AWS
│   ├── dev.py        # Interactive dev menu
│   ├── insights.py   # CloudWatch Insights
│   ├── invoke.py     # Function invocation
│   ├── logs.py       # Log viewing
│   ├── list_functions.py
│   ├── remove.py     # Remove stack
│   ├── requirements.py
│   └── zip.py        # Create deployment packages
│
├── core/             # Core utilities
│   ├── colors.py     # Terminal colors & emojis
│   ├── insights_formatter.py
│   ├── insights_queries.py
│   ├── logger.py     # Logging utilities
│   ├── menu.py       # Interactive menu system (fzf)
│   └── stats.py      # Build statistics
│
├── cli.py            # CLI entry point (orchestrator)
├── config.py         # Project configuration
└── README.md         # This file
```

### Interactive Menu System

The manager features a **tree-based interactive menu system** powered by `fzf`:

```
┌─ Main Menu ─────────────────────────────────┐
│ 🔨 Build                                    │
│ 🚀 Deploy                                   │
│ 📦 Zip                                      │
│ 📋 Logs                                     │
│ 🔍 Insights                                 │
│ ▶️  Invoke                                   │
│ 🧹 Clean                                    │
└─────────────────────────────────────────────┘
```

**How it works:**
1. Run `python manager.py` (no arguments) to enter interactive mode
2. Navigate menus with arrow keys
3. Select functions with `TAB` (multi-select support)
4. Confirm with `ENTER`
5. Go back with `ESC` or select "← Back"

**Key Features:**
- **Fuzzy search**: Type to filter options
- **Multi-select**: Use `TAB` to select multiple functions
- **Breadcrumb navigation**: See your path through the menu tree
- **Context-aware**: Each command has its own menu structure
- **Fallback to CLI**: Commands without interactive menus still work

### Command Discovery

The manager uses an **auto-discovery system** for commands:

1. All Python files in `commands/` are automatically discovered
2. Each command inherits from `BaseCommand`
3. Commands are registered in CLI with their `name` attribute
4. No manual registration needed - just add a new file!

**Example Command:**

```python
from manager.commands.base import BaseCommand

class MyCommand(BaseCommand):
    name = "mycommand"
    help = "Short description"
    description = "Detailed description"
    
    def add_arguments(self, parser):
        parser.add_argument('-f', '--flag')
    
    def execute(self, args):
        # Your logic here
        return True
```

---

## 📚 Commands

### Core Commands

#### `build`
Compile Go Lambda functions to Linux/amd64 binaries.

```bash
# Build all functions
python manager.py build

# Build specific function
python manager.py build -f getUsers

# From dev menu (supports multi-select)
python manager.py dev
→ Select functions → Build only
```

**Environment Variables Set:**
- `GOOS=linux`
- `GOARCH=amd64`
- `CGO_ENABLED=0`

**Build Flags:**
- `-ldflags="-s -w"` (strip debug info, reduce binary size)

---

#### `zip`
Create deployment packages for Lambda functions.

```bash
# Zip all functions
python manager.py zip

# Zip specific function
python manager.py zip -f getUsers
```

Creates `.zip` files in `.bin/` directory ready for Lambda deployment.

---

#### `deploy`
Deploy functions to AWS using Serverless Framework.

```bash
# Deploy all functions (full stack)
python manager.py deploy --all

# Deploy specific function
python manager.py deploy -f getUsers

# Debug mode
python manager.py deploy --debug
```

**Deployment Strategies:**
- **Single function**: Uses `serverless deploy function -f <name>` (fast)
- **Multiple functions**: Uses `serverless deploy` (full stack, slower but safer)

---

#### `dev`
Interactive development menu with fuzzy search.

```bash
python manager.py dev
```

**Features:**
- Multi-select functions with `TAB`
- Build → Zip → Deploy pipeline
- View logs for single function
- Invoke functions with payloads
- Run CloudWatch Insights queries

**Keyboard Shortcuts:**
- `TAB`: Select/deselect function
- `ENTER`: Confirm selection
- `ESC` or `Ctrl+C`: Exit menu

---

#### `logs`
View CloudWatch logs for Lambda functions.

```bash
# Interactive menu
python manager.py logs

# Specific function
python manager.py logs -f getUsers
```

**Log Options:**
1. **Last 30 minutes** (short format)
2. **Last 5 minutes** (short format)
3. **Real-time** (follow mode with `--follow`)
4. **Custom filter** (filter by pattern)

Logs are automatically saved to `functions/<name>/function.log`.

---

#### `invoke`
Test Lambda functions locally or remotely.

```bash
# Interactive menu
python manager.py invoke

# Specific function with payload
python manager.py invoke -f getUsers -p test-payloads/user.json

# Local invocation
python manager.py invoke -f getUsers --local
```

**Payload Discovery:**
- **Global**: `test-payloads/*.json` (shared across all functions)
- **Local**: `functions/<name>/payloads/*.json` (function-specific)

**Response Handling:**
- Pretty-printed JSON output
- Saves response to `functions/<name>/output.yaml`
- Color-coded status codes (green for 2xx, red for errors)

---

#### `insights`
Query CloudWatch Logs with Insights DSL.

```bash
# Interactive menu
python manager.py insights

# Specific function
python manager.py insights -f processContenedor
```

**Features:**
- **6 predefined templates** (errors, performance, cold starts, etc.)
- **Custom queries** with save/load functionality
- **Query library**: Global (`insights-queries/`) + Function-specific (`functions/<name>/queries/`)
- **Multiple targets**: Single function, all functions, or multi-select
- **YAML output** for easy reading

See [CloudWatch Insights](#cloudwatch-insights) section for details.

---

#### `list`
List all available Lambda functions.

```bash
python manager.py list
```

Displays all functions defined in `config.py`.

---

#### `clean`
Remove all build artifacts.

```bash
python manager.py clean
```

Deletes the `.bin/` directory with all compiled binaries and zip files.

---

#### `remove`
Remove the entire serverless stack from AWS.

```bash
# Remove stack
python manager.py remove

# With debug output
python manager.py remove --debug
```

**⚠️ Warning:** This permanently deletes all Lambda functions, API Gateway, and resources.

---

#### `requirements`
Check system dependencies.

```bash
python manager.py requirements status
```

Verifies installation of:
- Python, Go, AWS CLI, Serverless Framework, fzf
- Shows installation commands for missing dependencies

---

## ⚙️ Configuration

### `manager/config.py`

This is the **only file** you need to modify for your project.

```python
# ============================================================================
# AWS Configuration
# ============================================================================
ENV = "dev"                          # Environment: dev, staging, prod
AWS_PROFILE = "your-aws-profile"     # AWS CLI profile name
SERVICE_NAME = "your-service-name"   # Serverless service name

# ============================================================================
# Build Settings
# ============================================================================
BUILD_SETTINGS = {
    "GOOS": "linux",
    "GOARCH": "amd64",
    "CGO_ENABLED": "0",
}

BUILD_FLAGS = ["-ldflags", "-s -w"]  # Strip debug symbols

# ============================================================================
# Paths
# ============================================================================
FUNCTIONS_DIR = "functions"          # Go functions directory
BIN_DIR = ".bin"                     # Build output directory

# ============================================================================
# Deployment Settings
# ============================================================================
SERVERLESS_STAGE = ENV               # Serverless stage (same as ENV)
SERVERLESS_PROFILE = AWS_PROFILE     # AWS profile for deployment

# ============================================================================
# Invoke Settings
# ============================================================================
INVOKE_REMOTE_METHOD = "serverless"  # Options: "serverless" or "aws-cli"
INVOKE_AWS_REGION = "us-west-2"      # AWS region for Lambda invocations

# ============================================================================
# Function List
# ============================================================================
GO_FUNCTIONS = [
    "status",
    "getUsers",
    "createOrder",
    "processPayment",
    # Add all your Lambda function names here
]

# ============================================================================
# Required System Dependencies
# ============================================================================
REQUIRED_DEPENDENCIES = {
    "fzf": {
        "command": "fzf",
        "check": "--version",
        "install": {
            "macos": "brew install fzf",
            "ubuntu": "sudo apt install fzf",
        },
        "description": "Fuzzy finder for interactive menus",
        "required": True
    },
    # ... more dependencies
}
```

---

## 🔍 CloudWatch Insights

The `insights` command provides powerful log analysis capabilities using AWS CloudWatch Logs Insights.

### Quick Start

```bash
python manager.py insights -f processContenedor
```

### Features

#### 1. Predefined Templates

Six ready-to-use query templates:

- **🔴 Recent Errors**: Find ERROR and Exception messages
- **⚡ Performance Stats**: P50/P95/P99 latency analysis
- **🥶 Cold Starts**: Identify cold start invocations
- **🐌 Slowest Requests**: Top 20 slowest executions
- **📊 Error Rate by Hour**: Error count distribution
- **💾 Memory Usage**: Memory consumption statistics

#### 2. Custom Queries

Create and save custom queries for reuse:

**Global Queries** (`insights-queries/`):
```yaml
# insights-queries/my-query.query
name: My Custom Query
description: Find specific error patterns
time_range: 2h
target: single

---
fields @timestamp, @message, @requestId
| filter @message like /timeout/
| sort @timestamp desc
| limit 50
```

**Function-Specific Queries** (`functions/<name>/queries/`):
```yaml
# functions/processContenedor/queries/erp-dispatch-analysis.query
name: ERP Dispatch Analysis
description: Analyze ERP dispatch events
time_range: 2h

---
fields @timestamp, event, db_schema, function_arn, error
| filter event in ["erp_dispatch_started", "erp_dispatch_completed"]
| sort @timestamp desc
```

#### 3. Time Range Selection

Predefined ranges:
- Last 5, 15, 30 minutes
- Last 1, 3, 6, 12, 24 hours
- Last 7 days
- Custom (e.g., `2h`, `45m`, `3d`)

#### 4. Output Formats

**Console Output:**
```
@timestamp              | event                             | db_schema
------------------------+-----------------------------------+-----------
2026-01-06 16:41:51.903 | erp_dispatch_completed            | latam
2026-01-06 16:41:49.558 | erp_dispatch_started              |

Statistics:
  • Records matched: 8
  • Records scanned: 66
  • Bytes scanned: 12.24 KB
```

**YAML File** (`functions/<name>/insights-result.yaml`):
```yaml
query_metadata:
  query_name: ERP Dispatch Analysis
  function: processContenedor
  executed_at: '2026-01-06T16:45:22.123456'
  records_matched: 8
  records_scanned: 66

results:
- '@timestamp': '2026-01-06 16:41:51.903'
  event: erp_dispatch_completed
  db_schema: latam
  function_arn: arn:aws:lambda:us-west-2:...
```

### Query Syntax

CloudWatch Insights uses its own DSL (Domain Specific Language):

```
fields @timestamp, @message, @requestId
| filter @message like /ERROR/
| stats count(*) by bin(5m)
| sort @timestamp desc
| limit 20
```

**Common Patterns:**

```
# Find errors in last hour
fields @timestamp, @message
| filter level = "error"
| sort @timestamp desc

# Performance percentiles
fields @duration
| filter @type = "REPORT"
| stats avg(@duration), pct(@duration, 95), pct(@duration, 99)

# Count by field
fields event
| stats count(*) by event
| sort count(*) desc
```

**Reference**: [CloudWatch Logs Insights Query Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)

---

## 🔧 Development

### Adding a New Command

1. Create a new file in `manager/commands/`:

```python
# manager/commands/mycommand.py
from manager.commands.base import BaseCommand
from argparse import ArgumentParser, Namespace
from manager.core.menu import MenuNode

class MyCommand(BaseCommand):
    """Description of what this command does"""
    
    name = "mycommand"
    help = "Short help text"
    description = "Detailed description for --help"
    epilog = """Examples:
  manager.py mycommand --option value
"""
    
    def add_arguments(self, parser: ArgumentParser):
        """Add command-specific arguments"""
        parser.add_argument('--option', help='Option description')
    
    def execute(self, args: Namespace) -> bool:
        """Execute the command logic"""
        # Your implementation here
        return True  # Return True on success, False on failure
    
    def get_menu_tree(self) -> Optional[MenuNode]:
        """
        Optional: Define interactive menu structure.
        
        If you don't implement this, the command only works via CLI.
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

2. That's it! The command is automatically discovered and registered.

3. Test it:
```bash
# CLI mode
python manager.py mycommand --help

# Interactive mode (if get_menu_tree() is implemented)
python manager.py
```

### Command Auto-Discovery

The CLI automatically discovers commands by:

1. Scanning `manager/commands/` directory
2. Loading all `.py` files (except `__init__.py` and `base.py`)
3. Finding classes that inherit from `BaseCommand`
4. Registering them using their `name` attribute

**No manual registration needed!**

### Extending BaseCommand

`BaseCommand` provides:

- **`_resolve_function_list(args)`**: Resolves function list from CLI args or dev menu
- **`_get_filtered_functions(filter)`**: Validates function names against config

**Example Usage:**

```python
def execute(self, args: Namespace) -> bool:
    # Get functions to process (supports both dev and CLI modes)
    functions = self._resolve_function_list(args)
    
    for func in functions:
        # Process each function
        print(f"Processing {func}")
    
    return True
```

---

## 🐛 Troubleshooting

### Common Issues

#### **1. `fzf: command not found`**

Install fzf:
```bash
# macOS
brew install fzf

# Ubuntu/Debian
sudo apt install fzf
```

#### **2. Build fails with `permission denied`**

Ensure Go binaries are executable:
```bash
chmod +x .bin/*
```

#### **3. Deployment fails with AWS credentials error**

Check AWS CLI configuration:
```bash
aws configure list --profile your-profile
```

#### **4. PyYAML import error**

Install PyYAML (optional but recommended):
```bash
pip install pyyaml
```

#### **5. Serverless Framework not found**

Install globally with npm:
```bash
npm install -g serverless
```

### Debug Mode

Enable debug output for deployment:
```bash
python manager.py deploy --debug
```

### Check Requirements

Verify all dependencies:
```bash
python manager.py requirements status
```

---

## 📖 Best Practices

### 1. Function Organization

```
functions/
├── status/
│   ├── main.go          # Lambda handler
│   ├── payloads/        # Test payloads for this function
│   │   └── test.json
│   └── queries/         # CloudWatch Insights queries
│       └── errors.query
├── getUsers/
│   ├── main.go
│   └── ...
└── ...
```

### 2. Payload Management

- **Global payloads**: Use `test-payloads/` for payloads shared across functions
- **Function-specific**: Use `functions/<name>/payloads/` for function-specific tests

### 3. Query Management

- **Global queries**: Use `insights-queries/` for general-purpose queries
- **Function-specific**: Use `functions/<name>/queries/` for specialized analysis

### 4. Deployment Strategy

For **development**:
```bash
# Deploy single function (fast)
python manager.py deploy -f status
```

For **production**:
```bash
# Deploy full stack (safer)
python manager.py deploy --all
```

### 5. Git Ignore

The manager automatically ignores:
- `.bin/` (build artifacts)
- `functions/*/output.yaml` (invocation responses)
- `functions/*/function.log` (log files)
- `functions/*/insights-result.*` (query results)

---

## 🤝 Contributing

### Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-command`)
3. Add your command in `manager/commands/`
4. Test thoroughly
5. Update this README if adding new features
6. Submit a pull request

### Code Style

- **Docstrings**: Use Google-style docstrings
- **Type hints**: Use Python type hints for all function signatures
- **Naming**: Use snake_case for functions, PascalCase for classes
- **Logging**: Use logger utilities from `manager.core.logger`

### Testing

Test your command:
```bash
# Test help text
python manager.py mycommand --help

# Test execution
python manager.py mycommand

# Test with dev menu integration (if applicable)
python manager.py dev
```

---

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details.

---

## 🙏 Acknowledgments

- **AWS Lambda**: Serverless compute platform
- **Serverless Framework**: Deployment automation
- **fzf**: Interactive fuzzy finder
- **CloudWatch Logs Insights**: Log analysis engine

---

## 📬 Support

For issues, questions, or contributions:

- **Issues**: [GitHub Issues](https://github.com/yourusername/yourrepo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/yourrepo/discussions)

---

**Built with ❤️ for serverless developers**
