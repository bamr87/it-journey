#!/usr/bin/env python3
"""Normalize frontmatter of every level README under ``pages/_quests``.

For each ``pages/_quests/<binary>/README.md`` where ``<binary>`` matches
``^[01]{4}$``:

- Ensure ``layout: quest-collection`` (the dynamic level hub layout).
- Force ``level`` to the quoted 4-digit binary form (`'0001'`) — historic
  READMEs persisted decimal values like ``1`` or ``64`` that broke
  ``{% assign filtered = site.quests | where: "level", page.level %}`` in
  ``_layouts/quest-collection.html``.
- Ensure ``categories: quests`` is present (kept as the simple scalar form
  used elsewhere in the repo).

Other frontmatter and the body are preserved untouched.

Usage::

    python3 scripts/development/update_level_readmes.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - dependency hint only
    print("Error: PyYAML required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parents[2]
QUESTS_DIR = REPO_ROOT / "pages" / "_quests"
LEVEL_DIR_RE = re.compile(r"^[01]{4}$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)", re.DOTALL)


def normalize_readme(path: Path, level: str, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        print(f"  skip (no frontmatter): {path}")
        return False

    try:
        fm = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        print(f"  skip (YAML error in {path}): {exc}")
        return False

    body = match.group(2)
    original = dict(fm)

    fm["layout"] = "quest-collection"
    fm["level"] = level
    if "categories" not in fm:
        fm["categories"] = "quests"

    if fm == original:
        print(f"  ok    {path.relative_to(REPO_ROOT)}")
        return False

    if dry_run:
        print(f"  would update {path.relative_to(REPO_ROOT)} → layout/level/categories")
        return True

    # Preserve insertion order: emit known keys first, then the rest.
    ordered = {}
    for key in ("title", "description", "preview", "permalink", "layout", "level", "categories"):
        if key in fm:
            ordered[key] = fm[key]
    for key, value in fm.items():
        ordered.setdefault(key, value)

    fm_text = yaml.dump(
        ordered, default_flow_style=False, allow_unicode=True, sort_keys=False
    ).rstrip("\n")
    path.write_text(f"---\n{fm_text}\n---\n{body}", encoding="utf-8")
    print(f"  updated {path.relative_to(REPO_ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    args = parser.parse_args()

    if not QUESTS_DIR.exists():
        print(f"Quests directory not found: {QUESTS_DIR}", file=sys.stderr)
        return 1

    changed = 0
    for entry in sorted(QUESTS_DIR.iterdir()):
        if not entry.is_dir() or not LEVEL_DIR_RE.match(entry.name):
            continue
        readme = entry / "README.md"
        if not readme.exists():
            print(f"  skip (no README): {entry}")
            continue
        if normalize_readme(readme, entry.name, args.dry_run):
            changed += 1

    print(f"\n{'Would update' if args.dry_run else 'Updated'} {changed} level README(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
