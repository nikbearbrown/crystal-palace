#!/usr/bin/env bash
# CP013_sash LIVE renders from rounds/c04.blend. Live CP013_sash = "Downes roof" KEEP (2026-11-11, parent viewed both pairs;
# DEPARTURES CN54). Live c04 (md5 c8d1abc5...) is a byte-copy of rounds/candidates/c04_cp013sash.blend, i.e.
# scripts/cand_cp013_sash_20261111.py applied to the pre-KEEP live c04 (md5 415e5100..., committed at construction b71f5ce).
# Everything new is CP013S_* with only_cams / hide_cams = CP013_sash, so the other 16 c04 cameras render as before.
# Renders ONLY CP013_sash_start / _end with the KEEP settings (1280x720, 48 spp, default people handling, exposure re-matched to
# the pre-KEEP mean luma: start -0.78, end -0.95) -> renders/c04/CP013_sash_{start,end}.png
# (= survey look/pairs_geo/KEEP_CP013_sash_{start,end}_after.png = renders/candidates/cp013_sash_20261111/after/*.png).
#   scripts/render_cp013_sash_live.sh [--rebuild] [samples=48] [outdir=renders/c04]
# --rebuild regenerates live rounds/c04.blend from the pre-KEEP live c04 pinned at construction commit b71f5ce (md5 415e5100...)
# with cand_cp013_sash_20261111.py. That base already carries the CP015 canvas KEEP (CN52), so nothing earlier is dropped.
# Never run the candidate script on the already-promoted live c04 (it would add a second CP013S_* set).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=b71f5ce
REL=course-models/crystal-palace-1851-construction-grok/rounds/c04.blend
EXPOSURES="CP013_sash_start:-0.78 CP013_sash_end:-0.95"
CHECK='import bpy; n=sum(o.name.startswith("CP013S_") for o in bpy.data.objects); print("CP013_SASH_IN_PLACE", n > 0, n)'
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/c04_base.blend"
  [[ $(md5sum < "$TMP/c04_base.blend" | cut -c1-8) == 415e5100 ]] || { echo "base c04 md5 mismatch"; rm -rf "$TMP"; exit 3; }
  "$B" -b "$TMP/c04_base.blend" -P scripts/cand_cp013_sash_20261111.py -- --out "$TMP/c04.blend" 2>&1 | grep -E "ROOF|FRONTS|SAVED|Error|Traceback" || true
  CHK=$("$B" -b "$TMP/c04.blend" --python-expr "$CHECK" 2>&1 | grep -E "CP013_SASH_IN_PLACE" || true)
  grep -q "CP013_SASH_IN_PLACE True" <<<"$CHK" || { echo "CP013_SASH_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/c04.blend" rounds/c04.blend; rm -rf "$TMP"
fi
S=${1:-48}; OUT=${2:-renders/c04}
CHK=$("$B" -b rounds/c04.blend --python-expr "$CHECK" 2>&1 | grep -E "CP013_SASH_IN_PLACE" || true)
echo "$CHK"; grep -q "CP013_SASH_IN_PLACE True" <<<"$CHK" || { echo "live c04 does not carry the CP013 sash KEEP (run with --rebuild)"; exit 3; }
for CE in $EXPOSURES; do
  "$B" -b rounds/c04.blend -P scripts/render_views.py -- --cams "${CE%%:*}" --outdir "$OUT" --res 1280x720 \
    --samples "$S" --exposure "${CE##*:}" 2>&1 | grep -E "WROTE|Error" || true
done
echo "done: $OUT/CP013_sash_start.png $OUT/CP013_sash_end.png"
