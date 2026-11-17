#!/usr/bin/env bash
# CP036 railway colonnade CANDIDATE (2026-11-17, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp036_candidate.sh [--no-build]
# before = rounds/sydenham-open54-r14.blend (md5 104ee46d, unchanged; the blend the live hero
#          renders/r14_open54_CAM_CP036_covered_way_28mm.png was rendered from).
# after  = rounds/candidates/sydenham-open54-r14_cp036colonnade.blend (scripts/candidate_cp036_colonnade.py on open54-r14).
# Live hero recipe = survey look v1.1: /workspace/crystal-palace-survey/look/apply_render.py --era 1851 --tod interior_daylit
#   --spp 24 --res 1280x720 --no-people (before at that recipe is pixel-identical to the live hero, max diff 0).
# Hero pairs: live recipe (live_1280x720_24spp/) AND the same look at 1920x1080 / 48 spp both sides (1920x1080_48spp/, the pair to judge).
# Side effects: every camera whose frustum contains changed geometry (scripts list below, from a frustum test), both sides
#   via scripts/render.py NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp (sidefx_before/ sidefx_after/). Cameras not moved.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-open54-r14.blend; CAND=rounds/candidates/sydenham-open54-r14_cp036colonnade.blend
OUT=renders/candidates/cp036_colonnade_20261117; LOG=/workspace/logs/cp036_colonnade_render.log
HERO=CAM_CP036_covered_way_28mm
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
SIDE="CAM_CP036_platform_arrival_28mm CAM_CP036_station_exterior_35mm CAM_CP035_dais_50mm CAM_CP035_procession_nave_28mm CAM_CP001_prologue_distant_35mm CAM_CP040_mediaeval_court_28mm CAM_CP040_mediaeval_front_28mm CAM_CP064_skyline_50mm CAM_compare_0108_alhambra"
mkdir -p "$OUT"/{live_1280x720_24spp,1920x1080_48spp}/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp036
[[ $(md5sum < $LIVE | cut -c1-8) == 104ee46d ]] || { echo "open54-r14 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp036_colonnade.py -- $CAND 2>&1 | grep -E "CP036 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
look() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) look $1 $2" >> $LOG
  "$B" -b $3 -P $LOOK -- --cam $HERO --out "$png" --scene-id CP036 --era 1851 --tod interior_daylit --spp $5 --res $4 --no-people >> $LOG 2>&1
}
look live_1280x720_24spp before $LIVE 1280x720 24; look live_1280x720_24spp after $CAND 1280x720 24
look 1920x1080_48spp before $LIVE 1920x1080 48; look 1920x1080_48spp after $CAND 1920x1080 48
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp036/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum */*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r14_open54_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
