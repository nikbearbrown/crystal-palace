#!/usr/bin/env bash
# CP011 near pile + timber bay CANDIDATE 2026-11-03 (DEPARTURES CN50; no verdict, NOT live).
# Builds rounds/candidates/c07_cp011pile.blend from live rounds/c07.blend (CN47 yard + CN49 one-tier lattice, md5 8cb193fe...;
# never written) via scripts/cand_cp011_pile_20261103.py, then renders CP011_yard_start/_end at the live settings
# (render_views.py, 1280x720, 48 spp, --no-people, one session per camera) with exposure re-matched to the live mean luma
# (start 124.0, end 111.1): 1.09 start / 1.16 end (live 0.97 / 1.00; the as-cast iron stock is darker).
#   scripts/render_cp011_pile.sh [samples=48] [outdir=renders/candidates/cp011_pile_20261103/after]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
S=${1:-48}; R=${2:-renders/candidates/cp011_pile_20261103/after}
"$B" -b rounds/c07.blend -P scripts/cand_cp011_pile_20261103.py 2>&1 | grep -E "DEAL|SAVED|Error|Traceback"
for CE in CP011_yard_start:1.09 CP011_yard_end:1.16; do
  "$B" -b rounds/candidates/c07_cp011pile.blend -P scripts/render_views.py -- --cams "${CE%%:*}" --outdir "$R" --res 1280x720 \
    --samples "$S" --no-people --exposure "${CE##*:}" 2>&1 | grep -E "WROTE|Error" || true
done
