#!/usr/bin/env bash
# CP011 "yard2" CANDIDATE 2026-11-03 (DEPARTURES CN51; KEEP 2026-11-03, now LIVE via --live, see render_cp011_yard_live.sh). Builds rounds/candidates/c07_cp011yard2.blend
# from the PRE-yard2 live c07 pinned at construction commit 49ae701 (CN47 yard + CN49 lattice + CN50 pile, md5 6920b1e9...; live c07 is
# never written) via scripts/cand_cp011_yard2_20261103.py, then renders CP011_yard_start/_end at the live settings
# (render_views.py, 1280x720, 48 spp, --no-people, one session per camera) with exposure re-matched to the live mean luma
# (start 124.0, end 111.0); the shed bounce light lifts the frame, so EXP_START/EXP_END default below live 1.09 / 1.16.
#   scripts/render_cp011_yard2.sh [samples=48] [outdir=renders/candidates/cp011_yard2_20261103/after]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
S=${1:-48}; R=${2:-renders/candidates/cp011_yard2_20261103/after}
ES=${EXP_START:-0.83}; EE=${EXP_END:-0.88}
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
git show 49ae701:course-models/crystal-palace-1851-construction-grok/rounds/c07.blend > "$TMP/c07.blend"
"$B" -b "$TMP/c07.blend" -P scripts/cand_cp011_yard2_20261103.py -- --out rounds/candidates/c07_cp011yard2.blend 2>&1 | grep -E "SMOKE|SAVED|Error|Traceback"
for CE in CP011_yard_start:$ES CP011_yard_end:$EE; do
  "$B" -b rounds/candidates/c07_cp011yard2.blend -P scripts/render_views.py -- --cams "${CE%%:*}" --outdir "$R" --res 1280x720 \
    --samples "$S" --no-people --exposure "${CE##*:}" 2>&1 | grep -E "WROTE|Error" || true
done
