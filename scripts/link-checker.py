#!/usr/bin/env python3
"""
IT-Journey Link Health Guardian - Comprehensive Link Checker
A unified script for link checking, analysis, and AI-powered insights
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import requests
import shutil


class LinkHealthGuardian:
    def __init__(self, config):
        self.config = config
        self.output_dir = config.get('output_dir', 'link-check-results')
        self.results = {}
        self.analysis = {}
        self.ai_analysis = {}
        
        # Ensure output directory exists
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup colored logging for better output visibility."""
        self.colors = {
            'INFO': '\033[0;34m',
            'SUCCESS': '\033[0;32m',
            'WARNING': '\033[1;33m',
            'ERROR': '\033[0;31m',
            'NC': '\033[0m'  # No Color
        }
    
    def log(self, level, message):
        """Log a message with color coding."""
        color = self.colors.get(level, '')
        nc = self.colors['NC']
        print(f"{color}[{level}]{nc} {message}")
    
    def install_dependencies(self):
        """Install required dependencies for link checking."""
        self.log('INFO', 'Installing link checking dependencies...')
        
        try:
            # Check if lychee is already installed
            result = subprocess.run(['lychee', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                self.log('SUCCESS', f'Lychee already installed: {result.stdout.strip()}')
                return True
        except FileNotFoundError:
            pass
        
        # Install lychee
        self.log('INFO', 'Installing Lychee link checker...')
        try:
            # Choose install method by platform
            platform = sys.platform

            # Prefer package managers if available
            if platform == 'darwin' and shutil.which('brew'):
                self.log('INFO', 'Installing lychee with Homebrew (macOS)')
                subprocess.run(['brew', 'install', 'lychee'], check=True)
            elif platform.startswith('linux'):
                # Try cargo install as primary method (most reliable)
                if shutil.which('cargo'):
                    self.log('INFO', 'Installing lychee with cargo')
                    try:
                        subprocess.run(['cargo', 'install', 'lychee', '--locked'], check=True, timeout=300)
                        return True
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                        self.log('WARNING', 'Cargo install failed or timed out, trying alternative methods')
                
                # Try downloading pre-built binary with retries and fallback versions
                self.log('INFO', 'Downloading lychee pre-built binary')
                
                # Try multiple versions for resilience
                versions_to_try = [
                    'latest',
                    'v0.16.1',  # Known stable version
                    'v0.15.1'   # Fallback
                ]
                
                for version in versions_to_try:
                    try:
                        if version == 'latest':
                            tarball_url = 'https://github.com/lycheeverse/lychee/releases/latest/download/lychee-x86_64-unknown-linux-gnu.tar.gz'
                        else:
                            tarball_url = f'https://github.com/lycheeverse/lychee/releases/download/{version}/lychee-x86_64-unknown-linux-gnu.tar.gz'
                        
                        self.log('INFO', f'Attempting download from {version}')
                        
                        # Download with retries
                        max_retries = 3
                        for attempt in range(max_retries):
                            try:
                                subprocess.run(['curl', '-sSfL', '--retry', '3', '--retry-delay', '2', 
                                              tarball_url, '-o', '/tmp/lychee.tar.gz'], 
                                              check=True, timeout=60)
                                break
                            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                                if attempt == max_retries - 1:
                                    raise
                                self.log('WARNING', f'Download attempt {attempt + 1} failed, retrying...')
                                time.sleep(2)
                        
                        subprocess.run(['tar', '-xzf', '/tmp/lychee.tar.gz', '-C', '/tmp'], check=True)
                        
                        # Install to /usr/local/bin or ~/.local/bin
                        if shutil.which('sudo'):
                            subprocess.run(['sudo', 'mv', '/tmp/lychee', '/usr/local/bin/'], check=True)
                            subprocess.run(['sudo', 'chmod', '+x', '/usr/local/bin/lychee'], check=True)
                        else:
                            # Fall back to user-local install
                            local_bin = os.path.expanduser('~/.local/bin')
                            os.makedirs(local_bin, exist_ok=True)
                            subprocess.run(['mv', '/tmp/lychee', local_bin], check=True)
                            subprocess.run(['chmod', '+x', f'{local_bin}/lychee'], check=True)
                            # Add to PATH if not already there
                            if local_bin not in os.environ.get('PATH', ''):
                                os.environ['PATH'] = f"{local_bin}:{os.environ.get('PATH', '')}"
                        
                        self.log('SUCCESS', f'Successfully installed lychee from {version}')
                        return True
                    except Exception as e:
                        self.log('WARNING', f'Failed to install from {version}: {e}')
                        continue
                
                # If all else fails, log error and return False
                self.log('ERROR', 'All installation methods failed')
                return False
            
            # Verify installation
            result = subprocess.run(['lychee', '--version'], 
                                  capture_output=True, text=True, check=True)
            self.log('SUCCESS', f'Lychee installed successfully: {result.stdout.strip()}')
            return True
            
        except subprocess.CalledProcessError as e:
            self.log('ERROR', f'Failed to install Lychee: {e}')
            return False
        except Exception as e:
            self.log('ERROR', f'Unexpected error during installation: {e}')
            return False
    
    def determine_scope_files(self, scope):
        """Determine which files to check based on scope."""
        scope_mapping = {
            'website': '.',
            'all': '.',
            'docs': 'docs/',
            'posts': 'pages/_posts/',
            'quests': 'pages/_quests/',
            'internal': '.',
            'external': '.'
        }
        
        base_path = scope_mapping.get(scope, '.')
        
        # Find all markdown & HTML files in the specified path
        files = []
        for ext in ['*.md', '*.html', '*.htm']:
            if os.path.exists(base_path):
                files.extend(Path(base_path).rglob(ext))
        
        # Convert to strings and filter
        file_list = [str(f) for f in files]
        
        # For internal/external scope, we'll filter during analysis
        self.log('INFO', f'Scope "{scope}" includes {len(file_list)} files')
        # Return an empty list if no files found - caller will handle default '.'
        return file_list
    
    def run_link_check(self):
        """Execute the main link checking with Lychee."""
        self.log('INFO', 'Starting comprehensive link health check...')
        
        scope = self.config.get('scope', 'website')
        files = self.determine_scope_files(scope)
        
        # Build lychee command
        output_file = os.path.join(self.output_dir, 'lychee_results.json')
        cmd = [
            'lychee',
            '--format', 'json',
            '--output', output_file,
            '--timeout', str(self.config.get('timeout', 30)),
            '--max-retries', str(self.config.get('max_retries', 3)),
            '--user-agent', 'IT-Journey-LinkChecker/2.0 (GitHub Actions)',
            '--verbose',
            '--no-progress',
            '--accept', '200,204,206,300,301,302,303,307,308',  # Accept common redirect codes
            '--base', 'https://it-journey.dev',  # Base URL for resolving root-relative links
            '--exclude', 'https://url/'  # Exclude placeholder URLs
        ]
        
        # Add scope-specific options
        if scope == 'internal':
            cmd.extend(['--exclude-all-private'])
        elif scope == 'external':
            cmd.extend(['--include-verbatim', 'http'])
        
        # Note: Removed --remap option as it was causing errors
        # --remap is for URL pattern remapping, not for following redirects
        # Lychee follows redirects by default
        
        # Add files to check
        # If no files were found, use repository root (lychee expects at least one path)
        if not files:
            files = ['.']
        cmd.extend(files)
        
        self.log('INFO', f'Running: {" ".join(cmd)}')
        
        try:
            # Run lychee and capture output
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
            
            # Log the result for debugging
            self.log('INFO', f'Lychee exit code: {result.returncode}')
            if result.stdout:
                self.log('INFO', f'Lychee stdout: {result.stdout[:500]}...')
            if result.stderr:
                self.log('INFO', f'Lychee stderr: {result.stderr[:500]}...')
            
            # Check if output file was created
            if not os.path.exists(output_file):
                self.log('WARNING', f'Lychee output file not created: {output_file}')
                
                # Try to parse stdout as JSON if file wasn't created
                if result.stdout.strip():
                    try:
                        json_data = json.loads(result.stdout)
                        with open(output_file, 'w') as f:
                            json.dump(json_data, f, indent=2)
                        self.log('INFO', 'Created results file from stdout')
                    except json.JSONDecodeError:
                        self.log('WARNING', 'Could not parse stdout as JSON')
                        
                # If still no file, create a minimal results file
                if not os.path.exists(output_file):
                    minimal_results = {
                        "total": 0,
                        "successful": 0,
                        "errors": 0,
                        "error_details": [],
                        "warnings": ["Lychee output file was not created"],
                        "stdout": result.stdout[:1000] if result.stdout else "",
                        "stderr": result.stderr[:1000] if result.stderr else ""
                    }
                    with open(output_file, 'w') as f:
                        json.dump(minimal_results, f, indent=2)
                    self.log('INFO', 'Created minimal results file for parsing')
            
            # Also generate markdown summary if requested
            if self.config.get('generate_summary', True):
                summary_cmd = cmd.copy()
                summary_cmd[summary_cmd.index('--format') + 1] = 'markdown'
                summary_cmd[summary_cmd.index('--output') + 1] = os.path.join(self.output_dir, 'summary.md')
                summary_result = subprocess.run(summary_cmd, capture_output=True, text=True)
                if summary_result.returncode != 0:
                    self.log('WARNING', f'Markdown summary generation failed: {summary_result.stderr}')
            
            self.log('SUCCESS', 'Link checking completed')
            return True
            
        except subprocess.TimeoutExpired:
            self.log('ERROR', 'Link checking timed out after 30 minutes')
            return False
        except subprocess.CalledProcessError as e:
            self.log('WARNING', f'Link checking completed with some failures: {e}')
            return True  # Continue with analysis even if some links failed
        except Exception as e:
            self.log('ERROR', f'Link checking failed: {e}')
            return False
    
    def parse_lychee_results(self):
        """Parse Lychee JSON results and extract statistics."""
        results_file = os.path.join(self.output_dir, 'lychee_results.json')
        
        if not os.path.exists(results_file):
            self.log('WARNING', 'No Lychee results file found')
            return False
        
        try:
            with open(results_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    self.log('WARNING', 'Lychee results file is empty')
                    return False
                data = json.loads(content)
            
            # Log file content for debugging
            self.log('INFO', f'Lychee results file size: {len(content)} characters')
            
            # Extract statistics - handle different lychee output formats
            if isinstance(data, list):
                # If data is a list of link results
                total = len(data)
                successful = sum(1 for item in data if item.get('status') == 'ok' or item.get('status') == 'success')
                errors = total - successful
                error_details = [item for item in data if item.get('status') not in ['ok', 'success']]
            elif isinstance(data, dict):
                # If data is a summary object
                total = data.get('total', data.get('total_links', 0))
                successful = data.get('successful', data.get('success_count', 0))
                errors = data.get('errors', data.get('error_count', total - successful))
                error_details = data.get('error_details', data.get('failures', []))
            else:
                self.log('WARNING', f'Unexpected data format in lychee results: {type(data)}')
                return False

            # If the raw output doesn't contain a canonical error_map, build one
            if isinstance(data, dict) and 'error_map' not in data:
                # Lychee may provide 'failures' or 'error_details' as a list
                if isinstance(data.get('error_details'), list) and data.get('error_details'):
                    failures = data.get('error_details')
                elif isinstance(data.get('failures'), list) and data.get('failures'):
                    failures = data.get('failures')
                elif isinstance(data, dict) and data.get('failed'):  # summary with nested
                    failures = data.get('failed')
                else:
                    failures = []

                error_map = defaultdict(list)
                for item in failures:
                    file_path = item.get('file', item.get('source', 'unknown'))
                    error_map[file_path].append(item)

                # Attach built map back to raw data for analysis
                data['error_map'] = dict(error_map)
            
            success_rate = (successful / total * 100) if total > 0 else 100
            
            # Store basic stats
            self.results = {
                'total_links': total,
                'successful_links': successful,
                'broken_links': errors,
                'success_rate': round(success_rate, 1),
                'raw_data': data
            }
            
            # Save statistics for GitHub Actions
            stats_file = os.path.join(self.output_dir, 'statistics.env')
            with open(stats_file, 'w') as f:
                f.write(f"TOTAL_COUNT={total}\n")
                f.write(f"BROKEN_COUNT={errors}\n")
                f.write(f"SUCCESS_RATE={success_rate:.1f}\n")
            
            self.log('SUCCESS', f'Parsed results: {total} total, {errors} broken, {success_rate:.1f}% success')
            return True
            
        except Exception as e:
            self.log('ERROR', f'Failed to parse Lychee results: {e}')
            return False
    
    def analyze_link_failures(self):
        """Analyze link failures and categorize them."""
        self.log('INFO', 'Analyzing link health patterns and trends...')
        
        if not self.results or not self.results.get('raw_data'):
            self.log('WARNING', 'No results data available for analysis')
            return False
        
        data = self.results['raw_data']
        
        # Initialize categories
        categories = {
            'broken_external': [],
            'broken_internal': [],
            'ssl_errors': [],
            'dns_errors': [],
            'timeouts': [],
            'rate_limited': [],
            'certificate_errors': [],
            'network_errors': [],
            'redirects': [],
            'unknown': []
        }
        
        # Process error map
        # Normalize data: lychee sometimes returns a list of results or nested failure
        if isinstance(data, list):
            # Convert list to error_map keyed by file
            error_map = defaultdict(list)
            for item in data:
                if item.get('status') in ['ok', 'success']:
                    continue
                file_key = item.get('file', 'unknown')
                error_map[file_key].append(item)
            error_map = dict(error_map)
        else:
            error_map = data.get('error_map', {}) or data.get('errors', {})
        for file_path, errors in (error_map or {}).items():
            for error in errors:
                try:
                    url = error.get('url', '')
                    error_msg = str(error.get('status', '')).lower()
                    
                    # Create result object
                    result = {
                        'url': url,
                        'error': error_msg,
                        'file': file_path,
                        'status': 'Failed'
                    }
                    
                    # Categorize by error type
                    if any(term in error_msg for term in ['ssl', 'tls', 'certificate']):
                        if 'ssl' in error_msg or 'tls' in error_msg:
                            categories['ssl_errors'].append(result)
                        else:
                            categories['certificate_errors'].append(result)
                    elif any(term in error_msg for term in ['dns', 'resolve', 'hostname']):
                        categories['dns_errors'].append(result)
                    elif any(term in error_msg for term in ['timeout', 'timed out']):
                        categories['timeouts'].append(result)
                    elif any(term in error_msg for term in ['429', 'rate limit', 'too many']):
                        categories['rate_limited'].append(result)
                    elif any(term in error_msg for term in ['network', 'connection', 'refused']):
                        categories['network_errors'].append(result)
                    elif url.startswith('http'):
                        categories['broken_external'].append(result)
                    elif url.startswith('/') or not url.startswith('http'):
                        categories['broken_internal'].append(result)
                    else:
                        categories['unknown'].append(result)
                        
                except Exception as e:
                    self.log('WARNING', f'Error processing error entry: {e}')
                    continue
        
        # Analyze patterns
        patterns = self.identify_patterns(categories)
        
        # Store analysis
        self.analysis = {
            'categories': categories,
            'patterns': patterns,
            'summary': {
                'total_broken': sum(len(cat) for cat in categories.values()),
                'most_common_error': self.get_most_common_error(categories),
                'problematic_domains': self.get_problematic_domains(categories)
            },
            'analysis_timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        # Generate detailed report
        self.generate_analysis_report()
        
        self.log('SUCCESS', f'Analysis completed: {len(patterns)} patterns identified')
        return True
    
    def identify_patterns(self, categories):
        """Identify patterns in link failures."""
        patterns = []
        
        # Domain failure analysis
        domain_failures = defaultdict(int)
        for category in ['broken_external', 'timeouts', 'rate_limited', 'ssl_errors', 'dns_errors']:
            for item in categories[category]:
                url = item.get('url', '')
                if url.startswith('http'):
                    try:
                        domain = url.split('/')[2]
                        domain_failures[domain] += 1
                    except:
                        pass
        
        if domain_failures:
            top_domains = sorted(domain_failures.items(), key=lambda x: x[1], reverse=True)[:3]
            patterns.append(f"Top failing domains: {', '.join([f'{d}({c})' for d, c in top_domains])}")
        
        # Category-specific patterns
        internal_count = len(categories['broken_internal'])
        if internal_count > 0:
            patterns.append(f"Found {internal_count} broken internal links - check Jekyll configuration")
        
        timeout_count = len(categories['timeouts'])
        if timeout_count > 5:
            patterns.append(f"High timeout rate ({timeout_count}) - network or slow sites")
        
        ssl_count = len(categories['ssl_errors'])
        if ssl_count > 0:
            patterns.append(f"SSL/TLS issues on {ssl_count} links - certificate problems")
        
        dns_count = len(categories['dns_errors'])
        if dns_count > 0:
            patterns.append(f"DNS resolution errors on {dns_count} links - domain issues")
        
        return patterns
    
    def get_most_common_error(self, categories):
        """Find the most common error category."""
        category_counts = {k: len(v) for k, v in categories.items()}
        if category_counts:
            return max(category_counts, key=category_counts.get)
        return 'none'
    
    def get_problematic_domains(self, categories):
        """Get list of problematic domains."""
        domains = set()
        for category in categories.values():
            for item in category:
                url = item.get('url', '')
                if url.startswith('http'):
                    try:
                        domain = url.split('/')[2]
                        domains.add(domain)
                    except:
                        pass
        return list(domains)[:5]  # Top 5
    
    def generate_analysis_report(self):
        """Generate detailed analysis report in markdown."""
        report_file = os.path.join(self.output_dir, 'detailed_analysis.md')
        
        with open(report_file, 'w') as f:
            f.write("# IT-Journey Link Health Analysis Report\n\n")
            f.write(f"**Analysis Date**: {self.analysis['analysis_timestamp']}\n")
            f.write(f"**Total Links**: {self.results['total_links']}\n")
            f.write(f"**Broken Links**: {self.results['broken_links']}\n")
            f.write(f"**Success Rate**: {self.results['success_rate']}%\n\n")
            
            if self.results['broken_links'] > 0:
                f.write("## Failure Categories\n\n")
                for category, items in self.analysis['categories'].items():
                    if items:
                        f.write(f"### {category.replace('_', ' ').title()}\n")
                        f.write(f"**Count**: {len(items)}\n\n")
                        for item in items[:5]:  # Show first 5
                            f.write(f"- **URL**: {item.get('url', 'Unknown')}\n")
                            f.write(f"  - **File**: {item.get('file', 'Unknown')}\n")
                            f.write(f"  - **Error**: {item.get('error', 'Unknown')}\n\n")
                        if len(items) > 5:
                            f.write(f"... and {len(items) - 5} more\n\n")
            
            if self.analysis['patterns']:
                f.write("## Identified Patterns\n\n")
                for pattern in self.analysis['patterns']:
                    f.write(f"- {pattern}\n")
                f.write("\n")
            
            f.write("## Recommendations\n\n")
            if self.results['broken_links'] == 0:
                f.write("🎉 Excellent! No broken links found.\n")
            else:
                f.write("### Priority Actions\n\n")
                f.write("1. **Fix Internal Links**: Address broken internal navigation first\n")
                f.write("2. **Update External Links**: Replace or remove broken external references\n")
                f.write("3. **Monitor SSL/DNS Issues**: Review certificate and domain problems\n")
                f.write("4. **Consider Rate Limiting**: Add problematic domains to ignore list\n")
        
        # Save analysis summary for GitHub Actions
        summary_file = os.path.join(self.output_dir, 'analysis_summary.env')
        with open(summary_file, 'w') as f:
            f.write(f"ANALYSIS_AVAILABLE=true\n")
            f.write(f"PATTERNS_COUNT={len(self.analysis['patterns'])}\n")
            f.write(f"MOST_COMMON_ERROR={self.analysis['summary']['most_common_error']}\n")
        
        self.log('SUCCESS', f'Analysis report generated: {report_file}')
    
    def run_ai_analysis(self):
        """Run AI-powered analysis if OpenAI API key is available."""
        if not self.config.get('ai_analysis', False):
            self.log('INFO', 'AI analysis disabled')
            return False
        
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            self.log('WARNING', 'OPENAI_API_KEY not found - skipping AI analysis')
            return self.generate_fallback_ai_analysis()
        
        self.log('INFO', 'Generating AI-powered insights...')
        
        try:
            # Prepare context for AI
            context = self.prepare_ai_context()
            
            # Make API request
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'user',
                        'content': self.build_ai_prompt(context)
                    }
                ],
                'max_tokens': 2000,
                'temperature': 0.3
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_content = result['choices'][0]['message']['content']
                
                # Save AI analysis
                self.save_ai_analysis(ai_content, True)
                self.log('SUCCESS', 'AI analysis completed successfully')
                return True
            else:
                try:
                    err = response.json()
                except Exception:
                    err = response.text
                self.log('ERROR', f'OpenAI API error: {response.status_code} - {err}')
                return self.generate_fallback_ai_analysis()
                
        except requests.exceptions.RequestException as e:
            # Network or timeout related exceptions
            self.log('ERROR', f'AI request failed: {e}')
            return self.generate_fallback_ai_analysis()
        except Exception as e:
            self.log('ERROR', f'AI analysis failed: {e}')
            return self.generate_fallback_ai_analysis()
    
    def prepare_ai_context(self):
        """Prepare context data for AI analysis."""
        return {
            'results': self.results,
            'analysis': self.analysis,
            'config': self.config,
            'repository': self.config.get('repository', 'IT-Journey'),
            'scope': self.config.get('scope', 'website')
        }
    
    def build_ai_prompt(self, context):
        """Build the AI analysis prompt."""
        results = context['results']
        analysis = context['analysis']
        
        prompt = f"""
Analyze this link health check for the IT-Journey educational repository:

## Summary Statistics
- Total links: {results['total_links']}
- Broken links: {results['broken_links']}
- Success rate: {results['success_rate']}%
- Scope: {context['scope']}

## Failure Categories
"""
        
        for category, items in analysis['categories'].items():
            if items:
                prompt += f"- {category.replace('_', ' ').title()}: {len(items)} links\n"
        
        if analysis['patterns']:
            prompt += f"\n## Identified Patterns\n"
            for pattern in analysis['patterns']:
                prompt += f"- {pattern}\n"
        
        prompt += """

## Analysis Request
Please provide a comprehensive analysis including:

1. **Root Cause Analysis**: Most likely causes for these link failures
2. **Educational Impact**: How these issues affect learning experience
3. **Priority Recommendations**: Specific actions ranked by importance
4. **Prevention Strategies**: How to avoid similar issues
5. **Technical Solutions**: Jekyll/GitHub Pages specific fixes

Focus on actionable insights for maintaining an educational platform.
Format your response in clear markdown sections.
"""
        
        return prompt
    
    def generate_fallback_ai_analysis(self):
        """Generate fallback analysis when AI is not available."""
        self.log('INFO', 'Generating fallback analysis...')
        
        results = self.results
        analysis = self.analysis
        
        content = f"""# AI-Powered Link Analysis (Fallback Mode)

## Executive Summary
Analyzed {results['total_links']} links with {results['broken_links']} failures ({results['success_rate']}% success rate).

## Root Cause Analysis
Based on failure patterns, the most common issues are:
- **{analysis['summary']['most_common_error'].replace('_', ' ').title()}**: Primary failure category
- **External Dependencies**: Third-party sites may have availability issues
- **Configuration Issues**: Internal links may reflect Jekyll setup problems

## Educational Impact Assessment
Link failures impact the learning experience by:
- Disrupting learning flow when students encounter broken references
- Reducing credibility of educational content
- Creating frustration during self-paced learning

## Priority Recommendations
1. **Fix Internal Links**: Highest priority - affects site navigation
2. **Review External Sources**: Update or replace unreliable external references
3. **Implement Monitoring**: Regular automated checks to catch issues early
4. **Documentation Updates**: Keep resource links current and valid

## Prevention Strategies
- Regular link health monitoring (weekly checks)
- Use archived links for critical external resources
- Implement redirect management for moved content
- Test links before publishing new content

*Note: Enhanced AI analysis requires OPENAI_API_KEY configuration.*
"""
        
        self.save_ai_analysis(content, False)
        return True
    
    def save_ai_analysis(self, content, is_ai_powered):
        """Save AI analysis results."""
        ai_file = os.path.join(self.output_dir, 'ai_analysis.md')
        with open(ai_file, 'w') as f:
            f.write(content)
        
        # Save summary for GitHub Actions
        ai_summary_file = os.path.join(self.output_dir, 'ai_analysis_summary.env')
        with open(ai_summary_file, 'w') as f:
            f.write(f"AI_ANALYSIS_AVAILABLE=true\n")
            f.write(f"AI_POWERED={str(is_ai_powered).lower()}\n")
            f.write(f"AI_ANALYSIS_TYPE={'openai' if is_ai_powered else 'fallback'}\n")
        
        self.log('SUCCESS', f'AI analysis saved: {ai_file}')
    
    def create_github_issue(self):
        """Create GitHub issue with comprehensive results."""
        if not self.config.get('create_issue', False):
            self.log('INFO', 'GitHub issue creation disabled')
            return False
        
        self.log('INFO', 'Creating GitHub issue with comprehensive results...')
        
        # Generate issue content
        issue_title = self.generate_issue_title()
        issue_body = self.generate_issue_body()
        
        # Save issue body for manual creation if needed
        issue_file = os.path.join(self.output_dir, 'issue_body.md')
        with open(issue_file, 'w') as f:
            f.write(issue_body)
        
        # Try to create issue using GitHub CLI
        try:
            cmd = [
                'gh', 'issue', 'create',
                '--title', issue_title,
                '--body-file', issue_file,
                '--label', self.get_issue_labels(),
                '--assignee', '@me'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issue_url = result.stdout.strip()
            
            # Save issue URL
            with open(os.path.join(self.output_dir, 'issue_url.txt'), 'w') as f:
                f.write(issue_url)
            
            self.log('SUCCESS', f'GitHub issue created: {issue_url}')
            return True
            
        except subprocess.CalledProcessError as e:
            self.log('ERROR', f'Failed to create GitHub issue: {e}')
            self.log('INFO', f'Issue body saved to: {issue_file}')
            return False
        except FileNotFoundError:
            self.log('ERROR', 'GitHub CLI not found - issue body saved for manual creation')
            self.log('INFO', f'Issue body saved to: {issue_file}')
            return False
    
    def generate_issue_title(self):
        """Generate appropriate issue title."""
        broken_count = self.results['broken_links']
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        if broken_count == 0:
            return f"🔗 Link Health Report - All Links Healthy ({date_str})"
        else:
            return f"🔗 Link Health Report - {broken_count} broken links found ({date_str})"
    
    def generate_issue_body(self):
        """Generate comprehensive issue body."""
        results = self.results
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        
        body = f"""# 🔗 IT-Journey Link Health Report

**Scan Date**: {timestamp}
**Repository**: {self.config.get('repository', 'IT-Journey')}
**Scope**: {self.config.get('scope', 'website')}
**Guardian Version**: 2.0.0

## 📊 Summary Statistics

- **Total links checked**: {results['total_links']}
- **Working links**: {results['successful_links']}
- **Broken links**: {results['broken_links']}
- **Success rate**: {results['success_rate']}%

"""
        
        if results['broken_links'] == 0:
            body += """## ✅ Status: Excellent

🎉 **All links are healthy!** Your IT-Journey site maintains perfect link integrity.

This demonstrates excellent maintenance practices and ensures a seamless learning experience for all users.
"""
        else:
            # Add status based on success rate
            success_rate = results['success_rate']
            if success_rate >= 95:
                status = "⚠️ Good (minor issues)"
            elif success_rate >= 90:
                status = "🟡 Fair (some issues)"
            elif success_rate >= 80:
                status = "🟠 Poor (multiple issues)"
            else:
                status = "🔴 Critical (major issues)"
            
            body += f"""## {status.split()[0]} Status: {status.split()[1:]}

**{results['broken_links']} broken links** were detected that may impact the learning experience.
"""
        
        # Add detailed analysis if available
        analysis_file = os.path.join(self.output_dir, 'detailed_analysis.md')
        if os.path.exists(analysis_file):
            body += "\n## 🔍 Detailed Analysis\n\n"
            with open(analysis_file, 'r') as f:
                body += f.read()
            body += "\n"
        
        # Add AI analysis if available
        ai_file = os.path.join(self.output_dir, 'ai_analysis.md')
        if os.path.exists(ai_file):
            body += "\n## 🤖 AI-Powered Insights\n\n"
            with open(ai_file, 'r') as f:
                body += f.read()
            body += "\n"
        
        # Add action items if there are broken links
        if results['broken_links'] > 0:
            body += """## 🛠️ Recommended Actions

### Immediate Actions
1. **Review Broken Links**: Check the detailed results above for specific URLs and errors
2. **Fix Internal Links**: Priority should be given to broken internal navigation
3. **Update External References**: Replace or remove broken external links
4. **Test Changes**: Verify fixes don't introduce new issues

### Preventive Measures
1. **Regular Monitoring**: Schedule weekly link health checks
2. **Content Guidelines**: Establish link validation procedures for new content
3. **Automated Testing**: Integrate link checking into CI/CD pipeline
4. **Documentation**: Update link maintenance procedures
"""
        
        body += f"""## 🔄 Re-running This Check

You can manually trigger another link check by:
1. Going to the [Actions tab](../../actions/workflows/link-health-guardian.yml)
2. Clicking "Run workflow"
3. Selecting your preferred scope and options

---

**Technical Details:**
- **Workflow**: Link Health Guardian v2.0
- **Scope**: {self.config.get('scope', 'website')}
- **Analysis Level**: {self.config.get('analysis_level', 'comprehensive')}
- **AI Analysis**: {'Enabled' if self.config.get('ai_analysis') else 'Disabled'}

*This issue was created automatically by the IT-Journey Link Health Guardian. 🤖*
"""
        
        return body
    
    def get_issue_labels(self):
        """Get appropriate labels for the GitHub issue."""
        labels = ['automated', 'link-checker', 'maintenance']
        
        if self.results['broken_links'] > 0:
            labels.append('bug')
        
        if os.path.exists(os.path.join(self.output_dir, 'ai_analysis.md')):
            labels.append('ai-analysis')
        
        return ','.join(labels)
    
    def run_full_workflow(self):
        """Run the complete link checking workflow."""
        self.log('INFO', 'IT-Journey Link Health Guardian v2.0')
        self.log('INFO', '=' * 50)
        
        # Step 1: Install dependencies (only on systems that need it)
        if not self.config.get('skip_install', False):
            if not self.install_dependencies():
                self.log('ERROR', 'Failed to install dependencies')
                return False
        
        # Step 2: Run link checking
        if self.config.get('analysis_level') != 'ai-only':
            if not self.run_link_check():
                self.log('ERROR', 'Link checking failed')
                return False
            
            if not self.parse_lychee_results():
                self.log('WARNING', 'Failed to parse link check results, but continuing...')
                # Create minimal results for continuation
                self.results = {
                    'total_links': 0,
                    'successful_links': 0,
                    'broken_links': 0,
                    'success_rate': 100.0,
                    'raw_data': {}
                }
        else:
            self.log('INFO', 'Skipping link checking (AI-only mode)')
        
        # Step 3: Analyze results (if analysis level requires it)
        analysis_level = self.config.get('analysis_level', 'comprehensive')
        if analysis_level in ['standard', 'comprehensive']:
            if not self.analyze_link_failures():
                self.log('WARNING', 'Analysis failed but continuing...')
        
        # Step 4: Run AI analysis (if enabled and level requires it)
        if analysis_level in ['comprehensive', 'ai-only']:
            if not self.run_ai_analysis():
                self.log('WARNING', 'AI analysis failed but continuing...')
        
        # Step 5: Create GitHub issue (if enabled)
        if self.config.get('create_issue', False):
            if not self.create_github_issue():
                self.log('WARNING', 'GitHub issue creation failed but continuing...')
        
        # Final summary
        self.log('INFO', 'Workflow Summary:')
        if hasattr(self, 'results') and self.results:
            self.log('INFO', f'  Total links: {self.results.get("total_links", 0)}')
            self.log('INFO', f'  Broken links: {self.results.get("broken_links", 0)}')
            self.log('INFO', f'  Success rate: {self.results.get("success_rate", 0)}%')
        
        self.log('SUCCESS', 'Link Health Guardian workflow completed!')
        
        # Return appropriate exit code
        if hasattr(self, 'results') and self.results.get('broken_links', 0) > 0:
            return False  # Indicate broken links found
        return True


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description='IT-Journey Link Health Guardian v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 link-checker.py --scope website --analysis-level comprehensive
    python3 link-checker.py --scope docs --analysis-level basic --no-ai
    python3 link-checker.py --scope posts --create-issue --timeout 60
    python3 link-checker.py --analysis-level ai-only --ai-analysis
        """
    )
    
    # Core options
    parser.add_argument('--scope', default='website',
                       choices=['website', 'internal', 'external', 'docs', 'posts', 'quests', 'all'],
                       help='Scope of link checking')
    
    parser.add_argument('--analysis-level', default='comprehensive',
                       choices=['basic', 'standard', 'comprehensive', 'ai-only'],
                       help='Level of analysis to perform')
    
    parser.add_argument('--output-dir', default='link-check-results',
                       help='Output directory for results')
    
    # Link checking options
    parser.add_argument('--timeout', type=int, default=30,
                       help='Request timeout in seconds')
    
    parser.add_argument('--max-retries', type=int, default=3,
                       help='Maximum retry attempts for failed links')
    
    parser.add_argument('--follow-redirects', action='store_true', default=True,
                       help='Follow HTTP redirects')
    
    parser.add_argument('--no-follow-redirects', dest='follow_redirects', action='store_false',
                       help='Do not follow HTTP redirects')
    
    # Analysis options
    parser.add_argument('--ai-analysis', action='store_true', default=True,
                       help='Enable AI-powered analysis')
    
    parser.add_argument('--no-ai', dest='ai_analysis', action='store_false',
                       help='Disable AI-powered analysis')
    
    # GitHub integration
    parser.add_argument('--create-issue', action='store_true', default=False,
                       help='Create GitHub issue with results')
    
    parser.add_argument('--repository',
                       help='Repository in format owner/repo')
    
    # System options
    parser.add_argument('--skip-install', action='store_true',
                       help='Skip dependency installation')
    
    args = parser.parse_args()
    
    # Convert args to config dict
    config = {
        'scope': args.scope,
        'analysis_level': args.analysis_level,
        'output_dir': args.output_dir,
        'timeout': args.timeout,
        'max_retries': args.max_retries,
        'follow_redirects': args.follow_redirects,
        'ai_analysis': args.ai_analysis,
        'create_issue': args.create_issue,
        'repository': args.repository,
        'skip_install': args.skip_install
    }
    
    # Run the workflow
    guardian = LinkHealthGuardian(config)
    success = guardian.run_full_workflow()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()