#!/usr/bin/env python3
"""
System Configuration Mappings

Ultra-simplified Python-based configuration mappings using named tuples.
Version 3.0 - Named tuple format (no type field, inline groups).
"""

from typing import NamedTuple, Optional

# Metadata
METADATA = {
    "version": "3.0",
    "description": "Ultra-simplified configuration mappings using named tuples",
    "last_updated": "2025-01-04",
    "migrated_from": "dict-based format (v2.0)",
}


# Configuration definition using named tuple
class Config(NamedTuple):
    """
    Configuration definition using named tuple.

    Args:
        name: Configuration identifier
        source: Path in konfig (relative to konfig root)
        target: System path (absolute or with ~/)
        group: Group name (for organization)
        display_name: Human-readable name (optional)
        requires_sudo: Whether sudo is required (optional, auto-detected)
    """

    name: str
    source: str
    target: str
    group: str
    display_name: Optional[str] = None
    requires_sudo: Optional[bool] = None

    def get_display_name(self):
        """Get display name with fallback to formatted name"""
        return (
            self.display_name or self.name.replace("-", " ").replace("_", " ").title()
        )


# Group descriptions (optional - for CLI help text)
GROUP_DESCRIPTIONS = {
    "hyprland": "Hyprland window manager and related components",
    "sudo": "Configurations requiring sudo privileges",
    "main": "Core system configurations",
    "themes": "System theming configurations",
    "shell": "Shell and terminal configurations",
    "code": "VSCode based editors configurations",
    "tmux": "Tmux terminal multiplexer",
    "others": "Other development tools",
}

# All configurations in simple list format
CONFIGS = [
    ############################################################
    # Hyprland ecosystem - Window manager and related components
    ##########
    Config("hyprland", "hypr", "~/.config/hypr", "hyprland", "Hyprland"),
    Config(
        "hyprshade",
        "hyprshade",
        "/usr/share/hyprshade",
        "hyprland",
        "Hyprshade",
        requires_sudo=True,
    ),
    Config("swaync", "swaync", "~/.config/swaync", "hyprland", "Swaync"),
    Config("waybar", "waybar", "~/.config/waybar", "hyprland", "Waybar"),
    Config("rofi", "rofi", "~/.config/rofi", "hyprland", "Rofi"),
    Config("wallust", "wallust", "~/.config/wallust", "hyprland", "Wallust"),
    Config("kitty", "kitty", "~/.config/kitty", "hyprland", "Kitty"),
    ############################################################
    # System themes - GTK, fonts, icons, wallpapers
    ##########
    Config("icons", "themes/icons", "~/.icons", "themes", "Icons"),
    Config("fonts", "themes/fonts", "~/.local/share/fonts", "themes", "Fonts"),
    Config("gtk-2.0", "themes/gtk-2.0", "~/.config/gtk-2.0", "themes", "GTK 2.0"),
    Config("gtk-3.0", "themes/gtk-3.0", "~/.config/gtk-3.0", "themes", "GTK 3.0"),
    Config("gtk-4.0", "themes/gtk-4.0", "~/.config/gtk-4.0", "themes", "GTK 4.0"),
    Config("kvantum", "themes/kvantum", "~/.config/Kvantum", "themes", "Kvantum"),
    Config("themes", "themes/themes", "~/.themes", "themes", "Themes"),
    # Config('wallpapers', 'themes/wallpapers', '~/Pictures/wallpapers', 'themes', 'Wallpapers'),
    ############################################################
    # System configurations requiring sudo
    ##########
    Config("keyd", "keyd", "/etc/keyd", "sudo", "Keyd", requires_sudo=True),
    ############################################################
    # Core system configurations
    ##########
    Config("rclone", "rclone", "~/.config/rclone", "main", "Rclone"),
    Config("gitconfig", ".gitconfig", "~/.gitconfig", "main", "Git Config"),
    Config(
        "git-credentials",
        ".git-credentials",
        "~/.git-credentials",
        "main",
        "Git Credentials",
    ),
    Config("aws", "aws", "~/.aws", "main", "AWS"),
    ############################################################
    # Shell configurations
    ##########
    Config("zsh", ".zshrc", "~/.zshrc", "shell", "Zsh"),
    Config(
        "zsh-custom", "zsh/custom", "~/.oh-my-zsh/custom", "shell", "Zsh Custom Folder"
    ),
    Config("p10k", ".p10k.zsh", "~/.p10k.zsh", "shell", "P10K"),
    Config("nvim", "nvim", "~/.config/nvim", "shell", "Nvim"),
    Config("fish-shell", "fish", "~/.config/fish", "shell"),
    Config(
        "starship",
        "starship/starship.toml",
        "~/.config/starship.toml",
        "shell",
        "Starship",
    ),
    Config("lazygit", "lazygit", "~/.config/lazygit", "shell", "Lazygit"),
    ############################################################
    # Agents configurations
    ##########
    Config(
        "opencode",
        "opencode/opencode.json",
        "~/.config/opencode/opencode.json",
        "agents",
        "OpenCode",
    ),
    Config(
        "opencode agents",
        "opencode/agent",
        "~/.config/opencode/agent",
        "agents",
        "OpenCode Agents",
    ),
    Config(
        "opencode skill",
        "opencode/skill",
        "~/.config/opencode/skill",
        "agents",
        "OpenCode Skills",
    ),
    Config(
        "opencode themes",
        "opencode/themes",
        "~/.config/opencode/themes",
        "agents",
        "OpenCode Themes",
    ),
    Config(
        "claude",
        "opencode/agent/architect.md",
        "~/.claude/CLAUDE.md",
        "agents",
        "Claude Main Agent (opencode arch)",
    ),
    Config(
        "claude agents", "opencode/agent", "~/.claude/agents", "agents", "Claude Agents"
    ),
    Config(
        "claude skill", "opencode/skill", "~/.claude/skills", "agents", "Claude Skills"
    ),
    ############################################################
    # Terminal multiplexer
    ##########
    Config("tmux-config", "tmux/tmux.conf", "~/.tmux.conf", "tmux", "Tmux"),
    Config("tmux-plugins", "tmux/tmux", "~/.tmux", "tmux", "Tmux Plugins"),
    ############################################################
    # Editor configurations
    ##########
    Config(
        "windsurf-keybindings",
        "code/keybindings.json",
        "~/.config/Windsurf/User/keybindings.json",
        "code",
        "Windsurf Keybindings",
    ),
    Config(
        "windsurf-settings",
        "code/settings.json",
        "~/.config/Windsurf/User/settings.json",
        "code",
        "Windsurf Settings",
    ),
    Config(
        "vscode-keybindings",
        "code/keybindings.json",
        "~/.config/Code/User/keybindings.json",
        "code",
        "VSCode Keybindings",
    ),
    Config(
        "vscode-settings",
        "code/settings.json",
        "~/.config/Code/User/settings.json",
        "code",
        "VSCode Settings",
    ),
    Config(
        "antigravity-keybindings",
        "code/keybindings.json",
        "~/.config/Antigravity/User/keybindings.json",
        "code",
        "Google Antigravity Keybindings",
    ),
    Config(
        "antigravity-settings",
        "code/settings.json",
        "~/.config/Antigravity/User/settings.json",
        "code",
        "Google Antigravity Settings",
    ),
    ############################################################
    # Other development tools
    ##########
    Config("idea-vim", ".ideavimrc", "~/.ideavimrc", "others", "IDEA Vim"),
    Config(
        "obsidian-vim",
        ".obsidian.vimrc",
        "~/Documents/Zettelkasten/.obsidian.vimrc",
        "others",
        "Obsidian Vim",
    ),
]


# Helper function for backward compatibility
def get_config_data():
    """
    Return configuration data in old dict format for backward compatibility.

    This converts the new named tuple format back to the old dict format
    for any code that still expects it.
    """
    configurations = {}
    groups = {}

    # Convert Config named tuples to dict format
    for config in CONFIGS:
        configurations[config.name] = {
            "source": config.source,
            "target": config.target,
            "type": "file",  # Default value for backward compatibility
            "display_name": config.display_name or config.get_display_name(),
            "group": config.group,
        }
        if config.requires_sudo:
            configurations[config.name]["requires_sudo"] = config.requires_sudo

    # Build groups from configs
    for config in CONFIGS:
        if config.group not in groups:
            groups[config.group] = {
                "description": GROUP_DESCRIPTIONS.get(config.group, ""),
                "configurations": [],
            }
        groups[config.group]["configurations"].append(config.name)

    return {"metadata": METADATA, "configurations": configurations, "groups": groups}
