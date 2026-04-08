#!/usr/bin/env python3
"""
Documentation Aggregator — Clone & Extract

Clones external repositories defined in docs_config.yml and extracts
documentation files into a staging area for transformation.

Usage:
    python3 aggregate.py [--config docs_config.yml] [--work-dir ../../work/docs-aggregator]
"""

import argparse
import fnmatch
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def extract_repo_name(repo_url: str) -> str:
    """Extract repository name from a Git URL."""
    return repo_url.rstrip("/").rstrip(".git").split("/")[-1]


def is_valid_repo_url(repo_url: str) -> bool:
    """Basic validation of Git repository URLs."""
    patterns = [
        r"^https://github\.com/[^/]+/[^/]+",
        r"^https://gitlab\.com/[^/]+/[^/]+",
        r"^git@github\.com:[^/]+/[^/]+",
    ]
    return any(re.match(p, repo_url) for p in patterns)


def git_clone(repo_url: str, dest: Path, branch: Optional[str] = None) -> bool:
    """Clone a repository.  Returns True on success."""
    cmd = ["git", "clone", "--depth", "1"]
    if branch:
        cmd += ["--branch", branch]
    cmd += [repo_url, str(dest)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"  [ERR] git clone failed: {result.stderr.strip()}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  [ERR] git clone timed out for {repo_url}")
        return False


def git_pull(repo_dir: Path) -> bool:
    """Pull latest changes in an existing clone."""
    try:
        result = subprocess.run(
            ["git", "pull"], cwd=str(repo_dir),
            capture_output=True, text=True, timeout=300,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return False


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def should_exclude(rel_path: str, exclude_patterns: List[str]) -> bool:
    """Check whether *rel_path* matches any exclusion pattern."""
    for pattern in exclude_patterns:
        # Directory exclusion (pattern ends with /)
        if pattern.endswith("/"):
            dir_name = pattern.rstrip("/")
            if rel_path.startswith(dir_name + "/") or f"/{dir_name}/" in rel_path:
                return True
        # Glob match against the full relative path and the filename
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(Path(rel_path).name, pattern):
            return True
    return False


def find_docs(
    repo_dir: Path,
    content_paths: List[str],
    include_extensions: List[str],
    exclude_patterns: List[str],
) -> List[Path]:
    """Return documentation files under *content_paths* inside *repo_dir*."""
    found: List[Path] = []
    for cp in content_paths:
        search_root = repo_dir / cp
        if not search_root.exists():
            print(f"  [WARN] content_path not found: {cp}")
            continue
        for fpath in search_root.rglob("*"):
            if not fpath.is_file():
                continue
            if ".git" in fpath.parts:
                continue
            if fpath.suffix.lower() not in include_extensions:
                continue
            rel = str(fpath.relative_to(repo_dir))
            if should_exclude(rel, exclude_patterns):
                continue
            found.append(fpath)
    return found


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def process_source(source: Dict, repos_dir: Path, raw_dir: Path) -> Dict:
    """Clone (or update) one source and stage its docs.

    Returns a result dict with status information.
    """
    name = source["name"]
    repo_url = source["repo"]
    branch = source.get("branch")
    content_paths = source.get("content_paths", ["."])
    include_ext = source.get("include_extensions", [".md"])
    exclude_pat = source.get("exclude_patterns", [])

    result = {
        "name": name,
        "repo": repo_url,
        "success": False,
        "files_found": 0,
        "files_staged": 0,
        "error": None,
    }

    if not is_valid_repo_url(repo_url):
        result["error"] = f"Invalid repo URL: {repo_url}"
        return result

    clone_dest = repos_dir / extract_repo_name(repo_url)

    # Clone or update
    if clone_dest.exists() and (clone_dest / ".git").exists():
        print(f"  Updating {name} ...")
        if not git_pull(clone_dest):
            # Stale clone — remove and re‑clone
            shutil.rmtree(clone_dest, ignore_errors=True)
            if not git_clone(repo_url, clone_dest, branch):
                result["error"] = "Clone failed after stale pull"
                return result
    else:
        print(f"  Cloning {name} ({branch or 'default branch'}) ...")
        if not git_clone(repo_url, clone_dest, branch):
            result["error"] = "Clone failed"
            return result

    # Find documentation files
    docs = find_docs(clone_dest, content_paths, include_ext, exclude_pat)
    result["files_found"] = len(docs)

    if not docs:
        result["error"] = "No documentation files found"
        return result

    # Stage into raw_dir/<source_name>/
    dest_root = raw_dir / name
    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    staged = 0
    for fpath in docs:
        # Preserve directory structure relative to the first content_path match
        for cp in content_paths:
            search_root = clone_dest / cp
            if str(fpath).startswith(str(search_root)):
                rel = fpath.relative_to(search_root)
                break
        else:
            rel = fpath.relative_to(clone_dest)

        dest_file = dest_root / rel
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fpath, dest_file)
        staged += 1

    result["files_staged"] = staged
    result["success"] = staged > 0
    return result


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Aggregate external documentation")
    parser.add_argument(
        "--config", default=str(Path(__file__).parent / "docs_config.yml"),
        help="Path to docs_config.yml",
    )
    parser.add_argument(
        "--work-dir",
        default=str(Path(__file__).resolve().parents[1].parent / "work" / "docs-aggregator"),
        help="Working directory for clones and staging",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    sources = config.get("sources", [])
    if not sources:
        print("No sources defined in config.")
        sys.exit(0)

    work = Path(args.work_dir)
    repos_dir = work / "repos"
    raw_dir = work / "raw"
    repos_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Documentation Aggregator ===")
    print(f"Config : {config_path}")
    print(f"Work   : {work}")
    print(f"Sources: {len(sources)}\n")

    results = []
    for source in sources:
        print(f"[{source['name']}]")
        res = process_source(source, repos_dir, raw_dir)
        results.append(res)
        status = "OK" if res["success"] else f"FAIL ({res['error']})"
        print(f"  Status: {status}  |  Found: {res['files_found']}  |  Staged: {res['files_staged']}\n")

    # Summary
    ok = sum(1 for r in results if r["success"])
    total_files = sum(r["files_staged"] for r in results)
    print(f"=== Summary: {ok}/{len(results)} sources OK, {total_files} files staged ===")

    # Write manifest for downstream transform step
    manifest_path = work / "manifest.yml"
    manifest = {
        "sources": [
            {
                "name": s["name"],
                "category": s.get("category", "misc"),
                "description": s.get("description", ""),
                "tags": s.get("tags", []),
                "license": s.get("license", ""),
                "license_url": s.get("license_url", ""),
                "repo": s["repo"],
                "branch": s.get("branch", ""),
                "framework": s.get("framework", "plain"),
                "raw_dir": str(raw_dir / s["name"]),
            }
            for s, r in zip(sources, results)
            if r["success"]
        ]
    }
    with open(manifest_path, "w") as f:
        yaml.dump(manifest, f, default_flow_style=False)
    print(f"Manifest written to {manifest_path}")

    if ok < len(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
