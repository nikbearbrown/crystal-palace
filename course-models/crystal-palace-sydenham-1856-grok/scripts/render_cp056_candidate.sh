#!/usr/bin/env bash
# CP056 RND nave drill CANDIDATE (2026-11-13, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp056_candidate.sh [--no-build]
# before = live rounds/sydenham-war-r14.blend (md5 718c4b3d, unchanged); after = rounds/candidates/sydenham-war-r14_cp056rnd.blend.
# Recipe both sides = the live CP056 hero recipe (r14: scripts/render.py, blend lighting/exposure, baked people57, no adopt),
#   raised to 1920x1080 / 48 spp; same camera both sides (cameras not moved).
# Side-effect cams from the frustum/occlusion test (/workspace/tmp/cp056/vis.py): CP059_nave_fire, nave_interior_28mm,
#   ext_elevated_overview; CP056 terrace_drill + ranks rendered as no-change checks.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-war-r14.blend; CAND=rounds/candidates/sydenham-war-r14_cp056rnd.blend
OUT=renders/candidates/cp056_rnd_20261113; LOG=/workspace/logs/cp056_rnd_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs /workspace/tmp/cp056
[[ $(md5sum < $LIVE | cut -c1-8) == 718c4b3d ]] || { echo "live war-r14 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp056_rnd_nave_drill.py 2>&1 | grep -E "CP056 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
export NO_PEOPLE=1 RES=1920x1080 THREADS=8
one() { # side blend cam
  local side=$1 bl=$2 cam=$3; local png="$OUT/$side/$cam.png"
  [[ -s "$png" ]] && { echo "skip $png" >> $LOG; return; }
  local tmp=/workspace/tmp/cp056/rtmp_${side}_${cam}; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
  "$B" -b $bl -P scripts/render.py -- $tmp r 100 48 $cam >> $LOG 2>&1 && mv $tmp/r_$cam.png "$png"
}
for cam in CAM_CP056_nave_drill_gallery_28mm CAM_CP059_nave_fire_28mm CAM_nave_interior_28mm CAM_ext_elevated_overview CAM_CP056_terrace_drill_35mm CAM_CP056_ranks_50mm; do
  one before $LIVE $cam; one after $CAND $cam
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
