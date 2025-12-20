#!/usr/bin/env python3
"""
SEO Performance Tracker for IT-Journey

This script helps track SEO metrics and generate reports from data exported 
from Google Search Console. It compares current metrics against baselines 
and identifies opportunities for improvement.

Usage:
    python seo-tracker.py --report weekly
    python seo-tracker.py --baseline
    python seo-tracker.py --compare baseline.csv current.csv
    python seo-tracker.py --opportunities

Requirements:
    pip install pandas tabulate
    
Data Source:
    Export from Google Search Console > Performance > Export
"""

import argparse
import csv
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Try to import optional dependencies
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Note: pandas not installed. Some features limited. Run: pip install pandas")

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


# ============================================================================
# Configuration
# ============================================================================

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEO_DIR = PROJECT_ROOT / "TODO" / "seo"
DATA_DIR = SEO_DIR / "data"

# Baseline metrics (from Google Search Console analysis)
BASELINE_METRICS = {
    "overall": {
        "avg_ctr": 0.7,
        "avg_position": 32,
        "total_impressions": 10000,  # per month estimate
    },
    "pages": {
        "/quests/level-010-nerd-font-enchantment/": {
            "impressions": 755,
            "ctr": 0.7,
            "position": 35,
            "optimized": "2025-12-19"
        },
        "/posts/2024/03/27/bootable-mac-os/": {
            "impressions": 557,
            "ctr": 0.5,
            "position": 40,
            "optimized": "2025-12-19"
        },
        "/posts/django-pi-guide/": {
            "impressions": 461,
            "ctr": 2.2,
            "position": 20,
            "optimized": None  # Already performing well
        },
        "/quests/bashcrawl/": {
            "impressions": 352,
            "ctr": 1.4,
            "position": 25,
            "optimized": None  # Already performing well
        }
    },
    "targets": {
        "ctr": 1.5,  # Target CTR %
        "position": 20,  # Target average position
        "impressions_growth": 20  # Target % growth
    }
}

# New content tracking (Phase 3)
NEW_CONTENT = {
    "/docs/terminal-shortcuts-cheat-sheet/": {
        "title": "Terminal Shortcuts Cheat Sheet",
        "published": "2025-12-20",
        "target_keywords": ["terminal shortcuts", "bash shortcuts", "command line shortcuts"]
    },
    "/posts/essential-vscode-extensions-developers/": {
        "title": "VS Code Extensions Guide",
        "published": "2025-12-20",
        "target_keywords": ["vscode extensions", "best vscode extensions"]
    },
    "/posts/docker-beginners-tutorial/": {
        "title": "Docker Tutorial for Beginners",
        "published": "2025-12-20",
        "target_keywords": ["docker tutorial", "docker for beginners", "learn docker"]
    }
}


# ============================================================================
# Utility Functions
# ============================================================================

def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


def format_percent(value: float) -> str:
    """Format a number as a percentage."""
    return f"{value:.1f}%"


def format_change(current: float, baseline: float) -> str:
    """Format change between two values with color indicator."""
    if baseline == 0:
        return "NEW"
    change = ((current - baseline) / baseline) * 100
    if change > 0:
        return f"↑ {change:.1f}%"
    elif change < 0:
        return f"↓ {abs(change):.1f}%"
    else:
        return "→ 0%"


def simple_table(headers: List[str], rows: List[List]) -> str:
    """Create a simple ASCII table."""
    if HAS_TABULATE:
        return tabulate(rows, headers=headers, tablefmt="pipe")
    
    # Simple fallback
    col_widths = [max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))]
    
    lines = []
    # Header
    lines.append(" | ".join(h.ljust(w) for h, w in zip(headers, col_widths)))
    lines.append("-+-".join("-" * w for w in col_widths))
    # Rows
    for row in rows:
        lines.append(" | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)))
    
    return "\n".join(lines)


# ============================================================================
# Report Generation
# ============================================================================

def generate_baseline_report() -> str:
    """Generate a baseline report from stored metrics."""
    lines = [
        "=" * 60,
        "SEO BASELINE REPORT - IT-Journey",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 60,
        "",
        "## Overall Metrics (Baseline)",
        "",
    ]
    
    overall = BASELINE_METRICS["overall"]
    targets = BASELINE_METRICS["targets"]
    
    headers = ["Metric", "Baseline", "Target", "Gap"]
    rows = [
        ["Average CTR", f"{overall['avg_ctr']}%", f"{targets['ctr']}%", 
         f"{targets['ctr'] - overall['avg_ctr']:.1f}%"],
        ["Average Position", str(overall['avg_position']), str(targets['position']),
         f"{overall['avg_position'] - targets['position']} positions"],
        ["Monthly Impressions", f"{overall['total_impressions']:,}", 
         f"+{targets['impressions_growth']}%", "—"],
    ]
    
    lines.append(simple_table(headers, rows))
    lines.append("")
    
    # Page-level baseline
    lines.append("## Page-Level Baseline")
    lines.append("")
    
    headers = ["Page", "Impressions", "CTR", "Position", "Optimized"]
    rows = []
    for page, metrics in BASELINE_METRICS["pages"].items():
        rows.append([
            page[:40] + "..." if len(page) > 40 else page,
            str(metrics["impressions"]),
            f"{metrics['ctr']}%",
            str(metrics["position"]),
            metrics["optimized"] or "N/A"
        ])
    
    lines.append(simple_table(headers, rows))
    lines.append("")
    
    # New content tracking
    lines.append("## New Content (Phase 3)")
    lines.append("")
    
    headers = ["Content", "Published", "Target Keywords"]
    rows = []
    for url, info in NEW_CONTENT.items():
        rows.append([
            info["title"],
            info["published"],
            ", ".join(info["target_keywords"][:2])
        ])
    
    lines.append(simple_table(headers, rows))
    
    return "\n".join(lines)


def generate_weekly_template() -> str:
    """Generate a weekly review template."""
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    template = f"""# Weekly SEO Review: {week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}

## Data Collection Checklist

- [ ] Export Google Search Console data (Performance > Export)
- [ ] Save to `TODO/seo/data/gsc-{today.strftime('%Y-%m-%d')}.csv`
- [ ] Run comparison: `python scripts/seo-tracker.py --compare`

## Key Metrics This Week

| Metric | Last Week | This Week | Change |
|--------|-----------|-----------|--------|
| Total Impressions | ___ | ___ | ___ |
| Total Clicks | ___ | ___ | ___ |
| Average CTR | ___% | ___% | ___ |
| Average Position | ___ | ___ | ___ |

## Top Performing Pages

| Page | Impressions | CTR | Position |
|------|-------------|-----|----------|
| 1. ___ | ___ | ___% | ___ |
| 2. ___ | ___ | ___% | ___ |
| 3. ___ | ___ | ___% | ___ |

## Pages Needing Attention (High Impressions, Low CTR)

| Page | Impressions | CTR | Action |
|------|-------------|-----|--------|
| 1. ___ | ___ | ___% | ___ |
| 2. ___ | ___ | ___% | ___ |

## New Content Performance

| Content | Impressions | Clicks | Position | Status |
|---------|-------------|--------|----------|--------|
| Terminal Shortcuts | ___ | ___ | ___ | ___ |
| VS Code Extensions | ___ | ___ | ___ | ___ |
| Docker Tutorial | ___ | ___ | ___ | ___ |

## Wins 🎉

- 

## Concerns ⚠️

- 

## Actions for Next Week

1. 
2. 
3. 

## Notes

- 
"""
    return template


def identify_opportunities(data: Optional[Dict] = None) -> str:
    """Identify SEO improvement opportunities."""
    lines = [
        "=" * 60,
        "SEO OPPORTUNITY ANALYSIS",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 60,
        "",
    ]
    
    # High impressions, low CTR opportunities
    lines.append("## High Impressions, Low CTR (Optimize Titles/Descriptions)")
    lines.append("")
    lines.append("These pages get seen but not clicked - improve meta descriptions!")
    lines.append("")
    
    headers = ["Page", "Impressions", "CTR", "Recommendation"]
    rows = []
    
    for page, metrics in BASELINE_METRICS["pages"].items():
        if metrics["impressions"] > 100 and metrics["ctr"] < 1.0:
            rows.append([
                page[:35] + "..." if len(page) > 35 else page,
                str(metrics["impressions"]),
                f"{metrics['ctr']}%",
                "Improve meta description"
            ])
    
    if rows:
        lines.append(simple_table(headers, rows))
    else:
        lines.append("No opportunities found in this category.")
    
    lines.append("")
    
    # Position improvement opportunities
    lines.append("## Position Improvement Opportunities (Position 11-30)")
    lines.append("")
    lines.append("These pages are close to page 1 - small improvements could help!")
    lines.append("")
    
    headers = ["Page", "Position", "Action"]
    rows = []
    
    for page, metrics in BASELINE_METRICS["pages"].items():
        if 11 <= metrics["position"] <= 30:
            rows.append([
                page[:40] + "..." if len(page) > 40 else page,
                str(metrics["position"]),
                "Add internal links, improve content depth"
            ])
    
    if rows:
        lines.append(simple_table(headers, rows))
    else:
        lines.append("No opportunities found in this category.")
    
    lines.append("")
    
    # Content gap recommendations
    lines.append("## Content Gap Recommendations")
    lines.append("")
    lines.append("Based on related searches and competitor analysis:")
    lines.append("")
    
    gaps = [
        ("Python automation tutorials", "Build on Django success"),
        ("Git advanced workflows", "Extend Git basics quest"),
        ("DevOps pipeline tutorials", "Connect Docker content"),
        ("Jekyll themes customization", "Leverage existing Jekyll content"),
    ]
    
    headers = ["Topic", "Rationale"]
    lines.append(simple_table(headers, gaps))
    
    return "\n".join(lines)


# ============================================================================
# Main CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="SEO Performance Tracker for IT-Journey",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python seo-tracker.py --baseline        Show baseline metrics
    python seo-tracker.py --report weekly   Generate weekly review template
    python seo-tracker.py --opportunities   Identify improvement opportunities
    python seo-tracker.py --help            Show this help message
        """
    )
    
    parser.add_argument(
        "--baseline",
        action="store_true",
        help="Generate baseline report from stored metrics"
    )
    
    parser.add_argument(
        "--report",
        choices=["weekly", "monthly"],
        help="Generate report template (weekly or monthly)"
    )
    
    parser.add_argument(
        "--opportunities",
        action="store_true",
        help="Identify SEO improvement opportunities"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: stdout)"
    )
    
    args = parser.parse_args()
    
    # Ensure data directory exists
    ensure_data_dir()
    
    output = ""
    
    if args.baseline:
        output = generate_baseline_report()
    elif args.report == "weekly":
        output = generate_weekly_template()
    elif args.report == "monthly":
        output = "Monthly report template coming soon..."
    elif args.opportunities:
        output = identify_opportunities()
    else:
        parser.print_help()
        return
    
    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output)
        print(f"Report saved to: {output_path}")
    else:
        print(output)


if __name__ == "__main__":
    main()
