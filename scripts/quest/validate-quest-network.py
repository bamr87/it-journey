#!/usr/bin/env python3
"""
validate-quest-network.py

Validates the quest network integrity across the IT-Journey quest system.
Checks for:
- Required frontmatter fields
- Quest dependencies exist
- No circular dependencies
- Orphaned quests
- Broken links
- Quest progression paths
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

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

class QuestValidator:
    def __init__(self, quest_dir: str):
        self.quest_dir = Path(quest_dir)
        self.quests: Dict[str, Dict] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats = {
            'total_quests': 0,
            'complete_quests': 0,
            'placeholder_quests': 0,
            'draft_quests': 0,
            'orphaned_quests': 0,
            'broken_dependencies': 0
        }
        
        # Required frontmatter fields
        self.required_fields = [
            'title', 'description', 'level', 'difficulty', 
            'estimated_time', 'quest_type', 'permalink'
        ]
    
    def extract_frontmatter(self, file_path: Path) -> Tuple[Dict, str]:
        """Extract YAML frontmatter from markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if not match:
            return {}, content
        
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter or {}, body
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error in {file_path}: {e}")
            return {}, content
    
    def scan_quests(self):
        """Scan all quest markdown files and extract metadata."""
        print_info("Scanning quest files...")
        
        def process_quest_file(md_file):
            """Process a single quest file and store its data"""
            try:
                # Skip templates, READMEs, and certain meta files
                if any(skip in str(md_file) for skip in ['templates/', 'README.md', 'home.md', 'QUEST_BUILD_PLAN.md', 'PHASE1_COMPLETE.md', '/docs/']):
                    return
                
                frontmatter, body = self.extract_frontmatter(md_file)
                
                if not frontmatter:
                    self.warnings.append(f"No frontmatter found in {md_file}")
                    return
                
                # Store quest data
                permalink = frontmatter.get('permalink', str(md_file))
                self.quests[permalink] = {
                    'file_path': md_file,
                    'frontmatter': frontmatter,
                    'body': body
                }
                
                self.stats['total_quests'] += 1
                
                # Track quest status
                if frontmatter.get('draft', True):
                    self.stats['draft_quests'] += 1
                
                if '🔮' in body or 'Placeholder' in body:
                    self.stats['placeholder_quests'] += 1
                else:
                    self.stats['complete_quests'] += 1
                    
            except (OSError, PermissionError) as e:
                print_warn(f"Skipping file {md_file}: {e}")
        
        try:
            # Try recursive scan first
            for md_file in self.quest_dir.rglob('*.md'):
                process_quest_file(md_file)
        except (OSError, PermissionError, FileNotFoundError) as e:
            print_error(f"Error during recursive scan: {e}")
            print_info("Falling back to manual directory traversal...")
            
            # Fallback: manually traverse directories
            def scan_directory(directory):
                """Recursively scan a directory, skipping problematic paths"""
                try:
                    for item in directory.iterdir():
                        if item.is_file() and item.suffix == '.md':
                            process_quest_file(item)
                        elif item.is_dir() and item.name not in ['templates', '__pycache__', '.git']:
                            # Recursively scan subdirectories
                            scan_directory(item)
                except (OSError, PermissionError) as e:
                    print_warn(f"Skipping directory {directory}: {e}")
            
            scan_directory(self.quest_dir)
        
        print_success(f"Found {self.stats['total_quests']} quests")
    
    def validate_frontmatter(self):
        """Validate required frontmatter fields."""
        print_info("Validating frontmatter...")
        
        for permalink, quest_data in self.quests.items():
            frontmatter = quest_data['frontmatter']
            file_path = quest_data['file_path']
            
            # Check required fields
            missing_fields = []
            for field in self.required_fields:
                if field not in frontmatter:
                    missing_fields.append(field)
            
            if missing_fields:
                self.errors.append(
                    f"{file_path}: Missing required fields: {', '.join(missing_fields)}"
                )
            
            # Validate level format (should be 4 binary digits)
            level = frontmatter.get('level', '')
            if level and not re.match(r'^[01]{4}$', str(level)):
                self.warnings.append(
                    f"{file_path}: Invalid level format '{level}' (should be 4 binary digits)"
                )
            
            # Validate difficulty format
            difficulty = frontmatter.get('difficulty', '')
            valid_difficulties = ['🟢 Easy', '🟡 Medium', '🔴 Hard', '⚔️ Epic']
            if difficulty and difficulty not in valid_difficulties:
                self.warnings.append(
                    f"{file_path}: Invalid difficulty '{difficulty}'"
                )
            
            # Validate quest_type
            quest_type = frontmatter.get('quest_type', '')
            valid_types = ['main_quest', 'side_quest', 'bonus_quest', 'epic_quest']
            if quest_type and quest_type not in valid_types:
                self.warnings.append(
                    f"{file_path}: Invalid quest_type '{quest_type}'"
                )
    
    def validate_dependencies(self):
        """Validate quest dependencies and relationships."""
        print_info("Validating quest dependencies...")
        
        for permalink, quest_data in self.quests.items():
            frontmatter = quest_data['frontmatter']
            file_path = quest_data['file_path']
            
            # Check quest_dependencies
            dependencies = frontmatter.get('quest_dependencies', {})
            
            for dep_type in ['required_quests', 'recommended_quests', 'unlocks_quests']:
                dep_list = dependencies.get(dep_type, [])
                for dep_permalink in dep_list:
                    if dep_permalink not in self.quests:
                        self.errors.append(
                            f"{file_path}: Dependency not found: {dep_permalink} ({dep_type})"
                        )
                        self.stats['broken_dependencies'] += 1
            
            # Check quest_relationships
            relationships = frontmatter.get('quest_relationships', {})
            
            for rel_type in ['parent_quest', 'child_quests', 'parallel_quests', 'sequel_quests']:
                rel_data = relationships.get(rel_type)
                
                if rel_data is None:
                    continue
                
                # Handle both single value and list
                rel_list = rel_data if isinstance(rel_data, list) else [rel_data]
                
                for rel_permalink in rel_list:
                    if rel_permalink and rel_permalink not in self.quests:
                        self.warnings.append(
                            f"{file_path}: Related quest not found: {rel_permalink} ({rel_type})"
                        )
    
    def detect_circular_dependencies(self):
        """Detect circular dependencies in quest progression."""
        print_info("Checking for circular dependencies...")
        
        def has_cycle(quest_permalink, visited, stack):
            visited.add(quest_permalink)
            stack.add(quest_permalink)
            
            quest_data = self.quests.get(quest_permalink, {})
            dependencies = quest_data.get('frontmatter', {}).get('quest_dependencies', {})
            
            for dep_list_key in ['required_quests', 'recommended_quests']:
                for dep in dependencies.get(dep_list_key, []):
                    if dep in self.quests:
                        if dep not in visited:
                            if has_cycle(dep, visited, stack):
                                return True
                        elif dep in stack:
                            self.errors.append(f"Circular dependency detected: {quest_permalink} -> {dep}")
                            return True
            
            stack.remove(quest_permalink)
            return False
        
        visited = set()
        for permalink in self.quests:
            if permalink not in visited:
                has_cycle(permalink, visited, set())
    
    def find_orphaned_quests(self):
        """Find quests that are not referenced by any other quest."""
        print_info("Finding orphaned quests...")
        
        referenced_quests = set()
        
        for quest_data in self.quests.values():
            frontmatter = quest_data['frontmatter']
            
            # Collect all references
            dependencies = frontmatter.get('quest_dependencies', {})
            for dep_list in dependencies.values():
                if isinstance(dep_list, list):
                    referenced_quests.update(dep_list)
            
            relationships = frontmatter.get('quest_relationships', {})
            for rel_data in relationships.values():
                if rel_data:
                    if isinstance(rel_data, list):
                        referenced_quests.update(rel_data)
                    else:
                        referenced_quests.add(rel_data)
        
        # Find orphans (excluding level 0000 quests which are entry points)
        for permalink, quest_data in self.quests.items():
            level = quest_data['frontmatter'].get('level', '')
            
            # Skip entry-level quests (0000) as they're expected to be starting points
            if level == '0000':
                continue
            
            if permalink not in referenced_quests:
                self.warnings.append(f"Orphaned quest (not referenced): {permalink}")
                self.stats['orphaned_quests'] += 1
    
    def generate_report(self):
        """Generate validation report."""
        print()
        print("=" * 80)
        print("QUEST NETWORK VALIDATION REPORT")
        print("=" * 80)
        print()
        
        # Statistics
        print("📊 Quest Statistics:")
        print(f"  Total Quests:       {self.stats['total_quests']}")
        print(f"  Complete Quests:    {self.stats['complete_quests']}")
        print(f"  Placeholder Quests: {self.stats['placeholder_quests']}")
        print(f"  Draft Quests:       {self.stats['draft_quests']}")
        print(f"  Orphaned Quests:    {self.stats['orphaned_quests']}")
        print(f"  Broken Dependencies: {self.stats['broken_dependencies']}")
        print()
        
        # Errors
        if self.errors:
            print_error(f"❌ {len(self.errors)} Error(s) Found:")
            for error in self.errors:
                print(f"  • {error}")
            print()
        else:
            print_success("✅ No errors found!")
            print()
        
        # Warnings
        if self.warnings:
            print_warning(f"⚠️  {len(self.warnings)} Warning(s):")
            for warning in self.warnings:
                print(f"  • {warning}")
            print()
        else:
            print_success("✅ No warnings!")
            print()
        
        # Overall result
        print("=" * 80)
        if not self.errors:
            print_success("VALIDATION PASSED ✅")
            return 0
        else:
            print_error("VALIDATION FAILED ❌")
            return 1
    
    def run(self):
        """Run all validation checks."""
        self.scan_quests()
        self.validate_frontmatter()
        self.validate_dependencies()
        self.detect_circular_dependencies()
        self.find_orphaned_quests()
        return self.generate_report()

def main():
    """Main entry point."""
    # Get quest directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    quest_dir = project_root / 'pages' / '_quests'
    
    if not quest_dir.exists():
        print_error(f"Quest directory not found: {quest_dir}")
        return 1
    
    print_info(f"Quest directory: {quest_dir}")
    print()
    
    # Run validator
    validator = QuestValidator(str(quest_dir))
    return validator.run()

if __name__ == '__main__':
    sys.exit(main())
