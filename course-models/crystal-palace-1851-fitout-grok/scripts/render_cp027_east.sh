#!/usr/bin/env bash
# CP027 east-nave CANDIDATE renders (2026-11-12, DEPARTURES FT74-FT80). NOT live.
#   scripts/render_cp027_east.sh [--no-build] [--no-before]
# Builds rounds/candidates/h01_cp027east.blend from live rounds/h01.blend (never written) with scripts/cand_cp027_east_20261112.py,
# then renders before (live h01) and after (candidate) with the SAME recipe (FT80): render_views.py with people_lib v3.1 via
# scripts/render_views_ppl31.py (the lib of the live CP027 PNG, fitout b12c425/9494bf9), shared look --era 1851 (default tod
# interior_daylit, exposure from the look, identical both sides), 1920x1080, 48 spp, 8 threads.
# Hero CP027_stair_foot_start at 1920x1080/48 spp; side-effect cam CP027_gallery_rail_start at 1280x720/24 spp.
# Output renders/candidates/cp027_east_20261112/{before,after}/ ; log /workspace/logs/cp027_east_render.log ; done marker
# renders/candidates/cp027_east_20261112/DONE
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
SRC=rounds/h01.blend; CAND=rounds/candidates/h01_cp027east.blend
OUT=renders/candidates/cp027_east_20261112
BUILD=1; BEFORE=1
for a in "$@"; do case "$a" in --no-build) BUILD=0;; --no-before) BEFORE=0;; esac; done
mkdir -p $OUT/before $OUT/after; rm -f $OUT/DONE
if [[ $BUILD == 1 ]]; then "$B" -b -P scripts/cand_cp027_east_20261112.py -- --src $SRC --out $CAND; fi
R() { "$B" -b "$1" -P scripts/render_views_ppl31.py -- --cams "$2" --res "$3" --samples "$4" --era 1851 --threads 8 --outdir "$5"; }
for side in after before; do
  [[ $side == before && $BEFORE == 0 ]] && continue
  f=$CAND; [[ $side == before ]] && f=$SRC
  R $f CP027_stair_foot_start 1920x1080 48 $OUT/$side
  echo "CP027_EAST_STEP hero $side"
  R $f CP027_gallery_rail_start 1280x720 24 $OUT/$side
  echo "CP027_EAST_STEP sidefx $side"
done
md5sum $SRC $CAND > $OUT/md5.txt
date -u > $OUT/DONE
echo CP027_EAST_DONE
