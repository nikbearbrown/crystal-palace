#!/bin/bash
# usage: scripts/render_round.sh eNN [SAMPLES] [PCT]   (1280x720 base; never saves the .blend)
R=$1; S=${2:-28}; P=${3:-100}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
$B -b rounds/$R.blend -P scripts/render_shots.py -- --out renders/$R --samples $S --pct $P --frame 1 \
   --cams CP025_case_start,CP025_july_start,CP025_visitors_start,EX_osler_start,CP024_approach_start,EX_lineup_start
$B -b rounds/$R.blend -P scripts/render_shots.py -- --out renders/$R --samples $S --pct $P --frame 25 --suffix _f025 --exposure 0.3 --cams CP024_ram_start
echo ROUND_DONE
