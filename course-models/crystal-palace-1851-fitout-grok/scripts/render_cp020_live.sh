#!/usr/bin/env bash
# CP020 LIVE (KEEP 2026-11-11: nave FT60-FT66). Renders live rounds/f03.blend -> renders/f03/CP020_floor_start.png with the exact
# live recipe (render_views_ppl33.py = people_lib v3.3 from survey d19449b, --keep-lighting, 1280x720, 24 spp, exposure -1.768),
# so the live frame matches renders/candidates/cp020_nave_20261111/after/CP020_floor_start.png.
#   scripts/render_cp020_live.sh [--rebuild] [--no-render]
# --rebuild regenerates live f03 from the pre-keep f03 pinned at rounds/f03.blend.pre_cp020nave_keep (md5 18d4107f, = f03 as built
# by build_transept.py --state fitout on Oct 27) by running scripts/cand_cp020_nave_20261111.py on it (the script that built the KEEP
# candidate). THIS is the f03 rebuild path: a bare build_transept.py --state fitout rebuild has no nave; follow it with this script
# (cand_cp020_nave_20261111.py --src <fresh f03> --out <tmp>; mv) or the CP020 KEEP is lost.
# CP018/CP019 keep their own recipes: scripts/render_f03_others_live.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
PRE=rounds/f03.blend.pre_cp020nave_keep
P33=/workspace/tmp/cp020/ppl33
if [[ ! -f $P33/people_lib.py ]]; then mkdir -p $P33; git -C /workspace/crystal-palace-survey show d19449b:people/people_lib.py > $P33/people_lib.py; ln -sfn /workspace/crystal-palace-survey/people/vendor $P33/vendor; ln -sfn /workspace/crystal-palace-survey/people/v3 $P33/v3; fi
REBUILD=0; RENDER=1
for a in "$@"; do case "$a" in --rebuild) REBUILD=1;; --no-render) RENDER=0;; esac; done
if [[ $REBUILD == 1 ]]; then
  TMP=$(mktemp -d)
  "$B" -b -P scripts/cand_cp020_nave_20261111.py -- --src "$PRE" --out "$TMP/f03.blend"
  mv "$TMP/f03.blend" rounds/f03.blend
  rm -rf "$TMP"
fi
if [[ $RENDER == 1 ]]; then
  "$B" -b rounds/f03.blend -P scripts/render_views_ppl33.py -- --cams CP020_floor_start --res 1280x720 --samples 24 --keep-lighting --threads 8 --exposure -1.768 --outdir renders/f03
  echo "CP020_LIVE_DONE: renders/f03/CP020_floor_start.png"
fi
