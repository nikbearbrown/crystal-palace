#!/usr/bin/env bash
# CP029 east-nave CANDIDATE renders (2026-11-12, DEPARTURES FT81-FT87). NOT live.
#   scripts/render_cp029_east.sh [--no-build] [--no-before]
# Builds rounds/candidates/c02_cp029east.blend from live rounds/c02.blend (never written) with scripts/cand_cp029_east_20261112.py,
# then renders before (live c02) and after (candidate) with the SAME recipe (FT87): render_views.py with people_lib v3.1 via
# scripts/render_views_ppl31.py (the lib of the live CP029 PNG, fitout b7069ee), shared look --era 1851 (default tod
# interior_daylit, exposure from the look, identical both sides; a 640x360 test matched the stored live PNG, luma 58.9 vs 57.9,
# whereas --keep-lighting gave 105.7), 1920x1080, 48 spp, 8 threads.
# Hero CP029_dais_start and side-effect cam CP029_gallery_start, both 1920x1080/48 spp.
# Output renders/candidates/cp029_east_20261112/{before,after}/ ; done marker renders/candidates/cp029_east_20261112/DONE
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
SRC=rounds/c02.blend; CAND=rounds/candidates/c02_cp029east.blend
OUT=renders/candidates/cp029_east_20261112
BUILD=1; BEFORE=1
for a in "$@"; do case "$a" in --no-build) BUILD=0;; --no-before) BEFORE=0;; esac; done
mkdir -p $OUT/before $OUT/after; rm -f $OUT/DONE
if [[ $BUILD == 1 ]]; then "$B" -b -P scripts/cand_cp029_east_20261112.py -- --src $SRC --out $CAND; fi
R() { "$B" -b "$1" -P scripts/render_views_ppl31.py -- --cams "$2" --res "$3" --samples "$4" --era 1851 --threads 8 --outdir "$5"; }
for side in after before; do
  [[ $side == before && $BEFORE == 0 ]] && continue
  f=$CAND; [[ $side == before ]] && f=$SRC
  R $f CP029_dais_start 1920x1080 48 $OUT/$side
  echo "CP029_EAST_STEP hero $side"
  R $f CP029_gallery_start 1920x1080 48 $OUT/$side
  echo "CP029_EAST_STEP sidefx $side"
done
md5sum $SRC $CAND > $OUT/md5.txt
date -u > $OUT/DONE
echo CP029_EAST_DONE
