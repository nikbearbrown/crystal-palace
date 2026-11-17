#!/usr/bin/env bash
# CP048 upper-terrace north walk / bedding / visitors c. summer 1868 CANDIDATE (2026-11-17, no verdict): build + before/after renders,
# resumable per PNG.   scripts/render_cp048_candidate.sh [--no-build]
# before = rounds/sydenham-post66-r10.blend AS COMMITTED IN 972145e (md5 ed31acf2), extracted from git to /workspace/tmp/cp048/;
#          that is the blend the live hero renders/post66r10_CAM_CP048_terrace_hold_35mm.png was rendered from (look v1.1 batch,
#          survey look/sydenham_logs/CP048.log). The working-tree rounds/sydenham-post66-r10.blend (80f930f3, re-saved by S67b
#          b4daf98) renders differently (max diff 113) and is neither used nor touched.
# after  = rounds/candidates/sydenham-post66-r10_cp048terrace.blend (scripts/candidate_cp048_terrace.py on that base).
# Live hero recipe = survey look v1.1: /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP048 --era 1852
#   --tod exterior_afternoon --spp 24 --res 1280x720 --no-people (before at that recipe = live hero, max diff 0).
# Hero pair: live recipe (before/ after/) AND the same look at 1920x1080 / 48 spp both sides (1920x1080_48spp/).
# Side effects: the other post66-r10 exterior cameras that can see the upper terrace, both sides via scripts/render.py
#   NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp (sidefx_before/ sidefx_after/). Cameras not moved.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
REL=course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-post66-r10.blend
LIVE=/workspace/tmp/cp048/sydenham-post66-r10_972145e.blend; CAND=rounds/candidates/sydenham-post66-r10_cp048terrace.blend
OUT=renders/candidates/cp048_terrace_20261117; LOG=/workspace/logs/cp048_terrace_render.log
HERO=CAM_CP048_terrace_hold_35mm
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
SIDE="CAM_CP048_terrace_walk_35mm CAM_CP047_north_end_35mm CAM_ext_garden_34_terrace CAM_ext_elevated_overview"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp048
[[ -s $LIVE ]] || git show 972145e:$REL > $LIVE
[[ $(md5sum < $LIVE | cut -c1-8) == ed31acf2 ]] || { echo "post66-r10@972145e md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp048_terrace.py -- $CAND 2>&1 | grep -E "CP048 |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
look() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ "$1" == "." ]] && png="$OUT/$2/$HERO.png"
  [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) look $1 $2" >> $LOG
  "$B" -b $3 -P $LOOK -- --cam $HERO --out "$png" --scene-id CP048 --era 1852 --tod exterior_afternoon --spp $5 --res $4 --no-people >> $LOG 2>&1
}
look . before $LIVE 1280x720 24; look . after $CAND 1280x720 24
look 1920x1080_48spp before $LIVE 1920x1080 48; look 1920x1080_48spp after $CAND 1920x1080 48
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp048/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/post66r10_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
