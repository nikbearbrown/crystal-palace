#!/bin/bash
# Live CP016_wheels (v3 KEEP 2026-11-02, DEPARTURES CN43 + CN44). Renders ONLY CP016_wheels_start/end, from the CP016_wheels-only blend
# rounds/candidates/c06_cp016wheels_v3.blend (stub axles, 32 mm front cameras, far workmen in dark fustian, raised-arm KWORKER_028 hidden).
# If missing it is rebuilt: c06.blend -> c06_cp016wheels.blend (reframe) -> c06_cp016wheels_v2_noglaziers.blend -> c06_cp016wheels_v3.blend.
# Never render other shots from these blends (they hide the wagon_0 glaziers, their panes and KWORKER_028).
# usage: scripts/render_cp016_wheels.sh [samples=48] [outdir=renders/candidates/cp016_wheels_v3_20261102]
set -e
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
C=rounds/candidates
if [ ! -f $C/c06_cp016wheels_v3.blend ]; then
  [ -f $C/c06_cp016wheels.blend ] || $B -b rounds/c06.blend -P scripts/cand_cp016_wheels_20261102.py
  [ -f $C/c06_cp016wheels_v2_noglaziers.blend ] || $B -b $C/c06_cp016wheels.blend -P scripts/cand_cp016_wheels_v2_20261102.py -- \
    --stub-axles --swap-workers --cam front32 --out $C/c06_cp016wheels_v2_noglaziers.blend
  $B -b $C/c06_cp016wheels_v2_noglaziers.blend -P scripts/cand_cp016_wheels_v3_20261102.py -- \
    --hide KWORKER_028_CP016,KPANE_SLIDING_1 --repose KWORKER_029_CP016,KWORKER_030_CP016
fi
$B -b $C/c06_cp016wheels_v3.blend -P scripts/render_views.py -- --cams CP016_wheels_start,CP016_wheels_end \
  --outdir "${2:-renders/candidates/cp016_wheels_v3_20261102}" --res 1280x720 --samples "${1:-48}"
