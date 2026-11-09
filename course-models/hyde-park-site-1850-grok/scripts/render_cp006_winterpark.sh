#!/usr/bin/env bash
# CP006 "winterpark" CANDIDATE 2026-11-09 (DEPARTURES SD35-SD41; NOT live, awaiting review).
# Builds rounds/candidates/s02_cp006park.blend from the live rounds/s02.blend (never written) via
# scripts/cand_cp006_winterpark_20261109.py, then renders CP006_start/_end at 1920x1080, 96 spp, --no-people, each with
# the recipe that reproduces its live renders/s02_png frame (live start = authored lighting + CP006 state exposure -0.25,
# i.e. --keep-lighting --state-exposure; live end = shared look v1.1 path, exposure -0.85), exposure re-matched to the live
# mean luma (start 185.15, end 184.60 at 960x540 grey): start -0.25 -> 0.14, end -0.85 -> -0.50.
#   scripts/render_cp006_winterpark.sh [--no-build] [samples=96] [outdir=renders/candidates/cp006_winterpark_20261109/after]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BUILD=1; [ "${1:-}" = "--no-build" ] && { BUILD=0; shift; }
S=${1:-96}; R=${2:-renders/candidates/cp006_winterpark_20261109/after}
ES=${EXP_START:-0.14}; EE=${EXP_END:--0.50}
CAND=rounds/candidates/s02_cp006park.blend
mkdir -p rounds/candidates "$R"
if [ "$BUILD" = 1 ]; then
  "$B" -b rounds/s02.blend -P scripts/cand_cp006_winterpark_20261109.py -- --out "$CAND" 2>&1 | grep -E "W6|PERSON|Error|Traceback"
  md5sum "$CAND"
fi
"$B" -b "$CAND" -P scripts/render_shots.py -- --cams CP006_start --out "$R" --samples "$S" --pct 100 --keep-lighting --no-people --exposure "$ES" 2>&1 | grep -E "RENDERED|Error" || true
"$B" -b "$CAND" -P scripts/render_shots.py -- --cams CP006_end --out "$R" --samples "$S" --pct 100 --no-people --exposure "$EE" 2>&1 | grep -E "RENDERED|Error" || true
echo CP006_WINTERPARK_DONE
