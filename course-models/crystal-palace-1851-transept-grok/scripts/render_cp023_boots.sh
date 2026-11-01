#!/bin/bash
# 2026-11-01 CP023 boots-only START CANDIDATE (DEPARTURES PPL-C05; foreground PPL-C06 REJECTED for start).
# Same as live render_cp023_v2.sh (r11_envelope_v2.blend, exposure -0.9, people gate off, crowd dressing on,
# 1280x720, 64 spp, 8 threads) plus --cp023-boots only. Start camera only. Never saves any .blend.
# Output renders/candidates/cp023_boots_20261101/CP023_into_nave_start.png
# usage: scripts/render_cp023_boots.sh [EXPOSURE]
EXP=${1:--0.9}; [ "$EXP" = none ] && EXP=
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
O=renders/candidates/cp023_boots_20261101
X=(--cp023-boots); [ -n "$EXP" ] && X+=(--exposure "$EXP")
mkdir -p /workspace/logs
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams CP023_into_nave_start --outdir $O --res 1280x720 --samples 64 --threads 8 "${X[@]}" > /workspace/logs/transept_cp023_boots_start.log 2>&1
echo CP023BOOTS_DONE $?
