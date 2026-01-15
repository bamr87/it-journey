#!/usr/bin/env python3
"""
Phase 6 Quest Frontmatter Fixer

This script fixes common frontmatter issues in quest files:
1. Removes placeholder dependencies (level-XXXX-prerequisite-quest, etc.)
2. Adds missing required fields with defaults
3. Normalizes level format to 4-digit binary
4. Standardizes quest_type and difficulty values

Usage:
    python scripts/fix-quest-frontmatter.py [--dry-run] [--verbose]
"""

import os
import re
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Quest directory
QUEST_DIR = Path(__file__).parent.parent / "pages" / "_quests"

# Valid values
VALID_QUEST_TYPES = ["main_quest", "side_quest", "epic_quest", "bonus_quest", "reference"]
VALID_DIFFICULTIES = ["🟢 Easy", "🟡 Medium", "🔴 Hard", "⚔️ Epic"]

# Placeholder patterns to remove
PLACEHOLDER_PATTERNS = [
    r"/quests/level-\d{4}-prerequisite-quest/?",
    r"/quests/level-\d{4}-helpful-quest/?",
    r"/quests/level-\d{4}-next-quest/?",
]


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, "", content
    
    # Find the closing ---
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return {}, "", content
    
    end_pos = end_match.start() + 3
    yaml_content = content[4:end_pos]
    body = content[end_pos + 5:]  # Skip the closing ---\n
    
    try:
        frontmatter = yaml.safe_load(yaml_content)
        if frontmatter is None:
            frontmatter = {}
        return frontmatter, yaml_content, body
    except yaml.YAMLError as e:
        print(f"  YAML parse error: {e}")
        return {}, yaml_content, body


def serialize_frontmatter(frontmatter: Dict[str, Any]) -> str:
    """Serialize frontmatter back to YAML string."""
    return yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False, width=1000)


def is_placeholder_dependency(dep: str) -> bool:
    """Check if a dependency is a placeholder that should be removed."""
    for pattern in PLACEHOLDER_PATTERNS:
        if re.match(pattern, dep):
            return True
    return False


def clean_dependencies(deps: List[str]) -> List[str]:
    """Remove placeholder dependencies from a list."""
    if not deps:
        return []
    return [d for d in deps if not is_placeholder_dependency(d)]


def get_default_difficulty(level: str) -> str:
    """Get default difficulty based on level."""
    if not level:
        return "🟡 Medium"
    
    # Convert to binary level
    level_str = str(level).zfill(4)
    level_num = int(level_str, 2) if level_str.isdigit() else 0
    
    if level_num <= 3:  # 0000-0011
        return "🟢 Easy"
    elif level_num <= 7:  # 0100-0111
        return "🟡 Medium"
    elif level_num <= 11:  # 1000-1011
        return "🔴 Hard"
    else:  # 1100-1111
        return "⚔️ Epic"


def get_default_estimated_time(difficulty: str) -> str:
    """Get default estimated time based on difficulty."""
    if "Easy" in difficulty:
        return "30-60 minutes"
    elif "Medium" in difficulty:
        return "1-2 hours"
    elif "Hard" in difficulty:
        return "2-4 hours"
    else:
        return "4-8 hours"


def fix_quest_file(filepath: Path, dry_run: bool = False, verbose: bool = False) -> Dict[str, Any]:
    """Fix frontmatter issues in a single quest file."""
    stats = {
        "file": str(filepath.relative_to(QUEST_DIR)),
        "changes": [],
        "errors": []
    }
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        stats["errors"].append(f"Read error: {e}")
        return stats
    
    frontmatter, original_yaml, body = parse_frontmatter(content)
    
    if not frontmatter:
        stats["errors"].append("No valid frontmatter found")
        return stats
    
    modified = False
    
    # 1. Fix quest_dependencies - remove placeholders
    if "quest_dependencies" in frontmatter:
        deps = frontmatter["quest_dependencies"]
        for dep_type in ["required_quests", "recommended_quests", "unlocks_quests"]:
            if dep_type in deps and deps[dep_type]:
                original = deps[dep_type]
                cleaned = clean_dependencies(original)
                if len(cleaned) != len(original):
                    removed = len(original) - len(cleaned)
                    stats["changes"].append(f"Removed {removed} placeholder(s) from {dep_type}")
                    if cleaned:
                        deps[dep_type] = cleaned
                    else:
                        deps[dep_type] = []
                    modified = True
    
    # 2. Add missing difficulty
    if "difficulty" not in frontmatter or not frontmatter["difficulty"]:
        level = frontmatter.get("level", "")
        default_diff = get_default_difficulty(str(level) if level else "")
        frontmatter["difficulty"] = default_diff
        stats["changes"].append(f"Added difficulty: {default_diff}")
        modified = True
    
    # 3. Normalize difficulty format
    elif frontmatter.get("difficulty"):
        diff = frontmatter["difficulty"]
        # Fix common issues
        if diff in ["easy", "Easy"]:
            frontmatter["difficulty"] = "🟢 Easy"
            stats["changes"].append("Normalized difficulty to '🟢 Easy'")
            modified = True
        elif diff in ["medium", "Medium"]:
            frontmatter["difficulty"] = "🟡 Medium"
            stats["changes"].append("Normalized difficulty to '🟡 Medium'")
            modified = True
        elif diff in ["hard", "Hard"]:
            frontmatter["difficulty"] = "🔴 Hard"
            stats["changes"].append("Normalized difficulty to '🔴 Hard'")
            modified = True
        elif diff in ["epic", "Epic"]:
            frontmatter["difficulty"] = "⚔️ Epic"
            stats["changes"].append("Normalized difficulty to '⚔️ Epic'")
            modified = True
    
    # 4. Add missing estimated_time
    if "estimated_time" not in frontmatter or not frontmatter["estimated_time"]:
        diff = frontmatter.get("difficulty", "🟡 Medium")
        default_time = get_default_estimated_time(diff)
        frontmatter["estimated_time"] = default_time
        stats["changes"].append(f"Added estimated_time: {default_time}")
        modified = True
    
    # 5. Add missing quest_type
    if "quest_type" not in frontmatter or not frontmatter["quest_type"]:
        # Infer from filename or title
        filename = filepath.stem.lower()
        title = frontmatter.get("title", "").lower()
        
        if "epic" in filename or "epic" in title:
            quest_type = "epic_quest"
        elif "side" in filename or "side" in title:
            quest_type = "side_quest"
        elif "bonus" in filename or "bonus" in title:
            quest_type = "bonus_quest"
        elif "reference" in filename or "reference" in title or "example" in filename:
            quest_type = "reference"
        else:
            quest_type = "main_quest"
        
        frontmatter["quest_type"] = quest_type
        stats["changes"].append(f"Added quest_type: {quest_type}")
        modified = True
    
    # 6. Normalize level format (should be 4-digit string)
    if "level" in frontmatter and frontmatter["level"]:
        level = frontmatter["level"]
        if isinstance(level, int):
            # Convert integer to 4-digit binary string
            frontmatter["level"] = format(level, '04b') if level < 16 else str(level).zfill(4)
            stats["changes"].append(f"Normalized level {level} to {frontmatter['level']}")
            modified = True
        elif isinstance(level, str) and len(level) < 4 and level.isdigit():
            frontmatter["level"] = level.zfill(4)
            stats["changes"].append(f"Padded level to {frontmatter['level']}")
            modified = True
    
    # 7. Add missing permalink
    if "permalink" not in frontmatter or not frontmatter["permalink"]:
        level = frontmatter.get("level", "0000")
        slug = filepath.stem
        frontmatter["permalink"] = f"/quests/level-{level}-{slug}/"
        stats["changes"].append(f"Added permalink: {frontmatter['permalink']}")
        modified = True
    
    # Write changes if modified
    if modified and not dry_run:
        try:
            new_yaml = serialize_frontmatter(frontmatter)
            new_content = f"---\n{new_yaml}---\n{body}"
            filepath.write_text(new_content, encoding='utf-8')
        except Exception as e:
            stats["errors"].append(f"Write error: {e}")
    
    return stats


def fix_all_quests(dry_run: bool = False, verbose: bool = False) -> None:
    """Fix all quest files in the quest directory."""
    print(f"{'DRY RUN: ' if dry_run else ''}Fixing quest frontmatter...")
    print(f"Quest directory: {QUEST_DIR}\n")
    
    # Find all quest markdown files
    quest_files = []
    for level_dir in QUEST_DIR.iterdir():
        if level_dir.is_dir() and re.match(r'^\d{4}$', level_dir.name):
            for quest_file in level_dir.glob("*.md"):
                if quest_file.name != "README.md":
                    quest_files.append(quest_file)
    
    print(f"Found {len(quest_files)} quest files\n")
    
    total_changes = 0
    total_errors = 0
    files_modified = 0
    
    for quest_file in sorted(quest_files):
        stats = fix_quest_file(quest_file, dry_run, verbose)
        
        if stats["changes"]:
            files_modified += 1
            total_changes += len(stats["changes"])
            if verbose:
                print(f"📝 {stats['file']}")
                for change in stats["changes"]:
                    print(f"   - {change}")
        
        if stats["errors"]:
            total_errors += len(stats["errors"])
            print(f"❌ {stats['file']}")
            for error in stats["errors"]:
                print(f"   - {error}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Files scanned:  {len(quest_files)}")
    print(f"Files modified: {files_modified}")
    print(f"Total changes:  {total_changes}")
    print(f"Total errors:   {total_errors}")
    
    if dry_run:
        print("\nNo files were modified (dry run mode)")
    else:
        print(f"\n✅ Applied {total_changes} fixes to {files_modified} files")


def main():
    parser = argparse.ArgumentParser(description="Fix quest frontmatter issues")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without modifying files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    args = parser.parse_args()
    
    fix_all_quests(dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()
