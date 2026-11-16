#!/usr/bin/env bash
# CP033 slope works CANDIDATE (2026-11-16, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp033_candidate.sh [--no-build]
# before = rounds/sydenham-build53-r18b.blend (md5 dc579904, unchanged; the blend the live hero
#          renders/r18_build53_CAM_CP033_slope_up_35mm.png was rendered from — before re-render is pixel-identical to it)
# after  = rounds/candidates/sydenham-build53-r18b_cp033slope.blend (scripts/candidate_cp033_slope.py on build53-r18b).
# Recipe both sides = live hero recipe: scripts/render.py, NO_PEOPLE=1, KEEP_LIGHTING=1 (Filmic -1.0 EV), 1280x720, 48 spp,
#   same camera (cameras not moved). Every camera in the round is rendered on both sides so side effects can be measured.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-build53-r18b.blend; CAND=rounds/candidates/sydenham-build53-r18b_cp033slope.blend
OUT=renders/candidates/cp033_slope_20261116; LOG=/workspace/logs/cp033_slope_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs /workspace/tmp/cp033
[[ $(md5sum < $LIVE | cut -c1-8) == dc579904 ]] || { echo "build53-r18b md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp033_slope.py -- $CAND 2>&1 | grep -E "CP033 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
CAMS="CAM_CP033_slope_up_35mm CAM_CP033_terrace_cut_35mm CAM_CP033_frame_rising_35mm CAM_CP033_transept_ribs_28mm
CAM_ext_elevated_overview CAM_ext_garden_34_terrace CAM_CP001_prologue_distant_35mm CAM_CP057_1936_lower_terrace_35mm
CAM_CP062_morning_between_towers_35mm CAM_CP064_skyline_50mm CAM_CP073_steps_35mm CAM_CP073_sphinx_steps_50mm
CAM_CP061_transept_collapse_35mm CAM_CP047_north_end_35mm CAM_CP048_terrace_hold_35mm CAM_CP048_terrace_walk_35mm
CAM_central_transept_straight CAM_compare_0007 CAM_compare_0074 CAM_compare_0108_alhambra CAM_CP038_egyptian_entry_28mm
CAM_CP038_egyptian_hold_28mm CAM_CP041_alhambra_entry_28mm CAM_CP041_alhambra_hold_28mm CAM_CP041_insert_spandrel_50mm
CAM_CP058_parade_appliances_35mm CAM_CP059_nave_fire_28mm CAM_CP060_crowd_watching_35mm CAM_CP072_footprint_35mm
CAM_nave_interior_28mm CAM_north_transept_colossi_35mm CAM_section_cut_x-300 CAM_plan_overlay_top"
one() { # side blend cam
  local side=$1 bl=$2 cam=$3; local png="$OUT/$side/$cam.png"
  [[ -s "$png" ]] && { echo "skip $png" >> $LOG; return; }
  local tmp=/workspace/tmp/cp033/rtmp_${side}_${cam}; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
  "$B" -b $bl -P scripts/render.py -- $tmp r 100 48 $cam >> $LOG 2>&1 && mv $tmp/r_$cam.png "$png"
}
for cam in $CAMS; do one before $LIVE $cam; one after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
