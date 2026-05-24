#!/usr/bin/env python3
"""Generate ``_data/navigation/quests.yml`` from the quest collection.

Walks every quest file under ``pages/_quests/`` (skipping templates, docs,
inventory, and meta files), groups them by binary level, and emits a sidebar
navigation YAML compatible with the existing layouts.

Output structure mirrors the hand-maintained file the generator replaces:

```yaml
- title: Quest Hub
  icon: bi-map
  url: /quests/home/
  children:
    - title: Overworld Map
    - title: Quest Index
- title: "Level 0000 - Foundation & Init World"
  icon: <auto>
  url: /quests/0000/
  children:
    - title: Terminal Fundamentals
      url: /quests/0000/terminal-fundamentals/
    ...
- title: Resources
  children:
    - title: Codex
    - title: Inventory
    - title: Tools
```

Permalinks always carry a trailing slash so the menu matches Jekyll-generated
canonical URLs.

Usage::

    python3 scripts/quest/generate-quest-navigation.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:  # pragma: no cover
    print("Error: PyYAML required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parents[2]
QUESTS_DIR = REPO_ROOT / "pages" / "_quests"
NAV_PATH = REPO_ROOT / "_data" / "navigation" / "quests.yml"

LEVEL_RE = re.compile(r"^[01]{4}$")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)", re.DOTALL)

# Per-level metadata kept in sync with scripts/quest/quest_registry.py.
# Duplicated here to avoid an import-path quirk when this file is run via
# ``make`` from the repository root.
LEVEL_META = {
    "0000": ("Foundation & Init World", "bi-emoji-sunglasses"),
    "0001": ("Web Fundamentals", "bi-feather"),
    "0010": ("Terminal Mastery", "bi-terminal"),
    "0011": ("AI-Assisted Development", "bi-stars"),
    "0100": ("Frontend & Containers", "bi-box-seam"),
    "0101": ("CI/CD & DevOps", "bi-rocket-takeoff"),
    "0110": ("Database Mastery", "bi-database"),
    "0111": ("API Development", "bi-cloud-arrow-up"),
    "1000": ("Cloud Computing", "bi-cloud"),
    "1001": ("Kubernetes Orchestration", "bi-grid-3x3-gap"),
    "1010": ("Monitoring & Observability", "bi-graph-up"),
    "1011": ("Security & Compliance", "bi-shield-lock"),
    "1100": ("Data Engineering", "bi-diagram-3"),
    "1101": ("Machine Learning & AI", "bi-cpu"),
    "1110": ("Architecture & Design", "bi-building-gear"),
    "1111": ("Leadership & Innovation", "bi-trophy"),
}


def read_fm(md_path: Path):
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError:
        return None
    match = FM_RE.match(text)
    if not match:
        return None
    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def collect_quests():
    """Return mapping of level -> list of (title, url, quest_type)."""
    by_level: dict[str, list[tuple[str, str, str]]] = defaultdict(list)

    for md_file in sorted(QUESTS_DIR.rglob("*.md")):
        if md_file.name in {"README.md", "home.md", "QUEST_BUILD_PLAN.md", "NETWORK_REPORT.md"}:
            continue
        if any(part in {"templates", "docs", "inventory"} for part in md_file.parts):
            continue
        fm = read_fm(md_file)
        if fm is None:
            continue
        if fm.get("fmContentType") != "quest":
            continue
        permalink = fm.get("permalink")
        if not permalink:
            continue
        level = str(fm.get("level", ""))
        if not LEVEL_RE.match(level):
            continue
        title = fm.get("title") or md_file.stem
        url = str(permalink)
        if not url.endswith("/"):
            url += "/"
        quest_type = fm.get("quest_type") or "main_quest"
        by_level[level].append((title, url, quest_type))

    for level, items in by_level.items():
        # Main quests first, alphabetical within each group.
        items.sort(key=lambda t: (0 if t[2] == "main_quest" else 1, t[0].lower()))

    return by_level


def build_nav(by_level):
    nav = [
        {
            "title": "Quest Hub",
            "icon": "bi-map",
            "url": "/quests/home/",
            "children": [
                {"title": "Overworld Map", "url": "/quests/home/"},
                {"title": "Quest Index", "url": "/quests/"},
            ],
        }
    ]

    for level in sorted(LEVEL_META):
        theme, icon = LEVEL_META[level]
        quests = by_level.get(level, [])
        children = []
        for title, url, quest_type in quests:
            prefix = "⚔️ " if quest_type == "side_quest" else ""
            children.append({"title": f"{prefix}{title}", "url": url})
        nav.append(
            {
                "title": f"Level {level} - {theme}",
                "icon": icon,
                "url": f"/quests/{level}/",
                "children": children if children else None,
            }
        )

    nav.append(
        {
            "title": "Resources",
            "icon": "bi-book",
            "children": [
                {"title": "Codex", "url": "/quests/codex/"},
                {"title": "Inventory", "url": "/quests/inventory/"},
                {"title": "Tools", "url": "/quests/tools/"},
            ],
        }
    )

    # Drop None children so the YAML reads cleanly when a level has no quests.
    for entry in nav:
        if entry.get("children") is None:
            entry.pop("children", None)
    return nav


HEADER = (
    "# Auto-generated by scripts/quest/generate-quest-navigation.py — do not edit by hand.\n"
    "# Run `make quest-nav` or rerun the script to refresh.\n"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="print without writing")
    args = parser.parse_args()

    if not QUESTS_DIR.exists():
        print(f"Quests dir not found: {QUESTS_DIR}", file=sys.stderr)
        return 1

    by_level = collect_quests()
    nav = build_nav(by_level)
    body = HEADER + yaml.dump(nav, default_flow_style=False, allow_unicode=True, sort_keys=False)

    if args.dry_run:
        print(body)
        return 0

    NAV_PATH.parent.mkdir(parents=True, exist_ok=True)
    NAV_PATH.write_text(body, encoding="utf-8")
    total = sum(len(items) for items in by_level.values())
    print(f"Wrote {NAV_PATH.relative_to(REPO_ROOT)} ({total} quests across {len(by_level)} levels)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
