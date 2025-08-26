#!/usr/bin/env python3
"""
Utility script to organize markdown files in _posts based on frontmatter data.

This script scans all markdown files in the _posts directory and archives them 
into subfolders based on the 'section' frontmatter variable. Files are renamed
to use only the slug value from the frontmatter.

Usage:
    python organize-posts.py [--dry-run] [--posts-dir PATH] [--config-file PATH]

Requirements:
    - pyyaml: pip install pyyaml
"""

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install it with: pip install pyyaml")
    sys.exit(1)


class PostOrganizer:
    """Organizes Jekyll/markdown posts based on frontmatter metadata."""
    
    def __init__(self, posts_dir: str, config_file: str = None, dry_run: bool = False):
        self.posts_dir = Path(posts_dir)
        self.config_file = config_file
        self.dry_run = dry_run
        self.valid_sections: Set[str] = set()
        self.processed_files: List[str] = []
        self.skipped_files: List[Dict] = []
        self.error_files: List[Dict] = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('post-organization.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_valid_sections(self) -> None:
        """Load valid sections from posts.yml configuration file."""
        if not self.config_file:
            # Default sections based on the posts.yml we examined
            self.valid_sections = {
                'technology', 'tech', 'business', 'world', 'home'
            }
            self.logger.info(f"Using default sections: {self.valid_sections}")
            return
        
        try:
            config_path = Path(self.config_file)
            if not config_path.exists():
                self.logger.warning(f"Config file {self.config_file} not found, using defaults")
                self.valid_sections = {'technology', 'tech', 'business', 'world', 'home'}
                return
            
            with open(config_path, 'r', encoding='utf-8') as f:
                posts_config = yaml.safe_load(f)
            
            # Extract section names from posts.yml structure
            for item in posts_config:
                if isinstance(item, dict) and 'title' in item:
                    section_name = item['title'].lower().replace(' ', '-')
                    self.valid_sections.add(section_name)
                    # Also add the exact title
                    self.valid_sections.add(item['title'].lower())
            
            self.logger.info(f"Loaded {len(self.valid_sections)} valid sections from config")
            
        except Exception as e:
            self.logger.error(f"Error loading config file: {e}")
            self.valid_sections = {'technology', 'tech', 'business', 'world', 'home'}
    
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
    
    def extract_slug(self, frontmatter: Dict, filename: str) -> Optional[str]:
        """Extract slug from frontmatter or generate from filename/title."""
        # Try to get slug from permalink first
        if 'permalink' in frontmatter and frontmatter['permalink']:
            permalink = frontmatter['permalink']
            # Extract the last part of the permalink as slug
            slug = Path(permalink).name
            if slug and slug != '/':
                return slug
        
        # Try to get slug from explicit slug field
        if 'slug' in frontmatter and frontmatter['slug']:
            return frontmatter['slug']
        
        # Generate slug from title
        if 'title' in frontmatter and frontmatter['title']:
            title = frontmatter['title']
            # Convert title to slug format
            slug = re.sub(r'[^\w\s-]', '', title.lower())
            slug = re.sub(r'[-\s]+', '-', slug)
            return slug.strip('-')
        
        # Fallback: use filename without date prefix and extension
        # Remove date prefix (YYYY-MM-DD-) if present
        base_name = Path(filename).stem
        date_pattern = r'^\d{4}-\d{2}-\d{2}-'
        slug = re.sub(date_pattern, '', base_name)
        return slug if slug else None
    
    def get_section(self, frontmatter: Dict) -> Optional[str]:
        """Get the section from frontmatter."""
        if 'section' not in frontmatter:
            return None
        
        section = frontmatter['section']
        if not section:
            return None
        
        # Normalize section name
        section = section.lower().strip()
        
        # Check if it's a valid section
        if section in self.valid_sections:
            return section
        
        # Try variations
        section_variations = [
            section,
            section.replace(' ', '-'),
            section.replace('-', ' '),
            section.replace('_', '-'),
            section.replace('_', ' ')
        ]
        
        for variation in section_variations:
            if variation in self.valid_sections:
                return variation
        
        return None
    
    def create_target_directory(self, section: str) -> Path:
        """Create the target directory for the section."""
        target_dir = self.posts_dir / section
        
        if not self.dry_run:
            target_dir.mkdir(exist_ok=True)
            self.logger.info(f"Created/verified directory: {target_dir}")
        else:
            self.logger.info(f"[DRY RUN] Would create directory: {target_dir}")
        
        return target_dir
    
    def move_file(self, source_path: Path, target_path: Path) -> bool:
        """Move a file from source to target location."""
        try:
            if target_path.exists():
                self.logger.warning(f"Target file already exists: {target_path}")
                return False
            
            if not self.dry_run:
                source_path.rename(target_path)
                self.logger.info(f"Moved: {source_path.name} -> {target_path}")
            else:
                self.logger.info(f"[DRY RUN] Would move: {source_path.name} -> {target_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error moving file {source_path} to {target_path}: {e}")
            return False
    
    def process_file(self, file_path: Path) -> None:
        """Process a single markdown file."""
        self.logger.info(f"Processing: {file_path.name}")
        
        # Extract frontmatter
        frontmatter = self.extract_frontmatter(file_path)
        if not frontmatter:
            self.skipped_files.append({
                'file': file_path.name,
                'reason': 'No valid frontmatter found'
            })
            self.logger.warning(f"Skipped {file_path.name}: No valid frontmatter")
            return
        
        # Get section
        section = self.get_section(frontmatter)
        if not section:
            self.skipped_files.append({
                'file': file_path.name,
                'reason': 'No valid section found in frontmatter',
                'section_value': frontmatter.get('section', 'None')
            })
            self.logger.warning(f"Skipped {file_path.name}: No valid section")
            return
        
        # Get slug
        slug = self.extract_slug(frontmatter, file_path.name)
        if not slug:
            self.skipped_files.append({
                'file': file_path.name,
                'reason': 'Could not determine slug'
            })
            self.logger.warning(f"Skipped {file_path.name}: Could not determine slug")
            return
        
        # Create target directory
        target_dir = self.create_target_directory(section)
        
        # Ensure slug has .md extension
        if not slug.endswith('.md'):
            slug += '.md'
        
        target_path = target_dir / slug
        
        # Move the file
        if self.move_file(file_path, target_path):
            self.processed_files.append(f"{file_path.name} -> {section}/{slug}")
    
    def organize_posts(self) -> None:
        """Main method to organize all posts."""
        self.logger.info(f"Starting post organization in: {self.posts_dir}")
        self.logger.info(f"Dry run mode: {self.dry_run}")
        
        # Load valid sections
        self.load_valid_sections()
        
        # Check if posts directory exists
        if not self.posts_dir.exists():
            self.logger.error(f"Posts directory does not exist: {self.posts_dir}")
            return
        
        # Find all markdown files
        md_files = list(self.posts_dir.glob('*.md'))
        self.logger.info(f"Found {len(md_files)} markdown files to process")
        
        # Process each file
        for md_file in md_files:
            # Skip if it's already in a subdirectory
            if md_file.parent != self.posts_dir:
                continue
                
            try:
                self.process_file(md_file)
            except Exception as e:
                self.error_files.append({
                    'file': md_file.name,
                    'error': str(e)
                })
                self.logger.error(f"Error processing {md_file.name}: {e}")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print a summary of the organization process."""
        self.logger.info("\n" + "="*60)
        self.logger.info("POST ORGANIZATION SUMMARY")
        self.logger.info("="*60)
        
        self.logger.info(f"Successfully processed: {len(self.processed_files)} files")
        for file_move in self.processed_files:
            self.logger.info(f"  ✓ {file_move}")
        
        if self.skipped_files:
            self.logger.info(f"\nSkipped: {len(self.skipped_files)} files")
            for skipped in self.skipped_files:
                self.logger.info(f"  ⚠ {skipped['file']}: {skipped['reason']}")
                if 'section_value' in skipped:
                    self.logger.info(f"    Section value: '{skipped['section_value']}'")
        
        if self.error_files:
            self.logger.info(f"\nErrors: {len(self.error_files)} files")
            for error in self.error_files:
                self.logger.info(f"  ✗ {error['file']}: {error['error']}")
        
        self.logger.info(f"\nValid sections: {sorted(self.valid_sections)}")
        self.logger.info("="*60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Organize Jekyll posts based on frontmatter metadata"
    )
    parser.add_argument(
        '--posts-dir',
        default='pages/_posts',
        help='Path to the posts directory (default: pages/_posts)'
    )
    parser.add_argument(
        '--config-file',
        help='Path to posts.yml configuration file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually moving files'
    )
    
    args = parser.parse_args()
    
    # Convert to absolute path if relative
    posts_dir = Path(args.posts_dir)
    if not posts_dir.is_absolute():
        posts_dir = Path.cwd() / posts_dir
    
    organizer = PostOrganizer(
        posts_dir=str(posts_dir),
        config_file=args.config_file,
        dry_run=args.dry_run
    )
    
    organizer.organize_posts()


if __name__ == "__main__":
    main()
