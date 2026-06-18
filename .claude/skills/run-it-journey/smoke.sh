#!/usr/bin/env bash
# Driver / smoke harness for the IT-Journey Jekyll site.
#
# It does NOT start the server (that takes ~8 min the first time — see SKILL.md).
# It assumes the dev server is already serving on $BASE_URL, then:
#   1. waits for the server to answer,
#   2. checks a set of routes return HTTP 200,
#   3. captures full-width screenshots of key pages with headless Chrome.
#
# Usage (paths are relative to the repo root):
#   docker compose up -d jekyll                              # start server (first run ~8 min)
#   bash .claude/skills/run-it-journey/smoke.sh              # default routes + screenshots
#   bash .claude/skills/run-it-journey/smoke.sh /quests/ /docs/   # custom routes
#   BASE_URL=http://localhost:4002 SHOTS="/ /quests/ /docs/" bash .../smoke.sh
#
# Exit 0 = every route 200 and every screenshot written; non-zero otherwise.
# Screenshots land in $OUT_DIR (default /tmp/it-journey-shots) — open them to
# confirm the site actually rendered (a 200 with a blank body still "passes" curl).

set -uo pipefail

# The macOS login shell occasionally hands a stripped PATH to spawned tools,
# so curl/grep silently become "command not found". Pin a sane PATH up front.
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin:${PATH:-}"

BASE_URL="${BASE_URL:-http://localhost:4002}"
OUT_DIR="${OUT_DIR:-/tmp/it-journey-shots}"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"

# Routes to HTTP-check: positional args override the defaults.
if [ "$#" -gt 0 ]; then
  ROUTES=("$@")
else
  ROUTES=(/ /home/ /quests/ /docs/ /notes/ /about/ /sitemap/)
fi

# Routes to screenshot (space-separated string so it's easy to override via env).
read -r -a SHOT_ROUTES <<<"${SHOTS:-/ /quests/}"

mkdir -p "$OUT_DIR"
fail=0

echo "==> Waiting for $BASE_URL"
up=0
for _ in $(seq 1 15); do
  if curl -fsS -o /dev/null "$BASE_URL/"; then up=1; break; fi
  sleep 2
done
if [ "$up" -ne 1 ]; then
  echo "FAIL: $BASE_URL is not responding."
  echo "      Start it with:  docker compose up -d jekyll   (first build ~8 min)"
  echo "      Watch progress: docker compose logs -f jekyll  (wait for 'Server running')"
  exit 1
fi

echo "==> Route checks"
for path in "${ROUTES[@]}"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$path")
  if [ "$code" = "200" ]; then status="OK"; else status="FAIL"; fail=1; fi
  printf "    %-14s HTTP %s  %s\n" "$path" "$code" "$status"
done

echo "==> Screenshots -> $OUT_DIR"
if [ ! -x "$CHROME" ]; then
  echo "    WARN: Chrome not found at \$CHROME ($CHROME) — skipping screenshots."
  echo "          Set CHROME=/path/to/chrome to enable them."
else
  for path in "${SHOT_ROUTES[@]}"; do
    if [ "$path" = "/" ]; then name="home"; else name=$(printf '%s' "$path" | tr -cd 'a-z0-9'); fi
    out="$OUT_DIR/${name:-home}.png"
    "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-sandbox \
      --force-device-scale-factor=1 --window-size=1280,1600 \
      --virtual-time-budget=8000 \
      --screenshot="$out" "$BASE_URL$path" >/dev/null 2>&1
    if [ -s "$out" ]; then
      printf "    %-14s -> %s\n" "$path" "$out"
    else
      printf "    %-14s -> SCREENSHOT FAILED\n" "$path"
      fail=1
    fi
  done
fi

if [ "$fail" -eq 0 ]; then echo "==> PASS"; else echo "==> FAIL"; fi
exit "$fail"
