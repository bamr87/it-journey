#!/usr/bin/env python3
"""
Create per-collection GitHub issues from AI Content Reviewer results.

Reads the JSON output of ``scripts/validation/content-reviewer.py`` and creates
**one issue per Jekyll collection** (e.g. ``_posts``, ``_quests``, ``_docs``).
Each issue:

  * Lists every reviewed file in that collection with its action items
  * Carries labels ``ai-review``, ``content-improvement``, ``automated``,
    ``collection:<name>``
  * Is assigned to ``Copilot`` (the GitHub Copilot coding agent) so the agent
    opens a draft PR for resolution, guided by
    ``.github/instructions/ai-content-review.instructions.md``
  * Is idempotent: if an open issue with the same title already exists, it is
    updated in place instead of duplicated

Usage (CI):
    GITHUB_TOKEN=... GITHUB_REPOSITORY=owner/repo \\
        python scripts/validation/create-review-issues.py \\
            --results /tmp/ai_review_results.json

Environment variables:
    GITHUB_TOKEN        Required. Token with ``issues: write`` permission.
    GITHUB_REPOSITORY   ``owner/repo`` slug (auto-set in GitHub Actions).
    GITHUB_SHA          Optional commit SHA to reference in the issue body.
    ASSIGN_TO_COPILOT   ``"true"`` (default) to attempt assigning the issue to
                        the Copilot coding agent. Set ``"false"`` to skip.
    COPILOT_ASSIGNEE    Override the Copilot assignee login (default ``Copilot``).
    CREATE_STANDARDS_FOLLOWUP
                        ``"true"`` (default) to upsert a separate issue assigned
                        to Copilot for instruction/prompt hardening follow-up.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Set

API_ROOT = "https://api.github.com"

INSTRUCTIONS_PATH = ".github/instructions/ai-content-review.instructions.md"
INSTRUCTIONS_URL_TEMPLATE = (
    "https://github.com/{repo}/blob/main/" + INSTRUCTIONS_PATH
)
PROMPTS_PATH = ".github/prompts/"
PROMPTS_URL_TEMPLATE = "https://github.com/{repo}/tree/main/" + PROMPTS_PATH

DEFAULT_LABELS = ["ai-review", "content-improvement", "automated"]
UNKNOWN_COLLECTION = "other"
MAX_STANDARDS_GAPS = 20
REVIEW_GAP_FIELDS = (
    "action_items",
    "frontmatter_issues",
    "seo_improvements",
    "technical_issues",
    "accessibility_issues",
)


# ---------------------------------------------------------------------------
# GitHub REST helpers
# ---------------------------------------------------------------------------

def _request(
    method: str,
    url: str,
    token: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Tiny urllib-based GitHub REST helper.

    Returns the decoded JSON body. Raises on HTTP errors with the response body
    included so callers can decide whether to ignore (e.g. "validation failed"
    on optional assignee).
    """
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "it-journey-ai-content-review")
    if data is not None:
        req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"GitHub API {method} {url} → {exc.code}: {err_body}"
        ) from exc


def find_existing_issue(
    repo: str, token: str, title: str
) -> Optional[Dict[str, Any]]:
    """Find an open issue with an exact title match. Returns it or None."""
    # GitHub search API: exact-phrase title match on open issues in this repo.
    # Phrase-quote to avoid token splitting.
    quoted = title.replace('"', '\\"')
    q = f'repo:{repo} is:issue is:open in:title "{quoted}"'
    url = f"{API_ROOT}/search/issues?q={urllib.parse.quote(q)}&per_page=20"
    try:
        result = _request("GET", url, token)
    except RuntimeError as exc:
        print(f"  ⚠ Search failed, will create new: {exc}", file=sys.stderr)
        return None
    for item in result.get("items", []):
        if item.get("title") == title:
            return item
    return None


def create_issue(
    repo: str,
    token: str,
    title: str,
    body: str,
    labels: List[str],
    assignees: List[str],
) -> Dict[str, Any]:
    """Create a new issue. Retries without assignees if assignment fails."""
    url = f"{API_ROOT}/repos/{repo}/issues"
    payload = {
        "title": title,
        "body": body,
        "labels": labels,
        "assignees": assignees,
    }
    try:
        return _request("POST", url, token, payload)
    except RuntimeError as exc:
        # Common failure: assignee not assignable (e.g. Copilot not enabled).
        # Fall back to creating without assignees and warn.
        msg = str(exc)
        if assignees and ("assignee" in msg.lower() or "validation" in msg.lower()):
            print(
                f"  ⚠ Could not assign {assignees}, creating issue unassigned. "
                f"Reason: {msg}",
                file=sys.stderr,
            )
            payload["assignees"] = []
            return _request("POST", url, token, payload)
        raise


def update_issue(
    repo: str,
    token: str,
    number: int,
    body: str,
    labels: List[str],
) -> Dict[str, Any]:
    """Update an existing issue's body and labels in place (idempotent)."""
    url = f"{API_ROOT}/repos/{repo}/issues/{number}"
    payload = {"body": body, "labels": labels, "state": "open"}
    return _request("PATCH", url, token, payload)


def add_assignees(
    repo: str, token: str, number: int, assignees: List[str]
) -> None:
    """Best-effort assignee addition (e.g. re-assign Copilot on update)."""
    if not assignees:
        return
    url = f"{API_ROOT}/repos/{repo}/issues/{number}/assignees"
    try:
        _request("POST", url, token, {"assignees": assignees})
    except RuntimeError as exc:
        print(f"  ⚠ Could not add assignees {assignees}: {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Grouping & body formatting
# ---------------------------------------------------------------------------

def group_by_collection(
    reviews: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Group a flat ``{path: review}`` map by ``review["collection"]``."""
    grouped: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for path, review in reviews.items():
        collection = review.get("collection") or "other"
        grouped.setdefault(collection, {})[path] = review
    return grouped


def _format_list(items: List[Any], bullet: str = "-") -> str:
    if not items:
        return ""
    out: List[str] = []
    for item in items:
        out.append(f"  {bullet} {item}")
    return "\n".join(out)


def format_file_section(path: str, review: Dict[str, Any]) -> str:
    """Render one file's review as a markdown section with task checkboxes."""
    lines: List[str] = []
    score = review.get("overall_score", "N/A")
    rtype = review.get("review_type", "local")
    lines.append(f"### 📄 `{path}`")
    lines.append("")
    lines.append(f"- **Score:** {score}/10 (`{rtype}`)")

    if review.get("ai_error"):
        lines.append(f"- ⚠️ AI review error: {review['ai_error']}")

    action_items = review.get("action_items") or []
    if action_items:
        lines.append("- **Action items:**")
        for item in action_items:
            lines.append(f"  - [ ] {item}")

    fm_issues = review.get("frontmatter_issues") or []
    if fm_issues:
        lines.append("- **Frontmatter:**")
        lines.append(_format_list(fm_issues))

    seo = review.get("seo_improvements") or []
    if seo:
        lines.append("- **SEO:**")
        lines.append(_format_list(seo))

    tech = review.get("technical_issues") or []
    if tech:
        lines.append("- **Technical:**")
        lines.append(_format_list(tech))

    a11y = review.get("accessibility_issues") or []
    if a11y:
        lines.append("- **Accessibility:**")
        lines.append(_format_list(a11y))

    suggestions = review.get("content_suggestions") or []
    if suggestions:
        lines.append("- **Content:**")
        lines.append(_format_list(suggestions))

    positives = review.get("positive_aspects") or []
    if positives:
        lines.append("- **✅ Positive aspects:**")
        lines.append(_format_list(positives))

    lines.append("")
    return "\n".join(lines)


def format_issue_body(
    collection: str,
    reviews: Dict[str, Dict[str, Any]],
    repo: str,
    commit_sha: Optional[str],
) -> str:
    """Build the markdown body for a per-collection issue."""
    total = len(reviews)
    scores = [
        r.get("overall_score") for r in reviews.values()
        if isinstance(r.get("overall_score"), (int, float))
    ]
    avg = (sum(scores) / len(scores)) if scores else None
    ai_count = sum(1 for r in reviews.values() if r.get("review_type") == "ai")

    instructions_link = (
        f"[`{INSTRUCTIONS_PATH}`]({INSTRUCTIONS_URL_TEMPLATE.format(repo=repo)})"
        if repo
        else f"`{INSTRUCTIONS_PATH}`"
    )
    workflow_link = (
        "[`ai-content-review.yml`]"
        f"(https://github.com/{repo}/blob/main/.github/workflows/ai-content-review.yml)"
        if repo
        else "`.github/workflows/ai-content-review.yml`"
    )

    header = [
        f"## 🤖 AI Content Review — `_{collection}` collection",
        "",
        "This issue groups AI Content Reviewer feedback for files in the "
        f"**`_{collection}`** Jekyll collection. It was opened automatically by "
        f"{workflow_link}.",
        "",
        "### How to resolve",
        "",
        f"1. Read the resolution playbook: {instructions_link}",
        "2. Work through the file sections below — each action item is a "
        "checkbox.",
        f"3. Keep changes scoped to **`pages/_{collection}/`** in this PR.",
        f"4. Use a branch named `fix/ai-review-{collection}-<short-slug>`.",
        "5. Tick off items as you commit; reference this issue in the PR with "
        "`Closes #<number>`.",
        "",
        "### Summary",
        "",
        f"- **Files in scope:** {total}",
    ]
    if avg is not None:
        header.append(f"- **Average quality score:** {avg:.1f}/10")
    header.append(f"- **AI-enhanced reviews:** {ai_count} / {total}")
    if commit_sha:
        if repo:
            header.append(
                f"- **Source commit:** [`{commit_sha[:8]}`](https://github.com/{repo}/commit/{commit_sha})"
            )
        else:
            header.append(f"- **Source commit:** `{commit_sha[:8]}`")
    header.append("")
    header.append("---")
    header.append("")

    sections = [
        format_file_section(path, review)
        for path, review in sorted(reviews.items())
    ]

    footer = [
        "---",
        "",
        "> 🛟 **Stuck on an item?** Mark it as `~~skipped~~` in the checklist "
        "with a one-line reason and proceed with the rest. Open a follow-up "
        "issue for ambiguous cases — partial progress is preferred over "
        "blocking the whole collection.",
        "",
        "> 🔁 This issue is updated in place on every workflow run, so the "
        "checklist stays current. Re-running the workflow will not create "
        "duplicates.",
    ]

    return "\n".join(header + sections + footer)


def collect_standards_gaps(reviews: Dict[str, Dict[str, Any]]) -> List[str]:
    """Collect de-duplicated high-signal standards gaps from review output."""
    seen: Set[str] = set()
    gaps: List[str] = []
    for review in reviews.values():
        for field in REVIEW_GAP_FIELDS:
            for item in review.get(field) or []:
                text = str(item).strip()
                if not text:
                    continue
                key = text.lower()
                if key in seen:
                    continue
                seen.add(key)
                gaps.append(text)
                if len(gaps) >= MAX_STANDARDS_GAPS:
                    return gaps
    return gaps


def format_standards_issue_body(
    reviews: Dict[str, Dict[str, Any]],
    repo: str,
    commit_sha: Optional[str],
) -> str:
    """Build the markdown body for the instructions/prompt hardening issue."""
    instructions_link = (
        f"[`{INSTRUCTIONS_PATH}`]({INSTRUCTIONS_URL_TEMPLATE.format(repo=repo)})"
        if repo
        else f"`{INSTRUCTIONS_PATH}`"
    )
    prompts_link = (
        f"[`{PROMPTS_PATH}`]({PROMPTS_URL_TEMPLATE.format(repo=repo)})"
        if repo
        else f"`{PROMPTS_PATH}`"
    )
    collections = sorted(
        {
            (review.get("collection") or UNKNOWN_COLLECTION)
            for review in reviews.values()
        }
    )
    gaps = collect_standards_gaps(reviews)

    lines = [
        "## 🧭 Follow-up Task — Harden Instructions & Prompts",
        "",
        "Create a **separate PR** that updates repository instructions and prompts "
        "so recurring AI content-review misses are prevented going forward.",
        "",
        "### Scope",
        f"- Review rules in {instructions_link}",
        (
            f"- Update prompt(s) under {prompts_link} "
            "that guide AI content creation/review"
        ),
        "- Keep this work in its own PR (do not mix with collection content fixes)",
        "",
        "### Suggested checklist",
        "- [ ] Add or tighten rule text for the recurring misses listed below",
        "- [ ] Update relevant `.github/prompts/*.prompt.md` files to reinforce those rules",
        "- [ ] Add citations to validators/workflows for each new rule",
        "- [ ] Run targeted validation for changed prompt/instruction files",
        "- [ ] Open PR titled `docs(ai-review): harden instructions and prompts`",
        "",
        "### Context from this run",
        f"- Collections reviewed: {', '.join(f'`_{name}`' for name in collections)}",
        f"- Files reviewed: {len(reviews)}",
    ]
    if commit_sha:
        if repo:
            lines.append(
                f"- Source commit: [`{commit_sha[:8]}`](https://github.com/{repo}/commit/{commit_sha})"
            )
        else:
            lines.append(f"- Source commit: `{commit_sha[:8]}`")

    lines.extend(["", "### Recurring gaps to codify", ""])
    if gaps:
        for gap in gaps:
            lines.append(f"- [ ] {gap}")
    else:
        lines.append("- [ ] No explicit gaps found; review low-scoring files and tighten general guidance.")

    lines.extend([
        "",
        "> This issue is auto-updated in place each run; use it as the standing governance task for instruction/prompt hardening.",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--results", default="/tmp/ai_review_results.json",
        help="Path to AI review JSON results file",
    )
    p.add_argument(
        "--repo", default=os.environ.get("GITHUB_REPOSITORY", ""),
        help="owner/repo slug (defaults to $GITHUB_REPOSITORY)",
    )
    p.add_argument(
        "--commit-sha", default=os.environ.get("GITHUB_SHA"),
        help="Commit SHA to reference in the issue body",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be created without calling the GitHub API",
    )
    p.add_argument(
        "--min-files", type=int, default=1,
        help="Only create an issue when a collection has at least N files",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    if not os.path.exists(args.results):
        print(f"No results file at {args.results} — nothing to do.")
        return 0

    with open(args.results, "r", encoding="utf-8") as fh:
        reviews: Dict[str, Dict[str, Any]] = json.load(fh)

    if not reviews:
        print("Results file is empty — nothing to do.")
        return 0

    grouped = group_by_collection(reviews)
    print(
        f"Grouped {len(reviews)} reviews into "
        f"{len(grouped)} collection(s): {sorted(grouped.keys())}"
    )

    token = os.environ.get("GITHUB_TOKEN", "")
    if not args.dry_run and not token:
        print("ERROR: GITHUB_TOKEN is required (or use --dry-run)", file=sys.stderr)
        return 1

    if not args.dry_run and not args.repo:
        print(
            "ERROR: --repo or GITHUB_REPOSITORY is required (or use --dry-run)",
            file=sys.stderr,
        )
        return 1

    assign_copilot = os.environ.get("ASSIGN_TO_COPILOT", "true").lower() == "true"
    copilot_login = os.environ.get("COPILOT_ASSIGNEE", "Copilot")
    assignees = [copilot_login] if assign_copilot else []
    create_standards_followup = (
        os.environ.get("CREATE_STANDARDS_FOLLOWUP", "true").lower() == "true"
    )

    created = 0
    updated = 0
    skipped = 0

    for collection, items in sorted(grouped.items()):
        if len(items) < args.min_files:
            skipped += 1
            continue

        title = f"🤖 AI Content Review — `_{collection}` collection"
        body = format_issue_body(
            collection=collection,
            reviews=items,
            repo=args.repo,
            commit_sha=args.commit_sha,
        )
        labels = DEFAULT_LABELS + [f"collection:{collection}"]

        print(f"\n— Collection `_{collection}` ({len(items)} file(s)) —")

        if args.dry_run:
            print(f"  [dry-run] Would upsert issue: {title}")
            print(f"  [dry-run] Labels: {labels}")
            print(f"  [dry-run] Assignees: {assignees}")
            print(f"  [dry-run] Body preview ({len(body)} chars):")
            print("    " + body.splitlines()[0])
            continue

        existing = find_existing_issue(args.repo, token, title)
        if existing:
            number = existing["number"]
            print(f"  Updating existing issue #{number}")
            update_issue(args.repo, token, number, body, labels)
            if assignees:
                add_assignees(args.repo, token, number, assignees)
            updated += 1
        else:
            issue = create_issue(
                args.repo, token, title, body, labels, assignees,
            )
            print(f"  Created issue #{issue.get('number')}: {issue.get('html_url')}")
            created += 1

    if create_standards_followup:
        standards_title = "🤖 AI Content Review — Instructions & prompts hardening"
        standards_body = format_standards_issue_body(
            reviews=reviews,
            repo=args.repo,
            commit_sha=args.commit_sha,
        )
        print("\n— Standards hardening follow-up —")
        if args.dry_run:
            print(f"  [dry-run] Would upsert issue: {standards_title}")
            print(f"  [dry-run] Labels: {DEFAULT_LABELS}")
            print(f"  [dry-run] Assignees: {assignees}")
            print(f"  [dry-run] Body preview ({len(standards_body)} chars):")
            print("    " + standards_body.splitlines()[0])
        else:
            existing = find_existing_issue(args.repo, token, standards_title)
            if existing:
                number = existing["number"]
                print(f"  Updating existing issue #{number}")
                update_issue(args.repo, token, number, standards_body, DEFAULT_LABELS)
                if assignees:
                    add_assignees(args.repo, token, number, assignees)
                updated += 1
            else:
                issue = create_issue(
                    args.repo,
                    token,
                    standards_title,
                    standards_body,
                    DEFAULT_LABELS,
                    assignees,
                )
                print(f"  Created issue #{issue.get('number')}: {issue.get('html_url')}")
                created += 1

    print(
        f"\nDone. created={created} updated={updated} "
        f"skipped(<{args.min_files} files)={skipped}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
