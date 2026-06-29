#!/usr/bin/env python3
"""
triage_findings.py — classify crawler findings (theme vs content) and dedup.

Reads .frontend/findings.jsonl (from crawl.mjs) and .frontend/config.yml, groups
findings by their route-independent `signature`, decides which are THEME issues
(site-wide defects that belong upstream in the theme repo) vs content issues (keep
in it-journey), dedups the theme ones against EXISTING upstream issues, and writes
.frontend/upstream-candidates.json — the shortlist the theme-scout agent files.

  THEME (file upstream) when site-wide:
    - http-error whose path matches a theme-injected path (/authors, /tags,
      /search.json, /sitemap, /assets/js, …) — hits every remote-theme consumer
    - console-error referencing a theme asset bundle, OR recurring across routes
    - a11y / horizontal-overflow recurring across >= recur_threshold routes
  CONTENT (keep local) otherwise:
    - a single route 4xx/5xx, an img missing alt, a one-off page error

READ-ONLY: uses `gh` only to LIST existing upstream issues for dedup; never
creates/edits anything. Exit 0 on success (degrades to an empty candidate list).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG = ROOT / ".frontend" / "config.yml"


def warn(msg: str) -> None:
    print(f"::warning::{msg}", file=sys.stderr)


def load_config() -> dict[str, Any]:
    try:
        return yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        warn(f"{CONFIG} not found; using defaults")
        return {}


def load_findings(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        warn(f"{path} not found; no findings to triage")
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def fetch_upstream_issues(repo: str, state: str) -> list[dict[str, Any]]:
    """List existing upstream issues (title+body) for dedup. [] on any gh error."""
    cmd = ["gh", "issue", "list", "--repo", repo, "--state", state,
           "--limit", "500", "--json", "number,title,body"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
    except (OSError, FileNotFoundError) as exc:
        warn(f"gh unavailable for dedup ({exc}); treating as no existing issues")
        return []
    if proc.returncode != 0:
        warn(f"gh issue list failed ({proc.stderr.strip()[:160]}); skipping dedup")
        return []
    try:
        return json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return []


def classify(group: dict[str, Any], cls: dict[str, Any]) -> bool:
    """Return True if this signature-group is a THEME issue (file upstream)."""
    kind = group["kind"]
    details = " ".join(group["details"]).lower()
    n_routes = len(group["routes"])

    if kind in (cls.get("content_only_kinds") or []):
        return False
    if kind == "http-error":
        return any(h.lower() in details for h in (cls.get("theme_injected_paths") or []))
    if kind == "console-error":
        if any(h.lower() in details for h in (cls.get("theme_asset_hints") or [])):
            return True
        return n_routes >= int(cls.get("recur_threshold", 2))
    if kind in (cls.get("site_wide_kinds") or []):
        return n_routes >= int(cls.get("recur_threshold", 2))
    # page-status / navigation-error / anything else -> content (route-specific).
    return False


SEV_RANK = {"critical": 4, "serious": 3, "high": 3, "moderate": 2, "medium": 2,
            "minor": 1, "low": 1}


def group_findings(findings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for f in findings:
        s = f.get("signature") or ""
        g = groups.setdefault(s, {
            "signature": s, "kind": f.get("kind"), "rule": f.get("rule"),
            "routes": set(), "viewports": set(), "details": [],
            "severity": "low", "help_url": f.get("help_url"),
        })
        if f.get("route"):
            g["routes"].add(f["route"])
        if f.get("viewport"):
            g["viewports"].add(f["viewport"])
        if f.get("detail") and f["detail"] not in g["details"]:
            g["details"].append(f["detail"])
        if SEV_RANK.get(str(f.get("severity")), 0) > SEV_RANK.get(g["severity"], 0):
            g["severity"] = str(f.get("severity"))
    return groups


def area_label(kind: str) -> str:
    return {"a11y": "area:a11y", "img-missing-alt": "area:a11y",
            "http-error": "area:infra", "console-error": "area:infra",
            "horizontal-overflow": "area:a11y"}.get(kind, "area:infra")


def suggest_title(g: dict[str, Any]) -> str:
    kind = g["kind"]
    sample = (g["details"][0] if g["details"] else kind)
    if kind == "a11y":
        return f"a11y: {sample}"[:100]
    if kind == "http-error":
        return f"theme: site-wide {sample} (404 on theme-injected link)"[:100]
    if kind == "horizontal-overflow":
        return f"theme: horizontal overflow on mobile ({len(g['routes'])} routes)"[:100]
    if kind == "console-error":
        return f"theme: console error — {sample}"[:100]
    return f"theme: {sample}"[:100]


def main() -> int:
    cfg = load_config()
    cls = cfg.get("classification") or {}
    out_cfg = cfg.get("output") or {}
    dedup = cfg.get("dedup") or {}
    repo = cfg.get("upstream_repo") or "bamr87/zer0-mistakes"

    findings_path = ROOT / out_cfg.get("findings", ".frontend/findings.jsonl")
    cand_path = ROOT / out_cfg.get("candidates", ".frontend/upstream-candidates.json")

    findings = load_findings(findings_path)
    groups = group_findings(findings)

    theme_groups = [g for g in groups.values() if classify(g, cls)]
    theme_groups.sort(key=lambda g: (-SEV_RANK.get(g["severity"], 0), -len(g["routes"])))

    existing = fetch_upstream_issues(repo, str(dedup.get("upstream_state", "all")))
    existing_blob = "\n".join(
        f"{i.get('title','')}\n{i.get('body','')}" for i in existing
    ).lower()

    candidates = []
    cap = int(dedup.get("max_new_issues_per_run", 5) or 0)
    deduped = 0
    for g in theme_groups:
        # Dedup: skip if the signature or a distinctive detail phrase already
        # appears in an existing upstream issue.
        key = (g["details"][0] if g["details"] else g["signature"]).lower()
        if g["signature"] in existing_blob or (len(key) > 12 and key in existing_blob):
            deduped += 1
            continue
        candidates.append({
            "signature": g["signature"],
            "kind": g["kind"],
            "rule": g.get("rule"),
            "severity": g["severity"],
            "routes": sorted(g["routes"]),
            "viewports": sorted(g["viewports"]),
            "detail": g["details"][0] if g["details"] else "",
            "evidence": g["details"][:5],
            "help_url": g.get("help_url"),
            "suggested_title": suggest_title(g),
            "suggested_labels": sorted({"bug", area_label(g["kind"])}),
        })

    truncated = max(0, len(candidates) - cap) if cap else 0
    if cap:
        candidates = candidates[:cap]

    result = {
        "upstream_repo": repo,
        "total_findings": len(findings),
        "signatures": len(groups),
        "theme_signatures": len(theme_groups),
        "deduped_against_existing": deduped,
        "candidates": candidates,
        "truncated": truncated,
    }
    cand_path.parent.mkdir(parents=True, exist_ok=True)
    cand_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(f"findings={len(findings)} signatures={len(groups)} "
          f"theme={len(theme_groups)} deduped={deduped} "
          f"candidates={len(candidates)}"
          + (f" (+{truncated} over cap)" if truncated else ""))
    if truncated:
        warn(f"{truncated} theme candidate(s) over max_new_issues_per_run — not filed this run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
