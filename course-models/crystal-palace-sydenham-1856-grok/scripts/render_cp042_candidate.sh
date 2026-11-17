#!/usr/bin/env bash
# CP042 water temples / cascades / arcade cataract CANDIDATE (2026-11-17, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp042_candidate.sh [--no-build]
# before = rounds/sydenham-1856-r13.blend (md5 74dc7aa3, unchanged; the blend the live hero
#          renders/r13_1856_CAM_CP042_cascade_50mm.png was rendered from).
# after  = rounds/candidates/sydenham-1856-r13_cp042cascade.blend (scripts/candidate_cp042_cascades.py on r13).
# Live hero recipe = survey look v1.1: /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP042 --era 1851
#   --tod exterior_afternoon --spp 24 --res 1280x720 --no-people (before at that recipe is pixel-identical to the live hero, max diff 0).
# Hero pair: live recipe (before/ after/) AND the same look at 1920x1080 / 48 spp both sides (1920x1080_48spp/).
# Side effects (small set): the other three CP042 cameras + the elevated overview, both sides via scripts/render.py
#   NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp (sidefx_before/ sidefx_after/). Cameras not moved.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1856-r13.blend; CAND=rounds/candidates/sydenham-1856-r13_cp042cascade.blend
OUT=renders/candidates/cp042_cascade_20261117; LOG=/workspace/logs/cp042_cascade_render.log
HERO=CAM_CP042_cascade_50mm
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
SIDE="CAM_CP042_terrace_basin_35mm CAM_CP042_terrace_overlook_35mm CAM_CP042_great_basins_35mm CAM_ext_elevated_overview"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp042
[[ $(md5sum < $LIVE | cut -c1-8) == 74dc7aa3 ]] || { echo "r13 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp042_cascades.py -- $CAND 2>&1 | grep -E "CP042 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
look() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ "$1" == "." ]] && png="$OUT/$2/$HERO.png"
  [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) look $1 $2" >> $LOG
  "$B" -b $3 -P $LOOK -- --cam $HERO --out "$png" --scene-id CP042 --era 1851 --tod exterior_afternoon --spp $5 --res $4 --no-people >> $LOG 2>&1
}
look . before $LIVE 1280x720 24; look . after $CAND 1280x720 24
look 1920x1080_48spp before $LIVE 1920x1080 48; look 1920x1080_48spp after $CAND 1920x1080 48
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp042/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r13_1856_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
