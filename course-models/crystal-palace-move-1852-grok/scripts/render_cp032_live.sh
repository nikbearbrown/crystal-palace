#!/usr/bin/env bash
# CP032 LIVE (KEEP 2026-11-02: departure hands, DEPARTURES MV15). Renders live rounds/m02.blend ->
#   renders/m02/CP032_departure_start.png
# with the exact settings of the KEEP candidate (render_cp032_people.sh: 1920x1080, 24 spp, look exposure via
# render_shots.py), so a re-run reproduces the live frame pixel-identically.
#   scripts/render_cp032_live.sh [--rebuild]
# --rebuild regenerates live rounds/m02.blend from the pre-promotion m02 pinned at move commit 9cb8eb5 by running
# scripts/candidate_cp032_people.py --live on it (the KEEP candidate script, applied in place), then
# scripts/candidate_cp032_arrival.py --live (arrival hands KEEP 2026-11-02, MV16; touches only STAFF_07..11, so the
# departure frame is unchanged and the rebuilt m02 equals the live one), then scripts/candidate_cp032_foreground.py
# --live (arrival near-foreground KEEP 2026-11-02, MV17; Sydenham-only material + CP032_arrival-only state; departure
# frame differs from the pre-MV17 m02 by noise only, max 3/255), then scripts/candidate_cp032_yard.py --live (arrival
# yard dressing KEEP 2026-11-02, MV18; ARR_YD_* objects + Sydenham-only materials; asserts CP032_YARD_IN_PLACE True;
# departure frames differ from the pre-MV18 m02 by noise only).
# Note: render_shots.py's render-time people swap imports this folder's people_lib.py; reproduction assumes that file
# is unchanged since the live render.
# Since the CP032 arrival KEEP (2026-11-02, MV16) live m02 no longer reproduces the stored departure frame bit for bit:
# DEP_HAND_* figures are unchanged (vertex/material/transform hashes identical), but the scene change at Sydenham
# (render-time swap count 5 -> 1, arrival STAFF stand-ins gone) shifts Cycles noise: max diff 11/255, mean 0.01,
# 19155 px non-zero. The stored renders/m02/CP032_departure_start.png (= KEEP_CP032_people_after.png) was left as is;
# running this script will overwrite it with the noise-level variant.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=9cb8eb5
REL=course-models/crystal-palace-move-1852-grok/rounds/m02.blend
if [[ "${1:-}" == "--rebuild" ]]; then
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/m02.blend"
  "$B" -b "$TMP/m02.blend" -P scripts/candidate_cp032_people.py -- --live 2>&1 | grep -E "CP032_HANDS_IN_PLACE|Error|Traceback"
  "$B" -b "$TMP/m02.blend" -P scripts/candidate_cp032_arrival.py -- --live 2>&1 | grep -E "CP032_ARR_HANDS_IN_PLACE|Error|Traceback"
  "$B" -b "$TMP/m02.blend" -P scripts/candidate_cp032_foreground.py -- --live 2>&1 | grep -E "CP032_FG_IN_PLACE|Error|Traceback"
  YD=$("$B" -b "$TMP/m02.blend" -P scripts/candidate_cp032_yard.py -- --live 2>&1 | grep -E "CP032_YARD_IN_PLACE|Error|Traceback" || true)
  echo "$YD"; grep -q "CP032_YARD_IN_PLACE True" <<<"$YD" || { echo "CP032_YARD_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/m02.blend" rounds/m02.blend
  rm -rf "$TMP"
fi
"$B" -b rounds/m02.blend -P scripts/render_shots.py -- --out renders/m02 --cams CP032_departure_start --samples 24 --pct 100 \
  2>&1 | grep -E "PEOPLE|RENDERED|Error" || true
echo "done: renders/m02/CP032_departure_start.png"
