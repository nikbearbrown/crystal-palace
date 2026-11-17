#!/usr/bin/env bash
# CP036 Railway Colonnade KEEP (2026-11-17, D-SY-CP036-01..12): live hero recipe for CAM_CP036_covered_way_28mm ONLY.
# Round = rounds/sydenham-open54-r15_cp036colonnade.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-open54-r14_cp036colonnade.blend, md5 6b7e98a9).
# Recipe = the verified live CP036 hero recipe (scripts/render_cp036_candidate.sh live pair): survey look v1.1
#   /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP036 --era 1851 --tod interior_daylit --spp 24 --res 1280x720 --no-people
#   ('era 1851' is the survey look's Victorian preset name, not Hyde Park content).
#   scripts/render_cp036_colonnade_live.sh [--rebuild] [outdir=renders/r15_cp036colonnade]
# --rebuild regenerates the round from open54-r14 (md5-checked) into a TEMP blend and renders from that (open54-r15_cp036colonnade never overwritten).
# Every other open54-r14 camera keeps its current live round (side effects NOT promoted).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
ROUND=rounds/sydenham-open54-r15_cp036colonnade.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-open54-r14.blend | cut -c1-8) == 104ee46d ]] || { echo "open54-r14 md5 mismatch (expected 104ee46d)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  env -u CP036_NOSAVE "$B" -b rounds/sydenham-open54-r14.blend -P scripts/candidate_cp036_colonnade.py -- "$TMP/sydenham-open54-r15_cp036colonnade.blend" 2>&1 | grep -E "CP036 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-open54-r15_cp036colonnade.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-open54-r15_cp036colonnade.blend"
fi
OUT=${1:-renders/r15_cp036colonnade}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY54_railway_colonnade_avenue__1854_1856"); print("CP036_COLONNADE_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP036_COLONNADE_IN_PLACE" || true)
echo "$CHK"; grep -q "CP036_COLONNADE_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP036 colonnade KEEP"; exit 3; }
for CAM in CAM_CP036_covered_way_28mm; do
  "$B" -b "$ROUND" -P "$LOOK" -- --cam "$CAM" --out "$OUT/r15_open54colonnade_$CAM.png" --scene-id CP036 --era 1851 --tod interior_daylit --spp 24 --res 1280x720 --no-people 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true
done
echo "done: $OUT/r15_open54colonnade_CAM_CP036_covered_way_28mm.png"
