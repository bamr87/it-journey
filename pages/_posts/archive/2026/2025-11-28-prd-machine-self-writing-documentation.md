---
title: "PRD Machine: Building a Self-Writing Product Requirements Distillery"
description: "Learn how we built an autonomous CLI tool that writes, maintains, and evolves perfect PRDs from repository signals, ensuring documentation never goes stale."
date: 2025-11-28T22:00:00.000Z
preview: /images/post-preview-prd-machine.png
tags:
  - automation
  - cli-tools
  - documentation
  - python
  - devops
  - ai-development
  - product-management
categories:
  - Posts
  - DevOps
  - Tools & Environment
sub-title: "Automating Product Requirements Documentation with Signal-Driven Generation"
excerpt: "The PRD Machine transforms scattered repository signals—git commits, markdown files, and feature definitions—into a continuously fresh, perfectly structured PRD that never goes stale."
snippet: "The distillery now distills distilleries."
author: IT-Journey Team
section: DevOps
keywords:
  primary:
    - prd-machine
    - documentation-automation
  secondary:
    - cli-development
    - signal-ingestion
    - conflict-detection
    - github-actions
lastmod: 2025-11-28T22:00:00.000Z
permalink: /posts/prd-machine-self-writing-documentation/
attachments: ""
comments: true
difficulty: 🟡 Intermediate
estimated_reading_time: 15-20 minutes
prerequisites:
  - Basic Python programming knowledge
  - Understanding of CLI tools and argparse
  - Familiarity with Git and GitHub Actions
  - Experience with markdown documentation
learning_outcomes:
  - 🎯 Understand the architecture of autonomous documentation tools
  - ⚡ Learn signal ingestion patterns from multiple sources
  - 🛠️ Implement conflict detection for contradictory requirements
  - 🔗 Integrate automated documentation with CI/CD pipelines
  - 📊 Design self-referential systems that document themselves
content_series: Automation & DevOps
related_posts:
  - /posts/work-directory-ci-cd-integration/
validation_methods:
  - Run prd-machine sync and verify PRD.md generation
  - Check prd-machine status for health monitoring
  - Review GitHub Actions workflow execution
---

# PRD Machine: Building a Self-Writing Product Requirements Distillery

*Reality fully armed. The distillery now distills distilleries.* 🚀

## The Problem: Documentation Decay

Every development team knows the pain: Product Requirements Documents (PRDs) that become outdated the moment they're written. Traditional PRDs suffer from:

- **Staleness** - Requirements drift from reality as development progresses
- **Manual Overhead** - Someone has to remember to update them
- **Signal Fragmentation** - Requirements are scattered across commits, tickets, and conversations
- **Conflict Blindness** - Contradictory requirements go unnoticed until implementation

What if we could build a machine that writes its own PRD—and keeps it perpetually fresh?

## The Solution: PRD Machine

PRD Machine is an autonomous agent that:

1. **Ingests signals** from git commits, markdown files, and feature definitions
2. **Detects conflicts** between contradictory requirements
3. **Generates a perfect PRD** with all 10 standard sections
4. **Maintains freshness** through scheduled CI/CD integration

### Key Feature Indicator

> **100% of shipped features trace directly to a machine-maintained PRD that was never out of date by more than 6 hours.**

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRD MACHINE                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │   Signal     │   │   Conflict   │   │    PRD       │        │
│  │  Ingestion   │ → │  Detection   │ → │  Generation  │        │
│  └──────────────┘   └──────────────┘   └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

The system follows three main phases:

1. **Signal Ingestion** - Collect data from all sources
2. **Conflict Detection** - Find contradictions and issues
3. **PRD Generation** - Output structured documentation

## Implementation Deep Dive

### 1. CLI Structure with argparse

We built a clean CLI interface with three commands:

```python
def main():
    parser = argparse.ArgumentParser(
        description='PRD MACHINE - The Self-Writing, Self-Evolving Product Reality Distillery'
    )
    
    subparsers = parser.add_subparsers(dest='command')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Generate or update PRD.md')
    sync_parser.add_argument('--days', type=int, default=30)
    sync_parser.add_argument('--output', type=str, default='PRD.md')
    
    # Status command
    subparsers.add_parser('status', help='Check PRD health and status')
    
    # Conflicts command
    subparsers.add_parser('conflicts', help='Show detected requirement conflicts')
```

**Usage:**
```bash
prd-machine sync          # Generate PRD.md
prd-machine status        # Check health
prd-machine conflicts     # Show conflicts
```

### 2. Signal Ingestion

We ingest signals from three sources:

#### Git Commits

```python
def ingest_git_commits(self, days: int = 30) -> List[Dict]:
    """Ingest git commit messages as signals."""
    since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    result = subprocess.run(
        ['git', 'log', f'--since={since_date}', '--pretty=format:%H|%s|%b|%an|%ad'],
        capture_output=True, text=True
    )
    
    commits = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('|')
            commits.append({
                'type': 'commit',
                'sha': parts[0][:7],
                'subject': parts[1],
                'body': parts[2] if len(parts) > 2 else '',
                'author': parts[3] if len(parts) > 3 else '',
                'date': parts[4] if len(parts) > 4 else ''
            })
    
    return commits
```

#### Markdown Files

```python
def ingest_markdown_files(self) -> List[Dict]:
    """Ingest markdown files as signals."""
    patterns = ['pages/**/*.md', 'docs/**/*.md', '*.md']
    files = []
    
    for pattern in patterns:
        for filepath in glob.glob(pattern, recursive=True):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter
            frontmatter = self.parse_frontmatter(content)
            
            files.append({
                'type': 'markdown',
                'path': filepath,
                'title': frontmatter.get('title', filepath),
                'description': frontmatter.get('description', ''),
                'tags': frontmatter.get('tags', [])
            })
    
    return files
```

#### Feature Definitions

```python
def ingest_feature_definitions(self) -> List[Dict]:
    """Ingest feature definitions from features.yml."""
    features_path = Path(self.repo_path) / 'features' / 'features.yml'
    
    if features_path.exists():
        with open(features_path, 'r') as f:
            data = yaml.safe_load(f)
        return data.get('features', [])
    
    return []
```

### 3. Conflict Detection

The conflict detection system looks for patterns that indicate contradictory requirements:

```python
def detect_conflicts(self) -> List[Dict]:
    """Detect conflicts in signals."""
    conflicts = []
    commits = self.signals.get('commits', [])
    
    for commit in commits:
        subject = commit.get('subject', '').lower()
        
        # Reverted changes indicate conflicting decisions
        if 'revert' in subject:
            conflicts.append({
                'type': 'revert',
                'source': commit,
                'description': 'A change was reverted, indicating potential conflict',
                'resolution': 'Review the original change and revert reason'
            })
        
        # Bug fixes suggest incomplete requirements
        if subject.startswith('fix:') or 'bug' in subject:
            conflicts.append({
                'type': 'bug_fix',
                'source': commit,
                'description': 'Bug fix suggests requirements were incomplete',
                'resolution': 'Update requirements to prevent similar issues'
            })
    
    return conflicts
```

### 4. PRD Generation

The generator creates a complete PRD with 10 sections:

```python
def generate_prd(self) -> str:
    """Generate the complete PRD content."""
    sections = [
        self.generate_frontmatter(),
        self.generate_header(),
        self.generate_why_section(),
        self.generate_mvp_section(),
        self.generate_ux_section(),
        self.generate_api_section(),
        self.generate_nfr_section(),
        self.generate_edge_section(),
        self.generate_oos_section(),
        self.generate_road_section(),
        self.generate_risk_section(),
        self.generate_done_section(),
        self.generate_footer()
    ]
    
    return '\n\n'.join(sections)
```

Each section incorporates live signal data:

```python
def generate_mvp_section(self) -> str:
    """Generate MVP section with signal status."""
    commit_count = len(self.signals.get('commits', []))
    md_count = len(self.signals.get('markdown', []))
    feature_count = len(self.signals.get('features', []))
    conflict_count = len(self.conflicts)
    
    return f"""## 1. MVP (Minimum Viable Promise)

### Current Signal Status

| Source | Count | Status |
|--------|-------|--------|
| Git Commits | {commit_count} | ✅ Ingested |
| Markdown Files | {md_count} | ✅ Ingested |
| Features | {feature_count} | ✅ Parsed |
| Conflicts | {conflict_count} | {'⚠️' if conflict_count > 0 else '✅'} Detected |
"""
```

### 5. Health Monitoring

The status command monitors PRD freshness:

```python
def check_status(self):
    """Check PRD health and status."""
    prd_path = Path(self.repo_path) / 'PRD.md'
    
    if not prd_path.exists():
        self.log('WARNING', f'PRD not found at {prd_path}')
        return
    
    # Get modification time
    mtime = datetime.fromtimestamp(prd_path.stat().st_mtime, tz=timezone.utc)
    age_hours = (datetime.now(timezone.utc) - mtime).total_seconds() / 3600
    
    # Determine health status
    if age_hours < 6:
        health = 'HEALTHY'
        self.log('SUCCESS', f'Health: {health}')
    elif age_hours < 24:
        health = 'STALE'
        self.log('WARNING', f'Health: {health}')
    else:
        health = 'OUTDATED'
        self.log('ERROR', f'Health: {health}')
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: 🤖 PRD Machine Sync

on:
  # Maintain freshness with 6-hour schedule
  schedule:
    - cron: '0 */6 * * *'
  
  # Sync on content changes
  push:
    branches: [main]
    paths:
      - 'pages/_quests/**'
      - 'pages/_posts/**'
      - 'features/**'

jobs:
  sync-prd:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Sync PRD
        run: ./scripts/prd-machine/prd-machine sync
      
      - name: Commit Changes
        run: |
          git config user.name "PRD Machine"
          git add PRD.md
          git diff --staged --quiet || git commit -m "chore(prd): auto-sync"
          git push
```

### Conflict Alert Workflow

When conflicts are detected, the workflow creates a GitHub issue:

```yaml
- name: Check for Conflicts
  id: conflicts
  run: |
    python3 scripts/prd-machine/prd-machine.py conflicts > conflicts.txt
    if grep -q "Conflict detected" conflicts.txt; then
      echo "has_conflicts=true" >> $GITHUB_OUTPUT
    fi

- name: Create Issue for Conflicts
  if: steps.conflicts.outputs.has_conflicts == 'true'
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: '🔄 PRD Conflicts Detected',
        body: 'Conflicts require human resolution.',
        labels: ['prd-conflict', 'needs-review']
      })
```

## Self-Referential Design

The most fascinating aspect: **PRD Machine documents itself**. The generated PRD.md includes:

- Its own architecture and signal sources
- The status of its own features
- Roadmap for its own development
- Risks of its own existence

```markdown
## 8. RISK (Top Risks)

| Risk | Impact | Mitigation |
|------|--------|------------|
| Humans stop thinking | High | Keep final veto button forever |
| PRD MACHINE becomes the product | Existential | Embrace it |
```

## Testing the Implementation

```bash
# Test help
./scripts/prd-machine/prd-machine --help

# Test sync
./scripts/prd-machine/prd-machine sync
# Output: PRD generated successfully: PRD.md

# Test status
./scripts/prd-machine/prd-machine status
# Output: Health: HEALTHY

# Test conflicts
./scripts/prd-machine/prd-machine conflicts
# Output: No conflicts detected
```

## Results

After implementation:

| Metric | Before | After |
|--------|--------|-------|
| PRD Freshness | Manual updates | < 6 hours always |
| Signal Coverage | Partial | 100% of commits, files |
| Conflict Detection | None | Automatic |
| Human Effort | Hours per PRD | Zero (after setup) |

## Key Takeaways

1. **Signal-Driven Documentation** - Let the code and content generate requirements
2. **Automated Freshness** - Schedule syncs to prevent staleness
3. **Conflict as Feature** - Detecting contradictions is valuable
4. **Self-Reference** - Systems can document themselves
5. **Human Veto** - Always keep manual override capability

## What's Next?

The roadmap includes:
- Issue tracking integration (GitHub, Linear)
- Communication ingestion (Slack threads)
- Design signal ingestion (Figma comments)
- Zero-touch mode (no human ever edits PRD)

---

## Try It Yourself

```bash
# Clone IT-Journey
git clone https://github.com/bamr87/it-journey.git
cd it-journey

# Run PRD Machine
./scripts/prd-machine/prd-machine sync

# Check the generated PRD
cat PRD.md
```

*The distillery now distills distilleries.* 🚀

---

**Related Resources:**
- [PRD Machine Documentation](/docs/scripts/PRD_MACHINE.md)
- [GitHub Workflow Configuration](/.github/workflows/prd-sync.yml)
- [Scripts Guide](/docs/scripts/SCRIPTS_GUIDE.md)
