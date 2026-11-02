#!/bin/bash
# CANDIDATE CP032 departure hands (2026-11-02, no verdict). Rebuilds the sibling candidate blend from live m02 and
# renders BEFORE (live m02) and AFTER (candidate) CP032_departure_start with identical settings (1920x1080, 24 spp,
# look exposure via render_shots.py). Live m02.blend and renders/m02 are never written.
#   bash scripts/render_cp032_people.sh [OUTDIR]   (default /workspace/tmp_cp032)
set -e; cd "$(dirname "$0")/.."; B=/workspace/blender5/blender; O=${1:-/workspace/tmp_cp032}
$B -b rounds/m02.blend -P scripts/candidate_cp032_people.py 2>&1 | grep -E "CP032 saved|Error|Traceback"
$B -b rounds/m02.blend -P scripts/render_shots.py -- --out "$O/before" --cams CP032_departure_start --samples 24 --pct 100 2>&1 | grep -E "PEOPLE|RENDERED|Error"
$B -b rounds/candidates/m02_cp032people.blend -P scripts/render_shots.py -- --out "$O/after" --cams CP032_departure_start --samples 24 --pct 100 2>&1 | grep -E "PEOPLE|RENDERED|Error"
python3 scripts/make_cp032_people_pairs.py "$O"
