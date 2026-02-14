#!/usr/bin/env zsh
# =============================================================================
# Boss Battle Final Validation Script
# Quest: Terminal Enchantment — Boss Battle
# Purpose: Comprehensive scoring of all quest deliverables
# Usage: zsh boss-battle-validate.sh
# Expected: 95/100 for LEGENDARY, 80+ for VICTORY
# =============================================================================

echo "=== 🐉 BOSS BATTLE FINAL VALIDATION ==="
echo "Quest: Terminal Enchantment"
echo "Date: $(date)"
echo ""

score=0

echo "--- Phase 1: Foundation (25 pts) ---"

if [[ -x ~/setup-terminal.sh ]]; then
    echo "✅ Setup script exists and is executable (+5)"
    score=$((score + 5))
else
    echo "❌ Setup script missing or not executable"
fi

if grep -q 'set -euo pipefail' ~/setup-terminal.sh 2>/dev/null; then
    echo "✅ Strict mode enabled (+5)"
    score=$((score + 5))
else
    echo "❌ No strict mode (set -euo pipefail)"
fi

if grep -q 'backup' ~/setup-terminal.sh 2>/dev/null; then
    echo "✅ Backup mechanism included (+5)"
    score=$((score + 5))
else
    echo "❌ No backup mechanism"
fi

if grep -q 'rollback' ~/setup-terminal.sh 2>/dev/null; then
    echo "✅ Rollback capability (+10)"
    score=$((score + 10))
else
    echo "❌ No rollback support"
fi

echo ""
echo "--- Phase 2: Enchantment (30 pts) ---"

plugin_count=$(grep -A20 'plugins=(' ~/.zshrc | grep -c '[a-z]' 2>/dev/null || echo 0)
if [[ $plugin_count -ge 7 ]]; then
    echo "✅ $plugin_count plugins configured (+10)"
    score=$((score + 10))
else
    echo "❌ Only $plugin_count plugins (need 7+)"
fi

alias_count=$(grep -c '^alias ' ~/.zshrc 2>/dev/null || echo 0)
if [[ $alias_count -ge 5 ]]; then
    echo "✅ $alias_count aliases active (+10)"
    score=$((score + 10))
else
    echo "❌ Only $alias_count aliases (need 5+)"
fi

if grep -q '^function ' ~/.zshrc 2>/dev/null; then
    echo "✅ Custom functions found (+10)"
    score=$((score + 10))
else
    echo "❌ No custom functions in .zshrc"
fi

echo ""
echo "--- Phase 3: Integration (20 pts) ---"

if [[ "$(uname)" == "Darwin" ]]; then
    settings_file="$HOME/Library/Application Support/Code/User/settings.json"
elif [[ "$(uname)" == "Linux" ]]; then
    settings_file="$HOME/.config/Code/User/settings.json"
else
    settings_file="$APPDATA/Code/User/settings.json"
fi

if [[ -f "$settings_file" ]] && grep -q 'fontFamily' "$settings_file" 2>/dev/null; then
    echo "✅ VSCode settings configured (+10)"
    score=$((score + 10))
else
    echo "❌ VSCode settings missing"
fi

if [[ -x ~/validate-vscode-terminal.sh ]] || [[ -x ~/validate-plugins.sh ]]; then
    echo "✅ Health check script exists (+10)"
    score=$((score + 10))
else
    echo "❌ Health check script missing"
fi

echo ""
echo "--- Phase 4: Documentation (25 pts) ---"

if [[ -f ~/TERMINAL-SETUP.md ]]; then
    echo "✅ Documentation exists (+10)"
    score=$((score + 10))
else
    echo "❌ Documentation file missing"
fi

if grep -q 'Troubleshooting' ~/TERMINAL-SETUP.md 2>/dev/null; then
    echo "✅ Troubleshooting guide included (+5)"
    score=$((score + 5))
else
    echo "❌ No troubleshooting section"
fi

if grep -q 'Quick Reference' ~/TERMINAL-SETUP.md 2>/dev/null; then
    echo "✅ Quick reference card included (+5)"
    score=$((score + 5))
else
    echo "❌ No quick reference section"
fi

# Bonus: Check for rollback-tested backup directories
backup_count=$(ls -d ~/.zsh-backup-* 2>/dev/null | wc -l | tr -d ' ')
if [[ $backup_count -gt 0 ]]; then
    echo "✅ Backup directories found: $backup_count (+5 bonus)"
    score=$((score + 5))
fi

echo ""
echo "==========================================="
echo "  FINAL SCORE: $score / 100"
echo "==========================================="

if [[ $score -ge 95 ]]; then
    echo "👑 LEGENDARY! You are a Terminal Archmage!"
elif [[ $score -ge 80 ]]; then
    echo "🏆 VICTORY! The Boss is defeated!"
elif [[ $score -ge 60 ]]; then
    echo "⚔️ Good fight! Almost there — review the failing sections."
else
    echo "🛡️ Keep questing, adventurer! Revisit the chapters above."
fi
