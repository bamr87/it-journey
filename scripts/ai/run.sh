#!/usr/bin/env bash
# =============================================================================
# run.sh — the universal AI runner (Claude Code first, Claude API fallback)
# -----------------------------------------------------------------------------
# EVERY AI call in the repo goes through here — every workflow agent step and
# every skill — so the model, the auth, and the fallback are configured in ONE
# place (_data/ai.yml + the auth env below). Primary is Claude Code (the full
# agent with tools); if the `claude` CLI is missing or the run fails, it falls
# back to the Claude API (scripts/ai/api_call.py) for a single-shot text result.
#
#   scripts/ai/run.sh --prompt "..." [--agent name] [--tools "Bash,Read,..."] \
#                     [--mcp cfg.json] [--system "..."] [--out file]
#   echo "..." | scripts/ai/run.sh            # stdin prompt
#
# Auth (either works for the primary Claude Code path):
#   CLAUDE_CODE_OAUTH_TOKEN — a Claude Code token from `claude setup-token`
#                             (subscription auth; the preferred CI credential).
#   ANTHROPIC_API_KEY       — a pay-per-use API key; ALSO the only credential the
#                             Claude API fallback (api_call.py) can use.
# Env: ITJ_AI_FORCE_API=1 (skip Claude Code, go straight to the API),
#      ITJ_AI_MODEL (override the model from _data/ai.yml).
#
# Ported from lifehacker.dev/scripts/ai/run.sh so the sibling sites share one
# agentic convention; the YAML read is done in python (this repo's tooling lang).
# =============================================================================
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# The Claude Code CLI reads CLAUDE_CODE_OAUTH_TOKEN or ANTHROPIC_API_KEY from the
# env. Prefer the OAuth token when present, and drop an empty ANTHROPIC_API_KEY
# (an unset GitHub secret renders as "") so the CLI never attempts empty-key auth.
if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] && [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  unset ANTHROPIC_API_KEY
fi

MODEL="$(python3 - "$REPO/_data/ai.yml" <<'PY' 2>/dev/null || echo claude-opus-4-8
import os, sys
try:
    import yaml
    cfg = yaml.safe_load(open(sys.argv[1])) or {}
except Exception:
    cfg = {}
print(os.environ.get("ITJ_AI_MODEL") or cfg.get("model") or "claude-opus-4-8")
PY
)"

prompt=""; tools=""; mcp=""; system=""; out=""; agent=""
while [ $# -gt 0 ]; do
  case "$1" in
    --prompt|-p) prompt="$2"; shift 2;;
    --tools)     tools="$2";  shift 2;;
    --mcp)       mcp="$2";    shift 2;;
    --system)    system="$2"; shift 2;;
    --out)       out="$2";    shift 2;;
    --agent)     agent="$2";  shift 2;;
    *) shift;;
  esac
done
# No --prompt? read stdin.
[ -z "$prompt" ] && [ ! -t 0 ] && prompt="$(cat)"

run_claude_code() {
  local args=(-p "$prompt" --model "$MODEL" --permission-mode acceptEdits)
  # Run AS a named agent (.claude/agents/<name>.md) when given — its system
  # prompt, tool scope, and role constraints are the single source of truth, so
  # every CI invocation of that role behaves identically. --tools/--system layer on.
  [ -n "$agent" ]  && args+=(--agent "$agent")
  [ -n "$tools" ]  && args+=(--allowedTools "$tools")
  [ -n "$mcp" ]    && args+=(--mcp-config "$mcp")
  # Appended (not replaced) so Claude Code's own agent prompt stays intact —
  # otherwise a guardrail like "never merge" would bind only the API fallback.
  [ -n "$system" ] && args+=(--append-system-prompt "$system")
  claude "${args[@]}"
}

# After the agent edits files, DETERMINISTICALLY unwrap any markdown it changed
# to the house "one paragraph per line" rule (the `oneline` CI gate) — LLMs
# soft-wrap prose by habit, and this is the shared chokepoint every AI call flows
# through, so normalizing here keeps wrapped prose out of every workflow's PR
# without a per-workflow step. Best-effort: never fails the run, skips the
# machine-authored/generated files the gate excludes. Catches uncommitted edits;
# an agent that commits inside its own run is covered by the Claude Code
# PostToolUse hook instead (see docs/prose-oneline-universal.md). Idempotent with
# quest-fix's M8 step. Upstream to bamr87/bamr87 + lifehacker.dev so siblings share it.
normalize_changed_markdown() {
  command -v git >/dev/null 2>&1 || return 0
  [ -f "$REPO/tools/unwrap-prose.py" ] || return 0
  local files
  files="$(cd "$REPO" && { git diff --name-only --diff-filter=ACMR -- '*.md' '*.markdown'
                           git diff --cached --name-only --diff-filter=ACMR -- '*.md' '*.markdown'; } 2>/dev/null \
           | sort -u \
           | grep -vE '(^|/)(SCHEMA|CHANGELOG)\.md$|(^|/)pages/_quest-reports/|(^|/)test/quest-validator/walkthroughs/' \
           || true)"
  [ -n "$files" ] || return 0
  # shellcheck disable=SC2086
  (cd "$REPO" && printf '%s\n' "$files" | xargs -r python3 tools/unwrap-prose.py --write) >&2 || true
}

# --- Primary: Claude Code ----------------------------------------------------
if [ "${ITJ_AI_FORCE_API:-0}" != "1" ] && command -v claude >/dev/null 2>&1; then
  if [ -n "$out" ]; then
    if run_claude_code > "$out"; then normalize_changed_markdown; exit 0; fi
  else
    if run_claude_code; then normalize_changed_markdown; exit 0; fi
  fi
  echo "[ai] Claude Code unavailable/failed — falling back to the Claude API." >&2
fi

# --- Fallback: Claude API (single-shot) --------------------------------------
# The raw API needs an ANTHROPIC_API_KEY. If there's none (OAuth-only auth, or no
# auth at all), don't hard-abort — no-op cleanly (exit 0) so direct callers and
# the claude-run action degrade gracefully ("no auth -> no-op").
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "[ai] no ANTHROPIC_API_KEY for the Claude API fallback — skipping (no-op)." >&2
  exit 0
fi
api=(python3 "$REPO/scripts/ai/api_call.py" --prompt "$prompt")
[ -n "$system" ] && api+=(--system "$system")
if [ -n "$out" ]; then
  "${api[@]}" > "$out"
else
  "${api[@]}"
fi
