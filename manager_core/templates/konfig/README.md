# Konfig Manager Template

Interactive symlink manager for Linux dotfiles and system configurations.

## Overview

Konfig Manager helps you manage system configuration files through symlinks, organizing them in a central repository (~/.config/konfig) and linking them to their system locations.

## Quick Start

### 1. Initialize Project

```bash
cd ~/my-konfig-project
manager init --template konfig
```

### 2. Configure Paths

Edit `config.py`:
```python
KONFIG_PATH = "~/.config/konfig"  # Your konfig repository
```

### 3. Define Your Configurations

Edit `mappings.py` to add your configs:
```python
from mappings import Config

CONFIGS = [
    Config('nvim', 'nvim', '~/.config/nvim', 'shell', 'Neovim'),
    Config('zshrc', '.zshrc', '~/.zshrc', 'shell', 'Zsh Config'),
    # ... add more configs
]
```

### 4. Run Interactive Menu

```bash
manager
```

## Configuration Format

```python
Config(
    name='identifier',           # Unique ID
    source='path/in/konfig',     # Relative to KONFIG_PATH
    target='~/target/path',      # System location
    group='category',            # Group for organization
    display_name='Display Name', # Optional, shown in menus
    requires_sudo=False          # Optional, auto-detected
)
```

## Features

### Browse Configurations
- Navigate by group (Hyprland, Themes, Shell, etc.)
- View all configurations in flat list
- Visual status indicators

### Quick Actions
- Link all configurations at once
- Unlink all configurations
- View status summary table
- Verify symlink integrity

### Status Icons

| Icon | Meaning |
|------|---------|
| ✓ (green) | Symlink exists and points correctly |
| ✗ (red) | Not linked |
| ⚠ (yellow) | Conflict: file/dir exists (not a symlink) |
| 🔗 (cyan) | Symlink exists but points to wrong target |
| 📁 (gray) | Source file missing in konfig |

## Groups

Organize configs into logical groups:
- **hyprland**: Window manager and related tools
- **themes**: GTK, icons, fonts, wallpapers
- **shell**: Zsh, Bash, Nvim, Starship
- **main**: Core configs (Git, AWS, Rclone)
- **sudo**: Configs requiring root (e.g., /etc/keyd)
- **code**: VSCode, Windsurf, IDEs
- **tmux**: Terminal multiplexer
- **agents**: AI assistants (Claude, OpenCode)
- **others**: Miscellaneous tools

## Workflows

### Link Specific Group
1. `manager` → Browse → By Group
2. Select group (e.g., "Hyprland")
3. Choose "Link All in Group"

### Link Individual Config
1. `manager` → Browse → By Group → Hyprland
2. Select config (e.g., "hyprland")
3. Automatically links if not already linked

### Check Status
1. `manager` → Quick Actions → Show Status Summary
2. View table with counts per status type

### Verify Integrity
1. `manager` → Quick Actions → Verify Integrity
2. Detects broken symlinks and issues

## Conflict Resolution

When a target file/directory already exists:
1. **Backup and Replace**: Moves existing to `.backup`
2. **Skip**: Leaves existing file unchanged
3. **Abort**: Cancels the operation

## Sudo Configs

Configs targeting `/etc/` or `/usr/` automatically require sudo:
```python
Config('keyd', 'keyd', '/etc/keyd', 'sudo', 'Keyd', requires_sudo=True)
```

Password will be prompted when linking/unlinking.

## Tips

- **Test first**: Use a test directory to verify configs before production
- **Backup important files**: Always backup before linking
- **Group wisely**: Organize configs by functionality for easier navigation
- **Use descriptive names**: Make display_name clear and searchable

## Troubleshooting

### "No manager project found"
- Make sure you ran `manager init --template konfig`
- Check you're in the project directory (or subdirectory)

### "Template 'konfig' not found"
- Ensure manager-core is up to date: `pip install --upgrade manager-core`

### "Source file missing"
- Check `KONFIG_PATH` in `config.py` is correct
- Verify source files exist in `~/.config/konfig/`

### Symlink permission denied
- Configs targeting `/etc/` or `/usr/` require sudo
- System will prompt for password automatically

## Example mappings.py

See the included `mappings.py` for a complete example with 50+ configurations covering Hyprland, themes, shell tools, and development environments.
