#!/usr/bin/env bash
# CP026 turnstiles LIVE (KEEP scoped 2026-11-13: south entrance frame + Kensington Road elms FT95-FT100, CP026_turnstiles_start ONLY).
# Live blend rounds/h05.blend (= approved candidate rounds/candidates/h03_cp026turnstiles.blend, md5 c1fe13bcb1fb5ffe3b7d606f8bd6973a).
# (Named h05, not h04: rounds/h04.blend is already the live CP027 stair-foot blend, cc938620, and must not be overwritten.)
# Routing: scripts/fitout_live_heroes.json. ONLY CP026_turnstiles_start renders from h05. rounds/h03.blend (md5
# 0a1da8f271d50b3c02f878cd8f7d86e4) is never written and stays live for every other h03 camera: CP026_shilling_ext_start (side
# effect REJECTED: black rectangles on the new door posts at the door-head line, FT99), CP028_watering_start and CP028_louvre_start
# (no visible change). renders/h01/CP026_turnstiles_start.png stays in place as the pre-keep frame.
#   scripts/render_cp026turnstiles_live.sh [--rebuild] [--no-render] [--force] [--blend PATH] [--outdir DIR]
# Recipe (FT100, the live CP026 recipe): render_views_ppl31.py (people_lib v3.1 survey 0dfacfa), look era 1851, tod
# exterior_midday, exposure -0.7, 1920x1080, 48 spp, 8 threads. Output matches
# renders/candidates/cp026_turnstiles_20261113/after/CP026_turnstiles_start.png.
# --rebuild regenerates the blend from live h03 (pre-keep, unchanged) with scripts/cand_cp026_turnstiles_20261113.py, the script
# that built the KEEP candidate (md5 differs per save by metadata only). If h03 is ever rebuilt, follow with this --rebuild or the
# CP026 turnstiles KEEP is lost.
# RESUMABLE (the box is snapshotted/restored about every two hours): an existing --blend is not rebuilt and an existing PNG is not
# re-rendered unless --force; the rebuild and the render go to a scratch dir and are moved in only when complete. Just re-run.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
SRC=rounds/h03.blend
BLEND=rounds/h05.blend
OUTDIR=renders/h05
CAM=CP026_turnstiles_start
REBUILD=0; RENDER=1; FORCE=0
while [[ $# -gt 0 ]]; do case "$1" in
  --rebuild) REBUILD=1;; --no-render) RENDER=0;; --force) FORCE=1;;
  --blend) BLEND="$2"; shift;; --outdir) OUTDIR="$2"; shift;;
esac; shift; done
P31=/workspace/tmp/cp026/ppl31
if [[ ! -f $P31/people_lib.py ]]; then mkdir -p $P31; git -C /workspace/crystal-palace-survey show 0dfacfa:people/people_lib.py > $P31/people_lib.py; ln -sfn /workspace/crystal-palace-survey/people/vendor $P31/vendor; ln -sfn /workspace/crystal-palace-survey/people/v3 $P31/v3; fi
if [[ $REBUILD == 1 ]]; then
  if [[ -f "$BLEND" && $FORCE == 0 ]]; then echo "CP026T_LIVE_SKIP rebuild ($BLEND exists)"; else
    TMP=$(mktemp -d /workspace/tmp/cp026trebuild.XXXXXX); mkdir -p "$TMP/rounds/candidates"   # the build script only writes under */rounds/candidates/
    "$B" -b -P scripts/cand_cp026_turnstiles_20261113.py -- --src "$SRC" --out "$TMP/rounds/candidates/h05_rebuild.blend"
    mv "$TMP/rounds/candidates/h05_rebuild.blend" "$BLEND"
    rm -rf "$TMP"
    echo "CP026T_LIVE_REBUILT: $BLEND"
  fi
fi
if [[ $RENDER == 1 ]]; then
  mkdir -p "$OUTDIR"
  if [[ -f "$OUTDIR/$CAM.png" && $FORCE == 0 ]]; then echo "CP026T_LIVE_SKIP $OUTDIR/$CAM.png (exists)"; else
    S=$(mktemp -d /workspace/tmp/cp026trender.XXXXXX)
    "$B" -b "$BLEND" -P scripts/render_views_ppl31.py -- --cams $CAM --res 1920x1080 --samples 48 --era 1851 --tod exterior_midday --threads 8 --exposure -0.7 --outdir "$S"
    mv "$S/$CAM.png" "$OUTDIR/$CAM.png"; rm -rf "$S"
    echo "CP026T_LIVE_STEP: $OUTDIR/$CAM.png"
  fi
  echo "CP026T_LIVE_DONE: $OUTDIR"
fi
