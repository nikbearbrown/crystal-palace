#!/usr/bin/env bash
# CP020 nave CANDIDATE regression preview (2026-11-11): the other f03 cams with live renders, live f03 vs candidate, same recipe both sides
# (people v3.3 wrapper, --keep-lighting at the blend exposure, 960x540, 16 spp: a change map, NOT the live recipes) -> /workspace/tmp/cp020/regress/{live,cand}
# Since the KEEP (2026-11-11) "live" here means the pre-keep pin; the keep regression is scripts/regress_cp020_nave_keep.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; R=/workspace/tmp/cp020/regress
for side in live cand; do
  f=rounds/f03.blend.pre_cp020nave_keep; [[ $side == cand ]] && f=rounds/candidates/f03_cp020nave.blend
  mkdir -p $R/$side
  "$B" -b $f -P scripts/render_views_ppl33.py -- --cams CP018_paint_start,CP018_cradle_start,CP019_doors_start,CP019_dray_start --res 960x540 --samples 16 --keep-lighting --threads 8 --outdir $R/$side
done
echo REGRESS_DONE
