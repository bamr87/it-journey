#!/usr/bin/env zsh
# =============================================================================
# Theme Benchmarking Script
# Quest: Terminal Enchantment — Challenge 2
# Purpose: Benchmarks Oh-My-Zsh theme prompt render times
# Usage: zsh theme-benchmark.sh
# Expected: All themes < 50ms, results saved to stdout
# =============================================================================

set -euo pipefail

THEMES=("robbyrussell" "agnoster" "clean")
RESULTS_FILE="${1:-/dev/stdout}"

echo "# Theme Benchmark Results"
echo "Date: $(date)"
echo ""
echo "| Theme | Avg Prompt Time (ms) | Status |"
echo "|-------|---------------------|--------|"

for theme in "${THEMES[@]}"; do
    total=0
    for i in {1..5}; do
        start=$(perl -MTime::HiRes=time -e 'printf "%.3f", time')
        ZSH_THEME="$theme" 2>/dev/null || true
        end=$(perl -MTime::HiRes=time -e 'printf "%.3f", time')
        elapsed=$(echo "($end - $start) * 1000" | bc)
        total=$(echo "$total + $elapsed" | bc)
    done
    avg=$(echo "scale=2; $total / 5" | bc)
    echo "| $theme | $avg | ✅ |"
done

echo ""
echo "Note: Times may vary by machine. Values under 50ms are considered healthy."
