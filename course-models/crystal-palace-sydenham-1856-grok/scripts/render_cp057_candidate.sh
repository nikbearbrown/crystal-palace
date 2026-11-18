#!/usr/bin/env bash
# CP057 'Trying to recover an audience' lower terrace, interwar visitors summer 1936 CANDIDATE
# (2026-11-18, no verdict): build + before/after renders, resumable per PNG.   scripts/render_cp057_candidate.sh [--no-build]
# before = rounds/sydenham-1936-r11.blend (md5 40140697, unchanged since 1b3c92d): the blend the live hero
#          renders/r11_1936_CAM_CP057_1936_lower_terrace_35mm.png was rendered from (look v1.1 batch, survey look/sydenham_logs/CP057.log).
# after  = rounds/candidates/sydenham-1936-r11_cp057visitors.blend (scripts/candidate_cp057_visitors.py on that base).
# Live hero recipe = survey look v1.1: /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP057 --era 1852
#   --tod exterior_afternoon --spp 24 --res 1280x720 --no-people (before at that recipe = live hero, max diff 0).
# Hero pair: live recipe (before/ after/) AND the same look at 1920x1080 / 48 spp both sides (1920x1080_48spp/).
# Side effects: the r11 cameras that see any new object (ray-cast visibility test, scripts/cp057_visibility.py ->
#   CP073 steps_35mm 1.87 %, central_transept_straight 0.93 %, compare_0074 0.37 %, ext_garden_34_terrace 0.29 %, compare_0007 0.02 %,
#   ext_elevated_overview 0.02 %, all other r11 cams 0) both sides via
#   scripts/render.py NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp (sidefx_before/ sidefx_after/).
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1936-r11.blend; CAND=rounds/candidates/sydenham-1936-r11_cp057visitors.blend
OUT=renders/candidates/cp057_visitors_20261118; LOG=/workspace/logs/cp057_visitors_render.log
HERO=CAM_CP057_1936_lower_terrace_35mm
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
SIDE="${CP057_SIDE:-CAM_CP073_steps_35mm CAM_central_transept_straight CAM_compare_0074 CAM_ext_garden_34_terrace CAM_compare_0007 CAM_ext_elevated_overview}"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp057
[[ $(md5sum < $LIVE | cut -c1-8) == 40140697 ]] || { echo "1936-r11 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp057_visitors.py -- $CAND 2>&1 | grep -E "CP057 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
look() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ "$1" == "." ]] && png="$OUT/$2/$HERO.png"
  [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) look $1 $2" >> $LOG
  "$B" -b $3 -P $LOOK -- --cam $HERO --out "$png" --scene-id CP057 --era 1852 --tod exterior_afternoon --spp $5 --res $4 --no-people >> $LOG 2>&1
}
look . before $LIVE 1280x720 24; look . after $CAND 1280x720 24
look 1920x1080_48spp before $LIVE 1920x1080 48; look 1920x1080_48spp after $CAND 1920x1080 48
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp057/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r11_1936_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
