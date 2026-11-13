#!/usr/bin/env bash
# CP026 turnstiles CANDIDATE renders (2026-11-13, DEPARTURES FT95-FT100). NOT live.
#   nohup scripts/render_cp026_turnstiles.sh [--no-build] > /workspace/tmp/cp026cand/render.log 2>&1 &
# Builds rounds/candidates/h03_cp026turnstiles.blend from live rounds/h03.blend (never written) with
# scripts/cand_cp026_turnstiles_20261113.py (skipped if the candidate exists or --no-build), then renders before (live h03) and
# after (candidate), SAME recipe per camera both sides (FT100), all 1920x1080, 48 spp:
#   CP026_turnstiles_start (hero), CP026_shilling_ext_start (side effect): the live CP026 recipe, scripts/render_views_ppl31.py
#       (people_lib v3.1 survey 0dfacfa), look era 1851 tod exterior_midday, exposure -0.7 (scripts/render_cp026_live.sh,
#       scripts/regress_cp026_env_keep.sh)
#   CP028_watering_start (side effect): render_views_ppl31.py, era 1851, default tod interior_daylit (regress_cp026_env_keep.sh)
#   CP028_louvre_start (side effect): render_views.py --no-people --keep-lighting (scripts/render_cp028_live.sh)
# RESUMABLE: every PNG that already exists is skipped; each render goes to a scratch dir and is moved in only when complete
# (box snapshot/restore kills long renders). Just re-run the same command. Progress: /workspace/tmp/cp026cand/PROGRESS.md
# Output renders/candidates/cp026_turnstiles_20261113/{before,after}/ ; done marker .../DONE ; ALL_DONE logged in PROGRESS.md
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
SRC=rounds/h03.blend; CAND=rounds/candidates/h03_cp026turnstiles.blend
OUT=renders/candidates/cp026_turnstiles_20261113; PG=/workspace/tmp/cp026cand/PROGRESS.md
P31=/workspace/tmp/cp026/ppl31
if [[ ! -f $P31/people_lib.py ]]; then mkdir -p $P31; git -C /workspace/crystal-palace-survey show 0dfacfa:people/people_lib.py > $P31/people_lib.py; ln -sfn /workspace/crystal-palace-survey/people/vendor $P31/vendor; ln -sfn /workspace/crystal-palace-survey/people/v3 $P31/v3; fi
BUILD=1; for a in "$@"; do case "$a" in --no-build) BUILD=0;; esac; done
mkdir -p $OUT/before $OUT/after
log() { echo "- $(date -u +%FT%TZ) $*" >> $PG; echo "$*"; }
if [[ $BUILD == 1 && ! -f $CAND ]]; then "$B" -b -P scripts/cand_cp026_turnstiles_20261113.py -- --src $SRC --out $CAND; log "built $CAND"; fi
[[ -f $CAND ]] || { echo "no candidate blend"; exit 3; }
R() {
  local side=$1 cam=$2 rec=$3 f=$CAND; [[ $side == before ]] && f=$SRC
  local dst=$OUT/$side/$cam.png
  if [[ -f $dst ]]; then echo "CP026T_SKIP $side $cam (exists)"; return; fi
  local T=/workspace/tmp/cp026cand/scratch_${side}_$cam; rm -rf $T; mkdir -p $T
  case $rec in
    ext) "$B" -b $f -P scripts/render_views_ppl31.py -- --cams $cam --res 1920x1080 --samples 48 --era 1851 --tod exterior_midday --threads 8 --exposure -0.7 --outdir $T ;;
    int) "$B" -b $f -P scripts/render_views_ppl31.py -- --cams $cam --res 1920x1080 --samples 48 --era 1851 --threads 8 --outdir $T ;;
    lou) "$B" -b $f -P scripts/render_views.py -- --cams $cam --res 1920x1080 --samples 48 --no-people --keep-lighting --threads 8 --outdir $T ;;
  esac
  mv $T/$cam.png $dst; rm -rf $T
  log "CP026T_STEP $side $cam"
}
for side in after before; do R $side CP026_turnstiles_start ext; done
for side in after before; do R $side CP026_shilling_ext_start ext; done
for side in after before; do R $side CP028_watering_start int; done
for side in after before; do R $side CP028_louvre_start lou; done
md5sum $SRC $CAND > $OUT/md5.txt
date -u > $OUT/DONE
log "ALL_DONE renders (8/8) in $OUT"
echo CP026T_DONE
