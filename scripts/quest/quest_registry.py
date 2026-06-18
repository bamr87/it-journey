#!/usr/bin/env python3
"""
quest_registry.py — Single source of truth for the IT-Journey quest framework.

Everything taxonomy- and schema-related is defined here exactly once. All quest
tooling (validators, network builder, data/navigation generators, scaffolder)
and — via the generated ``_data/quests/*.yml`` files — every Jekyll layout import
from this module so the framework cannot drift.

What lives here:
  * Level taxonomy   — LEVEL_ORDER, TIERS, LEVELS, TIER_EMOJI, per-level icons
  * Controlled vocab — QUEST_TYPES, FM_CONTENT_TYPES, DIFFICULTIES, SKILL_FOCUS,
                       LEARNING_STYLE
  * Frontmatter schema — REQUIRED_FIELDS, OPTIONAL_FIELDS and the nested sub-key
                       contracts for prerequisites / rewards / quest_dependencies
  * Collection rules — SKIP_SUBDIRS, SKIP_STEMS, is_quest(), is_scored()
  * Routing          — canonical permalink helpers + slug rules + regexes

Tier model is 4 tiers (Apprentice / Adventurer / Warrior / Master). There is NO
"Legend" tier; level 1111 belongs to Master. The 👑 emoji is reserved for the
epic_quest quest-type icon and must never be used as a tier emoji.
"""

from __future__ import annotations

import re

# ─────────────────────────────────────────────────────────────────────────────
# Level taxonomy
# ─────────────────────────────────────────────────────────────────────────────

# Ordered list of all binary level codes (decimal 0–15).
LEVEL_ORDER = [
    "0000", "0001", "0010", "0011",
    "0100", "0101", "0110", "0111",
    "1000", "1001", "1010", "1011",
    "1100", "1101", "1110", "1111",
]

# Tier groupings (4 tiers — no Legend tier).
TIERS = {
    "Apprentice": ["0000", "0001", "0010", "0011"],
    "Adventurer": ["0100", "0101", "0110", "0111"],
    "Warrior":    ["1000", "1001", "1010", "1011"],
    "Master":     ["1100", "1101", "1110", "1111"],
}

# Tier emoji prefixes. 👑 is intentionally absent — it is the epic_quest icon.
TIER_EMOJI = {
    "Apprentice": "🌱",
    "Adventurer": "⚔️",
    "Warrior":    "🔥",
    "Master":     "⚡",
}

# Canonical level metadata. ``theme`` and ``icon`` (a Bootstrap Icons class) are
# the only per-level strings; everything else (tier emoji, XP) is derived.
LEVELS = {
    "0000": {"theme": "Foundation & Init World",        "tier": "Apprentice", "decimal": 0,  "xp_range": "0-250",    "icon": "bi-emoji-sunglasses"},
    "0001": {"theme": "Web Fundamentals",               "tier": "Apprentice", "decimal": 1,  "xp_range": "250-500",  "icon": "bi-feather"},
    "0010": {"theme": "Terminal Mastery",               "tier": "Apprentice", "decimal": 2,  "xp_range": "500-750",  "icon": "bi-terminal"},
    "0011": {"theme": "AI-Assisted Development",        "tier": "Apprentice", "decimal": 3,  "xp_range": "750-1000", "icon": "bi-stars"},
    "0100": {"theme": "Frontend & Containers",          "tier": "Adventurer", "decimal": 4,  "xp_range": "1000-1500","icon": "bi-box-seam"},
    "0101": {"theme": "CI/CD & DevOps",                 "tier": "Adventurer", "decimal": 5,  "xp_range": "1500-2000","icon": "bi-rocket-takeoff"},
    "0110": {"theme": "Database Mastery",               "tier": "Adventurer", "decimal": 6,  "xp_range": "2000-2500","icon": "bi-database"},
    "0111": {"theme": "API Development",                "tier": "Adventurer", "decimal": 7,  "xp_range": "2500-3000","icon": "bi-cloud-arrow-up"},
    "1000": {"theme": "Cloud Computing",                "tier": "Warrior",    "decimal": 8,  "xp_range": "3000-3750","icon": "bi-cloud"},
    "1001": {"theme": "Kubernetes Orchestration",       "tier": "Warrior",    "decimal": 9,  "xp_range": "3750-4500","icon": "bi-grid-3x3-gap"},
    "1010": {"theme": "Monitoring & Observability",     "tier": "Warrior",    "decimal": 10, "xp_range": "4500-5250","icon": "bi-graph-up"},
    "1011": {"theme": "Security & Compliance",          "tier": "Warrior",    "decimal": 11, "xp_range": "5250-6000","icon": "bi-shield-lock"},
    "1100": {"theme": "Data Engineering",               "tier": "Master",     "decimal": 12, "xp_range": "6000-7000","icon": "bi-diagram-3"},
    "1101": {"theme": "Machine Learning & AI",          "tier": "Master",     "decimal": 13, "xp_range": "7000-8000","icon": "bi-cpu"},
    "1110": {"theme": "Architecture & Design Patterns", "tier": "Master",     "decimal": 14, "xp_range": "8000-9000","icon": "bi-building-gear"},
    "1111": {"theme": "Leadership & Innovation",        "tier": "Master",     "decimal": 15, "xp_range": "9000+",    "icon": "bi-trophy"},
}

# ─────────────────────────────────────────────────────────────────────────────
# Controlled vocabularies
# ─────────────────────────────────────────────────────────────────────────────

# Playable quest types (the value of the ``quest_type`` frontmatter field).
QUEST_TYPES = ["main_quest", "side_quest", "epic_quest", "bonus_quest"]

# Quest-type display icons. 👑 = epic_quest (NOT a tier).
QUEST_TYPE_EMOJI = {
    "main_quest":  "🗡️",
    "side_quest":  "⚔️",
    "epic_quest":  "👑",
    "bonus_quest": "🎁",
}

# fmContentType discriminates what a page IS. Only ``quest`` enters quest
# collections / scoring / the network graph; the rest are support content.
FM_CONTENT_TYPES = ["quest", "documentation", "template", "codex"]

# Difficulty enum — emoji-prefixed, the one vocabulary already consistent across
# content, templates and validator.
DIFFICULTIES = ["🟢 Easy", "🟡 Medium", "🔴 Hard", "⚔️ Epic"]

# Lower-cased keyword → canonical difficulty, for normalization of legacy values.
DIFFICULTY_BY_KEY = {
    "easy":   "🟢 Easy",
    "medium": "🟡 Medium",
    "hard":   "🔴 Hard",
    "epic":   "⚔️ Epic",
}

# skill_focus controlled vocabulary (data-engineering, not data-science).
SKILL_FOCUS = [
    "frontend", "backend", "fullstack", "devops", "security",
    "data-engineering", "cloud", "infrastructure", "ai-ml",
]

# learning_style controlled vocabulary.
LEARNING_STYLE = [
    "hands-on", "conceptual", "project-based",
    "problem-solving", "guided-tutorial", "exploratory",
]

# ─────────────────────────────────────────────────────────────────────────────
# Frontmatter schema
# ─────────────────────────────────────────────────────────────────────────────
# Required fields every published quest must carry. ``layout`` and ``author``
# are typically supplied by _config.yml collection defaults, so validators
# should treat a config-default as satisfying the requirement.
REQUIRED_FIELDS = [
    "title", "description", "date", "level", "difficulty",
    "estimated_time", "quest_type", "permalink", "layout",
    "fmContentType", "keywords", "author",
]

# Recommended-but-optional scalar fields.
OPTIONAL_FIELDS = [
    "lastmod", "categories", "tags", "excerpt", "sub_title", "preview",
    "primary_technology", "skill_focus", "learning_style", "quest_series",
    "draft", "comments",
]

# Structured-optional fields with one canonical shape each.
PREREQUISITES_KEYS = ["knowledge_requirements", "system_requirements", "skill_level_indicators"]
REWARDS_KEYS = ["badges", "skills_unlocked", "progression_points", "unlocks_features"]
QUEST_DEPENDENCIES_KEYS = ["required_quests", "recommended_quests", "unlocks_quests"]

# Fields retired from the canonical schema (migrate then drop). Kept here so the
# normalizer and validator know what to strip / migrate.
RETIRED_FIELDS = [
    "quest_relationships", "quest_mapping", "learning_paths",
    "related_quests", "snippet", "sub-title",
]

# ─────────────────────────────────────────────────────────────────────────────
# Collection rules
# ─────────────────────────────────────────────────────────────────────────────
# Subdirectories under pages/_quests/ that never contain scored quests.
SKIP_SUBDIRS = {"templates", "docs", "inventory"}

# File stems (any directory) that are not quests.
SKIP_STEMS = {"home", "README", "QUEST_BUILD_PLAN", "NETWORK_REPORT"}

# ─────────────────────────────────────────────────────────────────────────────
# Regexes
# ─────────────────────────────────────────────────────────────────────────────
LEVEL_RE = re.compile(r"^[01]{4}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# estimated_time: "N minutes", "N-M minutes", "N hours", "N-M hours".
ESTIMATED_TIME_RE = re.compile(r"^\d+(?:-\d+)?\s+(?:minutes?|hours?)$")
# primary_technology: a slug starting with a letter (rejects corrupted numerics).
PRIMARY_TECH_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
PLACEHOLDER_MARKER = "Placeholder (Content to be developed)"
PLACEHOLDER_TOKEN_RE = re.compile(r"\[(?:technology|advanced topic|specific[^\]]*|real-world[^\]]*)\]", re.IGNORECASE)


# ─────────────────────────────────────────────────────────────────────────────
# Derived accessors
# ─────────────────────────────────────────────────────────────────────────────

def tier_of(level: str) -> str | None:
    """Return the tier name for a level code, or None if unknown."""
    meta = LEVELS.get(level)
    return meta["tier"] if meta else None


def tier_emoji_of(level: str) -> str:
    """Return the tier emoji for a level code (empty string if unknown)."""
    tier = tier_of(level)
    return TIER_EMOJI.get(tier, "") if tier else ""


def theme_of(level: str) -> str:
    return LEVELS.get(level, {}).get("theme", "Unknown")


def is_valid_level(level: str) -> bool:
    return level in LEVELS


# ─────────────────────────────────────────────────────────────────────────────
# Content-set predicates
# ─────────────────────────────────────────────────────────────────────────────

def is_quest(fm: dict) -> bool:
    """True if a frontmatter dict represents a playable quest page."""
    return isinstance(fm, dict) and fm.get("fmContentType") == "quest"


def is_draft(fm: dict) -> bool:
    """True if a quest is marked draft (draft: true)."""
    return bool(fm.get("draft")) is True and fm.get("draft") not in (False, "false", "False", None)


def is_scored(fm: dict) -> bool:
    """True if a quest should be quality-scored and gated (published quests)."""
    return is_quest(fm) and not is_draft(fm)


def has_placeholder_marker(body: str) -> bool:
    """True if a quest body still contains placeholder scaffolding."""
    if not body:
        return False
    return PLACEHOLDER_MARKER in body or bool(PLACEHOLDER_TOKEN_RE.search(body))


# ─────────────────────────────────────────────────────────────────────────────
# Routing helpers
# ─────────────────────────────────────────────────────────────────────────────

def canonical_level_permalink(level: str) -> str:
    """Return canonical permalink for a level hub: /quests/XXXX/"""
    return f"/quests/{level}/"


def canonical_quest_permalink(level: str, slug: str) -> str:
    """Return canonical permalink for a level quest: /quests/XXXX/slug/"""
    return f"/quests/{level}/{slug}/"


def canonical_permalink(slug: str, *, level: str | None = None,
                        quest_type: str = "main_quest",
                        content_type: str = "quest") -> str:
    """Return the canonical permalink for any quest-tree page.

    Routing model (side quests are flattened — no /side-quests/ segment):
        main_quest / side_quest / epic_quest  -> /quests/{level}/{slug}/
        bonus_quest                            -> /quests/codex/{slug}/
        fmContentType codex                    -> /quests/codex/{slug}/
        fmContentType documentation            -> /quests/docs/{slug}/
        fmContentType template                 -> /quests/templates/{slug}/
    """
    if content_type == "documentation":
        return f"/quests/docs/{slug}/"
    if content_type == "template":
        return f"/quests/templates/{slug}/"
    if content_type == "codex" or quest_type == "bonus_quest":
        return f"/quests/codex/{slug}/"
    if level and is_valid_level(level):
        return f"/quests/{level}/{slug}/"
    return f"/quests/{slug}/"


def slug_from_filename(filename: str) -> str:
    """Derive a URL slug from a quest markdown filename.

    Strips a leading date prefix (YYYY-MM-DD-) and the .md extension.
    """
    stem = filename[:-3] if filename.endswith(".md") else filename
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)


def slug_from_permalink(permalink: str) -> str:
    """Return the final slug segment of a permalink (no trailing slash)."""
    return permalink.strip("/").rsplit("/", 1)[-1]


def previous_level(level: str):
    idx = LEVEL_ORDER.index(level)
    return LEVEL_ORDER[idx - 1] if idx > 0 else None


def next_level(level: str):
    idx = LEVEL_ORDER.index(level)
    return LEVEL_ORDER[idx + 1] if idx < len(LEVEL_ORDER) - 1 else None


def level_title(level: str) -> str:
    """Return formatted title: 'Level XXXX - Theme Name'."""
    return f"Level {level} - {theme_of(level)}"


if __name__ == "__main__":
    print("Quest Registry — Level Metadata")
    print("=" * 60)
    for lvl in LEVEL_ORDER:
        meta = LEVELS[lvl]
        print(f"  {lvl} ({meta['decimal']:>2d}) | {TIER_EMOJI[meta['tier']]} {meta['tier']:<11s} "
              f"| {meta['xp_range']:>9s} | {meta['theme']}")
    print("=" * 60)
    print(f"Tiers: {', '.join(TIERS)} (no Legend tier — 1111 is Master)")
    print(f"Quest types: {', '.join(QUEST_TYPES)}")
    print(f"Difficulties: {', '.join(DIFFICULTIES)}")
    print(f"Required fields ({len(REQUIRED_FIELDS)}): {', '.join(REQUIRED_FIELDS)}")
