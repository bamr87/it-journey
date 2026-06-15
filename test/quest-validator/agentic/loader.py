"""
Quest discovery + frontmatter parsing for the agentic validator.

Reuses ``quest_registry`` (the single source of truth) for the is-quest / is-draft
rules and the skip lists, so this tier can never disagree with tier 1 about what
counts as a playable quest.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Optional

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "scripts" / "quest"))
import quest_registry as reg  # noqa: E402

QUESTS_DIR = _REPO_ROOT / "pages" / "_quests"
_FM_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)', re.DOTALL)


class Quest:
    """A loaded, parsed quest ready to hand to the agent."""

    __slots__ = ("path", "rel_path", "fm", "body", "title", "level",
                 "difficulty", "quest_type", "slug")

    def __init__(self, path: Path, fm: dict, body: str):
        self.path = path
        try:
            self.rel_path = str(path.relative_to(_REPO_ROOT))
        except ValueError:
            self.rel_path = str(path)
        self.fm = fm or {}
        self.body = body or ""
        self.title = str(self.fm.get("title") or path.stem)
        self.level = str(self.fm.get("level") or "")
        self.difficulty = str(self.fm.get("difficulty") or "")
        self.quest_type = str(self.fm.get("quest_type") or "")
        self.slug = reg.slug_from_filename(path.name)

    @property
    def theme(self) -> str:
        return reg.theme_of(self.level) if self.level else ""

    def objectives(self) -> List[str]:
        """Best-effort pull of stated learning objectives from frontmatter."""
        for key in ("learning_objectives", "objectives", "validation_criteria"):
            val = self.fm.get(key)
            if isinstance(val, list):
                return [str(v) for v in val][:12]
        return []

    def to_meta(self) -> dict:
        return {
            "path": self.rel_path, "title": self.title, "level": self.level,
            "theme": self.theme, "difficulty": self.difficulty,
            "quest_type": self.quest_type, "slug": self.slug,
        }


def _parse(path: Path) -> Optional[Quest]:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = _FM_RE.match(text)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    return Quest(path, fm, m.group(2))


def load_quest(path) -> Optional[Quest]:
    p = Path(path)
    if not p.is_absolute():
        p = (_REPO_ROOT / p).resolve()
    if not p.exists():
        raise FileNotFoundError(p)
    return _parse(p)


def discover(directory=None, include_drafts: bool = False) -> List[Quest]:
    """All playable, scored quests under ``directory`` (default pages/_quests)."""
    root = Path(directory) if directory else QUESTS_DIR
    if not root.is_absolute():
        root = (_REPO_ROOT / root).resolve()
    out: List[Quest] = []
    for path in sorted(root.rglob("*.md")):
        parts = set(path.relative_to(root).parts[:-1])
        if parts & set(reg.SKIP_SUBDIRS):
            continue
        if path.stem in getattr(reg, "SKIP_STEMS", ()):  # README etc.
            continue
        q = _parse(path)
        if q is None or not reg.is_quest(q.fm):
            continue
        if not include_drafts and reg.is_draft(q.fm):
            continue
        out.append(q)
    return out


def sample(quests: List[Quest], n: int) -> List[Quest]:
    """A deterministic, representative sample: spread across levels, round-robin.

    Picks at most ``n`` quests, taking one from each level in turn (levels in
    canonical order) before taking a second from any level — so a small sample
    still covers the breadth of the curriculum rather than clustering in 0000.
    """
    if n <= 0 or n >= len(quests):
        return list(quests)
    by_level: dict = {}
    for q in quests:
        by_level.setdefault(q.level, []).append(q)
    order = [lv for lv in reg.LEVEL_ORDER if lv in by_level] + \
            [lv for lv in by_level if lv not in reg.LEVEL_ORDER]
    picked: List[Quest] = []
    round_i = 0
    while len(picked) < n:
        progressed = False
        for lv in order:
            bucket = by_level.get(lv, [])
            if round_i < len(bucket):
                picked.append(bucket[round_i])
                progressed = True
                if len(picked) >= n:
                    break
        if not progressed:
            break
        round_i += 1
    return picked
