#!/usr/bin/env bash
# CP015_blinds "canvas" CANDIDATE 2026-11-09 (DEPARTURES CN52; no verdict, NOT live). Builds rounds/candidates/c04_cp015canvas.blend
# from the LIVE CP015 source rounds/c04.blend (md5 7810ed1f..., never written) via scripts/cand_cp015_canvas_20261109.py, then renders
# CP015_blinds_start before (live c04, look exposure -0.85) and after (candidate, frame 36, exposure -1.73 re-matched to the
# before mean luma ~84.9) at 1280x720, 48 spp, --no-people (no figures in this frame).
#   scripts/render_cp015_canvas.sh [samples=48] [outdir=renders/candidates/cp015_canvas_20261109]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; S=${1:-48}; R=${2:-renders/candidates/cp015_canvas_20261109}
EB=${EXP_BEFORE:--0.85}; EA=${EXP_AFTER:--1.73}
"$B" -b rounds/c04.blend -P scripts/cand_cp015_canvas_20261109.py -- --out rounds/candidates/c04_cp015canvas.blend 2>&1 | grep -E "CANVAS|LOUVRE|FRAME|SAVED|Error|Traceback"
"$B" -b rounds/c04.blend -P scripts/render_views.py -- --cams CP015_blinds_start --outdir "$R/before" --res 1280x720 --samples "$S" --no-people --exposure "$EB" 2>&1 | grep -E "WROTE|Error" || true
"$B" -b rounds/candidates/c04_cp015canvas.blend -P scripts/render_views.py -- --cams CP015_blinds_start --outdir "$R/after" --res 1280x720 --samples "$S" --no-people --exposure "$EA" 2>&1 | grep -E "WROTE|Error" || true
