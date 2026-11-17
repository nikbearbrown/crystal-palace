#!/usr/bin/env bash
# CP039 Pompeian Court peristyle CANDIDATE (2026-11-17, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp039_candidate.sh [--no-build]
# before = rounds/sydenham-1856-r13.blend (md5 74dc7aa3, unchanged; the blend the live hero
#          renders/r13_1856_CAM_CP039_pompeian_peristyle_28mm.png was rendered from).
# after  = rounds/candidates/sydenham-1856-r13_cp039pompeian.blend (scripts/candidate_cp039_pompeian.py on r13).
# Live hero recipe = r13 finals (/workspace/syd_scratch/r13/render_r13.sh): scripts/render.py, RES=1280x720, 100 %, 32 spp,
#   no PEOPLE_ERA / KEEP_LIGHTING / EXPO (look v1.1 REVERTED for CP039). before at that recipe = live hero, max diff 0.
# Hero pair: live recipe (before/ after/) AND 1920x1080 / 48 spp both sides (1920x1080_48spp/).
# Side effects: the two other CP039 cams at their r13 recipe (EXPO=1.5, 1280x720, 32 spp) and the exterior / compare cams whose
#   frustum contains the court, render.py NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp (sidefx_before/ sidefx_after/). Cameras not moved.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1856-r13.blend; CAND=rounds/candidates/sydenham-1856-r13_cp039pompeian.blend
OUT=renders/candidates/cp039_pompeian_20261117; LOG=/workspace/logs/cp039_pompeian_render.log
HERO=CAM_CP039_pompeian_peristyle_28mm
SIDE15="CAM_CP039_pompeian_atrium_28mm CAM_CP039_pompeian_wall_50mm"
SIDE="CAM_ext_elevated_overview CAM_compare_0007 CAM_CP042_cascade_50mm"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp039
[[ $(md5sum < $LIVE | cut -c1-8) == 74dc7aa3 ]] || { echo "r13 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp039_pompeian.py -- $CAND 2>&1 | grep -E "CP039 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
one() { # outpng blend cam res spp [env...]
  local png="$1" blend=$2 cam=$3 res=$4 spp=$5; shift 5
  [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp039/rtmp_$(basename $(dirname $png))_$(basename $(dirname $(dirname $png)))_$cam; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $png" >> $LOG
  env RES=$res THREADS=8 "$@" "$B" -b $blend -P scripts/render.py -- $tmp r 100 $spp $cam >> $LOG 2>&1 && mv $tmp/r_$cam.png "$png"
}
one $OUT/before/$HERO.png $LIVE $HERO 1280x720 32
one $OUT/after/$HERO.png $CAND $HERO 1280x720 32
one $OUT/1920x1080_48spp/before/$HERO.png $LIVE $HERO 1920x1080 48
one $OUT/1920x1080_48spp/after/$HERO.png $CAND $HERO 1920x1080 48
for cam in $SIDE15; do one $OUT/sidefx_before/$cam.png $LIVE $cam 1280x720 32 EXPO=1.5; one $OUT/sidefx_after/$cam.png $CAND $cam 1280x720 32 EXPO=1.5; done
for cam in $SIDE; do one $OUT/sidefx_before/$cam.png $LIVE $cam 1280x720 48 NO_PEOPLE=1 KEEP_LIGHTING=1; one $OUT/sidefx_after/$cam.png $CAND $cam 1280x720 48 NO_PEOPLE=1 KEEP_LIGHTING=1; done
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r13_1856_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
