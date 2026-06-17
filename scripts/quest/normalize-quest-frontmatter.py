#!/usr/bin/env python3
"""
normalize-quest-frontmatter.py — the ONE idempotent, registry-driven frontmatter
normalizer for the quest collection. Replaces the deleted one-off fixers.

It uses round-trip YAML (ruamel.yaml) so it only changes what it touches —
comments, key order, and quoting of untouched fields are preserved.

Transforms (all idempotent):
  1. Migrate ``quest_relationships`` INTO the canonical ``quest_dependencies``
     block, then drop it:
         parent_quest(s)            -> required_quests
         child_quests / sequel_quests / unlocks -> unlocks_quests
         parallel_quests / related  -> recommended_quests
     and fix typo sub-keys in quest_dependencies (required -> required_quests,
     recommended -> recommended_quests). Lists are unioned + de-duped.
  2. Rename ``sub-title`` -> ``sub_title`` (when sub_title is absent).
  3. ``skill_focus``: data-science -> data-engineering.
  4. ``draft``: normalize to a real boolean (string 'draft'/'true'/'false').
  5. Drop retired fields (registry.RETIRED_FIELDS) once migrated:
     quest_relationships, quest_mapping, learning_paths, related_quests,
     snippet, sub-title.

Usage:
  python3 scripts/quest/normalize-quest-frontmatter.py [PATH] [--apply]
  (default PATH = pages/_quests; without --apply it is a dry run)
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from ruamel.yaml import YAML

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import quest_registry as reg  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parent.parent

# quest_relationships sub-key -> quest_dependencies sub-key
REL_MAP = {
    "parent_quest": "required_quests",
    "parent_quests": "required_quests",
    "child_quests": "unlocks_quests",
    "sequel_quests": "unlocks_quests",
    "unlocks": "unlocks_quests",
    "parallel_quests": "recommended_quests",
    "related": "recommended_quests",
}
# quest_dependencies typo sub-keys -> canonical
DEP_TYPO_MAP = {"required": "required_quests", "recommended": "recommended_quests"}

yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096  # don't wrap long lines


def _aslist(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [v] if v.strip() else []
    if isinstance(v, list):
        return [x for x in v if x not in (None, "")]
    return []


def split_frontmatter(text: str):
    if not text.startswith("---"):
        return None, None, None
    end = text.find("\n---", 3)
    if end == -1:
        return None, None, None
    fm_text = text[text.find("\n", 0) + 1:end].rstrip("\n")
    after = text[end + 4:]
    return text[:text.find("\n") + 1], fm_text, after


def normalize_fm(fm) -> bool:
    """Mutate the ruamel mapping in place. Return True if anything changed."""
    changed = False

    # 1. Migrate quest_relationships -> quest_dependencies
    rel = fm.get("quest_relationships")
    if isinstance(rel, dict):
        dep = fm.get("quest_dependencies")
        if not isinstance(dep, dict):
            from ruamel.yaml.comments import CommentedMap
            dep = CommentedMap()
        # fold typo sub-keys already inside quest_dependencies
        for typo, canon in DEP_TYPO_MAP.items():
            if typo in dep:
                merged = _aslist(dep.get(canon)) + _aslist(dep.get(typo))
                dep[canon] = _dedupe(merged)
                del dep[typo]
                changed = True
        # fold quest_relationships sub-keys in
        for rk, target in REL_MAP.items():
            if rk in rel:
                merged = _aslist(dep.get(target)) + _aslist(rel.get(rk))
                cleaned = _dedupe(merged)
                if cleaned:
                    dep[target] = cleaned
        # ensure the three canonical keys exist (empty list if absent)
        for k in reg.QUEST_DEPENDENCIES_KEYS:
            if k not in dep:
                dep[k] = []
        fm["quest_dependencies"] = dep
        changed = True

    # quest_dependencies may only contain permalinks (start with '/'); drop
    # prose entries like "GitHub account" / "Level 001: HTML Basics" that break
    # the dependency graph (they belong in prerequisites.knowledge_requirements).
    dep = fm.get("quest_dependencies")
    if isinstance(dep, dict):
        for k in reg.QUEST_DEPENDENCIES_KEYS:
            vals = dep.get(k)
            if isinstance(vals, list):
                kept = [x for x in vals if isinstance(x, str) and x.startswith("/quests/")]
                if len(kept) != len(vals):
                    dep[k] = kept
                    changed = True

    # 2. sub-title -> sub_title
    if "sub-title" in fm:
        if not fm.get("sub_title"):
            fm["sub_title"] = fm["sub-title"]
        changed = True  # removal handled in step 5

    # 3. skill_focus value fix
    if fm.get("skill_focus") == "data-science":
        fm["skill_focus"] = "data-engineering"
        changed = True

    # 4. draft -> bool
    if "draft" in fm and not isinstance(fm["draft"], bool):
        val = str(fm["draft"]).strip().lower()
        fm["draft"] = val in ("true", "draft", "yes")
        changed = True

    # 5. drop retired fields
    for rf in reg.RETIRED_FIELDS:
        if rf in fm:
            del fm[rf]
            changed = True

    return changed


def _dedupe(seq):
    seen = set(); out = []
    for x in seq:
        if x not in seen:
            seen.add(x); out.append(x)
    return out


def process(path: Path, apply: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    head, fm_text, after = split_frontmatter(text)
    if fm_text is None:
        return False
    try:
        fm = yaml.load(fm_text)
    except Exception as e:  # noqa: BLE001
        print(f"  ! skip (unparseable frontmatter): {path}  ({e})")
        return False
    if not hasattr(fm, "get"):
        return False
    if not normalize_fm(fm):
        return False
    buf = io.StringIO()
    yaml.dump(fm, buf)
    new_text = head + buf.getvalue().rstrip("\n") + "\n---" + after
    if apply:
        path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", default="pages/_quests")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    args = ap.parse_args()

    root = Path(args.path)
    if not root.is_absolute():
        root = REPO_ROOT / root
    files = sorted(root.rglob("*.md")) if root.is_dir() else [root]

    changed = 0
    for f in files:
        if f.stem in reg.SKIP_STEMS:
            continue
        if any(p in reg.SKIP_SUBDIRS for p in f.parts):
            continue
        if process(f, args.apply):
            changed += 1
            print(f"  {'fixed' if args.apply else 'would fix'}: {f.relative_to(REPO_ROOT)}")

    verb = "Normalized" if args.apply else "Would normalize"
    print(f"\n{verb} {changed} file(s).{'' if args.apply else '  Re-run with --apply to write.'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
