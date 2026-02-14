# PRD MACHINE

*The Self-Writing, Self-Evolving Product Reality Distillery*

## Overview

PRD MACHINE is an autonomous agent that writes, maintains, and evolves perfect PRDs (Product Requirements Documents) faster and more accurately than any human PM.

**Key Feature Indicator (KFI):** 100% of shipped features trace directly to a machine-maintained PRD that was never out of date by more than 6 hours.

## Quick Start

```bash
# Navigate to the repository root
cd /path/to/it-journey

# Generate or update PRD.md
./scripts/prd-machine/prd-machine sync

# Check PRD health status
./scripts/prd-machine/prd-machine status

# Show detected conflicts
./scripts/prd-machine/prd-machine conflicts
```

## Installation

The PRD Machine is a Python-based CLI tool. No external dependencies are required beyond Python 3.8+.

### Make it Available System-wide (Optional)

```bash
# Add to PATH
export PATH="${PATH}:/path/to/it-journey/scripts/prd-machine"

# Or create a symlink
ln -sf /path/to/it-journey/scripts/prd-machine/prd-machine /usr/local/bin/prd-machine
```

## Commands

### `sync`

Generate or update the PRD.md file by ingesting signals from the repository.

```bash
prd-machine sync                    # Generate PRD with default settings
prd-machine sync --days 7           # Use only last 7 days of commits
prd-machine sync --output my-prd.md # Custom output path
```

**What it does:**
1. Ingests git commits from the repository
2. Scans markdown files for feature and documentation signals
3. Parses feature definitions from `features/features.yml`
4. Detects conflicts and potential issues
5. Generates a complete PRD.md with all sections

### `status`

Check the health and freshness of the current PRD.

```bash
prd-machine status
```

**Output includes:**
- PRD existence and location
- Last modification time
- Age in hours
- Health status (healthy < 6h, stale < 24h, outdated > 24h)

### `conflicts`

Analyze signals and show detected requirement conflicts.

```bash
prd-machine conflicts
```

**Detects:**
- Reverted changes that may indicate conflicting requirements
- Bug fixes that suggest incomplete initial requirements
- Contradictory signals from different sources

**Conflict Severity:**
- 🔴 **High**: Significant issues (CI failures, auth problems, security issues)
- 🟡 **Medium**: Standard bug fixes that may indicate requirement gaps

**Smart Filtering:**
The conflict detection automatically filters out trivial fixes (typos, formatting, emoji corrections, broken links) to reduce false positives and focus on meaningful requirement issues.

## PRD Structure

The generated PRD.md follows a standardized structure:

| Section | Description |
|---------|-------------|
| **0. WHY** | Mission and key success metric |
| **1. MVP** | Minimum Viable Promise and current signal status |
| **2. UX** | User experience flow with Mermaid diagrams |
| **3. API** | CLI commands and programmatic interface |
| **4. NFR** | Non-functional requirements with metrics |
| **5. EDGE** | Edge cases, dependencies, and gotchas |
| **6. OOS** | Out of scope items |
| **7. ROAD** | Roadmap with milestones and status |
| **8. RISK** | Top risks with mitigation strategies |
| **9. DONE** | Definition of done and success criteria |

## Signal Sources

PRD Machine ingests signals from:

| Source | Type | Description |
|--------|------|-------------|
| Git Commits | Active | Subject, body, author, date |
| Markdown Files | Active | Quests, posts, docs with frontmatter |
| Features YAML | Active | Feature definitions and status |
| Issues | Planned | GitHub/Linear issue tracking |
| Slack | Planned | Thread and message content |
| Figma | Planned | Comment and annotation data |

## Configuration

PRD Machine uses sensible defaults but can be configured:

```yaml
# Future: .prd-machine.yml
signals:
  git:
    days: 30
    branches: [main, develop]
  markdown:
    patterns:
      - "pages/_quests/*.md"
      - "pages/_posts/*.md"
      - "docs/**/*.md"
  features:
    path: "features/features.yml"

output:
  path: "PRD.md"
  sections:
    - why
    - mvp
    - ux
    - api
    - nfr
    - edge
    - oos
    - road
    - risk
    - done
```

## CI/CD Integration

PRD Machine can be integrated into your CI/CD pipeline:

```yaml
# .github/workflows/prd-sync.yml
name: PRD Sync

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  sync-prd:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Sync PRD
        run: ./scripts/prd-machine/prd-machine sync
      - name: Commit Changes
        run: |
          git config user.name "PRD Machine"
          git config user.email "prd-machine@it-journey.dev"
          git add PRD.md
          git diff --staged --quiet || git commit -m "chore(prd): auto-sync PRD.md"
          git push
```

## Roadmap

| Milestone | Objective | Status |
|-----------|-----------|--------|
| Alpha | Single-repo, CLI-based sync | ✅ Complete |
| Beta | GitHub Actions integration | 🔄 In Progress |
| 1.0 | Multi-source signal ingestion | 📋 Planned |
| 2.0 | Zero-touch autonomous mode | 🔮 Vision |

## Philosophy

The PRD Machine embodies several core principles:

1. **Automation Over Manual Work**: Requirements should write themselves from signals
2. **Data-Backed Reality**: The machine uses actual evidence, not opinions
3. **Human Veto Power**: Humans always have final say via the conflict resolution system
4. **Continuous Freshness**: PRDs should never be stale by more than 6 hours

## Contributing

Contributions are welcome! The PRD Machine is part of the IT-Journey ecosystem.

### Development

```bash
# Run tests
python3 -m pytest scripts/prd-machine/tests/

# Run linting
python3 -m pylint scripts/prd-machine/prd-machine.py
```

### Adding New Signal Sources

1. Create a new `ingest_*` method in `PRDMachine` class
2. Store signals in `self.signals` dictionary
3. Update relevant sections to use the new signals
4. Add tests for the new ingestion logic

## License

MIT License - Part of the IT-Journey project.

---

*Reality fully armed. The distillery now distills distilleries.* 🚀
