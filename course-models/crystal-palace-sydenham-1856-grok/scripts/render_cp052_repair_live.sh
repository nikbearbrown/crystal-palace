#!/usr/bin/env bash
# CP052 'Repair never finishes', glaziers' pole scaffold / painters' cradle + ladder / weathered west bays on the transept front, c. 1900 KEEP
#   (2026-11-18, D-SY-CP052-01..09): live hero recipe for CAM_CP052_scaffold_reglaze_35mm ONLY.
# Round = rounds/sydenham-late11-r16_cp052repair.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-late11-r16_cp052repair.blend, md5 5aadfd45; candidate commit e9e6835).
# Recipe = the verified live CP052 hero recipe (survey dud-fix v4 reframe + look v1.1): scripts/render_cp052_look.py
#   (apply_look CP052 = 1852 / exterior_afternoon, 1280x720, 32 spp; camera saved in the blend).
#   scripts/render_cp052_repair_live.sh [--rebuild] [outdir=renders/r16_cp052repair]
# --rebuild regenerates the round from rounds/sydenham-late11-r16.blend AS COMMITTED IN 80f43ba (md5 3ce48caf, extracted from git
#   to a TEMP dir) into a TEMP blend and renders from that (r16_cp052repair never overwritten).
# Every other camera keeps its current live round (side effects NOT promoted: CAM_CP061_transept_collapse_35mm (r16 view),
#   CAM_CP049_worn_garden_front_35mm, CAM_section_cut_x-300, CAM_ext_elevated_overview, CAM_CP053_empire_pavilions_wide_35mm,
#   CAM_CP064_skyline_50mm stay on their current live rounds).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
REL=course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-late11-r16.blend
ROUND=rounds/sydenham-late11-r16_cp052repair.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  git show 80f43ba:$REL > "$TMP/late11-r16_80f43ba.blend"
  [[ $(md5sum < "$TMP/late11-r16_80f43ba.blend" | cut -c1-8) == 3ce48caf ]] || { echo "late11-r16@80f43ba md5 mismatch (expected 3ce48caf)"; exit 3; }
  env -u CP052_NOSAVE "$B" -b "$TMP/late11-r16_80f43ba.blend" -P scripts/candidate_cp052_repair.py -- "$TMP/sydenham-late11-r16_cp052repair.blend" 2>&1 | grep -E "CP052 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-late11-r16_cp052repair.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-late11-r16_cp052repair.blend"
fi
OUT=${1:-renders/r16_cp052repair}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY00_transept_front_glaziers_painters__c1900"); print("CP052_REPAIR_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP052_REPAIR_IN_PLACE" || true)
echo "$CHK"; grep -q "CP052_REPAIR_IN_PLACE True 24" <<<"$CHK" || { echo "$ROUND does not carry the CP052 repair KEEP"; exit 3; }
for CAM in CAM_CP052_scaffold_reglaze_35mm; do
  "$B" -b "$ROUND" -P scripts/render_cp052_look.py -- "$OUT/r16_late11repair_$CAM.png" "$CAM" 32 1280x720 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true
done
echo "done: $OUT/r16_late11repair_CAM_CP052_scaffold_reglaze_35mm.png"
