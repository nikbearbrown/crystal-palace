#!/bin/bash
# CP034b dinner CANDIDATE renders (2026-11-13). Resumable: skips any PNG already present; writes DONE when all exist.
# usage: nohup scripts/render_cp034b_dinner.sh [--no-build] &   log: /workspace/logs/cp034b_dinner_render.log
# Recipe both sides: scripts/render.py on the round blend, 100%, 48 spp, 1920x1080 (scene res), no EXPO/RES overrides.
set -u
B=/workspace/blender5/blender
D=/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok
cd $D
OUT=renders/candidates/cp034b_dinner_20261113
LIVE=rounds/dinosaurs-1854-r05.blend
CAND=rounds/dinosaurs-1854-r06-cand.blend
CAMS="CAM_CP034b_iguanodon_dinner_28mm CAM_CP034_hawkins_studio_28mm"
mkdir -p $OUT/before $OUT/after
if [ "${1:-}" != "--no-build" ] && [ ! -f $CAND ]; then
  $B -b -P scripts/cand_cp034b_dinner_20261113.py || exit 1
fi
for side in before after; do
  blend=$LIVE; [ $side = after ] && blend=$CAND
  for c in $CAMS; do
    [ -f $OUT/$side/${side}_$c.png ] && { echo "skip $side $c"; continue; }
    [ -f $blend ] || { echo "missing $blend"; continue; }
    $B -b $blend -P scripts/render.py -- $OUT/$side.tmp $side 100 48 $c && mkdir -p $OUT/$side && mv $OUT/$side.tmp/${side}_$c.png $OUT/$side/ && echo "done $side $c $(date -u +%H:%M)"
  done
done
n=$(ls $OUT/before/*.png $OUT/after/*.png 2>/dev/null | wc -l)
[ $n -ge 4 ] && { md5sum $LIVE $CAND > $OUT/md5.txt; date -u > $OUT/DONE; echo ALL_DONE; }
