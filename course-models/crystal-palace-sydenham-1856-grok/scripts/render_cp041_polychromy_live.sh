#!/usr/bin/env bash
# CP041 Alhambra Court, Owen Jones painted-stucco polychromy (blue/red/gold sebka diaper, three inscription-style bands) and
#   stilted imposts carrying the arcades onto the capitals, 1854-1856 KEEP (2026-11-18, D-SY-CP041-01..08): live hero recipe for
#   CAM_CP041_insert_spandrel_50mm ONLY.
# Round = rounds/sydenham-1856-r08b_cp041polychromy.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-1856-r08b_cp041polychromy.blend, md5 f2460070; candidate commit 59d0a9e).
# Recipe = the verified live CP041 hero recipe (r08bfinal; survey look v1.1 pass reverted): scripts/render.py -- <dir> <tag> 100 48 <cam>
#   (the blend's own 1920x1080, Filmic -1.0 EV, 48 spp, no people; RES/EXPO/KEEP_LIGHTING/NO_PEOPLE/PEOPLE_ERA/THREADS unset).
#   scripts/render_cp041_polychromy_live.sh [--rebuild] [outdir=renders/r08b_cp041polychromy]
# --rebuild regenerates the round from rounds/sydenham-1856-r08b.blend AS COMMITTED IN 702eddf (md5 60c76d85, extracted from git
#   to a TEMP dir) into a TEMP blend and renders from that (r08b_cp041polychromy never overwritten).
# Every other camera keeps its current live round (side effects NOT promoted: CAM_CP041_alhambra_hold_28mm,
#   CAM_CP041_alhambra_entry_28mm, CAM_compare_0108_alhambra, CAM_section_cut_x-300 stay on their current live rounds).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
REL=course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-1856-r08b.blend
ROUND=rounds/sydenham-1856-r08b_cp041polychromy.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  git show 702eddf:$REL > "$TMP/1856-r08b_702eddf.blend"
  [[ $(md5sum < "$TMP/1856-r08b_702eddf.blend" | cut -c1-8) == 60c76d85 ]] || { echo "1856-r08b@702eddf md5 mismatch (expected 60c76d85)"; exit 3; }
  env -u CP041_NOSAVE "$B" -b "$TMP/1856-r08b_702eddf.blend" -P scripts/candidate_cp041_polychromy.py -- "$TMP/sydenham-1856-r08b_cp041polychromy.blend" 2>&1 | grep -E "CP041 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-1856-r08b_cp041polychromy.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1856-r08b_cp041polychromy.blend"
fi
OUT=${1:-renders/r08b_cp041polychromy}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY54_alhambra_court_OJ_polychromy_stilts__1854_1856"); print("CP041_POLYCHROMY_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP041_POLYCHROMY_IN_PLACE" || true)
echo "$CHK"; grep -q "CP041_POLYCHROMY_IN_PLACE True 2" <<<"$CHK" || { echo "$ROUND does not carry the CP041 polychromy KEEP"; exit 3; }
for CAM in CAM_CP041_insert_spandrel_50mm; do
  ( unset RES EXPO KEEP_LIGHTING NO_PEOPLE PEOPLE_ERA PEOPLE_SEED THREADS
    "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r08b_1856polychromy 100 48 "$CAM" 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true )
done
echo "done: $OUT/r08b_1856polychromy_CAM_CP041_insert_spandrel_50mm.png"
