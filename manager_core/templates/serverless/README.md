# Serverless Manager Template

AWS Lambda + Go serverless functions manager with interactive menus.

## Features

- 📦 **Build, Zip, Deploy** Go Lambda functions
- 🔍 **CloudWatch Logs** (view, tail, filter)
- ▶️ **Invoke** functions locally or remotely
- 📊 **CloudWatch Insights** queries
- 🎯 **Composable Payloads** with PayloadNavigator
- 🚀 **Full Pipeline** (Build → Zip → Deploy)
- 📈 **Status & Monitoring** (dependencies, build status, config)

## Quick Start

### 1. Initialize Project

```bash
manager init --template serverless
cd my-serverless-project
```

### 2. Configure

Edit `config.py`:

```python
# AWS Configuration
ENV = "dev"
AWS_PROFILE = "my-profile"
SERVICE_NAME = "my-service"

# Function List
GO_FUNCTIONS = [
    "status",
    "getUsers",
    "createUser",
]
```

### 3. Run Interactive Menu

```bash
manager
```

## Menu Structure

```
🚀 SERVERLESS MANAGER
├── 📦 Functions
│   ├── Build Functions (All / Select)
│   ├── Zip Functions (All / Select)
│   ├── Deploy Functions (All / Select)
│   ├── Full Pipeline (Build → Zip → Deploy)
│   └── Clean Build Artifacts
│
├── 🔍 Logs & Monitoring
│   ├── View Recent Logs
│   ├── Tail Live Logs
│   └── CloudWatch Insights
│
├── ▶️ Invoke Functions
│   ├── Local Invocation
│   ├── Remote Invocation (AWS)
│   └── Payload Navigator
│
└── 📊 Status & Info
    ├── List All Functions
    ├── Build Status
    ├── Check Dependencies
    └── Show Configuration
```

## Project Structure

```
my-serverless-project/
├── commands/                  # Menu commands
│   ├── functions.py          # Build/Zip/Deploy menu
│   ├── logs_menu.py          # Logs & Monitoring menu
│   ├── invoke_menu.py        # Invoke menu
│   ├── status.py             # Status & Info menu
│   └── core_commands/        # Core command implementations
│       ├── build.py          # Build Go functions
│       ├── zip.py            # Zip binaries
│       ├── deploy.py         # Deploy to AWS
│       ├── logs.py           # CloudWatch logs
│       ├── invoke.py         # Local/Remote invocation
│       ├── insights.py       # CloudWatch Insights
│       └── clean.py          # Clean artifacts
│
├── core/                      # Core utilities
│   ├── payload_composer.py   # Composable payload system
│   ├── payload_navigator.py  # Interactive payload browser
│   ├── insights_queries.py   # Predefined Insights queries
│   └── insights_formatter.py # Insights output formatting
│
├── functions/                 # Go Lambda functions (your code)
│   ├── status/
│   │   └── main.go
│   ├── getUsers/
│   │   └── main.go
│   └── createUser/
│       └── main.go
│
├── payloads/                  # Composable payloads
│   ├── base/
│   │   └── common.json
│   └── dev/
│       └── override.json
│
├── .bin/                      # Build output (auto-generated)
│   ├── status/
│   │   └── bootstrap
│   └── ...
│
├── config.py                  # Project configuration
└── serverless.yml             # Serverless Framework config
```

## Workflows

### Build & Deploy

```bash
# Interactive menu
manager
# → Functions → Full Pipeline → All Functions

# CLI mode (if needed)
python -m commands.core_commands.build
python -m commands.core_commands.zip
python -m commands.core_commands.deploy
```

### View Logs

```bash
# Interactive menu
manager
# → Logs & Monitoring → View Recent Logs → Select Function

# Tail live logs
# → Logs & Monitoring → Tail Live Logs → Select Function
```

### Invoke Functions

```bash
# Interactive menu
manager
# → Invoke Functions → Local Invocation → Select Function

# Remote invocation
# → Invoke Functions → Remote Invocation → Select Function
```

### CloudWatch Insights

```bash
# Interactive menu
manager
# → Logs & Monitoring → CloudWatch Insights → Run Query
```

## Composable Payloads

The template includes a powerful payload composition system:

### Directory Structure

```
payloads/
├── base/              # Base payloads (shared)
│   └── common.json
├── dev/               # Dev environment overrides
│   └── override.json
└── prod/              # Prod environment overrides
    └── override.json
```

### Payload Composition

Payloads are merged in order:
1. `base/` (common values)
2. `{stage}/` (environment-specific overrides)
3. Function-specific payloads (if any)

### Example

**base/common.json:**
```json
{
  "userId": "test-user",
  "limit": 10
}
```

**dev/override.json:**
```json
{
  "limit": 100,
  "debug": true
}
```

**Result (dev):**
```json
{
  "userId": "test-user",
  "limit": 100,
  "debug": true
}
```

## Configuration

### AWS Settings

```python
ENV = "dev"                    # Environment (dev, staging, prod)
AWS_PROFILE = "my-profile"     # AWS CLI profile
SERVICE_NAME = "my-service"    # Serverless service name
```

### Build Settings

```python
BUILD_SETTINGS = {
    "GOOS": "linux",           # Target OS
    "GOARCH": "amd64",         # Target architecture
    "CGO_ENABLED": "0",        # Disable CGO
}

BUILD_FLAGS = ["-ldflags", "-s -w"]  # Strip debug info
```

### Invoke Settings

```python
INVOKE_REMOTE_METHOD = "serverless"  # or "aws-cli"
INVOKE_AWS_REGION = "us-west-2"
```

### Payload Settings

```python
PAYLOADS_DIR = "payloads"
PAYLOAD_DEFAULT_STAGE = ENV
PAYLOAD_LEGACY_SUPPORT = True
PAYLOAD_SHOW_MERGE_SOURCES = True
```

## Dependencies

Required tools (auto-checked by `manager status`):

- **fzf** - Fuzzy finder for interactive menus
- **serverless** - Serverless Framework CLI
- **aws** - AWS CLI
- **go** - Go programming language
- **python** - Python 3.8+

Install on macOS:
```bash
brew install fzf awscli go python3
npm install -g serverless
```

Install on Linux (Arch):
```bash
sudo pacman -S fzf aws-cli go python3
npm install -g serverless
```

## Tips

### 1. Use Full Pipeline for Quick Deploys

The "Full Pipeline" option builds, zips, and deploys in one go:
- Saves time on multi-function deploys
- Ensures consistency (no stale zips)
- Shows progress for each step

### 2. Tail Logs During Testing

Use "Tail Live Logs" to watch function execution in real-time:
- See errors immediately
- Debug invocation issues
- Monitor performance

### 3. Use Payload Navigator

The PayloadNavigator shows:
- All available payloads
- Merge sources (base + stage + function)
- Final composed payload
- Validation errors

### 4. Check Build Status Regularly

Use "Status & Info → Build Status" to:
- See which functions are built
- Find missing source files
- Check binary sizes

## Troubleshooting

### Build Fails

```bash
# Check Go installation
go version

# Check function source exists
ls functions/myFunction/main.go

# Check build settings
manager
# → Status & Info → Show Configuration
```

### Deploy Fails

```bash
# Check AWS credentials
aws sts get-caller-identity --profile my-profile

# Check Serverless config
serverless info --stage dev --aws-profile my-profile

# Check binary exists
ls .bin/myFunction/bootstrap
```

### Invoke Fails

```bash
# Local: Check binary exists
ls .bin/myFunction/bootstrap

# Remote: Check function is deployed
aws lambda get-function --function-name myFunction --profile my-profile

# Check payload is valid JSON
cat payloads/base/common.json | jq .
```

## Advanced

### Custom Insights Queries

Edit `core/insights_queries.py` to add custom queries:

```python
CUSTOM_QUERIES = {
    "my-query": {
        "name": "My Custom Query",
        "query": """
            fields @timestamp, @message
            | filter @message like /ERROR/
            | stats count() by bin(5m)
        """,
        "description": "Count errors by 5-minute bins",
    }
}
```

### Custom Commands

Add new commands in `commands/`:

```python
from manager_core.commands.base import BaseCommand
from manager_core.core.menu import MenuNode

class MyCommand(BaseCommand):
    name = "mycommand"
    help = "My custom command"
    
    def execute(self, args):
        # Your logic here
        return True
    
    def get_menu_tree(self):
        return MenuNode(
            label="My Command",
            emoji="⚙️",
            action=lambda: self.execute(None)
        )
```

## License

MIT

## Support

For issues or questions, see the main manager-core documentation.
