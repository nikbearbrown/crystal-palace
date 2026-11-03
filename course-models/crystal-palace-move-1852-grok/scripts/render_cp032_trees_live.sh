#!/usr/bin/env bash
# CP032 LIVE (KEEP 2026-11-02: parkland oaks + Sydenham meadow + weathered bearers/crates + workmen hats/hair,
# DEPARTURES MV19). Renders live rounds/m02.blend ->
#   renders/m02/CP032_arrival_start.png and renders/m02/CP032_arrival_end.png
# with the exact settings of the KEEP candidate (render_cp032_trees.sh: render_shots.py, 1920x1080, 24 spp, look
# exposure, EACH camera in its own Blender session), so a re-run reproduces the live frames
# (= look/pairs_geo/KEEP_CP032_trees_{start,end}_after.png = renders/candidates/cp032_trees_20261102/*.png).
#   scripts/render_cp032_trees_live.sh [--rebuild]
# --rebuild regenerates live rounds/m02.blend from the pre-trees live m02 pinned at move commit d1711db (departure
# hands MV15 + arrival hands MV16 + near-foreground MV17 + yard dressing MV18 already in) by running
# scripts/candidate_cp032_trees.py --live on it (lollipop parkland meshes swapped for parametric oaks, Sydenham meadow,
# ARR-only weathered bearers/crates, ARR_HD_HAT felt hats + hair on the ARR_HAND workmen) and asserting
# CP032_TREES_IN_PLACE True.
# Note: render_shots.py's render-time people swap imports this folder's people_lib.py; reproduction assumes that file
# is unchanged since the live render.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=d1711db
REL=course-models/crystal-palace-move-1852-grok/rounds/m02.blend
if [[ "${1:-}" == "--rebuild" ]]; then
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/m02.blend"
  TR=$("$B" -b "$TMP/m02.blend" -P scripts/candidate_cp032_trees.py -- --live 2>&1 | grep -E "CP032_TREES_IN_PLACE|Error|Traceback" || true)
  echo "$TR"; grep -q "CP032_TREES_IN_PLACE True" <<<"$TR" || { echo "CP032_TREES_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/m02.blend" rounds/m02.blend
  rm -rf "$TMP"
fi
for C in CP032_arrival_start CP032_arrival_end; do
  "$B" -b rounds/m02.blend -P scripts/render_shots.py -- --out renders/m02 --cams "$C" --samples 24 --pct 100 \
    2>&1 | grep -E "PEOPLE|RENDERED|Error" || true
done
echo "done: renders/m02/CP032_arrival_start.png renders/m02/CP032_arrival_end.png"
