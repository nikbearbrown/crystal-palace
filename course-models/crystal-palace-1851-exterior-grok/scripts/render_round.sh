#!/bin/bash
# usage: scripts/render_round.sh xNN RES SAMPLES TRANSEPT_BLEND
# Every frame is the completed 1851 building: Claude's west frame + Grok transept + this exterior, appended read-only.
R=$1; RES=${2:-1280x720}; S=${3:-48}
TB=${4:-/workspace/crystal-palace/course-models/crystal-palace-1851-transept-grok/rounds/r07.blend}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
CL=../crystal-palace-1851-claude/crystal-palace-1851.blend
$B -b rounds/$R.blend -P scripts/render_views.py -- --cams EXT_SE_34_start,EXT_east_end_start,EXT_NE_strip_start,EXT_int_east_nave_start,PLATE_V_east_ortho_start,PLATE_IV_full_south_ortho_start,REF_aerial_SE_start --outdir renders/$R --res $RES --samples $S --claude $CL --transept $TB
echo ROUND_DONE
