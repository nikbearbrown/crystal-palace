#!/usr/bin/env bash
# CP041 Alhambra Court Owen Jones polychromy + stilted imposts, 1854-1856 CANDIDATE
# (2026-11-18, no verdict): build + before/after renders, resumable per PNG.   scripts/render_cp041_candidate.sh [--no-build]
# before = rounds/sydenham-1856-r08b.blend (md5 60c76d85): the blend the live hero renders/r08bfinal_CAM_CP041_insert_spandrel_50mm.png
#          (md5 33f7133c, COVERAGE.md CP041) was rendered from (commit 45f1031; survey look v1.1 pass reverted, look/sydenham_verdicts.json).
# after  = rounds/candidates/sydenham-1856-r08b_cp041polychromy.blend (scripts/candidate_cp041_polychromy.py on that base).
# Live hero recipe = scripts/render.py -- <dir> r08bfinal 100 48 <cam> (the blend's own 1920x1080, Filmic -1.0 EV, 48 spp, no people;
#   before at that recipe = live hero, max diff 0).
# Side effects: the r08b cameras that see any new object (ray-cast visibility, scripts/cp041_visibility.py -> CP041 alhambra_hold 49.2 %,
#   alhambra_entry 45.3 %, compare_0108_alhambra 32.8 %, section_cut_x-300 0.10 %, all other r08b cams 0) both sides via
#   scripts/render.py NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/sydenham-1856-r08b.blend; CAND=rounds/candidates/sydenham-1856-r08b_cp041polychromy.blend
OUT=renders/candidates/cp041_polychromy_20261118; LOG=/workspace/logs/cp041_polychromy_render.log
HERO=CAM_CP041_insert_spandrel_50mm
SIDE="${CP041_SIDE:-CAM_CP041_alhambra_hold_28mm CAM_CP041_alhambra_entry_28mm CAM_compare_0108_alhambra CAM_section_cut_x-300}"
mkdir -p "$OUT"/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp041
[[ $(md5sum < $LIVE | cut -c1-8) == 60c76d85 ]] || { echo "1856-r08b md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp041_polychromy.py -- $CAND 2>&1 | grep -E "CP041 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
hero() { # side blend
  local png="$OUT/$1/$HERO.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp041/htmp_$1; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) hero $1" >> $LOG
  ( unset RES EXPO KEEP_LIGHTING NO_PEOPLE PEOPLE_ERA THREADS; "$B" -b $2 -P scripts/render.py -- $tmp r08bfinal 100 48 $HERO >> $LOG 2>&1 ) && mv $tmp/r08bfinal_$HERO.png "$png"
}
hero before $LIVE; hero after $CAND
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp041/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r08bfinal_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
