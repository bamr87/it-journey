#!/usr/bin/env python3
"""
IT-Journey AI Content Reviewer

Vendor-agnostic content review for markdown files.  Extracted from the
``ai-content-review.yml`` GitHub Actions workflow so that the review logic
lives in the repository and the workflow merely orchestrates environment setup.

Usage (CI):
    python scripts/validation/content-reviewer.py \
        --files pages/_posts/2025-01-01-example.md \
        --output /tmp/ai_review_results.json \
        --summary /tmp/review_summary.md

Usage (local):
    python scripts/validation/content-reviewer.py \
        --files pages/_posts/*.md --dry-run

Environment Variables:
    AI_PROVIDER         - "openai", "anthropic", or "none" (default: "none")
    AI_MODEL            - Model override (e.g. "gpt-4o-mini", "claude-sonnet-4-20250514")
    OPENAI_API_KEY      - Required when AI_PROVIDER=openai
    ANTHROPIC_API_KEY   - Required when AI_PROVIDER=anthropic
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

# Allow importing shared AIClient from scripts/lib/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "lib"))
try:
    from ai_client import AIClient
except ImportError:
    AIClient = None  # type: ignore[assignment,misc]


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, ".github", "content-review-config.yml"
)


def load_review_config(path: Optional[str] = None) -> Dict[str, Any]:
    """Load the content-review-config.yml file (if available)."""
    config_path = path or DEFAULT_CONFIG_PATH
    if yaml is None:
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except FileNotFoundError:
        return {}


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------

def extract_frontmatter_and_content(file_path: str) -> Tuple[Dict[str, Any], str]:
    """Extract YAML frontmatter and body content from a markdown file."""
    try:
        text = Path(file_path).read_text(encoding="utf-8")
    except Exception as exc:
        print(f"  ⚠ Error reading {file_path}: {exc}")
        return {}, ""

    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2 and yaml is not None:
            try:
                fm = yaml.safe_load(parts[0][4:])
                return (fm if fm else {}), parts[1]
            except Exception:
                pass
    return {}, text


# ---------------------------------------------------------------------------
# Local (non-AI) review logic
# ---------------------------------------------------------------------------

def local_review(
    frontmatter: Dict[str, Any],
    body: str,
    filename: str,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Run lightweight rule-based checks that do not require an AI provider."""
    required = config.get("required_fields", [
        "title", "description", "date", "author", "categories", "tags",
    ])
    recommended = config.get("recommended_fields", [
        "excerpt", "lastmod", "draft", "keywords",
    ])
    seo = config.get("seo", {})
    quality = config.get("quality_thresholds", {})

    fm_issues: List[str] = []
    content_suggestions: List[str] = []
    seo_improvements: List[str] = []
    positive: List[str] = []

    # Frontmatter checks
    for field in required:
        if field not in frontmatter:
            fm_issues.append(f"Missing required field: {field}")
    for field in recommended:
        if field not in frontmatter:
            fm_issues.append(f"Missing recommended field: {field}")
    if not fm_issues:
        positive.append("All required frontmatter fields present")

    # Title length
    title = frontmatter.get("title", "")
    tmin = seo.get("title_min_length", 30)
    tmax = seo.get("title_max_length", 60)
    if title and len(title) < tmin:
        seo_improvements.append(f"Title too short ({len(title)} chars, min {tmin})")
    elif title and len(title) > tmax:
        seo_improvements.append(f"Title too long ({len(title)} chars, max {tmax})")

    # Description length
    desc = frontmatter.get("description", "")
    dmin = seo.get("description_min_length", 120)
    dmax = seo.get("description_max_length", 160)
    if desc and len(desc) < dmin:
        seo_improvements.append(f"Description too short ({len(desc)} chars, min {dmin})")
    elif desc and len(desc) > dmax:
        seo_improvements.append(f"Description too long ({len(desc)} chars, max {dmax})")

    # Word count
    words = body.split()
    wmin = quality.get("min_word_count", 100)
    wmax = quality.get("max_word_count", 3000)
    if len(words) < wmin:
        content_suggestions.append(f"Content seems short ({len(words)} words, min {wmin})")
    elif len(words) > wmax:
        content_suggestions.append(f"Content is very long ({len(words)} words) — consider splitting")
    else:
        positive.append(f"Good content length ({len(words)} words)")

    # Heading structure
    headings = re.findall(r"^#+\s", body, re.MULTILINE)
    hmin = quality.get("min_headers", 1)
    if len(headings) < hmin:
        content_suggestions.append(f"Only {len(headings)} heading(s) found (recommend ≥{hmin})")
    else:
        positive.append(f"Good heading structure ({len(headings)} headings)")

    # Simple score
    total_issues = len(fm_issues) + len(content_suggestions) + len(seo_improvements)
    score = max(1, 10 - total_issues)

    return {
        "overall_score": score,
        "frontmatter_issues": fm_issues,
        "content_suggestions": content_suggestions,
        "seo_improvements": seo_improvements,
        "technical_issues": [],
        "positive_aspects": positive,
        "action_items": (fm_issues + content_suggestions + seo_improvements)[:5],
        "review_type": "local",
    }


# ---------------------------------------------------------------------------
# AI-enhanced review
# ---------------------------------------------------------------------------

_REVIEW_PROMPT_TEMPLATE = """\
You are an expert content reviewer for a technical blog/documentation site called "IT-Journey".
Please review the following markdown file and provide feedback on:

1. **Frontmatter completeness**: Check if required fields are present and properly formatted
2. **Content quality**: Assess writing quality, structure, and technical accuracy
3. **SEO optimization**: Suggest improvements for discoverability
4. **Accessibility**: Check for proper heading structure and alt text
5. **Technical accuracy**: Review any code examples or technical content

Required frontmatter fields: {required}
Preferred frontmatter fields: {recommended}

File: {filename}
Content:
{content}

Please provide a JSON response with the following structure:
{{
  "overall_score": <1-10>,
  "frontmatter_issues": ["list of issues"],
  "content_suggestions": ["list of suggestions"],
  "seo_improvements": ["list of SEO suggestions"],
  "technical_issues": ["list of technical issues"],
  "positive_aspects": ["list of good things"],
  "action_items": ["prioritized list of actions to take"]
}}
"""


def ai_review(
    full_content: str,
    filename: str,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Call the shared AIClient to get an AI-powered review."""
    if AIClient is None:
        return {"error": "AIClient not available — install scripts/lib/ai_client.py"}

    ai_cfg = config.get("ai_review", {})
    provider = ai_cfg.get("provider", os.environ.get("AI_PROVIDER", "none"))
    model = ai_cfg.get("model")  # None → AIClient uses env var or default

    client = AIClient(
        provider=provider,
        model=model,
        timeout=60,
    )

    required = ", ".join(config.get("required_fields", []))
    recommended = ", ".join(config.get("recommended_fields", []))

    # Truncate very large files to stay within token limits
    max_chars = 12000
    truncated = full_content[:max_chars]
    if len(full_content) > max_chars:
        truncated += "\n\n[... content truncated for review ...]"

    prompt = _REVIEW_PROMPT_TEMPLATE.format(
        required=required,
        recommended=recommended,
        filename=filename,
        content=truncated,
    )

    result = client.chat(
        prompt=prompt,
        max_tokens=ai_cfg.get("max_tokens", 1500),
        temperature=ai_cfg.get("temperature", 0.3),
    )

    if not result.success:
        return {"error": f"AI call failed: {result.error}"}

    # Try to extract JSON from the response
    try:
        json_match = re.search(r"\{.*\}", result.content or "", re.DOTALL)
        if json_match:
            review = json.loads(json_match.group())
            review["review_type"] = "ai"
            review["ai_provider"] = result.provider
            review["ai_model"] = result.model
            return review
        return {"error": "No JSON found in AI response", "raw_response": result.content}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in AI response", "raw_response": result.content}


# ---------------------------------------------------------------------------
# Summary generation
# ---------------------------------------------------------------------------

def generate_summary(reviews: Dict[str, Dict[str, Any]]) -> str:
    """Generate a markdown summary from review results."""
    lines: List[str] = []
    lines.append("## 🤖 AI Content Review Summary\n")

    total = len(reviews)
    successful = len([r for r in reviews.values() if "error" not in r])
    lines.append(f"**Files reviewed:** {total}  ")
    lines.append(f"**Successful reviews:** {successful}  \n")

    if successful > 0:
        avg = sum(
            r.get("overall_score", 0) for r in reviews.values() if "error" not in r
        ) / successful
        lines.append(f"**Average quality score:** {avg:.1f}/10\n")

    for fpath, review in reviews.items():
        lines.append(f"### 📄 `{fpath}`\n")

        if "error" in review:
            lines.append(f"❌ **Error:** {review['error']}\n")
            continue

        score = review.get("overall_score", "N/A")
        rtype = review.get("review_type", "unknown")
        lines.append(f"**Quality Score:** {score}/10  ")
        lines.append(f"**Review type:** {rtype}\n")

        if review.get("positive_aspects"):
            lines.append("**✅ Positive Aspects:**")
            for a in review["positive_aspects"]:
                lines.append(f"- {a}")
            lines.append("")

        if review.get("action_items"):
            lines.append("**🎯 Priority Action Items:**")
            for item in review["action_items"][:3]:
                lines.append(f"- {item}")
            lines.append("")

        if review.get("frontmatter_issues"):
            lines.append("**⚠️ Frontmatter Issues:**")
            for issue in review["frontmatter_issues"]:
                lines.append(f"- {issue}")
            lines.append("")

        lines.append("---\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="AI Content Reviewer — vendor-agnostic markdown review",
    )
    p.add_argument(
        "--files", nargs="*", default=[],
        help="Markdown files to review (also reads CHANGED_FILES env var)",
    )
    p.add_argument(
        "--output", default="/tmp/ai_review_results.json",
        help="Path to write JSON review results",
    )
    p.add_argument(
        "--summary", default="/tmp/review_summary.md",
        help="Path to write markdown summary",
    )
    p.add_argument(
        "--config", default=None,
        help="Path to content-review-config.yml",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Run local checks only, skip AI calls",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    config = load_review_config(args.config)

    # Collect files from CLI args + CHANGED_FILES env var
    files: List[str] = list(args.files)
    env_files = os.environ.get("CHANGED_FILES", "")
    for f in env_files.split("\n"):
        f = f.strip()
        if f and f not in files:
            files.append(f)

    if not files:
        print("No files to review.")
        return 0

    ai_cfg = config.get("ai_review", {})
    provider = ai_cfg.get("provider", os.environ.get("AI_PROVIDER", "none"))
    use_ai = provider != "none" and not args.dry_run

    print(f"Content Reviewer — provider={provider}, ai={'on' if use_ai else 'off'}, files={len(files)}")

    reviews: Dict[str, Dict[str, Any]] = {}
    for fpath in files:
        if not os.path.exists(fpath):
            print(f"  ⚠ Skipping {fpath} (not found)")
            continue

        print(f"  Reviewing: {fpath}")
        fm, body = extract_frontmatter_and_content(fpath)

        # Always run local checks
        review = local_review(fm, body, fpath, config)

        # Optionally enhance with AI
        if use_ai and yaml is not None:
            full = f"---\n{yaml.dump(fm)}---\n{body}"
            ai_result = ai_review(full, fpath, config)
            if "error" not in ai_result:
                review = ai_result  # AI review replaces local review
            else:
                review["ai_error"] = ai_result.get("error")

        reviews[fpath] = review
        score = review.get("overall_score", "N/A")
        rtype = review.get("review_type", "local")
        print(f"    Score: {score}/10 ({rtype})")

    # Write results
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(reviews, fh, indent=2)
    print(f"Results written to {args.output}")

    # Write summary
    summary = generate_summary(reviews)
    with open(args.summary, "w", encoding="utf-8") as fh:
        fh.write(summary)
    print(f"Summary written to {args.summary}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
