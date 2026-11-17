#!/usr/bin/env bash
# CP035 royal dais CANDIDATE (2026-11-17, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp035_candidate.sh [--no-build]
# before = rounds/sydenham-open54-r16.blend (md5 683b1bc9, unchanged; the blend the live hero
#          renders/r16/r16_CAM_CP035_transept_gallery_28mm.png was rendered from).
# after  = rounds/candidates/sydenham-open54-r16_cp035dais.blend (scripts/install_cp035_royal_dais.py on open54-r16).
# Live hero recipe = scripts/render.py, NO_PEOPLE=1, blend lighting (KEEP_LIGHTING=1, Filmic -1.0 EV), 1280x720, **28 spp**
#   (r16 'lean heroes'); before at 28 spp is pixel-identical to the live hero. Both sides are ALSO rendered at 48 spp
#   (the pair to judge) for every camera in the round so side effects can be measured. Cameras not moved.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-open54-r16.blend; CAND=rounds/candidates/sydenham-open54-r16_cp035dais.blend
OUT=renders/candidates/cp035_dais_20261117; LOG=/workspace/logs/cp035_dais_render.log
HERO=CAM_CP035_transept_gallery_28mm
mkdir -p "$OUT/before" "$OUT/after" "$OUT/before_28spp" "$OUT/after_28spp" /workspace/logs /workspace/tmp/cp035
[[ $(md5sum < $LIVE | cut -c1-8) == 683b1bc9 ]] || { echo "open54-r16 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/install_cp035_royal_dais.py -- $CAND 2>&1 | grep -E "CP035 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
CAMS=$("$B" -b $LIVE --python-expr "import bpy; print('CAMLIST', ' '.join(sorted(o.name for o in bpy.data.objects if o.type == 'CAMERA')))" 2>/dev/null | grep '^CAMLIST' | cut -d' ' -f2-)
one() { # dir blend cam spp
  local d=$1 bl=$2 cam=$3 spp=$4; local png="$OUT/$d/$cam.png"
  [[ -s "$png" ]] && { echo "skip $png" >> $LOG; return; }
  local tmp=/workspace/tmp/cp035/rtmp_${d}_${cam}; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $d $cam" >> $LOG
  "$B" -b $bl -P scripts/render.py -- $tmp r 100 $spp $cam >> $LOG 2>&1 && mv $tmp/r_$cam.png "$png"
}
one before_28spp $LIVE $HERO 28; one after_28spp $CAND $HERO 28
one before $LIVE $HERO 48; one after $CAND $HERO 48
for cam in $CAMS; do one before $LIVE $cam 48; one after $CAND $cam 48; done
( cd $OUT && md5sum before*/*.png after*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r16/r16_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
