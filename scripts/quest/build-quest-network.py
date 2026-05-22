#!/usr/bin/env python3
"""
build-quest-network.py

Scans all quest files under pages/_quests/ and generates a quest dependency
network in two formats:
  - assets/data/quest-network.json  (served as static asset for JS graph views)
  - _data/quests/network.yml        (consumed by Jekyll Liquid templates)

Usage:
  python3 scripts/quest/build-quest-network.py [--quest-dir DIR] [--json PATH] [--yaml PATH]

Output JSON shape:
  {
    "generated": "<ISO timestamp>",
    "stats": { "total": N, "by_level": {...}, "by_type": {...} },
    "nodes": [{ "id", "title", "level", "type", "difficulty", "technology", "file" }, ...],
    "edges": [{ "source", "target", "kind" }, ...]
  }
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required.  pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ── constants ────────────────────────────────────────────────────────────────
QUEST_DIR_DEFAULT = "pages/_quests"
JSON_OUT_DEFAULT  = "assets/data/quest-network.json"
YAML_OUT_DEFAULT  = "_data/quests/network.yml"

# Skip these stems regardless of directory
SKIP_STEMS = {"home", "README", "QUEST_BUILD_PLAN", "NETWORK_REPORT"}
# Skip these subdirs entirely
SKIP_SUBDIRS = {"templates", "docs", "inventory", "tools"}
# Level directory pattern: 4-digit binary string
LEVEL_RE = re.compile(r"^[01]{4}$")

EDGE_KINDS = [
    ("required_quests",    "required"),
    ("recommended_quests", "recommended"),
    ("unlocks_quests",     "unlocks"),
]


# ── helpers ──────────────────────────────────────────────────────────────────

def _extract_frontmatter(path: Path):
    """Return (dict, body_str) from a markdown file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, text[m.end():]


def _iter_quest_files(quest_dir: Path):
    """Yield (Path, level_or_None) for every quest .md file to process."""
    for entry in sorted(quest_dir.iterdir()):
        if not entry.is_dir():
            # Top-level .md files (codex level, etc.)
            if entry.suffix == ".md" and entry.stem not in SKIP_STEMS:
                yield entry, None
            continue

        if entry.name in SKIP_SUBDIRS:
            continue

        level = entry.name if LEVEL_RE.match(entry.name) else None

        for md in sorted(entry.rglob("*.md")):
            if md.stem in SKIP_STEMS:
                continue
            # Skip files in excluded subdirs
            relative = md.relative_to(entry)
            if any(p in SKIP_SUBDIRS for p in relative.parts[:-1]):
                continue
            yield md, level


# ── core ─────────────────────────────────────────────────────────────────────

def build_network(quest_dir: Path):
    nodes = []
    edges = []
    by_level = {}
    by_type  = {}

    for md_path, level in _iter_quest_files(quest_dir):
        fm, _ = _extract_frontmatter(md_path)
        permalink = fm.get("permalink", "")
        if not permalink:
            continue

        quest_type = fm.get("quest_type", "")
        node_level = str(fm.get("level", level or ""))
        title      = str(fm.get("title", md_path.stem))
        difficulty = str(fm.get("difficulty", ""))
        technology = str(fm.get("primary_technology", ""))

        # Normalise trailing slash
        node_id = permalink if permalink.endswith("/") else permalink + "/"

        nodes.append({
            "id":         node_id,
            "title":      title,
            "level":      node_level,
            "type":       quest_type,
            "difficulty": difficulty,
            "technology": technology,
            "file":       str(md_path),
        })

        # Stats
        by_level[node_level] = by_level.get(node_level, 0) + 1
        by_type[quest_type]  = by_type.get(quest_type,  0) + 1

        # Edges from quest_dependencies
        deps = fm.get("quest_dependencies") or {}
        if isinstance(deps, dict):
            for fm_key, edge_kind in EDGE_KINDS:
                targets = deps.get(fm_key) or []
                if isinstance(targets, str):
                    targets = [targets]
                for tgt in targets:
                    if not tgt:
                        continue
                    tgt = tgt if tgt.endswith("/") else tgt + "/"
                    edges.append({
                        "source": node_id,
                        "target": tgt,
                        "kind":   edge_kind,
                    })

    network = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "total":    len(nodes),
            "by_level": dict(sorted(by_level.items())),
            "by_type":  dict(sorted(by_type.items())),
        },
        "nodes": nodes,
        "edges": edges,
    }
    return network


# ── I/O ──────────────────────────────────────────────────────────────────────

def write_json(network, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(network, f, ensure_ascii=False, indent=2)
    print(f"[JSON] {len(network['nodes'])} nodes, {len(network['edges'])} edges → {path}")


def write_yaml(network, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    # For Jekyll _data/: write a trimmed version (title + level + type + edges)
    # Omit large string fields to keep the file manageable.
    slim_nodes = [
        {"id": n["id"], "title": n["title"], "level": n["level"],
         "type": n["type"], "difficulty": n["difficulty"]}
        for n in network["nodes"]
    ]
    slim = {
        "generated": network["generated"],
        "stats":     network["stats"],
        "nodes":     slim_nodes,
        "edges":     network["edges"],
    }
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(slim, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    print(f"[YAML] {len(slim_nodes)} nodes → {path}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build quest dependency network data files.")
    parser.add_argument("--quest-dir", default=QUEST_DIR_DEFAULT,
                        help=f"Path to quest collection (default: {QUEST_DIR_DEFAULT})")
    parser.add_argument("--json", default=JSON_OUT_DEFAULT,
                        help=f"Output JSON path (default: {JSON_OUT_DEFAULT})")
    parser.add_argument("--yaml", default=YAML_OUT_DEFAULT,
                        help=f"Output YAML path (default: {YAML_OUT_DEFAULT})")
    parser.add_argument("--no-yaml", action="store_true",
                        help="Skip YAML output")
    args = parser.parse_args()

    quest_dir = Path(args.quest_dir)
    if not quest_dir.is_dir():
        print(f"Error: quest dir not found: {quest_dir}", file=sys.stderr)
        sys.exit(1)

    network = build_network(quest_dir)
    write_json(network, Path(args.json))
    if not args.no_yaml:
        write_yaml(network, Path(args.yaml))

    print(f"\nSummary:")
    print(f"  Nodes : {network['stats']['total']}")
    print(f"  Edges : {len(network['edges'])}")
    print(f"  Levels: {', '.join(sorted(network['stats']['by_level']))}")


if __name__ == "__main__":
    main()
