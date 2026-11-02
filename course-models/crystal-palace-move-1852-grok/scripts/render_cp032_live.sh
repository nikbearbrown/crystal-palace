#!/usr/bin/env bash
# CP032 LIVE (KEEP 2026-11-02: departure hands, DEPARTURES MV15). Renders live rounds/m02.blend ->
#   renders/m02/CP032_departure_start.png
# with the exact settings of the KEEP candidate (render_cp032_people.sh: 1920x1080, 24 spp, look exposure via
# render_shots.py), so a re-run reproduces the live frame pixel-identically.
#   scripts/render_cp032_live.sh [--rebuild]
# --rebuild regenerates live rounds/m02.blend from the pre-promotion m02 pinned at move commit 9cb8eb5 by running
# scripts/candidate_cp032_people.py --live on it (the KEEP candidate script, applied in place).
# Note: render_shots.py's render-time people swap imports this folder's people_lib.py; reproduction assumes that file
# is unchanged since the live render.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=9cb8eb5
REL=course-models/crystal-palace-move-1852-grok/rounds/m02.blend
if [[ "${1:-}" == "--rebuild" ]]; then
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/m02.blend"
  "$B" -b "$TMP/m02.blend" -P scripts/candidate_cp032_people.py -- --live 2>&1 | grep -E "CP032_HANDS_IN_PLACE|Error|Traceback"
  mv "$TMP/m02.blend" rounds/m02.blend
  rm -rf "$TMP"
fi
"$B" -b rounds/m02.blend -P scripts/render_shots.py -- --out renders/m02 --cams CP032_departure_start --samples 24 --pct 100 \
  2>&1 | grep -E "PEOPLE|RENDERED|Error" || true
echo "done: renders/m02/CP032_departure_start.png"
