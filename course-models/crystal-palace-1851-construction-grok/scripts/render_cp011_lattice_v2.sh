#!/usr/bin/env bash
# CP011 lattice v2 CANDIDATE 2026-11-03 (DEPARTURES CN49). Verdict 2026-11-03: one-tier KEEP (live, see
# render_cp011_yard_live.sh / render_cp011_lattice_live.sh); 2-tier REJECTED (reads as a wall). v1 (CN48) REJECTED: floating smoke + dark.
# Builds two sibling candidates from the PRE-lattice live c07 pinned at construction commit 2bdb3ea (live rounds/c07.blend
# carries the one-tier lattice since the KEEP; never written here) via scripts/cand_cp011_lattice_v2_20261103.py:
#   rounds/candidates/c07_cp011lattice_v2.blend        --tiers 1 (recommended: one tier, ~3.5 ft stockpile)
#   rounds/candidates/c07_cp011lattice_v2_2tier.blend  --tiers 2 (CN48 two-tier ~7 ft rows, for comparison)
# No new smoke: the live CN47 chimney smoke is untouched. Renders CP011_yard_start/_end at the live settings
# (1280x720, 48 spp, --no-people, one session per camera) with exposure re-matched to the live KEEP mean luma
# (start 123.8, end 110.7): 1-tier 0.97 / 1.00, 2-tier 1.08 / 1.30 (live was 0.95 / 1.06).
#   scripts/render_cp011_lattice_v2.sh [samples=48] [outroot]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
S=${1:-48}; R=${2:-renders/candidates/cp011_lattice_v2_20261103}
TMP=$(mktemp -d); git show 2bdb3ea:course-models/crystal-palace-1851-construction-grok/rounds/c07.blend > "$TMP/c07.blend"
"$B" -b "$TMP/c07.blend" -P scripts/cand_cp011_lattice_v2_20261103.py -- --tiers 1 --out rounds/candidates/c07_cp011lattice_v2.blend 2>&1 | grep -E "GIRDERS|SAVED|Error|Traceback"
"$B" -b "$TMP/c07.blend" -P scripts/cand_cp011_lattice_v2_20261103.py -- --tiers 2 --out rounds/candidates/c07_cp011lattice_v2_2tier.blend 2>&1 | grep -E "GIRDERS|SAVED|Error|Traceback"
for J in c07_cp011lattice_v2:after:CP011_yard_start:0.97 c07_cp011lattice_v2:after:CP011_yard_end:1.00 \
         c07_cp011lattice_v2_2tier:after_2tier:CP011_yard_start:1.08 c07_cp011lattice_v2_2tier:after_2tier:CP011_yard_end:1.30; do
  IFS=: read -r BL SUB CAM E <<<"$J"
  "$B" -b "rounds/candidates/$BL.blend" -P scripts/render_views.py -- --cams "$CAM" --outdir "$R/$SUB" --res 1280x720 \
    --samples "$S" --no-people --exposure "$E" 2>&1 | grep -E "WROTE|Error" || true
done
rm -rf "$TMP"
