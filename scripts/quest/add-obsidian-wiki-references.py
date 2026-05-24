#!/usr/bin/env python3
"""
add-obsidian-wiki-references.py

Ensure every playable quest (fmContentType: quest) includes a Knowledge Graph
section with Obsidian-style [[wiki links]] to level hubs, dependencies, and
series hubs. Idempotent: re-run safely replaces an existing section.

Usage:
  python3 scripts/quest/add-obsidian-wiki-references.py [--dry-run] [--verbose]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required.  pip install pyyaml", file=sys.stderr)
    sys.exit(1)

QUEST_DIR_DEFAULT = Path("pages/_quests")
SKIP_STEMS = {"home", "README", "QUEST_BUILD_PLAN", "NETWORK_REPORT"}
SKIP_SUBDIRS = {"templates", "docs", "inventory"}
LEVEL_RE = re.compile(r"^[01]{4}$")

SECTION_HEADING = "## 🕸️ Knowledge Graph"
SECTION_MARKER = SECTION_HEADING

OVERWORLD_TITLE = "🏰 Overworld - Master Quest Map"
STUDY_HUB_TITLE = "The Agentic Codex: GH-600 Study Hub"
NOTES_HUB_TITLE = "GH-600 Agentic AI Quick-Reference Notes"
OBSIDIAN_DOCS_TITLE = "Obsidian Knowledge Graph and Wiki Links"

# Agentic quest slug → related GH-600 quick-reference note title
AGENTIC_NOTE_MAP = {
    "agentic-mcp-server-mastery": "MCP Quick Reference",
    "agentic-autonomy-levels-matrix": "Autonomy Levels Matrix",
    "agentic-success-criteria-and-signals": "Evaluation Signals Table",
    "agentic-codex-capstone-exam-trial": "GH-600 Skills Checklist",
    "agentic-sdlc-integration": "GH-600 Exam Overview",
}

DEP_KINDS = [
    ("required_quests", "Prerequisites"),
    ("recommended_quests", "Recommended"),
    ("unlocks_quests", "Unlocks"),
]

PLAYABLE_QUEST_TYPES = {"main_quest", "side_quest", "bonus_quest", "epic_quest"}


def _extract_frontmatter(path: Path) -> tuple[dict, str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}, text, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    body = text[m.end():]
    return fm, text, body


def _iter_quest_files(quest_dir: Path):
    for entry in sorted(quest_dir.iterdir()):
        if not entry.is_dir():
            if entry.suffix == ".md" and entry.stem not in SKIP_STEMS:
                yield entry, None
            continue
        if entry.name in SKIP_SUBDIRS:
            continue
        level = entry.name if LEVEL_RE.match(entry.name) else None
        for md in sorted(entry.rglob("*.md")):
            if md.stem in SKIP_STEMS:
                continue
            relative = md.relative_to(entry)
            if any(p in SKIP_SUBDIRS for p in relative.parts[:-1]):
                continue
            yield md, level


def _norm_permalink(url: str) -> str | None:
    if not url or not isinstance(url, str):
        return None
    url = url.split("#", 1)[0].strip()
    if "planned quest" in url.lower():
        return None
    if not url.startswith("/quests/"):
        return None
    return url if url.endswith("/") else url + "/"


def _wiki_link(title: str) -> str:
    return f"[[{title}]]"


def _wiki_line(label: str, titles: list[str]) -> str | None:
    if not titles:
        return None
    links = " · ".join(_wiki_link(t) for t in titles)
    return f"**{label}:** {links}"


def _load_level_titles(quest_dir: Path) -> dict[str, str]:
    titles: dict[str, str] = {}
    for level_dir in quest_dir.iterdir():
        if not level_dir.is_dir() or not LEVEL_RE.match(level_dir.name):
            continue
        readme = level_dir / "README.md"
        if not readme.is_file():
            continue
        fm, _, _ = _extract_frontmatter(readme)
        title = fm.get("title")
        if title:
            titles[level_dir.name] = str(title)
    return titles


def _build_title_index(quest_dir: Path) -> dict[str, str]:
    index: dict[str, str] = {}
    for md_path, _ in _iter_quest_files(quest_dir):
        fm, _, _ = _extract_frontmatter(md_path)
        permalink = fm.get("permalink")
        title = fm.get("title")
        if permalink and title:
            key = _norm_permalink(str(permalink))
            if key:
                index[key] = str(title)
    return index


def _resolve_titles(urls, title_index: dict[str, str]) -> list[str]:
    titles: list[str] = []
    seen: set[str] = set()
    if isinstance(urls, str):
        urls = [urls]
    if not isinstance(urls, list):
        return titles
    for raw in urls:
        if not raw:
            continue
        key = _norm_permalink(str(raw))
        if not key:
            continue
        title = title_index.get(key)
        if title and title not in seen:
            seen.add(title)
            titles.append(title)
    return titles


def _is_playable_quest(fm: dict) -> bool:
    if fm.get("fmContentType") == "quest":
        return True
    return str(fm.get("quest_type", "")) in PLAYABLE_QUEST_TYPES


def _is_agentic_quest(fm: dict, md_path: Path) -> bool:
    quest_line = str(fm.get("quest_line", "")).lower()
    quest_arc = str(fm.get("quest_arc", ""))
    if quest_line == "gh-600" or quest_arc == "The Agentic Codex":
        return True
    return md_path.name.startswith("agentic-")


def _related_note_title(md_path: Path) -> str | None:
    stem = md_path.stem
    return AGENTIC_NOTE_MAP.get(stem)


def _build_section(fm: dict, md_path: Path, title_index: dict[str, str], level_titles: dict[str, str]) -> str:
    lines: list[str] = [
        SECTION_HEADING,
        "",
        "*Structured wiki-links connect this quest to the IT-Journey knowledge graph. "
        "Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*",
        "",
    ]

    body_lines: list[str] = []

    level = str(fm.get("level", ""))
    if level in level_titles:
        body_lines.append(_wiki_line("Level hub", [level_titles[level]]))

    body_lines.append(_wiki_line("Overworld", [OVERWORLD_TITLE]))

    if _is_agentic_quest(fm, md_path):
        agentic_links = [STUDY_HUB_TITLE, NOTES_HUB_TITLE]
        note = _related_note_title(md_path)
        if note:
            agentic_links.append(note)
        body_lines.append(_wiki_line("Study track", agentic_links))

    deps = fm.get("quest_dependencies") or {}
    if isinstance(deps, dict):
        for fm_key, label in DEP_KINDS:
            resolved = _resolve_titles(deps.get(fm_key), title_index)
            line = _wiki_line(label, resolved)
            if line:
                body_lines.append(line)

    # Cross-links from quest_relationships when present
    rels = fm.get("quest_relationships") or {}
    if isinstance(rels, dict):
        for fm_key, label in [
            ("sequel_quests", "Sequel quests"),
            ("parallel_quests", "Parallel quests"),
            ("child_quests", "Related quests"),
        ]:
            resolved = _resolve_titles(rels.get(fm_key), title_index)
            line = _wiki_line(label, resolved)
            if line:
                body_lines.append(line)

    body_lines.append(_wiki_line("Obsidian docs", [OBSIDIAN_DOCS_TITLE]))

    for line in body_lines:
        if line:
            lines.append(line)

    lines.append("")
    return "\n".join(lines)


def _strip_existing_section(body: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(SECTION_MARKER)}\s*\n.*?(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub("", body).rstrip()


def _apply_section(body: str, section: str) -> str:
    body = _strip_existing_section(body)
    if not body:
        return section + "\n"
    return body + "\n\n" + section + "\n"


def _normalized(body: str, section: str) -> str:
    return _apply_section(body, section)


def process_quest_dir(quest_dir: Path, dry_run: bool, verbose: bool) -> tuple[int, int, int]:
    title_index = _build_title_index(quest_dir)
    level_titles = _load_level_titles(quest_dir)
    updated = skipped = errors = 0

    for md_path, _ in _iter_quest_files(quest_dir):
        fm, full_text, body = _extract_frontmatter(md_path)
        if not _is_playable_quest(fm):
            continue
        if not fm.get("title") or not fm.get("permalink"):
            skipped += 1
            continue

        section = _build_section(fm, md_path, title_index, level_titles)
        new_body = _normalized(body, section)

        if new_body == body:
            skipped += 1
            continue

        if verbose or dry_run:
            print(f"{'[dry-run] ' if dry_run else ''}update: {md_path}")

        if not dry_run:
            try:
                m = re.match(r"^(---\s*\n.*?\n---\s*\n?)", full_text, re.DOTALL)
                if not m:
                    errors += 1
                    print(f"  skip (no frontmatter): {md_path}", file=sys.stderr)
                    continue
                md_path.write_text(m.group(1) + new_body, encoding="utf-8")
            except OSError as exc:
                errors += 1
                print(f"  error: {md_path}: {exc}", file=sys.stderr)
                continue

        updated += 1

    return updated, skipped, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quest-dir", type=Path, default=QUEST_DIR_DEFAULT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    quest_dir = args.quest_dir
    if not quest_dir.is_dir():
        print(f"Error: quest dir not found: {quest_dir}", file=sys.stderr)
        return 1

    updated, skipped, errors = process_quest_dir(quest_dir, args.dry_run, args.verbose)
    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}Obsidian wiki references: {updated} updated, {skipped} unchanged/skipped, {errors} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
