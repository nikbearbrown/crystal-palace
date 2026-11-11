#!/usr/bin/env bash
# CP014 LIVE renders (all four CP014 shots) from rounds/k01.blend. Live k01 = CP014 cams KEEP (2026-11-11, parent viewed all
# four pairs; DEPARTURES KD14-KD16) on top of the CP014_drain_whole "Downes plate" KEEP (KD07-KD13). Live k01
# (md5 dc8469af...) is a byte-copy of rounds/candidates/k01_cp014cams.blend, i.e. scripts/cand_cp014_cams_20261111.py applied
# to the pre-KEEP live k01 (md5 2c1e3235..., committed at 4f7da40; local pin rounds/k01.blend.pre_cp014cams_keep).
# Renders CP014_drain_{whole,roof,gutter,base}_start, ONE camera per Blender session (the recipe of render_cp014_cams.sh),
# look v1 era 1850 / tod studio, 24 spp, 1280x720 (whole 720x1280 portrait via its res prop), exposures re-matched to the
# pre-KEEP mean luma: whole -0.13, roof 0.40, gutter 0.42, base 0.30 -> renders/k01/CP014_drain_<cam>_start.png
# (= renders/candidates/cp014_cams_20261111/after/*.png = survey look/pairs_geo/CANDIDATE_CP014_cams_*_after.png).
#   scripts/render_cp014_cams_live.sh [--rebuild | --rebuild-scratch] [samples=24] [outdir=renders/k01]
# --rebuild regenerates live rounds/k01.blend as build_drain.py output -> cand_cp014_plate_20261111.py ->
# cand_cp014_cams_20261111.py, taking the build_drain.py output as COMMITTED at f2c8530 (k01 md5 6f647743..., also at 9436402).
# Reproduces the live renders at max diff 0 (checked 2026-11-11).
# --rebuild-scratch runs today's scripts/build_drain.py instead. It does NOT reproduce live (checked 2026-11-11: whole max 218,
# base max 118, roof/gutter max ~170): build_drain.py was edited at ae50e7d (rejected Muse gutter profile MK03b) and a fresh
# build places the scale figure differently (visible in CP014_drain_base), so a fresh build != committed k01 even before KD07.
# build_drain.py alone, or + the plate script alone, DROPS the polish.
# Never run either candidate script on the already-promoted live k01 (they assert "candidate already applied").
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
CHECK='import bpy; o=bpy.data.objects; a=sum(x.name.startswith("KD7_") for x in o); b=sum(x.name.startswith("KD14_") for x in o); print("CP014_CAMS_IN_PLACE", a > 0 and b > 0, a, b)'
if [[ "${1:-}" == "--rebuild" || "${1:-}" == "--rebuild-scratch" ]]; then
  MODE=$1; shift
  TMP=$(mktemp -d)
  if [[ "$MODE" == "--rebuild" ]]; then
    git show "f2c8530:course-models/crystal-palace-1851-construction-grok/rounds/k01.blend" > "$TMP/k01_drain.blend"
    [[ $(md5sum < "$TMP/k01_drain.blend" | cut -c1-8) == 6f647743 ]] || { echo "committed build_drain k01 md5 mismatch"; rm -rf "$TMP"; exit 3; }
  else
    echo "WARNING: --rebuild-scratch does not reproduce the live renders (see header)"
    "$B" -b -P scripts/build_drain.py -- --out "$TMP/k01_drain.blend" 2>&1 | grep -E "Saved|Error|Traceback" || true
    [[ -f "$TMP/k01_drain.blend" ]] || { echo "build_drain.py failed"; rm -rf "$TMP"; exit 3; }
  fi
  "$B" -b "$TMP/k01_drain.blend" -P scripts/cand_cp014_plate_20261111.py -- --out "$TMP/k01_plate.blend" 2>&1 | grep -E "SOIL|LABELS_OUT|SAVED|Error|Traceback" || true
  "$B" -b "$TMP/k01_plate.blend" -P scripts/cand_cp014_cams_20261111.py -- --out "$TMP/k01.blend" 2>&1 | grep -E "KD1|LABELS_OUT|SAVED|Error|Traceback" || true
  CHK=$("$B" -b "$TMP/k01.blend" --python-expr "$CHECK" 2>&1 | grep -E "CP014_CAMS_IN_PLACE" || true)
  grep -q "CP014_CAMS_IN_PLACE True" <<<"$CHK" || { echo "CP014_CAMS_IN_PLACE check failed: $CHK"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/k01.blend" rounds/k01.blend; rm -rf "$TMP"
fi
S=${1:-24}; OUT=${2:-renders/k01}
CHK=$("$B" -b rounds/k01.blend --python-expr "$CHECK" 2>&1 | grep -E "CP014_CAMS_IN_PLACE" || true)
echo "$CHK"; grep -q "CP014_CAMS_IN_PLACE True" <<<"$CHK" || { echo "live k01 does not carry the CP014 cams KEEP (run with --rebuild)"; exit 3; }
declare -A EA=([whole]=-0.13 [roof]=0.40 [gutter]=0.42 [base]=0.30)
for c in whole roof gutter base; do
  "$B" -b rounds/k01.blend -P scripts/render_views.py -- --cams CP014_drain_${c}_start --outdir "$OUT" --res 1280x720 \
    --samples "$S" --era 1850 --tod studio --threads 8 --exposure "${EA[$c]}" 2>&1 | grep -E "WROTE|Error" || true
done
echo "done: $OUT/CP014_drain_{whole,roof,gutter,base}_start.png"
