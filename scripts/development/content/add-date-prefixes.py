#!/usr/bin/env python3
"""
Utility script to add date prefixes to Jekyll posts that are missing them.

This script scans all markdown files in the _posts subdirectories and renames them
to include the YYYY-MM-DD prefix required by Jekyll, extracting dates from frontmatter.

Usage:
    python add-date-prefixes.py [--dry-run] [--posts-dir PATH]

Requirements:
    - pyyaml: pip install pyyaml
"""

import argparse
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install it with: pip install pyyaml")
    sys.exit(1)


class DatePrefixAdder:
    """Adds date prefixes to Jekyll posts that are missing them."""
    
    def __init__(self, posts_dir: str, dry_run: bool = False):
        self.posts_dir = Path(posts_dir)
        self.dry_run = dry_run
        self.processed_files = []
        self.skipped_files = []
        self.error_files = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('add-date-prefixes.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def extract_frontmatter(self, file_path: Path) -> Optional[Dict]:
        """Extract YAML frontmatter from a markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file starts with frontmatter
            if not content.startswith('---'):
                return None
            
            # Find the end of frontmatter
            frontmatter_end = content.find('\n---\n', 3)
            if frontmatter_end == -1:
                return None
            
            frontmatter_content = content[3:frontmatter_end]
            return yaml.safe_load(frontmatter_content)
            
        except Exception as e:
            self.logger.error(f"Error reading frontmatter from {file_path}: {e}")
            return None
    
    def extract_date_from_frontmatter(self, frontmatter: Dict) -> Optional[str]:
        """Extract date from frontmatter and return as YYYY-MM-DD format."""
        date_fields = ['date', 'created', 'published']
        
        for field in date_fields:
            if field in frontmatter and frontmatter[field]:
                date_value = frontmatter[field]
                try:
                    if isinstance(date_value, str):
                        # Parse various date formats
                        if 'T' in date_value:  # ISO format
                            date_obj = datetime.fromisoformat(date_value.replace('Z', '+00:00').split('T')[0])
                        elif ' ' in date_value:  # Space-separated format
                            date_obj = datetime.strptime(date_value.split(' ')[0], '%Y-%m-%d')
                        else:
                            date_obj = datetime.strptime(date_value, '%Y-%m-%d')
                        return date_obj.strftime('%Y-%m-%d')
                    elif hasattr(date_value, 'strftime'):  # datetime object
                        return date_value.strftime('%Y-%m-%d')
                except Exception as e:
                    self.logger.warning(f"Error parsing date {date_value}: {e}")
                    continue
        
        return None
    
    def needs_date_prefix(self, filename: str) -> bool:
        """Check if filename already has a date prefix."""
        date_pattern = r'^\d{4}-\d{2}-\d{2}-'
        return not re.match(date_pattern, filename)
    
    def create_new_filename(self, original_filename: str, date_prefix: str) -> str:
        """Create new filename with date prefix."""
        # Remove extension for processing
        name_without_ext = Path(original_filename).stem
        extension = Path(original_filename).suffix
        
        # Create new filename with date prefix
        new_filename = f"{date_prefix}-{name_without_ext}{extension}"
        return new_filename
    
    def rename_file(self, source_path: Path, new_filename: str) -> bool:
        """Rename a file with the new filename."""
        target_path = source_path.parent / new_filename
        
        try:
            if target_path.exists():
                self.logger.warning(f"Target file already exists: {target_path}")
                return False
            
            if not self.dry_run:
                source_path.rename(target_path)
                self.logger.info(f"Renamed: {source_path.name} -> {new_filename}")
            else:
                self.logger.info(f"[DRY RUN] Would rename: {source_path.name} -> {new_filename}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error renaming file {source_path} to {new_filename}: {e}")
            return False
    
    def process_file(self, file_path: Path) -> None:
        """Process a single markdown file."""
        filename = file_path.name
        
        # Skip if already has date prefix
        if not self.needs_date_prefix(filename):
            self.skipped_files.append({
                'file': filename,
                'reason': 'Already has date prefix'
            })
            return
        
        self.logger.info(f"Processing: {filename}")
        
        # Extract frontmatter
        frontmatter = self.extract_frontmatter(file_path)
        if not frontmatter:
            self.skipped_files.append({
                'file': filename,
                'reason': 'No valid frontmatter found'
            })
            self.logger.warning(f"Skipped {filename}: No valid frontmatter")
            return
        
        # Extract date from frontmatter
        date_prefix = self.extract_date_from_frontmatter(frontmatter)
        if not date_prefix:
            # Use current date as fallback
            date_prefix = datetime.now().strftime('%Y-%m-%d')
            self.logger.warning(f"No date found in frontmatter for {filename}, using current date: {date_prefix}")
        
        # Create new filename
        new_filename = self.create_new_filename(filename, date_prefix)
        
        # Rename the file
        if self.rename_file(file_path, new_filename):
            self.processed_files.append({
                'original': filename,
                'new': new_filename,
                'date': date_prefix,
                'path': str(file_path.parent.relative_to(self.posts_dir))
            })
    
    def process_directory(self, directory: Path) -> None:
        """Process all markdown files in a directory."""
        if not directory.is_dir():
            return
        
        # Find all markdown files in this directory
        md_files = list(directory.glob('*.md'))
        
        if md_files:
            self.logger.info(f"Processing directory: {directory.relative_to(self.posts_dir)}")
            self.logger.info(f"Found {len(md_files)} markdown files")
        
        for md_file in md_files:
            try:
                self.process_file(md_file)
            except Exception as e:
                self.error_files.append({
                    'file': md_file.name,
                    'error': str(e),
                    'path': str(md_file.parent.relative_to(self.posts_dir))
                })
                self.logger.error(f"Error processing {md_file.name}: {e}")
    
    def add_date_prefixes(self) -> None:
        """Main method to add date prefixes to all posts."""
        self.logger.info(f"Starting date prefix addition in: {self.posts_dir}")
        self.logger.info(f"Dry run mode: {self.dry_run}")
        
        # Check if posts directory exists
        if not self.posts_dir.exists():
            self.logger.error(f"Posts directory does not exist: {self.posts_dir}")
            return
        
        # Process root directory files first
        self.process_directory(self.posts_dir)
        
        # Process all subdirectories
        for item in self.posts_dir.iterdir():
            if item.is_dir():
                self.process_directory(item)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print a summary of the process."""
        self.logger.info("\n" + "="*60)
        self.logger.info("DATE PREFIX ADDITION SUMMARY")
        self.logger.info("="*60)
        
        self.logger.info(f"Successfully processed: {len(self.processed_files)} files")
        for file_info in self.processed_files:
            path_info = f" (in {file_info['path']})" if file_info['path'] else ""
            self.logger.info(f"  ✓ {file_info['original']} -> {file_info['new']}{path_info}")
            self.logger.info(f"    Date: {file_info['date']}")
        
        if self.skipped_files:
            self.logger.info(f"\nSkipped: {len(self.skipped_files)} files")
            for skipped in self.skipped_files:
                self.logger.info(f"  ⚠ {skipped['file']}: {skipped['reason']}")
        
        if self.error_files:
            self.logger.info(f"\nErrors: {len(self.error_files)} files")
            for error in self.error_files:
                path_info = f" (in {error['path']})" if error['path'] else ""
                self.logger.info(f"  ✗ {error['file']}: {error['error']}{path_info}")
        
        self.logger.info("="*60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Add date prefixes to Jekyll posts based on frontmatter"
    )
    parser.add_argument(
        '--posts-dir',
        default='pages/_posts',
        help='Path to the posts directory (default: pages/_posts)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually renaming files'
    )
    
    args = parser.parse_args()
    
    # Convert to absolute path if relative
    posts_dir = Path(args.posts_dir)
    if not posts_dir.is_absolute():
        posts_dir = Path.cwd() / posts_dir
    
    adder = DatePrefixAdder(
        posts_dir=str(posts_dir),
        dry_run=args.dry_run
    )
    
    adder.add_date_prefixes()


if __name__ == "__main__":
    main()