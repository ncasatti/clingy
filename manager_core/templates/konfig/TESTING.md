# Konfig Template Testing Checklist

## Setup
- [ ] `manager init --template konfig` creates project
- [ ] Edit `config.py` - set KONFIG_PATH to ~/.config/konfig (or test path)
- [ ] `manager` shows main menu with Browse, Quick Actions, Status

## Browse Command
- [ ] Browse → By Group shows all groups (Hyprland, Themes, Shell, etc.)
- [ ] Config items show correct status icons (✓ ✗ ⚠ 🔗 📁)
- [ ] Can select and link single config
- [ ] Can unlink single config
- [ ] "Link All in Group" links all configs in group
- [ ] "Unlink All in Group" unlinks all configs

## Quick Actions
- [ ] "Link All" shows confirmation and links all
- [ ] "Unlink All" shows confirmation and unlinks all
- [ ] "Status Summary" shows table with counts
- [ ] "Verify Integrity" detects broken symlinks

## Status Command
- [ ] "Full Status Table" shows all configs with icons
- [ ] "Groups Summary" shows counts per group
- [ ] "Problems Only" filters to show only issues

## Edge Cases
- [ ] Missing source (konfig file doesn't exist) → shows warning
- [ ] Conflict (target exists as regular file) → shows options
- [ ] Broken symlink detection works
- [ ] Sudo configs (e.g., /etc/keyd) → prompts for password
- [ ] ESC key navigates back correctly

## Integration
- [ ] Works from subdirectories (context detection)
- [ ] Multiple links/unlinks in sequence work
- [ ] No crashes or errors during navigation
