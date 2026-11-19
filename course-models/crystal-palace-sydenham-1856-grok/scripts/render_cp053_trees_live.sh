#!/usr/bin/env bash
# CP053 'The company fails': Festival of Empire grounds, summer 1911 - lower-park trees in leaf KEEP (2026-11-19, D-SY-CP053-01..07):
#   live hero recipe for CAM_CP053_empire_pavilions_wide_35mm ONLY.
# Round = rounds/sydenham-late11-r14_cp053trees.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-late11-r14_cp053trees.blend, md5 dba3f65b; candidate commit 29c6694).
# Recipe = the verified live CP053 hero recipe (survey look v1.1): /workspace/crystal-palace-survey/look/apply_render.py
#   --scene-id CP053 --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people (look/sydenham_logs/CP053.log).
#   scripts/render_cp053_trees_live.sh [--rebuild] [outdir=renders/r14_cp053trees]
# --rebuild regenerates the round from rounds/sydenham-late11-r14.blend AS COMMITTED IN 1c96ad7 (md5 9f90df23, extracted from git
#   to a TEMP dir) into a TEMP blend and renders from that (r14_cp053trees never overwritten).
# Every other camera keeps its current live round (side effects NOT promoted: CAM_CP001_prologue_distant_35mm,
#   CAM_CP053_festival_of_empire_35mm, CAM_CP060_crowd_watching_35mm, CAM_CP062_morning_between_towers_35mm, CAM_CP064_skyline_50mm,
#   CAM_compare_0007, CAM_compare_0108_alhambra, CAM_ext_elevated_overview stay on their current live rounds).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; LOOK=/workspace/crystal-palace-survey/look/apply_render.py
REL=course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-late11-r14.blend
ROUND=rounds/sydenham-late11-r14_cp053trees.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  git show 1c96ad7:$REL > "$TMP/late11-r14_1c96ad7.blend"
  [[ $(md5sum < "$TMP/late11-r14_1c96ad7.blend" | cut -c1-8) == 9f90df23 ]] || { echo "late11-r14@1c96ad7 md5 mismatch (expected 9f90df23)"; exit 3; }
  env -u CP053_NOSAVE -u CP053_DENSITY "$B" -b "$TMP/late11-r14_1c96ad7.blend" -P scripts/candidate_cp053_trees_in_leaf.py -- "$TMP/sydenham-late11-r14_cp053trees.blend" 2>&1 | grep -E "CP053 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-late11-r14_cp053trees.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-late11-r14_cp053trees.blend"
fi
OUT=${1:-renders/r14_cp053trees}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY11_lower_park_trees_in_leaf__summer1911"); print("CP053_TREES_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP053_TREES_IN_PLACE" || true)
echo "$CHK"; grep -q "CP053_TREES_IN_PLACE True 2" <<<"$CHK" || { echo "$ROUND does not carry the CP053 trees KEEP"; exit 3; }
for CAM in CAM_CP053_empire_pavilions_wide_35mm; do
  "$B" -b "$ROUND" -P "$LOOK" -- --cam "$CAM" --out "$OUT/r14_late11trees_$CAM.png" --scene-id CP053 --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true
done
echo "done: $OUT/r14_late11trees_CAM_CP053_empire_pavilions_wide_35mm.png"
