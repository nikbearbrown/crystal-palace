#!/usr/bin/env bash
# SYDENHAM r18 CLEARANCE LIVE hero: CP063 crane_lift 50mm ONLY, from rounds/sydenham-clearance-r18_cp063.blend =
# CP063 clearance scrap-sorting + hand pull-down KEEP (2026-11-13, parent viewed the pairs; DEPARTURES D-SY-CP063-01..10).
# r18_cp063 (md5 5ec53dd9...) is a byte copy of the approved candidate rounds/candidates/sydenham-clearance-r17_cp063scrap.blend,
# i.e. scripts/candidate_cp063_scrap_clearance.py applied to live rounds/sydenham-clearance-r17.blend (md5 055ef338..., pinned
# by tag pre_cp063scrap_keep). clearance-r17 is NOT changed and still serves CAM_CP063_scrap_gang_35mm,
# CAM_CP063_clearance_perimeter_35mm and CAM_CP063_terrace_edge_35mm (those candidate side effects were REJECTED).
# Only CAM_CP063_crane_lift_50mm renders from r18_cp063 (manifest: scripts/sydenham_live_heroes.json).
# Recipe = the approved candidate "after" recipe (= live CP063 r17q hero recipe raised to 1920x1080 / 48 spp):
#   render.py, NO_PEOPLE=1, blend lighting/exposure, 1920x1080, 48 spp, one camera per Blender session.
#   scripts/render_cp063_scrap_live.sh [--rebuild] [outdir=renders/r18]
# --rebuild regenerates the round from clearance-r17 (md5-checked) into a TEMP blend and renders from that (r18_cp063 never overwritten).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/sydenham-clearance-r18_cp063.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-clearance-r17.blend | cut -c1-8) == 055ef338 ]] || { echo "clearance-r17 md5 mismatch (expected 055ef338)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  "$B" -b rounds/sydenham-clearance-r17.blend -P scripts/candidate_cp063_scrap_clearance.py -- "$TMP/sydenham-clearance-r18_cp063.blend" 2>&1 | grep -E "CP063 SAVED|Error|Traceback" || true
  [[ -f "$TMP/sydenham-clearance-r18_cp063.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-clearance-r18_cp063.blend"
fi
OUT=${1:-renders/r18}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY37_clearance_scrap_sorting_remnant__1937"); print("CP063_SCRAP_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP063_SCRAP_IN_PLACE" || true)
echo "$CHK"; grep -q "CP063_SCRAP_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP063 scrap KEEP"; exit 3; }
export NO_PEOPLE=1 RES=1920x1080 THREADS=8
for CAM in CAM_CP063_crane_lift_50mm; do
  "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r18_clearance 100 48 "$CAM" 2>&1 | grep -E "PEOPLE_ADOPT|RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r18_clearance_CAM_CP063_crane_lift_50mm.png"
