#!/usr/bin/env python3
"""
Documentation Transformer — Jekyll Frontmatter & Content Normalization

Reads raw documentation files staged by aggregate.py, generates
it-journey-compatible Jekyll frontmatter, rewrites links, and writes
the final output into pages/_docs/<category>/<source>/.

Also generates a navigation YAML fragment for _data/navigation/docs.yml.

Usage:
    python3 transform.py [--work-dir ../../work/docs-aggregator] [--output-dir ../../pages/_docs]
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Split YAML frontmatter from body.  Returns ({}, body) if none found."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("---", 3)
    if end == -1:
        return {}, content
    try:
        fm = yaml.safe_load(content[3:end]) or {}
    except yaml.YAMLError:
        fm = {}
    body = content[end + 3:].lstrip("\n")
    return fm, body


def extract_title(fm: Dict, body: str, filename: str) -> str:
    """Determine a page title from frontmatter, H1, or filename."""
    if fm.get("title"):
        return str(fm["title"])
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return Path(filename).stem.replace("-", " ").replace("_", " ").title()


def extract_description(fm: Dict, body: str) -> str:
    """Build a short description from existing frontmatter or first paragraph."""
    if fm.get("description"):
        return str(fm["description"])
    # Strip headings and blank lines, grab first real paragraph
    for para in body.split("\n\n"):
        text = para.strip()
        if text and not text.startswith("#") and not text.startswith("```"):
            # Clean markdown
            text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
            text = re.sub(r"[`*_]", "", text)
            text = text.strip()
            if len(text) > 20:
                return text[:250] + ("..." if len(text) > 250 else "")
    return ""


def build_jekyll_frontmatter(
    source_meta: Dict,
    existing_fm: Dict,
    body: str,
    rel_path: Path,
    filename: str,
) -> Dict[str, Any]:
    """Build a complete it-journey-compatible frontmatter dict."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    title = extract_title(existing_fm, body, filename)
    description = extract_description(existing_fm, body)

    source_name = source_meta["name"]
    category = source_meta["category"]
    repo_url = source_meta["repo"]
    branch = source_meta.get("branch", "main") or "main"
    source_tags = source_meta.get("tags", [])

    # Build permalink from category and relative path
    # e.g. wargames/bandit/index.md → /docs/wargames/bandit/
    parts = list(rel_path.parent.parts) if rel_path.parent != Path(".") else []
    slug = rel_path.stem
    if slug == "index":
        permalink = f"/docs/{category}/" + "/".join(parts) + ("/" if parts else "")
    else:
        permalink = f"/docs/{category}/" + "/".join(parts + [slug]) + "/"

    # Build source URL pointing to the file on GitHub
    source_file_path = "/".join(rel_path.parts)
    source_url = f"{repo_url.rstrip('/')}/blob/{branch}/{source_file_path}"

    fm: Dict[str, Any] = {
        "title": title,
        "description": description,
        "permalink": permalink,
        "date": existing_fm.get("date", now),
        "lastmod": now,
        "categories": [category],
        "tags": list(dict.fromkeys(source_tags + existing_fm.get("tags", []))),
        "sidebar": {"nav": "docs"},
        "toc_sticky": True,
        "source_repo": repo_url,
        "source_url": source_url,
        "source_name": source_name,
        "license": source_meta.get("license", ""),
    }
    return fm


# ---------------------------------------------------------------------------
# Content transformation
# ---------------------------------------------------------------------------

def rewrite_relative_links(body: str, repo_url: str, branch: str, content_base: str) -> str:
    """Rewrite relative markdown links to point to the source repository on GitHub."""

    def _rewrite(match: re.Match) -> str:
        text = match.group(1)
        href = match.group(2)
        # Skip absolute URLs, anchors, mailto
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return match.group(0)
        # Build GitHub URL
        clean = href.lstrip("./")
        gh_url = f"{repo_url.rstrip('/')}/blob/{branch}/{content_base.rstrip('/')}/{clean}"
        return f"[{text}]({gh_url})"

    return re.sub(r"\[([^\]]*)\]\(([^)]+)\)", _rewrite, body)


def strip_jekyll_includes(body: str) -> str:
    """Remove Jekyll {% include ... %} tags that won't work outside the source site."""
    return re.sub(r"\{%\s*include\s+[^%]+%\}", "", body)


def add_source_attribution(body: str, source_meta: Dict) -> str:
    """Prepend a source attribution banner to the body."""
    repo_url = source_meta["repo"]
    license_text = source_meta.get("license", "")
    license_url = source_meta.get("license_url", "")
    lic = f" ([{license_text}]({license_url}))" if license_text and license_url else ""

    banner = (
        f"> **Source:** This content is aggregated from "
        f"[{source_meta['name']}]({repo_url}){lic}. "
        f"Visit the original repository for the latest version.\n\n"
    )
    return banner + body


def transform_file(
    raw_path: Path,
    output_path: Path,
    source_meta: Dict,
    rel_path: Path,
) -> bool:
    """Transform a single raw file and write to output."""
    try:
        content = raw_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"    [ERR] Cannot read {raw_path}: {e}")
        return False

    existing_fm, body = parse_frontmatter(content)

    # Build new frontmatter
    fm = build_jekyll_frontmatter(source_meta, existing_fm, body, rel_path, raw_path.name)

    # Transform body
    branch = source_meta.get("branch", "main") or "main"
    content_base = source_meta.get("content_paths", [""])[0] if "content_paths" in source_meta else ""
    body = strip_jekyll_includes(body)
    body = rewrite_relative_links(body, source_meta["repo"], branch, content_base)
    body = add_source_attribution(body, source_meta)

    # Serialize
    fm_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    final = f"---\n{fm_str}---\n\n{body}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Navigation generation
# ---------------------------------------------------------------------------

def generate_nav_fragment(
    source_meta: Dict,
    output_dir: Path,
    category: str,
) -> Dict:
    """Build a navigation entry dict for this source's content."""
    # Discover generated pages
    cat_dir = output_dir / category / source_meta["name"]
    pages: List[Dict[str, str]] = []
    if cat_dir.exists():
        for md in sorted(cat_dir.rglob("*.md")):
            rel = md.relative_to(cat_dir)
            # Read title from frontmatter
            try:
                content = md.read_text(encoding="utf-8", errors="replace")
                fm, _ = parse_frontmatter(content)
                title = fm.get("title", rel.stem.replace("-", " ").title())
                url = fm.get("permalink", f"/docs/{category}/{source_meta['name']}/{rel.stem}/")
            except Exception:
                title = rel.stem.replace("-", " ").title()
                url = f"/docs/{category}/{source_meta['name']}/{rel.stem}/"
            pages.append({"title": title, "url": url})

    nav_entry = {
        "title": source_meta["name"].replace("-", " ").title(),
        "url": f"/docs/{category}/",
        "icon": "bi-globe",
        "children": pages,
    }
    return nav_entry


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Transform raw docs into Jekyll pages")
    parser.add_argument(
        "--work-dir",
        default=str(Path(__file__).resolve().parents[1].parent / "work" / "docs-aggregator"),
        help="Working directory containing manifest.yml and raw/",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parents[1].parent / "pages" / "_docs"),
        help="Output directory (pages/_docs/)",
    )
    parser.add_argument(
        "--nav-output",
        default=None,
        help="Path to write generated navigation YAML fragment",
    )
    args = parser.parse_args()

    work = Path(args.work_dir)
    output_dir = Path(args.output_dir)
    manifest_path = work / "manifest.yml"

    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}")
        print("Run aggregate.py first.")
        sys.exit(1)

    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    sources = manifest.get("sources", [])
    if not sources:
        print("No sources in manifest.")
        sys.exit(0)

    print(f"=== Documentation Transformer ===")
    print(f"Work   : {work}")
    print(f"Output : {output_dir}")
    print(f"Sources: {len(sources)}\n")

    nav_fragments: List[Dict] = []

    for source in sources:
        name = source["name"]
        category = source["category"]
        raw_source_dir = Path(source["raw_dir"])

        print(f"[{name}] → pages/_docs/{category}/{name}/")

        if not raw_source_dir.exists():
            print(f"  [SKIP] Raw directory not found: {raw_source_dir}")
            continue

        dest_dir = output_dir / category / name
        transformed = 0
        failed = 0

        for raw_file in sorted(raw_source_dir.rglob("*.md")):
            rel = raw_file.relative_to(raw_source_dir)
            out_file = dest_dir / rel
            ok = transform_file(raw_file, out_file, source, rel)
            if ok:
                transformed += 1
                print(f"    ✓ {rel}")
            else:
                failed += 1
                print(f"    ✗ {rel}")

        print(f"  Transformed: {transformed}  |  Failed: {failed}\n")

        # Build nav fragment
        nav_entry = generate_nav_fragment(source, output_dir, category)
        nav_fragments.append(nav_entry)

    # Write navigation fragment
    nav_out = Path(args.nav_output) if args.nav_output else work / "nav_fragment.yml"
    with open(nav_out, "w") as f:
        yaml.dump(nav_fragments, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"Navigation fragment written to {nav_out}")

    print("\n=== Transformation complete ===")


if __name__ == "__main__":
    main()
