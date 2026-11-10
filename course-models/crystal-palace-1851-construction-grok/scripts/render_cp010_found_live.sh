#!/usr/bin/env bash
# CP010_foundations LIVE renders from rounds/c06.blend. Live CP010_foundations = "setting out + gravel" KEEP (2026-11-10,
# parent viewed the pairs; DEPARTURES CN53), promoted with scripts/cand_cp010_found_20261110.py --live: everything new is
# CP010F_* with only_cams=CP010_foundations (stakes, hero bedding, rough spoil copies, 64 pre-built people_lib workmen
# CP010F_HAND_*), replaced originals (KSPOIL heaps near the walk, the KWORKER figures in frame) carry hide_cams=CP010_foundations,
# and the ground / far spoil field swap material by cam_mat. CP010_extent, CP010_base_insert, CP016 and every other c06 shot
# render as before (render_views.py reads only_cams / hide_cams / cam_mat).
# Renders ONLY CP010_foundations_start / _end with the exact KEEP settings (1280x720, 48 spp, look v1.1, --no-people because the
# figures are pre-built, each camera in its own Blender session, per-shot exposure re-matched to the pre-KEEP mean luma)
# -> renders/c06/CP010_foundations_{start,end}.png (= survey look/pairs_geo/KEEP_CP010_found_{start,end}_after.png
#    = renders/candidates/cp010_found_20261110/after/*.png).
#   scripts/render_cp010_found_live.sh [--rebuild] [samples=48] [outdir=renders/c06]
# --rebuild regenerates live rounds/c06.blend from the pre-KEEP live c06 pinned at construction commit fdf7c8a (md5 e461f024...)
# with cand_cp010_found_20261110.py --live (no --fix-digger: moving the original digger changes CP010_extent_end, see PROGRESS). Never render CP010_foundations with render_round.sh (wrong exposure + people swap).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=fdf7c8a
REL=course-models/crystal-palace-1851-construction-grok/rounds/c06.blend
EXPOSURES="CP010_foundations_start:-0.42 CP010_foundations_end:-0.31"
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/c06.blend"
  OUTP=$("$B" -b "$TMP/c06.blend" -P scripts/cand_cp010_found_20261110.py -- --live 2>&1 | grep -E "PEOPLE_SWAPPED|DIGGER|SAVED|Error|Traceback" || true)
  echo "$OUTP"
  CHK=$("$B" -b "$TMP/c06.blend" -P scripts/cand_cp010_found_20261110.py -- --check 2>&1 | grep -E "CP010_FOUND_IN_PLACE" || true)
  grep -q "CP010_FOUND_IN_PLACE True" <<<"$CHK" || { echo "CP010_FOUND_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/c06.blend" rounds/c06.blend; rm -rf "$TMP"
fi
S=${1:-48}; OUT=${2:-renders/c06}
CHK=$("$B" -b rounds/c06.blend -P scripts/cand_cp010_found_20261110.py -- --check 2>&1 | grep -E "CP010_FOUND_IN_PLACE" || true)
echo "$CHK"; grep -q "CP010_FOUND_IN_PLACE True" <<<"$CHK" || { echo "live c06 does not carry the CP010 foundations KEEP (run with --rebuild)"; exit 3; }
for CE in $EXPOSURES; do
  "$B" -b rounds/c06.blend -P scripts/render_views.py -- --cams "${CE%%:*}" --outdir "$OUT" --res 1280x720 \
    --samples "$S" --no-people --exposure "${CE##*:}" 2>&1 | grep -E "WROTE|Error" || true
done
echo "done: $OUT/CP010_foundations_start.png $OUT/CP010_foundations_end.png"
