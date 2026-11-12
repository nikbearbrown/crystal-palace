#!/usr/bin/env bash
# CP027 LIVE (KEEP scoped 2026-11-12: east nave FT74-FT80, CP027_stair_foot_start ONLY). Live blend rounds/h04.blend (= approved
# candidate rounds/candidates/h01_cp027east.blend, md5 cc9386207f3a063384da6fa14be9de69). Routing: scripts/fitout_live_heroes.json.
# ONLY CP027_stair_foot_start (hero) renders from h04. CP027_gallery_rail_start and every other h01 camera stay on
# rounds/h01.blend (md5 73c09039f67f61267b78ba2735ea81ce, never written): the gallery_rail side effect was REJECTED (only darker,
# its west lawn stays).
#   scripts/render_cp027_live.sh [--rebuild] [--no-render] [--blend PATH] [--outdir DIR]
# Recipe (FT80): render_views.py with people_lib v3.1 via scripts/render_views_ppl31.py, shared look --era 1851 (interior_daylit,
# exposure from the look), 1920x1080, 48 spp, 8 threads. Output matches
# renders/candidates/cp027_east_20261112/after/CP027_stair_foot_start.png pixel for pixel.
# --rebuild regenerates the live h04 from live h01 (pre-keep, unchanged) with scripts/cand_cp027_east_20261112.py, the script that
# built the KEEP candidate (md5 differs per save by metadata only). If h01 is ever rebuilt, follow with this --rebuild or the
# CP027 KEEP is lost.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
SRC=rounds/h01.blend
BLEND=rounds/h04.blend
OUTDIR=renders/h04
REBUILD=0; RENDER=1
while [[ $# -gt 0 ]]; do case "$1" in
  --rebuild) REBUILD=1;; --no-render) RENDER=0;;
  --blend) BLEND="$2"; shift;; --outdir) OUTDIR="$2"; shift;;
esac; shift; done
if [[ $REBUILD == 1 ]]; then
  TMP=$(mktemp -d)
  "$B" -b -P scripts/cand_cp027_east_20261112.py -- --src "$SRC" --out "$TMP/h04_rebuild.blend"
  mv "$TMP/h04_rebuild.blend" "$BLEND"
  rm -rf "$TMP"
fi
if [[ $RENDER == 1 ]]; then
  mkdir -p "$OUTDIR"
  "$B" -b "$BLEND" -P scripts/render_views_ppl31.py -- --cams CP027_stair_foot_start --res 1920x1080 --samples 48 --era 1851 --threads 8 --outdir "$OUTDIR"
  echo "CP027_LIVE_DONE: $OUTDIR/CP027_stair_foot_start.png"
fi
