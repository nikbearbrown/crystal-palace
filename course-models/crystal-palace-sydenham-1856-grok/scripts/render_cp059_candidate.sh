#!/usr/bin/env bash
# CP059 nave planting burning, night of 30 Nov 1936 CANDIDATE (2026-11-18, no verdict): build + before/after renders,
# resumable per PNG.   scripts/render_cp059_candidate.sh [--no-build]
# before = rounds/sydenham-1936fire-r11b.blend (md5 62396fca): the blend the live hero renders/r11b_1936fire_CAM_CP059_nave_fire_28mm.png
#          (md5 77640c3a, COVERAGE.md CP059) was rendered from (commit 9aff52a).
# after  = rounds/candidates/sydenham-1936fire-r11b_cp059planting.blend (scripts/candidate_cp059_burning_planting.py on that base).
# Live hero recipe = RES=960x540 scripts/render.py -- <dir> r11b_1936fire 100 32 <cam> (blend's own Filmic -0.5 EV, no people, no look
#   pass; before at that recipe = live hero, max diff 0). Also a 1920x1080 48 spp pair (the blend's own size/spp) for the 1080p cut.
# Side effects: ray-cast visibility (scripts/cp059_visibility.py) sees the new collection only from CP059 (4.44 %), section_cut_x-300
#   (0.77 %) and plan_overlay_top (0.02 %); ray casts stop at glass, so the cameras that look through the glazing at the nave are rendered
#   too: CP061 transept_collapse (live hero on this round), nave_interior_28mm, central_transept_straight, ext_elevated_overview, CP001.
#   Both sides via scripts/render.py NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1936fire-r11b.blend; CAND=rounds/candidates/sydenham-1936fire-r11b_cp059planting.blend
OUT=renders/candidates/cp059_planting_20261118; LOG=/workspace/logs/cp059_planting_render.log
HERO=CAM_CP059_nave_fire_28mm
SIDE="${CP059_SIDE:-CAM_CP061_transept_collapse_35mm CAM_nave_interior_28mm CAM_section_cut_x-300 CAM_plan_overlay_top CAM_central_transept_straight CAM_ext_elevated_overview CAM_CP001_prologue_distant_35mm}"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp059
[[ $(md5sum < $LIVE | cut -c1-8) == 62396fca ]] || { echo "1936fire-r11b md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp059_burning_planting.py -- $CAND 2>&1 | grep -E "CP059 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
hero() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ "$1" == "." ]] && png="$OUT/$2/$HERO.png"
  [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp059/htmp_$1_$2; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) hero $1 $2" >> $LOG
  ( unset EXPO KEEP_LIGHTING NO_PEOPLE PEOPLE_ERA THREADS; RES=$4 "$B" -b $3 -P scripts/render.py -- $tmp r11b_1936fire 100 $5 $HERO >> $LOG 2>&1 ) && mv $tmp/r11b_1936fire_$HERO.png "$png"
}
hero . before $LIVE 960x540 32; hero . after $CAND 960x540 32
hero 1920x1080_48spp before $LIVE 1920x1080 48; hero 1920x1080_48spp after $CAND 1920x1080 48
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp059/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r11b_1936fire_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
