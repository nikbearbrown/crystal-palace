#!/bin/bash
# CANDIDATE CP025 exhibit-court scan props (2026-11-09). Never writes live rounds/e02.blend.
# usage: scripts/render_scanprops_cand.sh [SAMPLES=28] [PCT=100]
#   1) rebuilds rounds/candidates/e02_scanprops.blend from live e02 (scripts/polish_scanprops_cand.py; props from assets/scanprops/)
#   2) renders BEFORE (live e02) and AFTER (candidate) with identical settings (render_round.sh settings:
#      28 spp, 1920x1080, frame 1, shared look v1 interior_daylit exposure, people swap on):
#      pairs: CP025_visitors_start, CP025_visitors_end, EX_lineup_start; regression only: CP025_july_start, CP025_case_start
#   3) copies to survey look/pairs_geo/CANDIDATE_<shot>_scanprops_{before,after}.png (+ _pair.png via scripts/pair_luma.py)
set -e
S=${1:-28}; P=${2:-100}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
PAIRS=/workspace/crystal-palace-survey/look/pairs_geo
O=renders/candidates/scanprops_20261109
M0=$(md5sum rounds/e02.blend | cut -d' ' -f1)
$B -b -P scripts/polish_scanprops_cand.py -- --out rounds/candidates/e02_scanprops.blend
CAMS=CP025_visitors_start,CP025_visitors_end,EX_lineup_start,CP025_july_start,CP025_case_start
for side in before after; do
  if [ $side = before ]; then BL=rounds/e02.blend; else BL=rounds/candidates/e02_scanprops.blend; fi
  [ -f $O/$side/CP025_case_start.png ] && [ "$FORCE" != 1 ] && { echo "skip $side (done; FORCE=1 to redo)"; continue; }
  $B -b $BL -P scripts/render_shots.py -- --out $O/$side --samples $S --pct $P --frame 1 --cams $CAMS
done
[ "$M0" = "$(md5sum rounds/e02.blend | cut -d' ' -f1)" ] || { echo "LIVE e02 CHANGED"; exit 1; }
for shot in CP025_visitors_start CP025_visitors_end EX_lineup_start; do
  cp $O/before/$shot.png $PAIRS/CANDIDATE_${shot}_scanprops_before.png
  cp $O/after/$shot.png  $PAIRS/CANDIDATE_${shot}_scanprops_after.png
done
python3 scripts/pair_luma.py $O $PAIRS | tee $O/luma.txt
echo SCANPROPS_CAND_DONE
