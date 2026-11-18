#!/usr/bin/env bash
# CP040 English Mediaeval Court KEEP (2026-11-18, D-SY-CP040-01..12): Rochester doorway coloured, niches and canopies round the walls,
#   upper-tier statues beneath canopies, Queen Eleanor + Black Prince monuments, 1854-1856.
# Live hero recipe for CAM_CP040_mediaeval_court_28mm ONLY.
# Round = rounds/sydenham-1856-r14_cp040mediaeval.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-1856-r14_cp040mediaeval.blend, md5 b4121c1a; candidate commit 1f4fd56).
# Recipe = the verified live CP040 hero recipe (scripts/render_cp040_candidate.sh live pair): survey look v1.1
#   /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP040 --era 1851 --tod interior_daylit --spp 24 --res 1280x720 --no-people
#   scripts/render_cp040_mediaeval_live.sh [--rebuild] [outdir=renders/r14_cp040mediaeval]
# --rebuild regenerates the round from rounds/sydenham-1856-r14.blend (md5 00df0959, unchanged) into a TEMP blend and renders
#   from that (r14_cp040mediaeval never overwritten).
# Every other camera keeps its current live round (side effects NOT promoted: CAM_CP040_rochester_door_50mm,
#   CAM_CP040_mediaeval_front_28mm, CAM_compare_0108_alhambra and the other r14 views).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
BASE=rounds/sydenham-1856-r14.blend
ROUND=rounds/sydenham-1856-r14_cp040mediaeval.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < "$BASE" | cut -c1-8) == 00df0959 ]] || { echo "r14 md5 mismatch (expected 00df0959)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  env -u CP040_NOSAVE "$B" -b "$BASE" -P scripts/candidate_cp040_mediaeval.py -- "$TMP/sydenham-1856-r14_cp040mediaeval.blend" 2>&1 | grep -E "CP040 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-1856-r14_cp040mediaeval.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1856-r14_cp040mediaeval.blend"
fi
OUT=${1:-renders/r14_cp040mediaeval}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY54_english_mediaeval_court_dressed__1854_1856"); print("CP040_MEDIAEVAL_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP040_MEDIAEVAL_IN_PLACE" || true)
echo "$CHK"; grep -q "CP040_MEDIAEVAL_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP040 mediaeval KEEP"; exit 3; }
for CAM in CAM_CP040_mediaeval_court_28mm; do
  "$B" -b "$ROUND" -P "$LOOK" -- --cam "$CAM" --out "$OUT/r14_1856mediaeval_$CAM.png" --scene-id CP040 --era 1851 --tod interior_daylit --spp 24 --res 1280x720 --no-people 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true
done
echo "done: $OUT/r14_1856mediaeval_CAM_CP040_mediaeval_court_28mm.png"
