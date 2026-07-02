#!/usr/bin/env bash
# =============================================================================
# drift-guard.sh — state-snapshot context-drift detector for agent runs
# -----------------------------------------------------------------------------
# GH-600 Domain 3 (Memory, State & Execution) implemented for this repo: an
# agent plans against a snapshot of the world; before it ACTS, the world must
# still match the snapshot. If a watched file changed between planning and
# acting, the run must abort or re-plan — never act on a stale belief.
#
#   scripts/ai/drift-guard.sh snapshot FILE...   # hash the watched files
#   scripts/ai/drift-guard.sh verify             # re-hash and compare
#
# The snapshot lives at $DRIFT_SNAPSHOT (default .agent/snapshot.sha256) so a
# plan job can write it, ship it inside an artifact, and an execute job can
# verify it after a human-approval delay — see
# .github/workflows/agent-plan-then-act.yml for the reference wiring.
#
# Exit codes: 0 = no drift / snapshot written; 78 = drift detected (abort
# before acting); 1 = usage error. 78 is deliberate: distinguishable from an
# ordinary failure so an orchestrator can route it to a re-plan path.
#
# Taught by: /quests/1001/agentic-codex-03-memory-state-and-execution/
# =============================================================================
set -euo pipefail

SNAP="${DRIFT_SNAPSHOT:-.agent/snapshot.sha256}"
cmd="${1:-}"

case "$cmd" in
  snapshot)
    shift
    [ "$#" -gt 0 ] || { echo "usage: drift-guard.sh snapshot FILE..." >&2; exit 1; }
    mkdir -p "$(dirname "$SNAP")"
    sha256sum "$@" > "$SNAP"
    echo "Snapshot of $# file(s) written to $SNAP"
    ;;
  verify)
    [ -f "$SNAP" ] || { echo "::error::No snapshot at $SNAP — run 'snapshot' first." >&2; exit 1; }
    if sha256sum -c "$SNAP" --quiet 2>/dev/null; then
      echo "No drift — the world still matches the snapshot. Safe to act."
    else
      echo "::warning::Context drift detected — watched files changed since the snapshot was taken."
      sha256sum -c "$SNAP" 2>&1 | grep -v ': OK$' || true
      exit 78
    fi
    ;;
  *)
    echo "usage: drift-guard.sh {snapshot FILE...|verify}" >&2
    exit 1
    ;;
esac
