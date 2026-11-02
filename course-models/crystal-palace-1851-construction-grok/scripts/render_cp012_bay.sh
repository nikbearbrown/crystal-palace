#!/bin/bash
# Live CP012_bay (KEEP 2026-11-02 start+end, DEPARTURES CN45; parent viewed the pairs). Live renders:
# renders/candidates/cp012_bay_20261102/CP012_bay_{start,end}.png. Superseded c07 files (rounds/c07.blend, renders/c07/CP012_bay_start.png) are kept.
# Renders ONLY CP012_bay_start (frame 1: girder hanging, top 19 ft) and CP012_bay_end (frame 96: girder seated, top 22 ft 2 in)
# from the CP012-only blend rounds/candidates/c07_cp012bay.blend; rebuilt from rounds/c07.blend if missing.
# Never render other shots from that blend (moved head scaffolds, cameras, gate cart group; hidden KWORKER_005/006/062; animated girder).
# CP012_joint_insert is NOT rendered here (still c07).
# usage: scripts/render_cp012_bay.sh [samples=48] [outdir=renders/candidates/cp012_bay_20261102]
set -e
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
C=rounds/candidates/c07_cp012bay.blend
OUT="${2:-renders/candidates/cp012_bay_20261102}"
if [ ! -f $C ]; then
  $B -b rounds/c07.blend -P scripts/cand_cp012_bay_20261102.py -- --out $C \
    --cam walk --z0 19 --scaf-dy 14 --deck-face 0 --tag-hand 543.6:-166.2:3.9 \
    --move "KWORKER_007_CP012=544:-166:0:200,KWORKER_064_CP012=559:-168:0:15" \
    --hide KWORKER_005_CP012,KWORKER_006_CP012,KWORKER_062_CP010S \
    --shift "KCART_gate_crates=-30:0,KHORSE_gate_crates=-30:0,KWORKER_032_CARTS=-30:0" \
    --poses "KWORKER_007_CP012=hauling,KWORKER_064_CP012=standing"
fi
# people are pre-built in the blend (people_lib 1850s_workman, explicit poses, dark fustian): --no-people stops re-randomising
$B -b $C --python-expr "import bpy; bpy.context.scene.frame_set(1)" -P scripts/render_views.py -- \
  --cams CP012_bay_start --outdir "$OUT" --res 1280x720 --samples "${1:-48}" --no-people
$B -b $C --python-expr "import bpy; bpy.context.scene.frame_set(96)" -P scripts/render_views.py -- \
  --cams CP012_bay_end --outdir "$OUT" --res 1280x720 --samples "${1:-48}" --no-people
