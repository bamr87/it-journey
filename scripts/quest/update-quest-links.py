#!/usr/bin/env python3
"""
update-quest-links.py

Update all quest links across documentation files (home.md, README.md, level READMEs).
Parses all quest files, extracts permalinks and relationships, and updates documentation.
"""

import re
import sys
from collections import defaultdict
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
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def print_info(msg):
    print(f"{BLUE}[INFO]{NC} {msg}")


def print_success(msg):
    print(f"{GREEN}[SUCCESS]{NC} {msg}")


def print_warning(msg):
    print(f"{YELLOW}[WARNING]{NC} {msg}")


def print_error(msg):
    print(f"{RED}[ERROR]{NC} {msg}")


class QuestLinkUpdater:
    def __init__(self, quest_dir: str):
        self.quest_dir = Path(quest_dir)
        self.quests: Dict[str, Dict] = {}
        self.level_quests: Dict[str, List[str]] = defaultdict(list)
        self.updated_files: List[Path] = []

    def extract_frontmatter(self, file_path: Path) -> Tuple[Dict, str]:
        """Extract YAML frontmatter from markdown file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            print_warning(f"Could not read {file_path}: {e}")
            return {}, ""

        # Match frontmatter between --- delimiters
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
        if not match:
            return {}, content

        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter or {}, body
        except yaml.YAMLError as e:
            print_warning(f"YAML parsing error in {file_path}: {e}")
            return {}, content

    def scan_quests(self):
        """Scan all quest markdown files and extract metadata."""
        print_info("Scanning quest files...")

        def process_quest_file(md_file):
            """Process a single quest file and store its data"""
            try:
                # Skip templates, READMEs, and certain meta files
                skip_patterns = [
                    "templates/",
                    "README.md",
                    "home.md",
                    "QUEST_BUILD_PLAN.md",
                    "PHASE",
                    "VALIDATION",
                    "docs/",
                    "codex/",
                    "inventory/",
                ]
                if any(skip in str(md_file) for skip in skip_patterns):
                    return

                frontmatter, body = self.extract_frontmatter(md_file)

                if not frontmatter:
                    return

                # Store quest data
                permalink = frontmatter.get("permalink", "")
                title = frontmatter.get("title", "")
                level = frontmatter.get("level", "")

                if not permalink:
                    return

                self.quests[permalink] = {
                    "file_path": md_file,
                    "title": title,
                    "level": level,
                    "frontmatter": frontmatter,
                }

                # Group by level
                if level:
                    self.level_quests[level].append(permalink)

            except Exception as e:
                print_warning(f"Skipping file {md_file}: {e}")

        # Scan quest files
        try:
            for md_file in self.quest_dir.rglob("*.md"):
                process_quest_file(md_file)
        except Exception as e:
            print_error(f"Error during scan: {e}")

        print_success(
            f"Found {len(self.quests)} quests across {len(self.level_quests)} levels"
        )

    def generate_level_quest_table(self, level: str) -> str:
        """Generate a markdown table of quests for a level."""
        if level not in self.level_quests:
            return ""

        quests = self.level_quests[level]
        if not quests:
            return ""

        # Build table header
        table = "| Quest | Difficulty | Time | Type | Status |\n"
        table += "|-------|------------|------|------|--------|\n"

        for permalink in sorted(quests):
            quest_data = self.quests[permalink]
            frontmatter = quest_data["frontmatter"]
            title = quest_data["title"]

            difficulty = frontmatter.get("difficulty", "N/A")
            estimated_time = frontmatter.get("estimated_time", "N/A")
            quest_type = frontmatter.get("quest_type", "N/A")
            draft = frontmatter.get("draft", True)
            status = "🔮 Placeholder" if draft else "✅ Complete"

            # Create link
            link_text = title if title else permalink
            link = f"[{link_text}]({permalink})"

            table += f"| {link} | {difficulty} | {estimated_time} | {quest_type} | {status} |\n"

        return table

    def update_level_readme(self, level: str, readme_path: Path):
        """Update a level README with quest listings."""
        if not readme_path.exists():
            print_warning(f"README not found: {readme_path}")
            return False

        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print_error(f"Could not read {readme_path}: {e}")
            return False

        # Generate quest table
        quest_table = self.generate_level_quest_table(level)

        if not quest_table:
            return False

        # Look for existing quest table section and replace it
        # Pattern: ## Available Quests or ## Quests section
        pattern = r"(##\s+(?:Available\s+)?Quests[^\n]*\n.*?)(?=\n##|\Z)"

        replacement = f"## Available Quests\n\n{quest_table}\n"

        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            content = re.sub(
                pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE
            )
        else:
            # Append if section doesn't exist
            content += f"\n\n{replacement}\n"

        # Write back
        try:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.updated_files.append(readme_path)
            return True
        except Exception as e:
            print_error(f"Could not write {readme_path}: {e}")
            return False

    def update_all_level_readmes(self):
        """Update all level README files."""
        print_info("Updating level README files...")

        updated_count = 0
        for level in sorted(self.level_quests.keys()):
            level_dir = self.quest_dir / level
            readme_path = level_dir / "README.md"

            if readme_path.exists():
                if self.update_level_readme(level, readme_path):
                    updated_count += 1
                    print_success(f"Updated {readme_path}")
                else:
                    print_warning(f"Could not update {readme_path}")

        print_success(f"Updated {updated_count} level README files")

    def generate_quest_summary(self) -> str:
        """Generate a summary of all quests for main README."""
        summary = "## Quest System Overview\n\n"
        summary += f"Total Quests: **{len(self.quests)}**\n\n"

        summary += "### Quest Distribution by Level\n\n"
        summary += "| Level | Quests | Theme |\n"
        summary += "|-------|--------|-------|\n"

        # Level themes mapping
        themes = {
            "0000": "Foundation",
            "0001": "Web Fundamentals",
            "0010": "Terminal Mastery",
            "0011": "AI-Assisted Dev",
            "0100": "Containers & Frontend",
            "0101": "CI/CD & DevOps",
            "0110": "Database Mastery",
            "0111": "API Development",
            "1000": "Cloud Computing",
            "1001": "Kubernetes",
            "1010": "Monitoring",
            "1011": "Security",
            "1100": "Data Engineering",
            "1101": "Machine Learning",
            "1110": "Architecture",
            "1111": "Leadership",
        }

        for level in sorted(self.level_quests.keys()):
            count = len(self.level_quests[level])
            theme = themes.get(level, "Unknown")
            summary += f"| {level} | {count} | {theme} |\n"

        return summary

    def update_main_readme(self, readme_path: Path):
        """Update main quest README with quest summary."""
        if not readme_path.exists():
            print_warning(f"Main README not found: {readme_path}")
            return False

        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print_error(f"Could not read {readme_path}: {e}")
            return False

        # Generate summary
        summary = self.generate_quest_summary()

        # Look for existing quest system overview section
        pattern = r"(##\s+Quest\s+System\s+Overview[^\n]*\n.*?)(?=\n##|\Z)"

        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            content = re.sub(pattern, summary, content, flags=re.DOTALL | re.IGNORECASE)
        else:
            # Append if section doesn't exist
            content += f"\n\n{summary}\n"

        # Write back
        try:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.updated_files.append(readme_path)
            return True
        except Exception as e:
            print_error(f"Could not write {readme_path}: {e}")
            return False

    def run(self, dry_run: bool = False):
        """Run the link updater."""
        self.scan_quests()

        if dry_run:
            print_info("=== DRY RUN - No files will be modified ===")
            print_info(f"Would update {len(self.level_quests)} level READMEs")
            print_info("Would update main README")
            return 0

        # Update level READMEs
        self.update_all_level_readmes()

        # Update main README
        main_readme = self.quest_dir / "README.md"
        if main_readme.exists():
            if self.update_main_readme(main_readme):
                print_success(f"Updated main README: {main_readme}")

        # Summary
        print()
        print("=" * 80)
        print_success(f"Updated {len(self.updated_files)} file(s)")
        print("=" * 80)

        return 0


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Update quest links across documentation files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without making changes",
    )
    parser.add_argument(
        "--quest-dir", type=str, help="Path to quest directory (default: pages/_quests)"
    )

    args = parser.parse_args()

    # Get quest directory
    if args.quest_dir:
        quest_dir = Path(args.quest_dir)
    else:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent
        quest_dir = project_root / "pages" / "_quests"

    if not quest_dir.exists():
        print_error(f"Quest directory not found: {quest_dir}")
        return 1

        print_info("Quest directory: " + str(quest_dir))
    print()

    # Run updater
    updater = QuestLinkUpdater(str(quest_dir))
    return updater.run(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
