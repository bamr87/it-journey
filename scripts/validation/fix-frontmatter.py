#!/usr/bin/env python3
"""
fix-frontmatter.py — auto-fill missing required frontmatter fields in posts.

Targets the three error types found in the post-cleanup baseline:

- Missing/empty ``description``  — generates from first prose paragraph.
- Missing ``date``               — extracts from the filename ``YYYY-MM-DD-*.md``.
- Missing ``categories``         — derives from the parent folder
                                    (kebab-case → Title Case).

Idempotent: skips fields that already have non-empty values. Always preserves
existing frontmatter ordering and trailing body content. Use ``--dry-run`` to
preview changes without writing.

Usage:
    python3 fix-frontmatter.py pages/_posts [--dry-run] [--verbose]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

FM_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)
FILENAME_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
DESC_MAX = 155


def folder_to_category(folder: str) -> str:
    """Convert kebab-case folder to Title Case category name."""
    # Special-case '&' restoration where original had it
    overrides = {
        "ai-machine-learning": "AI & Machine Learning",
        "creative-experimental": "Creative & Experimental",
        "culture-society": "Culture & Society",
        "data-analytics": "Data & Analytics",
        "system-administration": "System Administration",
        "tools-environment": "Tools & Environment",
        "trends-ideas": "Trends & Ideas",
        "web-development": "Web Development",
    }
    return overrides.get(folder, folder.replace("-", " ").title())


def first_prose_paragraph(body: str) -> Optional[str]:
    """Pull the first prose paragraph from a markdown body for use as description.

    Skips headings, code fences, blockquotes, lists, HTML, and front matter
    artifacts. Strips inline markdown (links, emphasis) before returning.
    """
    in_code = False
    paragraph: list[str] = []
    for raw in body.splitlines():
        line = raw.rstrip()
        if line.startswith("```") or line.startswith("~~~"):
            in_code = not in_code
            if paragraph:
                break
            continue
        if in_code:
            continue
        stripped = line.lstrip()
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith(("#", ">", "|", "<", "{", "}", "[", "]", '"')):
            continue
        # True list/bullet markers require a following space
        if re.match(r"^[-*+]\s", stripped):
            continue
        if re.match(r"^\d+\.\s", stripped):
            continue
        paragraph.append(stripped)
    if not paragraph:
        return None
    text = " ".join(paragraph)
    # Strip markdown links: [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Strip emphasis markers
    text = re.sub(r"[*_`]+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > DESC_MAX:
        cut = text[: DESC_MAX - 1].rsplit(" ", 1)[0]
        text = cut.rstrip(".,;:") + "…"
    return text or None


def fix_file(path: Path, posts_root: Path, dry_run: bool, verbose: bool) -> dict:
    """Apply available fixes; return per-file change record."""
    text = path.read_text(encoding="utf-8")
    match = FM_RE.match(text)
    if not match:
        return {"path": str(path), "skipped": "no-frontmatter"}

    fm_text, body = match.group(1), match.group(2)
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as exc:
        return {"path": str(path), "skipped": f"yaml-error: {exc}"}
    if not isinstance(fm, dict):
        return {"path": str(path), "skipped": "frontmatter-not-mapping"}

    changes: list[str] = []

    # 1. date
    if not fm.get("date"):
        m = FILENAME_DATE_RE.match(path.name)
        if m:
            fm["date"] = f"{m.group(1)}T00:00:00.000Z"
            changes.append(f"date={fm['date']}")

    # 2. categories — derive from parent folder
    cats = fm.get("categories")
    if not cats:
        try:
            rel = path.relative_to(posts_root)
            parts = rel.parts
            if len(parts) >= 2:
                category = folder_to_category(parts[0])
                fm["categories"] = [category]
                changes.append(f"categories=[{category}]")
        except ValueError:
            pass

    # 3. description
    desc = fm.get("description")
    if not desc or (isinstance(desc, str) and not desc.strip()):
        generated = first_prose_paragraph(body)
        if generated:
            fm["description"] = generated
            changes.append(f"description={generated[:60]}…")

    if not changes:
        return {"path": str(path), "skipped": "no-fix-needed"}

    if dry_run:
        if verbose:
            print(f"[dry] {path}: {', '.join(changes)}")
        return {"path": str(path), "would_fix": changes}

    new_fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000).rstrip("\n")
    new_text = f"---\n{new_fm_text}\n---\n{body}"
    path.write_text(new_text, encoding="utf-8")
    if verbose:
        print(f"[fix] {path}: {', '.join(changes)}")
    return {"path": str(path), "fixed": changes}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", type=Path, help="Posts directory (e.g. pages/_posts)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--report", type=Path, help="Write JSON report to this path")
    args = ap.parse_args()

    if not args.root.is_dir():
        print(f"ERROR: not a directory: {args.root}", file=sys.stderr)
        return 2

    files = sorted(args.root.rglob("*.md"))
    records = [fix_file(f, args.root, args.dry_run, args.verbose) for f in files]

    fixed = [r for r in records if "fixed" in r or "would_fix" in r]
    skipped = [r for r in records if "skipped" in r]

    print(f"\nProcessed {len(files)} files")
    print(f"  Changed: {len(fixed)}")
    print(f"  Skipped: {len(skipped)}")
    if args.report:
        args.report.write_text(json.dumps(records, indent=2), encoding="utf-8")
        print(f"  Report : {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
