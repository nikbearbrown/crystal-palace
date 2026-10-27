#!/bin/bash
# usage: scripts/render_round.sh rNN RES SAMPLES
R=$1; RES=${2:-1280x720}; S=${3:-64}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
$B -b rounds/$R.blend -P scripts/render_views.py -- --cams REV_int_up_start,CP017_park_inside_end,REV_ext34_start,REV_south_start,PLATE_IV_south_ortho_start,REF_talbot_start,REF_absolon_start,REF_elm_north_start,CP017_park_inside_start,CP008_build_around_end,OPEN_gallery_start,DET_fountain_start --portrait REF_talbot_start --outdir renders/$R --res $RES --samples $S
$B -b rounds/$R.blend -P scripts/render_views.py -- --cams REV_combo_start --outdir renders/$R --res $RES --samples $S --claude ../crystal-palace-1851-claude/crystal-palace-1851.blend
echo ROUND_DONE
if [ -f rounds/${R}_owen.blend ]; then
$B -b rounds/${R}_owen.blend -P scripts/render_views.py -- --cams REV_int_up_start,REF_talbot_start,OPEN_gallery_start --portrait REF_talbot_start --outdir renders/$R/owen --res $RES --samples $S
echo OWEN_DONE
fi
