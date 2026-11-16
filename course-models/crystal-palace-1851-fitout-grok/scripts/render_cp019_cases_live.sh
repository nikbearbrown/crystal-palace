#!/usr/bin/env bash
# CP019 cases LIVE (KEEP scoped 2026-11-16: south-door packing cases, bales, opened sculpture case, flywheel, queued dray, consignment
# marks, bare Kensington Road elms, FT101-FT108; CP019_doors_start ONLY).
# Live blend rounds/f04_cp019cases.blend (= approved candidate rounds/candidates/f03_cp019cases.blend, md5 8dc7a27ae8e79870b2b1189209f04aa5).
# (Named f04_cp019cases, not f04: rounds/f04.blend is already the live CP018 east-nave blend, 5d238d1c, and must not be overwritten.)
# Routing: scripts/fitout_live_heroes.json. ONLY CP019_doors_start renders from f04_cp019cases. rounds/f03.blend (md5
# 3e80da59b1cf3bb3cf133d15edcc69e9) is never written and stays live for every other f03 camera: CP019_dray_start (side effect NOT
# promoted: noise-level change, luma 204.37->204.21), CP018_cradle_start, CP020_floor_start.
# renders/f03/CP019_doors_start.png stays in place as the pre-keep frame.
#   scripts/render_cp019_cases_live.sh [--rebuild] [--no-render] [--force] [--blend PATH] [--outdir DIR]
# Recipe (FT107, the live CP019_doors recipe, "rv2" set of scripts/render_f03_others_live.sh): fitout scripts 387a34c + people_lib 2.0
# (survey dab5204) + look survey 0008c1c, look/exposure from the blend era, 1920x1080, 48 spp. Output matches
# renders/candidates/cp019_cases_20261116/after/CP019_doors_start.png.
# --rebuild regenerates the blend from live f03 (unchanged) with scripts/cand_cp019_cases_20261116.py, the script that built the KEEP
# candidate (md5 differs per save by metadata only). If f03 is ever rebuilt, follow with this --rebuild or the CP019 cases KEEP is lost.
# RESUMABLE: an existing --blend is not rebuilt and an existing PNG is not re-rendered unless --force; the rebuild and the render go
# to a scratch dir and are moved in only when complete. Just re-run.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
SRC=rounds/f03.blend
BLEND=rounds/f04_cp019cases.blend
OUTDIR=renders/f04_cp019cases
CAM=CP019_doors_start
REBUILD=0; RENDER=1; FORCE=0
while [[ $# -gt 0 ]]; do case "$1" in
  --rebuild) REBUILD=1;; --no-render) RENDER=0;; --force) FORCE=1;;
  --blend) BLEND="$2"; shift;; --outdir) OUTDIR="$2"; shift;;
esac; shift; done
K=/workspace/tmp/cp020keep
if [[ ! -f $K/rv2/wrap.py ]]; then   # same pinned set as scripts/render_f03_others_live.sh (scratch, rebuilt if missing)
  G=/workspace/crystal-palace-fitout; SV=/workspace/crystal-palace-survey; S=course-models/crystal-palace-1851-fitout-grok/scripts; d=$K/rv2
  mkdir -p $d
  for f in $(git -C $G ls-tree --name-only 387a34c $S/ | grep '\.py$\|\.sh$'); do git -C $G show 387a34c:$f > $d/$(basename $f); done
  ln -sfn $SV/people/v3 $d/v3; ln -sfn $SV/people/vendor $d/vendor
  printf 'import sys\nD = "%s"\nsys.path.insert(0, D)\nRV = D + "/render_views.py"\nexec(compile(open(RV).read(), RV, "exec"), {"__name__": "__main__", "__file__": RV})\n' "$d" > $d/wrap.py
  git -C $SV show dab5204:people/people_lib.py > $d/people_lib.py
  git -C $SV show 0008c1c:look/crystal_palace_look.py > $d/crystal_palace_look.py
  echo 'from people_lib import swap_scene_people, PEOPLE_VERSION  # pinned survey dab5204 (people 2.0)' > $d/cpl_people.py
  echo 'from crystal_palace_look import LOOK_VERSION, apply_look, era_for_scene, tod_for_scene, clamp_materials, EXPOSURE, ERA_SUN_RGB, SUN  # pinned survey 0fb0f79' > $d/cpl_look.py
fi
if [[ $REBUILD == 1 ]]; then
  if [[ -f "$BLEND" && $FORCE == 0 ]]; then echo "CP019C_LIVE_SKIP rebuild ($BLEND exists)"; else
    TMP=$(mktemp -d /workspace/tmp/cp019crebuild.XXXXXX); mkdir -p "$TMP/rounds/candidates"   # the build script only writes under */rounds/candidates/
    python3 scripts/make_cp019_stencils.py
    "$B" -b -P scripts/cand_cp019_cases_20261116.py -- --src "$SRC" --out "$TMP/rounds/candidates/f04_cp019cases_rebuild.blend"
    mv "$TMP/rounds/candidates/f04_cp019cases_rebuild.blend" "$BLEND"
    rm -rf "$TMP"
    echo "CP019C_LIVE_REBUILT: $BLEND"
  fi
fi
if [[ $RENDER == 1 ]]; then
  mkdir -p "$OUTDIR"
  if [[ -f "$OUTDIR/$CAM.png" && $FORCE == 0 ]]; then echo "CP019C_LIVE_SKIP $OUTDIR/$CAM.png (exists)"; else
    T=$(mktemp -d /workspace/tmp/cp019crender.XXXXXX)
    "$B" -b "$BLEND" -P $K/rv2/wrap.py -- --cams $CAM --res 1920x1080 --samples 48 --outdir "$T"
    mv "$T/$CAM.png" "$OUTDIR/$CAM.png"; rm -rf "$T"
    echo "CP019C_LIVE_STEP: $OUTDIR/$CAM.png"
  fi
  echo "CP019C_LIVE_DONE: $OUTDIR"
fi
