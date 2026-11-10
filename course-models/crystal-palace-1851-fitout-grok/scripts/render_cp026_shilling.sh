#!/usr/bin/env bash
# CP026 shilling CANDIDATE (2026-11-10, FT55-FT57, FT59). NOT live.
#   scripts/render_cp026_shilling.sh [--no-build]
# before = live renders/h03/CP026_shilling_ext_start.png (reproduced by this recipe from live h03: max diff 8, mean 0.0005)
# recipe = the live one: 1280x720, 24 spp, look v1.1 era 1851 tod exterior_midday, people_lib v3.1 (survey 0dfacfa) via
# scripts/render_views_ppl31.py (needs /workspace/tmp/cp026/ppl31/people_lib.py = `git -C /workspace/crystal-palace-survey show 0dfacfa:people/people_lib.py`
# with vendor -> survey people/vendor). After exposure override -0.76 (live blend -0.7) for luma match.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
OUT=renders/candidates/cp026_shilling_20261110
P31=/workspace/tmp/cp026/ppl31
if [[ ! -f $P31/people_lib.py ]]; then mkdir -p $P31; git -C /workspace/crystal-palace-survey show 0dfacfa:people/people_lib.py > $P31/people_lib.py; ln -sfn /workspace/crystal-palace-survey/people/vendor $P31/vendor; fi
sed -i "s#/workspace/tmp/cp026/ppl31/people_lib.py#$P31/people_lib.py#" scripts/render_views_ppl31.py
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b -P scripts/cand_cp026_shilling_20261110.py -- --src rounds/h03.blend --out rounds/candidates/h03_cp026shilling.blend
fi
mkdir -p $OUT/after
"$B" -b rounds/candidates/h03_cp026shilling.blend -P scripts/render_views_ppl31.py -- --cams CP026_shilling_ext_start --res 1280x720 --samples 24 --era 1851 --tod exterior_midday --threads 8 --exposure -0.76 --outdir $OUT/after
echo CP026_SHILLING_DONE
