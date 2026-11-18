#!/usr/bin/env bash
# CP047 north end from the upper terrace, summer-1868 terrace walk / bedding / visitors CANDIDATE
# (2026-11-18, no verdict): build + before/after renders, resumable per PNG.   scripts/render_cp047_candidate.sh [--no-build]
# before = rounds/sydenham-post66-r10.blend AS COMMITTED IN 972145e (md5 ed31acf2), extracted from git to /workspace/tmp/cp047/;
#          that is the blend the live hero renders/r10final_CAM_CP047_north_end_35mm.png was rendered from (look v1.1 batch,
#          survey look/sydenham_logs/CP047.log). The working-tree rounds/sydenham-post66-r10.blend (80f930f3) is neither used nor touched.
# after  = rounds/candidates/sydenham-post66-r10_cp047northend.blend (scripts/candidate_cp047_northend.py on that base).
# Live hero recipe = survey look v1.1: /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP047 --era 1852
#   --tod exterior_afternoon --spp 24 --res 1280x720 --no-people (before at that recipe = live hero, max diff 0).
# Hero pair: live recipe (before/ after/) AND the same look at 1920x1080 / 48 spp both sides (1920x1080_48spp/).
# Side effects: the post66-r10 cameras that see any new object (ray-cast visibility test, scripts/cp047_visibility.py),
#   (CP048 terrace_hold 22.4 %, CP048 terrace_walk 22.4 %, plan_overlay_top 9.3 %, ext_elevated_overview 5.2 %, compare_0007 0.02 %,
#   ext_garden_34_terrace 0 %, all other post66-r10 cams 0) both sides via scripts/render.py NO_PEOPLE=1 KEEP_LIGHTING=1 1280x720 48 spp (sidefx_before/ sidefx_after/). Cameras not moved.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
REL=course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-post66-r10.blend
LIVE=/workspace/tmp/cp047/sydenham-post66-r10_972145e.blend; CAND=rounds/candidates/sydenham-post66-r10_cp047northend.blend
OUT=renders/candidates/cp047_northend_20261118; LOG=/workspace/logs/cp047_northend_render.log
HERO=CAM_CP047_north_end_35mm
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
SIDE="${CP047_SIDE:-CAM_CP048_terrace_hold_35mm CAM_CP048_terrace_walk_35mm CAM_plan_overlay_top CAM_ext_elevated_overview CAM_compare_0007 CAM_ext_garden_34_terrace}"
mkdir -p "$OUT"/{before,after} "$OUT"/1920x1080_48spp/{before,after} "$OUT/sidefx_before" "$OUT/sidefx_after" /workspace/logs /workspace/tmp/cp047
[[ -s $LIVE ]] || git show 972145e:$REL > $LIVE
[[ $(md5sum < $LIVE | cut -c1-8) == ed31acf2 ]] || { echo "post66-r10@972145e md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp047_northend.py -- $CAND 2>&1 | grep -E "CP04[78] |Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
look() { # dir side blend res spp
  local png="$OUT/$1/$2/$HERO.png"; [[ "$1" == "." ]] && png="$OUT/$2/$HERO.png"
  [[ -s "$png" ]] && return
  echo "$(date -u +%FT%TZ) look $1 $2" >> $LOG
  "$B" -b $3 -P $LOOK -- --cam $HERO --out "$png" --scene-id CP047 --era 1852 --tod exterior_afternoon --spp $5 --res $4 --no-people >> $LOG 2>&1
}
look . before $LIVE 1280x720 24; look . after $CAND 1280x720 24
look 1920x1080_48spp before $LIVE 1920x1080 48; look 1920x1080_48spp after $CAND 1920x1080 48
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
one() { # dir blend cam
  local png="$OUT/$1/$3.png"; [[ -s "$png" ]] && return
  local tmp=/workspace/tmp/cp047/rtmp_$1_$3; mkdir -p $tmp
  echo "$(date -u +%FT%TZ) render $1 $3" >> $LOG
  "$B" -b $2 -P scripts/render.py -- $tmp r 100 48 $3 >> $LOG 2>&1 && mv $tmp/r_$3.png "$png"
}
for cam in $SIDE; do one sidefx_before $LIVE $cam; one sidefx_after $CAND $cam; done
( cd $OUT && md5sum before/*.png after/*.png 1920x1080_48spp/*/*.png sidefx_*/*.png > md5.txt ); md5sum $LIVE $CAND renders/r10final_$HERO.png >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
