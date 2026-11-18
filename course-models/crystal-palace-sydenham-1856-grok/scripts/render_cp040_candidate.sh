#!/usr/bin/env bash
# CP040 English Mediaeval Court: Rochester door coloured / niches + canopies / upper-tier statues / two floor monuments CANDIDATE
# (2026-11-18, no verdict): build + before/after renders, resumable per PNG.   scripts/render_cp040_candidate.sh [--no-build]
# before = rounds/sydenham-1856-r14.blend (md5 00df0959, unchanged since 1c96ad7) = the blend the live hero
#          renders/r14_1856_CAM_CP040_mediaeval_court_28mm.png was rendered from (survey look v1.1 batch, look/sydenham_logs/CP040.log).
# after  = rounds/candidates/sydenham-1856-r14_cp040mediaeval.blend (scripts/candidate_cp040_mediaeval.py on that base).
# Live hero recipe = survey look v1.1: /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP040 --era 1851
#   --tod interior_daylit --spp 24 --res 1280x720 --no-people (before at that recipe = live hero, max diff 0).
# Hero pair: live recipe (before/ after/) AND the same look at 1920x1080 / 48 spp both sides (1920x1080_48spp/).
# Side effects: the r14 cameras that see any new object (ray-cast visibility test over all 44 r14 cameras: rochester_door_50mm
#   53.9 %, mediaeval_front_28mm 5.2 %, compare_0108_alhambra 0.02 %, all others 0), both sides via scripts/render.py
#   NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp (sidefx_before/ sidefx_after/). Cameras not moved.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1856-r14.blend; CAND=rounds/candidates/sydenham-1856-r14_cp040mediaeval.blend
OUT=renders/candidates/cp040_mediaeval_20261118; LOG=/workspace/logs/cp040_mediaeval_render.log
HERO=CAM_CP040_mediaeval_court_28mm
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
SIDE="CAM_CP040_rochester_door_50mm CAM_CP040_mediaeval_front_28mm CAM_compare_0108_alhambra"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp040r
[[ $(md5sum < $LIVE | cut -c1-8) == 00df0959 ]] || { echo "r14 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp040_mediaeval.py -- $CAND 2>&1 | grep -E "CP040 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
look() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ "$1" == "." ]] && png="$OUT/$2/$HERO.png"
  [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) look $1 $2" >> $LOG
  "$B" -b $3 -P $LOOK -- --cam $HERO --out "$png" --scene-id CP040 --era 1851 --tod interior_daylit --spp $5 --res $4 --no-people >> $LOG 2>&1
}
look . before $LIVE 1280x720 24; look . after $CAND 1280x720 24
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp040r/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
unset NO_PEOPLE KEEP_LIGHTING RES THREADS
look 1920x1080_48spp before $LIVE 1920x1080 48; look 1920x1080_48spp after $CAND 1920x1080 48
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r14_1856_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
