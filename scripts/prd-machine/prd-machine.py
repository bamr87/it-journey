#!/usr/bin/env python3
"""
PRD MACHINE v2 - PR-Driven Product Reality Distillery

Maintains PRD.md by updating only dynamic sections (marker-delimited)
while preserving human-authored content. Analyzes merged PRs to decide
if updates are warranted, optionally using GitHub Models API for
semantic analysis.

Commands:
  init       Generate a new PRD.md with markers + scaffolding
  sync       Update dynamic sections in existing PRD.md
  check      Determine if PRD needs updating (exit 0=no, 1=yes)
  status     Show PRD health and freshness
  conflicts  Show detected requirement conflicts
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.error import URLError
from urllib.request import Request, urlopen

# Optional YAML support
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

VERSION = "2.0.0"

# ── Marker constants ────────────────────────────────────────────
MARKER_BEGIN = "<!-- AUTO:BEGIN:{name} -->"
MARKER_END = "<!-- AUTO:END:{name} -->"
MARKER_RE = re.compile(
    r"<!-- AUTO:BEGIN:(\w+) -->\n(.*?)<!-- AUTO:END:\1 -->",
    re.DOTALL,
)

# ── Section relevance map ───────────────────────────────────────
# Maps file-path glob patterns to the dynamic PRD sections they affect.
SECTION_RELEVANCE: Dict[str, List[str]] = {
    "pages/_quests/**":        ["mvp"],
    "pages/_posts/**":         ["mvp"],
    "features/**":             ["mvp", "edge"],
    "scripts/**":              ["mvp"],
    ".github/workflows/**":    ["mvp"],
    "Gemfile*":                ["edge"],
    "Dockerfile*":             ["edge"],
    "docker-compose*":         ["edge"],
    "docs/**":                 [],  # informational only
}

# Patterns that indicate trivial (non-requirement) fixes
TRIVIAL_PATTERNS = [
    r"\btypo\b", r"\bspelling\b", r"\bformatting\b", r"\bindentation\b",
    r"\bwhitespace\b", r"\bemoji\b", r"\bicon\b", r"\bcomment\b",
    r"\bdocstring\b", r"\blink\b.*\bbroken\b", r"\bupdate.*\bdependenc",
    r"\bversion\s+bump\b", r"\bminor\s+fix\b", r"\bsmall\s+fix\b",
]

# Patterns that indicate significant requirement issues
SIGNIFICANT_PATTERNS = [
    r"\bworkflow\b.*\bfail", r"\bci\b.*\bfail", r"token",
    r"\bauth", r"\bpermission\b", r"\bsecurity\b", r"\bcrash\b",
    r"\berror\b.*\bhandl", r"\bvalidation\b.*\bfail",
]


# ════════════════════════════════════════════════════════════════
class PRDMachine:
    """PR-driven PRD maintainer with marker-based partial updates."""

    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or self._find_repo_root()
        self.prd_path = self.repo_root / "PRD.md"
        self.signals: Dict[str, List[Any]] = {
            "git_commits": [], "markdown_files": [],
            "features": [],    "conflicts": [],
        }
        self._colors = {
            "INFO": "\033[0;34m", "SUCCESS": "\033[0;32m",
            "WARNING": "\033[1;33m", "ERROR": "\033[0;31m",
            "HEADER": "\033[0;35m", "NC": "\033[0m",
        }

    # ── helpers ──────────────────────────────────────────────────
    @staticmethod
    def _find_repo_root() -> Path:
        try:
            out = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, check=True,
            )
            return Path(out.stdout.strip())
        except subprocess.CalledProcessError:
            return Path.cwd()

    def log(self, level: str, msg: str) -> None:
        c = self._colors.get(level, "")
        nc = self._colors["NC"]
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{c}[{ts}] [{level}]{nc} {msg}")

    # ── signal ingestion ─────────────────────────────────────────
    def ingest_git_commits(self, days: int = 30) -> List[Dict[str, str]]:
        self.log("INFO", f"Ingesting git commits from last {days} days...")
        try:
            result = subprocess.run(
                ["git", "log", f"--since={days} days ago",
                 "--pretty=format:%H|%s|%an|%ad|%b", "--date=iso"],
                capture_output=True, text=True, cwd=self.repo_root,
            )
            commits, skipped = [], 0
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split("|", 4)
                if len(parts) < 4:
                    continue
                subject = parts[1]
                if subject.strip().startswith("chore(prd): auto-sync"):
                    skipped += 1
                    continue
                commits.append({
                    "hash": parts[0][:8], "subject": subject,
                    "author": parts[2], "date": parts[3],
                    "body": parts[4] if len(parts) > 4 else "",
                })
            self.signals["git_commits"] = commits
            self.log("SUCCESS", f"Ingested {len(commits)} commits (skipped {skipped} auto-sync)")
            return commits
        except subprocess.CalledProcessError as e:
            self.log("WARNING", f"Failed to get git commits: {e}")
            return []

    def ingest_markdown_files(self) -> List[Dict[str, Any]]:
        self.log("INFO", "Ingesting markdown files...")
        patterns = ["pages/_quests/**/*.md", "pages/_posts/**/*.md", "docs/**/*.md"]
        md_files = []
        for pattern in patterns:
            for path in self.repo_root.glob(pattern):
                if path.is_file():
                    try:
                        fm = self._parse_frontmatter(path.read_text(encoding="utf-8"))
                        md_files.append({
                            "path": str(path.relative_to(self.repo_root)),
                            "title": fm.get("title", path.stem),
                        })
                    except Exception:
                        pass
        self.signals["markdown_files"] = md_files
        self.log("SUCCESS", f"Ingested {len(md_files)} markdown files")
        return md_files

    def ingest_features(self) -> List[Dict[str, Any]]:
        self.log("INFO", "Ingesting feature definitions...")
        features_file = self.repo_root / "features" / "features.yml"
        features: list = []
        if features_file.exists() and YAML_AVAILABLE:
            try:
                data = yaml.safe_load(features_file.read_text(encoding="utf-8")) or {}
                features = data.get("features", data) if isinstance(data, dict) else data
                self.log("SUCCESS", f"Ingested {len(features)} features")
            except Exception as e:
                self.log("WARNING", f"Failed to parse features file: {e}")
        self.signals["features"] = features
        return features

    @staticmethod
    def _parse_frontmatter(content: str) -> Dict[str, Any]:
        m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not m:
            return {}
        result: Dict[str, Any] = {}
        cur_key, cur_list = None, None
        for line in m.group(1).split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("- ") and cur_key and cur_list is not None:
                cur_list.append(stripped[2:].strip())
                continue
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                key, val = key.strip(), val.strip()
                if val:
                    result[key] = val.strip("\"'")
                    cur_key = cur_list = None
                else:
                    cur_list = []
                    result[key] = cur_list
                    cur_key = key
        return result

    def detect_conflicts(self) -> List[Dict[str, Any]]:
        self.log("INFO", "Detecting conflicts in requirements...")
        conflicts = []
        for commit in self.signals.get("git_commits", []):
            subj = commit["subject"].lower()
            orig = commit["subject"]
            if "revert" in subj or "rollback" in subj:
                conflicts.append({
                    "type": "revert", "source": f"commit:{commit['hash']}",
                    "description": f"Reverted change: {orig}",
                    "resolution": "Review if revert addresses a conflicting requirement",
                    "severity": "high",
                })
                continue
            if subj.startswith("fix:") or subj.startswith("fix("):
                is_trivial = any(re.search(p, subj) for p in TRIVIAL_PATTERNS)
                is_sig = any(re.search(p, subj) for p in SIGNIFICANT_PATTERNS)
                if is_sig or not is_trivial:
                    conflicts.append({
                        "type": "fix", "source": f"commit:{commit['hash']}",
                        "description": f"Bug fix suggests incomplete requirement: {orig}",
                        "resolution": "Consider if original requirement needs clarification",
                        "severity": "high" if is_sig else "medium",
                    })
        self.signals["conflicts"] = conflicts
        lvl = "WARNING" if conflicts else "SUCCESS"
        self.log(lvl, f"Detected {len(conflicts)} potential conflicts")
        return conflicts

    # ── dynamic section generators ───────────────────────────────
    def _gen_metadata(self) -> str:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        ver = datetime.now().strftime("%Y-%m-%d")
        return (
            f"---\n"
            f'title: "PRD: IT-Journey – Open-Source IT Education Platform"\n'
            f'description: "Product requirements for IT-Journey"\n'
            f"date: {now}\nlastmod: {now}\nstatus: Living\nversion: {ver}\n"
            f"auto_generated: true\ngenerator: prd-machine\n"
            f"repository: https://github.com/bamr87/it-journey\n---\n"
        )

    def _gen_mvp_status(self) -> str:
        quest_n = sum(1 for f in self.signals["markdown_files"] if "_quests" in f["path"])
        post_n = sum(1 for f in self.signals["markdown_files"] if "_posts" in f["path"])
        md_n = len(self.signals["markdown_files"])
        feat_n = len(self.signals["features"])
        commit_n = len(self.signals["git_commits"])
        conflict_n = len(self.signals["conflicts"])
        c_status = "⚠️ Review needed" if conflict_n else "✅ None"
        return (
            f"### Current Content Status\n\n"
            f"| Source | Count | Status |\n|--------|-------|--------|\n"
            f"| Learning Quests | {quest_n} | ✅ Published |\n"
            f"| Educational Posts | {post_n} | ✅ Published |\n"
            f"| Total Markdown Files | {md_n} | ✅ Indexed |\n"
            f"| Implemented Features | {feat_n} | ✅ Tracked |\n"
            f"| Recent Commits | {commit_n} | ✅ Analyzed |\n"
            f"| Detected Issues | {conflict_n} | {c_status} |\n"
        )

    def _gen_edge_issues(self) -> str:
        conflicts = self.signals.get("conflicts", [])
        if not conflicts:
            return ""
        lines = ["\n### Recent Issues Detected\n"]
        sorted_c = sorted(conflicts, key=lambda c: 0 if c.get("severity") == "high" else 1)
        for c in sorted_c[:5]:
            icon = "🔴" if c.get("severity") == "high" else "🟡"
            lines.append(f"- {icon} **{c['type'].upper()}**: {c['description']}")
            lines.append(f"  - *Action*: {c['resolution']}")
        return "\n".join(lines) + "\n"

    # ── marker-based update engine ───────────────────────────────
    def _wrap(self, name: str, content: str) -> str:
        """Wrap content in AUTO markers."""
        begin = MARKER_BEGIN.format(name=name)
        end = MARKER_END.format(name=name)
        return f"{begin}\n{content}{end}"

    def _update_markers(self, doc: str, updates: Dict[str, str]) -> str:
        """Replace marker-delimited sections in doc with new content."""
        def _replacer(m: re.Match) -> str:
            name = m.group(1)
            if name in updates:
                begin = MARKER_BEGIN.format(name=name)
                end = MARKER_END.format(name=name)
                return f"{begin}\n{updates[name]}{end}"
            return m.group(0)  # preserve unknown markers
        return MARKER_RE.sub(_replacer, doc)

    # ── commands ─────────────────────────────────────────────────
    def init(self, output_path: Optional[Path] = None) -> bool:
        """Generate a new PRD.md with markers + static scaffolding."""
        output_path = output_path or self.prd_path
        self.log("HEADER", "═" * 50)
        self.log("HEADER", "   PRD MACHINE - Initializing PRD.md")
        self.log("HEADER", "═" * 50)

        self.ingest_git_commits()
        self.ingest_markdown_files()
        self.ingest_features()
        self.detect_conflicts()

        sections = [
            self._wrap("metadata", self._gen_metadata()),
            "",
            "# IT-Journey",
            "",
            "*Open-Source IT Education Platform*",
            "",
            self._wrap("status_line",
                f"> **Status:** Living | **Version:** {datetime.now().strftime('%Y-%m-%d')} | **Auto-Generated:** ✅\n"),
            "",
            _STATIC_SECTION_WHY,
            self._wrap("mvp_status", self._gen_mvp_status()),
            "",
            _STATIC_SECTION_UX,
            _STATIC_SECTION_API,
            _STATIC_SECTION_NFR,
            _STATIC_SECTION_EDGE_HEADER,
            self._wrap("edge_issues", self._gen_edge_issues()),
            "",
            _STATIC_SECTION_OOS,
            _STATIC_SECTION_ROAD,
            _STATIC_SECTION_RISK,
            _STATIC_SECTION_DONE,
        ]

        output_path.write_text("\n".join(sections), encoding="utf-8")
        self.log("SUCCESS", f"PRD initialized: {output_path}")
        return True

    def sync(self, output_path: Optional[Path] = None, days: int = 30) -> bool:
        """Update only marker-delimited sections in existing PRD.md."""
        output_path = output_path or self.prd_path

        if not output_path.exists():
            self.log("WARNING", "No PRD.md found — running init instead")
            return self.init(output_path)

        self.log("HEADER", "═" * 50)
        self.log("HEADER", "   PRD MACHINE - Syncing PRD.md")
        self.log("HEADER", "═" * 50)

        self.ingest_git_commits(days)
        self.ingest_markdown_files()
        self.ingest_features()
        self.detect_conflicts()

        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        ver = datetime.now().strftime("%Y-%m-%d")

        updates = {
            "metadata": self._gen_metadata(),
            "status_line": f"> **Status:** Living | **Version:** {ver} | **Auto-Generated:** ✅\n",
            "mvp_status": self._gen_mvp_status(),
            "edge_issues": self._gen_edge_issues(),
        }

        existing = output_path.read_text(encoding="utf-8")
        updated = self._update_markers(existing, updates)

        # Compare ignoring volatile metadata (dates inside markers)
        def _strip_volatile(s: str) -> str:
            s = re.sub(r"^(date|lastmod|version):.*$", "", s, flags=re.MULTILINE)
            return re.sub(r"\*\*Version:\*\*\s*\S+", "", s)

        if _strip_volatile(existing) == _strip_volatile(updated):
            self.log("INFO", "No meaningful changes — skipping write")
            return True

        output_path.write_text(updated, encoding="utf-8")
        self.log("SUCCESS", f"PRD synced: {output_path}")
        total = sum(len(v) for v in self.signals.values())
        self.log("INFO", f"Total signals processed: {total}")
        return True

    def check(self, pr_json_path: Optional[str] = None,
              ai: bool = False, model: str = "") -> Dict[str, Any]:
        """Determine if PRD needs updating. Returns analysis dict.

        Exit semantics (for CI):
          - result["needs_update"] == False  → exit 0
          - result["needs_update"] == True   → exit 1
        """
        self.log("HEADER", "═" * 50)
        self.log("HEADER", "   PRD MACHINE - Quick Check")
        self.log("HEADER", "═" * 50)

        result: Dict[str, Any] = {
            "needs_update": False,
            "affected_sections": [],
            "reason": "",
            "changed_files": [],
            "ai_analysis": None,
        }

        # 1. Gather changed files — from PR JSON or git log
        changed_files = self._get_changed_files(pr_json_path)
        result["changed_files"] = changed_files

        if not changed_files:
            result["reason"] = "No relevant file changes detected"
            self.log("INFO", result["reason"])
            return result

        # 2. Map changed files → affected sections via relevance map
        affected: set = set()
        for fpath in changed_files:
            for pattern, sections in SECTION_RELEVANCE.items():
                if fnmatch(fpath, pattern):
                    affected.update(sections)

        result["affected_sections"] = sorted(affected)

        if not affected:
            result["reason"] = f"{len(changed_files)} files changed but none affect dynamic PRD sections"
            self.log("INFO", result["reason"])
            return result

        result["needs_update"] = True
        result["reason"] = (
            f"{len(changed_files)} files changed affecting sections: "
            + ", ".join(sorted(affected))
        )
        self.log("WARNING", result["reason"])

        # 3. Optional AI analysis
        if ai and affected:
            analysis = self._ai_analyze(changed_files, list(affected), model)
            result["ai_analysis"] = analysis

        return result

    def _get_changed_files(self, pr_json_path: Optional[str] = None) -> List[str]:
        """Get list of changed files from PR JSON or git log."""
        # Try PR JSON first
        pr_path = pr_json_path or os.environ.get("GITHUB_EVENT_PATH")
        if pr_path and Path(pr_path).exists():
            try:
                event = json.loads(Path(pr_path).read_text(encoding="utf-8"))
                pr = event.get("pull_request", {})
                base_sha = pr.get("base", {}).get("sha", "")
                head_sha = pr.get("head", {}).get("sha", "")
                if base_sha and head_sha:
                    out = subprocess.run(
                        ["git", "diff", "--name-only", base_sha, head_sha],
                        capture_output=True, text=True, cwd=self.repo_root,
                    )
                    files = [f for f in out.stdout.strip().split("\n") if f]
                    self.log("INFO", f"Got {len(files)} changed files from PR event")
                    return files
            except Exception as e:
                self.log("WARNING", f"Failed to read PR event: {e}")

        # Fallback: files changed since last PRD modification
        if self.prd_path.exists():
            mtime = self.prd_path.stat().st_mtime
            since = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
            try:
                out = subprocess.run(
                    ["git", "log", f"--since={since}", "--name-only",
                     "--pretty=format:", "--diff-filter=ACMR"],
                    capture_output=True, text=True, cwd=self.repo_root,
                )
                files = sorted(set(f for f in out.stdout.strip().split("\n") if f))
                self.log("INFO", f"Got {len(files)} changed files since last PRD update")
                return files
            except subprocess.CalledProcessError:
                pass

        return []

    # ── AI analysis via GitHub Models API ────────────────────────
    def _ai_analyze(self, changed_files: List[str],
                    affected_sections: List[str],
                    model: str = "") -> Optional[Dict[str, Any]]:
        """Use GitHub Models API for semantic analysis of changes."""
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            self.log("INFO", "No GITHUB_TOKEN — skipping AI analysis")
            return None

        model = model or os.environ.get("PRD_AI_MODEL", "openai/gpt-4o-mini")
        endpoint = "https://models.github.ai/inference/chat/completions"

        prompt = self._build_analysis_prompt(changed_files, affected_sections)

        payload = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content":
                    "You are a product requirements analyst. Given a list of "
                    "changed files and affected PRD sections, provide a brief "
                    "JSON analysis with: needs_update (bool), summary (string), "
                    "and suggestions (list of strings for human-editable sections "
                    "that might need manual review). Be concise."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 500,
        }).encode("utf-8")

        req = Request(endpoint, data=payload, method="POST")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")

        try:
            self.log("INFO", f"Calling GitHub Models API ({model})...")
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            # Try to parse JSON from response
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                self.log("SUCCESS", f"AI analysis: {analysis.get('summary', 'done')}")
                return analysis
            return {"summary": content, "needs_update": True, "suggestions": []}
        except (URLError, json.JSONDecodeError, KeyError) as e:
            self.log("WARNING", f"AI analysis failed (falling back to rule-based): {e}")
            return None

    def _build_analysis_prompt(self, changed_files: List[str],
                               sections: List[str]) -> str:
        return (
            f"Changed files in this PR:\n"
            + "\n".join(f"- {f}" for f in changed_files[:30])
            + f"\n\nAffected dynamic PRD sections: {', '.join(sections)}\n\n"
            f"Human-editable PRD sections (not auto-updated): "
            f"WHY, UX, API, NFR, OOS, ROAD, RISK, DONE\n\n"
            f"Should any human-editable sections be reviewed or updated "
            f"based on these changes? Respond with JSON."
        )

    # ── status / conflicts ───────────────────────────────────────
    def show_status(self) -> None:
        self.log("HEADER", "═" * 50)
        self.log("HEADER", "   PRD MACHINE - Status")
        self.log("HEADER", "═" * 50)
        if not self.prd_path.exists():
            self.log("WARNING", "No PRD.md found. Run 'prd-machine init'.")
            return
        stat = self.prd_path.stat()
        age_h = (datetime.now(timezone.utc).timestamp() - stat.st_mtime) / 3600
        health = "healthy" if age_h < 6 else ("stale" if age_h < 24 else "outdated")
        lvl = {"healthy": "SUCCESS", "stale": "WARNING", "outdated": "ERROR"}[health]
        self.log("INFO", f"PRD Path: {self.prd_path}")
        mod = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
        self.log("INFO", f"Last Modified: {mod}")
        self.log("INFO", f"Age: {round(age_h, 1)} hours")
        self.log(lvl, f"Health: {health.upper()}")

    def show_conflicts(self, days: int = 30) -> int:
        self.ingest_git_commits(days)
        conflicts = self.detect_conflicts()
        if not conflicts:
            self.log("SUCCESS", "No conflicts detected")
            return 0
        self.log("WARNING", f"Found {len(conflicts)} conflicts:")
        for c in conflicts:
            icon = "🔴" if c.get("severity") == "high" else "🟡"
            print(f"  {icon} [{c['type']}] {c['description']}")
            print(f"    Resolution: {c['resolution']}")
        return 0


# ════════════════════════════════════════════════════════════════
# Static section templates (used only by `init`)
# ════════════════════════════════════════════════════════════════

_STATIC_SECTION_WHY = """\
## 0. WHY

Build **IT-Journey** — an open-source educational platform that democratizes IT education
through gamified quests, practical tutorials, and AI-enhanced learning experiences,
transforming complete beginners into skilled IT professionals.

**KFI:** 100% of learners who complete a quest path can demonstrate measurable skill
improvement through hands-on projects in their portfolio.
"""

_STATIC_SECTION_UX = """\
## 2. UX (User eXperience Flow)

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

_STATIC_SECTION_API = """\
## 3. API (Atomic Programmable Interface)

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
python3 scripts/prd-machine/prd-machine.py sync

# Link health check
python3 scripts/validation/link-checker.py --scope website
```

### GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `build-validation.yml` | Push/PR | Validate Jekyll build |
| `link-checker.yml` | Schedule/Manual | Check link health |
| `prd-sync.yml` | PR merge/Manual | Update PRD.md |
| `frontmatter-validation.yml` | Push | Validate content metadata |
"""

_STATIC_SECTION_NFR = """\
## 4. NFR (Non-Functional Realities)

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

_STATIC_SECTION_EDGE_HEADER = """\
## 5. EDGE (Exceptions, Dependencies, Gotchas)

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
"""

_STATIC_SECTION_OOS = """\
## 6. OOS (Out Of Scope)

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

_STATIC_SECTION_ROAD = """\
## 7. ROAD (Roadmap)

| Milestone | Objective | Target | Status |
|-----------|-----------|--------|--------|
| **Foundation** | Jekyll site + GitHub Pages deployment | 2024 Q1 | ✅ Complete |
| **Content** | Initial quest collection + tutorials | 2024 Q2 | ✅ Complete |
| **Guardian 2.0** | Advanced link monitoring + AI analysis | 2025 Q1 | ✅ Complete |
| **PRD Machine** | Automated requirements documentation | 2025 Q4 | ✅ Complete |
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

_STATIC_SECTION_RISK = """\
## 8. RISK (Top Risks)

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

_STATIC_SECTION_DONE = """\
## 9. DONE (Definition of Done)

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


# ════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(
        description="PRD MACHINE v2 - PR-Driven Product Reality Distillery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  prd-machine init                    # Create PRD.md with markers
  prd-machine sync                    # Update dynamic sections
  prd-machine check                   # Quick: does PRD need updating?
  prd-machine check --ai              # AI-enhanced analysis
  prd-machine check --pr-json ev.json # Analyze a specific PR
  prd-machine status                  # Health check
  prd-machine conflicts               # Show conflicts
""",
    )
    sub = parser.add_subparsers(dest="command")

    # init
    init_p = sub.add_parser("init", help="Create PRD.md with markers + scaffolding")
    init_p.add_argument("-o", "--output", type=str, default=None)

    # sync
    sync_p = sub.add_parser("sync", help="Update dynamic sections in PRD.md")
    sync_p.add_argument("--days", type=int, default=30)
    sync_p.add_argument("-o", "--output", type=str, default=None)
    sync_p.add_argument("--ai", action="store_true", help="Enable AI analysis")
    sync_p.add_argument("--model", type=str, default="", help="AI model override")

    # check
    check_p = sub.add_parser("check", help="Quick check: does PRD need updating?")
    check_p.add_argument("--pr-json", type=str, default=None, help="Path to PR event JSON")
    check_p.add_argument("--ai", action="store_true", help="Enable AI analysis")
    check_p.add_argument("--model", type=str, default="", help="AI model override")

    # status
    sub.add_parser("status", help="Show PRD health")

    # conflicts
    conflicts_p = sub.add_parser("conflicts", help="Show detected conflicts")
    conflicts_p.add_argument("--days", type=int, default=30)

    parser.add_argument("--version", action="version", version=f"prd-machine {VERSION}")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    machine = PRDMachine()

    if args.command == "init":
        out = Path(args.output) if args.output else None
        return 0 if machine.init(out) else 1

    if args.command == "sync":
        out = Path(args.output) if args.output else None
        return 0 if machine.sync(out, days=args.days) else 1

    if args.command == "check":
        result = machine.check(
            pr_json_path=args.pr_json,
            ai=args.ai,
            model=args.model,
        )
        # Output JSON for CI consumption
        print(json.dumps(result, indent=2))
        return 1 if result["needs_update"] else 0

    if args.command == "status":
        machine.show_status()
        return 0

    if args.command == "conflicts":
        return machine.show_conflicts(days=args.days)

    return 0


if __name__ == "__main__":
    sys.exit(main())
