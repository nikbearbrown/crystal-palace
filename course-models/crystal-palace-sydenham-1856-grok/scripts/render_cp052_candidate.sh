#!/usr/bin/env bash
# CP052 'Repair never finishes' transept front, glaziers + painters c.1900 CANDIDATE
# (2026-11-18, no verdict): build + before/after renders, resumable per PNG.   scripts/render_cp052_candidate.sh [--no-build]
# before = rounds/sydenham-late11-r16.blend (md5 3ce48caf): the blend the live hero renders/r16/r16_CAM_CP052_scaffold_reglaze_35mm.png
#          was rendered from (survey dud-fix v4, look/dud_fix/diag/r_CP052.log; camera saved into the blend by that reframe).
# after  = rounds/candidates/sydenham-late11-r16_cp052repair.blend (scripts/candidate_cp052_repair.py on that base).
# Live hero recipe = scripts/render_cp052_look.py (look v1.1 apply_look CP052 = 1852 / exterior_afternoon, 1280x720, 32 spp;
#   before at that recipe = live hero, max diff 0).
# Hero pair: live recipe (before/ after/) AND the same look at 1920x1080 / 48 spp both sides (1920x1080_48spp/).
# Side effects: the r16 cameras that see any new object (ray-cast visibility, scripts/cp052_visibility.py -> CP061 transept_collapse 2.03 %,
#   CP049 worn_garden_front 0.19 %, section_cut_x-300 0.12 %, ext_elevated_overview 0.06 %, CP053 empire_pavilions_wide 0.02 %,
#   CP064 skyline 0.02 %, all other r16 cams 0) both sides via scripts/render.py NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-late11-r16.blend; CAND=rounds/candidates/sydenham-late11-r16_cp052repair.blend
OUT=renders/candidates/cp052_repair_20261118; LOG=/workspace/logs/cp052_repair_render.log
HERO=CAM_CP052_scaffold_reglaze_35mm
SIDE="${CP052_SIDE:-CAM_CP061_transept_collapse_35mm CAM_CP049_worn_garden_front_35mm CAM_section_cut_x-300 CAM_ext_elevated_overview CAM_CP053_empire_pavilions_wide_35mm CAM_CP064_skyline_50mm}"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp052
[[ $(md5sum < $LIVE | cut -c1-8) == 3ce48caf ]] || { echo "late11-r16 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp052_repair.py -- $CAND 2>&1 | grep -E "CP052 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
look() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ "$1" == "." ]] && png="$OUT/$2/$HERO.png"
  [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) look $1 $2" >> $LOG
  "$B" -b $3 -P scripts/render_cp052_look.py -- "$png" $HERO $5 $4 >> $LOG 2>&1
}
look . before $LIVE 1280x720 32; look . after $CAND 1280x720 32
look 1920x1080_48spp before $LIVE 1920x1080 48; look 1920x1080_48spp after $CAND 1920x1080 48
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp052/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r16/r16_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
