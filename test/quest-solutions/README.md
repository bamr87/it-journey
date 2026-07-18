# Quest Solutions Framework

**Purpose**: Centralized validation, answer keys, and reference materials for all IT-Journey quest completions. **Location**: `test/quest-solutions/` **CI Workflow**: `.github/workflows/validate-solutions.yml`

---

## Overview

The Quest Solutions Framework provides a structured, scalable system for:

- **Answer Keys** — Full expected outputs and solutions for each quest
- **Validation Scripts** — Automated checks to verify quest completion
- **Reference Reports** — Expected audit findings, benchmark data, and documentation
- **Scoring Engine** — Point-based scoring with rank determination

> **Philosophy**: Solutions exist to validate learning, not to shortcut it. Complete the quest first, then cross-check your work.

## Directory Structure

```
test/quest-solutions/
├── README.md                              ← You are here
├── validate-quest-solution.sh             ← Main validation entry point
├── _shared/                               ← Shared toolkit
│   ├── lib/
│   │   ├── common.sh                      ← Assertions, logging, platform detection
│   │   └── scoring.sh                     ← Point-based scoring engine
│   └── templates/
│       ├── quest-solution-readme-template.md
│       ├── answer-key-template.md
│       └── validation-script-template.sh
├── 0000/                                  ← Level 0000: Foundation & Init World
│   └── README.md
├── 0001/                                  ← Level 0001: Journeyman Challenges
│   └── README.md
├── 0010/                                  ← Level 0010: Terminal Enhancement
│   ├── README.md
│   └── oh-my-zsh-terminal-enchantment/    ← ✅ Complete solution set
│       ├── README.md
│       ├── answer-key.md
│       ├── scripts/
│       │   ├── boss-battle-validate.sh
│       │   ├── setup-terminal.sh
│       │   ├── theme-benchmark.sh
│       │   ├── validate-plugins.sh
│       │   └── validate-vscode-terminal.sh
│       └── reports/
│           ├── security-audit.md
│           ├── theme-benchmark-results.md
│           └── terminal-setup-guide.md
├── 0011/                                  ← Level 0011: Dev Tools & AI
│   └── README.md
├── 0100/                                  ← Level 0100: Frontend & Docker
│   └── README.md
└── 0101/                                  ← Level 0101: Advanced DevOps
    └── README.md
```

## Quick Start

### Validate Solutions

```bash
# Validate all quest solutions (structural checks — CI-safe)
./test/quest-solutions/validate-quest-solution.sh --all

# Validate a specific quest
./test/quest-solutions/validate-quest-solution.sh 0010/oh-my-zsh-terminal-enchantment

# Validate all solutions in a level
./test/quest-solutions/validate-quest-solution.sh --level 0010
```

### Run a Quest-Specific Validator

```bash
# Run the full Boss Battle validation locally
zsh test/quest-solutions/0010/oh-my-zsh-terminal-enchantment/scripts/boss-battle-validate.sh

# Run a challenge validator
zsh test/quest-solutions/0010/oh-my-zsh-terminal-enchantment/scripts/validate-plugins.sh
```

## Shared Toolkit

### Common Library (`_shared/lib/common.sh`)

Provides logging, assertions, platform detection, and summary functions:

```bash
source test/quest-solutions/_shared/lib/common.sh

qs_header "My Validation"
qs_check "Config file exists"    qs_file_exists "$HOME/.zshrc"
qs_check "Theme is configured"   qs_file_contains "$HOME/.zshrc" 'ZSH_THEME='
qs_check "Docker is installed"   command -v docker
qs_summary
```

**Functions**:
| Function | Purpose |
|----------|---------|
| `qs_check` | Assert a condition and track pass/fail |
| `qs_skip` | Skip a check with reason |
| `qs_file_exists`, `qs_dir_exists` | File/directory existence checks |
| `qs_file_contains` | Check if file contains a string |
| `qs_detect_platform` | Returns `macos`, `linux`, or `windows` |
| `qs_detect_challenge_pattern` | Returns `template` or `implementation` from quest markdown |
| `qs_summary` | Print pass/fail/skip summary |

### Scoring Engine (`_shared/lib/scoring.sh`)

Extends common.sh with point-based scoring and rank calculation:

```bash
source test/quest-solutions/_shared/lib/scoring.sh

qs_header "Boss Battle"
qs_score "Setup script exists" 5 5 qs_file_executable "$HOME/setup-terminal.sh"
qs_score "Strict mode enabled" 5 5 qs_file_contains "$HOME/setup-terminal.sh" 'set -euo pipefail'
qs_score_summary "Terminal Enchantment"
```

**Rank Thresholds**:
| Score | Rank |
|-------|------|
| 95–100% | 👑 LEGENDARY |
| 80–94% | 🏆 VICTORY |
| 60–79% | ⚔️ Good Fight |
| < 60% | 🛡️ Keep Questing |

## Creating Quest Solutions

### Step 1: Scaffold the Directory

```bash
LEVEL="0010"
QUEST="my-quest-slug"

mkdir -p test/quest-solutions/$LEVEL/$QUEST/{scripts,reports}
```

### Step 2: Copy Templates

```bash
cp test/quest-solutions/_shared/templates/quest-solution-readme-template.md \
   test/quest-solutions/$LEVEL/$QUEST/README.md

cp test/quest-solutions/_shared/templates/answer-key-template.md \
   test/quest-solutions/$LEVEL/$QUEST/answer-key.md

cp test/quest-solutions/_shared/templates/validation-script-template.sh \
   test/quest-solutions/$LEVEL/$QUEST/scripts/validate-main.sh
```

### Step 3: Customize

1. **README.md** — Fill in quest title, purpose, directory structure, scoring summary
2. **answer-key.md** — Document expected outputs for each chapter/challenge
3. **scripts/** — Write validation scripts that source `_shared/lib/common.sh`
4. **reports/** — Add reference reports (audit findings, benchmarks, etc.)

### Step 4: Validate

```bash
./test/quest-solutions/validate-quest-solution.sh $LEVEL/$QUEST
```

### Step 5: Update the Level README

Add an entry to `test/quest-solutions/$LEVEL/README.md` in the Available Solutions table.

## Two Challenge Patterns

The framework supports both quest challenge patterns found in the repository:

### Pattern A: Template-Style (Novice/Intermediate/Advanced)

Used by quests like Advanced Markdown, YAML Configuration. Solutions include:
- Per-difficulty validation scripts
- Graduated answer keys (Novice → Advanced)
- Cumulative scoring across difficulty levels

### Pattern B: Implementation Challenge + Boss Battle

Used by quests like Oh-My-Zsh Terminal Enchantment. Solutions include:
- Per-challenge validation scripts (Challenge 1–4)
- Boss Battle final validation with comprehensive scoring
- Phase-based scoring (Foundation, Enchantment, Integration, Documentation)

The `qs_detect_challenge_pattern` function in `common.sh` auto-detects which pattern a quest uses by inspecting its markdown content.

## CI/CD Integration

The GitHub Actions workflow (`.github/workflows/validate-solutions.yml`) runs on every push/PR that touches `test/quest-solutions/`:

**Structural checks (CI-safe, no environment dependencies)**:
- Required files present (`README.md`, `answer-key.md`)
- Shell script syntax validation (`bash -n`)
- Report files non-empty
- Internal markdown links valid

**Manual dispatch** supports validating a specific level:
```
gh workflow run validate-solutions.yml -f level=0010
```

**Note**: Full quest validation (environment checks, tool installation) must be run locally since it requires system state (e.g., Oh-My-Zsh installed, Docker running).

## Related Resources

- **Quest Content**: [pages/_quests/](../../pages/_quests/) — Quest markdown files
- **Quest Validator**: [test/quest-validator/](../quest-validator/) — Validates quest *structure* (frontmatter, content)
- **Quest Templates**: [pages/_quests/templates/](../../pages/_quests/templates/) — Templates for creating new quests
- **test/ README**: [test/README.md](../README.md) — Overview of all testing systems

---

**Last Updated**: 2026-02-14
