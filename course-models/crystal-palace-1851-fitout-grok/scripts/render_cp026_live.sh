#!/usr/bin/env bash
# CP026 LIVE (KEEP 2026-11-10: environment-only polish FT56/FT56b, FT57, FT59; no FT55). Renders live rounds/h03.blend ->
# renders/h03/CP026_shilling_ext_start.png with the exact live recipe (render_views_ppl31.py = people_lib v3.1 from survey 0dfacfa,
# 1280x720, 24 spp, look v1.1 era 1851 exterior_midday, exposure -0.7), so the live frame matches
# renders/candidates/cp026_env_20261110/after/CP026_shilling_ext_start.png.
#   scripts/render_cp026_live.sh [--rebuild]
# --rebuild regenerates live h03 from the pre-keep h03 pinned at rounds/h03.blend.pre_cp026env_keep (md5 df1e46cf, = h03 after the
# CP028 v2 KEEP) by running scripts/cand_cp026_env_20261110.py on it (the same script that built the KEEP candidate).
# CP028_louvre_start keeps its own recipe: scripts/render_cp028_live.sh (without --rebuild!).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
PRE=rounds/h03.blend.pre_cp026env_keep
P31=/workspace/tmp/cp026/ppl31
if [[ ! -f $P31/people_lib.py ]]; then mkdir -p $P31; git -C /workspace/crystal-palace-survey show 0dfacfa:people/people_lib.py > $P31/people_lib.py; ln -sfn /workspace/crystal-palace-survey/people/vendor $P31/vendor; ln -sfn /workspace/crystal-palace-survey/people/v3 $P31/v3; fi
if [[ "${1:-}" == "--rebuild" ]]; then
  TMP=$(mktemp -d)
  "$B" -b -P scripts/cand_cp026_env_20261110.py -- --src "$PRE" --out "$TMP/h03.blend"
  mv "$TMP/h03.blend" rounds/h03.blend
  rm -rf "$TMP"
fi
"$B" -b rounds/h03.blend -P scripts/render_views_ppl31.py -- --cams CP026_shilling_ext_start --res 1280x720 --samples 24 --era 1851 --tod exterior_midday --threads 8 --exposure -0.7 --outdir renders/h03
echo "CP026_LIVE_DONE: renders/h03/CP026_shilling_ext_start.png"
