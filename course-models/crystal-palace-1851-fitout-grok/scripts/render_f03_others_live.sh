#!/usr/bin/env bash
# f03 non-CP020 cams at their live recipes (2026-11-11, CP020 nave KEEP regression). Recreates the two historical script sets from git
# under /workspace/tmp/cp020keep/{rda494a9,rv2} (scratch, rebuilt if missing) and renders 1280x720, 48 spp, look applied by the blend era:
#   CP018_cradle_start, CP019_dray_start : fitout scripts at da494a9 (no people pass)       -> re-render of pre-keep f03 = live PNG, max diff 0
#   CP018_paint_start,  CP019_doors_start: fitout scripts at 387a34c + people_lib 2.0 (survey dab5204) + look survey 0008c1c
#                                          -> re-render of pre-keep f03 vs live PNG max 53/67, mean 2.3/1.2 (people placement noise; close, not exact)
#   scripts/render_f03_others_live.sh <blend> <outdir>
# Default blend rounds/f03.blend. Compare the two sides with the SAME recipe; do not chase pixel-exact paint/doors repro (that stalled the first KEEP attempt).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; F=${1:-rounds/f03.blend}; OUT=${2:-/workspace/tmp/cp020keep/others}
K=/workspace/tmp/cp020keep; S=course-models/crystal-palace-1851-fitout-grok/scripts; G=/workspace/crystal-palace-fitout; SV=/workspace/crystal-palace-survey
mk() { # dir commit
  local d=$1 c=$2; [[ -f $d/wrap.py ]] && return; mkdir -p $d
  for f in $(git -C $G ls-tree --name-only $c $S/ | grep '\.py$\|\.sh$'); do git -C $G show $c:$f > $d/$(basename $f); done
  ln -sfn $SV/people/v3 $d/v3; ln -sfn $SV/people/vendor $d/vendor
  printf 'import sys\nD = "%s"\nsys.path.insert(0, D)\nRV = D + "/render_views.py"\nexec(compile(open(RV).read(), RV, "exec"), {"__name__": "__main__", "__file__": RV})\n' "$d" > $d/wrap.py
}
mk $K/rda494a9 da494a9
if [[ ! -f $K/rv2/wrap.py ]]; then
  mk $K/rv2 387a34c
  git -C $SV show dab5204:people/people_lib.py > $K/rv2/people_lib.py
  git -C $SV show 0008c1c:look/crystal_palace_look.py > $K/rv2/crystal_palace_look.py
  echo 'from people_lib import swap_scene_people, PEOPLE_VERSION  # pinned survey dab5204 (people 2.0)' > $K/rv2/cpl_people.py
  echo 'from crystal_palace_look import LOOK_VERSION, apply_look, era_for_scene, tod_for_scene, clamp_materials, EXPOSURE, ERA_SUN_RGB, SUN  # pinned survey 0fb0f79' > $K/rv2/cpl_look.py
fi
mkdir -p $OUT
"$B" -b $F -P $K/rda494a9/wrap.py -- --cams CP018_cradle_start,CP019_dray_start --res 1280x720 --samples 48 --outdir $OUT
"$B" -b $F -P $K/rv2/wrap.py -- --cams CP018_paint_start,CP019_doors_start --res 1280x720 --samples 48 --outdir $OUT
echo "F03_OTHERS_DONE $OUT"
