#!/usr/bin/env bash
# CP062 morning after the fire, 1 Dec 1936 CANDIDATE (2026-11-17, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp062_candidate.sh [--no-build]
# before = rounds/sydenham-ruins-r17.blend (md5 2c3343c6, = as committed in 80f43ba dud-fix v4, unchanged since); that is the blend
#          the live hero renders/r17q_ruins_CAM_CP062_morning_between_towers_35mm.png (md5 acc315a7) was rendered from
#          (survey look/dud_fix/scripts/reframe_and_render.py: camera reframed + horizon_haze/fill hidden and SAVED into the round,
#          then crystal-palace-look v1.1 exterior_morning, 1280x720, 32 spp). Copied to /workspace/tmp/cp062/ and rendered from there.
# after  = rounds/candidates/sydenham-ruins-r17_cp062morning.blend (scripts/candidate_cp062_morning.py on that base).
# Live hero recipe = survey look v1.1: /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP062 --era 1852
#   --tod exterior_morning --spp 32 --res 1280x720 --no-people (before at that recipe = live hero, max diff 0).
# Hero pair: live recipe (before/ after/) AND the same look at 1920x1080 / 48 spp both sides (1920x1080_48spp/).
# Side effects: other ruins-r17 cameras that see the new geometry, both sides via scripts/render.py NO_PEOPLE=1 KEEP_LIGHTING=1
#   1280x720 48 spp (sidefx_before/ sidefx_after/). Cameras not moved.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=/workspace/tmp/cp062/sydenham-ruins-r17_2c3343c6.blend; CAND=rounds/candidates/sydenham-ruins-r17_cp062morning.blend
OUT=renders/candidates/cp062_morning_20261117; LOG=/workspace/logs/cp062_morning_render.log
HERO=CAM_CP062_morning_between_towers_35mm
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
SIDE="CAM_CP064_skyline_50mm CAM_CP072_footprint_35mm CAM_CP073_sphinx_steps_50mm CAM_compare_0007 CAM_ext_elevated_overview CAM_ext_garden_34_terrace"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp062
[[ -s $LIVE ]] || cp rounds/sydenham-ruins-r17.blend $LIVE
[[ $(md5sum < $LIVE | cut -c1-8) == 2c3343c6 ]] || { echo "ruins-r17 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp062_morning.py -- $CAND 2>&1 | grep -E "CP062 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
look() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ "$1" == "." ]] && png="$OUT/$2/$HERO.png"
  [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) look $1 $2" >> $LOG
  "$B" -b $3 -P $LOOK -- --cam $HERO --out "$png" --scene-id CP062 --era 1852 --tod exterior_morning --spp $5 --res $4 --no-people >> $LOG 2>&1
}
look . before $LIVE 1280x720 32; look . after $CAND 1280x720 32
look 1920x1080_48spp before $LIVE 1920x1080 48; look 1920x1080_48spp after $CAND 1920x1080 48
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp062/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r17q_ruins_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
