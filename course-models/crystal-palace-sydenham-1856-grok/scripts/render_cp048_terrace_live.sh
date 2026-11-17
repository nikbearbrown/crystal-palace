#!/usr/bin/env bash
# CP048 upper-terrace north walk / ribbon bedding / visitors c. summer 1868 KEEP (2026-11-17, D-SY-CP048-01..12): live hero recipe for CAM_CP048_terrace_hold_35mm ONLY.
# Round = rounds/sydenham-post66-r10_cp048terrace.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-post66-r10_cp048terrace.blend, md5 16f1f73d; candidate commit 5f2fb71).
# Recipe = the verified live CP048 hero recipe (scripts/render_cp048_candidate.sh live pair): survey look v1.1
#   /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP048 --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people
#   scripts/render_cp048_terrace_live.sh [--rebuild] [outdir=renders/r10_cp048terrace]
# --rebuild regenerates the round from rounds/sydenham-post66-r10.blend AS COMMITTED IN 972145e (md5 ed31acf2, extracted from git
#   to a TEMP dir; the working-tree post66-r10 is a later S67b re-save and is not used) into a TEMP blend and renders from that
#   (post66-r10_cp048terrace never overwritten).
# Every other camera keeps its current live round (side effects NOT promoted: CAM_CP048_terrace_walk_35mm, CAM_CP047_north_end_35mm,
#   CAM_ext_elevated_overview (lopsided, north half only: REJECTED), CAM_ext_garden_34_terrace).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LOOK=/workspace/crystal-palace-survey/look/apply_render.py
REL=course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-post66-r10.blend
ROUND=rounds/sydenham-post66-r10_cp048terrace.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  git show 972145e:$REL > "$TMP/post66-r10_972145e.blend"
  [[ $(md5sum < "$TMP/post66-r10_972145e.blend" | cut -c1-8) == ed31acf2 ]] || { echo "post66-r10@972145e md5 mismatch (expected ed31acf2)"; exit 3; }
  env -u CP048_NOSAVE "$B" -b "$TMP/post66-r10_972145e.blend" -P scripts/candidate_cp048_terrace.py -- "$TMP/sydenham-post66-r10_cp048terrace.blend" 2>&1 | grep -E "CP048 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-post66-r10_cp048terrace.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-post66-r10_cp048terrace.blend"
fi
OUT=${1:-renders/r10_cp048terrace}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY68_upper_terrace_north_walk_bedding_visitors__summer1868"); print("CP048_TERRACE_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP048_TERRACE_IN_PLACE" || true)
echo "$CHK"; grep -q "CP048_TERRACE_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP048 terrace KEEP"; exit 3; }
for CAM in CAM_CP048_terrace_hold_35mm; do
  "$B" -b "$ROUND" -P "$LOOK" -- --cam "$CAM" --out "$OUT/r10_post66terrace_$CAM.png" --scene-id CP048 --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true
done
echo "done: $OUT/r10_post66terrace_CAM_CP048_terrace_hold_35mm.png"
