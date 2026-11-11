#!/usr/bin/env bash
# CP013_sash "Downes roof" CANDIDATE 2026-11-11 (DEPARTURES CN54; no verdict, NOT live). Builds rounds/candidates/c04_cp013sash.blend
# from the LIVE CP013 source rounds/c04.blend (md5 415e5100..., never written) via scripts/cand_cp013_sash_20261111.py, then renders
# CP013_sash_start/_end before (live c04, look exposure -0.85) and after (candidate; exposure re-matched to the before mean luma:
# start -0.78, end -0.95) at 1280x720, 48 spp, default people handling (as the live renders).
#   scripts/render_cp013_sash.sh [samples=48] [outdir=renders/candidates/cp013_sash_20261111]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; S=${1:-48}; R=${2:-renders/candidates/cp013_sash_20261111}
EB=${EXP_BEFORE:--0.85}; ES=${EXP_AFTER_START:--0.78}; EE=${EXP_AFTER_END:--0.95}
# KEEP 2026-11-11: live c04 now IS this candidate (md5 c8d1abc5). To reproduce the candidate, the script must read the pre-KEEP
# live c04 (md5 415e5100, pinned at construction b71f5ce), never the promoted live c04 (that would add a second CP013S_* set).
BASE=$(mktemp --suffix=.blend); trap 'rm -f "$BASE"' EXIT
git show b71f5ce:course-models/crystal-palace-1851-construction-grok/rounds/c04.blend > "$BASE"
"$B" -b "$BASE" -P scripts/cand_cp013_sash_20261111.py -- --out rounds/candidates/c04_cp013sash.blend 2>&1 | grep -E "ROOF|FRONTS|SAVED|Error|Traceback"
"$B" -b "$BASE" -P scripts/render_views.py -- --cams CP013_sash_start,CP013_sash_end --outdir "$R/before" --res 1280x720 --samples "$S" --exposure "$EB" 2>&1 | grep -E "WROTE|Error" || true
"$B" -b rounds/candidates/c04_cp013sash.blend -P scripts/render_views.py -- --cams CP013_sash_start --outdir "$R/after" --res 1280x720 --samples "$S" --exposure "$ES" 2>&1 | grep -E "WROTE|Error" || true
"$B" -b rounds/candidates/c04_cp013sash.blend -P scripts/render_views.py -- --cams CP013_sash_end --outdir "$R/after" --res 1280x720 --samples "$S" --exposure "$EE" 2>&1 | grep -E "WROTE|Error" || true
