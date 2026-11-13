#!/usr/bin/env bash
# SYDENHAM r18 LIVE heroes: CP044 x2 (pay_desks 35mm at the railway entrance + maintenance 50mm) from
# rounds/sydenham-1856-r18_cp044.blend = CP044 railway-entrance admission KEEP (2026-11-13, parent viewed the pairs;
# DEPARTURES D-SY-CP044-01..18). r18_cp044 (md5 70f5ef98...) is a byte copy of the approved candidate
# rounds/candidates/sydenham-1856-r16_cp044gate.blend, i.e. scripts/candidate_cp044_railway_entrance.py applied to live
# rounds/sydenham-1856-r16.blend (md5 1b984fb6..., pinned by tag pre_cp044gate_keep). r16 is NOT changed and still serves
# every other EARLY cam (CP037/CP041/CP042 ...); CP064 keeps rendering from rounds/sydenham-ruins-r17.blend (the candidate's
# CP064 side effect was REJECTED). Only the two CP044 cams render from r18_cp044 (manifest: scripts/sydenham_live_heroes.json).
# Recipe = the approved candidate "after" recipe (= live CP044 hero recipe, batch_people_v31_crowds.py CP037+CP044 group):
#   render.py, PEOPLE_ERA=1850s PEOPLE_SEED=81, blend lighting, 1920x1080, 48 spp, one camera per Blender session.
#   scripts/render_cp044_gate_live.sh [--rebuild] [outdir=renders/r18]
# --rebuild regenerates the round from r16 (md5-checked) into a TEMP blend and renders from that (r18_cp044 never overwritten).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/sydenham-1856-r18_cp044.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-1856-r16.blend | cut -c1-8) == 1b984fb6 ]] || { echo "r16 md5 mismatch (expected 1b984fb6)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  "$B" -b rounds/sydenham-1856-r16.blend -P scripts/candidate_cp044_railway_entrance.py -- "$TMP/sydenham-1856-r18_cp044.blend" 2>&1 | grep -E "CP044 SAVED|Error|Traceback" || true
  [[ -f "$TMP/sydenham-1856-r18_cp044.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1856-r18_cp044.blend"
fi
OUT=${1:-renders/r18}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY56_railway_entrance_admission__c1856"); print("CP044_GATE_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP044_GATE_IN_PLACE" || true)
echo "$CHK"; grep -q "CP044_GATE_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP044 gate KEEP"; exit 3; }
export PEOPLE_ERA=1850s PEOPLE_SEED=81 RES=1920x1080 THREADS=8
for CAM in CAM_CP044_pay_desks_35mm CAM_CP044_maintenance_50mm; do
  "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r18 100 48 "$CAM" 2>&1 | grep -E "PEOPLE_ADOPT|RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r18_CAM_CP044_{pay_desks_35mm,maintenance_50mm}.png"
