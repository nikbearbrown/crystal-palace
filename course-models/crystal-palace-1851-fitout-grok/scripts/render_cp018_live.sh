#!/usr/bin/env bash
# CP018 LIVE (KEEP scoped 2026-11-12: east nave FT88-FT94, CP018_paint_start (hero) + CP018_paint_end). Live blend rounds/f04.blend
# (= approved candidate rounds/candidates/f03_cp018east.blend, md5 5d238d1c1a1f811b42fd544093f51937). Routing:
# scripts/fitout_live_heroes.json. Only CP018_paint_start and CP018_paint_end render from f04. rounds/f03.blend (md5
# 3e80da59b1cf3bb3cf133d15edcc69e9) is never written and stays live for every other f03 camera (CP020_floor_start: side effect
# REJECTED, only darker; CP019_dray_start: no visible change; CP018_cradle_start, CP019_doors_start untouched). rounds/f01.blend and
# its PNGs are never written; renders/f01/CP018_paint_end.png and renders/f03/CP018_paint_start.png stay as the pre-keep frames.
#   scripts/render_cp018_live.sh [--rebuild] [--no-render] [--force] [--blend PATH] [--outdir DIR]
# Recipe (FT94, the live CP018_paint recipe): the "rv2" set (fitout scripts 387a34c + people_lib 2.0 survey dab5204 + look survey
# 0008c1c; exposure/look from the blend era), rebuilt from git under /workspace/tmp/cp020keep/rv2 if missing; 1920x1080, 48 spp.
# Output matches renders/candidates/cp018_east_20261112/after/CP018_paint_{start,end}.png pixel for pixel.
# --rebuild regenerates the blend from live f03 (pre-keep, unchanged) with scripts/cand_cp018_east_20261112.py, the script that
# built the KEEP candidate (md5 differs per save by metadata only). If f03 is ever rebuilt, follow with this --rebuild or the CP018
# KEEP is lost.
# RESUMABLE (the box is snapshotted/restored about every two hours): an existing --blend is not rebuilt and an existing PNG is not
# re-rendered unless --force; the rebuild and each render go to a scratch dir and are moved in only when complete. Just re-run.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; K=/workspace/tmp/cp020keep
SRC=rounds/f03.blend
BLEND=rounds/f04.blend
OUTDIR=renders/f04
REBUILD=0; RENDER=1; FORCE=0
while [[ $# -gt 0 ]]; do case "$1" in
  --rebuild) REBUILD=1;; --no-render) RENDER=0;; --force) FORCE=1;;
  --blend) BLEND="$2"; shift;; --outdir) OUTDIR="$2"; shift;;
esac; shift; done
if [[ $REBUILD == 1 ]]; then
  if [[ -f "$BLEND" && $FORCE == 0 ]]; then echo "CP018_LIVE_SKIP rebuild ($BLEND exists)"; else
    TMP=$(mktemp -d /workspace/tmp/cp018rebuild.XXXXXX)
    "$B" -b -P scripts/cand_cp018_east_20261112.py -- --src "$SRC" --out "$TMP/f04_rebuild.blend"
    mv "$TMP/f04_rebuild.blend" "$BLEND"
    rm -rf "$TMP"
    echo "CP018_LIVE_REBUILT: $BLEND"
  fi
fi
if [[ $RENDER == 1 ]]; then
  if [[ ! -f $K/rv2/wrap.py ]]; then  # recreate the pinned rv2 recipe set (same as scripts/render_f03_others_live.sh)
    G=/workspace/crystal-palace-fitout; SV=/workspace/crystal-palace-survey; S=course-models/crystal-palace-1851-fitout-grok/scripts; d=$K/rv2
    mkdir -p $d
    for f in $(git -C $G ls-tree --name-only 387a34c $S/ | grep '\.py$\|\.sh$'); do git -C $G show 387a34c:$f > $d/$(basename $f); done
    ln -sfn $SV/people/v3 $d/v3; ln -sfn $SV/people/vendor $d/vendor
    git -C $SV show dab5204:people/people_lib.py > $d/people_lib.py
    git -C $SV show 0008c1c:look/crystal_palace_look.py > $d/crystal_palace_look.py
    echo 'from people_lib import swap_scene_people, PEOPLE_VERSION  # pinned survey dab5204 (people 2.0)' > $d/cpl_people.py
    echo 'from crystal_palace_look import LOOK_VERSION, apply_look, era_for_scene, tod_for_scene, clamp_materials, EXPOSURE, ERA_SUN_RGB, SUN  # pinned survey 0fb0f79' > $d/cpl_look.py
    printf 'import sys\nD = "%s"\nsys.path.insert(0, D)\nRV = D + "/render_views.py"\nexec(compile(open(RV).read(), RV, "exec"), {"__name__": "__main__", "__file__": RV})\n' "$d" > $d/wrap.py
  fi
  mkdir -p "$OUTDIR"
  for cam in CP018_paint_start CP018_paint_end; do
    if [[ -f "$OUTDIR/$cam.png" && $FORCE == 0 ]]; then echo "CP018_LIVE_SKIP $OUTDIR/$cam.png (exists)"; continue; fi
    S=$(mktemp -d /workspace/tmp/cp018render.XXXXXX)
    "$B" -b "$BLEND" -P $K/rv2/wrap.py -- --cams "$cam" --res 1920x1080 --samples 48 --outdir "$S"
    mv "$S/$cam.png" "$OUTDIR/$cam.png"; rm -rf "$S"
    echo "CP018_LIVE_STEP: $OUTDIR/$cam.png"
  done
  echo "CP018_LIVE_DONE: $OUTDIR"
fi
