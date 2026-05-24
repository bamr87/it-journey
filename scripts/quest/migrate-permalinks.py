#!/usr/bin/env python3
"""
migrate-permalinks.py

Migrates quest permalinks to the canonical level-prefixed hierarchy:

  main_quest   : /quests/XXXX/slug/
  side_quest   : /quests/XXXX/side-quests/slug/
  Level README : /quests/XXXX/
  codex        : /quests/codex/slug/

Old patterns recognised and rewritten:
  /quests/level-XXXX/             → /quests/XXXX/
  /quests/level-XXXX-slug/        → /quests/XXXX/slug/   (main_quest)
                                    /quests/XXXX/side-quests/slug/ (side_quest)
  /quests/side-quest-slug/        → /quests/XXXX/side-quests/slug/
  /quests/level-codex/slug/       → /quests/codex/slug/
  /quests/side-quests/slug/       → /quests/XXXX/side-quests/slug/  (legacy flat)

Old URLs are preserved in redirect_from:.
A two-pass strategy is used so that dependency URLs whose old form was
/quests/side-quest-slug/ can be mapped to the correct level-prefixed new URL.

Usage:
  python3 scripts/quest/migrate-permalinks.py [--dry-run] [--verbose]
  python3 scripts/quest/migrate-permalinks.py --directory pages/_quests
"""

import re
import sys
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML required.  Install with: pip install pyyaml")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

LEVEL_RE = re.compile(r"^[01]{4}$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)", re.DOTALL)

SKIP_STEMS = {"home", "README", "QUEST_BUILD_PLAN"}
SKIP_SUBDIRS = {"templates", "docs", "inventory"}


# ──────────────────────────────────────────────────────────────────────────────
# YAML helpers
# ──────────────────────────────────────────────────────────────────────────────

def read_fm(md_path: Path):
    """Return (frontmatter_dict, body_str) or (None, None)."""
    text = md_path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, None
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None, None
    if not isinstance(fm, dict):
        return None, None
    return fm, m.group(2)


def write_fm(md_path: Path, fm: dict, body: str):
    fm_text = yaml.dump(
        fm, default_flow_style=False, allow_unicode=True, sort_keys=False
    ).rstrip("\n")
    md_path.write_text(f"---\n{fm_text}\n---\n{body}", encoding="utf-8")


# ──────────────────────────────────────────────────────────────────────────────
# Permalink computation
# ──────────────────────────────────────────────────────────────────────────────

def _clean_side_slug(permalink: str, file_stem: str) -> str:
    """Return the bare slug for a side quest (without the 'side-quest-' prefix)."""
    p = str(permalink).rstrip("/")
    # Already has side-quest- prefix in URL
    m = re.match(r"^/quests/side-quest-(.+)$", p)
    if m:
        return m.group(1)
    m = re.match(r"^/quests/level-[01]{4}-(.+)$", p)
    if m:
        return m.group(1)
    # Fall back to file stem
    stem = file_stem
    if stem.startswith("side-quest-"):
        stem = stem[len("side-quest-"):]
    return stem


def compute_new_permalink(
    current: str,
    level_dir: str | None,
    file_path: Path,
    quest_type: str | None,
) -> str | None:
    """
    Return the canonical new permalink, or None if already correct / unknown.

    Canonical rules
    ───────────────
    main_quest / untyped   /quests/XXXX/slug/
    side_quest             /quests/XXXX/side-quests/slug/
    Level README           /quests/XXXX/
    codex / bonus_quest    /quests/codex/slug/
    """
    if not current:
        return None

    p = str(current).rstrip("/")

    # ── gh-600 namespace  /quests/gh-600/slug
    # Used by the agentic quest series; resolves to the canonical level/slug
    # form using the file's parent directory as the level.
    m = re.match(r"^/quests/gh-600/(.+)$", p)
    if m and level_dir and LEVEL_RE.match(level_dir):
        slug = m.group(1)
        if quest_type == "side_quest":
            return f"/quests/{level_dir}/side-quests/{slug}/"
        return f"/quests/{level_dir}/{slug}/"

    # ── Level README  /quests/level-XXXX
    m = re.match(r"^/quests/level-([01]{4})$", p)
    if m:
        return f"/quests/{m.group(1)}/"

    # ── Codex  /quests/level-codex/slug
    m = re.match(r"^/quests/level-codex/(.+)$", p)
    if m:
        return f"/quests/codex/{m.group(1)}/"

    # ── Old flat side-quest  /quests/side-quest-slug
    m = re.match(r"^/quests/side-quest-(.+)$", p)
    if m and level_dir and LEVEL_RE.match(level_dir):
        return f"/quests/{level_dir}/side-quests/{m.group(1)}/"

    # ── Legacy flat side-quests (from previous migration run)  /quests/side-quests/slug
    m = re.match(r"^/quests/side-quests/(.+)$", p)
    if m and level_dir and LEVEL_RE.match(level_dir):
        return f"/quests/{level_dir}/side-quests/{m.group(1)}/"

    # ── Main-style  /quests/level-XXXX-slug
    m = re.match(r"^/quests/level-([01]{4})-(.+)$", p)
    if m:
        lvl, slug = m.group(1), m.group(2)
        if quest_type == "side_quest":
            clean = _clean_side_slug(current, file_path.stem)
            return f"/quests/{lvl}/side-quests/{clean}/"
        return f"/quests/{lvl}/{slug}/"

    # ── File typed side_quest with unrecognised permalink
    if quest_type == "side_quest" and level_dir and LEVEL_RE.match(level_dir):
        slug = _clean_side_slug(current, file_path.stem)
        return f"/quests/{level_dir}/side-quests/{slug}/"

    return None  # already canonical or unhandled


# ──────────────────────────────────────────────────────────────────────────────
# Pass 1 — build old-URL → new-URL lookup table
# ──────────────────────────────────────────────────────────────────────────────

def build_url_map(quest_dir: Path) -> dict[str, str]:
    """
    First pass: scan every quest file, compute old→new permalink pairs.
    Returns a dict keyed by old URL (with trailing slash) → new URL.
    """
    url_map: dict[str, str] = {}

    for md_file in sorted(quest_dir.rglob("*.md")):
        if any(p in md_file.parts for p in SKIP_SUBDIRS):
            continue
        if md_file.parent == quest_dir and md_file.stem in SKIP_STEMS:
            continue

        fm, _ = read_fm(md_file)
        if fm is None:
            continue

        parent = md_file.parent.name
        level_dir = parent if LEVEL_RE.match(parent) else None
        current = fm.get("permalink")
        if not current:
            continue

        new_pl = compute_new_permalink(
            str(current), level_dir, md_file, fm.get("quest_type")
        )
        if new_pl and new_pl != str(current):
            old_norm = str(current).rstrip("/") + "/"
            url_map[old_norm] = new_pl
            # Also index without trailing slash
            url_map[str(current).rstrip("/")] = new_pl

    return url_map


# ──────────────────────────────────────────────────────────────────────────────
# Dependency-URL rewriting (uses url_map from Pass 1)
# ──────────────────────────────────────────────────────────────────────────────

def _remap(url: str, url_map: dict[str, str]) -> str | None:
    k_slash = url.rstrip("/") + "/"
    k_plain = url.rstrip("/")
    # Also try generic level/slug patterns not in map (no level context)
    mapped = url_map.get(k_slash) or url_map.get(k_plain)
    if mapped:
        return mapped
    # Fallback: transform without level context (level-XXXX-slug, README, codex)
    p = url.rstrip("/")
    m = re.match(r"^/quests/level-([01]{4})$", p)
    if m:
        return f"/quests/{m.group(1)}/"
    m = re.match(r"^/quests/level-codex/(.+)$", p)
    if m:
        return f"/quests/codex/{m.group(1)}/"
    m = re.match(r"^/quests/level-([01]{4})-(.+)$", p)
    if m:
        return f"/quests/{m.group(1)}/{m.group(2)}/"
    # gh-600 dependency URLs without level context fall through; the
    # owning file's level is needed to rewrite them, so they are picked up
    # via the url_map populated in pass 1.
    return None


def _update_dep_list(dep_list: list, url_map: dict) -> tuple[list, list]:
    if not isinstance(dep_list, list):
        return dep_list, []
    new_list, changed = [], []
    for item in dep_list:
        if isinstance(item, str):
            raw = item.split("#")[0].strip()
            comment = (" #" + item.split("#", 1)[1]) if "#" in item else ""
            mapped = _remap(raw, url_map)
            if mapped and mapped != raw:
                changed.append((raw, mapped))
                new_list.append(mapped + comment)
            else:
                new_list.append(item)
        else:
            new_list.append(item)
    return new_list, changed


def _update_dep_block(block, url_map: dict) -> tuple[object, list]:
    if not isinstance(block, dict):
        return block, []
    new_block, all_changed = {}, []
    for key, value in block.items():
        if isinstance(value, list):
            new_val, ch = _update_dep_list(value, url_map)
            new_block[key] = new_val
            all_changed.extend(ch)
        elif isinstance(value, str):
            mapped = _remap(value.split("#")[0].strip(), url_map)
            if mapped and mapped != value:
                all_changed.append((value, mapped))
                new_block[key] = mapped
            else:
                new_block[key] = value
        else:
            new_block[key] = value
    return new_block, all_changed


# ──────────────────────────────────────────────────────────────────────────────
# Pass 2 — apply changes to each file
# ──────────────────────────────────────────────────────────────────────────────

def process_file(
    md_path: Path,
    url_map: dict[str, str],
    dry_run: bool,
    verbose: bool,
) -> dict:
    result = {
        "path": str(md_path),
        "changed": False,
        "permalink_change": None,
        "dep_changes": [],
        "error": None,
    }

    fm, body = read_fm(md_path)
    if fm is None:
        return result

    parent = md_path.parent.name
    level_dir = parent if LEVEL_RE.match(parent) else None
    quest_type = fm.get("quest_type")
    current_pl = fm.get("permalink")

    # 1. Permalink
    new_pl = compute_new_permalink(str(current_pl), level_dir, md_path, quest_type) if current_pl else None
    pl_changed = bool(new_pl and new_pl != str(current_pl))

    # 2. Dep URLs
    dep_changes: list = []
    for dep_key in ("quest_dependencies", "quest_relationships"):
        if dep_key in fm:
            new_block, ch = _update_dep_block(fm[dep_key], url_map)
            if ch:
                fm[dep_key] = new_block
                dep_changes.extend(ch)

    if not pl_changed and not dep_changes:
        return result

    result["changed"] = True
    result["dep_changes"] = dep_changes

    if pl_changed:
        old_pl = str(current_pl)
        result["permalink_change"] = (old_pl, new_pl)

        rf = fm.get("redirect_from") or []
        if isinstance(rf, str):
            rf = [rf]
        else:
            rf = list(rf)
        old_norm = old_pl.rstrip("/") + "/"
        if old_pl not in rf and old_norm not in rf:
            rf.append(old_norm)
        fm["redirect_from"] = rf
        fm["permalink"] = new_pl

    if not dry_run:
        write_fm(md_path, fm, body)

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def iter_quest_files(quest_dir: Path):
    for md_file in sorted(quest_dir.rglob("*.md")):
        if any(p in md_file.parts for p in SKIP_SUBDIRS):
            continue
        if md_file.parent == quest_dir and md_file.stem in SKIP_STEMS:
            continue
        yield md_file


def main():
    parser = argparse.ArgumentParser(
        description="Migrate quest permalinks to /quests/XXXX/[side-quests/]slug/ format"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Show changes without writing files")
    parser.add_argument("--verbose", action="store_true",
                        help="Show per-file dep-URL changes")
    parser.add_argument("--directory", default="pages/_quests",
                        help="Quest directory (default: pages/_quests)")
    args = parser.parse_args()

    quest_dir = Path(args.directory)
    if not quest_dir.exists():
        print(f"ERROR: Quest directory not found: {quest_dir}")
        sys.exit(1)

    if args.dry_run:
        print("DRY RUN — no files will be modified\n")

    # ── Pass 1: build URL map ────────────────────────────────────────────
    url_map = build_url_map(quest_dir)
    print(f"URL map: {len(url_map) // 2} old permalinks → new permalinks\n")

    # ── Pass 2: apply ────────────────────────────────────────────────────
    total = changed = errors = 0
    for md_file in iter_quest_files(quest_dir):
        total += 1
        result = process_file(md_file, url_map, dry_run=args.dry_run, verbose=args.verbose)

        if result["error"]:
            errors += 1
            print(f"  ERROR {md_file}: {result['error']}")
        elif result["changed"]:
            changed += 1
            pl = result["permalink_change"]
            rel = md_file.relative_to(quest_dir.parent.parent)
            if pl:
                print(f"  ✅ {rel}")
                print(f"     {pl[0]}  →  {pl[1]}")
            if args.verbose:
                for old_dep, new_dep in result["dep_changes"]:
                    print(f"     dep: {old_dep}  →  {new_dep}")

    print()
    print(f"Scanned: {total}  Changed: {changed}  Errors: {errors}")
    if args.dry_run:
        print("(dry run — no files written)")


if __name__ == "__main__":
    main()
