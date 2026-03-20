#!/usr/bin/env python3
"""
quest_registry.py — Single source of truth for quest level metadata.

All quest management scripts import from this module to ensure
consistent level names, themes, ordering, and permalink formats.
"""

# Ordered list of all binary level codes
LEVEL_ORDER = [
    "0000", "0001", "0010", "0011",
    "0100", "0101", "0110", "0111",
    "1000", "1001", "1010", "1011",
    "1100", "1101", "1110", "1111",
]

# Tier groupings
TIERS = {
    "Apprentice": ["0000", "0001", "0010", "0011"],
    "Adventurer": ["0100", "0101", "0110", "0111"],
    "Warrior":    ["1000", "1001", "1010", "1011"],
    "Master":     ["1100", "1101", "1110", "1111"],
}

# Canonical level metadata
LEVELS = {
    "0000": {"theme": "Foundation & Init World",            "tier": "Apprentice", "decimal": 0,  "xp_range": "0-250"},
    "0001": {"theme": "Web Fundamentals",                   "tier": "Apprentice", "decimal": 1,  "xp_range": "250-500"},
    "0010": {"theme": "Terminal Mastery",                    "tier": "Apprentice", "decimal": 2,  "xp_range": "500-750"},
    "0011": {"theme": "AI-Assisted Development",            "tier": "Apprentice", "decimal": 3,  "xp_range": "750-1000"},
    "0100": {"theme": "Frontend & Containers",              "tier": "Adventurer", "decimal": 4,  "xp_range": "1000-1500"},
    "0101": {"theme": "CI/CD & DevOps",                     "tier": "Adventurer", "decimal": 5,  "xp_range": "1500-2000"},
    "0110": {"theme": "Database Mastery",                   "tier": "Adventurer", "decimal": 6,  "xp_range": "2000-2500"},
    "0111": {"theme": "API Development",                    "tier": "Adventurer", "decimal": 7,  "xp_range": "2500-3000"},
    "1000": {"theme": "Cloud Computing",                    "tier": "Warrior",    "decimal": 8,  "xp_range": "3000-3500"},
    "1001": {"theme": "Kubernetes Orchestration",           "tier": "Warrior",    "decimal": 9,  "xp_range": "3500-4000"},
    "1010": {"theme": "Monitoring & Observability",         "tier": "Warrior",    "decimal": 10, "xp_range": "4000-4500"},
    "1011": {"theme": "Security & Compliance",              "tier": "Warrior",    "decimal": 11, "xp_range": "4500-5000"},
    "1100": {"theme": "Data Engineering",                   "tier": "Master",     "decimal": 12, "xp_range": "5000-6000"},
    "1101": {"theme": "Machine Learning & AI",              "tier": "Master",     "decimal": 13, "xp_range": "6000-7000"},
    "1110": {"theme": "Architecture & Design Patterns",     "tier": "Master",     "decimal": 14, "xp_range": "7000-8000"},
    "1111": {"theme": "Leadership & Innovation",            "tier": "Master",     "decimal": 15, "xp_range": "8000+"},
}

# Tier emoji prefixes
TIER_EMOJI = {
    "Apprentice": "🌱",
    "Adventurer": "⚔️",
    "Warrior":    "🔥",
    "Master":     "⚡",
}


def canonical_level_permalink(level: str) -> str:
    """Return canonical permalink for a level README: /quests/XXXX/"""
    return f"/quests/{level}/"


def canonical_quest_permalink(level: str, slug: str) -> str:
    """Return canonical permalink for a quest: /quests/XXXX/slug/"""
    return f"/quests/{level}/{slug}/"


def slug_from_filename(filename: str) -> str:
    """Derive a URL slug from a quest markdown filename.

    Strips leading date prefixes (YYYY-MM-DD-) and the .md extension.
    """
    import re
    stem = filename.replace(".md", "")
    # Strip date prefix if present
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
    return stem


def previous_level(level: str):
    """Return the previous level code, or None if this is the first level."""
    idx = LEVEL_ORDER.index(level)
    return LEVEL_ORDER[idx - 1] if idx > 0 else None


def next_level(level: str):
    """Return the next level code, or None if this is the last level."""
    idx = LEVEL_ORDER.index(level)
    return LEVEL_ORDER[idx + 1] if idx < len(LEVEL_ORDER) - 1 else None


def level_title(level: str) -> str:
    """Return formatted title: 'Level XXXX - Theme Name'"""
    meta = LEVELS.get(level, {})
    theme = meta.get("theme", "Unknown")
    return f"Level {level} - {theme}"


if __name__ == "__main__":
    print("Quest Registry — Level Metadata")
    print("=" * 50)
    for lvl in LEVEL_ORDER:
        meta = LEVELS[lvl]
        print(f"  {lvl} ({meta['decimal']:>2d}) | {meta['tier']:<11s} | {meta['theme']}")
