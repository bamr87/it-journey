#!/usr/bin/env bash
#
# Offline test suite for the agentic quest validator (tier 2).
# Exercises the entire pipeline WITHOUT calling Claude (no auth, no cost):
#   compile · discovery/sampling · dry-run command build · mock scoring/report ·
#   success-path envelope parsing (all 3 output shapes) · exit-code gating.
#
# Usage: test/quest-validator/test-agentic.sh
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
CLI="$HERE/agentic_validate.py"
PY="${PYTHON:-}"
if [ -z "$PY" ]; then
  if [ -x /tmp/questvenv/bin/python ]; then PY=/tmp/questvenv/bin/python; else PY="$(command -v python3)"; fi
fi

cd "$REPO"
pass=0; fail=0
ok()   { echo "  ✅ $1"; pass=$((pass+1)); }
bad()  { echo "  ❌ $1"; fail=$((fail+1)); }

echo "── 1. modules compile ──"
if "$PY" -m py_compile "$CLI" "$HERE"/agentic/*.py; then ok "py_compile"; else bad "py_compile"; fi

echo "── 2. discovery + sampling ──"
n=$("$PY" "$CLI" -d pages/_quests --sample 5 --list 2>/dev/null | grep -c '^[01]\{4\}  ')
[ "$n" = "5" ] && ok "sample 5 spread across levels" || bad "expected 5 listed, got $n"

echo "── 3. dry-run builds correct tool restrictions ──"
rev=$("$PY" "$CLI" pages/_quests/0101/docker-mastery-example.md --mode review --dry-run 2>/dev/null | grep '^command:')
echo "$rev" | grep -q -- '--allowedTools Read' && echo "$rev" | grep -q -- '--disallowedTools Bash' \
  && ok "review mode is read-only" || bad "review mode tools wrong"
exe=$("$PY" "$CLI" pages/_quests/0101/docker-mastery-example.md --mode execute --dry-run 2>/dev/null | grep '^command:')
echo "$exe" | grep -q 'bypassPermissions' && echo "$exe" | grep -q 'Bash(sudo:\*)' \
  && ok "execute mode is sandboxed + foot-gun denied" || bad "execute mode tools wrong"

echo "── 4. mock end-to-end (score + json) ──"
"$PY" "$CLI" -d pages/_quests --sample 3 --mock --report /tmp/_agentic_selftest.json >/dev/null 2>&1
"$PY" - <<'PY' && ok "mock report well-formed" || bad "mock report malformed"
import json,sys
d=json.load(open("/tmp/_agentic_selftest.json"))
assert d["total"]==3 and d["scored"]==3, d
assert set(d["counts"])=={"pass","warn","fail"}
assert 0<=d["average"]<=100
r=d["results"][0]
assert set(r["per_dimension"])>={"commands_work","content_accuracy","safety"}
PY

echo "── 5. success-path envelope parsing (3 shapes) ──"
"$PY" - <<'PY' && ok "all envelope shapes -> 84.0" || bad "envelope parsing"
import sys,json
sys.path.insert(0,"test/quest-validator")
from agentic import runner, loader, schema
R=runner.AgenticRunner(mode="review")
q=loader.load_quest("pages/_quests/0101/docker-mastery-example.md")
v={"executed":False,
   "dimensions":{k:{"score":s,"findings":["x"]} for k,s in zip(schema.DIM_KEYS,[4,5,4,3,4,5])},
   "commands":[],"recommendations":[],"summary":"ok"}
envs={"fenced":{"result":"pre\n```json\n"+json.dumps(v)+"\n```"},
      "dict":{"result":v},"struct":{"structured_output":v,"result":""}}
for name,e in envs.items():
    p=R._parse_envelope(json.dumps(e)); vv,_=R._extract_verdict(p)
    res=R._finalize(q,vv,meta={"mock":False})
    assert res["overall"]==84.0, (name,res["overall"])
PY

echo "── 6. exit-code gating ──"
"$PY" "$CLI" pages/_quests/0101/docker-mastery-example.md --mock --fail-threshold 95 >/dev/null 2>&1
[ $? -eq 1 ] && ok "below-threshold -> exit 1" || bad "threshold 95 should fail"
"$PY" "$CLI" pages/_quests/0101/docker-mastery-example.md --mock --fail-threshold 80 >/dev/null 2>&1
[ $? -eq 0 ] && ok "above-threshold -> exit 0" || bad "threshold 80 should pass"

echo ""
echo "════════════════════════════════════════"
echo "agentic self-test: $pass passed, $fail failed"
echo "════════════════════════════════════════"
[ "$fail" -eq 0 ]
