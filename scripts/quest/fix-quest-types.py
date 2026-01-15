#!/usr/bin/env python3
"""
fix-quest-types.py

Standardizes quest_type values in quest frontmatter.
Replaces invalid quest_type values with valid ones.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Try to import yaml, provide helpful error if not available
try:
    import yaml
except ImportError:
    print("Error: PyYAML is required but not installed.")
    print("Install it with: pip3 install pyyaml")
    sys.exit(1)

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

def print_info(msg): print(f"{BLUE}[INFO]{NC} {msg}")
def print_success(msg): print(f"{GREEN}[SUCCESS]{NC} {msg}")
def print_warning(msg): print(f"{YELLOW}[WARNING]{NC} {msg}")
def print_error(msg): print(f"{RED}[ERROR]{NC} {msg}")

# Valid quest types
VALID_QUEST_TYPES = ['main_quest', 'side_quest', 'bonus_quest', 'epic_quest', 'reference', 'documentation']

# Replacement mappings for invalid quest types
REPLACEMENTS = {
    'Integration Mastery': 'main_quest',
    'language-learning': 'side_quest',
    'tool-mastery': 'main_quest',
    'main': 'main_quest',
    'Project Building': 'main_quest',
    'documentation': 'documentation',
    'reference': 'reference',
}

class QuestTypeFixer:
    def __init__(self, quest_dir: str):
        self.quest_dir = Path(quest_dir)
        self.fixed_files: List[Path] = []
        self.stats = {
            'scanned': 0,
            'fixed': 0,
            'skipped': 0
        }
    
    def extract_frontmatter(self, file_path: Path) -> Tuple[Dict, str]:
        """Extract YAML frontmatter from markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print_warning(f"Could not read {file_path}: {e}")
            return {}, ""
        
        # Match frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if not match:
            return {}, content
        
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter or {}, body
        except yaml.YAMLError as e:
            print_warning(f"YAML parsing error in {file_path}: {e}")
            return {}, content
    
    def fix_quest_type(self, file_path: Path, dry_run: bool = False) -> bool:
        """Fix quest_type in a single file."""
        self.stats['scanned'] += 1
        
        # Skip certain files
        skip_patterns = ['templates/', 'README.md', 'home.md', 'QUEST_BUILD_PLAN.md', 
                        'PHASE', 'VALIDATION', 'docs/', 'codex/', 'inventory/']
        if any(skip in str(file_path) for skip in skip_patterns):
            return False
        
        frontmatter, body = self.extract_frontmatter(file_path)
        
        if not frontmatter:
            return False
        
        quest_type = frontmatter.get('quest_type', '')
        
        if not quest_type:
            return False
        
        # Check if quest_type is valid
        if quest_type in VALID_QUEST_TYPES:
            return False
        
        # Check if we have a replacement
        if quest_type not in REPLACEMENTS:
            print_warning(f"Unknown quest_type '{quest_type}' in {file_path} - no replacement defined")
            self.stats['skipped'] += 1
            return False
        
        replacement = REPLACEMENTS[quest_type]
        
        if dry_run:
            print_info(f"Would fix {file_path}: '{quest_type}' -> '{replacement}'")
            return True
        
        # Read full file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print_error(f"Could not read {file_path}: {e}")
            return False
        
        # Replace quest_type value
        # Pattern: quest_type: "old_value" or quest_type: 'old_value' or quest_type: old_value
        patterns = [
            (rf'quest_type:\s*["\']?{re.escape(quest_type)}["\']?', f'quest_type: {replacement}'),
            (rf'quest_type:\s*["\']?{re.escape(quest_type)}["\']?', f'quest_type: "{replacement}"'),
        ]
        
        modified = False
        for pattern, replacement_str in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement_str, content)
                modified = True
                break
        
        if modified:
            # Write back
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_files.append(file_path)
                self.stats['fixed'] += 1
                print_success(f"Fixed {file_path}: '{quest_type}' -> '{replacement}'")
                return True
            except Exception as e:
                print_error(f"Could not write {file_path}: {e}")
                return False
        
        return False
    
    def run(self, dry_run: bool = False):
        """Run the quest type fixer."""
        print_info("Scanning quest files for invalid quest_type values...")
        
        # Find all quest markdown files
        for md_file in self.quest_dir.rglob('*.md'):
            self.fix_quest_type(md_file, dry_run)
        
        # Summary
        print()
        print("=" * 80)
        print_info("=== Summary ===")
        print_info(f"Files scanned: {self.stats['scanned']}")
        print_info(f"Files fixed: {self.stats['fixed']}")
        print_info(f"Files skipped: {self.stats['skipped']}")
        
        if dry_run:
            print_info("Run without --dry-run to apply fixes")
        else:
            print_success(f"Fixed {len(self.fixed_files)} file(s)")
        
        print("=" * 80)
        
        return 0

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Fix invalid quest_type values in quest frontmatter'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fixed without making changes'
    )
    parser.add_argument(
        '--quest-dir',
        type=str,
        help='Path to quest directory (default: pages/_quests)'
    )
    
    args = parser.parse_args()
    
    # Get quest directory
    if args.quest_dir:
        quest_dir = Path(args.quest_dir)
    else:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent
        quest_dir = project_root / 'pages' / '_quests'
    
    if not quest_dir.exists():
        print_error(f"Quest directory not found: {quest_dir}")
        return 1
    
    print_info(f"Quest directory: {quest_dir}")
    print()
    
    # Run fixer
    fixer = QuestTypeFixer(str(quest_dir))
    return fixer.run(dry_run=args.dry_run)

if __name__ == '__main__':
    sys.exit(main())
