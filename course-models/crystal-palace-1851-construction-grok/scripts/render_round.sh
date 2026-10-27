#!/bin/bash
# usage: scripts/render_round.sh cNN RES SAMPLES
R=$1; RES=${2:-1280x720}; S=${3:-48}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
$B -b rounds/$R.blend -P scripts/render_views.py -- --cams CP010_foundations_start,CP010_base_insert_start,CP011_yard_start,CP012_bay_start,CP012_joint_insert_start,CP013_sash_start,CP013_platform_start,CP014_gutter_start,CP015_blinds_start,CP016_trolley_start,REV_site_aerial_start --outdir renders/$R --res $RES --samples $S --frame 48
$B -b rounds/$R.blend -P scripts/render_views.py -- --cams CP015_louvre_start --outdir renders/$R --res $RES --samples $S --frame 1 --suffix _f001
$B -b rounds/$R.blend -P scripts/render_views.py -- --cams CP015_louvre_start --outdir renders/$R --res $RES --samples $S --frame 48 --suffix _f048
$B -b rounds/$R.blend -P scripts/render_views.py -- --cams CP014_section_start --outdir renders/$R --res 720x1280 --samples $S --frame 48
echo ROUND_DONE
