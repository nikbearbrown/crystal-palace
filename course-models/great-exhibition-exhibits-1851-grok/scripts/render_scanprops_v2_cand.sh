#!/bin/bash
# CANDIDATE v2 CP025 scan-props polish (2026-11-09). Never writes live rounds/e02.blend.
# usage: scripts/render_scanprops_v2_cand.sh [SAMPLES=28] [PCT=100]   (FORCE=1 to re-render)
#   1) builds rounds/candidates/e02_scanprops_v2.blend from live e02 (scripts/polish_scanprops_v2_cand.py, defaults)
#   2) renders BEFORE (live e02) and AFTER (candidate) with identical settings (render_round settings: 28 spp,
#      1920x1080, frame 1, shared look v1 interior_daylit exposure, people swap on; SAME camera order on both sides,
#      because the people swap runs per camera and its result depends on the order)
#   3) copies to survey look/pairs_geo/CANDIDATE_<shot>_scanprops_v2_{before,after}.png + _pair.png (scripts/pair_luma.py)
set -e
S=${1:-28}; P=${2:-100}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
PAIRS=/workspace/crystal-palace-survey/look/pairs_geo
O=renders/candidates/scanprops_v2_20261109
M0=$(md5sum rounds/e02.blend | cut -d' ' -f1)
[ "$M0" = fce122dabf730ae76b47d3cacf6d36b7 ] || echo "NOTE: live e02 md5 $M0 is not the 68cfae5 KEEP (fce122da)"
$B -b -P scripts/polish_scanprops_v2_cand.py -- --out rounds/candidates/e02_scanprops_v2.blend
CAMS=CP025_visitors_start,CP025_visitors_end,EX_lineup_start,CP025_july_start,CP025_case_start
for side in before after; do
  if [ $side = before ]; then BL=rounds/e02.blend; else BL=rounds/candidates/e02_scanprops_v2.blend; fi
  [ -f $O/$side/CP025_case_start.png ] && [ "$FORCE" != 1 ] && { echo "skip $side (done; FORCE=1 to redo)"; continue; }
  $B -b $BL -P scripts/render_shots.py -- --out $O/$side --samples $S --pct $P --frame 1 --cams $CAMS
done
[ "$M0" = "$(md5sum rounds/e02.blend | cut -d' ' -f1)" ] || { echo "LIVE e02 CHANGED"; exit 1; }
for shot in CP025_visitors_start CP025_visitors_end EX_lineup_start; do
  cp $O/before/$shot.png $PAIRS/CANDIDATE_${shot}_scanprops_v2_before.png
  cp $O/after/$shot.png  $PAIRS/CANDIDATE_${shot}_scanprops_v2_after.png
done
python3 scripts/pair_luma.py $O $PAIRS --tag scanprops_v2 --label "AFTER CANDIDATE e02_scanprops_v2 (lit gilt cabinet, Greek Slave niche + fill, vase fill)" | tee $O/luma.txt
echo SCANPROPS_V2_CAND_DONE
