#!/usr/bin/env python3
"""
Preview Image Generator - AI-powered preview image generation for Jekyll content.

This module provides a Python-based interface for generating preview images
using various AI providers (OpenAI DALL-E, Stability AI, etc.).

Usage:
    python3 preview_generator.py --file path/to/post.md
    python3 preview_generator.py --collection posts --dry-run
    python3 preview_generator.py --list-missing

Dependencies:
    pip install openai pyyaml requests pillow

Environment Variables:
    OPENAI_API_KEY - Required for OpenAI provider
    STABILITY_API_KEY - Required for Stability AI provider
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Any
import yaml

# Optional imports with fallback
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class ContentFile:
    """Represents a Jekyll content file with its metadata."""
    path: Path
    title: str
    description: str
    categories: List[str]
    tags: List[str]
    preview: Optional[str]
    content: str
    front_matter: Dict[str, Any]


@dataclass
class GenerationResult:
    """Result of an image generation attempt."""
    success: bool
    image_path: Optional[str]
    preview_url: Optional[str]
    error: Optional[str]
    prompt_used: Optional[str]


class Colors:
    """Terminal colors for output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    PURPLE = '\033[0;35m'
    NC = '\033[0m'  # No Color


def log(msg: str, level: str = "info"):
    """Print formatted log message."""
    colors = {
        "info": Colors.BLUE,
        "success": Colors.GREEN,
        "warning": Colors.YELLOW,
        "error": Colors.RED,
        "debug": Colors.PURPLE,
        "step": Colors.CYAN,
    }
    color = colors.get(level, Colors.NC)
    prefix = f"[{level.upper()}]"
    print(f"{color}{prefix}{Colors.NC} {msg}")


class PreviewGenerator:
    """AI-powered preview image generator for Jekyll content."""
    
    def __init__(
        self,
        project_root: Path,
        provider: str = "openai",
        output_dir: str = "assets/images/previews",
        image_style: str = "digital art, professional blog illustration",
        image_size: str = "1024x1024",
        dry_run: bool = False,
        verbose: bool = False,
        force: bool = False,
    ):
        self.project_root = project_root
        self.provider = provider
        self.output_dir = project_root / output_dir
        self.image_style = image_style
        self.image_size = image_size
        self.dry_run = dry_run
        self.verbose = verbose
        self.force = force
        
        # Statistics
        self.processed = 0
        self.generated = 0
        self.skipped = 0
        self.errors = 0
        
        # Ensure output directory exists
        if not dry_run:
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def debug(self, msg: str):
        """Print debug message if verbose mode is enabled."""
        if self.verbose:
            log(msg, "debug")
    
    def parse_front_matter(self, file_path: Path) -> Optional[ContentFile]:
        """Parse front matter and content from a markdown file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            log(f"Failed to read {file_path}: {e}", "error")
            return None
        
        # Extract front matter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if not fm_match:
            self.debug(f"No front matter found in: {file_path}")
            return None
        
        try:
            front_matter = yaml.safe_load(fm_match.group(1))
            post_content = fm_match.group(2)
        except yaml.YAMLError as e:
            log(f"Failed to parse YAML in {file_path}: {e}", "error")
            return None
        
        if not front_matter:
            return None
        
        # Extract fields with defaults
        categories = front_matter.get('categories', [])
        if isinstance(categories, str):
            categories = [categories]
        
        tags = front_matter.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        return ContentFile(
            path=file_path,
            title=front_matter.get('title', ''),
            description=front_matter.get('description', ''),
            categories=categories,
            tags=tags,
            preview=front_matter.get('preview'),
            content=post_content,
            front_matter=front_matter,
        )
    
    def check_preview_exists(self, preview_path: Optional[str]) -> bool:
        """Check if the preview image file exists."""
        if not preview_path:
            return False
        
        # Handle absolute and relative paths
        clean_path = preview_path.lstrip('/')
        
        # Check direct path
        full_path = self.project_root / clean_path
        if full_path.exists():
            return True
        
        # Check in assets directory
        assets_path = self.project_root / 'assets' / clean_path
        if assets_path.exists():
            return True
        
        return False
    
    def generate_prompt(self, content: ContentFile) -> str:
        """Generate an AI prompt from content metadata."""
        prompt_parts = [
            f"Create a professional blog preview image for an article titled '{content.title}'."
        ]
        
        if content.description:
            prompt_parts.append(f"The article is about: {content.description}.")
        
        if content.categories:
            prompt_parts.append(f"Categories: {', '.join(content.categories)}.")
        
        if content.tags:
            prompt_parts.append(f"Tags: {', '.join(content.tags[:5])}.")  # Limit tags
        
        # Add content excerpt (first 500 chars)
        content_excerpt = content.content[:500].strip()
        if content_excerpt:
            # Remove markdown formatting
            clean_content = re.sub(r'[#*`\[\]()]', '', content_excerpt)
            clean_content = re.sub(r'\n+', ' ', clean_content)
            prompt_parts.append(f"Key themes: {clean_content}")
        
        # Add style instructions
        prompt_parts.extend([
            f"Style: {self.image_style}.",
            "The image should be suitable as a blog header/preview image.",
            "Clean composition, professional look, visually appealing.",
            "No text or letters in the image.",
        ])
        
        return ' '.join(prompt_parts)
    
    def generate_filename(self, title: str) -> str:
        """Generate a safe filename from title."""
        # Convert to lowercase and replace special chars
        safe_name = re.sub(r'[^a-z0-9]+', '-', title.lower())
        safe_name = re.sub(r'-+', '-', safe_name).strip('-')
        return safe_name[:50]  # Limit length
    
    def generate_image_openai(self, prompt: str, output_path: Path) -> GenerationResult:
        """Generate image using OpenAI DALL-E."""
        if not HAS_OPENAI:
            return GenerationResult(
                success=False,
                image_path=None,
                preview_url=None,
                error="openai package not installed. Run: pip install openai",
                prompt_used=prompt,
            )
        
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return GenerationResult(
                success=False,
                image_path=None,
                preview_url=None,
                error="OPENAI_API_KEY environment variable not set",
                prompt_used=prompt,
            )
        
        try:
            client = OpenAI(api_key=api_key)
            
            self.debug(f"Generating with prompt: {prompt[:200]}...")
            
            # Parse size
            size_map = {
                "1024x1024": "1024x1024",
                "1792x1024": "1792x1024",
                "1024x1792": "1024x1792",
            }
            size = size_map.get(self.image_size, "1024x1024")
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download image
            if not HAS_REQUESTS:
                return GenerationResult(
                    success=False,
                    image_path=None,
                    preview_url=image_url,
                    error="requests package not installed. Run: pip install requests",
                    prompt_used=prompt,
                )
            
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            output_path.write_bytes(img_response.content)
            
            return GenerationResult(
                success=True,
                image_path=str(output_path),
                preview_url=str(output_path.relative_to(self.project_root)),
                error=None,
                prompt_used=prompt,
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                image_path=None,
                preview_url=None,
                error=str(e),
                prompt_used=prompt,
            )
    
    def generate_image_stability(self, prompt: str, output_path: Path) -> GenerationResult:
        """Generate image using Stability AI."""
        if not HAS_REQUESTS:
            return GenerationResult(
                success=False,
                image_path=None,
                preview_url=None,
                error="requests package not installed",
                prompt_used=prompt,
            )
        
        api_key = os.environ.get('STABILITY_API_KEY')
        if not api_key:
            return GenerationResult(
                success=False,
                image_path=None,
                preview_url=None,
                error="STABILITY_API_KEY environment variable not set",
                prompt_used=prompt,
            )
        
        try:
            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "text_prompts": [{"text": prompt}],
                    "cfg_scale": 7,
                    "height": 1024,
                    "width": 1024,
                    "samples": 1,
                    "steps": 30,
                },
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'artifacts' not in data or not data['artifacts']:
                return GenerationResult(
                    success=False,
                    image_path=None,
                    preview_url=None,
                    error="No image data in response",
                    prompt_used=prompt,
                )
            
            import base64
            image_data = base64.b64decode(data['artifacts'][0]['base64'])
            output_path.write_bytes(image_data)
            
            return GenerationResult(
                success=True,
                image_path=str(output_path),
                preview_url=str(output_path.relative_to(self.project_root)),
                error=None,
                prompt_used=prompt,
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                image_path=None,
                preview_url=None,
                error=str(e),
                prompt_used=prompt,
            )
    
    def generate_image(self, prompt: str, output_path: Path) -> GenerationResult:
        """Generate image using configured provider."""
        if self.provider == "openai":
            return self.generate_image_openai(prompt, output_path)
        elif self.provider == "stability":
            return self.generate_image_stability(prompt, output_path)
        else:
            return GenerationResult(
                success=False,
                image_path=None,
                preview_url=None,
                error=f"Unknown provider: {self.provider}",
                prompt_used=prompt,
            )
    
    def update_front_matter(self, file_path: Path, preview_path: str) -> bool:
        """Update the front matter with new preview path."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check if preview field exists
            if re.search(r'^preview:', content, re.MULTILINE):
                # Update existing preview
                new_content = re.sub(
                    r'^preview:.*$',
                    f'preview: {preview_path}',
                    content,
                    flags=re.MULTILINE,
                )
            else:
                # Add preview after description or title
                if 'description:' in content:
                    new_content = re.sub(
                        r'(^description:.*$)',
                        f'\\1\npreview: {preview_path}',
                        content,
                        flags=re.MULTILINE,
                    )
                else:
                    new_content = re.sub(
                        r'(^title:.*$)',
                        f'\\1\npreview: {preview_path}',
                        content,
                        flags=re.MULTILINE,
                    )
            
            file_path.write_text(new_content, encoding='utf-8')
            return True
            
        except Exception as e:
            log(f"Failed to update front matter: {e}", "error")
            return False
    
    def process_file(self, file_path: Path, list_only: bool = False) -> bool:
        """Process a single content file."""
        self.processed += 1
        
        content = self.parse_front_matter(file_path)
        if not content:
            self.skipped += 1
            return False
        
        self.debug(f"Processing: {content.title}")
        
        # Check if preview exists
        if content.preview and self.check_preview_exists(content.preview):
            if not self.force:
                self.debug(f"Preview exists: {content.preview}")
                self.skipped += 1
                return True
            else:
                log(f"Force mode: regenerating preview for {content.title}", "info")
        
        # List only mode
        if list_only:
            print(f"{Colors.YELLOW}Missing preview:{Colors.NC} {file_path}")
            print(f"  Title: {content.title}")
            if content.preview:
                print(f"  Current preview (not found): {content.preview}")
            print()
            return True
        
        log(f"Generating preview for: {content.title}", "info")
        
        # Generate filename and paths
        safe_filename = self.generate_filename(content.title)
        output_file = self.output_dir / f"{safe_filename}.png"
        # Generate preview URL - relative path without leading slash, theme adds /assets/
        relative_path = str(self.output_dir.relative_to(self.project_root))
        if relative_path.startswith('assets/'):
            relative_path = relative_path[7:]  # Remove 'assets/' prefix
        preview_url = f"{relative_path}/{safe_filename}.png"  # No leading slash
        
        # Generate prompt
        prompt = self.generate_prompt(content)
        self.debug(f"Prompt: {prompt[:300]}...")
        
        # Dry run mode
        if self.dry_run:
            log(f"[DRY RUN] Would generate image:", "info")
            print(f"  Output: {output_file}")
            print(f"  Preview URL: {preview_url}")
            print(f"  Prompt: {prompt[:200]}...")
            print()
            self.generated += 1
            return True
        
        # Generate image
        result = self.generate_image(prompt, output_file)
        
        if result.success:
            # Update front matter
            if self.update_front_matter(file_path, preview_url):
                log(f"Updated front matter with: {preview_url}", "success")
                self.generated += 1
                return True
            else:
                self.errors += 1
                return False
        else:
            log(f"Failed to generate image: {result.error}", "warning")
            self.errors += 1
            return False
    
    def process_collection(self, collection_path: Path, list_only: bool = False):
        """Process all markdown files in a collection."""
        if not collection_path.exists():
            log(f"Collection not found: {collection_path}", "warning")
            return
        
        for md_file in collection_path.rglob("*.md"):
            self.process_file(md_file, list_only)
    
    def print_summary(self):
        """Print processing summary."""
        print()
        print(f"{Colors.CYAN}{'=' * 40}{Colors.NC}")
        print(f"{Colors.CYAN}📊 Summary{Colors.NC}")
        print(f"{Colors.CYAN}{'=' * 40}{Colors.NC}")
        print(f"  Files processed: {self.processed}")
        print(f"  Images generated: {self.generated}")
        print(f"  Files skipped: {self.skipped}")
        print(f"  Errors: {self.errors}")
        print()
        
        if self.dry_run:
            log("This was a dry run. No actual changes were made.", "info")
        
        if self.errors > 0:
            log("Some files had errors. Check the output above.", "warning")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI-powered preview image generator for Jekyll content"
    )
    parser.add_argument(
        '-f', '--file',
        help="Process a specific file only"
    )
    parser.add_argument(
        '-c', '--collection',
        choices=['posts', 'quickstart', 'docs', 'quests', 'all'],
        help="Process specific collection"
    )
    parser.add_argument(
        '-p', '--provider',
        choices=['openai', 'stability'],
        default='openai',
        help="AI provider for image generation"
    )
    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help="Preview without making changes"
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable verbose output"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help="Regenerate images even if preview exists"
    )
    parser.add_argument(
        '--list-missing',
        action='store_true',
        help="Only list files with missing previews"
    )
    parser.add_argument(
        '--output-dir',
        default='assets/images/previews',
        help="Output directory for generated images"
    )
    parser.add_argument(
        '--style',
        default='digital art, professional blog illustration, clean design',
        help="Image style prompt"
    )
    
    args = parser.parse_args()
    
    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    # Initialize generator
    generator = PreviewGenerator(
        project_root=project_root,
        provider=args.provider,
        output_dir=args.output_dir,
        image_style=args.style,
        dry_run=args.dry_run,
        verbose=args.verbose,
        force=args.force,
    )
    
    print(f"{Colors.BLUE}{'=' * 40}{Colors.NC}")
    print(f"{Colors.BLUE}🎨 Preview Image Generator{Colors.NC}")
    print(f"{Colors.BLUE}{'=' * 40}{Colors.NC}")
    print()
    
    log(f"Provider: {args.provider}", "info")
    log(f"Output Dir: {args.output_dir}", "info")
    log(f"Dry Run: {args.dry_run}", "info")
    print()
    
    # Process files
    if args.file:
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = project_root / file_path
        generator.process_file(file_path, args.list_missing)
    elif args.collection:
        collections = {
            'posts': project_root / 'pages' / '_posts',
            'quickstart': project_root / 'pages' / '_quickstart',
            'docs': project_root / 'pages' / '_docs',
            'quests': project_root / 'pages' / '_quests',
        }
        
        if args.collection == 'all':
            for name, path in collections.items():
                log(f"Processing {name}...", "step")
                generator.process_collection(path, args.list_missing)
        else:
            log(f"Processing {args.collection}...", "step")
            generator.process_collection(collections[args.collection], args.list_missing)
    else:
        # Default: process all
        collections = [
            project_root / 'pages' / '_posts',
            project_root / 'pages' / '_quickstart',
            project_root / 'pages' / '_docs',
        ]
        for collection in collections:
            log(f"Processing {collection.name}...", "step")
            generator.process_collection(collection, args.list_missing)
    
    generator.print_summary()
    
    return 0 if generator.errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
