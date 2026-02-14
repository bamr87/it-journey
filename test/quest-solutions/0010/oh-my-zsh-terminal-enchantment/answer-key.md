# Terminal Enchantment: Answer Key & Expected Outputs

**Quest**: Oh-My-Zsh Terminal Enchantment
**Purpose**: Reference answers for all challenges and expected validation outputs

> **Spoiler Warning**: This file contains solutions. Attempt the quest yourself first!

---

## Chapter 1: The Installation Ritual

### Expected State After Completion

```
~/.oh-my-zsh/           # Oh-My-Zsh framework directory
~/.zshrc                # New config from Oh-My-Zsh template
~/.zshrc.pre-oh-my-zsh  # Backup of original .zshrc
```

### Key Commands Used

```bash
# Download the install script
wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh

# Or with curl
curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -o install.sh

# Run unattended install
sh install.sh --unattended
```

---

## Chapter 2: Theme Configuration

### Expected .zshrc Theme Line

```bash
ZSH_THEME="agnoster"
```

### Verifying Theme

```bash
grep 'ZSH_THEME=' ~/.zshrc
# Expected output: ZSH_THEME="agnoster"
```

### Available Themes Count

```bash
ls ~/.oh-my-zsh/themes/ | wc -l
# Expected: ~143 themes (may vary by version)
```

---

## Chapter 3: Plugin Installation

### Expected Plugin List in .zshrc

```bash
plugins=(
  git
  docker
  vscode
  web-search
  colored-man-pages
  jsontools
  copypath
  zsh-autosuggestions
  zsh-syntax-highlighting
)
```

### External Plugins — Clone Commands

```bash
# zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions.git \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### Verifying External Plugins

```bash
ls ~/.oh-my-zsh/custom/plugins/
# Expected: zsh-autosuggestions  zsh-syntax-highlighting
```

### Expected Custom Aliases

```bash
# VSCode shortcuts
alias c="code ."
alias vsc="code --new-window"
alias zshconfig="code ~/.zshrc"
alias ohmyzsh="code ~/.oh-my-zsh"

# Git shortcuts
alias gs="git status"
alias glog="git log --oneline --graph --decorate -10"
alias gd="git diff"

# Navigation shortcuts
alias ll="ls -lah"
alias ..="cd .."
alias ...="cd ../.."
```

### Expected Custom Functions

```bash
# Project jumper — navigates to ~/github/<name>
function proj() { ... }

# Quick note taker — saves to ~/.dev-notes/YYYY-MM-DD.md
function note() { ... }

# Make directory and cd into it
function mkcd() { ... }
```

---

## Chapter 4: VSCode Integration

### Nerd Font Installation (macOS)

```bash
brew install --cask font-meslo-lg-nerd-font
# Expected: ~72 font files installed
```

### Expected VSCode settings.json Additions

```json
{
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.fontFamily": "MesloLGM Nerd Font Mono",
    "terminal.integrated.fontSize": 14,
    "terminal.integrated.cursorStyle": "line",
    "terminal.integrated.cursorWidth": 2
}
```

---

## Challenge Expected Outputs

### Challenge 1: Security Audit

See [security-audit.md](reports/security-audit.md) for full reference.

**Key findings to discover:**
- `set -e` for error handling
- `.zshrc.pre-oh-my-zsh` backup mechanism
- Sudo only for `chsh`
- No destructive `rm -rf` on user data

### Challenge 2: Theme Benchmark

See [theme-benchmark-results.md](reports/theme-benchmark-results.md) for reference values.

**Expected**: All themes under 50ms average prompt time.

### Challenge 3: Plugin Validation

```
=== Oh-My-Zsh Plugin Validation ===
✅ git - PASS
✅ docker - PASS
✅ vscode - PASS
✅ web-search - PASS
✅ colored-man-pages - PASS
✅ jsontools - PASS
✅ copypath - PASS
✅ zsh-autosuggestions - PASS
✅ zsh-syntax-highlighting - PASS

Results: 9 passed, 0 failed
🏆 All plugins validated!
```

### Challenge 4: VSCode Terminal Validation

```
=== VSCode Terminal Integration Validation ===
✅ Shell is zsh (/bin/zsh)
✅ Oh-My-Zsh installed at: /Users/<you>/.oh-my-zsh
✅ Theme configured: ZSH_THEME="agnoster"
✅ Nerd Fonts installed: 72 font files
✅ VSCode terminal font configured
✅ 10 custom aliases configured in .zshrc
✅ 3 custom functions in .zshrc
✅ TERM_PROGRAM detection (OK for script mode)

Score: 8 / 8 checks passed
🏆 Perfect integration!
```

---

## Boss Battle Expected Output

```
=== 🐉 BOSS BATTLE FINAL VALIDATION ===

--- Phase 1: Foundation (25 pts) ---
✅ Setup script exists and is executable (+5)
✅ Strict mode enabled (+5)
✅ Backup mechanism included (+5)
✅ Rollback capability (+10)

--- Phase 2: Enchantment (30 pts) ---
✅ 16 plugins configured (+10)
✅ 10 aliases active (+10)
✅ Custom functions found (+10)

--- Phase 3: Integration (20 pts) ---
✅ VSCode settings configured (+10)
✅ Health check script exists (+10)

--- Phase 4: Documentation (25 pts) ---
✅ Documentation exists (+10)
✅ Troubleshooting guide included (+5)
✅ Quick reference card included (+5)

===========================================
  FINAL SCORE: 95 / 100
===========================================
👑 LEGENDARY! You are a Terminal Archmage!
```

### Scoring Breakdown

| Phase | Max Points | What's Checked |
|-------|-----------|----------------|
| Foundation | 25 | Setup script, strict mode, backup, rollback |
| Enchantment | 30 | 7+ plugins, 5+ aliases, custom functions |
| Integration | 20 | VSCode settings, health check script |
| Documentation | 25 | Docs file, troubleshooting, quick reference |
| **Total** | **100** | |

### Rank Thresholds

| Score | Rank |
|-------|------|
| 95–100 | 👑 LEGENDARY — Terminal Archmage |
| 80–94 | 🏆 VICTORY — Boss Defeated |
| 60–79 | ⚔️ Good Fight — Almost There |
| < 60 | 🛡️ Keep Questing |
