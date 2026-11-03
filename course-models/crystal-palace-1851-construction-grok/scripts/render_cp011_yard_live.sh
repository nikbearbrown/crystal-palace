#!/usr/bin/env bash
# CP011 LIVE renders from rounds/c07.blend. Live CP011 = works yard KEEP (2026-11-03, DEPARTURES CN47) + one-tier girder
# lattice v2 KEEP (2026-11-03, parent viewed the pairs; DEPARTURES CN49; 2-tier v2 and v1 CN48 REJECTED) + near pile /
# timber bay KEEP (2026-11-03, parent viewed the pairs; DEPARTURES CN50).
#   yard    (CN47): brick works + chimneys, cinder yard, column piles on bearers, timber bay, trolley, 9 people_lib figures.
#   lattice (CN49): identical girder24 members on edge, one tier ~3.5 ft (3 rows x 8), bearer extensions, timber-bay
#                   sightline (trolley/haulers/clerk moved) + deal floor; no new smoke (CN47 smoke unchanged).
#   pile    (CN50): 9 in / 12 in x 1.1 in flanges on the 24 girders, as-cast dark iron on CP011 iron stock (object-level),
#                   CN49 deal floor replaced (footprint fix) + deal landing + two sticked Baltic-deal stacks; smoke unchanged.
# Renders ONLY CP011_yard_start / CP011_yard_end with the exact KEEP settings (render_views.py, 1280x720, 48 spp, look v1,
# --no-people because the figures are pre-built, each camera in its own Blender session) -> renders/c07/CP011_yard_{start,end}.png
# (= survey look/pairs_geo/KEEP_CP011_pile_{start,end}_after.png = renders/candidates/cp011_pile_20261103/after/*.png).
#   scripts/render_cp011_yard_live.sh [--rebuild] [samples=48] [outdir=renders/c07]
#   (scripts/render_cp011_lattice_live.sh is the same script.)
# --rebuild regenerates live rounds/c07.blend from the pre-yard live c07 pinned at construction commit f73d09c
# (md5 c6189435...): cand_cp011_yard_20261103.py --live (asserts CP011_YARD_IN_PLACE True), then
# cand_cp011_lattice_v2_20261103.py --live (asserts CP011_LATTICE_IN_PLACE True), then
# cand_cp011_pile_20261103.py --live (asserts CP011_PILE_IN_PLACE True).
# All three builds are camera-scoped (only_cams / hide_cams / cam_mat = CP011_yard, read by render_views.py), so CP014 and every
# other c07 shot render as before. Never render CP011 with render_round.sh (wrong exposure + people swap).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=f73d09c
REL=course-models/crystal-palace-1851-construction-grok/rounds/c07.blend
# Per-shot live exposure (KEEP CN50 pile, re-matched to the CN49 live mean luma 124.0 / 111.1 because the as-cast iron is
# darker; CN49 was 0.97 / 1.00, CN47 alone 0.95 / 1.06).
EXPOSURES="CP011_yard_start:1.09 CP011_yard_end:1.16"
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/c07.blend"
  YD=$("$B" -b "$TMP/c07.blend" -P scripts/cand_cp011_yard_20261103.py -- --live 2>&1 | grep -E "CP011_YARD|Error|Traceback" || true)
  echo "$YD"; grep -q "CP011_YARD_IN_PLACE True" <<<"$YD" || { echo "CP011_YARD_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  LT=$("$B" -b "$TMP/c07.blend" -P scripts/cand_cp011_lattice_v2_20261103.py -- --live 2>&1 | grep -E "GIRDERS|CP011_LATTICE|Error|Traceback" || true)
  echo "$LT"; grep -q "CP011_LATTICE_IN_PLACE True" <<<"$LT" || { echo "CP011_LATTICE_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  PL=$("$B" -b "$TMP/c07.blend" -P scripts/cand_cp011_pile_20261103.py -- --live 2>&1 | grep -E "DEAL|CP011_PILE|Error|Traceback" || true)
  echo "$PL"; grep -q "CP011_PILE_IN_PLACE True" <<<"$PL" || { echo "CP011_PILE_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/c07.blend" rounds/c07.blend
  rm -rf "$TMP"
fi
S=${1:-48}; OUT=${2:-renders/c07}
CHK=$("$B" -b rounds/c07.blend -P scripts/cand_cp011_yard_20261103.py -- --check 2>&1 | grep -E "CP011_YARD_IN_PLACE" || true)
echo "$CHK"; grep -q "CP011_YARD_IN_PLACE True" <<<"$CHK" || { echo "live c07 does not carry the CP011 yard (run with --rebuild)"; exit 3; }
CHK=$("$B" -b rounds/c07.blend -P scripts/cand_cp011_lattice_v2_20261103.py -- --check 2>&1 | grep -E "CP011_LATTICE_IN_PLACE" || true)
echo "$CHK"; grep -q "CP011_LATTICE_IN_PLACE True" <<<"$CHK" || { echo "live c07 does not carry the CP011 lattice (run with --rebuild)"; exit 3; }
CHK=$("$B" -b rounds/c07.blend -P scripts/cand_cp011_pile_20261103.py -- --check 2>&1 | grep -E "CP011_PILE_IN_PLACE" || true)
echo "$CHK"; grep -q "CP011_PILE_IN_PLACE True" <<<"$CHK" || { echo "live c07 does not carry the CP011 pile (run with --rebuild)"; exit 3; }
for CE in $EXPOSURES; do
  "$B" -b rounds/c07.blend -P scripts/render_views.py -- --cams "${CE%%:*}" --outdir "$OUT" --res 1280x720 \
    --samples "$S" --no-people --exposure "${CE##*:}" 2>&1 | grep -E "WROTE|Error" || true
done
echo "done: $OUT/CP011_yard_start.png $OUT/CP011_yard_end.png"
