#!/usr/bin/env bash
# CP007 "committee" CANDIDATE 2026-11-10 (DEPARTURES SD43-SD49; NOT live, awaiting review).
# Builds rounds/candidates/s02_cp007committee.blend from the live rounds/s02.blend (never written) via
# scripts/cand_cp007_committee_20261110.py, then renders CP007_start at 1920x1080, 96 spp, --keep-lighting --no-people
# (the recipe that reproduces the live renders/s02_png/CP007_start.png: authored lighting, scene exposure -0.4), with the
# exposure re-matched to the live mean luma (155.35 at 960x540 grey): -0.4 -> 0.85.
#   scripts/render_cp007_committee.sh [--no-build] [samples=96] [outdir=renders/candidates/cp007_committee_20261110/after]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BUILD=1; [ "${1:-}" = "--no-build" ] && { BUILD=0; shift; }
S=${1:-96}; R=${2:-renders/candidates/cp007_committee_20261110/after}
ES=${EXP_START:-0.85}
CAND=rounds/candidates/s02_cp007committee.blend
mkdir -p rounds/candidates "$R"
if [ "$BUILD" = 1 ]; then
  python3 scripts/cp007_plan_sheet.py
  "$B" -b rounds/s02.blend -P scripts/cand_cp007_committee_20261110.py -- --out "$CAND" 2>&1 | grep -E "W7|Error|Traceback"
  md5sum "$CAND"
fi
"$B" -b "$CAND" -P scripts/render_shots.py -- --cams CP007_start --out "$R" --samples "$S" --pct 100 --keep-lighting --no-people --exposure "$ES" 2>&1 | grep -E "RENDERED|Error" || true
echo CP007_COMMITTEE_DONE
