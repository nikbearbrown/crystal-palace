#!/usr/bin/env bash
# LONDON ln04 LIVE heroes: CP002_lane_start + CP002_factory_start ONLY, from rounds/ln04_cp002lane.blend = CP002 1850
# railway lane KEEP (scoped, 2026-11-16, lead viewed the pairs; DEPARTURES D-LN-CP002-01..13). ln04_cp002lane.blend
# (md5 33262e1f...) is a byte-copy of the approved candidate rounds/candidates/ln03_cp002.blend, i.e.
# scripts/build_cp002_street.py applied to live rounds/ln02.blend (md5 56e47151..., pinned by tag pre_cp002lane_keep).
# ln02.blend is NOT changed; the side effects CP002_terrace_start and CP005_table_start were REJECTED and CP005_room_start
# showed no change, so those three cameras stay on rounds/ln02.blend (scripts/london_live_heroes.json).
# Recipe = the approved candidate "after" recipe = the live CP002 recipe (survey look/batch_mat_keeplight.py):
# scripts/render_cp002_candidate.py -> enhance_offsite_materials + render_views.py --keep-lighting, era 1840s,
# exterior_midday, authored exposure -0.10, 1280x720, 28 spp, 8 threads.
# Routing: scripts/london_live_heroes.json. The pre-KEEP frames renders/ln02/CP002_{lane,factory}_start.png stay in place.
#   scripts/render_cp002_lane_live.sh [--rebuild] [outdir=renders/ln04_cp002lane]
# --rebuild regenerates the round from ln02.blend (md5-checked) with build_cp002_street.py into a TEMP blend and renders
# from that (rounds/ln04_cp002lane.blend is never overwritten), so outdir PNGs can be diffed against the live heroes.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/ln04_cp002lane.blend; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
CAMS=CP002_lane_start,CP002_factory_start
CHECK='import bpy; o=[x for x in bpy.data.objects if x.name.startswith("LN2_")]; print("CP002_LANE_IN_PLACE", len(o) > 0 and bpy.data.objects.get("LN_Viaduct") is None, len(o))'
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/ln02.blend | cut -c1-8) == 56e47151 ]] || { echo "ln02.blend md5 mismatch (expected 56e47151)"; exit 3; }
  "$B" -b rounds/ln02.blend -P scripts/build_cp002_street.py -- --out "$TMP/ln04_cp002lane.blend" 2>&1 | grep -E "^SAVED|Error|Traceback" | cut -c1-200 || true
  [[ -f "$TMP/ln04_cp002lane.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/ln04_cp002lane.blend"
else
  [[ $(md5sum < "$ROUND" | cut -c1-8) == 33262e1f ]] || { echo "$ROUND md5 mismatch (expected 33262e1f)"; exit 3; }
fi
OUT=${1:-renders/ln04_cp002lane}; mkdir -p "$OUT"
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP002_LANE_IN_PLACE" || true)
echo "$CHK"; grep -q "CP002_LANE_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP002 lane KEEP"; exit 3; }
for CAM in ${CAMS//,/ }; do   # one camera per Blender session
  python3 scripts/render_cp002_candidate.py "$ROUND" "$CAM" "$TMP/r" > "$TMP/render_$CAM.log" 2>&1 || { tail -20 "$TMP/render_$CAM.log"; exit 3; }
  mv "$TMP/r/$CAM.png" "$OUT/$CAM.png"
  echo "done: $OUT/$CAM.png"
done
