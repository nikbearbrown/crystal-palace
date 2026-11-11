#!/usr/bin/env bash
# CP014_drain_whole LIVE render from rounds/k01.blend. Live CP014_drain_whole = "Downes plate" KEEP (2026-11-11, parent viewed
# the pair; DEPARTURES KD07-KD13). Live k01 (md5 2c1e3235...) is a byte-copy of rounds/candidates/k01_cp014plate.blend, i.e.
# scripts/cand_cp014_plate_20261111.py applied to the pre-KEEP live k01 (md5 6f647743..., committed at construction 9436402;
# local pin rounds/k01.blend.pre_cp014plate_keep). Everything new is KD7_* with only_cams / hide_cams = CP014_drain_whole, so
# CP014_drain_roof/gutter/base render exactly as before (and still show the old base piece / gutter: known follow-up).
# Renders ONLY CP014_drain_whole_start with the KEEP recipe (look v1 era 1850, tod studio, 24 spp, 720x1280 portrait, exposure
# -0.13 re-matched to the pre-KEEP mean luma) -> renders/k01/CP014_drain_whole_start.png
# (= survey look/pairs_geo/CANDIDATE_CP014_plate_whole_start_after.png = renders/candidates/cp014_plate_20261111/after/*.png).
#   scripts/render_cp014_plate_live.sh [--rebuild] [samples=24] [outdir=renders/k01]
# --rebuild regenerates live rounds/k01.blend from the pre-KEEP k01 at commit 9436402 with cand_cp014_plate_20261111.py.
# Never run the candidate script on the already-promoted live k01 (it asserts: "candidate already applied").
# SUPERSEDED 2026-11-11 by scripts/render_cp014_cams_live.sh: live k01 now also carries the CP014 cams KEEP (KD14-KD16,
# md5 dc8469af...). Rendering here still gives the live CP014_drain_whole hero (= render_cp014_cams_live.sh whole, max 0),
# but --rebuild is forwarded to render_cp014_cams_live.sh --rebuild (the plate-only rebuild would DROP KD14-KD16).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=9436402
REL=course-models/crystal-palace-1851-construction-grok/rounds/k01.blend
EXP=-0.13
CHECK='import bpy; n=sum(o.name.startswith("KD7_") for o in bpy.data.objects); print("CP014_PLATE_IN_PLACE", n > 0, n)'
if [[ "${1:-}" == "--rebuild" ]]; then
  echo "forwarding to scripts/render_cp014_cams_live.sh --rebuild (keeps KD07-KD16)"; exec scripts/render_cp014_cams_live.sh "$@"
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/k01_base.blend"
  [[ $(md5sum < "$TMP/k01_base.blend" | cut -c1-8) == 6f647743 ]] || { echo "base k01 md5 mismatch"; rm -rf "$TMP"; exit 3; }
  "$B" -b "$TMP/k01_base.blend" -P scripts/cand_cp014_plate_20261111.py -- --out "$TMP/k01.blend" 2>&1 | grep -E "SOIL|LABELS_OUT|SAVED|Error|Traceback" || true
  CHK=$("$B" -b "$TMP/k01.blend" --python-expr "$CHECK" 2>&1 | grep -E "CP014_PLATE_IN_PLACE" || true)
  grep -q "CP014_PLATE_IN_PLACE True" <<<"$CHK" || { echo "CP014_PLATE_IN_PLACE check failed"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/k01.blend" rounds/k01.blend; rm -rf "$TMP"
fi
S=${1:-24}; OUT=${2:-renders/k01}
CHK=$("$B" -b rounds/k01.blend --python-expr "$CHECK" 2>&1 | grep -E "CP014_PLATE_IN_PLACE" || true)
echo "$CHK"; grep -q "CP014_PLATE_IN_PLACE True" <<<"$CHK" || { echo "live k01 does not carry the CP014 plate KEEP (run with --rebuild)"; exit 3; }
"$B" -b rounds/k01.blend -P scripts/render_views.py -- --cams CP014_drain_whole_start --outdir "$OUT" --res 1280x720 \
  --samples "$S" --era 1850 --tod studio --threads 8 --exposure "$EXP" 2>&1 | grep -E "WROTE|Error" || true
echo "done: $OUT/CP014_drain_whole_start.png"
