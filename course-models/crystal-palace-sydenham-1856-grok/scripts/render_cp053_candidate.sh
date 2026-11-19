#!/usr/bin/env bash
# CP053 lower-park trees in leaf, summer 1911 CANDIDATE (2026-11-19, no verdict): build + hero before/after at the live recipe,
# resumable per PNG.   scripts/render_cp053_candidate.sh [--no-build] [--sidefx]
# before = rounds/sydenham-late11-r14.blend (md5 9f90df23): the blend the live hero renders/r14_late11_CAM_CP053_empire_pavilions_wide_35mm.png
#          (md5 9236eda7, COVERAGE.md CP053) was rendered from (look v1.1 keep-better, 1b3c92d).
# after  = rounds/candidates/sydenham-late11-r14_cp053trees.blend (scripts/candidate_cp053_trees_in_leaf.py on that base).
# Live hero recipe = survey look v1.1 /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP053 --era 1852
#   --tod exterior_afternoon --spp 24 --res 1280x720 --no-people (look/sydenham_logs/CP053.log); before at that recipe = live hero, max diff 0.
# --sidefx (only after the hero pair is committed): cameras that see the new collection (scripts/cp053_visibility.py), both sides via
#   scripts/render.py NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp; set CP053_SIDE to the list.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; LOOK=/workspace/crystal-palace-survey/look/apply_render.py
LIVE=rounds/sydenham-late11-r14.blend; CAND=rounds/candidates/sydenham-late11-r14_cp053trees.blend
OUT=renders/candidates/cp053_trees_20261119; LOG=/workspace/logs/cp053_trees_render.log
HERO=CAM_CP053_empire_pavilions_wide_35mm
mkdir -p "$OUT"/{before,after,rebuild} /workspace/logs /workspace/tmp/cp053
[[ $(md5sum < $LIVE | cut -c1-8) == 9f90df23 ]] || { echo "late11-r14 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" && "${1:-}" != "--sidefx" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp053_trees_in_leaf.py -- $CAND 2>&1 | grep -E "CP053 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
hero() { # side blend
  local png="$OUT/$1/$HERO.png"; [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) hero $1" >> $LOG
  "$B" -b $2 -P $LOOK -- --cam $HERO --out "$png" --scene-id CP053 --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people >> $LOG 2>&1
}
hero before $LIVE; hero after $CAND
if [[ ! -s "$OUT/rebuild/$HERO.png" ]]; then   # rebuild from the base into a temp blend: must render the same hero (max diff 0)
  T=/workspace/tmp/cp053/rebuild.blend
  "$B" -b $LIVE -P scripts/candidate_cp053_trees_in_leaf.py -- $T 2>&1 | grep -E "CP053 BUILT" >> $LOG
  hero rebuild $T; rm -f $T
fi
if [[ "${1:-}" == "--sidefx" ]]; then
  mkdir -p "$OUT/sidefx_before" "$OUT/sidefx_after"
  export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
  one() { # dir blend cam
    local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
    local tmp=/workspace/tmp/cp053/rtmp_$1_$3; mkdir -p $tmp
    echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
    "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
  }
  for cam in ${CP053_SIDE:-}; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
  touch $OUT/DONE
fi
( cd $OUT && md5sum $(ls before/*.png after/*.png rebuild/*.png sidefx_*/*.png 2>/dev/null) > md5.txt ); md5sum $LIVE $CAND renders/r14_late11_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) HERO PAIR DONE" | tee -a $LOG
