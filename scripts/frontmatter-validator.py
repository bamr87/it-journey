#!/usr/bin/env python3
"""
frontmatter-validator.py

IT-Journey Frontmatter Validation Tool
Validates YAML frontmatter across all content files for quality, SEO optimization,
and consistency with project standards.

Features:
- Multi-content type support (posts, quests, docs, notes)
- SEO field validation (description length, keywords)
- Required field checking by content type
- JSON report generation for automation
- Severity-based issue categorization

Author: IT-Journey Team
Created: 2025-12-20
Version: 1.0.0
"""

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Try to import yaml, provide helpful error if not available
try:
    import yaml
except ImportError:
    print("Error: PyYAML is required but not installed.")
    print("Install it with: pip3 install pyyaml")
    sys.exit(1)

# ANSI color codes for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color
    BOLD = '\033[1m'


def print_info(msg: str) -> None:
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")


def print_success(msg: str) -> None:
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")


def print_warning(msg: str) -> None:
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")


def print_error(msg: str) -> None:
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")


@dataclass
class ValidationIssue:
    """Represents a single validation issue"""
    severity: str  # 'error', 'warning', 'info'
    field: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class FileValidationResult:
    """Stores validation results for a single file"""
    file_path: str
    content_type: str  # posts, quests, docs, notes, other
    is_valid: bool = True
    issues: List[ValidationIssue] = field(default_factory=list)
    seo_score: int = 0
    max_seo_score: int = 100
    frontmatter_present: bool = True
    
    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.severity == 'error'])
    
    @property
    def warning_count(self) -> int:
        return len([i for i in self.issues if i.severity == 'warning'])
    
    @property
    def info_count(self) -> int:
        return len([i for i in self.issues if i.severity == 'info'])


@dataclass
class ValidationReport:
    """Aggregated validation report"""
    timestamp: str
    total_files: int = 0
    valid_files: int = 0
    invalid_files: int = 0
    total_errors: int = 0
    total_warnings: int = 0
    files_by_type: Dict[str, int] = field(default_factory=dict)
    results: List[FileValidationResult] = field(default_factory=list)
    average_seo_score: float = 0.0


class FrontmatterValidator:
    """Validates frontmatter across IT-Journey content files"""
    
    # Field requirements by content type
    REQUIRED_FIELDS = {
        'posts': ['title', 'description', 'date', 'categories'],
        'quests': ['title', 'description', 'level', 'difficulty', 'estimated_time', 
                   'permalink', 'categories'],
        'docs': ['title', 'description'],
        'notes': ['title'],
        'other': ['title']
    }
    
    # SEO-recommended fields (not required but contribute to SEO score)
    SEO_FIELDS = {
        'posts': ['keywords', 'tags', 'excerpt', 'author', 'lastmod', 'meta'],
        'quests': ['keywords', 'tags', 'excerpt', 'author', 'lastmod', 'preview'],
        'docs': ['keywords', 'tags', 'lastmod'],
        'notes': ['tags'],
        'other': ['tags']
    }
    
    # SEO constraints
    SEO_CONSTRAINTS = {
        'description_min': 50,
        'description_max': 160,
        'description_optimal_min': 120,
        'description_optimal_max': 155,
        'title_max': 60,
        'keywords_min': 3,
        'keywords_max': 10
    }
    
    # Directories to skip
    SKIP_DIRS = ['_site', 'node_modules', '.git', '__pycache__', 'templates', 
                 'ARCHIVE', 'work', 'test', 'TODO']
    
    # Files to skip
    SKIP_FILES = ['README.md', 'CHANGELOG.md', 'LICENSE', 'CONTRIBUTING.md',
                  'CODE_OF_CONDUCT.md', 'SECURITY.md']
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[FileValidationResult] = []
    
    def log(self, level: str, msg: str) -> None:
        """Log message if verbose mode is enabled"""
        if self.verbose:
            if level == 'info':
                print_info(msg)
            elif level == 'warning':
                print_warning(msg)
            elif level == 'error':
                print_error(msg)
    
    def detect_content_type(self, file_path: Path) -> str:
        """Detect content type from file path"""
        path_str = str(file_path).lower()
        
        if '_posts' in path_str or '/posts/' in path_str:
            return 'posts'
        elif '_quests' in path_str or '/quests/' in path_str:
            return 'quests'
        elif '_docs' in path_str or '/docs/' in path_str:
            return 'docs'
        elif '_notes' in path_str or '/notes/' in path_str:
            return 'notes'
        else:
            return 'other'
    
    def should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        # Skip specific filenames
        if file_path.name in self.SKIP_FILES:
            return True
        
        # Skip files in certain directories
        path_parts = file_path.parts
        for skip_dir in self.SKIP_DIRS:
            if skip_dir in path_parts:
                return True
        
        return False
    
    def extract_frontmatter(self, file_path: Path) -> Tuple[Optional[Dict], str, Optional[str]]:
        """
        Extract YAML frontmatter from markdown file.
        Returns: (frontmatter_dict, body_content, error_message)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, UnicodeDecodeError) as e:
            return None, '', f"Could not read file: {e}"
        
        # Match frontmatter between --- delimiters
        pattern = r'^---\s*\n(.*?)\n---\s*\n?(.*)'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            return None, content, "No frontmatter found (missing --- delimiters)"
        
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            if frontmatter is None:
                return None, body, "Empty frontmatter"
            return frontmatter, body, None
        except yaml.YAMLError as e:
            return None, content, f"YAML parsing error: {e}"
    
    def validate_required_fields(self, fm: Dict, content_type: str, result: FileValidationResult) -> None:
        """Validate that required fields are present and non-empty"""
        required = self.REQUIRED_FIELDS.get(content_type, self.REQUIRED_FIELDS['other'])
        
        for field_name in required:
            if field_name not in fm:
                result.issues.append(ValidationIssue(
                    severity='error',
                    field=field_name,
                    message=f"Missing required field: {field_name}",
                    suggestion=f"Add '{field_name}:' to frontmatter"
                ))
                result.is_valid = False
            elif fm[field_name] is None or (isinstance(fm[field_name], str) and not fm[field_name].strip()):
                result.issues.append(ValidationIssue(
                    severity='error',
                    field=field_name,
                    message=f"Required field is empty: {field_name}",
                    suggestion=f"Provide a value for '{field_name}'"
                ))
                result.is_valid = False
    
    def validate_seo_fields(self, fm: Dict, content_type: str, result: FileValidationResult) -> None:
        """Validate SEO fields and calculate SEO score"""
        seo_fields = self.SEO_FIELDS.get(content_type, self.SEO_FIELDS['other'])
        constraints = self.SEO_CONSTRAINTS
        
        score = 0
        max_score = 100
        
        # Description validation (40 points)
        description = fm.get('description', '')
        if description:
            desc_len = len(description)
            
            if desc_len < constraints['description_min']:
                result.issues.append(ValidationIssue(
                    severity='warning',
                    field='description',
                    message=f"Description too short ({desc_len} chars). Minimum: {constraints['description_min']}",
                    suggestion="Expand description with more detail about content and benefits"
                ))
                score += 10
            elif desc_len > constraints['description_max']:
                result.issues.append(ValidationIssue(
                    severity='warning',
                    field='description',
                    message=f"Description too long ({desc_len} chars). May be truncated in search results. Max: {constraints['description_max']}",
                    suggestion="Shorten description to under 160 characters"
                ))
                score += 25
            elif constraints['description_optimal_min'] <= desc_len <= constraints['description_optimal_max']:
                score += 40  # Optimal length
                result.issues.append(ValidationIssue(
                    severity='info',
                    field='description',
                    message=f"Description length optimal ({desc_len} chars)",
                    suggestion=None
                ))
            else:
                score += 30  # Good but not optimal
        else:
            result.issues.append(ValidationIssue(
                severity='error',
                field='description',
                message="Missing description - critical for SEO",
                suggestion="Add a compelling 120-155 character description"
            ))
        
        # Title validation (20 points)
        title = fm.get('title', '')
        if title:
            title_len = len(title)
            if title_len > constraints['title_max']:
                result.issues.append(ValidationIssue(
                    severity='warning',
                    field='title',
                    message=f"Title may be truncated in search ({title_len} chars). Max: {constraints['title_max']}",
                    suggestion="Consider shortening title"
                ))
                score += 10
            else:
                score += 20
        
        # Keywords validation (20 points)
        keywords = fm.get('keywords', [])
        if keywords:
            if isinstance(keywords, list):
                kw_count = len(keywords)
                if kw_count < constraints['keywords_min']:
                    result.issues.append(ValidationIssue(
                        severity='warning',
                        field='keywords',
                        message=f"Too few keywords ({kw_count}). Recommended: {constraints['keywords_min']}-{constraints['keywords_max']}",
                        suggestion="Add more relevant keywords"
                    ))
                    score += 10
                elif kw_count > constraints['keywords_max']:
                    result.issues.append(ValidationIssue(
                        severity='info',
                        field='keywords',
                        message=f"Many keywords ({kw_count}). Consider focusing on top {constraints['keywords_max']}",
                        suggestion=None
                    ))
                    score += 15
                else:
                    score += 20
            else:
                result.issues.append(ValidationIssue(
                    severity='warning',
                    field='keywords',
                    message="Keywords should be a list/array",
                    suggestion="Format as: keywords:\\n  - keyword1\\n  - keyword2"
                ))
        else:
            result.issues.append(ValidationIssue(
                severity='warning',
                field='keywords',
                message="Missing keywords field",
                suggestion="Add keywords for better discoverability"
            ))
        
        # Tags validation (10 points)
        if 'tags' in seo_fields:
            tags = fm.get('tags', [])
            if tags and isinstance(tags, list) and len(tags) >= 2:
                score += 10
            elif tags:
                score += 5
                result.issues.append(ValidationIssue(
                    severity='info',
                    field='tags',
                    message="Consider adding more tags",
                    suggestion=None
                ))
            else:
                result.issues.append(ValidationIssue(
                    severity='info',
                    field='tags',
                    message="No tags defined",
                    suggestion="Add relevant tags for categorization"
                ))
        
        # Lastmod validation (5 points)
        if fm.get('lastmod'):
            score += 5
        else:
            result.issues.append(ValidationIssue(
                severity='info',
                field='lastmod',
                message="No lastmod date",
                suggestion="Add lastmod to indicate content freshness"
            ))
        
        # Author validation (5 points)
        if fm.get('author'):
            score += 5
        
        result.seo_score = score
        result.max_seo_score = max_score
    
    def validate_quest_specific(self, fm: Dict, result: FileValidationResult) -> None:
        """Additional validation for quest content"""
        # Level format validation (4-digit binary)
        level = fm.get('level', '')
        if level:
            level_str = str(level)
            if not re.match(r'^\d{4}$', level_str):
                result.issues.append(ValidationIssue(
                    severity='warning',
                    field='level',
                    message=f"Level format unusual: {level}. Expected: 4-digit (e.g., '0010')",
                    suggestion="Use 4-digit format for consistency"
                ))
        
        # Difficulty validation
        valid_difficulties = ['🟢 Easy', '🟡 Medium', '🔴 Hard', '⚔️ Epic',
                             'beginner', 'intermediate', 'advanced', 'expert']
        difficulty = fm.get('difficulty', '')
        if difficulty and str(difficulty).lower() not in [d.lower() for d in valid_difficulties]:
            result.issues.append(ValidationIssue(
                severity='info',
                field='difficulty',
                message=f"Non-standard difficulty: {difficulty}",
                suggestion=f"Consider using: {', '.join(valid_difficulties[:4])}"
            ))
        
        # Permalink validation
        permalink = fm.get('permalink', '')
        if permalink and not permalink.startswith('/quests/'):
            result.issues.append(ValidationIssue(
                severity='warning',
                field='permalink',
                message=f"Quest permalink should start with '/quests/': {permalink}",
                suggestion="Update permalink to follow quest URL structure"
            ))
    
    def validate_file(self, file_path: Path) -> FileValidationResult:
        """Validate a single file"""
        content_type = self.detect_content_type(file_path)
        result = FileValidationResult(
            file_path=str(file_path),
            content_type=content_type
        )
        
        # Extract frontmatter
        fm, body, error = self.extract_frontmatter(file_path)
        
        if error:
            result.frontmatter_present = False
            result.is_valid = False
            result.issues.append(ValidationIssue(
                severity='error',
                field='frontmatter',
                message=error,
                suggestion="Ensure file starts with --- followed by YAML and closing ---"
            ))
            return result
        
        # Validate required fields
        self.validate_required_fields(fm, content_type, result)
        
        # Validate SEO fields
        self.validate_seo_fields(fm, content_type, result)
        
        # Content-type specific validation
        if content_type == 'quests':
            self.validate_quest_specific(fm, result)
        
        return result
    
    def scan_directory(self, directory: Path) -> List[FileValidationResult]:
        """Scan directory for markdown files and validate"""
        results = []
        
        try:
            for md_file in directory.rglob('*.md'):
                if self.should_skip(md_file):
                    self.log('info', f"Skipping: {md_file}")
                    continue
                
                self.log('info', f"Validating: {md_file}")
                result = self.validate_file(md_file)
                results.append(result)
        except Exception as e:
            print_error(f"Error scanning directory: {e}")
        
        return results
    
    def generate_report(self, results: List[FileValidationResult]) -> ValidationReport:
        """Generate aggregated validation report"""
        report = ValidationReport(
            timestamp=datetime.now().isoformat(),
            total_files=len(results),
            results=results
        )
        
        files_by_type: Dict[str, int] = {}
        total_seo_score = 0
        seo_scored_files = 0
        
        for r in results:
            # Count by validity
            if r.is_valid:
                report.valid_files += 1
            else:
                report.invalid_files += 1
            
            # Count by type
            files_by_type[r.content_type] = files_by_type.get(r.content_type, 0) + 1
            
            # Aggregate errors/warnings
            report.total_errors += r.error_count
            report.total_warnings += r.warning_count
            
            # Calculate average SEO score
            if r.frontmatter_present:
                total_seo_score += r.seo_score
                seo_scored_files += 1
        
        report.files_by_type = files_by_type
        if seo_scored_files > 0:
            report.average_seo_score = round(total_seo_score / seo_scored_files, 1)
        
        return report
    
    def print_summary(self, report: ValidationReport) -> None:
        """Print human-readable summary"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.NC}")
        print(f"{Colors.BOLD}📊 Frontmatter Validation Report{Colors.NC}")
        print(f"{Colors.BOLD}{'='*60}{Colors.NC}\n")
        
        print(f"📅 Timestamp: {report.timestamp}")
        print(f"📁 Files Scanned: {report.total_files}")
        print()
        
        # Validity summary
        valid_pct = (report.valid_files / report.total_files * 100) if report.total_files > 0 else 0
        print(f"{Colors.GREEN}✅ Valid Files: {report.valid_files}{Colors.NC}")
        print(f"{Colors.RED}❌ Invalid Files: {report.invalid_files}{Colors.NC}")
        print(f"📈 Validity Rate: {valid_pct:.1f}%")
        print()
        
        # Issue summary
        print(f"{Colors.RED}🚨 Total Errors: {report.total_errors}{Colors.NC}")
        print(f"{Colors.YELLOW}⚠️  Total Warnings: {report.total_warnings}{Colors.NC}")
        print()
        
        # SEO score
        print(f"🔍 Average SEO Score: {report.average_seo_score}/100")
        print()
        
        # Files by type
        print(f"{Colors.BOLD}📂 Files by Type:{Colors.NC}")
        for content_type, count in sorted(report.files_by_type.items()):
            print(f"   {content_type}: {count}")
        print()
        
        # Show top issues (files with most errors)
        problem_files = [r for r in report.results if r.error_count > 0]
        if problem_files:
            print(f"{Colors.BOLD}🔴 Files Requiring Attention:{Colors.NC}")
            problem_files.sort(key=lambda x: x.error_count, reverse=True)
            for r in problem_files[:10]:  # Top 10
                rel_path = Path(r.file_path).name
                print(f"   {Colors.RED}❌{Colors.NC} {rel_path}: {r.error_count} errors, {r.warning_count} warnings")
        else:
            print(f"{Colors.GREEN}✅ No files with errors!{Colors.NC}")
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.NC}\n")
    
    def save_json_report(self, report: ValidationReport, output_path: Path) -> None:
        """Save report as JSON"""
        # Convert dataclasses to dicts for JSON serialization
        report_dict = {
            'timestamp': report.timestamp,
            'summary': {
                'total_files': report.total_files,
                'valid_files': report.valid_files,
                'invalid_files': report.invalid_files,
                'total_errors': report.total_errors,
                'total_warnings': report.total_warnings,
                'average_seo_score': report.average_seo_score,
                'files_by_type': report.files_by_type
            },
            'files': []
        }
        
        for r in report.results:
            file_dict = {
                'file_path': r.file_path,
                'content_type': r.content_type,
                'is_valid': r.is_valid,
                'frontmatter_present': r.frontmatter_present,
                'seo_score': r.seo_score,
                'error_count': r.error_count,
                'warning_count': r.warning_count,
                'issues': [asdict(i) for i in r.issues]
            }
            report_dict['files'].append(file_dict)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2)
        
        print_success(f"JSON report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Validate frontmatter across IT-Journey content files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s pages/                    # Validate all files in pages/
  %(prog)s pages/_posts/ -v          # Verbose validation of posts
  %(prog)s pages/_quests/ -o report.json   # Save JSON report
  %(prog)s . --errors-only           # Show only files with errors
        """
    )
    
    parser.add_argument(
        'path',
        type=str,
        help='Directory or file to validate'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output JSON report to file'
    )
    
    parser.add_argument(
        '--errors-only',
        action='store_true',
        help='Only show files with errors'
    )
    
    parser.add_argument(
        '--type',
        type=str,
        choices=['posts', 'quests', 'docs', 'notes', 'all'],
        default='all',
        help='Filter by content type'
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = FrontmatterValidator(verbose=args.verbose)
    
    # Validate path
    target_path = Path(args.path)
    if not target_path.exists():
        print_error(f"Path does not exist: {target_path}")
        sys.exit(1)
    
    # Run validation
    print_info(f"Starting frontmatter validation: {target_path}")
    
    if target_path.is_file():
        results = [validator.validate_file(target_path)]
    else:
        results = validator.scan_directory(target_path)
    
    # Filter by content type if specified
    if args.type != 'all':
        results = [r for r in results if r.content_type == args.type]
    
    # Filter errors-only if specified
    if args.errors_only:
        results = [r for r in results if r.error_count > 0]
    
    # Generate report
    report = validator.generate_report(results)
    
    # Print summary
    validator.print_summary(report)
    
    # Save JSON report if requested
    if args.output:
        output_path = Path(args.output)
        validator.save_json_report(report, output_path)
    
    # Exit with error code if issues found
    if report.invalid_files > 0:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
