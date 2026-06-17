#!/usr/bin/env bash
# Parameterized post-deploy smoke test for static-guide overview videos.
# Usage: smoke-test.sh [BASE_URL] [BEACON_URL] [PROPOSAL_ID]
set -e
BASE="${1:-https://mulesoft-claude-cursor-onboarding.vercel.app}"
BEACON="${2:-https://smokin-territory.vercel.app/api/beacon}"
PID="${3:-mulesoft-anypoint-onboarding}"
SID="smoke_$(date +%s)"
fail=0
check() { code=$(curl -s -o /dev/null -w "%{http_code}" "$1"); echo "$([ "$code" = 200 ] && echo OK || echo FAIL) $code $1"; [ "$code" = 200 ] || fail=1; }
echo "=== Assets ==="
check "$BASE/demo-output/output.mp4"
check "$BASE/demo-output/output-hero-silent.mp4"
html=$(curl -s "$BASE/?editor=cursor")
for n in output.mp4 onboarding-welcome-full; do
  echo "$html" | grep -q "$n" && echo "OK page has $n" || { echo "FAIL missing $n"; fail=1; }
done
echo "$html" | grep -q "output-hero-silent" && { echo "FAIL silent loop still embedded"; fail=1; } || echo "OK no silent loop in HTML"
echo "=== Beacons ==="
for ev in video_started video_completed video_unmuted; do
  r=$(curl -s -X POST "$BEACON" -H "Content-Type: text/plain" -d "{\"proposal_id\":\"$PID\",\"session_id\":\"$SID\",\"event_type\":\"$ev\",\"slide_number\":0,\"slide_title\":\"smoke\",\"metadata\":{}}")
  echo "$r" | grep -q '"ok":true' && echo "OK $ev" || { echo "FAIL $ev"; fail=1; }
done
[ $fail -eq 0 ] && echo "SMOKE PASS" || { echo "SMOKE FAIL"; exit 1; }
