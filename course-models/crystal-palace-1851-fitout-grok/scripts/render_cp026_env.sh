#!/usr/bin/env bash
# CP026 env CANDIDATE (2026-11-10, FT56/FT56b, FT57, FT59; no FT55). NOT live.
#   scripts/render_cp026_env.sh [--no-build] [exposure]   (default exposure -0.7 = live blend value)
# Live recipe exactly: 1280x720, 24 spp, look v1.1 era 1851 exterior_midday, people_lib v3.1 (survey 0dfacfa) via
# scripts/render_views_ppl31.py, so the live figures render as in renders/h03/CP026_shilling_ext_start.png.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
OUT=renders/candidates/cp026_env_20261110
P31=/workspace/tmp/cp026/ppl31
if [[ ! -f $P31/people_lib.py ]]; then mkdir -p $P31; git -C /workspace/crystal-palace-survey show 0dfacfa:people/people_lib.py > $P31/people_lib.py; ln -sfn /workspace/crystal-palace-survey/people/vendor $P31/vendor; ln -sfn /workspace/crystal-palace-survey/people/v3 $P31/v3; fi
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b -P scripts/cand_cp026_env_20261110.py -- --src rounds/h03.blend --out rounds/candidates/h03_cp026env.blend
else shift; fi
EXP=${1:--0.7}
mkdir -p $OUT/after
"$B" -b rounds/candidates/h03_cp026env.blend -P scripts/render_views_ppl31.py -- --cams CP026_shilling_ext_start --res 1280x720 --samples 24 --era 1851 --tod exterior_midday --threads 8 --exposure $EXP --outdir $OUT/after
echo CP026_ENV_DONE
