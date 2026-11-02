#!/bin/bash
# Live CP016_wheels (KEEP 2026-11-02, DEPARTURES CN43). Renders ONLY CP016_wheels_start/end, from the CP016_wheels-only blend
# rounds/candidates/c06_cp016wheels.blend (rebuilt from rounds/c06.blend by scripts/cand_cp016_wheels_20261102.py if missing).
# Never render other shots from that blend (it hides the wagon_0 glaziers and their panes).
# usage: scripts/render_cp016_wheels.sh [samples=48]
set -e
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
[ -f rounds/candidates/c06_cp016wheels.blend ] || $B -b rounds/c06.blend -P scripts/cand_cp016_wheels_20261102.py
$B -b rounds/candidates/c06_cp016wheels.blend -P scripts/render_views.py -- --cams CP016_wheels_start,CP016_wheels_end \
  --outdir renders/candidates/cp016_wheels_20261102 --res 1280x720 --samples "${1:-48}"
