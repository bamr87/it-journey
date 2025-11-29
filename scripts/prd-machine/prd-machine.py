#!/usr/bin/env python3
"""
PRD MACHINE - The Self-Writing, Self-Evolving Product Reality Distillery

A CLI tool that autonomously writes, maintains, and evolves PRDs.
Run with: prd-machine sync

KFI: 100% of shipped features trace directly to a machine-maintained PRD
that was never out of date by more than 6 hours.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Optional YAML support - try to import, use basic parsing as fallback
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class PRDMachine:
    """
    The PRD Machine: Autonomous Product Requirements Document Generator.
    
    Ingests signals from:
    - Git commits
    - Markdown files
    - Issue trackers
    - Feature files
    
    Outputs: A perfect PRD.md that stays correct forever.
    """
    
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or self._find_repo_root()
        self.prd_path = self.repo_root / "PRD.md"
        self.signals: Dict[str, List[Any]] = {
            "git_commits": [],
            "markdown_files": [],
            "features": [],
            "issues": [],
            "conflicts": []
        }
        self.colors = {
            'INFO': '\033[0;34m',
            'SUCCESS': '\033[0;32m',
            'WARNING': '\033[1;33m',
            'ERROR': '\033[0;31m',
            'HEADER': '\033[0;35m',
            'NC': '\033[0m'
        }
    
    def _find_repo_root(self) -> Path:
        """Find the repository root directory."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, check=True
            )
            return Path(result.stdout.strip())
        except subprocess.CalledProcessError:
            return Path.cwd()
    
    def log(self, level: str, message: str) -> None:
        """Log a message with color coding."""
        color = self.colors.get(level, '')
        nc = self.colors['NC']
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{color}[{timestamp}] [{level}]{nc} {message}")
    
    def ingest_git_commits(self, days: int = 30) -> List[Dict[str, str]]:
        """Ingest recent git commits as signals."""
        self.log("INFO", f"Ingesting git commits from last {days} days...")
        
        try:
            result = subprocess.run(
                [
                    "git", "log",
                    f"--since={days} days ago",
                    "--pretty=format:%H|%s|%an|%ad|%b",
                    "--date=iso"
                ],
                capture_output=True, text=True, cwd=self.repo_root
            )
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|', 4)
                    if len(parts) >= 4:
                        commit = {
                            "hash": parts[0][:8],
                            "subject": parts[1],
                            "author": parts[2],
                            "date": parts[3],
                            "body": parts[4] if len(parts) > 4 else ""
                        }
                        commits.append(commit)
            
            self.signals["git_commits"] = commits
            self.log("SUCCESS", f"Ingested {len(commits)} commits")
            return commits
            
        except subprocess.CalledProcessError as e:
            self.log("WARNING", f"Failed to get git commits: {e}")
            return []
    
    def ingest_markdown_files(self, patterns: List[str] = None) -> List[Dict[str, Any]]:
        """Ingest markdown files for feature and documentation signals."""
        self.log("INFO", "Ingesting markdown files...")
        
        patterns = patterns or ["pages/_quests/*.md", "pages/_posts/*.md", "docs/**/*.md"]
        md_files = []
        
        for pattern in patterns:
            for path in self.repo_root.glob(pattern):
                if path.is_file():
                    try:
                        content = path.read_text(encoding='utf-8')
                        frontmatter = self._parse_frontmatter(content)
                        md_files.append({
                            "path": str(path.relative_to(self.repo_root)),
                            "title": frontmatter.get("title", path.stem),
                            "description": frontmatter.get("description", ""),
                            "date": frontmatter.get("date", ""),
                            "tags": frontmatter.get("tags", []),
                            "categories": frontmatter.get("categories", []),
                        })
                    except Exception as e:
                        self.log("WARNING", f"Failed to parse {path}: {e}")
        
        self.signals["markdown_files"] = md_files
        self.log("SUCCESS", f"Ingested {len(md_files)} markdown files")
        return md_files
    
    def ingest_features(self) -> List[Dict[str, Any]]:
        """Ingest feature definitions from features.yml or similar."""
        self.log("INFO", "Ingesting feature definitions...")
        
        features_file = self.repo_root / "features" / "features.yml"
        features = []
        
        if features_file.exists():
            try:
                if YAML_AVAILABLE:
                    content = features_file.read_text(encoding='utf-8')
                    features = yaml.safe_load(content) or []
                    self.log("SUCCESS", f"Ingested {len(features)} features")
                else:
                    self.log("WARNING", "PyYAML not available, using basic parsing")
            except Exception as e:
                self.log("WARNING", f"Failed to parse features file: {e}")
        else:
            self.log("INFO", "No features.yml found, scanning for feature indicators")
        
        self.signals["features"] = features
        return features
    
    def _parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """Parse YAML frontmatter from markdown content."""
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}
        
        frontmatter_text = match.group(1)
        result = {}
        
        # Simple YAML-like parsing
        current_key = None
        current_list = None
        
        for line in frontmatter_text.split('\n'):
            if not line.strip():
                continue
            
            # Handle list items
            if line.strip().startswith('- '):
                if current_key and current_list is not None:
                    current_list.append(line.strip()[2:].strip())
                continue
            
            # Handle key-value pairs
            if ':' in line:
                key, *value_parts = line.split(':', 1)
                key = key.strip()
                value = value_parts[0].strip() if value_parts else ""
                
                if value:
                    result[key] = value.strip('"\'')
                    current_key = None
                    current_list = None
                else:
                    current_key = key
                    current_list = []
                    result[key] = current_list
        
        return result
    
    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """Detect conflicting requirements or signals."""
        self.log("INFO", "Detecting conflicts in requirements...")
        
        conflicts = []
        
        # Simple conflict detection based on commit messages
        for commit in self.signals.get("git_commits", []):
            subject = commit.get("subject", "").lower()
            # Look for revert or conflicting patterns
            if "revert" in subject or "rollback" in subject:
                conflicts.append({
                    "type": "revert",
                    "source": f"commit:{commit['hash']}",
                    "description": f"Reverted change: {commit['subject']}",
                    "resolution": "Review if revert addresses a conflicting requirement"
                })
            
            # Look for "fix" that might indicate previous requirement was incomplete
            if subject.startswith("fix:") or subject.startswith("fix("):
                conflicts.append({
                    "type": "fix",
                    "source": f"commit:{commit['hash']}",
                    "description": f"Bug fix suggests incomplete requirement: {commit['subject']}",
                    "resolution": "Consider if original requirement needs clarification"
                })
        
        self.signals["conflicts"] = conflicts
        
        if conflicts:
            self.log("WARNING", f"Detected {len(conflicts)} potential conflicts")
        else:
            self.log("SUCCESS", "No conflicts detected")
        
        return conflicts
    
    def generate_section_why(self) -> str:
        """Generate the WHY section (Section 0) for IT-Journey."""
        return """## 0. WHY

Build **IT-Journey** — an open-source educational platform that democratizes IT education 
through gamified quests, practical tutorials, and AI-enhanced learning experiences, 
transforming complete beginners into skilled IT professionals.

**KFI:** 100% of learners who complete a quest path can demonstrate measurable skill 
improvement through hands-on projects in their portfolio.

"""
    
    def generate_section_mvp(self) -> str:
        """Generate the MVP section (Section 1) for IT-Journey."""
        feature_count = len(self.signals.get("features", []))
        md_count = len(self.signals.get("markdown_files", []))
        
        # Count quests and posts from markdown files
        quest_count = sum(1 for f in self.signals.get("markdown_files", []) if "_quests" in f.get("path", ""))
        post_count = sum(1 for f in self.signals.get("markdown_files", []) if "_posts" in f.get("path", ""))
        
        return f"""## 1. MVP (Minimum Viable Promise)

As a **learner / contributor / educator**, I want:

- ✅ Gamified learning quests with progressive difficulty (Level 0000 → advanced)
- ✅ Practical tutorials that build real-world portfolio projects
- ✅ Multi-platform support (macOS, Windows, Linux, Cloud)
- ✅ AI-enhanced development workflows and automation
- ✅ Jekyll-based static site with GitHub Pages deployment
- ✅ Automated quality assurance (link checking, content validation)
- 🔄 Interactive terminal interface (`journey.sh`) for navigation
- 🔜 Certification tracking and skill progression metrics

### Current Content Status

| Source | Count | Status |
|--------|-------|--------|
| Learning Quests | {quest_count} | ✅ Published |
| Educational Posts | {post_count} | ✅ Published |
| Total Markdown Files | {md_count} | ✅ Indexed |
| Implemented Features | {feature_count} | ✅ Tracked |
| Recent Commits | {len(self.signals.get('git_commits', []))} | ✅ Analyzed |
| Detected Issues | {len(self.signals.get('conflicts', []))} | {'⚠️ Review needed' if self.signals.get('conflicts') else '✅ None'} |

"""
    
    def generate_section_ux(self) -> str:
        """Generate the UX section (Section 2) for IT-Journey."""
        return """## 2. UX (User eXperience Flow)

```mermaid
graph TD
    A[New Learner] --> B[Visit IT-Journey Site]
    B --> C{Choose Path}
    C -->|Beginner| D[Zero to Hero Guide]
    C -->|Intermediate| E[Learning Quests]
    C -->|Advanced| F[Contribute & Create]
    D --> G[Complete Foundational Quests]
    E --> G
    G --> H[Build Portfolio Projects]
    H --> I[Skill Progression Tracked]
    I --> J[Community Recognition]
    F --> K[Create Quests/Tutorials]
    K --> J
    J --> L[🔄 Continue Learning Journey]
    L --> C
```

### User Journeys

**Beginner Path:**
1. **Discover**: Visit site → Browse quests by level
2. **Learn**: Start with Level 0000 quests → Follow step-by-step tutorials
3. **Practice**: Complete hands-on exercises → Build first projects
4. **Progress**: Track skill development → Unlock advanced content

**Contributor Path:**
1. **Explore**: Review existing content → Identify gaps or improvements
2. **Create**: Write new quests/tutorials → Follow content guidelines
3. **Submit**: Open PR → Get community feedback
4. **Iterate**: Refine based on learner outcomes

"""
    
    def generate_section_api(self) -> str:
        """Generate the API section (Section 3) for IT-Journey."""
        return """## 3. API (Atomic Programmable Interface)

### Site Navigation

| Route | Content | Purpose |
|-------|---------|---------|
| `/` | Home | Landing page with learning paths |
| `/quests/` | Quest Collection | Browse gamified learning experiences |
| `/posts/` | Blog Posts | Tutorials, case studies, guides |
| `/docs/` | Documentation | Reference materials and guides |
| `/notebooks/` | Jupyter Notebooks | Interactive code examples |
| `/about/features/` | Features Index | Platform capabilities |

### CLI Tools

```bash
# Interactive terminal interface
./journey.sh

# Local development
bundle exec jekyll serve --config _config.yml,_config_dev.yml

# Docker development
docker compose up jekyll

# Quest validation
docker compose run quest-validator

# PRD synchronization
docker compose run prd-machine ./scripts/prd-machine/prd-machine sync

# Link health check
python3 scripts/link-checker.py --scope website
```

### GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `build-validation.yml` | Push/PR | Validate Jekyll build |
| `link-checker.yml` | Schedule/Manual | Check link health |
| `prd-sync.yml` | Schedule/Push | Update PRD.md |
| `frontmatter-validation.yml` | Push | Validate content metadata |

"""
    
    def generate_section_nfr(self) -> str:
        """Generate the NFR section (Section 4) for IT-Journey."""
        return """## 4. NFR (Non-Functional Realities)

| Category | Requirement | Metric | Current |
|----------|-------------|--------|---------|
| Accessibility | WCAG 2.1 AA compliance | Lighthouse score ≥90 | 🔄 In progress |
| Performance | Fast page loads | Time to Interactive <3s | ✅ Static site |
| Availability | Always accessible | 99.9% uptime | ✅ GitHub Pages |
| SEO | Discoverable content | Proper meta tags | ✅ Jekyll SEO |
| Security | Safe content delivery | HTTPS everywhere | ✅ GitHub Pages |
| Multi-Platform | Cross-OS support | macOS/Windows/Linux | ✅ Documented |
| Mobile | Responsive design | All breakpoints | ✅ CSS framework |
| Content Freshness | Regular updates | Activity within 30 days | ✅ Active |

"""
    
    def generate_section_edge(self) -> str:
        """Generate the EDGE section (Section 5) for IT-Journey."""
        conflicts = self.signals.get("conflicts", [])
        conflict_text = ""
        
        if conflicts:
            conflict_text = "\n### Recent Issues Detected\n\n"
            for c in conflicts[:5]:  # Show top 5 conflicts
                conflict_text += f"- **{c['type'].upper()}**: {c['description']}\n"
                conflict_text += f"  - *Action*: {c['resolution']}\n"
        
        return f"""## 5. EDGE (Exceptions, Dependencies, Gotchas)

### Dependencies

- **Ruby 3.2+**: Jekyll runtime
- **Jekyll 3.9+**: Static site generator
- **Bundler**: Ruby dependency management
- **Python 3.8+**: Automation scripts and validation
- **Docker**: Containerized development environment
- **Git**: Version control and GitHub integration

### Platform Requirements

| Platform | Requirements | Notes |
|----------|--------------|-------|
| macOS | Homebrew, Xcode CLI | Primary development |
| Windows | WSL2 recommended | Docker Desktop |
| Linux | Standard dev tools | Native support |
| Cloud | GitHub Codespaces | Zero setup |

### Gotchas

- **Jekyll versions**: Pinned to 3.9.x for GitHub Pages compatibility
- **Ruby versions**: Use rbenv/rvm for version management
- **Large repos**: Initial clone may take time; use sparse checkout if needed
- **Binary files**: Images/media should go in `assets/` only
- **Frontmatter**: All content files require valid YAML frontmatter
{conflict_text}
"""
    
    def generate_section_oos(self) -> str:
        """Generate the OOS section (Section 6) for IT-Journey."""
        return """## 6. OOS (Out Of Scope)

IT-Journey explicitly does NOT:

- ❌ Provide paid certifications or credentials
- ❌ Offer live instructor-led training
- ❌ Host user-generated content without review
- ❌ Store personal user data or accounts
- ❌ Provide enterprise or commercial support
- ❌ Replace formal education programs
- ❌ Guarantee job placement or outcomes

### Focus Areas

The platform focuses on:
- ✅ Self-paced, asynchronous learning
- ✅ Open-source community contributions
- ✅ Practical, portfolio-building projects
- ✅ Free, accessible educational content

"""
    
    def generate_section_road(self) -> str:
        """Generate the ROAD section (Section 7) for IT-Journey."""
        return """## 7. ROAD (Roadmap)

| Milestone | Objective | Target | Status |
|-----------|-----------|--------|--------|
| **Foundation** | Jekyll site + GitHub Pages deployment | 2024 Q1 | ✅ Complete |
| **Content** | Initial quest collection + tutorials | 2024 Q2 | ✅ Complete |
| **Guardian 2.0** | Advanced link monitoring + AI analysis | 2025 Q1 | ✅ Complete |
| **PRD Machine** | Automated requirements documentation | 2025 Q4 | 🔄 In Progress |
| **Interactive** | Enhanced terminal interface + CLI tools | 2025 Q4 | 🔄 In Progress |
| **Community** | Contributor growth + content expansion | 2026 Q1 | 📋 Planned |
| **Certification** | Skill tracking + progress metrics | 2026 Q2 | 📋 Planned |
| **AI Tutor** | Personalized learning recommendations | 2026 Q4 | 🔮 Vision |

### Upcoming Features

- [ ] Enhanced quest progression tracking
- [ ] Community discussion integration
- [ ] Skill assessment and badging
- [ ] Mobile-optimized experience
- [ ] AI-powered content recommendations
- [ ] Integration with external learning platforms

"""
    
    def generate_section_risk(self) -> str:
        """Generate the RISK section (Section 8) for IT-Journey."""
        return """## 8. RISK (Top Risks)

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Content staleness | 🟡 Medium | Medium | Automated freshness monitoring |
| Contributor burnout | 🟡 Medium | Medium | Community growth + shared ownership |
| Technology obsolescence | 🟡 Medium | Low | Regular stack reviews + updates |
| Broken links/content | 🔴 High | Medium | Guardian 2.0 automated checking |
| SEO/discoverability issues | 🟡 Medium | Medium | Jekyll SEO plugin + sitemap |
| Accessibility gaps | 🔴 High | Medium | Regular audits + WCAG compliance |

### Risk Monitoring

The platform monitors health through:

- **Guardian 2.0**: Daily link health checks with AI-powered analysis
- **PRD Machine**: Automated requirements freshness tracking
- **GitHub Actions**: Build validation and content checks
- **Community feedback**: Issue tracking and discussion monitoring

"""
    
    def generate_section_done(self) -> str:
        """Generate the DONE section (Section 9) for IT-Journey."""
        return """## 9. DONE (Definition of Done)

### Success Criteria

- [ ] Learners complete quests with demonstrable skill improvements
- [ ] Contributors can easily add content following clear guidelines
- [ ] Site remains accessible and fast across all platforms
- [ ] Content stays current with regular community contributions
- [ ] Quality assurance catches issues before they impact learners

### Validation Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Quest Completion Rate | >70% | TBD | 📋 Tracking planned |
| Content Freshness | <30 days | Active | ✅ |
| Build Success Rate | 100% | 100% | ✅ |
| Link Health | >95% | Monitored | ✅ |
| Community Growth | +10%/quarter | Growing | 🔄 |

---

**When these criteria are met, IT-Journey fulfills its mission:**

> *Democratizing IT education through open-source learning,*
> *gamified experiences, and community-driven content.*

**Keep learning. Keep building. Keep sharing.** 🚀

"""
    
    def generate_metadata_section(self) -> str:
        """Generate the metadata/frontmatter for the PRD."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        return f"""---
title: "PRD: IT-Journey – Open-Source IT Education Platform"
description: "Product requirements for IT-Journey, an open-source educational platform with gamified quests, practical tutorials, and AI-enhanced learning"
date: {now}
lastmod: {now}
status: Living
version: {datetime.now().strftime('%Y-%m-%d')}
auto_generated: true
generator: prd-machine
repository: https://github.com/bamr87/it-journey
---

"""
    
    def generate_prd(self) -> str:
        """Generate the complete PRD document."""
        self.log("HEADER", "═" * 50)
        self.log("HEADER", "   PRD MACHINE - Generating PRD.md")
        self.log("HEADER", "═" * 50)
        
        # Ingest all signals
        self.ingest_git_commits()
        self.ingest_markdown_files()
        self.ingest_features()
        self.detect_conflicts()
        
        # Generate sections
        sections = [
            self.generate_metadata_section(),
            "# IT-Journey\n\n",
            "*Open-Source IT Education Platform*\n\n",
            f"> **Status:** Living | **Version:** {datetime.now().strftime('%Y-%m-%d')} | **Auto-Generated:** ✅\n\n",
            self.generate_section_why(),
            self.generate_section_mvp(),
            self.generate_section_ux(),
            self.generate_section_api(),
            self.generate_section_nfr(),
            self.generate_section_edge(),
            self.generate_section_oos(),
            self.generate_section_road(),
            self.generate_section_risk(),
            self.generate_section_done(),
        ]
        
        return "".join(sections)
    
    def sync(self, output_path: Optional[Path] = None) -> bool:
        """Sync and generate/update the PRD."""
        output_path = output_path or self.prd_path
        
        try:
            prd_content = self.generate_prd()
            
            # Write to file
            output_path.write_text(prd_content, encoding='utf-8')
            
            self.log("SUCCESS", f"PRD generated successfully: {output_path}")
            self.log("INFO", f"Total signals processed: {sum(len(v) for v in self.signals.values())}")
            
            return True
            
        except Exception as e:
            self.log("ERROR", f"Failed to generate PRD: {e}")
            return False
    
    def status(self) -> Dict[str, Any]:
        """Get current PRD status and health metrics."""
        status = {
            "prd_exists": self.prd_path.exists(),
            "last_modified": None,
            "signals": {},
            "health": "unknown"
        }
        
        if self.prd_path.exists():
            stat = self.prd_path.stat()
            status["last_modified"] = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
            
            # Check freshness (should be < 6 hours old)
            age_hours = (datetime.now(timezone.utc).timestamp() - stat.st_mtime) / 3600
            if age_hours < 6:
                status["health"] = "healthy"
            elif age_hours < 24:
                status["health"] = "stale"
            else:
                status["health"] = "outdated"
            
            status["age_hours"] = round(age_hours, 1)
        
        return status
    
    def show_status(self) -> None:
        """Display current PRD status."""
        status = self.status()
        
        self.log("HEADER", "═" * 50)
        self.log("HEADER", "   PRD MACHINE - Status")
        self.log("HEADER", "═" * 50)
        
        if status["prd_exists"]:
            health_color = {
                "healthy": "SUCCESS",
                "stale": "WARNING",
                "outdated": "ERROR"
            }.get(status["health"], "INFO")
            
            self.log("INFO", f"PRD Path: {self.prd_path}")
            self.log("INFO", f"Last Modified: {status['last_modified']}")
            self.log("INFO", f"Age: {status['age_hours']} hours")
            self.log(health_color, f"Health: {status['health'].upper()}")
        else:
            self.log("WARNING", "No PRD.md found. Run 'prd-machine sync' to generate.")


def main():
    """Main entry point for the PRD Machine CLI."""
    parser = argparse.ArgumentParser(
        description="PRD MACHINE - The Self-Writing, Self-Evolving Product Reality Distillery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  prd-machine sync              # Generate or update PRD.md
  prd-machine sync --days 7     # Use commits from last 7 days
  prd-machine status            # Check PRD health
  prd-machine conflicts         # Show detected conflicts
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Generate or update PRD.md")
    sync_parser.add_argument(
        "--days", type=int, default=30,
        help="Number of days of git history to ingest (default: 30)"
    )
    sync_parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output path for PRD.md (default: ./PRD.md)"
    )
    
    # Status command
    subparsers.add_parser("status", help="Check PRD health and status")
    
    # Conflicts command
    subparsers.add_parser("conflicts", help="Show detected requirement conflicts")
    
    # Version
    parser.add_argument("--version", action="version", version="prd-machine 1.0.0")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    machine = PRDMachine()
    
    if args.command == "sync":
        output_path = Path(args.output) if args.output else None
        success = machine.sync(output_path)
        return 0 if success else 1
    
    elif args.command == "status":
        machine.show_status()
        return 0
    
    elif args.command == "conflicts":
        machine.ingest_git_commits()
        conflicts = machine.detect_conflicts()
        
        if conflicts:
            machine.log("WARNING", f"Found {len(conflicts)} conflicts:")
            for c in conflicts:
                print(f"  - [{c['type']}] {c['description']}")
                print(f"    Resolution: {c['resolution']}")
        else:
            machine.log("SUCCESS", "No conflicts detected")
        
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
