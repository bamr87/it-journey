#!/usr/bin/env python3
"""
AI Analyzer - Hyperlink Guardian Intelligence Engine
Part of the IT-Journey Testing Framework

This script provides intelligent analysis of hyperlink health scan results
using OpenAI's GPT-4 to identify patterns, root causes, and recommendations.
"""

import json
import os
import sys
import logging
import argparse
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import re
from urllib.parse import urlparse
from pathlib import Path

# Version information
__version__ = "2.0.0"
__author__ = "IT-Journey Testing Framework"

# Get script directory and project root
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PROJECT_ROOT / 'test-results' / 'artifacts' / 'ai-analyzer.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

try:
    import openai
    import requests
except ImportError as e:
    logger.info(f"Installing required packages: {e.name}")
    import subprocess
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "openai", "requests", "pyyaml", "--break-system-packages"
    ])
    import openai
    import requests
    import yaml

class HyperlinkIntelligenceEngine:
    """
    Advanced AI-powered analysis engine for hyperlink health intelligence
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4", config_file: Optional[str] = None):
        """Initialize the intelligence engine with OpenAI configuration"""
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.analysis_timestamp = datetime.utcnow()
        self.config = self.load_config(config_file)
        
        # Override model from config if specified
        if self.config.get('ai_analysis', {}).get('model'):
            self.model = self.config['ai_analysis']['model']
            
        logger.info(f"Initialized Hyperlink Intelligence Engine v{__version__}")
        logger.info(f"Using model: {self.model}")
    
    def load_config(self, config_file: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from YAML or JSON file"""
        config = {}
        
        # Determine config file to use
        if config_file and Path(config_file).exists():
            config_path = Path(config_file)
        elif (CONFIG_DIR / "guardian-config.yml").exists():
            config_path = CONFIG_DIR / "guardian-config.yml"
        elif (CONFIG_DIR / "test-config.json").exists():
            config_path = CONFIG_DIR / "test-config.json"
        else:
            logger.warning("No configuration file found, using defaults")
            return config
        
        try:
            logger.info(f"Loading AI analyzer configuration from: {config_path}")
            
            if config_path.suffix in ['.yml', '.yaml']:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f) or {}
            elif config_path.suffix == '.json':
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
            logger.info("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            
        return config
    
    def load_scan_data(self, input_dir: str) -> Dict[str, Any]:
        """Load all scan data and context for analysis"""
        logger.info(f"Loading scan data from: {input_dir}")
        input_path = Path(input_dir)
        
        try:
            scan_data = {
                'analysis_timestamp': self.analysis_timestamp.isoformat()
            }
            
            # Load primary scan results (new format)
            summary_file = input_path / "summary.json"
            if summary_file.exists():
                with open(summary_file, 'r') as f:
                    scan_data['summary'] = json.load(f)
                logger.info("Loaded comprehensive summary")
            else:
                logger.warning("No summary.json found, creating basic summary")
                scan_data['summary'] = {
                    'summary_statistics': {'broken_links': 0, 'total_links': 0},
                    'broken_link_details': []
                }
            
            # Load broken links analysis (new format)
            broken_links_file = input_path / "broken-links.json"
            if broken_links_file.exists():
                with open(broken_links_file, 'r') as f:
                    scan_data['broken_links_detailed'] = json.load(f)
                logger.info("Loaded detailed broken links analysis")
            else:
                scan_data['broken_links_detailed'] = []
            
            # Load repository context
            context_file = input_path / "repository_context.json"
            if context_file.exists():
                with open(context_file, 'r') as f:
                    scan_data['repository_context'] = json.load(f)
                logger.info("Loaded repository context")
            else:
                # Try to get context from summary
                if 'scan_metadata' in scan_data['summary']:
                    scan_data['repository_context'] = {
                        'repository': 'it-journey',
                        'site_url': scan_data['summary']['scan_metadata'].get('site_url')
                    }
                else:
                    scan_data['repository_context'] = {}
            
            # Load detailed test results for enhanced analysis
            results_file = input_path / "detailed-results.csv"
            if results_file.exists():
                scan_data['detailed_results'] = self._parse_enhanced_csv_results(results_file)
                logger.info(f"Loaded {len(scan_data['detailed_results'])} detailed test results")
            else:
                scan_data['detailed_results'] = []
            
            # Load recent commits if available
            commits_file = input_path / "recent_commits.txt"
            if commits_file.exists():
                with open(commits_file, 'r') as f:
                    scan_data['recent_commits'] = f.read().strip().split('\n')
                logger.info(f"Loaded {len(scan_data['recent_commits'])} recent commits")
            else:
                scan_data['recent_commits'] = []
            
            return scan_data
            
        except Exception as e:
            logger.error(f"Failed to load scan data: {str(e)}")
            raise
    
    def _parse_enhanced_csv_results(self, csv_file: Path) -> List[Dict[str, str]]:
        """Parse enhanced CSV test results with new categorization fields"""
        results = []
        
        with open(csv_file, 'r') as f:
            lines = f.readlines()
            
        # Skip header line and parse enhanced format
        for line in lines[1:]:
            parts = line.strip().split('|')
            if len(parts) >= 10:  # Enhanced format with more fields
                results.append({
                    'timestamp': parts[0],
                    'url': parts[1],
                    'status_code': parts[2],
                    'response_time': parts[3],
                    'status': parts[4],
                    'error_message': parts[5],
                    'source_file': parts[6],
                    'link_category': parts[7],
                    'url_type': parts[8],
                    'error_category': parts[9] if len(parts) > 9 else 'unknown'
                })
            elif len(parts) >= 7:  # Legacy format compatibility
                results.append({
                    'timestamp': parts[0],
                    'url': parts[1],
                    'status_code': parts[2],
                    'response_time': parts[3],
                    'status': parts[4],
                    'error_message': parts[5],
                    'source_file': parts[6],
                    'link_category': 'unknown',
                    'url_type': 'unknown',
                    'error_category': 'unknown'
                })
        
        return results
    
    def categorize_broken_links_enhanced(self, broken_links: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Enhanced categorization with new Guardian 2.0 fields"""
        logger.info("Performing enhanced categorization of broken links")
        
        categories = {
            'external_documentation': [],
            'github_repositories': [],
            'academic_resources': [],
            'commercial_tools': [],
            'social_media': [],
            'internal_links': [],
            'deprecated_services': [],
            'temporary_failures': [],
            'cdn_resources': [],
            'api_endpoints': [],
            'ssl_certificate_issues': [],
            'dns_resolution_failures': [],
            'connection_timeouts': [],
            'unknown': []
        }
        
        for link in broken_links:
            url = link.get('url', '')
            status_code = link.get('status_code', '')
            error_message = link.get('error_message', '')
            error_category = link.get('error_category', 'unknown')
            url_type = link.get('url_type', 'unknown')
            
            # Parse URL for analysis
            try:
                parsed = urlparse(url)
                domain = parsed.netloc.lower()
            except Exception:
                domain = ''
            
            # Enhanced categorization using new fields
            if error_category == 'ssl_error':
                categories['ssl_certificate_issues'].append(link)
            elif error_category == 'dns_error':
                categories['dns_resolution_failures'].append(link)
            elif error_category in ['timeout', 'connection_error', 'connection_refused']:
                categories['connection_timeouts'].append(link)
            elif error_category in ['server_error', 'temporary_failure'] or status_code in ['500', '502', '503', '504']:
                categories['temporary_failures'].append(link)
            elif url_type.startswith('internal'):
                categories['internal_links'].append(link)
            elif any(repo_host in domain for repo_host in ['github.com', 'gitlab.com', 'bitbucket.org']):
                categories['github_repositories'].append(link)
            elif any(doc_site in domain for doc_site in ['docs.', 'documentation.', 'wiki.', 'manual.', 'help.']):
                categories['external_documentation'].append(link)
            elif any(academic in domain for academic in ['.edu', 'arxiv.org', 'scholar.google', 'ieee.org']):
                categories['academic_resources'].append(link)
            elif any(social in domain for social in ['twitter.com', 'linkedin.com', 'facebook.com', 'instagram.com']):
                categories['social_media'].append(link)
            elif any(cdn in domain for cdn in ['cdn.', 'cloudflare.', 'jsdelivr.', 'unpkg.com']):
                categories['cdn_resources'].append(link)
            elif '/api/' in url or 'api.' in domain:
                categories['api_endpoints'].append(link)
            elif status_code == '404':
                categories['deprecated_services'].append(link)
            else:
                categories['unknown'].append(link)
        
        # Remove empty categories and log statistics
        filtered_categories = {k: v for k, v in categories.items() if v}
        
        for category, links in filtered_categories.items():
            logger.info(f"Enhanced category '{category}': {len(links)} links")
        
        return filtered_categories
    
    def identify_enhanced_patterns(self, scan_data: Dict[str, Any]) -> List[str]:
        """Enhanced pattern identification using new categorization data"""
        logger.info("Analyzing enhanced failure patterns")
        
        patterns = []
        broken_links = scan_data.get('broken_links_detailed', scan_data['summary'].get('broken_link_details', []))
        detailed_results = scan_data.get('detailed_results', [])
        
        if not broken_links:
            return patterns
        
        # Enhanced pattern analysis with new fields
        domain_patterns = {}
        error_category_patterns = {}
        url_type_patterns = {}
        source_file_patterns = {}
        link_category_patterns = {}
        
        for link in broken_links:
            # Domain analysis
            try:
                domain = urlparse(link.get('url', '')).netloc
                domain_patterns[domain] = domain_patterns.get(domain, 0) + 1
            except Exception:
                pass
            
            # Error category analysis (new in Guardian 2.0)
            error_cat = link.get('error_category', 'unknown')
            error_category_patterns[error_cat] = error_category_patterns.get(error_cat, 0) + 1
            
            # URL type analysis
            url_type = link.get('url_type', 'unknown')
            url_type_patterns[url_type] = url_type_patterns.get(url_type, 0) + 1
            
            # Source file analysis
            source = link.get('source_file', '')
            if source:
                source_file_patterns[source] = source_file_patterns.get(source, 0) + 1
            
            # Link category analysis
            link_cat = link.get('link_category', 'unknown')
            link_category_patterns[link_cat] = link_category_patterns.get(link_cat, 0) + 1
        
        # Generate enhanced pattern insights
        for domain, count in domain_patterns.items():
            if count > 1 and domain:
                patterns.append(f"Multiple failures from domain: {domain} ({count} links)")
        
        for error_cat, count in error_category_patterns.items():
            if count > 2 and error_cat != 'unknown':
                patterns.append(f"Frequent {error_cat} errors ({count} occurrences)")
        
        for url_type, count in url_type_patterns.items():
            if count > 3 and url_type != 'unknown':
                patterns.append(f"High failure rate in {url_type} links ({count} failures)")
        
        for source_file, count in source_file_patterns.items():
            if count > 3:
                patterns.append(f"High failure rate in file: {source_file} ({count} broken links)")
        
        for link_cat, count in link_category_patterns.items():
            if count > 2 and link_cat != 'unknown':
                patterns.append(f"Multiple {link_cat} link failures ({count} occurrences)")
        
        # Performance-based patterns
        if detailed_results:
            slow_responses = [r for r in detailed_results if r.get('response_time') and float(r.get('response_time', 0)) > 5.0]
            if len(slow_responses) > 5:
                patterns.append(f"Performance concern: {len(slow_responses)} links with response time > 5 seconds")
        
        logger.info(f"Identified {len(patterns)} enhanced failure patterns")
        return patterns
    
    def generate_ai_analysis(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive AI analysis with enhanced categorization"""
        logger.info("Starting enhanced AI-powered analysis")
        
        # Use detailed broken links if available, fallback to summary
        broken_links = scan_data.get('broken_links_detailed', scan_data['summary'].get('broken_link_details', []))
        
        if not broken_links:
            return self._create_healthy_analysis(scan_data)
        
        categorized_links = self.categorize_broken_links_enhanced(broken_links)
        identified_patterns = self.identify_enhanced_patterns(scan_data)
        
        # Build enhanced analysis prompt
        analysis_prompt = self._build_enhanced_analysis_prompt(
            scan_data, categorized_links, identified_patterns, broken_links
        )
        
        try:
            # Get AI configuration from config file
            ai_config = self.config.get('ai_analysis', {})
            max_tokens = ai_config.get('max_tokens', 3000)
            temperature = ai_config.get('temperature', 0.3)
            
            logger.info(f"Sending enhanced analysis request to OpenAI (model: {self.model})")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": """You are an expert DevOps engineer, technical writer, and educational content strategist with deep expertise in maintaining high-quality learning platforms. 

Your specialties include:
- Advanced link rot prevention and detection strategies
- Educational content maintenance best practices  
- Technical troubleshooting and root cause analysis
- Automated monitoring and quality assurance systems
- Performance optimization and reliability engineering
- AI-enhanced testing and validation frameworks

Provide actionable, specific, and technically sound recommendations that prioritize educational value, learner experience, and system reliability."""
                    },
                    {
                        "role": "user", 
                        "content": analysis_prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            logger.info("Received enhanced AI analysis response")
            
            # Try to parse as JSON
            analysis_result = self._parse_ai_response(ai_response)
            
            # Add enhanced metadata
            analysis_result['ai_analysis_metadata'] = {
                'model_used': self.model,
                'analysis_timestamp': self.analysis_timestamp.isoformat(),
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 'unknown',
                'broken_links_analyzed': len(broken_links),
                'patterns_identified': len(identified_patterns),
                'categories_found': len(categorized_links),
                'guardian_version': '2.0.0',
                'config_file_used': bool(self.config)
            }
            
            logger.info("Enhanced AI analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Enhanced AI analysis failed: {str(e)}")
            return self._create_enhanced_fallback_analysis(scan_data, categorized_links, identified_patterns)
    
    def _create_healthy_analysis(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create analysis for when no broken links are found"""
        total_links = scan_data['summary'].get('summary_statistics', {}).get('total_links', 0)
        success_rate = scan_data['summary'].get('summary_statistics', {}).get('success_rate', 100)
        
        return {
            "executive_summary": f"Outstanding! All {total_links} links are healthy with {success_rate}% success rate. Your IT-Journey site maintains excellent link integrity.",
            "health_status": "excellent",
            "health_assessment": {
                "overall_grade": "A+",
                "critical_issues": [],
                "educational_impact_level": "none"
            },
            "priority_actions": [
                {
                    "action": "Continue proactive monitoring with Guardian 2.0",
                    "priority": "low",
                    "effort": "low", 
                    "impact": "medium",
                    "educational_benefit": "Maintains reliable access to learning resources",
                    "timeline": "ongoing"
                }
            ],
            "preventive_measures": [
                {
                    "measure": "Maintain current automated monitoring frequency",
                    "implementation": "Daily Guardian 2.0 scans are working effectively",
                    "automation_potential": "Fully automated with enhanced categorization",
                    "educational_context": "Ensures uninterrupted learner experience"
                }
            ],
            "educational_impact_assessment": {
                "learner_experience_impact": "Perfect - no disruptions to learning pathways",
                "content_accessibility": "Full access to all educational resources",
                "learning_journey_disruption": "None - all learning paths remain clear",
                "recommendations": ["Continue current monitoring approach"]
            },
            "technical_recommendations": [
                {
                    "recommendation": "Consider implementing historical trend analysis",
                    "justification": "Long-term data helps predict and prevent future issues",
                    "implementation_complexity": "medium",
                    "educational_benefit": "Proactive issue prevention enhances learning reliability"
                }
            ]
        }
    
    def _build_enhanced_analysis_prompt(self, scan_data: Dict[str, Any], categorized_links: Dict[str, List], 
                                      identified_patterns: List[str], broken_links: List[Dict]) -> str:
        """Build comprehensive enhanced analysis prompt for AI"""
        
        repo_context = scan_data.get('repository_context', {})
        summary_stats = scan_data['summary'].get('summary_statistics', {})
        scan_metadata = scan_data['summary'].get('scan_metadata', {})
        
        return f"""
As an expert DevOps engineer and technical content strategist, analyze this comprehensive hyperlink health report for an educational IT platform using Guardian 2.0 enhanced categorization.

ENHANCED CONTEXT:
- Repository: {repo_context.get('repository', 'Unknown')}
- Site URL: {scan_metadata.get('site_url', 'Unknown')}
- Total Links: {summary_stats.get('total_links', 0)}
- Working Links: {summary_stats.get('working_links', 0)}
- Broken Links: {summary_stats.get('broken_links', 0)}
- Redirects: {summary_stats.get('redirects', 0)}
- Success Rate: {summary_stats.get('success_rate', 0)}%
- Average Response Time: {summary_stats.get('average_response_time', 'Unknown')}s
- Scan Time: {scan_metadata.get('scan_timestamp', 'Unknown')}
- Guardian Version: {scan_metadata.get('guardian_version', '2.0.0')}

PLATFORM DETAILS:
- This is a Jekyll-based GitHub Pages educational site about IT learning journeys
- The site contains technical documentation, tutorials, learning quests, and educational content
- Links may reference external documentation, GitHub repositories, educational tools, or internal content
- This platform focuses on democratizing IT education through open-source principles
- Guardian 2.0 provides enhanced categorization and error analysis

ENHANCED BROKEN LINKS CATEGORIZATION:
{json.dumps(categorized_links, indent=2)}

ADVANCED FAILURE PATTERNS IDENTIFIED:
{json.dumps(identified_patterns, indent=2)}

DETAILED BROKEN LINK ANALYSIS (first 15 with enhanced data):
{json.dumps(broken_links[:15], indent=2)}

RECENT REPOSITORY ACTIVITY:
{json.dumps(scan_data.get('recent_commits', [])[:5], indent=2)}

ENHANCED ANALYSIS REQUIREMENTS:
1. Provide comprehensive executive summary highlighting critical issues, overall health, and Guardian 2.0 improvements
2. Analyze each enhanced category with specific focus on educational impact and technical implications
3. Identify root causes using enhanced error categorization (ssl_error, dns_error, timeout, etc.)
4. Prioritize immediate actions by educational impact, effort, technical complexity, and learner disruption
5. Suggest preventive measures specifically for educational content platforms with Guardian 2.0 capabilities
6. Assess how broken links affect learner experience, educational outcomes, and platform reliability
7. Provide technical recommendations for maintaining link health at scale with enhanced monitoring
8. Consider performance implications and response time patterns
9. Evaluate the effectiveness of Guardian 2.0's enhanced categorization
10. Recommend monitoring enhancements and automation improvements

RESPONSE FORMAT:
Respond in valid JSON format with this exact structure:

{{
  "executive_summary": "Comprehensive overview highlighting key issues, Guardian 2.0 enhancements, and overall platform health",
  "health_assessment": {{
    "overall_grade": "A+|A|B|C|D|F",
    "critical_issues": ["list of most urgent problems requiring immediate attention"],
    "educational_impact_level": "none|low|medium|high|critical",
    "guardian_effectiveness": "Assessment of Guardian 2.0's enhanced categorization and detection"
  }},
  "category_analysis": {{
    "category_name": {{
      "impact": "high|medium|low",
      "educational_significance": "How this category affects learning outcomes",
      "root_cause": "Primary technical reason for failures in this category",
      "recommended_actions": ["specific_action1", "specific_action2"],
      "timeline": "immediate|short-term|long-term",
      "guardian_insight": "How Guardian 2.0's categorization helps with this issue"
    }}
  }},
  "priority_actions": [
    {{
      "action": "Specific actionable task",
      "priority": "high|medium|low",
      "effort": "low|medium|high",
      "impact": "high|medium|low",
      "educational_benefit": "How this specifically helps learners",
      "timeline": "immediate|short-term|long-term",
      "implementation_steps": ["step1", "step2", "step3"]
    }}
  ],
  "preventive_measures": [
    {{
      "measure": "Preventive action description",
      "implementation": "How to implement this measure",
      "automation_potential": "Can this be automated? How with Guardian 2.0?",
      "educational_context": "Why this is important for learning platforms"
    }}
  ],
  "educational_impact_assessment": {{
    "learner_experience_impact": "Detailed assessment of how broken links affect students",
    "content_accessibility": "Analysis of content availability and reachability",
    "learning_journey_disruption": "How failures interrupt educational progression",
    "recommendations": ["learner-focused improvements with Guardian 2.0"]
  }},
  "technical_recommendations": [
    {{
      "recommendation": "Technical improvement suggestion",
      "justification": "Why this is important for educational platforms",
      "implementation_complexity": "low|medium|high",
      "educational_benefit": "How this improves learning outcomes",
      "guardian_integration": "How this works with Guardian 2.0 capabilities"
    }}
  ],
  "monitoring_enhancements": [
    {{
      "enhancement": "Monitoring improvement suggestion",
      "rationale": "Why this is needed for educational content",
      "implementation": "How to implement with Guardian 2.0",
      "automation_potential": "Level of automation possible"
    }}
  ],
  "guardian_assessment": {{
    "categorization_effectiveness": "Assessment of Guardian 2.0's enhanced categorization",
    "detection_improvements": "How the new system improves issue detection",
    "recommended_enhancements": ["suggestions for further Guardian improvements"]
  }}
}}

Focus on actionable insights that leverage Guardian 2.0's enhanced capabilities, maintain educational value, improve learner experience, and ensure reliable access to learning resources.
        """
    
    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI response with enhanced fallback handling"""
        try:
            # Try to parse as direct JSON
            return json.loads(ai_response)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', ai_response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # If JSON parsing fails completely, return structured fallback
            logger.warning("Failed to parse AI response as JSON, using enhanced structured fallback")
            return {
                "executive_summary": "Enhanced AI analysis completed with parsing challenges - Guardian 2.0 data available",
                "raw_analysis": ai_response,
                "analysis_status": "partial_parse_failure", 
                "fallback_analysis": True,
                "guardian_version": "2.0.0"
            }
    
    def _create_enhanced_fallback_analysis(self, scan_data: Dict[str, Any], categorized_links: Dict, 
                                         identified_patterns: List[str]) -> Dict[str, Any]:
        """Create enhanced fallback analysis when AI service fails"""
        broken_count = len(scan_data.get('broken_links_detailed', scan_data['summary'].get('broken_link_details', [])))
        
        return {
            "executive_summary": f"Guardian 2.0 detected {broken_count} broken links with enhanced categorization. Full AI analysis unavailable but detailed categorization provides actionable insights.",
            "fallback_analysis": True,
            "guardian_version": "2.0.0",
            "broken_links_count": broken_count,
            "categories_identified": list(categorized_links.keys()),
            "patterns_identified": identified_patterns,
            "health_assessment": {
                "overall_grade": "C" if broken_count > 10 else "B",
                "critical_issues": [f"{broken_count} broken links requiring attention"],
                "educational_impact_level": "high" if broken_count > 20 else "medium" if broken_count > 5 else "low"
            },
            "priority_actions": [
                {
                    "action": "Review broken links using Guardian 2.0 categorization data",
                    "priority": "high",
                    "effort": "medium",
                    "impact": "high", 
                    "educational_benefit": "Restores access to educational resources",
                    "timeline": "immediate"
                },
                {
                    "action": "Investigate patterns identified by Guardian 2.0",
                    "priority": "medium",
                    "effort": "low",
                    "impact": "medium",
                    "educational_benefit": "Prevents similar future failures",
                    "timeline": "short-term"
                }
            ],
            "preventive_measures": [
                {
                    "measure": "Leverage Guardian 2.0's enhanced monitoring capabilities",
                    "implementation": "Continue daily scans with improved categorization",
                    "automation_potential": "Fully automated with Guardian 2.0 framework",
                    "educational_context": "Proactive detection prevents learner disruption"
                }
            ],
            "educational_impact_assessment": {
                "learner_experience_impact": "Broken links may disrupt learning pathways and access to resources",
                "content_accessibility": "Some educational content may be temporarily inaccessible",
                "learning_journey_disruption": "Link failures can interrupt planned learning sequences",
                "recommendations": ["Use Guardian 2.0 data to prioritize fixes by educational impact"]
            },
            "guardian_assessment": {
                "categorization_effectiveness": "Guardian 2.0 successfully categorized all link failures",
                "detection_improvements": "Enhanced error categorization provides better troubleshooting guidance",
                "recommended_enhancements": ["Configure AI analysis for full intelligent recommendations"]
            },
            "analysis_metadata": {
                "analysis_type": "enhanced_fallback",
                "timestamp": self.analysis_timestamp.isoformat(),
                "categories_found": len(categorized_links),
                "patterns_found": len(identified_patterns),
                "guardian_version": "2.0.0"
            }
        }
    
    def save_analysis_results(self, analysis_result: Dict[str, Any], output_file: str) -> None:
        """Save enhanced analysis results to file"""
        logger.info(f"Saving enhanced analysis results to: {output_file}")
        
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(analysis_result, f, indent=2, default=str)
            logger.info("Enhanced analysis results saved successfully")
        except Exception as e:
            logger.error(f"Failed to save analysis results: {str(e)}")
            raise

def main():
    """Main execution function for enhanced AI analysis"""
    parser = argparse.ArgumentParser(
        description="Enhanced AI-powered hyperlink analysis for Guardian 2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ai-analyzer.py --input ./test-results --output ./ai-analysis.json
  python ai-analyzer.py --verbose --model gpt-3.5-turbo --config custom-config.yml
  python ai-analyzer.py --input /path/to/results --output enhanced-analysis.json
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        default=str(PROJECT_ROOT / 'test-results'),
        help='Input directory containing scan results (default: PROJECT_ROOT/test-results)'
    )
    
    parser.add_argument(
        '--output', '-o', 
        default='./ai-analysis.json',
        help='Output file for analysis results (default: ./ai-analysis.json)'
    )
    
    parser.add_argument(
        '--model', '-m',
        default='gpt-4',
        help='OpenAI model to use for analysis (default: gpt-4)'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Configuration file path (YAML or JSON)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'Guardian 2.0 AI Analyzer v{__version__}'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled")
    
    # Configuration
    input_dir = args.input
    output_file = args.output
    model = args.model
    config_file = args.config
    
    # Check for required environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable is required")
        logger.error("Please set your OpenAI API key:")
        logger.error("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    try:
        # Initialize enhanced AI engine
        logger.info("🧠 Initializing Enhanced Hyperlink Intelligence Engine (Guardian 2.0)...")
        ai_engine = HyperlinkIntelligenceEngine(api_key, model, config_file)
        
        # Load scan data
        logger.info("📂 Loading enhanced scan data...")
        scan_data = ai_engine.load_scan_data(input_dir)
        
        # Check if there are any broken links to analyze
        broken_count = scan_data['summary'].get('summary_statistics', {}).get('broken_links', 0)
        logger.info(f"Found {broken_count} broken links for enhanced analysis")
        
        # Generate enhanced AI analysis
        logger.info("🔍 Generating enhanced AI analysis with Guardian 2.0...")
        analysis_result = ai_engine.generate_ai_analysis(scan_data)
        
        # Save enhanced analysis result
        ai_engine.save_analysis_results(analysis_result, output_file)
        
        # Output summary for GitHub Actions
        logger.info(f"✅ Enhanced analysis complete! Results saved to {output_file}")
        
        # Print key insights for immediate visibility
        if 'executive_summary' in analysis_result:
            print("\n" + "="*70)
            print("🧠 GUARDIAN 2.0 AI ANALYSIS SUMMARY")
            print("="*70)
            print(analysis_result['executive_summary'])
            
            if 'health_assessment' in analysis_result:
                health = analysis_result['health_assessment']
                print(f"\n📊 Health Grade: {health.get('overall_grade', 'Unknown')}")
                print(f"🎯 Educational Impact: {health.get('educational_impact_level', 'Unknown')}")
                print(f"🛡️ Guardian Effectiveness: {health.get('guardian_effectiveness', 'Unknown')}")
            
            if 'guardian_assessment' in analysis_result:
                guardian = analysis_result['guardian_assessment']
                print(f"🔍 Categorization: {guardian.get('categorization_effectiveness', 'Unknown')}")
            
            print("="*70)
        
        return analysis_result
        
    except KeyboardInterrupt:
        logger.info("Enhanced analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Enhanced analysis failed: {str(e)}")
        if args.verbose:
            import traceback
            logger.debug(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 