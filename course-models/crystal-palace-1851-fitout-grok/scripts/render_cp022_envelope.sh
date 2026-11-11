#!/usr/bin/env bash
# CP022 envelope CANDIDATE (2026-11-11, FT67-FT73). NOT live, no verdict. Live rounds/o01.blend is never written.
#   scripts/render_cp022_envelope.sh [--no-build] [--no-before]
# Recipe (FT73): render_views.py with people_lib 3.3 (survey d19449b) via scripts/render_views_ppl33.py, --keep-lighting
# (blend exposure -0.7, AgX MHC), 1280x720, 48 spp, same live cameras for before (live o01) and after (candidate).
# Live renders/o01/CP022_fountain_start.png (Oct 27 08:24) re-rendered this way: structure identical, people differ
# (max 246, mean 2.13, luma 146.75 vs 146.72); so before = live o01 re-rendered with the identical recipe.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
OUT=renders/candidates/cp022_envelope_20261111
P33=/workspace/tmp/cp020/ppl33
if [[ ! -f $P33/people_lib.py ]]; then mkdir -p $P33; git -C /workspace/crystal-palace-survey show d19449b:people/people_lib.py > $P33/people_lib.py; ln -sfn /workspace/crystal-palace-survey/people/vendor $P33/vendor; ln -sfn /workspace/crystal-palace-survey/people/v3 $P33/v3; fi
BUILD=1; BEFORE=1
while [[ "${1:-}" == --* ]]; do case "$1" in --no-build) BUILD=0;; --no-before) BEFORE=0;; esac; shift; done
if [[ $BUILD == 1 ]]; then "$B" -b -P scripts/cand_cp022_envelope_20261111.py -- --src rounds/o01.blend --out rounds/candidates/o01_cp022envelope.blend; fi
CAMS=CP022_fountain_start,CP021_doors_start,CP021_dais_start,CP022_crossing_start
R="--cams $CAMS --res 1280x720 --samples 48 --keep-lighting --threads 8"
mkdir -p $OUT/after
"$B" -b rounds/candidates/o01_cp022envelope.blend -P scripts/render_views_ppl33.py -- $R --outdir $OUT/after
if [[ $BEFORE == 1 ]]; then mkdir -p $OUT/before; "$B" -b rounds/o01.blend -P scripts/render_views_ppl33.py -- $R --outdir $OUT/before; fi
echo CP022_ENVELOPE_DONE
