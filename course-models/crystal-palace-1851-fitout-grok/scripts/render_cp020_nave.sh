#!/usr/bin/env bash
# CP020 nave CANDIDATE (2026-11-11, FT60-FT66). KEPT 2026-11-11 and now live (live path: scripts/render_cp020_live.sh [--rebuild]).
# Since the KEEP, rounds/f03.blend already contains the nave, so the build and --before render use the pre-keep pin
# rounds/f03.blend.pre_cp020nave_keep (md5 18d4107f), never live f03 (running the nave script on live f03 would double the nave).
#   scripts/render_cp020_nave.sh [--no-build] [--before] [exposure]   (default exposure -1.768 = live frame's value)
# Live recipe for renders/f03/CP020_floor_start.png (Oct 27 06:46, people v3.3 pass): render_views.py with people_lib 3.3
# (survey d19449b) via scripts/render_views_ppl33.py, --keep-lighting, 1280x720, 24 spp, exposure -1.768. Re-rendering live
# f03 this way gives max diff 1/255, mean 0.05, luma 128.75 vs 128.76 (the live PNG's exposure was not logged; -1.768 was
# found by search; blend exposure is -0.7). The current people_lib 3.4 skips the close-up figures, so a plain re-render is NOT the live frame.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
OUT=renders/candidates/cp020_nave_20261111
P33=/workspace/tmp/cp020/ppl33
if [[ ! -f $P33/people_lib.py ]]; then mkdir -p $P33; git -C /workspace/crystal-palace-survey show d19449b:people/people_lib.py > $P33/people_lib.py; ln -sfn /workspace/crystal-palace-survey/people/vendor $P33/vendor; ln -sfn /workspace/crystal-palace-survey/people/v3 $P33/v3; fi
BUILD=1; BEFORE=0
while [[ "${1:-}" == --* ]]; do case "$1" in --no-build) BUILD=0;; --before) BEFORE=1;; esac; shift; done
EXP=${1:--1.768}
if [[ $BUILD == 1 ]]; then "$B" -b -P scripts/cand_cp020_nave_20261111.py -- --src rounds/f03.blend.pre_cp020nave_keep --out rounds/candidates/f03_cp020nave.blend; fi
R="--cams CP020_floor_start --res 1280x720 --samples 24 --keep-lighting --threads 8 --exposure $EXP"
if [[ $BEFORE == 1 ]]; then mkdir -p $OUT/before_rerender; "$B" -b rounds/f03.blend.pre_cp020nave_keep -P scripts/render_views_ppl33.py -- $R --outdir $OUT/before_rerender; fi
mkdir -p $OUT/after
"$B" -b rounds/candidates/f03_cp020nave.blend -P scripts/render_views_ppl33.py -- $R --outdir $OUT/after
echo CP020_NAVE_DONE
