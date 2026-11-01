#!/bin/bash
# 2026-11-01 CP023 crowd dressing CANDIDATE (DEPARTURES PPL-C01..C04): same as render_cp023_v2.sh
# (r11_envelope_v2.blend, exposure -0.9, people gate off) but with the CP023 dressing on
# (render_views.py default) and output under renders/candidates/cp023_dressing_20261101/.
# usage: scripts/render_cp023_dressing.sh [lean|full|both] [EXPOSURE]   (never saves any .blend)
MODE=${1:-both}; EXP=${2:--0.9}; [ "$EXP" = none ] && EXP=
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
C=CP023_into_nave_start,CP023_into_nave_end; O=renders/candidates/cp023_dressing_20261101
X=(); [ -n "$EXP" ] && X=(--exposure "$EXP")
mkdir -p /workspace/logs
if [ "$MODE" != full ]; then
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams $C --outdir $O/lean --res 1280x720 --samples 28 --threads 8 "${X[@]}" > /workspace/logs/transept_cp023_dress_lean.log 2>&1
fi
if [ "$MODE" != lean ]; then
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams $C --outdir $O/full --res 1280x720 --samples 64 --threads 8 "${X[@]}" > /workspace/logs/transept_cp023_dress_full.log 2>&1
fi
echo CP023DRESS_DONE $MODE
