#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Terminal Enchantment: Oh-My-Zsh Setup Script
# Quest: Terminal Enchantment — Boss Battle (Phase 1-3)
# =============================================================================
# Automates Oh-My-Zsh installation, theme configuration, plugin setup,
# custom aliases/functions, and VSCode integration.
#
# Usage:
#   ./setup-terminal.sh           # Full install
#   ./setup-terminal.sh --dry-run # Preview what would happen
#   ./setup-terminal.sh --rollback <backup-dir>  # Restore previous config
# =============================================================================

DRY_RUN=false
ROLLBACK_DIR=""
BACKUP_DIR=""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }
log_step()  { echo -e "${BLUE}[STEP]${NC} $*"; }

# ---- Argument Parsing ----
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dry-run) DRY_RUN=true; shift ;;
            --rollback) ROLLBACK_DIR="$2"; shift 2 ;;
            --help|-h)
                echo "Usage: $0 [--dry-run] [--rollback <backup-dir>]"
                echo ""
                echo "Options:"
                echo "  --dry-run              Preview changes without applying"
                echo "  --rollback <dir>       Restore config from backup directory"
                echo "  --help, -h             Show this help message"
                exit 0
                ;;
            *) log_error "Unknown argument: $1"; exit 1 ;;
        esac
    done
}

# ---- Pre-flight Checks ----
check_prerequisites() {
    log_step "Running pre-flight checks..."
    local ok=true

    command -v zsh >/dev/null 2>&1 || { log_error "zsh is required but not installed"; ok=false; }
    command -v git >/dev/null 2>&1 || { log_error "git is required but not installed"; ok=false; }
    command -v curl >/dev/null 2>&1 || { log_error "curl is required but not installed"; ok=false; }

    # Internet connectivity
    if curl -s --connect-timeout 5 --head https://github.com | head -1 | grep -qE "200|301|302"; then
        log_info "Internet connectivity: OK"
    else
        log_error "Cannot reach github.com — check your internet connection"
        ok=false
    fi

    # Zsh version
    local zsh_ver
    zsh_ver=$(zsh --version | awk '{print $2}')
    log_info "Zsh version: $zsh_ver"

    if [[ "$ok" == "false" ]]; then
        log_error "Pre-flight checks failed. Aborting."
        exit 1
    fi

    log_info "✅ All pre-flight checks passed"
}

# ---- Backup ----
backup_config() {
    BACKUP_DIR="$HOME/.zsh-backup-$(date +%Y%m%d%H%M%S)"
    log_step "Backing up existing config to $BACKUP_DIR"

    if $DRY_RUN; then
        log_info "[DRY-RUN] Would create backup at $BACKUP_DIR"
        return
    fi

    mkdir -p "$BACKUP_DIR"
    [[ -f ~/.zshrc ]] && cp ~/.zshrc "$BACKUP_DIR/zshrc.bak"
    [[ -d ~/.oh-my-zsh ]] && cp -r ~/.oh-my-zsh "$BACKUP_DIR/oh-my-zsh.bak"
    log_info "📦 Backup saved to: $BACKUP_DIR"
}

# ---- Rollback ----
rollback() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        log_error "Backup directory not found: $dir"
        exit 1
    fi

    log_step "Rolling back from $dir..."
    [[ -f "$dir/zshrc.bak" ]] && cp "$dir/zshrc.bak" ~/.zshrc && log_info "Restored .zshrc"
    if [[ -d "$dir/oh-my-zsh.bak" ]]; then
        rm -rf ~/.oh-my-zsh
        cp -r "$dir/oh-my-zsh.bak" ~/.oh-my-zsh
        log_info "Restored .oh-my-zsh directory"
    fi
    log_info "✅ Rollback complete"
    exit 0
}

# ---- Oh-My-Zsh Installation ----
install_omz() {
    log_step "Installing Oh-My-Zsh..."

    if [[ -d "$HOME/.oh-my-zsh" ]]; then
        log_info "Oh-My-Zsh already installed — skipping"
        return
    fi

    if $DRY_RUN; then
        log_info "[DRY-RUN] Would install Oh-My-Zsh"
        return
    fi

    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    log_info "✅ Oh-My-Zsh installed"
}

# ---- External Plugins ----
install_plugins() {
    log_step "Installing external plugins..."

    local custom_dir="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

    local plugins=(
        "zsh-users/zsh-autosuggestions"
        "zsh-users/zsh-syntax-highlighting"
    )

    for plugin in "${plugins[@]}"; do
        local name="${plugin##*/}"
        local dest="$custom_dir/plugins/$name"
        if [[ -d "$dest" ]]; then
            log_info "$name already installed — skipping"
        elif $DRY_RUN; then
            log_info "[DRY-RUN] Would clone $plugin to $dest"
        else
            git clone "https://github.com/$plugin.git" "$dest" 2>/dev/null
            log_info "✅ Installed $name"
        fi
    done
}

# ---- Nerd Font ----
install_nerd_font() {
    log_step "Checking Nerd Font..."

    if [[ "$(uname)" == "Darwin" ]]; then
        local font_count
        font_count=$(ls ~/Library/Fonts/ 2>/dev/null | grep -ci "nerd" || echo 0)

        if [[ $font_count -gt 0 ]]; then
            log_info "Nerd Font already installed ($font_count files) — skipping"
            return
        fi

        if $DRY_RUN; then
            log_info "[DRY-RUN] Would install font-meslo-lg-nerd-font via brew"
            return
        fi

        if command -v brew >/dev/null 2>&1; then
            brew install --cask font-meslo-lg-nerd-font
            log_info "✅ MesloLG Nerd Font installed"
        else
            log_warn "Homebrew not found — install Nerd Fonts manually from https://www.nerdfonts.com"
        fi
    elif [[ "$(uname)" == "Linux" ]]; then
        log_info "Linux detected — install Nerd Fonts manually:"
        log_info "  https://www.nerdfonts.com/font-downloads → MesloLG Nerd Font"
        log_info "  Extract to ~/.local/share/fonts/ and run: fc-cache -fv"
    fi
}

# ---- Configure .zshrc ----
configure_zshrc() {
    log_step "Configuring .zshrc with theme, plugins, aliases, and functions..."

    if $DRY_RUN; then
        log_info "[DRY-RUN] Would configure .zshrc with agnoster theme, 9 plugins, aliases, functions"
        return
    fi

    # Set theme
    sed -i '' 's/^ZSH_THEME=.*/ZSH_THEME="agnoster"/' ~/.zshrc

    # Set plugins
    sed -i '' '/^plugins=(/,/^)/c\
plugins=(\
  git\
  docker\
  vscode\
  web-search\
  colored-man-pages\
  jsontools\
  copypath\
  zsh-autosuggestions\
  zsh-syntax-highlighting\
)' ~/.zshrc

    # Append custom aliases and functions if not already present
    if ! grep -q '# === IT-Journey Terminal Enchantment ===' ~/.zshrc; then
        cat >> ~/.zshrc << 'CUSTOM'

# === IT-Journey Terminal Enchantment ===

# VSCode shortcuts
alias c="code ."
alias vsc="code --new-window"
alias zshconfig="code ~/.zshrc"
alias ohmyzsh="code ~/.oh-my-zsh"

# Git workflow shortcuts
alias gs="git status"
alias glog="git log --oneline --graph --decorate -10"
alias gd="git diff"

# Navigation shortcuts
alias ll="ls -lah"
alias ..="cd .."
alias ...="cd ../.."

# Project directory jumper
function proj() {
    local projects_dir="$HOME/github"
    if [[ -z "$1" ]]; then
        echo "Available projects:"
        ls -1 "$projects_dir" 2>/dev/null || echo "No projects found"
    elif [[ -d "$projects_dir/$1" ]]; then
        cd "$projects_dir/$1" && echo "📂 Jumped to $1"
    else
        echo "❌ Project '$1' not found"
    fi
}

# Quick note taker
function note() {
    local notes_dir="$HOME/.dev-notes"
    mkdir -p "$notes_dir"
    local today="$(date +%Y-%m-%d)"
    echo "[$(date +%H:%M)] $*" >> "$notes_dir/$today.md"
    echo "📝 Note saved to $notes_dir/$today.md"
}

# Make directory and cd into it
function mkcd() {
    mkdir -p "$1" && cd "$1"
}

# PATH additions
export PATH="$HOME/.local/bin:$PATH"
# === End IT-Journey Terminal Enchantment ===
CUSTOM
        log_info "✅ Custom aliases and functions added"
    else
        log_info "Custom config already present — skipping"
    fi
}

# ---- VSCode Settings ----
configure_vscode() {
    log_step "Configuring VSCode terminal settings..."

    local settings_file
    if [[ "$(uname)" == "Darwin" ]]; then
        settings_file="$HOME/Library/Application Support/Code/User/settings.json"
    elif [[ "$(uname)" == "Linux" ]]; then
        settings_file="$HOME/.config/Code/User/settings.json"
    else
        log_warn "Unsupported OS for VSCode auto-config — configure manually"
        return
    fi

    if $DRY_RUN; then
        log_info "[DRY-RUN] Would update VSCode settings at $settings_file"
        return
    fi

    if [[ ! -f "$settings_file" ]]; then
        mkdir -p "$(dirname "$settings_file")"
        echo '{}' > "$settings_file"
    fi

    python3 << 'PYEOF'
import json, os

if os.uname().sysname == "Darwin":
    settings_path = os.path.expanduser("~/Library/Application Support/Code/User/settings.json")
else:
    settings_path = os.path.expanduser("~/.config/Code/User/settings.json")

with open(settings_path, 'r') as f:
    settings = json.load(f)

terminal_settings = {
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.fontFamily": "MesloLGM Nerd Font Mono",
    "terminal.integrated.fontSize": 14,
    "terminal.integrated.cursorStyle": "line",
    "terminal.integrated.cursorWidth": 2
}

settings.update(terminal_settings)

with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=4)

print("VSCode settings updated successfully")
PYEOF

    log_info "✅ VSCode terminal configured with Nerd Font"
}

# ---- Health Check ----
health_check() {
    log_step "Running health check..."
    echo ""

    local score=0
    local total=8

    [[ -d "$HOME/.oh-my-zsh" ]] && { echo "✅ Oh-My-Zsh installed"; ((score++)); } || echo "❌ Oh-My-Zsh missing"
    grep -q 'ZSH_THEME="agnoster"' ~/.zshrc 2>/dev/null && { echo "✅ Theme: agnoster"; ((score++)); } || echo "❌ Theme not set"
    [[ -d "$HOME/.oh-my-zsh/custom/plugins/zsh-autosuggestions" ]] && { echo "✅ zsh-autosuggestions"; ((score++)); } || echo "❌ zsh-autosuggestions missing"
    [[ -d "$HOME/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting" ]] && { echo "✅ zsh-syntax-highlighting"; ((score++)); } || echo "❌ zsh-syntax-highlighting missing"

    local plugin_count
    plugin_count=$(grep -A20 'plugins=(' ~/.zshrc | grep -c '[a-z]' 2>/dev/null || echo 0)
    [[ $plugin_count -ge 7 ]] && { echo "✅ $plugin_count plugins configured"; ((score++)); } || echo "❌ Only $plugin_count plugins"

    local alias_count
    alias_count=$(grep -c '^alias ' ~/.zshrc 2>/dev/null || echo 0)
    [[ $alias_count -ge 5 ]] && { echo "✅ $alias_count aliases"; ((score++)); } || echo "❌ Only $alias_count aliases"

    local func_count
    func_count=$(grep -c '^function ' ~/.zshrc 2>/dev/null || echo 0)
    [[ $func_count -ge 2 ]] && { echo "✅ $func_count custom functions"; ((score++)); } || echo "❌ Only $func_count functions"

    local nerd_fonts=0
    if [[ "$(uname)" == "Darwin" ]]; then
        nerd_fonts=$(ls ~/Library/Fonts/ 2>/dev/null | grep -ci "nerd" || echo 0)
    fi
    [[ $nerd_fonts -gt 0 ]] && { echo "✅ Nerd Font installed ($nerd_fonts files)"; ((score++)); } || echo "❌ No Nerd Font"

    echo ""
    echo "Health Check Score: $score / $total"
    [[ $score -eq $total ]] && echo "🏆 Perfect health!" || echo "⚠️ Address failing checks"
}

# ---- Main ----
main() {
    parse_args "$@"

    echo "============================================"
    echo "🏰 Terminal Enchantment: Oh-My-Zsh Setup"
    echo "============================================"
    echo ""

    if [[ -n "$ROLLBACK_DIR" ]]; then
        rollback "$ROLLBACK_DIR"
    fi

    $DRY_RUN && log_warn "DRY-RUN MODE — no changes will be made"

    check_prerequisites
    backup_config
    install_omz
    install_plugins
    install_nerd_font
    configure_zshrc
    configure_vscode
    health_check

    echo ""
    if $DRY_RUN; then
        log_info "Dry run complete. Re-run without --dry-run to apply changes."
    else
        log_info "🎉 Terminal enchantment complete! Run 'source ~/.zshrc' or open a new terminal."
    fi
}

main "$@"
