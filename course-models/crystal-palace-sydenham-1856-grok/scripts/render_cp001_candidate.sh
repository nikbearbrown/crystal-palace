#!/usr/bin/env bash
# CP001 glow-on-the-hill CANDIDATE (2026-11-16, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp001_candidate.sh [--no-build]
# before = rounds/sydenham-1936-r18b.blend (md5 66edd7cd, unchanged; the blend the live hero was rendered from: PNG metadata
#          File=rounds/sydenham-1936-r18b.blend, Camera=CAM_CP001_prologue_distant_35mm, cycles samples 48, 1280x720).
# after  = rounds/candidates/sydenham-1936-r18b_cp001glow.blend (scripts/candidate_cp001_glow.py on 1936-r18b).
# Live recipe both sides: scripts/render.py, NO_PEOPLE=1, KEEP_LIGHTING=1 (blend exposure Filmic -1.0 EV, unchanged by the
#   candidate), RES=1280x720 (the live hero's resolution), 48 spp, same camera (cameras not moved).
# Side-effect cams: every other storyboard camera in this round (the candidate changes the world/sun to night, so all of them
#   change); none has a live hero on 1936-r18b (COVERAGE: only CP001 lives on it).
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1936-r18b.blend; CAND=rounds/candidates/sydenham-1936-r18b_cp001glow.blend
OUT=renders/candidates/cp001_glow_20261116; LOG=/workspace/logs/cp001_glow_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs /workspace/tmp/cp001
[[ $(md5sum < $LIVE | cut -c1-8) == 66edd7cd ]] || { echo "1936-r18b md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp001_glow.py -- $CAND 2>&1 | grep -E "CP001 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # side blend cam
  local side=$1 bl=$2 cam=$3; local png="$OUT/$side/$cam.png"
  [[ -s "$png" ]] && { echo "skip $png" >> $LOG; return; }
  local tmp=/workspace/tmp/cp001/rtmp_${side}_${cam}; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
  "$B" -b $bl -P scripts/render.py -- $tmp r 100 48 $cam >> $LOG 2>&1 && mv $tmp/r_$cam.png "$png"
}
one before $LIVE CAM_CP001_prologue_distant_35mm; one after $CAND CAM_CP001_prologue_distant_35mm
for cam in CAM_CP057_1936_lower_terrace_35mm CAM_CP062_morning_between_towers_35mm CAM_CP064_skyline_50mm \
           CAM_CP060_crowd_watching_35mm CAM_CP058_parade_appliances_35mm CAM_CP061_transept_collapse_35mm \
           CAM_CP072_footprint_35mm CAM_CP073_steps_35mm CAM_CP073_sphinx_steps_50mm CAM_CP047_north_end_35mm \
           CAM_CP048_terrace_hold_35mm CAM_CP048_terrace_walk_35mm CAM_CP059_nave_fire_28mm CAM_CP038_egyptian_hold_28mm \
           CAM_CP038_egyptian_entry_28mm CAM_CP041_alhambra_hold_28mm CAM_CP041_alhambra_entry_28mm CAM_CP041_insert_spandrel_50mm; do
  one before $LIVE $cam; one after $CAND $cam
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
