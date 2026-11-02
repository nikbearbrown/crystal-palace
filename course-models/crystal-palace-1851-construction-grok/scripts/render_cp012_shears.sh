#!/bin/bash
# CANDIDATE CP012_bay sheer legs re-pitched (2026-11-02, DEPARTURES CN46; no verdict, NOT live).
# Builds rounds/candidates/c07_cp012bay_shears.blend from the LIVE rounds/candidates/c07_cp012bay.blend (unchanged)
# with scripts/cand_cp012_shears_20261102.py, then renders CP012_bay_start (frame 1) and CP012_bay_end (frame 96)
# with exactly the live settings of scripts/render_cp012_bay.sh (render_views.py, 1280x720, 48 spp, look exposure,
# --no-people). Before = the live renders (render_cp012_bay.sh reproduces them pixel-identically).
# usage: scripts/render_cp012_shears.sh [samples=48] [outdir=renders/candidates/cp012_shears_20261102] [--rebuild]
set -e
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
C=rounds/candidates/c07_cp012bay_shears.blend
OUT="${2:-renders/candidates/cp012_shears_20261102}"
if [ ! -f $C ] || [ "${3:-}" == "--rebuild" ]; then
  $B -b rounds/candidates/c07_cp012bay.blend -P scripts/cand_cp012_shears_20261102.py -- --out $C \
    --rake-dx 8 --splay 15 --move KWORKER_064_CP012=556:-171:15 2>&1 | grep -E "SPARS|HORSE|CLEAR|FRAME|SAVED|Error|Traceback"
fi
$B -b $C --python-expr "import bpy; bpy.context.scene.frame_set(1)" -P scripts/render_views.py -- \
  --cams CP012_bay_start --outdir "$OUT" --res 1280x720 --samples "${1:-48}" --no-people 2>&1 | grep -E "Saved|Error" || true
$B -b $C --python-expr "import bpy; bpy.context.scene.frame_set(96)" -P scripts/render_views.py -- \
  --cams CP012_bay_end --outdir "$OUT" --res 1280x720 --samples "${1:-48}" --no-people 2>&1 | grep -E "Saved|Error" || true
