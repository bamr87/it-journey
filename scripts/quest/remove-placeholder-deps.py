#!/usr/bin/env python3
"""
remove-placeholder-deps.py

Remove placeholder dependencies from quest frontmatter.
Properly handles YAML parsing to avoid breaking frontmatter structure.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List

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

# Placeholder patterns to remove
PLACEHOLDER_PATTERNS = [
    r'level-XXXX-side-quest-1',
    r'level-XXXX-side-quest-2',
    r'level-XXXX-alternative-path',
    r'level-XXXX-continuation',
    r'level-0000-side-quest-1',
    r'level-0000-side-quest-2',
    r'level-0001-side-quest-1',
    r'level-0001-side-quest-2',
    r'level-0010-side-quest-1',
    r'level-0010-side-quest-2',
    r'level-0011-side-quest-1',
    r'level-0011-side-quest-2',
]

class PlaceholderRemover:
    def __init__(self, quest_dir: str):
        self.quest_dir = Path(quest_dir)
        self.fixed_files: List[Path] = []
        self.stats = {
            'scanned': 0,
            'fixed': 0,
            'skipped': 0
        }
    
    def extract_frontmatter(self, file_path: Path) -> tuple:
        """Extract YAML frontmatter from markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print_warning(f"Could not read {file_path}: {e}")
            return None, None, None
        
        # Match frontmatter between --- delimiters
        match = re.match(r'^(---\s*\n)(.*?)(\n---\s*\n)(.*)', content, re.DOTALL)
        if not match:
            return None, None, content
        
        frontmatter_start = match.group(1)
        frontmatter_yaml = match.group(2)
        frontmatter_end = match.group(3)
        body = match.group(4)
        
        try:
            frontmatter = yaml.safe_load(frontmatter_yaml)
            return frontmatter or {}, frontmatter_yaml, body
        except yaml.YAMLError as e:
            print_warning(f"YAML parsing error in {file_path}: {e}")
            return None, None, content
    
    def remove_placeholders_from_list(self, items: List) -> List:
        """Remove placeholder items from a list."""
        if not isinstance(items, list):
            return items
        
        cleaned = []
        for item in items:
            if isinstance(item, str):
                # Check if item matches any placeholder pattern
                is_placeholder = any(re.search(pattern, item) for pattern in PLACEHOLDER_PATTERNS)
                if not is_placeholder:
                    cleaned.append(item)
            else:
                cleaned.append(item)
        
        return cleaned
    
    def clean_frontmatter(self, frontmatter: Dict) -> Dict:
        """Remove placeholder dependencies from frontmatter."""
        cleaned = frontmatter.copy()
        
        # Clean quest_dependencies
        if 'quest_dependencies' in cleaned:
            deps = cleaned['quest_dependencies']
            for key in ['required_quests', 'recommended_quests', 'unlocks_quests']:
                if key in deps and isinstance(deps[key], list):
                    deps[key] = self.remove_placeholders_from_list(deps[key])
        
        # Clean quest_relationships
        if 'quest_relationships' in cleaned:
            rels = cleaned['quest_relationships']
            for key in ['child_quests', 'parallel_quests', 'sequel_quests']:
                if key in rels and isinstance(rels[key], list):
                    rels[key] = self.remove_placeholders_from_list(rels[key])
            
            # Handle parent_quest (single value)
            if 'parent_quest' in rels:
                parent = rels['parent_quest']
                if isinstance(parent, str):
                    is_placeholder = any(re.search(pattern, parent) for pattern in PLACEHOLDER_PATTERNS)
                    if is_placeholder:
                        rels['parent_quest'] = None
        
        return cleaned
    
    def fix_file(self, file_path: Path, dry_run: bool = False) -> bool:
        """Fix placeholder dependencies in a single file."""
        self.stats['scanned'] += 1
        
        # Skip certain files
        skip_patterns = ['templates/', 'README.md', 'home.md', 'QUEST_BUILD_PLAN.md', 
                        'PHASE', 'VALIDATION', 'docs/', 'codex/', 'inventory/']
        if any(skip in str(file_path) for skip in skip_patterns):
            return False
        
        frontmatter, frontmatter_yaml, body = self.extract_frontmatter(file_path)
        
        if frontmatter is None:
            return False
        
        # Check if file has placeholder dependencies
        has_placeholders = False
        frontmatter_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, frontmatter_str):
                has_placeholders = True
                break
        
        if not has_placeholders:
            return False
        
        # Clean frontmatter
        cleaned_frontmatter = self.clean_frontmatter(frontmatter)
        
        if dry_run:
            print_info(f"Would remove placeholders from: {file_path}")
            return True
        
        # Reconstruct file
        try:
            cleaned_yaml = yaml.dump(cleaned_frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            # Preserve original YAML structure better by using the cleaned dict
            # Write back with proper formatting
            new_content = f"---\n{cleaned_yaml}---\n{body}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.fixed_files.append(file_path)
            self.stats['fixed'] += 1
            print_success(f"Removed placeholders from: {file_path}")
            return True
        except Exception as e:
            print_error(f"Could not write {file_path}: {e}")
            return False
    
    def run(self, dry_run: bool = False):
        """Run the placeholder remover."""
        print_info("Scanning quest files for placeholder dependencies...")
        
        # Find all quest markdown files
        for md_file in self.quest_dir.rglob('*.md'):
            self.fix_file(md_file, dry_run)
        
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
        description='Remove placeholder dependencies from quest frontmatter'
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
    
    # Run remover
    remover = PlaceholderRemover(str(quest_dir))
    return remover.run(dry_run=args.dry_run)

if __name__ == '__main__':
    sys.exit(main())
