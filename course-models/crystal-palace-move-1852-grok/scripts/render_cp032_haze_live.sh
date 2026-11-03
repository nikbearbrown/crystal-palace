#!/usr/bin/env bash
# CP032 LIVE (KEEP 2026-11-03: parkland depth + aerial haze v2 - layered hazed tree line with elms, far copses and
# hawthorns, continuous olive-green meadow GT_SydenhamMeadow1852c + fine sward, cart track, cut ruts faded in the girder
# shadow; DEPARTURES MV20 v2; v1 REJECTED). Renders live rounds/m02.blend ->
#   renders/m02/CP032_arrival_start.png and renders/m02/CP032_arrival_end.png
# with the exact settings of the KEEP candidate (render_cp032_haze_v2.sh: render_shots.py, 1920x1080, 24 spp, look
# exposure, EACH camera in its own Blender session), so a re-run reproduces the live frames
# (= look/pairs_geo/KEEP_CP032_haze_v2_{start,end}_after.png = renders/candidates/cp032_haze_v2_20261103/*.png).
#   scripts/render_cp032_haze_live.sh [--rebuild]
# --rebuild regenerates live rounds/m02.blend from the pre-haze live m02 pinned at move commit 5b943fa (departure
# hands MV15 + arrival hands MV16 + near-foreground MV17 + yard dressing MV18 + parkland oaks MV19 already in) by running
# scripts/candidate_cp032_haze_v2.py --live on it and asserting CP032_HAZE_IN_PLACE True.
# Note: render_shots.py's render-time people swap imports this folder's people_lib.py; reproduction assumes that file
# is unchanged since the live render.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=5b943fa
REL=course-models/crystal-palace-move-1852-grok/rounds/m02.blend
if [[ "${1:-}" == "--rebuild" ]]; then
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/m02.blend"
  HZ=$("$B" -b "$TMP/m02.blend" -P scripts/candidate_cp032_haze_v2.py -- --live 2>&1 | grep -E "CP032_HAZE_IN_PLACE|Error|Traceback" || true)
  echo "$HZ"; grep -q "CP032_HAZE_IN_PLACE True" <<<"$HZ" || { echo "CP032_HAZE_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/m02.blend" rounds/m02.blend
  rm -rf "$TMP"
fi
for C in CP032_arrival_start CP032_arrival_end; do
  "$B" -b rounds/m02.blend -P scripts/render_shots.py -- --out renders/m02 --cams "$C" --samples 24 --pct 100 \
    2>&1 | grep -E "PEOPLE|RENDERED|Error" || true
done
echo "done: renders/m02/CP032_arrival_start.png renders/m02/CP032_arrival_end.png"
