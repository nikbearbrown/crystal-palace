#!/usr/bin/env bash
# PARK-NOW r22 LIVE heroes: CP070 x2 (begin_walk + park_entry) from rounds/parknow-r22_cp070.blend = CP070 Low Level station
# KEEP (2026-11-13, parent viewed the pairs; DEPARTURES D-PM-33..41). parknow-r22_cp070.blend (md5 22ee900f...) is a byte-copy
# of the approved candidate rounds/candidates/parknow-r02_cp070station.blend, i.e. scripts/candidate_cp070_station.py applied
# to live rounds/parknow-r02.blend (md5 48fc01ec..., pinned by tag pre_cp070station_keep). parknow-r02.blend is NOT changed and
# still serves CP067/CP072/CP074/CP075 (the CP075 + CP067 side effects of the station candidate were REJECTED). Only the two
# CP070 cams render from r22 (manifest: scripts/parknow_live_heroes.json). The camera move to the station is part of the KEEP.
# Recipe = the approved candidate "after" recipe: pk_grass_plateau shown (scripts/live_plateau_show.py, = how the live CP070
# heroes were always rendered) + scripts/render_cp076_look.py (look v1.1 present / exterior_afternoon, exposure from the look
# (-0.8)), 1920x1080, 48 spp, one camera per Blender session.
#   scripts/render_cp070_station_live.sh [--rebuild] [outdir=renders]
# --rebuild regenerates the round from parknow-r02.blend (md5-checked) with candidate_cp070_station.py into a TEMP blend and
# renders from that (rounds/parknow-r22_cp070.blend is never overwritten), so outdir PNGs can be diffed against the live heroes.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/parknow-r22_cp070.blend; TMP=""
CHECK='import bpy; n=sum(1 for o in bpy.data.objects if "cp070_now" in o.keys()); print("CP070_STATION_IN_PLACE", n > 0, n)'
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/parknow-r02.blend | cut -c1-8) == 48fc01ec ]] || { echo "parknow-r02.blend md5 mismatch (expected 48fc01ec)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  "$B" -b rounds/parknow-r02.blend -P scripts/candidate_cp070_station.py -- --out "$TMP/parknow-r22_cp070.blend" 2>&1 | grep -E "CP070_CANDIDATE_SAVED|Error|Traceback" || true
  [[ -f "$TMP/parknow-r22_cp070.blend" ]] || { echo "rebuild failed"; exit 3; }
  git checkout -- checks/cp070_station_candidate.json 2>/dev/null || true   # candidate script rewrites its log; keep the committed one
  ROUND="$TMP/parknow-r22_cp070.blend"
fi
OUT=${1:-renders}; mkdir -p "$OUT"
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP070_STATION_IN_PLACE" || true)
echo "$CHK"; grep -q "CP070_STATION_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP070 station KEEP"; exit 3; }
for CAM in CAM_CP070_begin_walk_35mm CAM_CP070_park_entry_35mm; do
  "$B" -b "$ROUND" -P scripts/live_plateau_show.py -P scripts/render_cp076_look.py -- "$OUT/r22_parknow_${CAM}.png" "$CAM" CP070 none 1920x1080 48 2>&1 | grep -E "LIVE_PLATEAU_SHOW|RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r22_parknow_CAM_CP070_{begin_walk,park_entry}_35mm.png"
