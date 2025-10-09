#!/usr/bin/env python3
"""
Quest Validator - IT-Journey Quest Testing Framework
Validates quest structure, content, and quality standards

Author: IT-Journey Team
Created: 2025-10-08
Version: 1.0.0
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
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
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
        level = fm.get('level', '')
        
        # Should include /quests/ and level
        if not permalink.startswith('/quests/'):
            result.errors.append(f"Permalink should start with '/quests/': {permalink}")
            result.passed = False
        elif level and f"level-{level}" not in permalink:
            result.warnings.append(f"Permalink doesn't include level {level}: {permalink}")
        else:
            result.score += 5
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
        
        # Find all code blocks
        code_blocks = re.findall(r'```(\w*)\n', body)
        
        if code_blocks:
            unspecified = [i for i, lang in enumerate(code_blocks) if not lang]
            if unspecified:
                result.warnings.append(f"{len(unspecified)} code blocks without language specification")
            else:
                result.score += 5
                result.info.append(f"All {len(code_blocks)} code blocks have language specification")
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
    
    def validate_directory(self, directory: Path, pattern: str = "*.md") -> List[ValidationResult]:
        """Validate all quest files in a directory"""
        quest_files = sorted(directory.glob(pattern))
        
        if not quest_files:
            self.log_warning(f"No quest files found in {directory}")
            return []
        
        self.log_info(f"Found {len(quest_files)} quest files to validate")
        
        for quest_file in quest_files:
            # Skip README and similar files
            if quest_file.name.upper() in ['README.MD', 'INDEX.MD', 'HOME.MD']:
                self.log_info(f"Skipping: {quest_file.name}")
                continue
            
            result = self.validate_quest_file(quest_file)
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
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'average_score': avg_score,
            'results': self.results
        }
    
    def print_summary(self):
        """Print validation summary"""
        report = self.generate_report()
        
        print(f"\n{'='*60}")
        print("VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Quests:     {report['total']}")
        print(f"Passed:           {report['passed']} ✅")
        print(f"Failed:           {report['failed']} ❌")
        print(f"Total Errors:     {report['total_errors']}")
        print(f"Total Warnings:   {report['total_warnings']}")
        print(f"Average Score:    {report['average_score']:.1f}%")
        print(f"{'='*60}\n")

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
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.quest_file and not args.directory:
        parser.error("Either quest_file or --directory must be specified")
    
    # Create validator
    validator = QuestValidator(verbose=args.verbose)
    
    # Validate
    if args.directory:
        directory = Path(args.directory)
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            sys.exit(1)
        validator.validate_directory(directory, args.pattern)
    else:
        quest_file = Path(args.quest_file)
        if not quest_file.exists():
            print(f"❌ File not found: {quest_file}")
            sys.exit(1)
        result = validator.validate_quest_file(quest_file)
        validator.results.append(result)
        validator.print_result(result)
    
    # Print summary
    validator.print_summary()
    
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
                'score': r.score,
                'max_score': r.max_score
            }
            for r in report['results']
        ]
        with open(args.report, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report generated: {args.report}")
    
    # Exit with appropriate code
    report = validator.generate_report()
    sys.exit(0 if report['failed'] == 0 else 1)

if __name__ == '__main__':
    main()
