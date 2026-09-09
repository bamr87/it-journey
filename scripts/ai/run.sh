#!/usr/bin/env bash
# =============================================================================
# run.sh — the universal AI runner (Claude Code first, Claude API fallback)
# -----------------------------------------------------------------------------
# kit: ai-runner — this file is shared VERBATIM across the fleet's content sites
# (lifehacker.dev is the source of truth; it-journey and zer0-mistakes carry a
# byte-identical copy). Change it here, then copy it forward; never fork it.
#
# EVERY AI call in the repo goes through here — every workflow agent step and
# every skill — so model, auth, and the fallback are configured in ONE place
# (_data/ai.yml + the auth env below). Primary is Claude Code (the full agent
# with tools); if the `claude` CLI is missing or the run fails, it falls back to
# the Claude API (scripts/ai/api_call.rb, or api_call.py) for a single-shot text.
#
#   scripts/ai/run.sh --prompt "..." [--agent name] [--tools "Bash,Read,..."] \
#                     [--mcp cfg.json] [--system "..."] [--out file] \
#                     [--model id] [--max-turns N]
#   echo "..." | scripts/ai/run.sh            # stdin prompt
#
# Auth (either works for the primary Claude Code path):
#   CLAUDE_CODE_OAUTH_TOKEN — a Claude Code token from `claude setup-token`
#                             (subscription auth; the preferred CI credential).
#   ANTHROPIC_API_KEY       — a pay-per-use API key; ALSO the only credential the
#                             Claude API fallback can use.
# Env (canonical names — no repo prefix, so the file stays identical everywhere):
#   AI_MODEL      override the model from _data/ai.yml (also: --model)
#   AI_FORCE_API  =1 skips Claude Code and goes straight to the API fallback
#   AI_MAX_TURNS  cap the agent's turns (--max-turns); unset = the CLI default
#   AI_USAGE_DIR  where usage.rb writes records (default $RUNNER_TEMP/ai-usage)
#
# Optional companions — present means used, absent means the runner degrades
# honestly rather than failing:
#   scripts/ai/usage.rb            metering (one JSONL record per call)
#   scripts/ai/api_call.rb | .py   the single-shot Claude API fallback
#   tools/unwrap-prose.py          post-run "one paragraph per line" normalizer
#   .prose-excludes                extra exclude regexes for that normalizer
#
# EXIT CODES — a failed call is never silently green:
#   0  the call ran, or no AI call was ever attempted (no `claude` on PATH and
#      no API key: the documented no-op, so a human running a skill locally
#      without credentials degrades gracefully instead of aborting).
#   1  the call was ATTEMPTED and FAILED with no usable fallback. The reason the
#      run gave (auth rejected, quota exhausted, model unavailable) is printed
#      and, under Actions, raised as a ::error:: annotation. Before this, such a
#      run exited 0 and the caller only learned of it a step later, as a generic
#      "no PR was opened", with the evidence already deleted.
# =============================================================================
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# The Claude Code CLI reads CLAUDE_CODE_OAUTH_TOKEN or ANTHROPIC_API_KEY from the
# env. Prefer the OAuth token when present, and drop an empty ANTHROPIC_API_KEY
# (an unset GitHub secret renders as "") so the CLI never attempts empty-key auth.
if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] && [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  unset ANTHROPIC_API_KEY
fi

prompt=""; tools=""; mcp=""; system=""; out=""; agent=""; model_flag=""; max_turns="${AI_MAX_TURNS:-}"
while [ $# -gt 0 ]; do
  case "$1" in
    --prompt|-p)  prompt="$2";     shift 2;;
    --tools)      tools="$2";      shift 2;;
    --mcp)        mcp="$2";        shift 2;;
    --system)     system="$2";     shift 2;;
    --out)        out="$2";        shift 2;;
    --agent)      agent="$2";      shift 2;;
    --model)      model_flag="$2"; shift 2;;
    --max-turns)  max_turns="$2";  shift 2;;
    *) shift;;
  esac
done
# No --prompt? read stdin.
[ -z "$prompt" ] && [ ! -t 0 ] && prompt="$(cat)"

# Model: --model > AI_MODEL > _data/ai.yml model > the fleet default.
MODEL="$(AI_MODEL="${model_flag:-${AI_MODEL:-}}" ruby -ryaml -e '
  c = (YAML.respond_to?(:unsafe_load) ? YAML.unsafe_load(File.read(ARGV[0])) : YAML.load(File.read(ARGV[0]))) rescue {}
  m = ENV["AI_MODEL"].to_s
  puts(m.empty? ? ((c.is_a?(Hash) && c["model"]) || "claude-opus-4-8") : m)
' "$REPO/_data/ai.yml" 2>/dev/null || echo "${model_flag:-${AI_MODEL:-claude-opus-4-8}}")"

USAGE_RB="$REPO/scripts/ai/usage.rb"

run_claude_code() {
  # --output-format json: same run, but the final payload carries usage + cost
  # (total_cost_usd, per-model tokens) alongside the result text. emit_result
  # records the usage (when usage.rb is present) and re-emits the text, so
  # callers see exactly what they always did on stdout/--out.
  local args=(-p "$prompt" --model "$MODEL" --permission-mode acceptEdits --output-format json)
  # Run AS a named agent (.claude/agents/<name>.md) when given — its system prompt,
  # tool scope, and role constraints are the single source of truth, so every CI
  # invocation of that role behaves identically. --tools/--system still layer on.
  [ -n "$agent" ]     && args+=(--agent "$agent")
  [ -n "$tools" ]     && args+=(--allowedTools "$tools")
  [ -n "$mcp" ]       && args+=(--mcp-config "$mcp")
  [ -n "$max_turns" ] && args+=(--max-turns "$max_turns")
  # Same system prompt the API fallback gets — appended so Claude Code's own
  # agent prompt (tools/permissions) stays intact. Without this, a guardrail
  # like "never merge" would only bind the fallback path, not the primary one.
  [ -n "$system" ] && args+=(--append-system-prompt "$system")
  # OAuth-first invariant: when the subscription token exists, the CLI must
  # never see the metered API key (with both set it would silently bill the
  # key). The key stays exported in THIS shell for the API fallback below.
  if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
    env -u ANTHROPIC_API_KEY claude "${args[@]}"
  else
    claude "${args[@]}"
  fi
}

# Turn the JSON result payload into the caller's text. With usage.rb present the
# call is metered on the way through; without it the same contract holds via a
# stdlib one-liner: exit non-zero unless the payload is a successful Claude
# `result` (so a dead credential can never read as a green step).
emit_result() {
  local json="$1" rc="$2"
  if [ -f "$USAGE_RB" ]; then
    ruby "$USAGE_RB" ingest-claude "$json" --agent "$agent" --rc "$rc" --emit-result
  else
    ruby -rjson -e '
      res = (JSON.parse(File.read(ARGV[0], encoding: "UTF-8")) rescue nil)
      exit 1 unless res.is_a?(Hash) && res["type"] == "result" && !res["is_error"] && ARGV[1].to_i == 0
      print res["result"].to_s
    ' "$json" "$rc"
  fi
}

# After the agent edits files, DETERMINISTICALLY unwrap any markdown it changed
# to the house "one paragraph per line" rule (the markdown-oneline CI gate) —
# LLMs soft-wrap prose by habit, and this is the shared chokepoint every AI
# call flows through, so normalizing here keeps wrapped prose out of every
# workflow's PR without a per-workflow step. Best-effort: never fails the run.
# Always skips SCHEMA.md/CHANGELOG.md; a repo lists further exclusions (one
# extended regex per line, # comments allowed) in .prose-excludes — e.g.
# machine-authored transcripts the gate also ignores. Catches uncommitted
# edits; an agent that commits inside its own run is covered by the PR gate.
normalize_changed_markdown() {
  command -v git >/dev/null 2>&1 || return 0
  [ -f "$REPO/tools/unwrap-prose.py" ] || return 0
  local excl='(^|/)(SCHEMA|CHANGELOG)\.md$' files
  if [ -f "$REPO/.prose-excludes" ]; then
    while IFS= read -r line; do
      line="${line%%#*}"; line="${line#"${line%%[![:space:]]*}"}"; line="${line%"${line##*[![:space:]]}"}"
      [ -n "$line" ] && excl="$excl|$line"
    done < "$REPO/.prose-excludes"
  fi
  files="$(cd "$REPO" && { git diff --name-only --diff-filter=ACMR -- '*.md' '*.markdown'
                           git diff --cached --name-only --diff-filter=ACMR -- '*.md' '*.markdown'; } 2>/dev/null \
           | sort -u | grep -vE "$excl" || true)"
  [ -n "$files" ] || return 0
  (cd "$REPO" && printf '%s\n' "$files" | xargs python3 tools/unwrap-prose.py --write) >&2 || true
}

# `claude -p --output-format json` writes its FAILURE to stdout too: a result
# payload carrying `subtype` and a `result` message that says what the API
# refused and why. Pull that out (secrets scrubbed, one line, bounded) so the
# job log names the cause instead of guessing at it.
claude_failure_reason() {
  ruby -rjson -e '
    raw = (File.read(ARGV[0], encoding: "UTF-8") rescue "")
    res = (JSON.parse(raw) rescue nil)
    text = res.is_a?(Hash) ? [res["subtype"], res["result"] || res["error"]].compact.map(&:to_s).reject(&:empty?).join(": ") : raw
    puts text.to_s.gsub(/sk-ant-[A-Za-z0-9_-]{8,}/, "sk-ant-***").gsub(/\s+/, " ").strip[0, 600].to_s
  ' "$1" 2>/dev/null
}

# Name the operator action for the failures that actually recur here. Advisory
# only — the run's own message is always printed alongside it.
claude_failure_hint() {
  case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
    *"usage limit"*|*rate_limit*|*"too many requests"*|*429*)
      echo "the Claude quota behind this credential is exhausted — wait for the window to reset, or move the lane to a metered ANTHROPIC_API_KEY" ;;
    *authentication*|*unauthorized*|*"invalid api key"*|*invalid_api_key*|*expired*|*"/login"*|*401*|*403*)
      echo "the Claude credential was rejected — mint a fresh CLAUDE_CODE_OAUTH_TOKEN with \`claude setup-token\` and update the repo secret" ;;
    *overloaded*|*529*|*503*|*502*)
      echo "the API was overloaded — transient; the next scheduled run should recover" ;;
    *not_found*|*"does not support"*|*"unknown model"*)
      echo "the model pinned in _data/ai.yml is not available to this credential — check \`model:\` there" ;;
    *) echo "" ;;
  esac
}

# --- Primary: Claude Code ----------------------------------------------------
primary_failed=0
reason=""
if [ "${AI_FORCE_API:-0}" != "1" ] && command -v claude >/dev/null 2>&1; then
  tmp_json="$(mktemp "${TMPDIR:-/tmp}/ai-result.XXXXXX")"
  run_claude_code > "$tmp_json"
  rc=$?
  if [ "$rc" -eq 0 ]; then
    # Record usage, then emit the result text (the caller's contract). A parse
    # failure here means claude didn't produce a result payload — treat it
    # exactly like a failed run and let the fallback engage.
    if [ -n "$out" ]; then
      if emit_result "$tmp_json" "$rc" > "$out"; then
        rm -f "$tmp_json"; normalize_changed_markdown; exit 0
      fi
    else
      if emit_result "$tmp_json" "$rc"; then
        rm -f "$tmp_json"; normalize_changed_markdown; exit 0
      fi
    fi
  fi
  # Reaching here means the run failed: a non-zero exit, or an exit-0 payload the
  # ingester refused (an is_error result, or not a result at all). Tokens may
  # still have been spent — record them (status:error, with the reason) before
  # falling back, and no longer swallow the ingester's stderr, because that line
  # is half the diagnosis. Only the non-zero path ingests here: the exit-0 path
  # already ran the ingester above, and re-running it would append the record
  # twice (same stable id, but the step summary and ledger both count rows).
  primary_failed=1
  if [ "$rc" -ne 0 ] && [ -f "$USAGE_RB" ]; then
    ruby "$USAGE_RB" ingest-claude "$tmp_json" --agent "$agent" --rc "$rc" || true
  fi
  reason="$(claude_failure_reason "$tmp_json")"
  rm -f "$tmp_json"
  if [ "$rc" -ne 0 ]; then
    echo "[ai] Claude Code failed (exit $rc): ${reason:-no result payload — claude produced no JSON}" >&2
  else
    echo "[ai] Claude Code exited 0 with an unusable result: ${reason:-no result payload — claude produced no JSON}" >&2
  fi
  hint="$(claude_failure_hint "$reason")"
  [ -n "$hint" ] && echo "[ai] likely cause: $hint" >&2
  echo "[ai] falling back to the Claude API." >&2
fi

# --- Fallback: Claude API (single-shot) --------------------------------------
# The raw API needs an ANTHROPIC_API_KEY and a fallback script. With neither,
# what decides the exit code is what happened BEFORE this point:
#   * nothing was attempted (no `claude` on PATH, or AI_FORCE_API with no key)
#     -> the documented no-op, exit 0, so direct callers degrade gracefully.
#   * the primary path RAN AND FAILED -> exit non-zero. A rejected model call is
#     a failure, and a green step that produced nothing is how six days of dead
#     content-factory runs came to read as "no PR was opened (auth? duplicate?
#     build failure?)" one step downstream.
api=()
if   [ -f "$REPO/scripts/ai/api_call.rb" ]; then api=(ruby    "$REPO/scripts/ai/api_call.rb" --prompt "$prompt")
elif [ -f "$REPO/scripts/ai/api_call.py" ]; then api=(python3 "$REPO/scripts/ai/api_call.py" --prompt "$prompt")
fi
if [ -z "${ANTHROPIC_API_KEY:-}" ] || [ ${#api[@]} -eq 0 ]; then
  why="no ANTHROPIC_API_KEY"; [ ${#api[@]} -eq 0 ] && why="no scripts/ai/api_call.rb|py"
  if [ "$primary_failed" -eq 1 ]; then
    echo "[ai] $why to fall back to — the AI step failed." >&2
    [ "${GITHUB_ACTIONS:-}" = "true" ] && \
      echo "::error::AI step failed${agent:+ (agent: $agent)}: ${reason:-Claude Code produced no result payload}"
    exit 1
  fi
  echo "[ai] $why for the Claude API fallback — skipping (no-op)." >&2
  exit 0
fi
export AI_ROLE="$agent"   # so the fallback's usage record carries the role
[ -n "$system" ] && api+=(--system "$system")
if [ -n "$out" ]; then
  "${api[@]}" > "$out"
else
  "${api[@]}"
fi
