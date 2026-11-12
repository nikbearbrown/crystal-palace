#!/usr/bin/env bash
# CP018 east-nave CANDIDATE renders (2026-11-12, DEPARTURES FT88-FT94). NOT live.
#   nohup scripts/render_cp018_east.sh [--no-build] > /workspace/logs/cp018_east_render.log 2>&1 &
# Builds rounds/candidates/f03_cp018east.blend from live rounds/f03.blend (never written) with scripts/cand_cp018_east_20261112.py
# (skipped if the candidate exists or --no-build), then renders before (live f03) and after (candidate), SAME recipe per camera (FT94),
# all 1920x1080, 48 spp:
#   CP018_paint_start (hero), CP018_paint_end (side effect): the live CP018_paint recipe, scripts/render_f03_others_live.sh "rv2" set
#       (fitout scripts 387a34c + people_lib 2.0 survey dab5204 + look survey 0008c1c; exposure/look from the blend era, same both sides)
#   CP019_dray_start (side effect): the live dray recipe, fitout scripts da494a9 (no people pass)
#   CP020_floor_start (side effect): the live CP020 recipe (render_views_ppl33.py, people_lib v3.3, --keep-lighting, exposure -1.768)
# RESUMABLE: every PNG that already exists is skipped; each render goes to a scratch dir and is moved in only when complete
# (the box is snapshotted/restored about every two hours, which kills long renders). Just re-run the same command.
# Output renders/candidates/cp018_east_20261112/{before,after}/ ; done marker renders/candidates/cp018_east_20261112/DONE
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; K=/workspace/tmp/cp020keep
SRC=rounds/f03.blend; CAND=rounds/candidates/f03_cp018east.blend
OUT=renders/candidates/cp018_east_20261112
BUILD=1; for a in "$@"; do case "$a" in --no-build) BUILD=0;; esac; done
mkdir -p $OUT/before $OUT/after
if [[ ! -f $K/rv2/wrap.py || ! -f $K/rda494a9/wrap.py ]]; then echo "MISSING $K recipe sets: run scripts/render_f03_others_live.sh once (it rebuilds them)"; exit 2; fi
if [[ $BUILD == 1 && ! -f $CAND ]]; then "$B" -b -P scripts/cand_cp018_east_20261112.py -- --src $SRC --out $CAND; fi
[[ -f $CAND ]] || { echo "no candidate blend"; exit 3; }
R() { # side cam recipe
  local side=$1 cam=$2 rec=$3 f=$CAND; [[ $side == before ]] && f=$SRC
  local dst=$OUT/$side/$cam.png
  if [[ -f $dst ]]; then echo "CP018_EAST_SKIP $side $cam (exists)"; return; fi
  local T=/workspace/tmp/cp018/scratch_${side}_$cam; rm -rf $T; mkdir -p $T
  case $rec in
    rv2) "$B" -b $f -P $K/rv2/wrap.py -- --cams $cam --res 1920x1080 --samples 48 --outdir $T ;;
    rda) "$B" -b $f -P $K/rda494a9/wrap.py -- --cams $cam --res 1920x1080 --samples 48 --outdir $T ;;
    p33) "$B" -b $f -P scripts/render_views_ppl33.py -- --cams $cam --res 1920x1080 --samples 48 --keep-lighting --threads 8 --exposure -1.768 --outdir $T ;;
  esac
  mv $T/$cam.png $dst; rm -rf $T
  echo "CP018_EAST_STEP $side $cam $(date -u +%H:%M:%S)"
}
for side in after before; do R $side CP018_paint_start rv2; done
for side in after before; do R $side CP019_dray_start rda; done
for side in after before; do R $side CP018_paint_end rv2; done
for side in after before; do R $side CP020_floor_start p33; done
md5sum $SRC $CAND > $OUT/md5.txt
date -u > $OUT/DONE
echo CP018_EAST_DONE
