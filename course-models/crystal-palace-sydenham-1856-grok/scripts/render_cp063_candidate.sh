#!/usr/bin/env bash
# CP063 clearance CANDIDATE (2026-11-13, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp063_candidate.sh [--no-build]
# before = live rounds/sydenham-clearance-r17.blend (md5 055ef338, unchanged); after = rounds/candidates/sydenham-clearance-r17_cp063scrap.blend.
# Recipe both sides = the live CP063 hero recipe (r17q: scripts/render.py, blend lighting/exposure, no people adopt),
#   raised to 1920x1080 / 48 spp; same camera both sides (cameras not moved).
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-clearance-r17.blend; CAND=rounds/candidates/sydenham-clearance-r17_cp063scrap.blend
OUT=renders/candidates/cp063_scrap_20261113; LOG=/workspace/logs/cp063_scrap_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs /workspace/tmp/cp063
[[ $(md5sum < $LIVE | cut -c1-8) == 055ef338 ]] || { echo "live clearance-r17 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp063_scrap_clearance.py 2>&1 | grep -E "CP063 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
export NO_PEOPLE=1 RES=1920x1080 THREADS=8
one() { # side blend cam
  local side=$1 bl=$2 cam=$3; local png="$OUT/$side/$cam.png"
  [[ -s "$png" ]] && { echo "skip $png" >> $LOG; return; }
  local tmp=/workspace/tmp/cp063/rtmp_${side}_${cam}; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
  "$B" -b $bl -P scripts/render.py -- $tmp r 100 48 $cam >> $LOG 2>&1 && mv $tmp/r_$cam.png "$png"
}
for cam in CAM_CP063_crane_lift_50mm CAM_CP063_scrap_gang_35mm CAM_CP063_clearance_perimeter_35mm CAM_CP063_terrace_edge_35mm; do
  one before $LIVE $cam; one after $CAND $cam
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
