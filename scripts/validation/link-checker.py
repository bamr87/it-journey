#!/usr/bin/env python3
"""
IT-Journey Link Health Guardian v3.0 — Optimized Link Checker

Unified link checking with:
- Lychee (primary, via .lychee.toml) or curl (fallback) engines
- Persistent caching via .lycheecache (cross-run)
- Incremental --changed-only mode for PR checks
- Delta-only AI analysis (only new broken links sent to AI)
- Multi-provider AI (OpenAI, Anthropic, or none)
- --include-site flag for opt-in _site/ scanning
- Timing instrumentation for performance tracking
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None  # AI analysis unavailable without requests

# Allow importing the shared AI client from scripts/lib/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "lib"))
try:
    from ai_client import AIClient
except ImportError:
    AIClient = None  # Fallback if module not available


class LinkHealthGuardian:
    VERSION = "3.0.0"

    def __init__(self, config):
        self.config = config
        self.output_dir = config.get("output_dir", "link-check-results")
        self.results = {}
        self.analysis = {}
        self.timings = {}
        self._colors = {
            "INFO": "\033[0;34m",
            "SUCCESS": "\033[0;32m",
            "WARNING": "\033[1;33m",
            "ERROR": "\033[0;31m",
            "NC": "\033[0m",
        }
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    # -- Logging -----------------------------------------------------------
    def log(self, level, message):
        c = self._colors.get(level, "")
        nc = self._colors["NC"]
        print(f"{c}[{level}]{nc} {message}")

    # -- Timing helpers ----------------------------------------------------
    def _start(self, label):
        self.timings[label] = {"start": time.monotonic()}

    def _stop(self, label):
        t = self.timings.get(label, {})
        t["end"] = time.monotonic()
        t["elapsed"] = t["end"] - t.get("start", t["end"])
        self.timings[label] = t

    def _elapsed(self, label):
        return self.timings.get(label, {}).get("elapsed", 0)

    # -- Scope / file selection --------------------------------------------
    def determine_scope_files(self):
        scope = self.config.get("scope", "website")
        scope_map = {
            "website": ".", "all": ".", "docs": "docs/",
            "posts": "pages/_posts/", "quests": "pages/_quests/",
            "internal": ".", "external": ".",
        }
        base = scope_map.get(scope, ".")

        if self.config.get("changed_only"):
            files = self._get_changed_files()
            if files:
                self.log("INFO", f"--changed-only: {len(files)} changed file(s)")
                return files
            self.log("WARNING", "--changed-only found no changes; falling back to full scan")

        self.log("INFO", f'Scope "{scope}" -> base path: {base}')
        return [base]

    def _get_changed_files(self):
        diff_range = self.config.get("diff_range", "origin/main...HEAD")
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR", diff_range],
                capture_output=True, text=True, check=True,
            )
            all_changed = result.stdout.strip().splitlines()
            exts = {".md", ".html", ".htm"}
            return [f for f in all_changed if Path(f).suffix.lower() in exts and os.path.isfile(f)]
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []

    # -- Engine: Lychee ----------------------------------------------------
    def run_lychee(self, files):
        output_file = os.path.join(self.output_dir, "lychee_results.json")
        cmd = ["lychee", "--output", output_file]

        if self.config.get("include_site"):
            cmd.extend(["--include-path", "_site/"])

        cmd.extend(files)
        self.log("INFO", f"Running: {' '.join(cmd[:8])}{'...' if len(cmd) > 8 else ''}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            self.log("INFO", f"Lychee exit code: {result.returncode}")
            if result.stderr:
                for line in result.stderr.strip().splitlines()[:5]:
                    self.log("INFO", f"  stderr: {line}")

            if not os.path.exists(output_file):
                if result.stdout.strip():
                    try:
                        data = json.loads(result.stdout)
                        with open(output_file, "w") as f:
                            json.dump(data, f, indent=2)
                    except json.JSONDecodeError:
                        pass
                if not os.path.exists(output_file):
                    with open(output_file, "w") as f:
                        json.dump({"fail_map": {}, "error_map": {}}, f)

            return True
        except subprocess.TimeoutExpired:
            self.log("ERROR", "Lychee timed out after 30 minutes")
            return False
        except FileNotFoundError:
            self.log("ERROR", "lychee not found -- install it or use --engine curl")
            return False

    # -- Engine: curl (fallback) ---------------------------------------------
    def run_curl(self, files):
        self.log("INFO", "Using curl engine (fallback)")
        url_pattern = re.compile(r'https?://[^\s\)\]>"' + "'" + r']+')
        urls_by_file = defaultdict(set)

        for fpath in files:
            p = Path(fpath)
            if p.is_dir():
                targets = list(p.rglob("*.md")) + list(p.rglob("*.html"))
            elif p.is_file():
                targets = [p]
            else:
                continue
            for target in targets:
                try:
                    text = target.read_text(errors="replace")
                    for url in url_pattern.findall(text):
                        urls_by_file[str(target)].add(url)
                except OSError:
                    pass

        total = sum(len(v) for v in urls_by_file.values())
        self.log("INFO", f"Found {total} URLs across {len(urls_by_file)} files")

        fail_map = {}
        ok_count = 0
        for fpath, urls in urls_by_file.items():
            failures = []
            for url in urls:
                try:
                    r = subprocess.run(
                        ["curl", "-sSf", "-o", "/dev/null", "-w", "%{http_code}",
                         "--max-time", "15", "-L", url],
                        capture_output=True, text=True, timeout=20,
                    )
                    code = r.stdout.strip()
                    if r.returncode != 0:
                        failures.append({"url": url, "status": {"code": int(code) if code.isdigit() else 0, "details": "Failed"}})
                    else:
                        ok_count += 1
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                    failures.append({"url": url, "status": {"code": 0, "details": "Timeout"}})
            if failures:
                fail_map[fpath] = failures

        output_file = os.path.join(self.output_dir, "lychee_results.json")
        data = {"fail_map": fail_map, "total": total, "successful": ok_count, "failures": total - ok_count}
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        return True

    # -- Parse results -----------------------------------------------------
    def parse_results(self):
        results_file = os.path.join(self.output_dir, "lychee_results.json")
        if not os.path.exists(results_file):
            self.log("WARNING", "No results file found")
            return False

        try:
            with open(results_file) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            self.log("ERROR", f"Failed to read results: {e}")
            return False

        fail_map = data.get("fail_map", {})
        error_map = data.get("error_map", {})
        all_failures = defaultdict(list)
        for m in (fail_map, error_map):
            for fpath, entries in m.items():
                all_failures[fpath].extend(entries)

        broken = sum(len(v) for v in all_failures.values())
        total = data.get("total", broken)
        successful = data.get("successful", total - broken)
        if total == 0 and broken == 0:
            total = broken
            successful = 0
        rate = (successful / total * 100) if total > 0 else 100.0

        self.results = {
            "total_links": total,
            "successful_links": successful,
            "broken_links": broken,
            "success_rate": round(rate, 1),
            "fail_map": dict(all_failures),
            "raw_data": data,
        }

        stats_file = os.path.join(self.output_dir, "statistics.env")
        with open(stats_file, "w") as f:
            f.write(f"TOTAL_COUNT={total}\n")
            f.write(f"BROKEN_COUNT={broken}\n")
            f.write(f"SUCCESS_RATE={rate:.1f}\n")

        self.log("SUCCESS", f"Parsed: {total} total, {broken} broken, {rate:.1f}% success")
        return True

    # -- Generate markdown summary -----------------------------------------
    def generate_markdown_summary(self):
        summary_path = os.path.join(self.output_dir, "summary.md")
        fail_map = self.results.get("fail_map", {})

        lines = [
            "# Link Health Summary\n",
            f"**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ",
            f"**Total**: {self.results['total_links']}  ",
            f"**Broken**: {self.results['broken_links']}  ",
            f"**Success rate**: {self.results['success_rate']}%\n",
        ]

        if fail_map:
            lines.append("## Failures by file\n")
            for fpath, entries in sorted(fail_map.items()):
                lines.append(f"### {fpath}\n")
                for e in entries[:20]:
                    url = e.get("url", "?")
                    status = e.get("status", "")
                    if isinstance(status, dict):
                        status = status.get("details", status.get("code", ""))
                    lines.append(f"- [{status}] {url}")
                if len(entries) > 20:
                    lines.append(f"- ... and {len(entries) - 20} more\n")
                lines.append("")

        with open(summary_path, "w") as f:
            f.write("\n".join(lines))
        self.log("INFO", f"Summary written to {summary_path}")

    # -- Analyze failures --------------------------------------------------
    def analyze_failures(self):
        self.log("INFO", "Analyzing failure patterns...")
        fail_map = self.results.get("fail_map", {})

        categories = defaultdict(list)
        for fpath, entries in fail_map.items():
            for entry in entries:
                url = entry.get("url", "")
                status = entry.get("status", "")
                if isinstance(status, dict):
                    msg = str(status.get("details", status.get("code", ""))).lower()
                else:
                    msg = str(status).lower()
                rec = {"url": url, "error": msg, "file": fpath}

                if any(t in msg for t in ("ssl", "tls", "certificate")):
                    categories["ssl_errors"].append(rec)
                elif any(t in msg for t in ("dns", "resolve", "hostname")):
                    categories["dns_errors"].append(rec)
                elif any(t in msg for t in ("timeout", "timed out")):
                    categories["timeouts"].append(rec)
                elif any(t in msg for t in ("429", "rate limit", "too many")):
                    categories["rate_limited"].append(rec)
                elif any(t in msg for t in ("network", "connection", "refused")):
                    categories["network_errors"].append(rec)
                elif url.startswith("http"):
                    categories["broken_external"].append(rec)
                elif url.startswith("/") or not url.startswith("http"):
                    categories["broken_internal"].append(rec)
                else:
                    categories["unknown"].append(rec)

        domain_counts = defaultdict(int)
        for cat in ("broken_external", "timeouts", "rate_limited", "ssl_errors", "dns_errors"):
            for item in categories.get(cat, []):
                try:
                    domain_counts[item["url"].split("/")[2]] += 1
                except (IndexError, AttributeError):
                    pass

        patterns = []
        if domain_counts:
            top = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            patterns.append(f"Top failing domains: {', '.join(f'{d} ({c})' for d, c in top)}")
        n_internal = len(categories.get("broken_internal", []))
        if n_internal:
            patterns.append(f"{n_internal} broken internal links -- check Jekyll config")
        n_timeout = len(categories.get("timeouts", []))
        if n_timeout > 5:
            patterns.append(f"High timeout rate ({n_timeout}) -- network or slow sites")

        cat_counts = {k: len(v) for k, v in categories.items()}
        most_common = max(cat_counts, key=cat_counts.get) if cat_counts else "none"

        self.analysis = {
            "categories": dict(categories),
            "patterns": patterns,
            "summary": {
                "total_broken": sum(cat_counts.values()),
                "most_common_error": most_common,
                "problematic_domains": [d for d, _ in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:5]],
            },
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self._write_analysis_report()

        with open(os.path.join(self.output_dir, "analysis_summary.env"), "w") as f:
            f.write(f"ANALYSIS_AVAILABLE=true\n")
            f.write(f"PATTERNS_COUNT={len(patterns)}\n")
            f.write(f"MOST_COMMON_ERROR={most_common}\n")

        self.log("SUCCESS", f"Analysis done: {len(patterns)} patterns identified")
        return True

    def _write_analysis_report(self):
        path = os.path.join(self.output_dir, "detailed_analysis.md")
        with open(path, "w") as f:
            f.write("# Link Health Analysis Report\n\n")
            f.write(f"**Date**: {self.analysis['analysis_timestamp']}\n")
            f.write(f"**Total**: {self.results['total_links']} | ")
            f.write(f"**Broken**: {self.results['broken_links']} | ")
            f.write(f"**Rate**: {self.results['success_rate']}%\n\n")

            for cat, items in self.analysis["categories"].items():
                if not items:
                    continue
                f.write(f"## {cat.replace('_', ' ').title()} ({len(items)})\n\n")
                for item in items[:10]:
                    f.write(f"- `{item['url']}` in {item['file']} -- {item['error']}\n")
                if len(items) > 10:
                    f.write(f"- ... and {len(items) - 10} more\n")
                f.write("\n")

            if self.analysis["patterns"]:
                f.write("## Patterns\n\n")
                for p in self.analysis["patterns"]:
                    f.write(f"- {p}\n")

    # -- Delta computation -------------------------------------------------
    def compute_delta(self):
        baseline_path = os.path.join(self.output_dir, "broken_links_baseline.json")
        current_broken = set()
        for entries in self.results.get("fail_map", {}).values():
            for e in entries:
                current_broken.add(e.get("url", ""))

        previous_broken = set()
        if os.path.exists(baseline_path):
            try:
                with open(baseline_path) as f:
                    previous_broken = set(json.load(f))
            except (json.JSONDecodeError, OSError):
                pass

        new_broken = current_broken - previous_broken
        fixed = previous_broken - current_broken

        with open(baseline_path, "w") as f:
            json.dump(sorted(current_broken), f, indent=2)

        self.log("INFO", f"Delta: {len(new_broken)} new broken, {len(fixed)} fixed since last run")
        return new_broken, fixed

    # -- AI analysis (delta-only, vendor-agnostic via AIClient) -------------
    def run_ai_analysis(self, new_broken, fixed):
        if self.config.get("dry_run_ai"):
            self.log("INFO", "--dry-run-ai: skipping AI call")
            prompt = self._build_prompt(new_broken, fixed)
            self.log("INFO", f"Prompt would be ({len(prompt)} chars):\n{prompt[:500]}...")
            return self._fallback_ai(new_broken, fixed)

        provider = self.config.get("ai_provider", "none")
        if provider == "none":
            return self._fallback_ai(new_broken, fixed)

        if not new_broken:
            self.log("INFO", "No new broken links -- skipping AI analysis")
            content = f"# AI Analysis\n\nNo **new** broken links since last run. {len(fixed)} link(s) fixed.\n"
            self._save_ai(content, False)
            return True

        if AIClient is None:
            self.log("WARNING", "AIClient module not available -- using fallback")
            return self._fallback_ai(new_broken, fixed)

        prompt = self._build_prompt(new_broken, fixed)
        self.log("INFO", f"Sending {len(new_broken)} new broken link(s) to {provider}...")

        client = AIClient(
            provider=provider,
            model=self.config.get("ai_model"),
        )
        result = client.chat(
            prompt=prompt,
            system="You are a concise link-health advisor for a Jekyll educational site. Be brief.",
            max_tokens=500,
            temperature=0.2,
        )

        if result.success:
            self._save_ai(result.content, True)
            self.log("SUCCESS", f"{result.provider} analysis complete (model: {result.model})")
            return True

        self.log("WARNING", f"AI call failed: {result.error} -- using fallback")
        return self._fallback_ai(new_broken, fixed)

    def _build_prompt(self, new_broken, fixed):
        sample = sorted(new_broken)[:10]
        lines = ["New broken links found on it-journey.dev (educational Jekyll site):", ""]
        for url in sample:
            lines.append(f"- {url}")
        if len(new_broken) > 10:
            lines.append(f"... and {len(new_broken) - 10} more")
        lines.append("")
        lines.append(f"Links fixed since last run: {len(fixed)}")
        lines.append("")
        lines.append("Give 3 concise prioritized actions to fix these. Markdown format.")
        return "\n".join(lines)

    def _fallback_ai(self, new_broken=None, fixed=None):
        r = self.results
        a = self.analysis
        most_common = a.get("summary", {}).get("most_common_error", "unknown")
        content = (
            "# Link Analysis (Template)\n\n"
            f"**Total**: {r.get('total_links', 0)} | "
            f"**Broken**: {r.get('broken_links', 0)} | "
            f"**Rate**: {r.get('success_rate', 0)}%\n\n"
            f"## Top Issue: {most_common.replace('_', ' ').title()}\n\n"
            "### Recommended Actions\n"
            "1. Fix internal broken links first (navigation impact)\n"
            "2. Update or remove broken external references\n"
            "3. Add flaky domains to `.lycheeignore`\n\n"
            "*Enhanced analysis requires `--ai-provider openai` or "
            "`--ai-provider anthropic` with the corresponding API key.*\n"
        )
        self._save_ai(content, False)
        return True

    def _save_ai(self, content, is_ai_powered):
        with open(os.path.join(self.output_dir, "ai_analysis.md"), "w") as f:
            f.write(content)
        with open(os.path.join(self.output_dir, "ai_analysis_summary.env"), "w") as f:
            f.write(f"AI_ANALYSIS_AVAILABLE=true\n")
            f.write(f"AI_POWERED={str(is_ai_powered).lower()}\n")
        self.log("INFO", "AI analysis saved")

    # -- GitHub issue creation ---------------------------------------------
    def create_github_issue(self):
        if not self.config.get("create_issue"):
            return False
        broken = self.results.get("broken_links", 0)
        date_str = datetime.now().strftime("%Y-%m-%d")
        title = f"Link Health: {broken} broken ({date_str})" if broken else f"Links healthy ({date_str})"

        body_file = os.path.join(self.output_dir, "issue_body.md")
        with open(body_file, "w") as f:
            f.write("# Link Health Report\n\n")
            f.write(f"- Total: {self.results['total_links']}\n")
            f.write(f"- Broken: {broken}\n")
            f.write(f"- Rate: {self.results['success_rate']}%\n\n")
            f.write("See attached artifacts for details.\n")

        try:
            subprocess.run(
                ["gh", "issue", "create", "--title", title, "--body-file", body_file,
                 "--label", "automated,link-checker"],
                check=True, capture_output=True, text=True,
            )
            self.log("SUCCESS", "GitHub issue created")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.log("WARNING", f"Issue creation failed: {e}")
            return False

    # -- Timing report -----------------------------------------------------
    def _write_timings(self):
        stats_file = os.path.join(self.output_dir, "statistics.env")
        with open(stats_file, "a") as f:
            for label in ("lychee", "parse", "analysis", "ai", "total"):
                val = self._elapsed(label)
                if val:
                    f.write(f"TIME_{label.upper()}={val:.1f}\n")

    # -- Main workflow -----------------------------------------------------
    def run(self):
        self.log("INFO", f"IT-Journey Link Health Guardian v{self.VERSION}")
        self.log("INFO", "=" * 50)
        self._start("total")

        # 1. Determine files
        files = self.determine_scope_files()

        # 2. Run engine
        engine = self.config.get("engine", "lychee")
        self._start("lychee")
        if engine == "curl":
            ok = self.run_curl(files)
        else:
            ok = self.run_lychee(files)
        self._stop("lychee")
        if not ok:
            return False

        # 3. Parse results
        self._start("parse")
        if not self.parse_results():
            self.log("WARNING", "Parse failed -- creating minimal results")
            self.results = {"total_links": 0, "successful_links": 0, "broken_links": 0,
                            "success_rate": 100.0, "fail_map": {}, "raw_data": {}}
        self._stop("parse")

        # 4. Generate markdown summary (no 2nd lychee run)
        self.generate_markdown_summary()

        # 5. Analyze failures
        self._start("analysis")
        analysis_level = self.config.get("analysis_level", "comprehensive")
        if analysis_level in ("standard", "comprehensive"):
            self.analyze_failures()
        self._stop("analysis")

        # 6. Delta + AI
        self._start("ai")
        new_broken, fixed = self.compute_delta()
        if analysis_level in ("comprehensive", "ai-only"):
            self.run_ai_analysis(new_broken, fixed)
        self._stop("ai")

        # 7. Issue
        self.create_github_issue()

        # 8. Timings
        self._stop("total")
        self._write_timings()

        self.log("INFO", f"Total time: {self._elapsed('total'):.1f}s")
        self.log("SUCCESS", "Link Health Guardian complete!")
        return self.results.get("broken_links", 0) == 0


def main():
    parser = argparse.ArgumentParser(
        description=f"IT-Journey Link Health Guardian v{LinkHealthGuardian.VERSION}",
    )
    parser.add_argument("--scope", default="website",
                        choices=["website", "internal", "external", "docs", "posts", "quests", "all"])
    parser.add_argument("--analysis-level", default="comprehensive",
                        choices=["basic", "standard", "comprehensive", "ai-only"])
    parser.add_argument("--output-dir", default="link-check-results")

    parser.add_argument("--engine", default="lychee", choices=["lychee", "curl"],
                        help="Link checking engine")

    parser.add_argument("--changed-only", action="store_true",
                        help="Only check files changed vs main branch")
    parser.add_argument("--diff-range", default="origin/main...HEAD",
                        help="Git diff range for --changed-only")

    parser.add_argument("--include-site", action="store_true",
                        help="Also scan _site/ directory")

    parser.add_argument("--ai-provider", default="none",
                        choices=["openai", "anthropic", "none"],
                        help="AI provider for analysis")
    parser.add_argument("--ai-model", default=None,
                        help="Override default AI model")
    parser.add_argument("--dry-run-ai", action="store_true",
                        help="Show AI prompt without calling API")

    parser.add_argument("--create-issue", action="store_true")

    args = parser.parse_args()

    config = {
        "scope": args.scope,
        "analysis_level": args.analysis_level,
        "output_dir": args.output_dir,
        "engine": args.engine,
        "changed_only": args.changed_only,
        "diff_range": args.diff_range,
        "include_site": args.include_site,
        "ai_provider": args.ai_provider,
        "ai_model": args.ai_model,
        "dry_run_ai": args.dry_run_ai,
        "create_issue": args.create_issue,
    }

    guardian = LinkHealthGuardian(config)
    success = guardian.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
