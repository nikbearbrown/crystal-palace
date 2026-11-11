#!/usr/bin/env bash
# CP014_drain_whole "Downes plate" CANDIDATE 2026-11-11 (DEPARTURES KD07-KD13). KEEP 2026-11-11, now LIVE (see
# scripts/render_cp014_plate_live.sh). Builds rounds/candidates/k01_cp014plate.blend from the PRE-KEEP k01 (md5 6f647743...,
# committed at 9436402; never from the promoted live k01, which already carries KD7_*) via
# scripts/cand_cp014_plate_20261111.py, then renders CP014_drain_whole_start with the live hero recipe (look v1 era 1850,
# tod studio, 24 spp, 720x1280 portrait; reproduces the committed renders/k01/CP014_drain_whole_start.png at max diff 0):
# before = live k01 at the look exposure (0.40), after = candidate at -0.13 (re-matched to the before mean luma).
#   scripts/render_cp014_plate.sh [samples=24] [outdir=renders/candidates/cp014_plate_20261111]
set -euo pipefail
cd "$(dirname "$0")/.."
BASE=$(mktemp --suffix=.blend); trap 'rm -f "$BASE"' EXIT
git show 9436402:course-models/crystal-palace-1851-construction-grok/rounds/k01.blend > "$BASE"
[[ $(md5sum < "$BASE" | cut -c1-8) == 6f647743 ]] || { echo "base k01 md5 mismatch"; exit 3; }
B=/workspace/blender5/blender; S=${1:-24}; R=${2:-renders/candidates/cp014_plate_20261111}; EA=${EXP_AFTER:--0.13}
"$B" -b "$BASE" -P scripts/cand_cp014_plate_20261111.py -- --out rounds/candidates/k01_cp014plate.blend 2>&1 | grep -E "SOIL|LABELS_OUT|SAVED|Error|Traceback"
"$B" -b "$BASE" -P scripts/render_views.py -- --cams CP014_drain_whole_start --outdir "$R/before" --res 1280x720 --samples "$S" --era 1850 --tod studio --threads 8 2>&1 | grep -E "WROTE|Error" || true
"$B" -b rounds/candidates/k01_cp014plate.blend -P scripts/render_views.py -- --cams CP014_drain_whole_start --outdir "$R/after" --res 1280x720 --samples "$S" --era 1850 --tod studio --threads 8 --exposure "$EA" 2>&1 | grep -E "WROTE|Error" || true
