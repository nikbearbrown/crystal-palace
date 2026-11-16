#!/usr/bin/env bash
# LONDON ln05 LIVE hero: CP005_room_start ONLY, from rounds/ln05_cp005room.blend = CP005 1849-50 planning room
# KEEP (scoped, 2026-11-16, lead viewed the pairs; DEPARTURES D-LN-CP005-01..11). ln05_cp005room.blend
# (md5 06b10667...) is a byte-copy of the approved candidate rounds/candidates/ln03_cp005.blend, i.e.
# scripts/build_cp005_room.py applied to live rounds/ln02.blend (md5 56e47151..., pinned by tag pre_cp005room_keep).
# ln02.blend is NOT changed; the side effect CP005_table_start was REJECTED (luma 215 -> 142 not exposure-matched; the
# close-up exposes faceted low-poly jug/decanter/plates) and CP002_terrace_start showed no change, so those cameras stay
# on rounds/ln02.blend; CP002_lane_start + CP002_factory_start stay on rounds/ln04_cp002lane.blend
# (scripts/london_live_heroes.json).
# Recipe = the approved candidate "after" recipe = the live CP005 recipe (survey look/batch_mat_keeplight.py):
# scripts/render_cp005_candidate.py -> enhance_offsite_materials + render_views.py --keep-lighting, era 1850,
# exterior_midday, authored exposure -0.10, 1280x720, 28 spp, 8 threads.
# The pre-KEEP frame renders/ln02/CP005_room_start.png stays in place.
#   scripts/render_cp005_room_live.sh [--rebuild] [outdir=renders/ln05_cp005room]
# --rebuild regenerates the round from ln02.blend (md5-checked) with build_cp005_room.py into a TEMP blend and renders
# from that (rounds/ln05_cp005room.blend is never overwritten), so outdir PNGs can be diffed against the live hero.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/ln05_cp005room.blend; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
CAMS=CP005_room_start
CHECK='import bpy; o=[x for x in bpy.data.objects if x.name.startswith("LN3_")]; print("CP005_ROOM_IN_PLACE", len(o) > 0 and bpy.data.objects.get("LN_CommissionTable") is None, len(o))'
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/ln02.blend | cut -c1-8) == 56e47151 ]] || { echo "ln02.blend md5 mismatch (expected 56e47151)"; exit 3; }
  "$B" -b rounds/ln02.blend -P scripts/build_cp005_room.py -- --out "$TMP/ln05_cp005room.blend" 2>&1 | grep -E "^SAVED|Error|Traceback" | cut -c1-200 || true
  [[ -f "$TMP/ln05_cp005room.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/ln05_cp005room.blend"
else
  [[ $(md5sum < "$ROUND" | cut -c1-8) == 06b10667 ]] || { echo "$ROUND md5 mismatch (expected 06b10667)"; exit 3; }
fi
OUT=${1:-renders/ln05_cp005room}; mkdir -p "$OUT"
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP005_ROOM_IN_PLACE" || true)
echo "$CHK"; grep -q "CP005_ROOM_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP005 room KEEP"; exit 3; }
for CAM in ${CAMS//,/ }; do   # one camera per Blender session
  python3 scripts/render_cp005_candidate.py "$ROUND" "$CAM" "$TMP/r" --era 1850 > "$TMP/render_$CAM.log" 2>&1 || { tail -20 "$TMP/render_$CAM.log"; exit 3; }
  mv "$TMP/r/$CAM.png" "$OUT/$CAM.png"
  echo "done: $OUT/$CAM.png"
done
