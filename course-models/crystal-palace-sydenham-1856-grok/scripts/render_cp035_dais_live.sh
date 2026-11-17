#!/usr/bin/env bash
# SYDENHAM r17 OPEN54 LIVE hero: CP035 transept_gallery 28mm ONLY, from rounds/sydenham-open54-r17_cp035dais.blend =
# CP035 royal dais KEEP (2026-11-17, parent viewed the pairs; DEPARTURES D-SY-CP035-01..13).
# open54-r17_cp035dais (md5 09cd4606...) is a byte copy of the approved candidate rounds/candidates/sydenham-open54-r16_cp035dais.blend,
# i.e. scripts/install_cp035_royal_dais.py applied to live rounds/sydenham-open54-r16.blend (md5 683b1bc9..., pinned by tag
# pre_cp035dais_keep). open54-r16 is NOT changed; the candidate's side effects on the other open54-r16 cameras were NOT promoted
# (CAM_CP035_dais_50mm REJECTED: the dais is hidden behind close figures; procession_nave, CP040 greek_roman_fronts /
# mediaeval_front, CP038 egyptian_hold etc. REJECTED / NOTE) and stay on their current live rounds.
# Only CAM_CP035_transept_gallery_28mm renders from open54-r17_cp035dais (manifest: scripts/sydenham_live_heroes.json).
# Recipe = the r16 'lean hero' recipe = the approved candidate after_28spp recipe (scripts/render_cp035_candidate.sh):
#   render.py, NO_PEOPLE=1, KEEP_LIGHTING=1 (blend exposure Filmic -1.0 EV), 1280x720, 28 spp, one camera per Blender session.
#   scripts/render_cp035_dais_live.sh [--rebuild] [outdir=renders/r17_cp035dais]
# --rebuild regenerates the round from open54-r16 (md5-checked) into a TEMP blend and renders from that (open54-r17_cp035dais never overwritten).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/sydenham-open54-r17_cp035dais.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-open54-r16.blend | cut -c1-8) == 683b1bc9 ]] || { echo "open54-r16 md5 mismatch (expected 683b1bc9)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  env -u CP035_NOSAVE "$B" -b rounds/sydenham-open54-r16.blend -P scripts/install_cp035_royal_dais.py -- "$TMP/sydenham-open54-r17_cp035dais.blend" 2>&1 | grep -E "CP035 (SAVED|BUILT)|Error|Traceback" || true
  [[ -f "$TMP/sydenham-open54-r17_cp035dais.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-open54-r17_cp035dais.blend"
fi
OUT=${1:-renders/r17_cp035dais}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY54_royal_dais__10Jun1854"); print("CP035_DAIS_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP035_DAIS_IN_PLACE" || true)
echo "$CHK"; grep -q "CP035_DAIS_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP035 dais KEEP"; exit 3; }
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=${THREADS:-8}
for CAM in CAM_CP035_transept_gallery_28mm; do
  "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r17_open54dais 100 28 "$CAM" 2>&1 | grep -E "KEEP_LIGHTING|PEOPLE_ADOPT|RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r17_open54dais_CAM_CP035_transept_gallery_28mm.png"
