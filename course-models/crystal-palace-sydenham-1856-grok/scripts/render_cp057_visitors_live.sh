#!/usr/bin/env bash
# CP057 lower terrace 'Trying to recover an audience', interwar visitors / summer-dress skirts / hired deck chairs, summer 1936 KEEP
#   (2026-11-18, D-SY-CP057-01..09): live hero recipe for CAM_CP057_1936_lower_terrace_35mm ONLY.
# Round = rounds/sydenham-1936-r11_cp057visitors.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-1936-r11_cp057visitors.blend, md5 c6043c03; candidate commit ab04b59).
# Recipe = the verified live CP057 hero recipe (scripts/render_cp057_candidate.sh live pair): survey look v1.1
#   /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP057 --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people
#   scripts/render_cp057_visitors_live.sh [--rebuild] [outdir=renders/r11_cp057visitors]
# --rebuild regenerates the round from rounds/sydenham-1936-r11.blend AS COMMITTED IN 1b3c92d (md5 40140697, extracted from git
#   to a TEMP dir) into a TEMP blend and renders from that (r11_cp057visitors never overwritten).
# Every other camera keeps its current live round (side effects NOT promoted: CAM_CP073_steps_35mm, CAM_central_transept_straight,
#   CAM_compare_0074, CAM_ext_garden_34_terrace, CAM_ext_elevated_overview, CAM_compare_0007 stay on their current live rounds).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
REL=course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-1936-r11.blend
ROUND=rounds/sydenham-1936-r11_cp057visitors.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  git show 1b3c92d:$REL > "$TMP/1936-r11_1b3c92d.blend"
  [[ $(md5sum < "$TMP/1936-r11_1b3c92d.blend" | cut -c1-8) == 40140697 ]] || { echo "1936-r11@1b3c92d md5 mismatch (expected 40140697)"; exit 3; }
  env -u CP057_NOSAVE "$B" -b "$TMP/1936-r11_1b3c92d.blend" -P scripts/candidate_cp057_visitors.py -- "$TMP/sydenham-1936-r11_cp057visitors.blend" 2>&1 | grep -E "CP057 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-1936-r11_cp057visitors.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1936-r11_cp057visitors.blend"
fi
OUT=${1:-renders/r11_cp057visitors}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY36_lower_terrace_interwar_visitors__summer1936"); print("CP057_VISITORS_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP057_VISITORS_IN_PLACE" || true)
echo "$CHK"; grep -q "CP057_VISITORS_IN_PLACE True 149" <<<"$CHK" || { echo "$ROUND does not carry the CP057 visitors KEEP"; exit 3; }
for CAM in CAM_CP057_1936_lower_terrace_35mm; do
  "$B" -b "$ROUND" -P "$LOOK" -- --cam "$CAM" --out "$OUT/r11_1936visitors_$CAM.png" --scene-id CP057 --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true
done
echo "done: $OUT/r11_1936visitors_CAM_CP057_1936_lower_terrace_35mm.png"
