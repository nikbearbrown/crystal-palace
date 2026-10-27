#!/bin/bash
# usage: scripts/render_round.sh dNN RES SAMPLES
R=$1; RES=${2:-1280x720}; S=${3:-48}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
X=../crystal-palace-1851-exterior-grok/rounds/x05.blend
CL=../crystal-palace-1851-claude/crystal-palace-1851.blend
$B -b $X -P scripts/render_dismantle.py -- --dismantle rounds/${R}_empty.blend --state empty --cams CP030_empty_walk_start,CP030_empty_walk_end,CP030_empty_aisle_start --outdir renders/$R --res $RES --samples $S --claude $CL
$B -b $X -P scripts/render_dismantle.py -- --dismantle rounds/${R}_dismantle.blend --state dismantle --cams CP031_joint_detail_start,CP031_lateral_start,CP031_lateral_end,REV_dismantle_aerial_start --outdir renders/$R --res $RES --samples $S --claude $CL
echo ROUND_DONE
