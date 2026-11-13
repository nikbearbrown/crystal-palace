#!/usr/bin/env bash
# CP044 railway-entrance CANDIDATE (2026-11-13, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp044_candidate.sh [--no-build]
# before = live rounds/sydenham-1856-r16.blend (md5 1b984fb6, unchanged); after = rounds/candidates/sydenham-1856-r16_cp044gate.blend.
# Recipe both sides = the live CP044 hero recipe (scripts/batch_people_v31_crowds.py group CP037+CP044):
#   render.py, PEOPLE_ERA=1850s PEOPLE_SEED=81, blend lighting, raised to 1920x1080 / 48 spp; one camera per session.
#   before/live      : live camera CAM_CP044_pay_desks_35mm (nave palm garden)  -> reframe pair
#   before/samecam_* : live geometry seen from the candidate cameras (scripts/cp044_link_cams.py, in memory)
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1856-r16.blend; CAND=rounds/candidates/sydenham-1856-r16_cp044gate.blend
OUT=renders/candidates/cp044_gate_20261113; LOG=/workspace/logs/cp044_gate_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs
[[ $(md5sum < $LIVE | cut -c1-8) == 1b984fb6 ]] || { echo "live r16 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp044_railway_entrance.py 2>&1 | grep -E "CP044 SAVED|Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
export PEOPLE_ERA=1850s PEOPLE_SEED=81 RES=1920x1080 THREADS=8
one() { # side blend cam outname [extra -P]
  local side=$1 bl=$2 cam=$3 name=$4; shift 4; local png="$OUT/$side/$name.png"
  [[ -s "$png" ]] && { echo "skip $png" >> $LOG; return; }
  local tmp=/workspace/tmp/cp044/rtmp_${side}_${name}; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $side $name ($cam)" >> $LOG
  "$B" -b $bl "$@" -P scripts/render.py -- $tmp r 100 48 $cam >> $LOG 2>&1 && mv $tmp/r_$cam.png "$png"
}
one before $LIVE CAM_CP044_pay_desks_35mm live_CAM_CP044_pay_desks_35mm
one before $LIVE CAM_CP044_pay_desks_35mm samecam_CAM_CP044_pay_desks_35mm -P scripts/cp044_link_cams.py
one before $LIVE CAM_CP044_maintenance_50mm samecam_CAM_CP044_maintenance_50mm -P scripts/cp044_link_cams.py
one after $CAND CAM_CP044_pay_desks_35mm CAM_CP044_pay_desks_35mm
one after $CAND CAM_CP044_maintenance_50mm CAM_CP044_maintenance_50mm
for spec in ${SIDEFX:-}; do   # side-effect cams, same camera both sides
  one before $LIVE $spec $spec; one after $CAND $spec $spec
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
