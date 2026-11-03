#!/usr/bin/env bash
# CP011 lattice CANDIDATE 2026-11-03 (DEPARTURES CN48, no verdict, NOT live): builds rounds/candidates/c07_cp011lattice.blend
# from live rounds/c07.blend (CN47 yard, never written) via scripts/cand_cp011_lattice_20261103.py, then renders
# CP011_yard_start / _end with the exact live settings (render_cp011_yard_live.sh: 1280x720, 48 spp, --no-people,
# exposure 0.95 start / 1.06 end, one Blender session per camera) into renders/candidates/cp011_lattice_20261103/after/.
#   scripts/render_cp011_lattice.sh [samples=48] [outdir]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
S=${1:-48}; OUT=${2:-renders/candidates/cp011_lattice_20261103/after}
"$B" -b rounds/c07.blend -P scripts/cand_cp011_lattice_20261103.py 2>&1 | grep -E "SAVED|Error|Traceback"
for CE in CP011_yard_start:0.95 CP011_yard_end:1.06; do
  "$B" -b rounds/candidates/c07_cp011lattice.blend -P scripts/render_views.py -- --cams "${CE%%:*}" --outdir "$OUT" --res 1280x720 \
    --samples "$S" --no-people --exposure "${CE##*:}" 2>&1 | grep -E "WROTE|Error" || true
done
