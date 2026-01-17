#!/usr/bin/env python3
"""
Script: update-quest-home.py
Description: Update pages/_quests/home.md with an auto-generated quest index based on quest frontmatter.
Author: IT-Journey Team
Version: 1.0.0
Last Modified: 2026-01-15
Dependencies: python3, pyyaml
Tested On: macOS 13+, Ubuntu 22.04+, WSL2

Usage: update-quest-home.py [OPTIONS]
       update-quest-home.py --help

Exit Codes:
  0 - Success
  1 - General error
  2 - Misuse of command (invalid arguments)
  3 - Missing dependency
  4 - Permission denied
  5 - Configuration error
  6 - Runtime error

Related:
  - Docs: scripts/quest/README.md
  - Quest: pages/_quests/home.md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover - handled at runtime
    print("[ERROR] PyYAML is required but not installed. Install with: pip3 install pyyaml")
    sys.exit(3)


SCRIPT_VERSION = "1.0.0"
DEFAULT_QUEST_DIR = Path("pages/_quests")
DEFAULT_HOME_FILE = Path("pages/_quests/home.md")

MARKER_START = "<!-- QUEST_INDEX:START -->"
MARKER_END = "<!-- QUEST_INDEX:END -->"


class ScriptError(Exception):
    """Base exception for script failures."""


@dataclass
class QuestEntry:
    title: str
    permalink: str
    level: str
    difficulty: str
    estimated_time: str
    quest_type: str
    quest_series: str
    quest_line: str
    draft: bool


def log_info(message: str) -> None:
    print(f"[INFO] {message}")


def log_warn(message: str) -> None:
    print(f"[WARN] {message}")


def log_error(message: str) -> None:
    print(f"[ERROR] {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update pages/_quests/home.md with an auto-generated quest index."
    )
    parser.add_argument(
        "--quests-dir",
        type=Path,
        default=DEFAULT_QUEST_DIR,
        help="Path to quests directory (default: pages/_quests)",
    )
    parser.add_argument(
        "--home-file",
        type=Path,
        default=DEFAULT_HOME_FILE,
        help="Path to home.md to update (default: pages/_quests/home.md)",
    )
    parser.add_argument(
        "--exclude-drafts",
        action="store_true",
        help="Exclude quests marked as draft from the index",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without writing to disk",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {SCRIPT_VERSION}",
    )
    return parser.parse_args()


def read_text(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except PermissionError as exc:
        raise ScriptError(f"Permission denied reading {file_path}: {exc}") from exc
    except OSError as exc:
        raise ScriptError(f"Failed to read {file_path}: {exc}") from exc


def write_text(file_path: Path, content: str) -> None:
    try:
        file_path.write_text(content, encoding="utf-8")
    except PermissionError as exc:
        raise ScriptError(f"Permission denied writing {file_path}: {exc}") from exc
    except OSError as exc:
        raise ScriptError(f"Failed to write {file_path}: {exc}") from exc


def split_frontmatter(content: str) -> Tuple[Optional[str], str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1), match.group(2)


def parse_frontmatter(frontmatter_text: str, file_path: Path) -> Dict:
    try:
        data = yaml.safe_load(frontmatter_text) or {}
        if not isinstance(data, dict):
            log_warn(f"Frontmatter in {file_path} is not a mapping; skipping.")
            return {}
        return data
    except yaml.YAMLError as exc:
        log_warn(f"YAML parsing error in {file_path}: {exc}")
        return {}


def iter_quest_files(quests_dir: Path) -> Iterable[Path]:
    skip_tokens = {
        "templates/",
        "README.md",
        "home.md",
        "docs/",
        "codex/",
        "inventory/",
        "QUEST_ORGANIZATION_SUMMARY.md",
        "world_map.md",
    }
    for md_file in quests_dir.rglob("*.md"):
        md_str = md_file.as_posix()
        if any(token in md_str for token in skip_tokens):
            continue
        yield md_file


def build_quest_index(
    quests_dir: Path, exclude_drafts: bool, verbose: bool
) -> Tuple[Dict[str, List[QuestEntry]], int]:
    quests_by_level: Dict[str, List[QuestEntry]] = {}
    total = 0

    for md_file in iter_quest_files(quests_dir):
        content = read_text(md_file)
        frontmatter_text, _ = split_frontmatter(content)
        if not frontmatter_text:
            if verbose:
                log_warn(f"Skipping {md_file} (missing frontmatter)")
            continue

        frontmatter = parse_frontmatter(frontmatter_text, md_file)
        if not frontmatter:
            continue

        if frontmatter.get("fmContentType") != "quest":
            continue

        permalink = str(frontmatter.get("permalink", "")).strip()
        if not permalink:
            if verbose:
                log_warn(f"Skipping {md_file} (missing permalink)")
            continue

        draft = bool(frontmatter.get("draft", False))
        if exclude_drafts and draft:
            continue

        entry = QuestEntry(
            title=str(frontmatter.get("title", "Untitled Quest")).strip(),
            permalink=permalink,
            level=str(frontmatter.get("level", "unknown")).strip() or "unknown",
            difficulty=str(frontmatter.get("difficulty", "N/A")).strip(),
            estimated_time=str(frontmatter.get("estimated_time", "N/A")).strip(),
            quest_type=str(frontmatter.get("quest_type", "N/A")).strip(),
            quest_series=str(frontmatter.get("quest_series", "")).strip(),
            quest_line=str(frontmatter.get("quest_line", "")).strip(),
            draft=draft,
        )

        quests_by_level.setdefault(entry.level, []).append(entry)
        total += 1

    return quests_by_level, total


def level_sort_key(level: str) -> Tuple[int, str]:
    if level == "unknown":
        return (10_000, level)
    try:
        return (int(level, 2), level)
    except ValueError:
        return (9_999, level)


def render_level_table(entries: List[QuestEntry]) -> List[str]:
    lines = [
        "| Quest | Type | Difficulty | Time | Series | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in sorted(entries, key=lambda item: item.title.lower()):
        status = "🔮 Draft" if entry.draft else "✅ Complete"
        series = entry.quest_series or entry.quest_line or "—"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"[{entry.title}]({entry.permalink})",
                    entry.quest_type or "N/A",
                    entry.difficulty or "N/A",
                    entry.estimated_time or "N/A",
                    series,
                    status,
                ]
            )
            + " |"
        )
    return lines


def generate_index_content(
    quests_by_level: Dict[str, List[QuestEntry]], total: int
) -> str:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )
    lines: List[str] = [
        "_This section is auto-generated. Do not edit manually._",
        f"_Last generated: {generated_at}_",
        "",
        f"**Total quests:** {total}",
        "",
    ]

    for level in sorted(quests_by_level.keys(), key=level_sort_key):
        entries = quests_by_level[level]
        if not entries:
            continue
        if level == "unknown":
            lines.append("### Uncategorized Quests")
        else:
            lines.append(f"### Level {level}")
        lines.append("")
        lines.extend(render_level_table(entries))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def update_lastmod(frontmatter_text: str) -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )
    if re.search(r"^lastmod:\s*.*$", frontmatter_text, flags=re.MULTILINE):
        return re.sub(
            r"^lastmod:\s*.*$",
            f"lastmod: {timestamp}",
            frontmatter_text,
            count=1,
            flags=re.MULTILINE,
        )
    return frontmatter_text.rstrip() + f"\nlastmod: {timestamp}\n"


def inject_index(content: str, generated: str) -> str:
    frontmatter_text, body = split_frontmatter(content)
    if frontmatter_text is None:
        raise ScriptError("home.md is missing frontmatter; cannot update safely.")

    frontmatter_text = update_lastmod(frontmatter_text)
    updated_frontmatter = f"---\n{frontmatter_text}\n---\n"

    if MARKER_START in body and MARKER_END in body:
        pattern = re.compile(
            rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}",
            re.DOTALL,
        )
        replacement = f"{MARKER_START}\n{generated}{MARKER_END}"
        updated_body = pattern.sub(replacement, body)
    else:
        generated_section = (
            "\n\n## 🧭 Quest Index (Auto-Generated)\n\n"
            f"{MARKER_START}\n{generated}{MARKER_END}\n"
        )
        updated_body = body.rstrip() + generated_section

    return updated_frontmatter + updated_body


def main() -> int:
    args = parse_args()

    quests_dir = args.quests_dir
    home_file = args.home_file

    if not quests_dir.exists():
        log_error(f"Quests directory not found: {quests_dir}")
        return 5

    if not home_file.exists():
        log_error(f"Home file not found: {home_file}")
        return 5

    quests_by_level, total = build_quest_index(
        quests_dir=quests_dir,
        exclude_drafts=args.exclude_drafts,
        verbose=args.verbose,
    )

    if total == 0:
        log_error("No quests found. Ensure fmContentType: quest is set in frontmatter.")
        return 6

    generated = generate_index_content(quests_by_level, total)
    content = read_text(home_file)
    updated = inject_index(content, generated)

    if args.dry_run:
        log_info("Dry run enabled. No changes written.")
        print(updated)
        return 0

    write_text(home_file, updated)
    log_info(f"Updated quest index in {home_file}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ScriptError as exc:
        log_error(str(exc))
        raise SystemExit(1) from exc
