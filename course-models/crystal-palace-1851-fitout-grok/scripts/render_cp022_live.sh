#!/usr/bin/env bash
# CP022 LIVE (KEEP scoped 2026-11-11: envelope FT67-FT73, CP022 cams only). Live blend rounds/o02.blend (= approved candidate
# rounds/candidates/o01_cp022envelope.blend, md5 2cd47f234db677a644381c65dbe0c86a). Routing: scripts/fitout_live_heroes.json.
# ONLY CP022_fountain_start (hero) and CP022_crossing_start render from o02. CP021 (doors, dais) and every other o01 camera stay
# on rounds/o01.blend (md5 4776f6182fdfc758581eb79ce12d3345, never written): the CP021 side effects were REJECTED (people_lib
# reshuffles the foreground figures, no gain).
#   scripts/render_cp022_live.sh [--rebuild] [--no-render] [--blend PATH] [--outdir DIR]
# Recipe (FT73): render_views.py with people_lib 3.3 (survey d19449b) via scripts/render_views_ppl33.py, --keep-lighting
# (blend exposure -0.7, AgX MHC), 1280x720, 48 spp (= the live o01 hero recipe). Output matches
# renders/candidates/cp022_envelope_20261111/after/CP022_{fountain,crossing}_start.png pixel for pixel.
# --rebuild regenerates the live o02 from live o01 (pre-keep, unchanged) with scripts/cand_cp022_envelope_20261111.py, the script
# that built the KEEP candidate (md5 differs per save by metadata only; renders are max diff 0). o01 itself is rebuilt by
# build_transept.py --state opening; follow that with this --rebuild or the CP022 KEEP is lost.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
SRC=rounds/o01.blend
BLEND=rounds/o02.blend
OUTDIR=renders/o02
P33=/workspace/tmp/cp020/ppl33
if [[ ! -f $P33/people_lib.py ]]; then mkdir -p $P33; git -C /workspace/crystal-palace-survey show d19449b:people/people_lib.py > $P33/people_lib.py; ln -sfn /workspace/crystal-palace-survey/people/vendor $P33/vendor; ln -sfn /workspace/crystal-palace-survey/people/v3 $P33/v3; fi
REBUILD=0; RENDER=1
while [[ $# -gt 0 ]]; do case "$1" in
  --rebuild) REBUILD=1;; --no-render) RENDER=0;;
  --blend) BLEND="$2"; shift;; --outdir) OUTDIR="$2"; shift;;
esac; shift; done
if [[ $REBUILD == 1 ]]; then
  TMP=$(mktemp -d)
  "$B" -b -P scripts/cand_cp022_envelope_20261111.py -- --src "$SRC" --out "$TMP/o02.blend"
  mv "$TMP/o02.blend" "$BLEND"
  rm -rf "$TMP"
fi
if [[ $RENDER == 1 ]]; then
  mkdir -p "$OUTDIR"
  "$B" -b "$BLEND" -P scripts/render_views_ppl33.py -- --cams CP022_fountain_start,CP022_crossing_start --res 1280x720 --samples 48 --keep-lighting --threads 8 --outdir "$OUTDIR"
  echo "CP022_LIVE_DONE: $OUTDIR/CP022_fountain_start.png $OUTDIR/CP022_crossing_start.png"
fi
