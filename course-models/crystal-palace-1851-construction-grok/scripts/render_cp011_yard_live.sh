#!/usr/bin/env bash
# CP011 LIVE (KEEP 2026-11-03 start+end, parent viewed the pairs; DEPARTURES CN47): works yard dressing in the live
# rounds/c07.blend (brick works + chimneys, cinder yard, girder/column piles on bearers, timber bay, trolley, 9 people_lib
# figures). Renders ONLY CP011_yard_start / CP011_yard_end with the exact KEEP settings (render_views.py, 1280x720, 48 spp,
# look v1, --no-people because the figures are pre-built, exposure 0.95 start / 1.06 end, each camera in its own
# Blender session) -> renders/c07/CP011_yard_{start,end}.png
# (= survey look/pairs_geo/KEEP_CP011_yard_{start,end}_after.png = renders/candidates/cp011_yard_20261103/after/*.png).
#   scripts/render_cp011_yard_live.sh [--rebuild] [samples=48] [outdir=renders/c07]
# --rebuild regenerates live rounds/c07.blend from the pre-yard live c07 pinned at construction commit f73d09c
# (md5 c6189435...) by running scripts/cand_cp011_yard_20261103.py --live on it and asserting CP011_YARD_IN_PLACE True.
# The live build is camera-scoped: new CP011C_* objects carry only_cams=CP011_yard; the CP014 drainage cutaway
# (DETAIL_DRAINAGE), the old KYARD stock and KWORKER_024-026 carry hide_cams=CP011_yard (render_views.py), so CP014 and
# every other c07 shot render as before. Never render CP011 with render_round.sh (wrong exposure + people swap).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=f73d09c
REL=course-models/crystal-palace-1851-construction-grok/rounds/c07.blend
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/c07.blend"
  YD=$("$B" -b "$TMP/c07.blend" -P scripts/cand_cp011_yard_20261103.py -- --live 2>&1 | grep -E "CP011_YARD|Error|Traceback" || true)
  echo "$YD"; grep -q "CP011_YARD_IN_PLACE True" <<<"$YD" || { echo "CP011_YARD_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/c07.blend" rounds/c07.blend
  rm -rf "$TMP"
fi
S=${1:-48}; OUT=${2:-renders/c07}
CHK=$("$B" -b rounds/c07.blend -P scripts/cand_cp011_yard_20261103.py -- --check 2>&1 | grep -E "CP011_YARD_IN_PLACE" || true)
echo "$CHK"; grep -q "CP011_YARD_IN_PLACE True" <<<"$CHK" || { echo "live c07 does not carry the CP011 yard (run with --rebuild)"; exit 3; }
for CE in CP011_yard_start:0.95 CP011_yard_end:1.06; do
  "$B" -b rounds/c07.blend -P scripts/render_views.py -- --cams "${CE%%:*}" --outdir "$OUT" --res 1280x720 \
    --samples "$S" --no-people --exposure "${CE##*:}" 2>&1 | grep -E "WROTE|Error" || true
done
echo "done: $OUT/CP011_yard_start.png $OUT/CP011_yard_end.png"
