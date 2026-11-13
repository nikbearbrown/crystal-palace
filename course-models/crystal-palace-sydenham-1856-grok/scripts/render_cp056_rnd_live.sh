#!/usr/bin/env bash
# SYDENHAM r18 WAR LIVE hero: CP056 nave_drill_gallery 28mm ONLY, from rounds/sydenham-war-r15_cp056.blend =
# CP056 RND nave drill + screened mess space KEEP (2026-11-13, parent viewed the pairs; DEPARTURES D-SY-CP056-01..09).
# war-r15_cp056 (md5 0a431fc8...) is a byte copy of the approved candidate rounds/candidates/sydenham-war-r14_cp056rnd.blend,
# i.e. scripts/candidate_cp056_rnd_nave_drill.py applied to live rounds/sydenham-war-r14.blend (md5 718c4b3d..., pinned
# by tag pre_cp056rnd_keep). war-r14 is NOT changed and still serves CAM_CP056_terrace_drill_35mm, CAM_CP056_ranks_50mm,
# CAM_CP059_nave_fire_28mm (war round), CAM_nave_interior_28mm and CAM_ext_elevated_overview (those candidate side effects were REJECTED).
# Only CAM_CP056_nave_drill_gallery_28mm renders from war-r15_cp056 (manifest: scripts/sydenham_live_heroes.json).
# Recipe = the approved candidate "after" recipe (= live CP056 r14 hero recipe raised to 1920x1080 / 48 spp):
#   render.py, NO_PEOPLE=1, blend lighting/exposure, 1920x1080, 48 spp, one camera per Blender session.
#   scripts/render_cp056_rnd_live.sh [--rebuild] [outdir=renders/r18]
# --rebuild regenerates the round from war-r14 (md5-checked) into a TEMP blend and renders from that (war-r15_cp056 never overwritten).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/sydenham-war-r15_cp056.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-war-r14.blend | cut -c1-8) == 718c4b3d ]] || { echo "war-r14 md5 mismatch (expected 718c4b3d)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  "$B" -b rounds/sydenham-war-r14.blend -P scripts/candidate_cp056_rnd_nave_drill.py -- "$TMP/sydenham-war-r15_cp056.blend" 2>&1 | grep -E "CP056 SAVED|Error|Traceback" || true
  [[ -f "$TMP/sydenham-war-r15_cp056.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-war-r15_cp056.blend"
fi
OUT=${1:-renders/r18}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY15_rnd_depot_nave_drill_mess__1915"); print("CP056_RND_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP056_RND_IN_PLACE" || true)
echo "$CHK"; grep -q "CP056_RND_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP056 RND KEEP"; exit 3; }
export NO_PEOPLE=1 RES=1920x1080 THREADS=8
for CAM in CAM_CP056_nave_drill_gallery_28mm; do
  "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r18_war 100 48 "$CAM" 2>&1 | grep -E "PEOPLE_ADOPT|RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r18_war_CAM_CP056_nave_drill_gallery_28mm.png"
