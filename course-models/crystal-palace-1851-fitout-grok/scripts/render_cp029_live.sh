#!/usr/bin/env bash
# CP029 LIVE (KEEP scoped 2026-11-12: east nave FT81-FT87, CP029_dais_start + CP029_gallery_start). Live blend rounds/c03.blend
# (= approved candidate rounds/candidates/c02_cp029east.blend, md5 0651925dbe74cd2ea0cdb1df334a04fb). Routing:
# scripts/fitout_live_heroes.json. Both CP029 cams render from c03. rounds/c02.blend (md5 c0be5fff332040d906d148fb60c36f35) is
# never written and stays the pre-keep state; its PNGs in renders/c02/ are the pre-keep frames.
#   scripts/render_cp029_live.sh [--rebuild] [--no-render] [--blend PATH] [--outdir DIR]
# Recipe (FT87): render_views.py with people_lib v3.1 via scripts/render_views_ppl31.py, shared look --era 1851 (interior_daylit,
# exposure from the look), 1920x1080, 48 spp, 8 threads. Output matches
# renders/candidates/cp029_east_20261112/after/CP029_{dais,gallery}_start.png pixel for pixel.
# --rebuild regenerates the live c03 from live c02 (pre-keep, unchanged) with scripts/cand_cp029_east_20261112.py, the script that
# built the KEEP candidate (md5 differs per save by metadata only). If c02 is ever rebuilt, follow with this --rebuild or the
# CP029 KEEP is lost.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
SRC=rounds/c02.blend
BLEND=rounds/c03.blend
OUTDIR=renders/c03
REBUILD=0; RENDER=1
while [[ $# -gt 0 ]]; do case "$1" in
  --rebuild) REBUILD=1;; --no-render) RENDER=0;;
  --blend) BLEND="$2"; shift;; --outdir) OUTDIR="$2"; shift;;
esac; shift; done
if [[ $REBUILD == 1 ]]; then
  TMP=$(mktemp -d)
  "$B" -b -P scripts/cand_cp029_east_20261112.py -- --src "$SRC" --out "$TMP/c03_rebuild.blend"
  mv "$TMP/c03_rebuild.blend" "$BLEND"
  rm -rf "$TMP"
fi
if [[ $RENDER == 1 ]]; then
  mkdir -p "$OUTDIR"
  for cam in CP029_dais_start CP029_gallery_start; do
    "$B" -b "$BLEND" -P scripts/render_views_ppl31.py -- --cams "$cam" --res 1920x1080 --samples 48 --era 1851 --threads 8 --outdir "$OUTDIR"
    echo "CP029_LIVE_STEP: $OUTDIR/$cam.png"
  done
  echo "CP029_LIVE_DONE: $OUTDIR"
fi
