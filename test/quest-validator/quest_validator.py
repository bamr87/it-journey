#!/usr/bin/env python3
"""
Quest Validator - IT-Journey Quest Testing Framework
Validates quest structure, content, and quality standards

Author: IT-Journey Team
Created: 2025-10-08
Version: 2.0.0
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


@dataclass
class ValidationResult:
    """Stores validation results for a quest"""
    quest_file: str
    passed: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)
    score: int = 0
    max_score: int = 0

class QuestValidator:
    """Validates IT-Journey quest files against standards"""
    
    # Required frontmatter fields
    REQUIRED_FIELDS = [
        'title', 'description', 'date', 'level', 'difficulty',
        'estimated_time', 'primary_technology', 'quest_type',
        'skill_focus', 'learning_style', 'quest_series', 'author',
        'layout', 'keywords', 'permalink', 'fmContentType'
    ]
    
    # Enhanced quest hierarchy fields
    HIERARCHY_FIELDS = [
        'quest_line', 'quest_arc', 'prerequisites', 'quest_dependencies',
        'quest_relationships', 'learning_paths', 'rewards', 'validation_criteria'
    ]
    
    # Difficulty levels
    VALID_DIFFICULTIES = ['🟢 Easy', '🟡 Medium', '🔴 Hard', '⚔️ Epic']
    
    # Level format pattern (binary)
    LEVEL_PATTERN = re.compile(r'^\d{4}$')
    
    # Placeholder indicators in frontmatter values
    PLACEHOLDER_PATTERNS = [
        r'\[.*?\]',           # [Primary Skill Tree], [Your Name], etc.
        r'XXXX',              # Template level placeholder
        r'your-.*-here',      # your-quest-here, your-name-here
        r'Add .* here',       # Add quest description here
        r'TBD|TODO|FIXME',    # Common placeholder markers
        r'lorem ipsum',       # Lorem ipsum text
        r'placeholder',       # Explicit placeholder text
    ]

    def __init__(self, verbose: bool = False, exclude_drafts: bool = False, fail_threshold: int = 0):
        self.verbose = verbose
        self.exclude_drafts = exclude_drafts
        self.fail_threshold = fail_threshold
        self.results: List[ValidationResult] = []
    
    def log_info(self, message: str):
        """Log info message"""
        if self.verbose:
            print(f"ℹ️  {message}")
    
    def log_success(self, message: str):
        """Log success message"""
        print(f"✅ {message}")
    
    def log_warning(self, message: str):
        """Log warning message"""
        print(f"⚠️  {message}")
    
    def log_error(self, message: str):
        """Log error message"""
        print(f"❌ {message}")
    
    def extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Extract YAML frontmatter from markdown file"""
        # Match frontmatter between --- delimiters
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            return None, content
        
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter, body
        except yaml.YAMLError as e:
            self.log_error(f"YAML parsing error: {e}")
            return None, content
    
    def validate_frontmatter_required(self, fm: Dict, result: ValidationResult):
        """Validate required frontmatter fields"""
        self.log_info("Validating required frontmatter fields...")
        
        for field in self.REQUIRED_FIELDS:
            if field not in fm or not fm[field]:
                result.errors.append(f"Missing required field: {field}")
                result.passed = False
            else:
                result.score += 1
                result.max_score += 1
    
    def validate_frontmatter_hierarchy(self, fm: Dict, result: ValidationResult):
        """Validate enhanced quest hierarchy fields"""
        self.log_info("Validating quest hierarchy fields...")
        
        for field in self.HIERARCHY_FIELDS:
            if field in fm and fm[field]:
                result.score += 1
                result.info.append(f"Enhanced field present: {field}")
            else:
                result.warnings.append(f"Missing enhanced field: {field}")
            result.max_score += 1
    
    def validate_level_format(self, fm: Dict, result: ValidationResult):
        """Validate level format (binary)"""
        if 'level' not in fm:
            return
        
        level = str(fm['level'])
        if not self.LEVEL_PATTERN.match(level):
            result.errors.append(f"Invalid level format: {level}. Must be 4-digit binary (e.g., '0010')")
            result.passed = False
        else:
            result.score += 5
            decimal = int(level, 2)
            result.info.append(f"Level {level} (decimal: {decimal}) valid")
        result.max_score += 5
    
    def validate_difficulty(self, fm: Dict, result: ValidationResult):
        """Validate difficulty level"""
        if 'difficulty' not in fm:
            return
        
        difficulty = fm['difficulty']
        if difficulty not in self.VALID_DIFFICULTIES:
            result.errors.append(f"Invalid difficulty: {difficulty}. Must be one of {self.VALID_DIFFICULTIES}")
            result.passed = False
        else:
            result.score += 5
            result.info.append(f"Difficulty {difficulty} valid")
        result.max_score += 5
    
    def validate_estimated_time(self, fm: Dict, result: ValidationResult):
        """Validate estimated time format"""
        if 'estimated_time' not in fm:
            return
        
        time = fm['estimated_time']
        # Should match patterns like "30-60 minutes", "90-120 minutes", "1-2 hours"
        if not re.match(r'^\d+-\d+\s+(minutes|hours?)$', str(time)):
            result.warnings.append(f"Estimated time format unusual: {time}. Recommended: 'XX-XX minutes' or 'X-X hours'")
        else:
            result.score += 2
        result.max_score += 2
    
    def validate_permalink(self, fm: Dict, result: ValidationResult):
        """Validate permalink structure"""
        if 'permalink' not in fm or fm['permalink'] is None:
            return
        
        permalink = fm['permalink']
        level = str(fm.get('level', ''))
        
        # Must start with /quests/
        if not permalink.startswith('/quests/'):
            result.errors.append(f"Permalink should start with '/quests/': {permalink}")
            result.passed = False
        else:
            # Accept multiple valid permalink patterns:
            # 1. /quests/level-XXXX/slug/  (template style)
            # 2. /quests/{level_dir}/slug/ (e.g., /quests/0000/hello-noob/)
            # 3. /quests/{theme}/slug/     (e.g., /quests/init_world/hello-noob/)
            # 4. /quests/slug/             (standalone quests)
            # Check for broken patterns like ../README.md concatenation
            if '../' in permalink or 'README' in permalink:
                result.errors.append(f"Broken permalink (contains relative path or README): {permalink}")
                result.passed = False
            else:
                result.score += 5
                if level and f"level-{level}" not in permalink and f"/{level}/" not in permalink:
                    result.info.append(f"Permalink uses descriptive path (level {level}): {permalink}")
        result.max_score += 5
    
    def validate_content_structure(self, body: str, result: ValidationResult):
        """Validate quest content structure"""
        self.log_info("Validating content structure...")
        
        required_sections = [
            (r'##\s+🎯\s+Quest Objectives', 'Quest Objectives section'),
            (r'##\s+🗺️\s+Quest Prerequisites', 'Quest Prerequisites section (optional but recommended)'),
            (r'##\s+🌍\s+Choose Your Adventure Platform', 'Platform-specific instructions (optional)'),
        ]
        
        for pattern, description in required_sections:
            if re.search(pattern, body, re.IGNORECASE):
                result.score += 3
                result.info.append(f"Found: {description}")
            else:
                if 'optional' not in description.lower():
                    result.warnings.append(f"Missing recommended section: {description}")
            result.max_score += 3
    
    def validate_code_blocks(self, body: str, result: ValidationResult):
        """Validate code blocks have language specifications"""
        self.log_info("Validating code blocks...")
        
        # Find opening code fences only (not closing fences)
        # Handles nested fences: a fence opened with N backticks is only closed
        # by a line with >= N backticks and no language identifier.
        # Lines inside a higher-level fence are treated as content, not fences.
        lines = body.split('\n')
        fence_stack = []  # stack of backtick counts for nested fences
        total_blocks = 0
        unspecified_count = 0
        for line in lines:
            stripped = line.strip()
            # Match lines that are only backticks (3+) optionally followed by a language id
            m = re.match(r'^(`{3,})(.*)', stripped)
            if m:
                tick_count = len(m.group(1))
                lang = m.group(2).strip()
                if fence_stack and tick_count >= fence_stack[-1] and not lang:
                    # Closing fence: >= same backtick count and no language
                    fence_stack.pop()
                elif not fence_stack or tick_count < fence_stack[-1]:
                    # Opening fence at top level or nested inside a higher fence
                    if not fence_stack:
                        # Only count top-level fences for validation
                        total_blocks += 1
                        if not lang:
                            unspecified_count += 1
                    fence_stack.append(tick_count)
        
        if total_blocks > 0:
            if unspecified_count > 0:
                result.warnings.append(f"{unspecified_count} code blocks without language specification")
            else:
                result.score += 5
                result.info.append(f"All {total_blocks} code blocks have language specification")
            result.max_score += 5
    
    def validate_checkboxes(self, body: str, result: ValidationResult):
        """Validate presence of interactive checkboxes"""
        self.log_info("Validating interactive elements...")
        
        checkboxes = re.findall(r'- \[ \]', body)
        if checkboxes:
            result.score += 5
            result.info.append(f"Found {len(checkboxes)} interactive checkboxes for learner engagement")
        else:
            result.warnings.append("No interactive checkboxes found. Consider adding checklist items.")
        result.max_score += 5
    
    def validate_fantasy_theme(self, body: str, fm: Dict, result: ValidationResult):
        """Validate fantasy/gamification theme elements"""
        self.log_info("Validating fantasy theme integration...")
        
        fantasy_indicators = [
            r'quest',
            r'adventure',
            r'(spell|magic|enchant)',
            r'(wizard|master|hero)',
            r'(tower|realm|kingdom)',
            r'🎯|⚔️|🏆|🌟|🧙',  # Emoji indicators
        ]
        
        theme_score = 0
        for pattern in fantasy_indicators:
            if re.search(pattern, body, re.IGNORECASE):
                theme_score += 1
        
        if theme_score >= 4:
            result.score += 10
            result.info.append(f"Strong fantasy theme integration (score: {theme_score}/6)")
        elif theme_score >= 2:
            result.score += 5
            result.warnings.append(f"Moderate fantasy theme integration (score: {theme_score}/6)")
        else:
            result.warnings.append("Limited fantasy theme integration. Consider adding more gamification elements.")
        result.max_score += 10
    
    def validate_accessibility(self, body: str, result: ValidationResult):
        """Validate accessibility features"""
        self.log_info("Validating accessibility...")
        
        # Check for descriptive alt text in images
        images = re.findall(r'!\[([^\]]*)\]', body)
        if images:
            empty_alt = [img for img in images if not img.strip()]
            if empty_alt:
                result.warnings.append(f"{len(empty_alt)} images missing alt text")
            else:
                result.score += 3
                result.info.append(f"All {len(images)} images have alt text")
            result.max_score += 3
    
    def validate_citations(self, body: str, result: ValidationResult):
        """Validate presence of citations and references"""
        self.log_info("Validating citations...")
        
        # Look for citations or references sections
        if re.search(r'(##\s+.*Citations?|##\s+.*References?|##\s+.*Resources?)', body, re.IGNORECASE):
            result.score += 5
            result.info.append("Citations/references section found")
        else:
            result.warnings.append("No citations/references section found. Consider adding external resources.")
        result.max_score += 5
    
    def validate_quest_file(self, filepath: Path) -> ValidationResult:
        """Validate a single quest file"""
        result = ValidationResult(quest_file=str(filepath))
        
        self.log_info(f"\n{'='*60}")
        self.log_info(f"Validating: {filepath.name}")
        self.log_info(f"{'='*60}")
        
        try:
            # Try UTF-8 first, then fallback to other encodings
            try:
                content = filepath.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                # Try with error handling
                content = filepath.read_text(encoding='utf-8', errors='replace')
                self.log_warning(f"File contains invalid UTF-8 characters, replaced with placeholders")
        except Exception as e:
            result.errors.append(f"Failed to read file: {e}")
            result.passed = False
            return result
        
        # Extract frontmatter
        frontmatter, body = self.extract_frontmatter(content)
        
        if frontmatter is None:
            result.errors.append("Failed to parse frontmatter")
            result.passed = False
            return result
        
        # Check if this is a draft and we should skip it
        is_draft = frontmatter.get('draft', False)
        if is_draft and self.exclude_drafts:
            result.info.append("Skipped: draft quest (--exclude-drafts)")
            return result
        
        # Run all validations
        self.validate_frontmatter_required(frontmatter, result)
        self.validate_frontmatter_hierarchy(frontmatter, result)
        self.validate_level_format(frontmatter, result)
        self.validate_difficulty(frontmatter, result)
        self.validate_estimated_time(frontmatter, result)
        self.validate_permalink(frontmatter, result)
        self.validate_content_structure(body, result)
        self.validate_code_blocks(body, result)
        self.validate_checkboxes(body, result)
        self.validate_fantasy_theme(body, frontmatter, result)
        self.validate_accessibility(body, result)
        self.validate_citations(body, result)
        self.validate_placeholder_status(frontmatter, body, result)
        
        # Check against fail threshold
        if self.fail_threshold > 0 and result.max_score > 0:
            score_pct = (result.score / result.max_score) * 100
            if score_pct < self.fail_threshold:
                result.errors.append(f"Score {score_pct:.1f}% below threshold {self.fail_threshold}%")
                result.passed = False
        
        return result
    
    def print_result(self, result: ValidationResult):
        """Print validation result"""
        print(f"\n{'='*60}")
        print(f"Quest: {Path(result.quest_file).name}")
        print(f"{'='*60}")
        
        # Overall status
        if result.passed and not result.warnings:
            self.log_success("PASSED - Excellent quest quality!")
        elif result.passed:
            self.log_success("PASSED - With warnings")
        else:
            self.log_error("FAILED - Needs improvement")
        
        # Score
        percentage = (result.score / result.max_score * 100) if result.max_score > 0 else 0
        print(f"\n📊 Quality Score: {result.score}/{result.max_score} ({percentage:.1f}%)")
        
        # Errors
        if result.errors:
            print(f"\n❌ Errors ({len(result.errors)}):")
            for error in result.errors:
                try:
                    # Ensure the error message is properly encoded
                    safe_error = str(error).encode('utf-8', errors='replace').decode('utf-8')
                    print(f"   • {safe_error}")
                except Exception:
                    print(f"   • [Error message contains invalid characters]")
        
        # Warnings
        if result.warnings:
            print(f"\n⚠️  Warnings ({len(result.warnings)}):")
            for warning in result.warnings:
                try:
                    # Ensure the warning message is properly encoded
                    safe_warning = str(warning).encode('utf-8', errors='replace').decode('utf-8')
                    print(f"   • {safe_warning}")
                except Exception:
                    print(f"   • [Warning message contains invalid characters]")
        
        # Info
        if self.verbose and result.info:
            print(f"\nℹ️  Information ({len(result.info)}):")
            for info in result.info:
                try:
                    # Ensure the info message is properly encoded
                    safe_info = str(info).encode('utf-8', errors='replace').decode('utf-8')
                    print(f"   • {safe_info}")
                except Exception:
                    print(f"   • [Info message contains invalid characters]")
    
    def validate_placeholder_status(self, fm: Dict, body: str, result: ValidationResult):
        """Detect if a quest is a placeholder with template boilerplate"""
        placeholder_hits = 0
        
        # Check frontmatter values for placeholder patterns
        for key, value in fm.items():
            if isinstance(value, str):
                for pattern in self.PLACEHOLDER_PATTERNS:
                    if re.search(pattern, value, re.IGNORECASE):
                        placeholder_hits += 1
                        break
        
        # Check quest_relationships for placeholder paths like /quests/level-XXXX-side-quest-1/
        for rel_key in ['quest_relationships', 'quest_dependencies']:
            rel = fm.get(rel_key, {})
            if isinstance(rel, dict):
                for sub_key, sub_val in rel.items():
                    if isinstance(sub_val, list):
                        for item in sub_val:
                            if isinstance(item, str) and re.search(r'level-\d{4}-(side-quest|alternative|continuation)', item):
                                placeholder_hits += 1
        
        # Check body for template bracket placeholders like [Requirement 1], [Badge Name]
        body_bracket_placeholders = re.findall(
            r'\[(?:Requirement \d|Badge Name|Next Quest|Side Quest|Achievement|'
            r'Brief description|Complex Implementation|How to verify|'
            r'What to build|Suggested Quest|Related|Your |Technology|'
            r'Advanced Skill|Integration Skill|Campaign|Story arc)\b[^\]]*\]',
            body, re.IGNORECASE
        )
        if len(body_bracket_placeholders) >= 5:
            placeholder_hits += 3  # Strong signal: many template brackets in body
        elif len(body_bracket_placeholders) >= 2:
            placeholder_hits += 1
        
        # Check body for minimal content
        body_stripped = body.strip()
        body_lines = [l for l in body_stripped.split('\n') if l.strip()]
        if len(body_lines) < 20:
            placeholder_hits += 2  # Very short body is a strong placeholder signal
        
        if placeholder_hits >= 3:
            result.info.append(f"PLACEHOLDER_QUEST: {placeholder_hits} placeholder indicators found")
        elif placeholder_hits >= 1:
            result.info.append(f"PARTIAL_CONTENT: {placeholder_hits} placeholder indicators found")

    def validate_directory(self, directory: Path, pattern: str = "*.md", recursive: bool = True) -> List[ValidationResult]:
        """Validate all quest files in a directory"""
        # Skip directories that are not quest content
        skip_dirs = {'templates', 'tools', 'docs', 'inventory', 'codex', 'scripts'}
        
        if recursive:
            quest_files = sorted(directory.rglob(pattern))
        else:
            quest_files = sorted(directory.glob(pattern))
        
        if not quest_files:
            self.log_warning(f"No quest files found in {directory}")
            return []
        
        self.log_info(f"Found {len(quest_files)} quest files to validate")
        
        for quest_file in quest_files:
            # Skip README, INDEX, HOME files
            if quest_file.name.upper() in ['README.MD', 'INDEX.MD', 'HOME.MD']:
                self.log_info(f"Skipping: {quest_file.name}")
                continue
            
            # Skip non-quest directories
            rel_parts = quest_file.relative_to(directory).parts
            if any(part in skip_dirs for part in rel_parts[:-1]):
                self.log_info(f"Skipping (non-quest dir): {quest_file}")
                continue
            
            # Skip files that don't have frontmatter (like NETWORK_REPORT.md)
            if quest_file.stem.isupper() and '_' in quest_file.stem:
                self.log_info(f"Skipping (non-quest file): {quest_file.name}")
                continue
            
            result = self.validate_quest_file(quest_file)
            # Skip adding draft results when --exclude-drafts is active
            if self.exclude_drafts and any('Skipped: draft quest' in i for i in result.info):
                self.log_info(f"Skipping draft: {quest_file.name}")
                continue
            self.results.append(result)
            self.print_result(result)
        
        return self.results
    
    def generate_report(self) -> Dict:
        """Generate summary report"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        total_errors = sum(len(r.errors) for r in self.results)
        total_warnings = sum(len(r.warnings) for r in self.results)
        # Avoid division by zero
        scores = [r.score / r.max_score * 100 for r in self.results if r.max_score > 0]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Count placeholders vs complete quests
        placeholders = sum(1 for r in self.results
                          if any('PLACEHOLDER_QUEST' in i for i in r.info))
        complete = total - placeholders
        
        # Per-level breakdown
        level_stats = {}
        for r in self.results:
            # Extract level from path (e.g., pages/_quests/0010/file.md → 0010)
            parts = Path(r.quest_file).parts
            level = 'root'
            for part in parts:
                if re.match(r'^\d{4}$', part):
                    level = part
                    break
            if level not in level_stats:
                level_stats[level] = {'total': 0, 'passed': 0, 'failed': 0, 'scores': [], 'placeholders': 0}
            level_stats[level]['total'] += 1
            if r.passed:
                level_stats[level]['passed'] += 1
            else:
                level_stats[level]['failed'] += 1
            if r.max_score > 0:
                level_stats[level]['scores'].append(r.score / r.max_score * 100)
            if any('PLACEHOLDER_QUEST' in i for i in r.info):
                level_stats[level]['placeholders'] += 1
        
        # Score distribution buckets
        score_distribution = {'90-100': 0, '80-89': 0, '70-79': 0, '60-69': 0, '50-59': 0, '<50': 0}
        for s in scores:
            if s >= 90: score_distribution['90-100'] += 1
            elif s >= 80: score_distribution['80-89'] += 1
            elif s >= 70: score_distribution['70-79'] += 1
            elif s >= 60: score_distribution['60-69'] += 1
            elif s >= 50: score_distribution['50-59'] += 1
            else: score_distribution['<50'] += 1
        
        # Most common errors and warnings
        error_counts = {}
        warning_counts = {}
        for r in self.results:
            for e in r.errors:
                # Normalize error messages (strip variable parts)
                key = re.sub(r': .*$', '', e)
                error_counts[key] = error_counts.get(key, 0) + 1
            for w in r.warnings:
                key = re.sub(r': .*$', '', w)
                warning_counts[key] = warning_counts.get(key, 0) + 1
        
        top_errors = sorted(error_counts.items(), key=lambda x: -x[1])[:10]
        top_warnings = sorted(warning_counts.items(), key=lambda x: -x[1])[:10]
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'complete': complete,
            'placeholders': placeholders,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'average_score': avg_score,
            'score_distribution': score_distribution,
            'level_stats': {k: {**v, 'avg_score': sum(v['scores'])/len(v['scores']) if v['scores'] else 0}
                           for k, v in sorted(level_stats.items())},
            'top_errors': top_errors,
            'top_warnings': top_warnings,
            'results': self.results
        }
    
    def print_summary(self, detailed: bool = False):
        """Print validation summary"""
        report = self.generate_report()
        
        print(f"\n{'='*60}")
        print("VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Quests:     {report['total']}")
        print(f"  Complete:       {report['complete']}")
        print(f"  Placeholders:   {report['placeholders']}")
        print(f"Passed:           {report['passed']} ✅")
        print(f"Failed:           {report['failed']} ❌")
        print(f"Total Errors:     {report['total_errors']}")
        print(f"Total Warnings:   {report['total_warnings']}")
        print(f"Average Score:    {report['average_score']:.1f}%")
        print(f"{'='*60}")
        
        if detailed:
            print(f"\n{'='*60}")
            print("SCORE DISTRIBUTION")
            print(f"{'='*60}")
            for bucket, count in report['score_distribution'].items():
                bar = '█' * count
                print(f"  {bucket:>7}: {count:3d} {bar}")
            
            print(f"\n{'='*60}")
            print("PER-LEVEL BREAKDOWN")
            print(f"{'='*60}")
            print(f"{'Level':<8} {'Total':>5} {'Pass':>5} {'Fail':>5} {'Avg%':>6} {'Placeholders':>12}")
            print(f"{'-'*46}")
            for level, stats in report.get('level_stats', {}).items():
                avg = stats.get('avg_score', 0)
                print(f"{level:<8} {stats['total']:>5} {stats['passed']:>5} {stats['failed']:>5} {avg:>5.1f}% {stats['placeholders']:>12}")
            
            if report['top_errors']:
                print(f"\n{'='*60}")
                print("TOP ERRORS")
                print(f"{'='*60}")
                for err, count in report['top_errors']:
                    print(f"  [{count:3d}x] {err}")
            
            if report['top_warnings']:
                print(f"\n{'='*60}")
                print("TOP WARNINGS")
                print(f"{'='*60}")
                for warn, count in report['top_warnings']:
                    print(f"  [{count:3d}x] {warn}")
        
        print()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='IT-Journey Quest Validator - Validate quest files against standards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s quest.md                    # Validate single quest
  %(prog)s -d pages/_quests/           # Validate all quests in directory
  %(prog)s -d pages/_quests/ -v        # Verbose output
  %(prog)s quest.md --report report.json  # Generate JSON report
        '''
    )
    
    parser.add_argument('quest_file', nargs='?', help='Quest file to validate')
    parser.add_argument('-d', '--directory', help='Directory containing quest files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-r', '--report', help='Generate JSON report to file')
    parser.add_argument('--pattern', default='*.md', help='File pattern to match (default: *.md)')
    parser.add_argument('--no-recursive', action='store_true', help='Do not recurse into subdirectories')
    parser.add_argument('--exclude-drafts', action='store_true', help='Skip quests with draft: true')
    parser.add_argument('--fail-threshold', type=int, default=0,
                        help='Minimum score percentage to pass (0=disabled, e.g. 60 or 80)')
    parser.add_argument('--summary', action='store_true', help='Show detailed aggregate summary with per-level stats')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.quest_file and not args.directory:
        parser.error("Either quest_file or --directory must be specified")
    
    # Create validator
    validator = QuestValidator(
        verbose=args.verbose,
        exclude_drafts=args.exclude_drafts,
        fail_threshold=args.fail_threshold
    )
    
    # Validate
    if args.directory:
        directory = Path(args.directory)
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            sys.exit(1)
        validator.validate_directory(directory, args.pattern, recursive=not args.no_recursive)
    else:
        quest_file = Path(args.quest_file)
        if not quest_file.exists():
            print(f"❌ File not found: {quest_file}")
            sys.exit(1)
        result = validator.validate_quest_file(quest_file)
        validator.results.append(result)
        validator.print_result(result)
    
    # Print summary
    validator.print_summary(detailed=args.summary)
    
    # Generate report if requested
    if args.report:
        import json
        report = validator.generate_report()
        # Convert results to dict for JSON serialization
        report['results'] = [
            {
                'quest_file': r.quest_file,
                'passed': r.passed,
                'errors': r.errors,
                'warnings': r.warnings,
                'info': r.info,
                'score': r.score,
                'max_score': r.max_score,
                'score_pct': round(r.score / r.max_score * 100, 1) if r.max_score > 0 else 0,
                'is_placeholder': any('PLACEHOLDER_QUEST' in i for i in r.info)
            }
            for r in report['results']
        ]
        # Remove non-serializable score lists from level_stats
        for level, stats in report.get('level_stats', {}).items():
            stats.pop('scores', None)
        with open(args.report, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report generated: {args.report}")
    
    # Exit with appropriate code
    report = validator.generate_report()
    sys.exit(0 if report['failed'] == 0 else 1)

if __name__ == '__main__':
    main()
