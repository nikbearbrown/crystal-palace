#!/usr/bin/env bash
# SYDENHAM r18 LATE11 LIVE hero: CP051 electric_nave 28mm ONLY, from rounds/sydenham-late11-r17_cp051.blend =
# CP051 1903 SMMT motor show KEEP (2026-11-14, parent viewed the pairs; DEPARTURES D-SY-CP051-01..10).
# late11-r17_cp051 (md5 579800c4...) is a byte copy of the approved candidate rounds/candidates/sydenham-late11-r16_cp051motor.blend,
# i.e. scripts/candidate_cp051_motor_show.py applied to live rounds/sydenham-late11-r16.blend (md5 3ce48caf..., pinned by tag
# pre_cp051motor_keep). late11-r16 is NOT changed and still serves CAM_CP052_scaffold_reglaze_35mm, CAM_CP054_plymouth_rescue_35mm,
# CAM_CP049_worn_garden_front_35mm, CAM_nave_interior_28mm and CAM_CP059_nave_fire_28mm (late11 round) — those candidate side
# effects were REJECTED / not routed.
# Only CAM_CP051_electric_nave_28mm renders from late11-r17_cp051 (manifest: scripts/sydenham_live_heroes.json).
# Recipe = the approved candidate "after" recipe (scripts/render_cp051_candidate.sh = live LATE11 hero recipe raised to 1920x1080 / 48 spp):
#   render.py, NO_PEOPLE=1, blend lighting/exposure (late11-r16: Filmic -1.0), 1920x1080, 48 spp, one camera per Blender session.
#   scripts/render_cp051_motor_live.sh [--rebuild] [outdir=renders/r18]
# --rebuild regenerates the round from late11-r16 (md5-checked) into a TEMP blend and renders from that (late11-r17_cp051 never overwritten).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/sydenham-late11-r17_cp051.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-late11-r16.blend | cut -c1-8) == 3ce48caf ]] || { echo "late11-r16 md5 mismatch (expected 3ce48caf)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  env -u CP051_NOSAVE "$B" -b rounds/sydenham-late11-r16.blend -P scripts/candidate_cp051_motor_show.py -- "$TMP/sydenham-late11-r17_cp051.blend" 2>&1 | grep -E "CP051 (SAVED|BUILT)|Error|Traceback" || true
  [[ -f "$TMP/sydenham-late11-r17_cp051.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-late11-r17_cp051.blend"
fi
OUT=${1:-renders/r18}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY03_smmt_motor_show_nave__1903"); print("CP051_MOTOR_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP051_MOTOR_IN_PLACE" || true)
echo "$CHK"; grep -q "CP051_MOTOR_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP051 motor show KEEP"; exit 3; }
export NO_PEOPLE=1 RES=1920x1080 THREADS=8
for CAM in CAM_CP051_electric_nave_28mm; do
  "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r18_late11 100 48 "$CAM" 2>&1 | grep -E "PEOPLE_ADOPT|RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r18_late11_CAM_CP051_electric_nave_28mm.png"
