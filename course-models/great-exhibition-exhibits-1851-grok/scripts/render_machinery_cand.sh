#!/bin/bash
# CANDIDATE CP024 Machinery Court stand dressing (2026-11-02). Never writes live rounds/e02.blend.
# usage: scripts/render_machinery_cand.sh [SAMPLES] [PCT]
#   1) rebuilds rounds/candidates/e02_machinery_dress.blend from live e02 (scripts/polish_machinery_dress.py)
#   2) renders BEFORE (live e02) and AFTER (candidate) with identical settings:
#      CP024_approach_start/end at frame 1, shared look v1 exposure; CP024_ram_start at frame 25, --exposure 0.3
#   3) copies to survey look/pairs_geo/CANDIDATE_CP024_machinery_<shot>_{before,after}.png
set -e
S=${1:-28}; P=${2:-100}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
PAIRS=/workspace/crystal-palace-survey/look/pairs_geo
O=renders/candidates/machinery_20261102
M0=$(md5sum rounds/e02.blend | cut -d' ' -f1)
$B -b rounds/e02.blend -P scripts/polish_machinery_dress.py -- --out rounds/candidates/e02_machinery_dress.blend
for side in before after; do
  if [ $side = before ]; then BL=rounds/e02.blend; else BL=rounds/candidates/e02_machinery_dress.blend; fi
  $B -b $BL -P scripts/render_shots.py -- --out $O/$side --samples $S --pct $P --frame 1 --cams CP024_approach_start,CP024_approach_end
  $B -b $BL -P scripts/render_shots.py -- --out $O/$side --samples $S --pct $P --frame 25 --suffix _f025 --exposure 0.3 --cams CP024_ram_start
done
[ "$M0" = "$(md5sum rounds/e02.blend | cut -d' ' -f1)" ] || { echo "LIVE e02 CHANGED"; exit 1; }
for shot in approach_start approach_end ram_start_f025; do
  cp $O/before/CP024_$shot.png $PAIRS/CANDIDATE_CP024_machinery_${shot}_before.png
  cp $O/after/CP024_$shot.png  $PAIRS/CANDIDATE_CP024_machinery_${shot}_after.png
done
echo MACHINERY_CAND_DONE
