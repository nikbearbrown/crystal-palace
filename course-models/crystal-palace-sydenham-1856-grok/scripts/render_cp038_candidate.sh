#!/usr/bin/env bash
# CP038 Egyptian Court outer court: lion avenue / portico reliefs / winged globe / visitors CANDIDATE (2026-11-17, no verdict):
# build + before/after renders, resumable per PNG.   scripts/render_cp038_candidate.sh [--no-build]
# before = rounds/sydenham-1856-r08.blend (md5 0aa6e9ce, unchanged since 968c1d5) = the blend the live hero
#          renders/r08final_CAM_CP038_egyptian_hold_28mm.png was rendered from (survey look v1.1 batch, look/sydenham_logs/CP038.log).
# after  = rounds/candidates/sydenham-1856-r08_cp038lions.blend (scripts/candidate_cp038_lions.py on that base).
# Live hero recipe = survey look v1.1: /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP038 --era 1851
#   --tod interior_daylit --spp 24 --res 1280x720 --no-people (before at that recipe = live hero, max diff 0).
# Hero pair: live recipe (before/ after/) AND the same look at 1920x1080 / 48 spp both sides (1920x1080_48spp/).
# Side effects: every other camera in the r08 round, both sides via scripts/render.py NO_PEOPLE=1 KEEP_LIGHTING=1
#   1280x720 48 spp (sidefx_before/ sidefx_after/). Cameras not moved.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1856-r08.blend; CAND=rounds/candidates/sydenham-1856-r08_cp038lions.blend
OUT=renders/candidates/cp038_lions_20261117; LOG=/workspace/logs/cp038_lions_render.log
HERO=CAM_CP038_egyptian_hold_28mm
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
SIDE="CAM_CP038_egyptian_entry_28mm CAM_CP041_alhambra_entry_28mm CAM_CP041_alhambra_hold_28mm CAM_CP041_insert_spandrel_50mm CAM_central_transept_straight CAM_compare_0007 CAM_compare_0074 CAM_compare_0108_alhambra CAM_ext_elevated_overview CAM_ext_garden_34_terrace CAM_nave_interior_28mm CAM_plan_overlay_top CAM_section_cut_x-300"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp038
[[ $(md5sum < $LIVE | cut -c1-8) == 0aa6e9ce ]] || { echo "r08 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp038_lions.py -- $CAND 2>&1 | grep -E "CP038 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
look() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ "$1" == "." ]] && png="$OUT/$2/$HERO.png"
  [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) look $1 $2" >> $LOG
  "$B" -b $3 -P $LOOK -- --cam $HERO --out "$png" --scene-id CP038 --era 1851 --tod interior_daylit --spp $5 --res $4 --no-people >> $LOG 2>&1
}
look . before $LIVE 1280x720 24; look . after $CAND 1280x720 24
look 1920x1080_48spp before $LIVE 1920x1080 48; look 1920x1080_48spp after $CAND 1920x1080 48
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp038/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r08final_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
