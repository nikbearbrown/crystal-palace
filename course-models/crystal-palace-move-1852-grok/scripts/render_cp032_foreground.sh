#!/bin/bash
# CANDIDATE CP032 arrival near-foreground ground (2026-11-02, no verdict; DEPARTURES MV17). Rebuilds the sibling
# candidate blend rounds/candidates/m02_cp032fg.blend from live m02 and renders BEFORE (live m02) and AFTER
# (candidate) CP032_arrival_start and CP032_arrival_end with identical settings (render_shots.py, 1920x1080, 24 spp,
# look exposure, each camera in its own Blender session, as render_cp032_arrival_live.sh). Live m02.blend and
# renders/m02 are never written.   bash scripts/render_cp032_foreground.sh [OUTDIR]  (default /workspace/tmp_cp032fg/full)
set -e; cd "$(dirname "$0")/.."; B=/workspace/blender5/blender; O=${1:-/workspace/tmp_cp032fg/full}
$B -b rounds/m02.blend -P scripts/candidate_cp032_foreground.py 2>&1 | grep -E "CP032_FG|Error|Traceback"
for C in CP032_arrival_start CP032_arrival_end; do
  $B -b rounds/m02.blend -P scripts/render_shots.py -- --out "$O/before" --cams $C --samples 24 --pct 100 2>&1 | grep -E "RENDERED|Error" || true
  $B -b rounds/candidates/m02_cp032fg.blend -P scripts/render_shots.py -- --out "$O/after" --cams $C --samples 24 --pct 100 2>&1 | grep -E "RENDERED|Error" || true
done
python3 scripts/make_cp032_foreground_pairs.py "$O"
