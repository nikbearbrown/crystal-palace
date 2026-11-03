#!/bin/bash
# CANDIDATE CP032 parkland depth + aerial haze, meadow variation, cut cart ruts (2026-11-03, no verdict; DEPARTURES MV20).
# Rebuilds the sibling candidate blend rounds/candidates/m02_cp032haze.blend from live m02 and renders BEFORE (live m02)
# and AFTER (candidate) CP032_arrival_start and CP032_arrival_end with identical settings (render_shots.py, 1920x1080,
# 24 spp, look exposure, each camera in its own Blender session, as render_cp032_trees.sh), then the departure spot-check
# (CP032_departure_start/_end from live and candidate into $O/dep_*; scratch only). Live m02.blend and renders/m02 are
# never written.   bash scripts/render_cp032_haze.sh [OUTDIR]  (default /workspace/tmp_cp032hz/full)
set -e; cd "$(dirname "$0")/.."; B=/workspace/blender5/blender; O=${1:-/workspace/tmp_cp032hz/full}
$B -b rounds/m02.blend -P scripts/candidate_cp032_haze.py 2>&1 | grep -E "CP032_HAZE_IN|Error|Traceback"
for C in CP032_arrival_start CP032_arrival_end; do
  $B -b rounds/m02.blend -P scripts/render_shots.py -- --out "$O/before" --cams $C --samples 24 --pct 100 2>&1 | grep -E "RENDERED|Error" || true
  $B -b rounds/candidates/m02_cp032haze.blend -P scripts/render_shots.py -- --out "$O/after" --cams $C --samples 24 --pct 100 2>&1 | grep -E "RENDERED|Error" || true
done
for C in CP032_departure_start CP032_departure_end; do
  $B -b rounds/m02.blend -P scripts/render_shots.py -- --out "$O/dep_before" --cams $C --samples 24 --pct 100 2>&1 | grep -E "RENDERED|Error" || true
  $B -b rounds/candidates/m02_cp032haze.blend -P scripts/render_shots.py -- --out "$O/dep_after" --cams $C --samples 24 --pct 100 2>&1 | grep -E "RENDERED|Error" || true
done
python3 scripts/check_cp032_haze.py | grep CP032_HAZE_CHECKS
python3 scripts/make_cp032_haze_pairs.py "$O"
mkdir -p renders/candidates/cp032_haze_20261103 && cp "$O"/after/CP032_arrival_*.png renders/candidates/cp032_haze_20261103/
