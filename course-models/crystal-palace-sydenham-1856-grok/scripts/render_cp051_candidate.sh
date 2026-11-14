#!/usr/bin/env bash
# CP051 1903 SMMT motor show CANDIDATE (2026-11-14, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp051_candidate.sh [--no-build]
# before = live rounds/sydenham-late11-r16.blend (md5 3ce48caf, unchanged); after = rounds/candidates/sydenham-late11-r16_cp051motor.blend.
# Recipe both sides = the live LATE11 hero recipe (scripts/render.py, blend lighting/exposure Filmic -1.0, GN people57, no adopt),
#   raised to 1920x1080 / 48 spp; same camera both sides (cameras not moved).
# Side-effect cams from the frustum test (/workspace/tmp/cp051/vis.py): CP052 scaffold_reglaze, CP054 plymouth_rescue,
#   CP049 worn_garden_front (late11 flags hidden), nave_interior_28mm, CP059_nave_fire (late11 round only).
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-late11-r16.blend; CAND=rounds/candidates/sydenham-late11-r16_cp051motor.blend
OUT=renders/candidates/cp051_motor_20261114; LOG=/workspace/logs/cp051_motor_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs /workspace/tmp/cp051
[[ $(md5sum < $LIVE | cut -c1-8) == 3ce48caf ]] || { echo "live late11-r16 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  env -u CP051_NOSAVE "$B" -b $LIVE -P scripts/candidate_cp051_motor_show.py 2>&1 | grep -E "CP051 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
export NO_PEOPLE=1 RES=1920x1080 THREADS=8
one() { # side blend cam
  local side=$1 bl=$2 cam=$3; local png="$OUT/$side/$cam.png"
  [[ -s "$png" ]] && { echo "skip $png" >> $LOG; return; }
  local tmp=/workspace/tmp/cp051/rtmp_${side}_${cam}; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
  "$B" -b $bl -P scripts/render.py -- $tmp r 100 48 $cam >> $LOG 2>&1 && mv $tmp/r_$cam.png "$png"
}
for cam in CAM_CP051_electric_nave_28mm CAM_CP052_scaffold_reglaze_35mm CAM_CP054_plymouth_rescue_35mm CAM_CP049_worn_garden_front_35mm CAM_nave_interior_28mm CAM_CP059_nave_fire_28mm; do
  one before $LIVE $cam; one after $CAND $cam
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
