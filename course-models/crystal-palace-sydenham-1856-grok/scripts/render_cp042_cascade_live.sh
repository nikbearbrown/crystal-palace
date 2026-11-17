#!/usr/bin/env bash
# CP042 Water Temples / cascades / arcade cataract KEEP (2026-11-17, D-SY-CP042-01..12): live hero recipe for CAM_CP042_cascade_50mm ONLY.
# Round = rounds/sydenham-1856-r13_cp042cascade.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-1856-r13_cp042cascade.blend, md5 51fcecdf).
# Recipe = the verified live CP042 hero recipe (scripts/render_cp042_candidate.sh live pair): survey look v1.1
#   /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP042 --era 1851 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people
#   ('era 1851' is the survey look's Victorian preset name, not Hyde Park content).
#   scripts/render_cp042_cascade_live.sh [--rebuild] [outdir=renders/r13_cp042cascade]
# --rebuild regenerates the round from 1856-r13 (md5-checked) into a TEMP blend and renders from that (1856-r13_cp042cascade never overwritten).
# Every other camera keeps its current live round (side effects REJECTED / NOT promoted: CAM_CP042_great_basins_35mm black,
#   camera inside the new causeway; terrace_overlook, terrace_basin, ext_elevated_overview).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
ROUND=rounds/sydenham-1856-r13_cp042cascade.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-1856-r13.blend | cut -c1-8) == 74dc7aa3 ]] || { echo "1856-r13 md5 mismatch (expected 74dc7aa3)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  env -u CP042_NOSAVE "$B" -b rounds/sydenham-1856-r13.blend -P scripts/candidate_cp042_cascades.py -- "$TMP/sydenham-1856-r13_cp042cascade.blend" 2>&1 | grep -E "CP042 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-1856-r13_cp042cascade.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1856-r13_cp042cascade.blend"
fi
OUT=${1:-renders/r13_cp042cascade}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY56_water_temples_cascades_running__18Jun1856"); print("CP042_CASCADES_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP042_CASCADES_IN_PLACE" || true)
echo "$CHK"; grep -q "CP042_CASCADES_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP042 cascades KEEP"; exit 3; }
for CAM in CAM_CP042_cascade_50mm; do
  "$B" -b "$ROUND" -P "$LOOK" -- --cam "$CAM" --out "$OUT/r13_1856cascade_$CAM.png" --scene-id CP042 --era 1851 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true
done
echo "done: $OUT/r13_1856cascade_CAM_CP042_cascade_50mm.png"
