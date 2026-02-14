# Theme Benchmark — Expected Results

**Quest**: Terminal Enchantment — Challenge 2
**Purpose**: Reference benchmark data for common Oh-My-Zsh themes

---

## Sample Results (Apple Silicon Mac)

| Theme | Avg Prompt Time (ms) | Status |
|-------|---------------------|--------|
| robbyrussell | ~5.00 | ✅ |
| agnoster | ~4.80 | ✅ |
| clean | ~5.20 | ✅ |

## Interpretation Guide

| Time Range | Rating | Notes |
|-----------|--------|-------|
| < 10ms | 🟢 Excellent | Imperceptible delay |
| 10–50ms | 🟡 Good | No noticeable lag |
| 50–200ms | 🟠 Acceptable | Slight delay on each prompt |
| > 200ms | 🔴 Slow | Investigate plugin/theme load times |

## Notes

- Times will vary significantly based on hardware, shell plugins, and system load
- The benchmark script measures ZSH_THEME variable assignment, not full prompt rendering
- For a more accurate test in production, use: `time zsh -ic exit`
- All three default themes tested should fall well under 50ms
- **agnoster** is the recommended choice for this quest (balance of features and speed)

## How to Run Your Own Benchmark

```bash
# Quick startup time check
time zsh -ic exit

# Full benchmark with the provided script
zsh theme-benchmark.sh

# Test a specific theme manually
ZSH_THEME="powerlevel10k/powerlevel10k" zsh -ic exit
```
