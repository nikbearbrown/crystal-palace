#!/usr/bin/env bash
# CP019 cases CANDIDATE renders (2026-11-16, DEPARTURES FT101-FT108). NOT live.
#   nohup scripts/render_cp019_cases.sh [--no-build] > /workspace/logs/cp019_cases_render.log 2>&1 &
# Builds rounds/candidates/f03_cp019cases.blend from live rounds/f03.blend (never written) with scripts/cand_cp019_cases_20261116.py
# (skipped if the candidate exists or --no-build), then renders before (live f03) and after (candidate), SAME recipe per camera (FT107),
# all 1920x1080, 48 spp:
#   CP019_doors_start (hero): the live CP019_doors recipe, scripts/render_f03_others_live.sh "rv2" set
#       (fitout scripts 387a34c + people_lib 2.0 survey dab5204 + look survey 0008c1c; exposure/look from the blend era, same both sides)
#   CP019_dray_start (side effect): the live dray recipe, fitout scripts da494a9 (no people pass)
# CP018_cradle_start and CP020_floor_start (the other f03 cams) changed by noise only in a 480x270 test (max diff 10 / 18, 0 px > 20): not rendered.
# RESUMABLE: existing PNGs are skipped; each render goes to a scratch dir and is moved in only when complete.
# Output renders/candidates/cp019_cases_20261116/{before,after}/ ; done marker renders/candidates/cp019_cases_20261116/DONE
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; K=/workspace/tmp/cp020keep
SRC=rounds/f03.blend; CAND=rounds/candidates/f03_cp019cases.blend
OUT=renders/candidates/cp019_cases_20261116
BUILD=1; for a in "$@"; do case "$a" in --no-build) BUILD=0;; esac; done
mkdir -p $OUT/before $OUT/after
if [[ ! -f $K/rv2/wrap.py || ! -f $K/rda494a9/wrap.py ]]; then echo "MISSING $K recipe sets: run scripts/render_f03_others_live.sh once (it rebuilds them)"; exit 2; fi
if [[ $BUILD == 1 && ! -f $CAND ]]; then python3 scripts/make_cp019_stencils.py; "$B" -b -P scripts/cand_cp019_cases_20261116.py -- --src $SRC --out $CAND; fi
[[ -f $CAND ]] || { echo "no candidate blend"; exit 3; }
R() { # side cam recipe
  local side=$1 cam=$2 rec=$3 f=$CAND; [[ $side == before ]] && f=$SRC
  local dst=$OUT/$side/$cam.png
  if [[ -f $dst ]]; then echo "CP019_CASES_SKIP $side $cam (exists)"; return; fi
  local T=/workspace/tmp/cp019/scratch_${side}_$cam; rm -rf $T; mkdir -p $T
  case $rec in
    rv2) "$B" -b $f -P $K/rv2/wrap.py -- --cams $cam --res 1920x1080 --samples 48 --outdir $T ;;
    rda) "$B" -b $f -P $K/rda494a9/wrap.py -- --cams $cam --res 1920x1080 --samples 48 --outdir $T ;;
  esac
  mv $T/$cam.png $dst; rm -rf $T
  echo "CP019_CASES_STEP $side $cam $(date -u +%H:%M:%S)"
}
for side in after before; do R $side CP019_doors_start rv2; done
for side in after before; do R $side CP019_dray_start rda; done
md5sum $SRC $CAND > $OUT/md5.txt
date -u > $OUT/DONE
echo CP019_CASES_DONE
