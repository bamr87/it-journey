#!/usr/bin/env python3
"""
character_skills.py — generator + drift check for the per-character quest skills.

One Claude skill per character path lives in `.claude/skills/quest-character-<key>/
SKILL.md` (key = `_data/quests/paths.yml › key`). Each skill is HAND-AUTHORED
prose (persona, voice, walk/fix lenses, per-level exercises) wrapped around ONE
GENERATED block — the path roadmap — that this script derives from the same two
sources every other quest tool derives from:

  * `_data/quests/paths.yml`        (curated: key, name, icon, tagline, levels)
  * `scripts/quest/quest_registry.py` (levels → theme / tier / emoji / XP)

so the skills can never disagree with the planner (`walkthrough_plan.py` resolves
slices from the SAME data). The generated block sits between markers:

    <!-- BEGIN GENERATED: character-roadmap -->
    ...regenerated content; never hand-edit...
    <!-- END GENERATED: character-roadmap -->

Everything outside the markers is authored content and is never touched.

The check enforces, per character in paths.yml:
  1. the skill file exists (and no `quest-character-*` skill exists for a
     character that has been removed from paths.yml),
  2. the generated roadmap block is byte-identical to a fresh regeneration,
  3. the authored exercises cover the path: one `### Level <code>` heading per
     level the path visits (order-agnostic; extra prose is fine),
  4. the frontmatter `name:` matches the skill directory.

Usage:
    python3 scripts/quest/character_skills.py --check      # report drift; exit 1 if any
    python3 scripts/quest/character_skills.py --write      # regenerate blocks in place
    python3 scripts/quest/character_skills.py --list       # show the skill ↔ path map
    python3 scripts/quest/character_skills.py --selftest   # offline fixture round-trip

Make targets: `make quest-skills` (write) / `make quest-skills-check` (check).
`quest_audit.py` runs the same check as its non-gating `skills` layer, so drift
is surfaced by every audit without redding an unrelated content PR (the audit's
PR triggers don't watch paths.yml). This script never creates a missing skill
file — authoring a persona is human/agent work; it reports the gap instead.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("Error: PyYAML is required but not installed (pip install pyyaml).",
          file=sys.stderr)
    raise

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import quest_registry as reg  # noqa: E402

REPO_ROOT = _HERE.parents[1]
PATHS_YML = REPO_ROOT / "_data" / "quests" / "paths.yml"
SKILLS_ROOT = REPO_ROOT / ".claude" / "skills"
SKILL_PREFIX = "quest-character-"

BEGIN_MARK = "<!-- BEGIN GENERATED: character-roadmap -->"
END_MARK = "<!-- END GENERATED: character-roadmap -->"
BLOCK_RE = re.compile(
    re.escape(BEGIN_MARK) + r"\n.*?" + re.escape(END_MARK), re.DOTALL)
LEVEL_HEADING_RE = re.compile(r"^### .*?\bLevel (?P<code>[01]{4})\b", re.MULTILINE)
FM_NAME_RE = re.compile(r"^name:\s*(?P<name>\S+)\s*$", re.MULTILINE)


# --- data -------------------------------------------------------------------

def load_paths(path: Path = PATHS_YML) -> List[dict]:
    if not path.exists():
        raise FileNotFoundError(f"{path} not found.")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list) or not data:
        raise ValueError(f"{path} holds no character paths.")
    return data


def skill_name(key: str) -> str:
    return f"{SKILL_PREFIX}{key}"


def _rel(p: Path) -> Path:
    """Repo-relative when possible (fixture roots in the selftest are not)."""
    try:
        return p.relative_to(REPO_ROOT)
    except ValueError:
        return p


def skill_file(key: str, root: Path = SKILLS_ROOT) -> Path:
    return root / skill_name(key) / "SKILL.md"


# --- rendering --------------------------------------------------------------

def render_roadmap(char: dict) -> str:
    """The generated block body for one character (markers included).

    Table-only on purpose: every line is atomic for tools/unwrap-prose.py, and a
    table diffs cleanly when paths.yml or the registry moves.
    """
    key = char.get("key", "?")
    lines = [
        BEGIN_MARK,
        f"> {char.get('icon', '')} **{char.get('name', key)}** — {char.get('tagline', '')}".rstrip(),
        ">",
        f"> Path key `{key}` · {len(char.get('levels') or [])} levels · source: `_data/quests/paths.yml` + `scripts/quest/quest_registry.py` · regenerate: `make quest-skills`",
        "",
        "| # | Level | Theme | Tier | XP | Hub |",
        "|---|---|---|---|---|---|",
    ]
    for i, code in enumerate(char.get("levels") or [], 1):
        theme = reg.theme_of(code)
        tier = reg.tier_of(code) or "?"
        emoji = reg.tier_emoji_of(code)
        xp = reg.LEVELS.get(code, {}).get("xp_range", "?")
        lines.append(
            f"| {i} | `{code}` | {theme} | {emoji} {tier} | {xp} | `{reg.canonical_level_permalink(code)}` |")
    lines.append(END_MARK)
    return "\n".join(lines)


def inject(text: str, block: str, path: Path) -> str:
    """Replace the marked block in `text` with `block`. Errors are ValueErrors."""
    begins, ends = text.count(BEGIN_MARK), text.count(END_MARK)
    if begins != 1 or ends != 1:
        raise ValueError(
            f"{path}: expected exactly one generated block "
            f"({begins} BEGIN / {ends} END markers found).")
    new_text, n = BLOCK_RE.subn(lambda _m: block, text, count=1)
    if n != 1:
        raise ValueError(f"{path}: markers present but malformed (END before BEGIN?).")
    return new_text


# --- checking ---------------------------------------------------------------

def collect_problems(paths: Optional[List[dict]] = None,
                     root: Path = SKILLS_ROOT) -> List[str]:
    """Every way the skills can disagree with the data, as human-readable lines."""
    chars = paths if paths is not None else load_paths()
    problems: List[str] = []
    keys = [c.get("key", "") for c in chars]

    # 1. coverage both ways: every path has a skill, every skill has a path.
    for key in keys:
        if not skill_file(key, root).exists():
            problems.append(
                f"missing skill: {_rel(skill_file(key, root))} "
                f"(character '{key}' is in paths.yml but has no skill)")
    if root.exists():
        for d in sorted(root.glob(f"{SKILL_PREFIX}*")):
            key = d.name[len(SKILL_PREFIX):]
            if key not in keys:
                problems.append(
                    f"orphan skill: {_rel(d)} "
                    f"(no '{key}' character in paths.yml — remove or re-add the path)")

    for char in chars:
        key = char.get("key", "")
        f = skill_file(key, root)
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        rel = _rel(f)

        # 2. generated block freshness.
        try:
            fresh = inject(text, render_roadmap(char), f)
        except ValueError as e:
            problems.append(str(e).replace(str(f), str(rel)))
            continue
        if fresh != text:
            problems.append(
                f"stale roadmap: {rel} — run `make quest-skills` and commit")

        # 3. exercise coverage: one `### Level <code>` heading per path level.
        found = {m.group("code") for m in LEVEL_HEADING_RE.finditer(text)}
        for code in char.get("levels") or []:
            if code not in found:
                problems.append(
                    f"uncovered level: {rel} has no '### … Level {code}' exercises "
                    f"heading (the {key} path visits {code} — {reg.theme_of(code)})")
        for code in sorted(found.difference(char.get("levels") or [])):
            problems.append(
                f"extra level: {rel} has exercises for {code}, which the {key} "
                f"path does not visit in paths.yml")

        # 4. frontmatter name matches the directory.
        m = FM_NAME_RE.search(text)
        if not m or m.group("name") != skill_name(key):
            problems.append(
                f"name mismatch: {rel} frontmatter name "
                f"'{m.group('name') if m else '(none)'}' != '{skill_name(key)}'")
    return problems


def write_blocks(paths: Optional[List[dict]] = None,
                 root: Path = SKILLS_ROOT) -> int:
    """Regenerate every skill's roadmap block in place. Returns files changed."""
    chars = paths if paths is not None else load_paths()
    changed = 0
    for char in chars:
        key = char.get("key", "")
        f = skill_file(key, root)
        if not f.exists():
            print(f"  ⚠️  no skill for '{key}' ({_rel(f)}) — "
                  f"author it first (see docs/quests/CHARACTER_SKILLS.md), "
                  f"then rerun.")
            continue
        text = f.read_text(encoding="utf-8")
        fresh = inject(text, render_roadmap(char), f)
        if fresh != text:
            f.write_text(fresh, encoding="utf-8")
            changed += 1
            print(f"  ✏️  {_rel(f)} roadmap regenerated")
        else:
            print(f"  ✅ {_rel(f)} already fresh")
    return changed


# --- selftest ---------------------------------------------------------------

_FIXTURE = """---
name: quest-character-testchar
description: fixture
---

Intro prose.

<!-- BEGIN GENERATED: character-roadmap -->
(placeholder)
<!-- END GENERATED: character-roadmap -->

## Per-level exercises

### 🌱 Level 0000 — Foundation & Init World

- do the thing
"""


def _selftest() -> int:
    """Offline fixture round-trip: inject is idempotent; check finds each drift."""
    char = {"key": "testchar", "name": "Test Char", "icon": "🧪",
            "tagline": "Fixture.", "levels": ["0000"]}
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        f = root / skill_name("testchar") / "SKILL.md"
        f.parent.mkdir(parents=True)
        f.write_text(_FIXTURE, encoding="utf-8")

        # write → fresh; second write → no-op (idempotent).
        assert write_blocks([char], root) == 1, "first write must change the file"
        assert write_blocks([char], root) == 0, "second write must be a no-op"
        assert collect_problems([char], root) == [], "fresh fixture must be clean"

        # each drift class is detected.
        text = f.read_text(encoding="utf-8")
        f.write_text(text.replace("Foundation", "Fnd", 1), encoding="utf-8")
        assert any("stale roadmap" in p for p in collect_problems([char], root)), \
            "edited block must read as stale"
        f.write_text(text.replace("Level 0000", "Level 1111"), encoding="utf-8")
        probs = collect_problems([char], root)
        assert any("uncovered level" in p for p in probs), "missing heading undetected"
        # (renaming the heading to 1111 also makes the block stale — fine.)
        f.write_text(text, encoding="utf-8")

        # a path with no skill / a skill with no path.
        char2 = {"key": "ghost", "name": "Ghost", "icon": "👻",
                 "tagline": "?", "levels": ["0000"]}
        assert any("missing skill" in p
                   for p in collect_problems([char, char2], root))
        assert any("orphan skill" in p for p in collect_problems([char2], root))

    # live-data smoke: every registry lookup used by render resolves.
    for c in load_paths():
        block = render_roadmap(c)
        assert BEGIN_MARK in block and END_MARK in block
        assert "Unknown" not in block, f"unknown level theme in {c.get('key')} roadmap"
    print("✅ character_skills self-test passed (fixture round-trip + live render).")
    return 0


# --- CLI --------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Generator + drift check for .claude/skills/quest-character-*/SKILL.md.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="Report every drift problem; exit 1 if any.")
    mode.add_argument("--write", action="store_true",
                      help="Regenerate the roadmap blocks in place.")
    mode.add_argument("--list", action="store_true",
                      help="Show the character ↔ skill map, then exit.")
    mode.add_argument("--selftest", action="store_true",
                      help="Run the offline fixture self-check, then exit.")
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    chars = load_paths()

    if args.list or not (args.check or args.write):
        for c in chars:
            f = skill_file(c.get("key", ""))
            state = "✅" if f.exists() else "❌ missing"
            print(f"{c.get('icon', '')} {c.get('key', ''):<20} → "
                  f"{_rel(f)}  {state}")
        if not args.list:
            print("\n(use --check to verify freshness, --write to regenerate)")
        return 0

    if args.write:
        changed = write_blocks(chars)
        print(f"{changed} file(s) updated.")
        problems = collect_problems(chars)
        if problems:
            print("\nRemaining problems (authoring work, not generation):")
            for pr in problems:
                print(f"  ❌ {pr}")
            return 1
        return 0

    problems = collect_problems(chars)
    if problems:
        print(f"❌ {len(problems)} character-skill problem(s):")
        for pr in problems:
            print(f"  - {pr}")
        print("\nFix: `make quest-skills` for stale roadmaps; author/remove skill "
              "files for coverage gaps (see docs/quests/CHARACTER_SKILLS.md).")
        return 1
    print(f"✅ {len(chars)} character skills in sync with paths.yml + the registry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
