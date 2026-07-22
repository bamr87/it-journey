#!/usr/bin/env bash
# =============================================================================
# unwrap-md-hook.sh — Claude Code PostToolUse hook for the "oneline" prose rule.
# -----------------------------------------------------------------------------
# Wired from .claude/settings.json on Write|Edit|MultiEdit. After Claude writes
# or edits a markdown file, this unwraps it to the house "one paragraph per line"
# rule (tools/unwrap-prose.py) so soft-wrapped prose never reaches a commit — in
# EVERY session (local + the headless `claude -p` CI agents) and, when this repo's
# .claude/settings.json is used as the template, every repo it is copied into.
#
# Contract (per Claude Code hooks): reads the event JSON on stdin, acts only on
# markdown, is a pure side-effect, and ALWAYS exits 0 (never blocks the tool).
# No jq dependency — the JSON is parsed with python3 (already required by the
# unwrapper). Keep the EXCLUDES in lockstep with markdown-oneline.yml.
# =============================================================================
set -euo pipefail

root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
unwrap="$root/tools/unwrap-prose.py"
[ -f "$unwrap" ] || exit 0   # unwrapper not present in this repo — no-op

# Pull the edited file path from the PostToolUse event JSON on stdin.
file="$(python3 -c 'import json,sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
print((d.get("tool_input") or {}).get("file_path") or "")' 2>/dev/null || true)"

[ -n "$file" ] || exit 0
case "$file" in
  *.md|*.markdown) : ;;
  *) exit 0 ;;                # not markdown — nothing to do
esac
# Skip the generated / machine-authored files the oneline gate excludes.
case "$file" in
  SCHEMA.md|*/SCHEMA.md|CHANGELOG.md|*/CHANGELOG.md) exit 0 ;;
  pages/_quest-reports/*|*/pages/_quest-reports/*) exit 0 ;;
  test/quest-validator/walkthroughs/*|*/test/quest-validator/walkthroughs/*) exit 0 ;;
esac
[ -f "$file" ] || exit 0

python3 "$unwrap" --write "$file" >/dev/null 2>&1 || true
exit 0
