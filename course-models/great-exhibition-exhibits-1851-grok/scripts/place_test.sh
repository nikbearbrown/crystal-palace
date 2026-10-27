#!/bin/bash
# PLACEMENT TEST ONLY (EX11): hero assets instanced into the transept r10 east block-outs + Claude's west nave, appended at
# render time. Neither host file is written: no save call anywhere; Claude's .blend is only read by libraries.load.
# usage: scripts/place_test.sh eNN [SAMPLES] [PCT]
R=$1; S=${2:-48}; P=${3:-100}; W=$((1280*P/100)); H=$((720*P/100))
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."; HERE=$(pwd)
T=/workspace/crystal-palace/course-models/crystal-palace-1851-transept-grok
C=$T/../crystal-palace-1851-claude/crystal-palace-1851.blend
[ -f "$C" ] || C=$HERE/../crystal-palace-1851-claude/crystal-palace-1851.blend
mkdir -p renders/$R/placement
cd $T && $B -b rounds/r10.blend -P $HERE/scripts/place_exhibits.py -P scripts/render_views.py -- \
  --lib $HERE/rounds/$R.blend --hide-clash --clear-sightlines --frame 1 \
  --place "EXH_KOHINOOR:96,0,0,0;EXH_OSLER_CANDELABRUM:108,-22,0,0;EXH_NASMYTH_HAMMER:-456,4,0,0" \
  --pcam "PL_east_koh_osler:132,-33,5.25:103,-11,5.5:35;PL_west_hammer:-446,-30,5.25:-456,4,9:35" \
  --cams ${CAMS:-PL_east_koh_osler,PL_west_hammer} --outdir $HERE/renders/$R/placement --res ${W}x${H} --samples $S --claude $C
echo PLACE_DONE
