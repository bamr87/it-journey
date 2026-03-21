#!/usr/bin/env python3
"""
Update 'date' frontmatter in Markdown files using git history.

Scans all .md files in the repository and adds or updates the 'date'
frontmatter field to reflect the file's original creation date as
determined by git (the author date of the first commit that introduced
the file).

Usage:
    python update-date-frontmatter.py [--dry-run] [--root PATH] [--verbose]

Requirements:
    - git (in PATH)
    - pyyaml: pip install pyyaml
"""

import argparse
import logging
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install it with: pip install pyyaml")
    sys.exit(1)

# Directories to skip (relative to repo root)
SKIP_DIRS = {"_site", "node_modules", "work", ".git", "vendor", ".bundle"}

logger = logging.getLogger(__name__)


def get_repo_root(hint: str | None = None) -> Path:
    """Return the git repository root directory."""
    cwd = hint or os.getcwd()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, cwd=cwd,
    )
    if result.returncode != 0:
        logger.error("Not inside a git repository.")
        sys.exit(1)
    return Path(result.stdout.strip())


def git_creation_date(repo_root: Path, filepath: Path) -> str | None:
    """Return the ISO-8601 author date of the first commit that added *filepath*."""
    rel = filepath.relative_to(repo_root)
    result = subprocess.run(
        ["git", "log", "--follow", "--diff-filter=A", "--format=%aI", "--", str(rel)],
        capture_output=True, text=True, cwd=repo_root,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    # The last line is the earliest (first) commit
    lines = result.stdout.strip().splitlines()
    return lines[-1] if lines else None


def parse_frontmatter(text: str):
    """Return (frontmatter_dict, start_idx, end_idx) or (None, None, None)."""
    if not text.startswith("---"):
        return None, None, None
    # Find closing ---
    match = re.search(r"\n---\s*\n", text[3:])
    if match is None:
        # Try end-of-file case
        match = re.search(r"\n---\s*$", text[3:])
        if match is None:
            return None, None, None
    end = 3 + match.end()
    fm_text = text[3:3 + match.start()]
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        return None, None, None
    if not isinstance(fm, dict):
        return None, None, None
    return fm, 3, 3 + match.start()


def format_date(iso_str: str) -> str:
    """Normalise a git ISO date to YYYY-MM-DDTHH:MM:SS.000Z (UTC-style)."""
    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def update_file(filepath: Path, creation_date: str, dry_run: bool) -> str:
    """
    Add or update the 'date' field in the file's frontmatter.

    Returns a status string: 'added', 'updated', 'unchanged', or 'skipped'.
    """
    text = filepath.read_text(encoding="utf-8")
    fm, fm_start, fm_end = parse_frontmatter(text)
    if fm is None:
        return "skipped"

    formatted_date = format_date(creation_date)

    # Check if date already matches
    existing = fm.get("date")
    if existing is not None:
        # Normalise existing value for comparison
        try:
            if isinstance(existing, datetime):
                existing_str = existing.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            else:
                existing_str = format_date(str(existing))
            if existing_str == formatted_date:
                return "unchanged"
        except (ValueError, TypeError):
            pass  # Can't parse — will overwrite

    fm_text = text[fm_start:fm_end]

    # Regex to match an existing date line in frontmatter
    date_pattern = re.compile(r"^date:.*$", re.MULTILINE)
    new_date_line = f"date: {formatted_date}"

    if date_pattern.search(fm_text):
        new_fm_text = date_pattern.sub(new_date_line, fm_text, count=1)
        status = "updated"
    else:
        # Insert date after the first line (usually after title or description)
        new_fm_text = fm_text.rstrip("\n") + "\n" + new_date_line + "\n"
        status = "added"

    new_text = text[:fm_start] + new_fm_text + text[fm_end:]

    if not dry_run:
        filepath.write_text(new_text, encoding="utf-8")

    return status


def collect_md_files(repo_root: Path) -> list[Path]:
    """Collect all .md files, skipping excluded directories."""
    files = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        # Prune skipped directories in-place
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.lower().endswith(".md"):
                files.append(Path(dirpath) / fname)
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description="Add/update 'date' frontmatter in .md files using git creation date."
    )
    parser.add_argument(
        "--root", type=str, default=None,
        help="Repository root directory (auto-detected if omitted)."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without modifying files."
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Show details for every file processed."
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    repo_root = get_repo_root(args.root)
    logger.info("Repository root: %s", repo_root)

    md_files = collect_md_files(repo_root)
    logger.info("Found %d .md files to process.", len(md_files))

    counts = {"added": 0, "updated": 0, "unchanged": 0, "skipped": 0, "no_git_date": 0}

    for filepath in md_files:
        creation_date = git_creation_date(repo_root, filepath)
        if creation_date is None:
            logger.debug("No git history for %s — skipping.", filepath.relative_to(repo_root))
            counts["no_git_date"] += 1
            continue

        status = update_file(filepath, creation_date, dry_run=args.dry_run)
        counts[status] += 1

        if args.verbose or status in ("added", "updated"):
            prefix = "[DRY RUN] " if args.dry_run else ""
            logger.info(
                "%s%s — %s (date: %s)",
                prefix,
                filepath.relative_to(repo_root),
                status,
                format_date(creation_date),
            )

    logger.info("--- Summary ---")
    logger.info("  Added:       %d", counts["added"])
    logger.info("  Updated:     %d", counts["updated"])
    logger.info("  Unchanged:   %d", counts["unchanged"])
    logger.info("  Skipped (no frontmatter): %d", counts["skipped"])
    logger.info("  Skipped (no git date):    %d", counts["no_git_date"])
    if args.dry_run:
        logger.info("  (dry run — no files were modified)")


if __name__ == "__main__":
    main()
