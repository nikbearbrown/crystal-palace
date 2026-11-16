#!/usr/bin/env bash
# SYDENHAM r19 BUILD53 LIVE hero: CP033 slope_up 35mm ONLY, from rounds/sydenham-build53-r19_cp033slope.blend =
# CP033 slope works KEEP (2026-11-16, parent viewed the pairs; DEPARTURES D-SY-CP033-01..11).
# build53-r19_cp033slope (md5 ebb75f70...) is a byte copy of the approved candidate rounds/candidates/sydenham-build53-r18b_cp033slope.blend,
# i.e. scripts/candidate_cp033_slope.py applied to live rounds/sydenham-build53-r18b.blend (md5 dc579904..., pinned by tag
# pre_cp033slope_keep). build53-r18b is NOT changed; the candidate's 32 side-effect cameras in that round (CP033 terrace_cut/
# frame_rising/transept_ribs, compare_0007, ext_elevated_overview ground wedge, CP038 figure swap, etc.) were NOT promoted
# (REJECTED / NOTE) and stay on their current live rounds.
# Only CAM_CP033_slope_up_35mm renders from build53-r19_cp033slope (manifest: scripts/sydenham_live_heroes.json).
# Recipe = the approved candidate "after" recipe (scripts/render_cp033_candidate.sh = the live CP033 hero recipe):
#   render.py, NO_PEOPLE=1, KEEP_LIGHTING=1 (blend exposure Filmic -1.0 EV), 1280x720, 48 spp, one camera per Blender session.
#   scripts/render_cp033_slope_live.sh [--rebuild] [outdir=renders/r19_cp033slope]
# --rebuild regenerates the round from build53-r18b (md5-checked) into a TEMP blend and renders from that (build53-r19_cp033slope never overwritten).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/sydenham-build53-r19_cp033slope.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-build53-r18b.blend | cut -c1-8) == dc579904 ]] || { echo "build53-r18b md5 mismatch (expected dc579904)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  env -u CP033_NOSAVE "$B" -b rounds/sydenham-build53-r18b.blend -P scripts/candidate_cp033_slope.py -- "$TMP/sydenham-build53-r19_cp033slope.blend" 2>&1 | grep -E "CP033 (SAVED|BUILT)|Error|Traceback" || true
  [[ -f "$TMP/sydenham-build53-r19_cp033slope.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-build53-r19_cp033slope.blend"
fi
OUT=${1:-renders/r19_cp033slope}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY53_slope_works__autumn1853"); print("CP033_SLOPE_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP033_SLOPE_IN_PLACE" || true)
echo "$CHK"; grep -q "CP033_SLOPE_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP033 slope KEEP"; exit 3; }
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
for CAM in CAM_CP033_slope_up_35mm; do
  "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r19_build53slope 100 48 "$CAM" 2>&1 | grep -E "KEEP_LIGHTING|PEOPLE_ADOPT|RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r19_build53slope_CAM_CP033_slope_up_35mm.png"
