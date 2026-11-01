#!/bin/bash
# 2026-11-01 CP023 boots + foreground CANDIDATE (DEPARTURES PPL-C05, PPL-C06). Same as live
# render_cp023_v2.sh (r11_envelope_v2.blend, exposure -0.9, people gate off, crowd dressing on)
# plus --cp023-boots --cp023-foreground. Output renders/candidates/cp023_bootsfg_20261101/.
# "full" also saves the dressed scenes as sibling .blends (rounds/candidates/r11_envelope_v2_CP023_into_nave_{start,end}.blend).
# usage: scripts/render_cp023_bootsfg.sh [lean|full|both] [EXPOSURE]
MODE=${1:-both}; EXP=${2:--0.9}; [ "$EXP" = none ] && EXP=
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
C=CP023_into_nave_start,CP023_into_nave_end; O=renders/candidates/cp023_bootsfg_20261101
X=(--cp023-boots --cp023-foreground); [ -n "$EXP" ] && X+=(--exposure "$EXP")
mkdir -p /workspace/logs
if [ "$MODE" != full ]; then
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams $C --outdir $O/lean --res 1280x720 --samples 28 --threads 8 "${X[@]}" > /workspace/logs/transept_cp023_bootsfg_lean.log 2>&1
fi
if [ "$MODE" != lean ]; then
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams $C --outdir $O/full --res 1280x720 --samples 64 --threads 8 --save-blend-dir rounds/candidates "${X[@]}" > /workspace/logs/transept_cp023_bootsfg_full.log 2>&1
fi
echo CP023BOOTSFG_DONE $MODE
