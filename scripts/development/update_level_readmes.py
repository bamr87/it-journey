#!/usr/bin/env python3
"""
Script to ensure all level README files in pages/_quests have consistent frontmatter:
- layout: quest-collection
- level: <dir>
- categories: quests

This script updates only README.md files in direct child directories of pages/_quests
where the directory name is a 4-digit binary string (e.g., 1100).
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUESTS_DIR = ROOT / 'pages' / '_quests'

LEVEL_DIR_RE = re.compile(r'^[01]{4}$')

def process_readme(path: Path, level: str):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        print(f"Skipping {path}: no frontmatter detected")
        return

    # Split header and body
    parts = text.split('---', 2)
    # parts[0] == '' if starts with '---'
    header = parts[1]
    body = parts[2] if len(parts) > 2 else ''

    # Parse header into lines
    lines = [l.rstrip('\n') for l in header.split('\n')]

    # Check for keys
    has_layout = any(re.match(r'\s*layout\s*:', l) for l in lines)
    has_level = any(re.match(r'\s*level\s*:', l) for l in lines)
    has_categories = any(re.match(r'\s*categories\s*:', l) for l in lines)

    new_lines = lines.copy()
    appended = False
    if not has_layout:
        new_lines.append(f'layout: quest-collection')
        appended = True
    if not has_level:
        new_lines.append(f'level: {level}')
        appended = True
    if not has_categories:
        new_lines.append('categories: quests')
        appended = True

    if appended:
        new_header = '\n'.join(new_lines)
        new_text = '---\n' + new_header + '\n---' + body
        path.write_text(new_text, encoding='utf-8')
        print(f"Updated frontmatter for {path}")
    else:
        print(f"No changes for {path}")


def main():
    if not QUESTS_DIR.exists():
        print("Quests directory not found at:", QUESTS_DIR)
        return

    for entry in QUESTS_DIR.iterdir():
        if entry.is_dir() and LEVEL_DIR_RE.match(entry.name):
            readme = entry / 'README.md'
            if readme.exists():
                process_readme(readme, entry.name)
            else:
                print(f"Skipping {entry}: README.md not present")

if __name__ == '__main__':
    main()
