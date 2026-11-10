#!/usr/bin/env bash
# CP010_foundations "setting out + gravel" CANDIDATE 2026-11-10 (DEPARTURES CN53; no verdict, NOT live). Builds
# rounds/candidates/c06_cp010found.blend from the LIVE CP010 source rounds/c06.blend (md5 e461f024..., never written) via
# scripts/cand_cp010_found_20261110.py, then renders CP010_foundations_start/_end at 1280x720, 48 spp:
#   before = live c06, live pipeline (look v1.1 exterior_midday -0.85, people_lib swap on)
#   after  = candidate, --no-people (figures pre-swapped in the script), per-shot exposure re-matched to the before mean luma
#   scripts/render_cp010_found.sh [samples=48] [outdir=renders/candidates/cp010_found_20261110]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; S=${1:-48}; R=${2:-renders/candidates/cp010_found_20261110}
EB=${EXP_BEFORE:--0.85}; EAS=${EXP_AFTER_START:--0.42}; EAE=${EXP_AFTER_END:--0.31}
"$B" -b rounds/c06.blend -P scripts/cand_cp010_found_20261110.py -- --out rounds/candidates/c06_cp010found.blend 2>&1 | grep -E "CAND|PERSON|PEOPLE|SAVED|Error|Traceback"
"$B" -b rounds/c06.blend -P scripts/render_views.py -- --cams CP010_foundations_start,CP010_foundations_end --outdir "$R/before" --res 1280x720 --samples "$S" --exposure "$EB" 2>&1 | grep -E "WROTE|PEOPLE|Error" || true
"$B" -b rounds/candidates/c06_cp010found.blend -P scripts/render_views.py -- --cams CP010_foundations_start --outdir "$R/after" --res 1280x720 --samples "$S" --no-people --exposure "$EAS" 2>&1 | grep -E "WROTE|Error" || true
"$B" -b rounds/candidates/c06_cp010found.blend -P scripts/render_views.py -- --cams CP010_foundations_end --outdir "$R/after" --res 1280x720 --samples "$S" --no-people --exposure "$EAE" 2>&1 | grep -E "WROTE|Error" || true
