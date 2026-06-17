#!/usr/bin/env bash
# Entrypoint for the CMS review container (docker-compose.cms.yml).
#
# Usage (from the repo root):
#   docker compose -f docker-compose.cms.yml run --rm cms            # full review
#   docker compose -f docker-compose.cms.yml run --rm cms status     # dashboard only
#   docker compose -f docker-compose.cms.yml run --rm cms all        # rebuild outputs
#   docker compose -f docker-compose.cms.yml run --rm cms test       # unit tests
#   docker compose -f docker-compose.cms.yml run --rm cms normalize  # mechanical preview
#   docker compose -f docker-compose.cms.yml run --rm cms shell      # interactive shell
set -euo pipefail

# The engine only needs pyyaml. Installed quietly on container start.
pip install --quiet --disable-pip-version-check --root-user-action=ignore pyyaml \
  >/dev/null 2>&1 || pip install --quiet pyyaml

cmd="${1:-review}"
case "$cmd" in
  review)
    echo "════════════════════ IT-Journey CMS — review run ════════════════════"
    echo
    echo "▶ 1/4  Unit + integration test suite"
    python3 scripts/cms/test_cms.py
    echo
    echo "▶ 2/4  Build index + analysis report + worklist"
    python3 scripts/cms/cms.py all
    echo
    echo "▶ 3/4  Content health dashboard"
    python3 scripts/cms/cms.py status
    echo
    echo "▶ 4/4  Mechanical-lane PREVIEW (dry-run — no files written)"
    python3 scripts/content/normalize-frontmatter.py pages/ --quiet || true
    d="$(date -u +%F)"
    echo
    echo "─────────────────────────────────────────────────────────────────────"
    echo "Open these on your host to review (written via the bind mount):"
    echo "  .cms/reports/${d}.md      ← daily analysis report"
    echo "  .cms/worklists/${d}.md    ← prioritized worklist (mechanical / substantive)"
    echo "  .cms/index/summary.json   ← repo-wide rollup"
    echo "  .cms/index/content-index.json  ← full per-file index"
    echo "─────────────────────────────────────────────────────────────────────"
    ;;
  status|index|analyze|plan|all)
    python3 scripts/cms/cms.py "$cmd" ;;
  test)
    python3 scripts/cms/test_cms.py ;;
  normalize|normalize-preview)
    # Mechanical lane preview (dry-run). Exit 2 just means "changes pending".
    python3 scripts/content/normalize-frontmatter.py pages/ || true ;;
  shell)
    exec bash ;;
  *)
    exec "$@" ;;
esac
