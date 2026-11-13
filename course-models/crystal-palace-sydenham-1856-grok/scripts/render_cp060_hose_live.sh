#!/usr/bin/env bash
# SYDENHAM r18 FIRE LIVE hero: CP060 crowd_watching 35mm ONLY, from rounds/sydenham-1936fire-r13_cp060.blend =
# CP060 Parade hose crews KEEP (2026-11-13, parent viewed the pairs; DEPARTURES D-SY-CP060-01..08).
# fire-r13_cp060 (md5 dccd2c62...) is a byte copy of the approved candidate rounds/candidates/sydenham-1936fire-r12_cp060hose.blend,
# i.e. scripts/candidate_cp060_hose_crews.py applied to rounds/sydenham-1936fire-r12.blend (md5 33102f4b..., pinned by tag
# pre_cp060hose_keep). fire-r12 is NOT changed. The candidate side effects on CAM_CP058_parade_appliances_35mm and
# CAM_CP061_transept_collapse_35mm were REJECTED / not routed (CP058 stays on 1936after-r17, CP061 on 1936fire-r11b).
# Only CAM_CP060_crowd_watching_35mm renders from fire-r13_cp060 (manifest: scripts/sydenham_live_heroes.json).
# Recipe = the approved candidate "after" recipe (scripts/render_cp060_candidate.sh):
#   render.py, NO_PEOPLE=1, blend lighting/exposure (fire-r12: Filmic, -0.5 EV), 1920x1080, 48 spp, one camera per Blender session.
#   scripts/render_cp060_hose_live.sh [--rebuild] [outdir=renders/r18]
# --rebuild regenerates the round from fire-r12 (md5-checked) into a TEMP blend and renders from that (fire-r13_cp060 never overwritten).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/sydenham-1936fire-r13_cp060.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-1936fire-r12.blend | cut -c1-8) == 33102f4b ]] || { echo "fire-r12 md5 mismatch (expected 33102f4b)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  "$B" -b rounds/sydenham-1936fire-r12.blend -P scripts/candidate_cp060_hose_crews.py -- "$TMP/sydenham-1936fire-r13_cp060.blend" 2>&1 | grep -E "CP060 (SAVED|BUILT)|Error|Traceback" || true
  [[ -f "$TMP/sydenham-1936fire-r13_cp060.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1936fire-r13_cp060.blend"
fi
OUT=${1:-renders/r18}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY36_parade_hose_crews__30Nov1936"); print("CP060_HOSE_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP060_HOSE_IN_PLACE" || true)
echo "$CHK"; grep -q "CP060_HOSE_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP060 hose crews KEEP"; exit 3; }
export NO_PEOPLE=1 RES=1920x1080 THREADS=8
for CAM in CAM_CP060_crowd_watching_35mm; do
  "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r18_fire 100 48 "$CAM" 2>&1 | grep -E "PEOPLE_ADOPT|RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r18_fire_CAM_CP060_crowd_watching_35mm.png"
