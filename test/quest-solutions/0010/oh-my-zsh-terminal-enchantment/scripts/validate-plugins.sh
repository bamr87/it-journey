#!/usr/bin/env zsh
# =============================================================================
# Oh-My-Zsh Plugin Validation Script
# Quest: Terminal Enchantment — Challenge 3
# Purpose: Validates all 9 plugins are installed and accessible
# Usage: zsh validate-plugins.sh
# Expected: 9/9 plugins pass
# =============================================================================

echo "=== Oh-My-Zsh Plugin Validation ==="
echo "Quest: Terminal Enchantment — Challenge 3"
echo "Date: $(date)"
echo ""

passed=0
failed=0

check_plugin() {
    local name="$1"
    local test_cmd="$2"
    if eval "$test_cmd" > /dev/null 2>&1; then
        echo "✅ $name - PASS"
        ((passed++))
    else
        echo "❌ $name - FAIL"
        ((failed++))
    fi
}

# Built-in plugins (check directory exists under oh-my-zsh)
check_plugin "git" "[[ -d ~/.oh-my-zsh/plugins/git ]]"
check_plugin "docker" "type docker 2>/dev/null || [[ -d ~/.oh-my-zsh/plugins/docker ]]"
check_plugin "vscode" "[[ -d ~/.oh-my-zsh/plugins/vscode ]]"
check_plugin "web-search" "[[ -d ~/.oh-my-zsh/plugins/web-search ]]"
check_plugin "colored-man-pages" "[[ -d ~/.oh-my-zsh/plugins/colored-man-pages ]]"
check_plugin "jsontools" "[[ -d ~/.oh-my-zsh/plugins/jsontools ]]"
check_plugin "copypath" "[[ -d ~/.oh-my-zsh/plugins/copypath ]]"

# External plugins (check custom plugins directory)
check_plugin "zsh-autosuggestions" "[[ -d ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions ]]"
check_plugin "zsh-syntax-highlighting" "[[ -d ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting ]]"

echo ""
echo "Results: $passed passed, $failed failed"
[[ $failed -eq 0 ]] && echo "🏆 All plugins validated!" || echo "⚠️ Fix failing plugins before proceeding"
exit $failed
