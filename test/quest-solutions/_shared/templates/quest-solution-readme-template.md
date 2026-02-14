# [Quest Title] — Solutions & Validation

**Quest**: [Link to quest page]
**Level**: [NNNN] — [Level Title]
**Difficulty**: [🟢 Easy | 🟡 Medium | 🔴 Hard] | **Estimated Time**: [XX–YY minutes]

---

## Purpose

This directory contains all validation scripts, reference reports, and answer keys for the **[Quest Title]** quest. Use these materials to:

- **Cross-check your work** after completing each chapter
- **Run automated validators** to verify your environment
- **Review expected outputs** when troubleshooting
- **Score your quest completion** deliverables

> **Note**: Attempt the quest yourself before consulting the answer key. The learning happens in the doing!

## Directory Structure

```
[quest-slug]/
├── README.md                 ← You are here
├── answer-key.md             ← Full solutions & expected outputs
├── scripts/
│   ├── validate-[check].sh   ← Automated validation script
│   └── ...                   ← Additional validation scripts
└── reports/
    ├── [report-name].md      ← Reference output / findings
    └── ...                   ← Additional reference reports
```

## How to Use

### 1. Validation Scripts

Run after completing the relevant quest chapters:

```bash
# Navigate to the solutions directory
cd test/quest-solutions/[NNNN]/[quest-slug]

# Run a specific validator
zsh scripts/validate-[check].sh

# Or run all validators
for script in scripts/*.sh; do zsh "$script"; done
```

### 2. Answer Key

See [answer-key.md](answer-key.md) for:
- Expected file states after each chapter
- Commands used at each step
- Expected validation output
- Scoring breakdown

### 3. Reference Reports

| Report | Maps To |
|--------|---------|
| [report-name.md](reports/report-name.md) | Chapter/Challenge description |

## Scoring Summary

| Component | Checks | Max Score |
|-----------|--------|-----------|
| [Phase/Challenge 1] | [Description] | [XX points] |
| [Phase/Challenge 2] | [Description] | [XX points] |
| **Total** | | **[XXX points]** |

---

**Last Updated**: YYYY-MM-DD
