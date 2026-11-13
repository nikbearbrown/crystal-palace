#!/usr/bin/env bash
# CP060 hose crews CANDIDATE (2026-11-13, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp060_candidate.sh [--no-build]
# before = rounds/sydenham-1936fire-r12.blend (md5 33102f4b, unchanged; the FIRE state the storyboard asks for, 30 Nov 1936)
# after  = rounds/candidates/sydenham-1936fire-r12_cp060hose.blend (scripts/candidate_cp060_hose_crews.py on fire-r12).
# Recipe both sides: scripts/render.py, NO_PEOPLE=1 (baked figures), blend lighting/exposure (fire-r12: Filmic, -0.5 EV),
#   1920x1080, 48 spp, same camera (cameras not moved).
# Context only (NOT exposure-matched): the COVERAGE CP060 hero renders/r12_1936_CAM_CP060_crowd_watching_35mm.png comes from the
#   pre-fire daylight round rounds/sydenham-1936-r12.blend (md5 ab117e6c, -1.0 EV); re-rendered here at the same res/spp as livehero.
# Side-effect cams (frustum test /workspace/tmp/cp060/vis.py; none of them has a live hero on fire-r12): CP058 parade_appliances, CP061.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1936fire-r12.blend; CAND=rounds/candidates/sydenham-1936fire-r12_cp060hose.blend; DAY=rounds/sydenham-1936-r12.blend
OUT=renders/candidates/cp060_hose_20261113; LOG=/workspace/logs/cp060_hose_render.log
mkdir -p "$OUT/before" "$OUT/after" "$OUT/livehero" /workspace/logs /workspace/tmp/cp060
[[ $(md5sum < $LIVE | cut -c1-8) == 33102f4b ]] || { echo "fire-r12 md5 mismatch" | tee -a $LOG; exit 3; }
[[ $(md5sum < $DAY | cut -c1-8) == ab117e6c ]] || { echo "1936-r12 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp060_hose_crews.py 2>&1 | grep -E "CP060 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
export NO_PEOPLE=1 RES=1920x1080 THREADS=8
one() { # side blend cam
  local side=$1 bl=$2 cam=$3; local png="$OUT/$side/$cam.png"
  [[ -s "$png" ]] && { echo "skip $png" >> $LOG; return; }
  local tmp=/workspace/tmp/cp060/rtmp_${side}_${cam}; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
  "$B" -b $bl -P scripts/render.py -- $tmp r 100 48 $cam >> $LOG 2>&1 && mv $tmp/r_$cam.png "$png"
}
one before $LIVE CAM_CP060_crowd_watching_35mm; one after $CAND CAM_CP060_crowd_watching_35mm
one livehero $DAY CAM_CP060_crowd_watching_35mm
for cam in CAM_CP058_parade_appliances_35mm CAM_CP061_transept_collapse_35mm; do
  one before $LIVE $cam; one after $CAND $cam
done
( cd $OUT && md5sum before/*.png after/*.png livehero/*.png > md5.txt ); md5sum $LIVE $CAND $DAY >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
