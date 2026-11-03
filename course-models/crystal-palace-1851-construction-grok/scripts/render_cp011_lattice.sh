#!/usr/bin/env bash
# CP011 lattice CANDIDATE v1 2026-11-03 (DEPARTURES CN48, REJECTED by the parent: floating smoke + 6/9 luma dark; NOT live): builds rounds/candidates/c07_cp011lattice.blend
# from live rounds/c07.blend (CN47 yard, never written) via scripts/cand_cp011_lattice_20261103.py, then renders
# CP011_yard_start / _end with the exact live settings (render_cp011_yard_live.sh: 1280x720, 48 spp, --no-people,
# exposure 0.95 start / 1.06 end, one Blender session per camera) into renders/candidates/cp011_lattice_20261103/after/.
#   scripts/render_cp011_lattice.sh [samples=48] [outdir]
# Since the CN49 one-tier lattice went live (2026-11-03) this historical script reads the pre-lattice live c07 pinned at
# construction commit 2bdb3ea instead of rounds/c07.blend.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
S=${1:-48}; OUT=${2:-renders/candidates/cp011_lattice_20261103/after}
TMP=$(mktemp -d); git show 2bdb3ea:course-models/crystal-palace-1851-construction-grok/rounds/c07.blend > "$TMP/c07.blend"
"$B" -b "$TMP/c07.blend" -P scripts/cand_cp011_lattice_20261103.py -- --out rounds/candidates/c07_cp011lattice.blend 2>&1 | grep -E "SAVED|Error|Traceback"
for CE in CP011_yard_start:0.95 CP011_yard_end:1.06; do
  "$B" -b rounds/candidates/c07_cp011lattice.blend -P scripts/render_views.py -- --cams "${CE%%:*}" --outdir "$OUT" --res 1280x720 \
    --samples "$S" --no-people --exposure "${CE##*:}" 2>&1 | grep -E "WROTE|Error" || true
done
rm -rf "$TMP"
