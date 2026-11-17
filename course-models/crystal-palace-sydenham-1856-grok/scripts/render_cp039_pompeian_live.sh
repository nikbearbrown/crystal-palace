#!/usr/bin/env bash
# CP039 Pompeian Court peristyle KEEP (2026-11-17, D-SY-CP039-01..13): live hero recipe for CAM_CP039_pompeian_peristyle_28mm ONLY.
# Round = rounds/sydenham-1856-r13_cp039pompeian.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-1856-r13_cp039pompeian.blend, md5 49e02048).
# Recipe = the verified r13 finals live recipe (scripts/render_cp039_candidate.sh live pair; /workspace/syd_scratch/r13/render_r13.sh):
#   scripts/render.py, RES=1280x720, 100 %, 32 spp, no PEOPLE_ERA / KEEP_LIGHTING / EXPO (look v1.1 not used for CP039).
#   scripts/render_cp039_pompeian_live.sh [--rebuild] [outdir=renders/r13_cp039pompeian]
# --rebuild regenerates the round from 1856-r13 (md5-checked) into a TEMP blend and renders from that (1856-r13_cp039pompeian never overwritten).
# Every other camera keeps its current live round (side effects NOT promoted: CAM_CP039_pompeian_atrium_28mm 9.5 % px,
#   CAM_CP039_pompeian_wall_50mm, CAM_CP042_cascade_50mm, CAM_compare_0007, CAM_ext_elevated_overview).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/sydenham-1856-r13_cp039pompeian.blend; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-1856-r13.blend | cut -c1-8) == 74dc7aa3 ]] || { echo "1856-r13 md5 mismatch (expected 74dc7aa3)"; exit 3; }
  env -u CP039_NOSAVE "$B" -b rounds/sydenham-1856-r13.blend -P scripts/candidate_cp039_pompeian.py -- "$TMP/sydenham-1856-r13_cp039pompeian.blend" 2>&1 | grep -E "CP039 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-1856-r13_cp039pompeian.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1856-r13_cp039pompeian.blend"
fi
OUT=${1:-renders/r13_cp039pompeian}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY54_pompeian_peristyle_painted__1854_1856"); print("CP039_POMPEIAN_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP039_POMPEIAN_IN_PLACE" || true)
echo "$CHK"; grep -q "CP039_POMPEIAN_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP039 Pompeian KEEP"; exit 3; }
for CAM in CAM_CP039_pompeian_peristyle_28mm; do
  env -u PEOPLE_ERA -u KEEP_LIGHTING -u EXPO -u NO_PEOPLE RES=1280x720 THREADS=8 "$B" -b "$ROUND" -P scripts/render.py -- "$TMP/r" r 100 32 "$CAM" 2>&1 | grep -E "Error|Traceback|Saved" || true
  mv "$TMP/r/r_$CAM.png" "$OUT/r13_1856pompeian_$CAM.png"
done
echo "done: $OUT/r13_1856pompeian_CAM_CP039_pompeian_peristyle_28mm.png"
