#!/usr/bin/env bash
# CP032 LIVE (KEEP 2026-11-02: arrival yard dressing, DEPARTURES MV18). Renders live rounds/m02.blend ->
#   renders/m02/CP032_arrival_start.png and renders/m02/CP032_arrival_end.png
# with the exact settings of the KEEP candidate (render_cp032_yard.sh: render_shots.py, 1920x1080, 24 spp, look
# exposure, EACH camera in its own Blender session), so a re-run reproduces the live frames
# (= look/pairs_geo/KEEP_CP032_yard_{start,end}_after.png = renders/candidates/cp032_yard_20261102/*.png).
#   scripts/render_cp032_yard_live.sh [--rebuild]
# --rebuild regenerates live rounds/m02.blend from the pre-yard live m02 pinned at move commit b19926f (departure
# hands MV15 + arrival hands MV16 + near-foreground MV17 already in) by running scripts/candidate_cp032_yard.py --live
# on it (ARR_YD_* ruts, puddles, stones, boards, barrow, tools; GT_SydenhamClayYard rebuilt; spoil
# GT_SydenhamSpoil1852 + lumps; arrival sash-bar bundles GT_SashBarWeathered / GT_GutterTimberWeathered).
# Since the parkland oaks KEEP (2026-11-02, MV19) --rebuild then runs scripts/candidate_cp032_trees.py --live (asserting
# CP032_TREES_IN_PLACE True; parametric oaks, Sydenham meadow, ARR-only weathered bearers/crates, ARR_HD_HAT hats + hair),
# so the rebuilt m02 equals live and the arrival frames match KEEP_CP032_trees_{start,end}_after.png (earlier KEEP_*_after
# frames predate MV19). Without --rebuild this script is equivalent to render_cp032_trees_live.sh.
# Since the parkland haze v2 KEEP (2026-11-03, MV20) --rebuild then runs scripts/candidate_cp032_haze_v2.py --live
# (asserting CP032_HAZE_IN_PLACE True; layered hazed tree line with elms/far copses/hawthorns, continuous olive-green
# meadow + fine sward, cart track, cut ruts), so the rebuilt m02 equals live and the arrival frames match
# KEEP_CP032_haze_v2_{start,end}_after.png (earlier KEEP_*_after frames predate MV20). Without --rebuild this script is
# equivalent to render_cp032_haze_live.sh.
# Note: render_shots.py's render-time people swap imports this folder's people_lib.py; reproduction assumes that file
# is unchanged since the live render.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=b19926f
REL=course-models/crystal-palace-move-1852-grok/rounds/m02.blend
if [[ "${1:-}" == "--rebuild" ]]; then
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/m02.blend"
  YD=$("$B" -b "$TMP/m02.blend" -P scripts/candidate_cp032_yard.py -- --live 2>&1 | grep -E "CP032_YARD_IN_PLACE|Error|Traceback" || true)
  echo "$YD"; grep -q "CP032_YARD_IN_PLACE True" <<<"$YD" || { echo "CP032_YARD_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  TR=$("$B" -b "$TMP/m02.blend" -P scripts/candidate_cp032_trees.py -- --live 2>&1 | grep -E "CP032_TREES_IN_PLACE|Error|Traceback" || true)
  echo "$TR"; grep -q "CP032_TREES_IN_PLACE True" <<<"$TR" || { echo "CP032_TREES_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
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
