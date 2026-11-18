#!/usr/bin/env bash
# CP038 Egyptian Court outer court KEEP (2026-11-18, D-SY-CP038-13..23): portico reliefs, winged disc, flagged walk and visitors, 1854-1856.
# Live hero recipe for CAM_CP038_egyptian_hold_28mm ONLY.
# Round = rounds/sydenham-1856-r08_cp038reliefs.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-1856-r08_cp038reliefs.blend, md5 e01ea64c; candidate commit c39838b).
# Recipe = the verified live CP038 hero recipe (scripts/render_cp038_reliefs_candidate.sh live pair): survey look v1.1
#   /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP038 --era 1851 --tod interior_daylit --spp 24 --res 1280x720 --no-people
#   scripts/render_cp038_reliefs_live.sh [--rebuild] [outdir=renders/r08_cp038reliefs]
# --rebuild regenerates the round from rounds/sydenham-1856-r08.blend (md5 0aa6e9ce, unchanged) into a TEMP blend and renders
#   from that (r08_cp038reliefs never overwritten).
# Every other camera keeps its current live round (side effects NOT promoted: CAM_CP038_egyptian_entry_28mm, CAM_CP041_alhambra_*,
#   CAM_plan_overlay_top, CAM_central_transept_straight and the other r08 views).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
BASE=rounds/sydenham-1856-r08.blend
ROUND=rounds/sydenham-1856-r08_cp038reliefs.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < "$BASE" | cut -c1-8) == 0aa6e9ce ]] || { echo "r08 md5 mismatch (expected 0aa6e9ce)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  env -u CP038_NOSAVE "$B" -b "$BASE" -P scripts/candidate_cp038_reliefs.py -- "$TMP/sydenham-1856-r08_cp038reliefs.blend" 2>&1 | grep -E "CP038 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-1856-r08_cp038reliefs.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1856-r08_cp038reliefs.blend"
fi
OUT=${1:-renders/r08_cp038reliefs}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY54_egyptian_outer_court_portico_reliefs__1854_1856"); print("CP038_RELIEFS_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP038_RELIEFS_IN_PLACE" || true)
echo "$CHK"; grep -q "CP038_RELIEFS_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP038 reliefs KEEP"; exit 3; }
for CAM in CAM_CP038_egyptian_hold_28mm; do
  "$B" -b "$ROUND" -P "$LOOK" -- --cam "$CAM" --out "$OUT/r08_1856reliefs_$CAM.png" --scene-id CP038 --era 1851 --tod interior_daylit --spp 24 --res 1280x720 --no-people 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true
done
echo "done: $OUT/r08_1856reliefs_CAM_CP038_egyptian_hold_28mm.png"
