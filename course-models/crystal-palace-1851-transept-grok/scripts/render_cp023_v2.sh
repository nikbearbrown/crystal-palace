#!/bin/bash
# 2026-11-01 envelope v2 KEEP for CP023: render CP023 start/end from rounds/candidates/r11_envelope_v2.blend
# at the normal look exposure (no SHOT_EXPOSURE entry for this blend) plus a small lift:
# default EXPOSURE -0.9 = look interior_daylit -1.20 + 0.3 (DEPARTURES ENV2-11; read dim next to CP021/CP022).
# Pass "none" to render at the bare look exposure. People gate off for CP023 (render_views.py).
#   lean = 1280x720, 28 spp (check settings)   full = render_round.sh live settings (1280x720, 64 spp, 8 threads)
# usage: scripts/render_cp023_v2.sh [lean|full|both] [EXPOSURE]   (never saves any .blend)
MODE=${1:-both}; EXP=${2:--0.9}; [ "$EXP" = none ] && EXP=
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
C=CP023_into_nave_start,CP023_into_nave_end; O=renders/r11_envelope_v2
X=(); [ -n "$EXP" ] && X+=(--exposure "$EXP")   # crowd dressing KEEP 2026-11-01 (PPL-C01..C04): live is dressed; pass --no-cp023-dressing via render_views to undo
# 2026-11-01 parent review: END keeps boots + foreground (PPL-C05/C06 KEEP); START stays boots-free/foreground-free
# (foreground REJECTED; boots-only start is a CANDIDATE, scripts/render_cp023_boots.sh). Start and end render separately.
XEND=(--cp023-boots --cp023-foreground)
if [ "$MODE" != full ]; then
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams CP023_into_nave_start --outdir $O/cp023_lean --res 1280x720 --samples 28 --threads 8 "${X[@]}" > /workspace/logs/transept_cp023v2_lean.log 2>&1
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams CP023_into_nave_end --outdir $O/cp023_lean --res 1280x720 --samples 28 --threads 8 "${X[@]}" "${XEND[@]}" > /workspace/logs/transept_cp023v2_lean_end.log 2>&1
fi
if [ "$MODE" != lean ]; then
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams CP023_into_nave_start --outdir $O/cp023_full --res 1280x720 --samples 64 --threads 8 "${X[@]}" > /workspace/logs/transept_cp023v2_full.log 2>&1
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams CP023_into_nave_end --outdir $O/cp023_full --res 1280x720 --samples 64 --threads 8 "${X[@]}" "${XEND[@]}" > /workspace/logs/transept_cp023v2_full_end.log 2>&1
fi
echo CP023V2_DONE
