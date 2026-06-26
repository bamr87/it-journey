#!/usr/bin/env bash
# Entrypoint for the quest-audit container (docker-compose.yml `quest-audit`).
#
# Runs the unified quest validation system (scripts/quest/quest_audit.py) in a
# throwaway python:3.12-slim container so validation matches CI regardless of
# the host's Python/Ruby. The repo is bind-mounted at /app; the audit is
# read-only (its freshness check restores any file it regenerates).
#
# Usage (from the repo root):
#   docker compose run --rm quest-audit                 # full deterministic audit
#   docker compose run --rm quest-audit strict          # warnings fail the audit
#   docker compose run --rm quest-audit audit --json /app/quest-audit.json
#   docker compose run --rm quest-audit changed pages/_quests/0001/x.md
#   docker compose run --rm quest-audit tier2 review    # + Claude (needs CLI+token)
#   docker compose run --rm quest-audit execute --changed pages/_quests/0001/x.md
#                                                       # Claude RUNS a quest's snippets, isolated
#   docker compose run --rm quest-audit shell           # interactive shell
set -euo pipefail

# The deterministic audit only needs pyyaml. Installed quietly on start so the
# image stays a stock python:3.12-slim with no custom build step.
pip install --quiet --disable-pip-version-check --root-user-action=ignore pyyaml \
  >/dev/null 2>&1 || pip install --quiet pyyaml

AUDIT="python3 scripts/quest/quest_audit.py"

# The CONTAINER is the isolation boundary for execute mode — the Claude CLI is
# installed here (Node) so the agent's commands run inside this disposable box,
# never on the host. Returns 0 if a usable `claude` is available, 1 otherwise.
have_creds() { [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}${ANTHROPIC_API_KEY:-}" ]; }
ensure_claude() {
  command -v claude >/dev/null 2>&1 && return 0
  echo "▶ Installing Node + Claude Code CLI in the container (one-time per run)…"
  apt-get update -qq >/dev/null 2>&1 || true
  apt-get install -y -qq curl >/dev/null 2>&1 || true
  curl -fsSL https://deb.nodesource.com/setup_20.x 2>/dev/null | bash - >/dev/null 2>&1 || true
  apt-get install -y -qq nodejs >/dev/null 2>&1 || true
  npm install -g @anthropic-ai/claude-code >/dev/null 2>&1 || true
  command -v claude >/dev/null 2>&1
}

cmd="${1:-audit}"
shift || true

case "$cmd" in
  audit)
    exec $AUDIT "$@"
    ;;
  strict)
    exec $AUDIT --strict "$@"
    ;;
  changed)
    exec $AUDIT --changed "$@"
    ;;
  tier2)
    # First positional after `tier2` is the mode (review|execute); default review.
    mode="${1:-review}"; shift || true
    if ! have_creds; then
      echo "ℹ️  No Claude credentials in the container — running tier2 in --mock (advisory, no cost)."
      exec $AUDIT --tier2 "$mode" --tier2-mock "$@"
    fi
    if ! ensure_claude; then
      echo "⚠️  claude CLI unavailable in container; running tier2 in --mock (no cost)."
      exec $AUDIT --tier2 "$mode" --tier2-mock "$@"
    fi
    exec $AUDIT --tier2 "$mode" "$@"
    ;;
  execute)
    # Focused: a Claude agent walks ONE quest (or a sample) and ACTUALLY RUNS its
    # code snippets in this isolated container — no content/network/freshness.
    #   ... execute --changed pages/_quests/0001/x.md   (one quest)
    #   ... execute --tier2-sample 3                     (a spread of quests)
    if ! have_creds; then
      echo "ℹ️  No Claude credentials — running execute in --mock (no real commands run, no cost)."
      exec $AUDIT --no-content --no-network --no-freshness --tier2 execute --tier2-mock "$@"
    fi
    if ! ensure_claude; then
      echo "⚠️  claude CLI unavailable in container; running execute in --mock (no cost)."
      exec $AUDIT --no-content --no-network --no-freshness --tier2 execute --tier2-mock "$@"
    fi
    exec $AUDIT --no-content --no-network --no-freshness --tier2 execute "$@"
    ;;
  shell)
    exec bash "$@"
    ;;
  *)
    # Unknown subcommand → treat the whole argv as quest_audit flags.
    exec $AUDIT "$cmd" "$@"
    ;;
esac
