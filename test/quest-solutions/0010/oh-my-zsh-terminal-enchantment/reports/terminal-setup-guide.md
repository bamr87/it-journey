# Terminal Enchantment: Setup Guide & Reference

**Quest**: Terminal Enchantment — Boss Battle (Phase 4 Documentation)
**Purpose**: Comprehensive onboarding document for team terminal setup

---

## Quick Start

```bash
# Full automated setup
chmod +x setup-terminal.sh
./setup-terminal.sh

# Preview what will happen (no changes made)
./setup-terminal.sh --dry-run

# Rollback to previous config
./setup-terminal.sh --rollback ~/.zsh-backup-YYYYMMDDHHMMSS
```

## What Gets Installed

| Component | Description |
|-----------|-------------|
| **Oh-My-Zsh** | Zsh framework with 300+ plugins and 140+ themes |
| **Theme: agnoster** | Clean, informative prompt with git status |
| **MesloLG Nerd Font** | Patched font with icons for terminal themes |
| **9 plugins** | git, docker, vscode, web-search, colored-man-pages, jsontools, copypath, zsh-autosuggestions, zsh-syntax-highlighting |
| **10 aliases** | VSCode, git, and navigation shortcuts |
| **3 functions** | `proj`, `note`, `mkcd` |
| **VSCode config** | Terminal font and cursor settings |

## Custom Aliases

| Alias | Command | Description |
|-------|---------|-------------|
| `c` | `code .` | Open current dir in VSCode |
| `vsc` | `code --new-window` | Open new VSCode window |
| `zshconfig` | `code ~/.zshrc` | Edit zsh config in VSCode |
| `ohmyzsh` | `code ~/.oh-my-zsh` | Browse Oh-My-Zsh in VSCode |
| `gs` | `git status` | Quick git status |
| `glog` | `git log --oneline --graph --decorate -10` | Pretty git log |
| `gd` | `git diff` | Quick git diff |
| `ll` | `ls -lah` | Detailed file listing |
| `..` | `cd ..` | Go up one directory |
| `...` | `cd ../..` | Go up two directories |

## Custom Functions

### `proj [name]` — Project Jumper
```bash
proj              # List projects in ~/github/
proj it-journey   # Jump to ~/github/it-journey
```

### `note <message>` — Quick Note Taker
```bash
note Fixed the login bug    # Saves timestamped note to ~/.dev-notes/YYYY-MM-DD.md
```

### `mkcd <dir>` — Make & Enter Directory
```bash
mkcd new-project    # Creates and enters new-project/
```

## Troubleshooting

### 1. Icons show as boxes or question marks
**Cause**: Nerd Font not configured in terminal
**Fix**: Set terminal font to "MesloLGM Nerd Font Mono" in:
- VSCode: Settings → `terminal.integrated.fontFamily`
- iTerm2: Profiles → Text → Font
- Terminal.app: Preferences → Profiles → Font

### 2. `command not found: omz` after installation
**Cause**: Shell session wasn't reloaded
**Fix**: Run `source ~/.zshrc` or open a new terminal window

### 3. Plugins not loading
**Cause**: Plugin name typo or missing external plugin
**Fix**:
```bash
# Check plugin list
grep -A15 'plugins=(' ~/.zshrc

# Verify external plugins exist
ls ~/.oh-my-zsh/custom/plugins/
```

### 4. Slow shell startup
**Cause**: Too many plugins or slow plugin
**Fix**: Profile startup time:
```bash
time zsh -ic exit    # Should be < 500ms
```
Remove unused plugins from the `plugins=()` list.

### 5. Theme not rendering correctly in VSCode
**Cause**: VSCode using default font instead of Nerd Font
**Fix**: Verify settings:
```json
{
    "terminal.integrated.fontFamily": "MesloLGM Nerd Font Mono",
    "terminal.integrated.fontSize": 14
}
```

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│  Oh-My-Zsh Quick Reference                  │
├─────────────────────────────────────────────┤
│  NAVIGATION                                  │
│  ..       Go up one directory               │
│  ...      Go up two directories             │
│  ll       Detailed file listing             │
│  proj X   Jump to ~/github/X                │
│  mkcd X   Create & enter directory          │
├─────────────────────────────────────────────┤
│  GIT (Oh-My-Zsh aliases)                    │
│  gst      git status                        │
│  ga .     git add all                        │
│  gc -m    git commit -m                      │
│  gp       git push                           │
│  gl       git pull                           │
│  glog     Pretty git log (custom)            │
├─────────────────────────────────────────────┤
│  VSCODE                                      │
│  c        Open current dir in VSCode         │
│  vsc      New VSCode window                  │
│  zshconfig  Edit .zshrc in VSCode            │
├─────────────────────────────────────────────┤
│  UTILITIES                                   │
│  note X   Save timestamped note              │
│  web_search google "query"  Web search       │
│  pp_json  Pretty-print JSON (pipe into it)   │
└─────────────────────────────────────────────┘
```

## Files Modified

| File | Change |
|------|--------|
| `~/.zshrc` | Theme, plugins, aliases, functions |
| `~/.zshrc.pre-oh-my-zsh` | Backup of original config |
| `~/.oh-my-zsh/` | Oh-My-Zsh framework |
| `~/.oh-my-zsh/custom/plugins/` | External plugins |
| `~/Library/Fonts/` (macOS) | MesloLG Nerd Font files |
| VSCode `settings.json` | Terminal font and cursor settings |

## Validation

Run validation scripts to verify your setup:
```bash
# Full health check (built into setup script)
./setup-terminal.sh --dry-run

# Plugin validation
zsh validate-plugins.sh

# VSCode integration validation
zsh validate-vscode-terminal.sh

# Boss Battle final score
zsh boss-battle-validate.sh
```
